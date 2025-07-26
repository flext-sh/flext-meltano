"""Execution utilities for flext-meltano.

Clean execution using flext-core patterns.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from flext_core import FlextCommonResult

from flext_meltano.constants import FlextMeltanoConstants


class FlextMeltanoResult(FlextCommonResult):
    """Extensão de FlextResult para Meltano, sem lógica extra."""


def flext_meltano_execute_job(
    job_name: str,
    project_root: str = ".",
    environment: str = "dev",
) -> FlextMeltanoResult[dict[str, Any]]:
    """Execute a Meltano job.

    Args:
        job_name: Name of the job to execute
        project_root: Path to Meltano project root
        environment: Environment to run in

    Returns:
        FlextMeltanoResult containing execution result

    """
    try:
        project_path = Path(project_root)
        meltano_yml = project_path / "meltano.yml"

        if not meltano_yml.exists():
            return FlextMeltanoResult.fail(f"No meltano.yml found in {project_root}")

        cmd = [
            "meltano",
            "run",
            job_name,
        ]

        if environment != "dev":
            cmd.extend(["--environment", environment])

        result = subprocess.run(
            cmd,
            check=False,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=FlextMeltanoConstants.PIPELINE_TIMEOUT,
        )

        if result.returncode == 0:
            return FlextMeltanoResult.ok(
                {
                    "job_name": job_name,
                    "environment": environment,
                    "output": result.stdout,
                    "success": True,
                },
            )
        return FlextMeltanoResult.fail(
            result.stderr or f"Job {job_name} execution failed",
        )

    except subprocess.TimeoutExpired:
        return FlextMeltanoResult.fail(f"Job {job_name} execution timed out")
    except Exception as e:
        return FlextMeltanoResult.fail(f"Job {job_name} execution failed: {e}")


def flext_meltano_run_command(
    command: str,
    project_root: str = ".",
    args: list[str] | None = None,
) -> FlextMeltanoResult[dict[str, Any]]:
    """Run a Meltano command.

    Args:
        command: Meltano command to run
        project_root: Path to Meltano project root
        args: Additional command arguments

    Returns:
        FlextMeltanoResult containing command result

    """
    try:
        project_path = Path(project_root)
        meltano_yml = project_path / "meltano.yml"

        if not meltano_yml.exists():
            return FlextMeltanoResult.fail(f"No meltano.yml found in {project_root}")

        cmd = ["meltano", command]
        if args:
            cmd.extend(args)

        result = subprocess.run(
            cmd,
            check=False,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=FlextMeltanoConstants.COMMAND_TIMEOUT,
        )

        if result.returncode == 0:
            return FlextMeltanoResult.ok(
                {
                    "command": command,
                    "args": args or [],
                    "output": result.stdout,
                    "success": True,
                },
            )
        return FlextMeltanoResult.fail(
            result.stderr or f"Command {command} failed",
        )

    except subprocess.TimeoutExpired:
        return FlextMeltanoResult.fail(f"Command {command} timed out")
    except Exception as e:
        return FlextMeltanoResult.fail(f"Command {command} failed: {e}")


__all__ = [
    "FlextMeltanoResult",
    "flext_meltano_execute_job",
    "flext_meltano_run_command",
]
