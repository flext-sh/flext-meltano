"""FlextMeltano dbt Runner.

dbt execution components following Clean Architecture patterns.
"""

from __future__ import annotations

import asyncio
import subprocess
from typing import TYPE_CHECKING, Any

from flext_core import FlextResult

if TYPE_CHECKING:
    from pathlib import Path


class FlextMeltanoDbtRunner:
    """dbt command execution runner for Meltano integration."""

    def __init__(self, project_path: Path) -> None:
        """Initialize dbt runner."""
        self.project_path = project_path

    async def run_command(
        self,
        command: str,
        *args: str,
    ) -> FlextResult[dict[str, Any]]:
        """Run a dbt command asynchronously."""
        try:
            full_command = ["dbt", command, *args]

            process = await asyncio.create_subprocess_exec(
                *full_command,
                cwd=self.project_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            result = {
                "command": " ".join(full_command),
                "return_code": process.returncode,
                "stdout": stdout.decode(),
                "stderr": stderr.decode(),
                "success": process.returncode == 0,
            }

            if process.returncode == 0:
                return FlextResult.ok(result)
            return FlextResult.fail(f"dbt command failed: {stderr.decode()}")

        except (OSError, subprocess.SubprocessError) as e:
            return FlextResult.fail(f"Failed to run dbt command: {e}")

    async def run_models(self, *models: str) -> FlextResult[dict[str, Any]]:
        """Run specific dbt models."""
        if models:
            return await self.run_command("run", "--models", " ".join(models))
        return await self.run_command("run")

    async def test_models(self, *models: str) -> FlextResult[dict[str, Any]]:
        """Test specific dbt models."""
        if models:
            return await self.run_command("test", "--models", " ".join(models))
        return await self.run_command("test")
