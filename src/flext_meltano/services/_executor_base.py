"""FLEXT Meltano Executor - Base class with core command execution.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import override

from flext_core import r

from flext_meltano import (
    FlextMeltanoCLI,
    FlextMeltanoServiceBase,
    c,
    m,
    t,
    u,
)


class _FlextMeltanoExecutorBase(FlextMeltanoServiceBase):
    """Base executor providing Meltano command execution with error handling."""

    service_name: str = "FlextMeltanoExecutor"

    @property
    def project_root(self) -> Path:
        """Get project root directory - delegates to settings."""
        project_root = getattr(self.settings, "project_root", None)
        if project_root is not None:
            return m.Meltano.PathPayload(value=project_root).value
        return Path.cwd()

    @staticmethod
    def create_flext_cli() -> r[FlextMeltanoCLI]:
        """Create FLEXT CLI instance - delegates to CLI module."""
        try:
            cli = FlextMeltanoCLI()
            return r[FlextMeltanoCLI].ok(cli)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[FlextMeltanoCLI].fail(f"Failed to create CLI: {e}")

    @staticmethod
    def get_version() -> r[str]:
        """Get version information from Meltano CLI."""
        try:
            proc = subprocess.run(
                ["meltano", "version"],  # noqa: S607
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            version = (
                proc.stdout.strip()
                if proc.returncode == 0
                else c.Meltano.Defaults.SERVICE_VERSION
            )
            return r[str].ok(version)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[str].fail(f"Failed to get version: {e}")

    @override
    def execute(self) -> r[t.Meltano.ExecutionResultDict]:
        """Execute the Meltano executor service."""
        try:
            config_data: t.Meltano.ExecutionResultDict = {
                "executor_type": "flext_meltano_executor",
                "status": c.Meltano.Enums.OperationStatus.READY,
                "execution_timestamp": str(time.time()),
                "config": self.settings.model_dump()
                if u.is_pydantic_model(self.settings)
                else dict[str, t.NormalizedValue](),
            }
            self.logger.info("FlextMeltanoExecutor executed successfully")
            return r[t.Meltano.ExecutionResultDict].ok(config_data)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Executor execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.Meltano.ExecutionResultDict].fail(error_msg)

    def execute_meltano_command(
        self,
        command: t.StrSequence,
        timeout: int = c.Meltano.Network.MELTANO_DEFAULT_TIMEOUT,
        _cwd: Path | None = None,
    ) -> r[m.Meltano.CommandExecutionResult]:
        """Execute a Meltano command with timeout and error handling."""
        try:
            start_time = time.time()
            cwd = str(self.project_root) if _cwd is None else str(_cwd)
            self.logger.info(
                "Executing command",
                command=str(command),
                timeout=timeout,
                cwd=cwd,
            )
            proc = subprocess.run(
                list(command),
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                check=False,
            )
            execution_time = time.time() - start_time
            result = m.Meltano.CommandExecutionResult(
                command=command,
                success=proc.returncode == 0,
                exit_code=proc.returncode,
                output=proc.stdout,
                error=proc.stderr,
                execution_time=execution_time,
            )
            return r[m.Meltano.CommandExecutionResult].ok(result)
        except subprocess.TimeoutExpired as e:
            error_msg = f"Command timed out after {timeout}s: {e}"
            self.logger.exception(error_msg)
            return r[m.Meltano.CommandExecutionResult].fail(error_msg)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Command execution failed: {e}"
            self.logger.exception(error_msg)
            return r[m.Meltano.CommandExecutionResult].fail(error_msg)

    def execute_dbt_command(
        self,
        dbt_command: str,
        args: t.StrSequence | None = None,
    ) -> r[m.Meltano.CommandExecutionResult]:
        """Execute a DBT command."""
        try:
            command: list[str] = ["dbt", dbt_command]
            if args:
                command.extend(args)
            return self.execute_meltano_command(command)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[m.Meltano.CommandExecutionResult].fail(f"DBT command failed: {e}")

    def execute_pipeline(
        self,
        tap_name: str,
        target_name: str,
        _config: t.Meltano.MeltanoConfigDict | None = None,
    ) -> r[m.Meltano.CommandExecutionResult]:
        """Execute a complete ELT pipeline."""
        try:
            command: list[str] = ["meltano", "run", tap_name, target_name]
            return self.execute_meltano_command(command)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[m.Meltano.CommandExecutionResult].fail(
                f"Pipeline execution failed: {e}",
            )
