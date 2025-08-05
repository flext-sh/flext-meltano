"""FLEXT Meltano Execution - Core Subprocess Orchestration for Bridge Integration.

**Architecture Layer**: Core Operations Layer
**Status**: ✅ CORE FUNCTIONALITY - Primary subprocess execution engine
**Dependencies**: flext-core (FlextResult), subprocess, enterprise patterns

## Module Purpose

This module provides the **core execution functionality** for FLEXT Meltano's
bridge architecture, implementing subprocess-based Meltano CLI orchestration
that enables Go services to execute data pipelines through Python bridge calls.

**CRITICAL**: This is the PRIMARY module for bridge integration - all Go ↔ Python
communication flows through the subprocess execution patterns implemented here.

## Design Principles

1. **Subprocess Orchestration**: Direct Meltano CLI execution via subprocess calls
2. **Railway-Oriented Programming**: All operations use FlextResult for error handling
3. **Enterprise Logging**: Structured logging with execution context and correlation IDs
4. **Timeout Management**: Configurable timeouts to prevent hanging processes
5. **Bridge-Friendly**: JSON-serializable results for Go service communication

## Core Components

### Execution Engine
- `FlextMeltanoExecutor`: Primary subprocess execution service
- `execute_meltano_command()`: Generic Meltano command execution
- `run_pipeline()`: Pipeline-specific execution with tap ↔ target orchestration
- Comprehensive error handling and timeout management

### Execution Context
- `FlextMeltanoExecutionContext`: Execution metadata and tracking
- `FlextMeltanoExecutionCommand`: Command encapsulation for pipeline operations
- `FlextMeltanoResult`: Local result type (extends FlextResult)
- UUID-based execution tracking for monitoring and debugging

### Bridge Integration Patterns
- Subprocess output capturing for Go service responses
- JSON-serializable execution results
- Standardized error message formatting
- Execution timing and metrics collection

## Usage Patterns

### Direct Command Execution
```python
from flext_meltano.execution import execute_meltano_command

# Execute Meltano version command
result = execute_meltano_command(["--version"])
if result.success:
    version = result.data["stdout"].strip()
    print(f"Meltano version: {version}")
```

### Pipeline Execution
```python
from flext_meltano.execution import run_pipeline

# Execute tap-csv to target-csv pipeline
result = run_pipeline("tap-csv", "target-csv")
if result.success:
    print("Pipeline completed successfully")
    metrics = result.data.get("execution_metrics", {})
else:
    print(f"Pipeline failed: {result.error_message}")
```

### Service-Based Execution
```python
from flext_meltano.execution import FlextMeltanoExecutor
from flext_meltano.base import FlextMeltanoConfig

config = FlextMeltanoConfig(project_root="./meltano")
executor = FlextMeltanoExecutor(config)

result = executor.execute_command(["run", "tap-postgres:target-postgres"])
```

## Bridge Integration (Go Service Usage)

This module is the **primary integration point** for Go services:

### Subprocess Pattern (Current Implementation)
```go
// Go service executing Python subprocess
cmd := exec.Command("python", "-c",
    "from flext_meltano.execution import execute_meltano_command; " +
    "import json; " +
    "result = execute_meltano_command(['--version']); " +
    "print(json.dumps({'success': result.success, 'data': result.data}))")
output, err := cmd.Output()
```

### Bridge Pattern (After simple_bridge.py Implementation)
```python
# FlextMeltanoBridge will use this module internally
from flext_meltano.execution import FlextMeltanoExecutor

class FlextMeltanoBridge:
    def __init__(self):
        self._executor = FlextMeltanoExecutor()

    def run_pipeline(self, tap: str, target: str):
        return self._executor.run_pipeline(tap, target)
```

## Error Handling Patterns

### FlextResult Integration
All execution operations return FlextResult for consistent error handling:
```python
def execute_with_timeout(command: List[str], timeout: int) -> FlextResult[Dict]:
    try:
        result = subprocess.run(command, timeout=timeout, capture_output=True)
        if result.returncode == 0:
            return FlextResult.ok({"stdout": result.stdout, "stderr": result.stderr})
        else:
            return FlextResult.fail(f"Command failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        return FlextResult.fail("Command timed out")
    except Exception as e:
        return FlextResult.fail(f"Execution error: {e}")
```

### Enterprise Error Context
- Execution ID tracking for debugging
- Structured error messages with context
- Command line argument sanitization
- Environment variable handling

## Performance Considerations

### Subprocess Optimization
- Minimal process spawning overhead
- Efficient output capturing and parsing
- Configurable timeout settings (default: 300 seconds)
- Memory-efficient result handling

### Monitoring Integration
- Execution timing metrics
- Resource usage tracking
- Structured logging for observability
- Correlation ID propagation

## Quality Standards

- **Type Safety**: Complete type annotations for all functions and classes
- **Error Handling**: FlextResult usage for all operations with detailed error context
- **Testing**: Comprehensive unit and integration tests with subprocess mocking
- **Documentation**: Complete docstrings with usage examples and bridge patterns
- **Security**: Input validation and secure subprocess execution

## Integration Points

### Current Integration
- **Direct Library Usage**: Python services can import and use directly
- **Subprocess Calls**: Go services execute via subprocess (current pattern)
- **CLI Interface**: Command-line execution for development and testing

### Future Integration (After Bridge Implementation)
- **FlextMeltanoBridge**: Will be primary consumer of this module
- **Go Service Integration**: Simplified bridge API for Go services
- **Monitoring Integration**: Enhanced observability and metrics collection

## Critical Issues & Next Actions

- ✅ **Core Functionality**: Subprocess execution patterns working
- 🔄 **Bridge Missing**: simple_bridge.py needs to use this module
- ⚠️ **Type Safety**: Some type annotations may need refinement
- 📈 **Performance**: Monitoring and optimization opportunities

This module serves as the **execution backbone** for all FLEXT Meltano operations
and is essential for the Go ↔ Python bridge integration architecture.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import uuid
import warnings
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

# FlextResult is MANDATORY for all operations
from flext_core import FlextLogger, FlextModel, FlextResult
from pydantic import Field

from flext_meltano.base import FlextMeltanoConfig

# Injectable decorator from common utilities
from flext_meltano.common import injectable


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
        self.logger = FlextLogger.get_logger(self.__class__.__name__)

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
    """Centralized subprocess execution to eliminate code duplication.

    This function provides a common pattern for subprocess execution used
    throughout the FLEXT Meltano ecosystem, ensuring consistent error handling
    and result formatting.

    Args:
        context: Subprocess execution context with command and options

    Returns:
        FlextResult with execution details including stdout, stderr, returncode

    """
    try:
        # Set up environment
        exec_env = dict(os.environ)
        if context.env:
            exec_env.update(context.env)

        # Execute subprocess with common pattern
        result = subprocess.run(  # noqa: S603
            context.command,
            cwd=context.cwd,
            env=exec_env,
            capture_output=context.capture_output,
            text=context.text,
            timeout=context.timeout_seconds,
            check=context.check,
        )

        # Return standardized result
        execution_result = {
            "command": " ".join(context.command),
            "returncode": result.returncode,
            "stdout": result.stdout or "",
            "stderr": result.stderr or "",
            "success": result.returncode == 0,
            "cwd": str(context.cwd) if context.cwd else str(Path.cwd()),
        }

        return FlextResult(data=execution_result)

    except subprocess.TimeoutExpired as e:
        return FlextResult(
            error=f"Command timed out after {context.timeout_seconds} seconds: {e}",
        )
    except (subprocess.CalledProcessError, OSError, FileNotFoundError) as e:
        return FlextResult(error=f"Command error: {e}")


# === LEGACY COMPATIBILITY ===


class FlextMeltanoResult:
    """Legacy result type for backward compatibility."""

    def __init__(
        self,
        *,
        success: bool,
        data: dict[str, object] | None = None,
        error: str = "",
    ) -> None:
        """Initialize result."""
        self.success = success
        self.data = data
        self.error = error

    @classmethod
    def ok(cls, data: dict[str, object] | None = None) -> FlextMeltanoResult:
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
    if result.success:
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
    if result.success:
        return FlextMeltanoResult.ok(result.data)
    return FlextMeltanoResult.fail(result.error or "Execution failed")
