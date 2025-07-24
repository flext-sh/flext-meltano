"""FLEXT Meltano CLI Helpers.

Unified command-line interface helpers for all Meltano ecosystem components.
"""

from __future__ import annotations

import asyncio
import subprocess
from typing import TYPE_CHECKING, Any

from flext_core import FlextConstants, FlextResult

if TYPE_CHECKING:
    from pathlib import Path


async def flext_meltano_run_command(
    command: list[str],
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    cmd_timeout: int = FlextConstants.DEFAULT_TIMEOUT,
) -> FlextResult[dict[str, Any]]:
    """Run command asynchronously with comprehensive error handling.

    Args:
        command: Command and arguments to execute
        cwd: Working directory for command execution
        env: Environment variables
        cmd_timeout: Command timeout in seconds

    Returns:
        FlextResult with command output or error information

    """
    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            cwd=cwd,
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=cmd_timeout,
            )
        except TimeoutError:
            process.kill()
            await process.wait()
            return FlextResult.fail(
                f"Command timed out after {cmd_timeout} seconds: {' '.join(command)}",
            )

        result = {
            "command": " ".join(command),
            "returncode": process.returncode,
            "stdout": stdout.decode("utf-8") if stdout else "",
            "stderr": stderr.decode("utf-8") if stderr else "",
            "success": process.returncode == 0,
        }

        if process.returncode == 0:
            return FlextResult.ok(result)
        return FlextResult.fail(
            f"Command failed with return code {process.returncode}: "
            f"{result['stderr'] or result['stdout']}",
        )

    except Exception as e:
        return FlextResult.fail(f"Failed to execute command: {e}")


def flext_run_meltano_command(
    args: list[str],
    project_root: Path | None = None,
    environment: str | None = None,
) -> FlextResult[dict[str, Any]]:
    """Run Meltano CLI command synchronously.

    Args:
        args: Meltano command arguments
        project_root: Meltano project root directory
        environment: Meltano environment name

    Returns:
        FlextResult with command output

    """
    try:
        command = ["meltano", *args]

        env = {}
        if environment:
            env["MELTANO_ENVIRONMENT"] = environment
        if project_root:
            env["MELTANO_PROJECT_ROOT"] = str(project_root)

        result = subprocess.run(
            command,
            check=False,
            cwd=project_root,
            env=env,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes default
        )

        output = {
            "command": " ".join(command),
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
        }

        if result.returncode == 0:
            return FlextResult.ok(output)
        return FlextResult.fail(
            f"Meltano command failed: {result.stderr or result.stdout}",
        )

    except subprocess.TimeoutExpired:
        return FlextResult.fail("Meltano command timed out")
    except Exception as e:
        return FlextResult.fail(f"Failed to run Meltano command: {e}")


def flext_run_singer_command(
    tap_command: list[str],
    target_command: list[str] | None = None,
    config_file: Path | None = None,
    catalog_file: Path | None = None,
    state_file: Path | None = None,
) -> FlextResult[dict[str, Any]]:
    """Run Singer tap/target pipeline.

    Args:
        tap_command: Tap command to execute
        target_command: Optional target command
        config_file: Tap configuration file
        catalog_file: Singer catalog file
        state_file: State file for incremental extraction

    Returns:
        FlextResult with pipeline execution results

    """
    try:
        # Build tap command with configuration
        full_tap_command = tap_command.copy()

        if config_file and config_file.exists():
            full_tap_command.extend(["--config", str(config_file)])
        if catalog_file and catalog_file.exists():
            full_tap_command.extend(["--catalog", str(catalog_file)])
        if state_file and state_file.exists():
            full_tap_command.extend(["--state", str(state_file)])

        if target_command:
            # Run tap | target pipeline
            tap_process = subprocess.Popen(
                full_tap_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            target_process = subprocess.Popen(
                target_command,
                stdin=tap_process.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            tap_process.stdout.close()  # type: ignore[union-attr]
            target_stdout, target_stderr = target_process.communicate()
            tap_stderr = tap_process.stderr.read()  # type: ignore[union-attr]

            result = {
                "tap_command": " ".join(full_tap_command),
                "target_command": " ".join(target_command),
                "tap_returncode": tap_process.returncode,
                "target_returncode": target_process.returncode,
                "target_stdout": target_stdout,
                "target_stderr": target_stderr,
                "tap_stderr": tap_stderr,
                "success": (
                    tap_process.returncode == 0 and target_process.returncode == 0
                ),
            }
        else:
            # Run tap only
            tap_result = subprocess.run(
                full_tap_command,
                check=False,
                capture_output=True,
                text=True,
                timeout=1800,  # 30 minutes
            )

            result = {
                "tap_command": " ".join(full_tap_command),
                "tap_returncode": tap_result.returncode,
                "tap_stdout": tap_result.stdout,
                "tap_stderr": tap_result.stderr,
                "success": tap_result.returncode == 0,
            }

        if result["success"]:
            return FlextResult.ok(result)
        return FlextResult.fail("Singer pipeline failed")

    except Exception as e:
        return FlextResult.fail(f"Failed to run Singer pipeline: {e}")


def flext_run_dbt_command(
    command: list[str],
    project_dir: Path,
    profiles_dir: Path | None = None,
    target: str | None = None,
) -> FlextResult[dict[str, Any]]:
    """Run dbt command.

    Args:
        command: dbt command and arguments
        project_dir: dbt project directory
        profiles_dir: dbt profiles directory
        target: dbt target name

    Returns:
        FlextResult with dbt command output

    """
    try:
        full_command = ["dbt", *command]

        if profiles_dir:
            full_command.extend(["--profiles-dir", str(profiles_dir)])
        if target:
            full_command.extend(["--target", target])

        result = subprocess.run(
            full_command,
            check=False,
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=1800,  # 30 minutes
        )

        output = {
            "command": " ".join(full_command),
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
        }

        if result.returncode == 0:
            return FlextResult.ok(output)
        return FlextResult.fail(f"dbt command failed: {result.stderr or result.stdout}")

    except subprocess.TimeoutExpired:
        return FlextResult.fail("dbt command timed out")
    except Exception as e:
        return FlextResult.fail(f"Failed to run dbt command: {e}")
