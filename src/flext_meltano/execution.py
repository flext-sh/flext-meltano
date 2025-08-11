"""FLEXT Meltano Execution - Core Subprocess Orchestration."""

from __future__ import annotations

import os
import shutil
import subprocess
import time
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

# FlextResult is MANDATORY for all operations
from flext_core import FlextModel, FlextResult, get_logger

# Observability integration - using flext_core logger instead of flext_observability
from pydantic import Field

# Injectable decorator from common utilities
from flext_meltano.common import injectable

if TYPE_CHECKING:
    from flext_meltano.config import FlextMeltanoConfig

logger = get_logger(__name__)


class FlextMeltanoExecutionCommand:
    """Command for execution."""

    def __init__(self, tap_name: str, target_name: str) -> None:
        """Initialize execution command."""
        self.tap_name = tap_name
        self.target_name = target_name


class FlextMeltanoExecutionContext(FlextModel):
    """Execution context for pipeline operations."""

    execution_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pipeline_name: str = Field(...)
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    environment: str = Field(default="dev")
    project_root: Path = Field(default_factory=Path)
    timeout_seconds: int = Field(default=1800)
    metadata: dict[str, object] = Field(default_factory=dict)


@injectable
class FlextMeltanoExecutor:
    """Pipeline executor using MANDATORY patterns."""

    def __init__(self, config: FlextMeltanoConfig) -> None:
        """Initialize with dependency injection."""
        self.config = config
        self._initialized = False
        self._meltano_path: Path | None = None
        self.logger = get_logger(self.__class__.__name__)

    def initialize(self) -> FlextResult[bool]:
        """Initialize service."""
        try:
            validation_result = self.validate()
            if not validation_result.success:
                return validation_result
            self._initialized = True
            return FlextResult(data=True)
        except (ValueError, TypeError, ImportError) as e:
            return FlextResult(error=f"Service initialization failed: {e}")

    def validate(self) -> FlextResult[bool]:
        """Validate execution service."""
        try:
            meltano_path = self._find_meltano_executable()
            if not meltano_path:
                return FlextResult(error="Meltano CLI not found")

            self._meltano_path = meltano_path
            return FlextResult(data=True)
        except (OSError, ImportError) as e:
            return FlextResult(error=f"Validation failed: {e}")

    def get_health_status(self) -> FlextResult[dict[str, object]]:
        """Get executor health status."""
        return FlextResult(
            data={
                "service": "execution",
                "meltano_available": self._meltano_path is not None,
                "initialized": self._initialized,
            },
        )

    def _find_meltano_executable(self) -> Path | None:
        """Find Meltano executable."""
        project_path = Path(self.config.project_root)

        # Check workspace venv first (real location)
        workspace_venv_meltano = Path("/home/marlonsc/flext/.venv/bin/meltano")
        if workspace_venv_meltano.exists():
            return workspace_venv_meltano

        # Check project-local venv
        venv_meltano = project_path / ".venv" / "bin" / "meltano"
        if venv_meltano.exists():
            return venv_meltano

        # Check system PATH
        system_meltano = shutil.which("meltano")
        if system_meltano:
            return Path(system_meltano)

        return None

    def execute_pipeline(
        self,
        tap_name: str,
        target_name: str,
        context: FlextMeltanoExecutionContext | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Execute pipeline using enterprise patterns."""
        if not context:
            context = FlextMeltanoExecutionContext(
                pipeline_name=f"{tap_name}-{target_name}",
                environment=self.config.environment,
                project_root=Path(self.config.project_root),
            )

        try:
            if not self._meltano_path:
                validation_result = self.validate()
                if not validation_result.success:
                    return FlextResult(error=validation_result.error)

            # Build command
            command = [
                str(self._meltano_path),
                "run",
                tap_name,
                target_name,
            ]

            # Set environment
            env = {**os.environ, "MELTANO_ENVIRONMENT": context.environment}

            # Execute subprocess
            result = subprocess.run(  # noqa: S603  # noqa: S603
                command,
                check=False,
                cwd=context.project_root,
                env=env,
                capture_output=True,
                text=True,
                timeout=context.timeout_seconds,
            )

            execution_result = {
                "execution_id": context.execution_id,
                "pipeline_name": context.pipeline_name,
                "command": " ".join(command),
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
                "started_at": context.started_at.isoformat(),
                "completed_at": datetime.now(UTC).isoformat(),
                "duration_seconds": (
                    datetime.now(UTC) - context.started_at
                ).total_seconds(),
            }

            if result.returncode == 0:
                return FlextResult(data=execution_result)
            return FlextResult(
                error=f"Pipeline failed: {result.stderr or result.stdout}",
            )

        except subprocess.TimeoutExpired:
            return FlextResult(error="Pipeline execution timed out")
        except (OSError, subprocess.CalledProcessError) as e:
            return FlextResult(error=f"Execution error: {e}")

    def run_command(
        self,
        args: list[str],
        context: FlextMeltanoExecutionContext | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Run generic command using enterprise patterns."""
        if not context:
            context = FlextMeltanoExecutionContext(
                pipeline_name="meltano-command",
                environment=self.config.environment,
                project_root=Path(self.config.project_root),
                timeout_seconds=300,  # 5 minutes for generic commands
            )

        try:
            if not self._meltano_path:
                validation_result = self.validate()
                if not validation_result.success:
                    return FlextResult(error=validation_result.error)

            # Build command
            command = [str(self._meltano_path), *args]

            # Set environment
            env = {**os.environ, "MELTANO_ENVIRONMENT": context.environment}

            # Execute subprocess
            result = subprocess.run(  # noqa: S603  # noqa: S603
                command,
                check=False,
                cwd=context.project_root,
                env=env,
                capture_output=True,
                text=True,
                timeout=context.timeout_seconds,
            )

            execution_result = {
                "execution_id": context.execution_id,
                "command": " ".join(command),
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
                "started_at": context.started_at.isoformat(),
                "completed_at": datetime.now(UTC).isoformat(),
                "duration_seconds": (
                    datetime.now(UTC) - context.started_at
                ).total_seconds(),
            }

            if result.returncode == 0:
                return FlextResult(data=execution_result)
            return FlextResult(
                error=f"Command failed: {result.stderr or result.stdout}",
            )

        except subprocess.TimeoutExpired:
            return FlextResult(error="Command timed out")
        except (OSError, subprocess.CalledProcessError) as e:
            return FlextResult(error=f"Command error: {e}")

    def execute(
        self,
        command: FlextMeltanoExecutionCommand,
    ) -> FlextResult[dict[str, object]]:
        """Execute command using domain service pattern."""
        return self.execute_pipeline(command.tap_name, command.target_name)


def create_executor(config: FlextMeltanoConfig) -> FlextResult[FlextMeltanoExecutor]:
    """Create executor using dependency injection."""
    try:
        service = FlextMeltanoExecutor(config)
        init_result = service.initialize()
        if not init_result.success:
            return FlextResult(
                error=f"Executor initialization failed: {init_result.error}",
            )

        return FlextResult(data=service)
    except (ValueError, TypeError, ImportError) as e:
        return FlextResult(error=f"Failed to create executor: {e}")


# === COMMON SUBPROCESS EXECUTOR ===


@dataclass
class SubprocessExecutionContext:
    """Context for centralized subprocess execution."""

    command: list[str]
    cwd: Path | None = None
    env: dict[str, str] | None = None
    timeout_seconds: int = 300
    capture_output: bool = True
    text: bool = True
    check: bool = False


def execute_subprocess_common(
    context: SubprocessExecutionContext,
) -> FlextResult[dict[str, object]]:
    """Centralized subprocess execution with integrated observability.

    This function provides a common pattern for subprocess execution used
    throughout the FLEXT Meltano ecosystem, ensuring consistent error handling,
    result formatting, and comprehensive observability integration.

    Args:
        context: Subprocess execution context with command and options

    Returns:
        FlextResult with execution details including stdout, stderr, returncode

    """
    start_time = time.time()
    command_str = " ".join(context.command)

    # Log subprocess execution start
    logger.info(f"Starting subprocess execution: {command_str}")

    try:
        # Set up environment
        exec_env = dict(os.environ)
        if context.env:
            exec_env.update(context.env)

        # Execute subprocess with enhanced monitoring
        result = subprocess.run(  # noqa: S603
            context.command,
            cwd=context.cwd,
            env=exec_env,
            capture_output=context.capture_output,
            text=context.text,
            timeout=context.timeout_seconds,
            check=context.check,
        )

        # Calculate execution metrics
        execution_time = time.time() - start_time
        success = result.returncode == 0

        # Enhanced result with execution metrics
        execution_result = {
            "command": command_str,
            "returncode": result.returncode,
            "stdout": result.stdout or "",
            "stderr": result.stderr or "",
            "success": success,
            "execution_time": execution_time,
            "cwd": str(context.cwd) if context.cwd else str(Path.cwd()),
            "timeout_seconds": context.timeout_seconds,
        }

        # Log execution completion
        logger.info(f"Subprocess completed in {execution_time:.2f}s: {success}")

        return FlextResult(data=execution_result)

    except subprocess.TimeoutExpired as e:
        execution_time = time.time() - start_time
        logger.exception(
            f"Subprocess timed out after {execution_time:.2f}s: {command_str}",
        )
        return FlextResult(
            error=f"Command timed out after {context.timeout_seconds} seconds: {e}",
        )
    except (subprocess.CalledProcessError, OSError, FileNotFoundError) as e:
        execution_time = time.time() - start_time
        logger.exception(
            f"Subprocess failed after {execution_time:.2f}s: {command_str}",
        )
        return FlextResult(error=f"Command error: {e}")


# === LEGACY COMPATIBILITY ===
# Legacy functions have been moved to legacy.py for backward compatibility.
# Import them here for re-export to maintain existing API.

