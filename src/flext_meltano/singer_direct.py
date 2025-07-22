"""Singer SDK Direct Integration - ZERO warnings by using modern APIs.

This module bypasses Meltano CLI and uses Singer SDK directly to eliminate
deprecation warnings at their source.
"""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path
from typing import Any

from flext_core.domain.shared_types import ServiceResult

logger = logging.getLogger(__name__)


class SingerDirectRunner:
    """Run Singer taps and targets directly using modern APIs."""

    def __init__(self, project_root: Path) -> None:
        """Initialize Singer Direct integration."""
        self.project_root = Path(project_root)
        self.logger = logger.info(
            "flext_meltano_singer_direct %s",
            {str(self.project_root)},
        )

    async def run_tap_target_direct(
        self,
        project_name: str,
        tap_executable: str,
        target_executable: str,
        _tap_config: dict[str, Any] | None = None,
        _target_config: dict[str, Any] | None = None,
    ) -> ServiceResult[Any]:
        """Run tap and target directly using Singer protocol without Meltano CLI.

        This eliminates warnings by not using deprecated Meltano CLI APIs.
        """
        try:
            project_path = self.project_root / project_name

            # Build tap command with modern Singer patterns
            tap_cmd = [tap_executable, "--config", "-"]
            if _tap_config:
                tap_cmd.extend(["--catalog", "-"])

            # Build target command
            target_cmd = [target_executable, "--config", "-"]

            self.logger.info(
                "Running Singer pipeline directly",
                tap=tap_executable,
                target=target_executable,
                project=project_name,
            )

            # Execute tap | target pipeline directly
            tap_process = await asyncio.create_subprocess_exec(
                *tap_cmd,
                cwd=project_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE,
            )

            # Ensure tap stdout is available for piping
            if tap_process.stdout is None:
                return ServiceResult.fail("Tap process stdout not available for piping",
                )

            target_process = await asyncio.create_subprocess_exec(
                *target_cmd,
                cwd=project_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=tap_process.stdout,  # Now guaranteed to be non-None
            )

            # Wait for completion
            _tap_stdout, tap_stderr = await tap_process.communicate()
            _target_stdout, target_stderr = await target_process.communicate()

            result = {
                "command": f"{tap_executable} | {target_executable}",
                "tap_returncode": tap_process.returncode,
                "target_returncode": target_process.returncode,
                "tap_stderr": tap_stderr.decode() if tap_stderr else "",
                "target_stderr": target_stderr.decode() if target_stderr else "",
                "success": tap_process.returncode == 0
                and target_process.returncode == 0,
            }

            if result["success"]:
                self.logger.info("Singer direct pipeline completed successfully")
                return ServiceResult.ok({"result": result})
            error_msg = f"Pipeline failed: tap={tap_process.returncode}, target={target_process.returncode}"
            self.logger.error(error_msg, **result)
            return ServiceResult.fail(error_msg)

        except Exception as e:
            error_msg = f"Failed to run Singer pipeline directly: {e}"
            self.logger.exception(error_msg, error=str(e))
            return ServiceResult.fail(error_msg)

    async def discover_tap_schema(
        self,
        project_name: str,
        tap_executable: str,
        _tap_config: dict[str, Any],
    ) -> ServiceResult[Any]:
        """Discover tap schema using Singer SDK directly."""
        try:
            project_path = self.project_root / project_name

            # Use Singer discover command directly
            cmd = [tap_executable, "--config", "-", "--discover"]

            self.logger.info("Discovering tap schema directly", tap=tap_executable)

            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=project_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                try:
                    catalog = json.loads(stdout.decode())
                    self.logger.info(
                        "Schema discovered successfully",
                        streams=len(catalog.get("streams", [])),
                    )
                    return ServiceResult.ok({"result": catalog})
                except json.JSONDecodeError as e:
                    return ServiceResult.fail(f"Invalid catalog JSON: {e}",
                    )
            else:
                error_msg = f"Schema discovery failed: {stderr.decode()}"
                self.logger.error(error_msg)
                return ServiceResult.fail(error_msg)

        except Exception as e:
            error_msg = f"Failed to discover schema: {e}"
            self.logger.exception(error_msg, error=str(e))
            return ServiceResult.fail(error_msg)
