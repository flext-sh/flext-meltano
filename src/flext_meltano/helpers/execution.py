"""FLEXT Meltano execution helpers - ISOLADOS sem dependências externas.

Helpers simples para execução de jobs Meltano via subprocess.
BIBLIOTECA ISOLADA - não importa flext_core.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


class FlextMeltanoResult:
    """Local result type para evitar dependência flext_core."""

    def __init__(self, *, success: bool, data: dict[str, Any] | None = None, error: str = "") -> None:
        """Initialize FlextMeltanoResult.

        Args:
            success: Whether the operation was successful
            data: Operation result data
            error: Error message if operation failed
        """
        self.success = success
        self.data = data
        self.error = error

    @classmethod
    def ok(cls, data: dict[str, Any] | None = None) -> FlextMeltanoResult:
        """Create success result."""
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str) -> FlextMeltanoResult:
        """Create failure result."""
        return cls(success=False, error=error)


def flext_meltano_execute_job(
    tap_name: str,
    target_name: str,
    project_root: str | Path = ".",
    environment: str = "dev",
) -> FlextMeltanoResult:
    """Execute Meltano pipeline job.

    Args:
        tap_name: Source tap plugin name
        target_name: Target loader plugin name
        project_root: Meltano project directory
        environment: Meltano environment

    Returns:
        Result with execution status and output
    """
    try:
        project_path = Path(project_root)

        # Find meltano executable
        meltano_path = project_path / ".venv" / "bin" / "meltano"
        if not meltano_path.exists():
            meltano_cmd = shutil.which("meltano")
            if not meltano_cmd:
                return FlextMeltanoResult.fail("Meltano CLI not found")
            meltano_path = Path(meltano_cmd)

        # Build command
        command = [
            str(meltano_path),
            "run",
            tap_name,
            target_name,
        ]

        # Set environment - inherit system PATH and add Meltano environment
        env = {**os.environ, "MELTANO_ENVIRONMENT": environment}

        # Execute - command is trusted as it's built from known meltano path + user args
        result = subprocess.run(  # noqa: S603
            command,
            check=False, cwd=project_path,
            env=env,
            capture_output=True,
            text=True,
            timeout=1800,  # 30 minutes
        )

        output = {
            "command": " ".join(command),
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
        }

        if result.returncode == 0:
            return FlextMeltanoResult.ok(output)
        return FlextMeltanoResult.fail(f"Pipeline failed: {result.stderr or result.stdout}")

    except subprocess.TimeoutExpired:
        return FlextMeltanoResult.fail("Pipeline execution timed out")
    except (ValueError, TypeError, RuntimeError, OSError) as e:
        return FlextMeltanoResult.fail(f"Execution error: {e!s}")


def flext_meltano_run_command(
    args: list[str],
    project_root: str | Path = ".",
    environment: str = "dev",
) -> FlextMeltanoResult:
    """Run generic Meltano command.

    Args:
        args: Meltano command arguments
        project_root: Project directory
        environment: Meltano environment

    Returns:
        Result with command output
    """
    try:
        project_path = Path(project_root)

        # Find meltano executable
        meltano_path = project_path / ".venv" / "bin" / "meltano"
        if not meltano_path.exists():
            meltano_cmd = shutil.which("meltano")
            if not meltano_cmd:
                return FlextMeltanoResult.fail("Meltano CLI not found")
            meltano_path = Path(meltano_cmd)

        # Build command
        command = [str(meltano_path), *args]

        # Set environment - inherit system PATH and add Meltano environment
        env = {**os.environ, "MELTANO_ENVIRONMENT": environment}

        # Execute - command is trusted as it's built from known meltano path + user args
        result = subprocess.run(  # noqa: S603
            command,
            check=False, cwd=project_path,
            env=env,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes
        )

        output = {
            "command": " ".join(command),
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
        }

        if result.returncode == 0:
            return FlextMeltanoResult.ok(output)
        return FlextMeltanoResult.fail(f"Command failed: {result.stderr or result.stdout}")

    except subprocess.TimeoutExpired:
        return FlextMeltanoResult.fail("Command timed out")
    except (ValueError, TypeError, RuntimeError, OSError) as e:
        return FlextMeltanoResult.fail(f"Command error: {e!s}")
