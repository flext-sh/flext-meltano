"""Meltano execution using mandatory enterprise patterns.

Pipeline execution via subprocess with enterprise patterns.
Uses mandatory flext-core patterns for consistency.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import uuid
import warnings
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# FlextResult is MANDATORY for all operations
from flext_core import FlextLogger, FlextResult
from injectable import injectable
from pydantic import BaseModel, Field

from flext_meltano.base import FlextMeltanoConfig


class FlextMeltanoExecutionCommand:
    """Command for execution."""

    def __init__(self, tap_name: str, target_name: str) -> None:
        """Initialize execution command."""
        self.tap_name = tap_name
        self.target_name = target_name


class FlextMeltanoExecutionContext(BaseModel):
    """Execution context for pipeline operations."""

    execution_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pipeline_name: str = Field(...)
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    environment: str = Field(default="dev")
    project_root: Path = Field(default_factory=Path)
    timeout_seconds: int = Field(default=1800)
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic configuration."""

        arbitrary_types_allowed = True


@injectable
class FlextMeltanoExecutor:
    """Pipeline executor using MANDATORY patterns."""

    def __init__(self, config: FlextMeltanoConfig) -> None:
        """Initialize with dependency injection."""
        self.config = config
        self._initialized = False
        self._meltano_path: Path | None = None
        self.logger = FlextLogger.get_logger(self.__class__.__name__)

    def initialize(self) -> FlextResult[bool]:
        """Initialize service."""
        try:
            validation_result = self.validate()
            if not validation_result.is_success:
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

    def get_health_status(self) -> FlextResult[dict[str, Any]]:
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

        # Check project-local venv first
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
    ) -> FlextResult[dict[str, Any]]:
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
                if not validation_result.is_success:
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
            result = subprocess.run(  # noqa: S603
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
    ) -> FlextResult[dict[str, Any]]:
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
                if not validation_result.is_success:
                    return FlextResult(error=validation_result.error)

            # Build command
            command = [str(self._meltano_path), *args]

            # Set environment
            env = {**os.environ, "MELTANO_ENVIRONMENT": context.environment}

            # Execute subprocess
            result = subprocess.run(  # noqa: S603
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
    ) -> FlextResult[dict[str, Any]]:
        """Execute command using domain service pattern."""
        return self.execute_pipeline(command.tap_name, command.target_name)


def create_executor(config: FlextMeltanoConfig) -> FlextResult[FlextMeltanoExecutor]:
    """Create executor using dependency injection."""
    try:
        service = FlextMeltanoExecutor(config)
        init_result = service.initialize()
        if not init_result.is_success:
            return FlextResult(
                error=f"Executor initialization failed: {init_result.error}",
            )

        return FlextResult(data=service)
    except (ValueError, TypeError, ImportError) as e:
        return FlextResult(error=f"Failed to create executor: {e}")


# === LEGACY COMPATIBILITY ===


class FlextMeltanoResult:
    """Legacy result type for backward compatibility."""

    def __init__(
        self,
        *,
        success: bool,
        data: dict[str, Any] | None = None,
        error: str = "",
    ) -> None:
        """Initialize result."""
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
    """Execute pipeline job (legacy compatibility)."""
    warnings.warn(
        "flext_meltano_execute_job is deprecated. Use FlextMeltanoExecutor.execute_pipeline instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    config = FlextMeltanoConfig(
        project_root=str(project_root),
        environment=environment,
    )
    executor = FlextMeltanoExecutor(config)

    result = executor.execute_pipeline(tap_name, target_name)
    if result.is_success:
        return FlextMeltanoResult.ok(result.data)
    return FlextMeltanoResult.fail(result.error or "Execution failed")


def flext_meltano_run_command(
    args: list[str],
    project_root: str | Path = ".",
    environment: str = "dev",
) -> FlextMeltanoResult:
    """Run generic command (legacy compatibility)."""
    warnings.warn(
        "flext_meltano_run_command is deprecated. Use FlextMeltanoExecutor.run_command instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    config = FlextMeltanoConfig(
        project_root=str(project_root),
        environment=environment,
    )
    executor = FlextMeltanoExecutor(config)

    result = executor.run_command(args)
    if result.is_success:
        return FlextMeltanoResult.ok(result.data)
    return FlextMeltanoResult.fail(result.error or "Execution failed")
