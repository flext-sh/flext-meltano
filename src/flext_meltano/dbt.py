"""FLEXT Meltano DBT - Data Transformation Integration.

**Architecture Layer**: Data Transformation Layer
**Status**: ✅ STABLE - DBT integration and project management
**Dependencies**: flext-core (FlextResult), DBT Core, enterprise patterns

## Module Purpose

This module provides **DBT (Data Build Tool) integration** for FLEXT Meltano's
bridge architecture, enabling Go services to execute data transformation
workflows through subprocess orchestration with enterprise patterns.

## Design Principles

1. **DBT Project Management**: Complete DBT project lifecycle management
2. **Model Execution**: DBT model compilation, testing, and execution
3. **Bridge-Friendly**: JSON-serializable DBT results for Go services
4. **Enterprise Patterns**: FlextResult integration and structured error handling
5. **Pipeline Integration**: Seamless integration with Singer extract/load operations

## Core Components

### DBT Operations
- `FlextMeltanoDbtService`: Primary DBT operations service
- DBT model compilation, execution, and testing
- DBT documentation generation and lineage analysis
- Project configuration and environment management

### Bridge Integration
- DBT command execution via subprocess for Go services
- JSON-serializable execution results and model metadata
- DBT test results and data quality reporting
- Integration with Meltano pipeline orchestration

## Usage Patterns

### Basic DBT Operations
```python
from flext_meltano.dbt import FlextMeltanoDbtService

# Initialize DBT service
dbt_service = FlextMeltanoDbtService(project_dir="./dbt")

# Run DBT models
result = dbt_service.run_models()
if result.success:
    print("DBT models executed successfully")

# Test DBT models
test_result = dbt_service.test_models()
if test_result.success:
    print("All DBT tests passed")
```

### Bridge Integration
```python
# DBT operations designed for bridge consumption
def bridge_invoke_dbt(command: str, *args: str) -> FlextTypes.Core.JsonDict:
    '''Execute DBT command with JSON-serializable results for Go services.'''
    dbt_service = FlextMeltanoDbtService()
    result = dbt_service.execute_command(command, *args)

    return {
        "success": result.success,
        "command": command,
        "output": result.data if result.success else None,
        "error": result.error_message if result.is_failure else None,
    }
```

This module provides essential **data transformation capabilities** for FLEXT
Meltano's bridge architecture, enabling comprehensive DBT workflow management
for Go service integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from flext_core import FlextResult

from flext_meltano.base import FlextMeltanoConfig

if TYPE_CHECKING:
    from flext_core.semantic_types import FlextTypes

    from flext_meltano.execution import FlextMeltanoExecutor


def _get_default_executor(
    config: FlextMeltanoConfig | None = None,
) -> FlextMeltanoExecutor:
    """Create default executor instance avoiding circular imports."""
    # Import locally to avoid circular import at module level
    from flext_meltano.execution import FlextMeltanoExecutor  # noqa: PLC0415

    used_config = config or FlextMeltanoConfig()
    return FlextMeltanoExecutor(used_config)


class FlextMeltanoDbtManager:
    """DBT Manager with real implementation using Meltano executor."""

    def __init__(
        self,
        project_dir: Path | str | None = None,
        executor: FlextMeltanoExecutor | None = None,
        config: FlextMeltanoConfig | None = None,
    ) -> None:
        """Initialize DBT manager with real executor integration."""
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()

        # Use dependency injection pattern from CLAUDE.md
        if executor is not None:
            self.executor = executor
        else:
            self.executor = _get_default_executor(config)

    def run_models(
        self,
        models: list[str] | None = None,
        select: str | None = None,
        exclude: str | None = None,
    ) -> FlextResult[FlextTypes.Core.JsonDict]:
        """Run DBT models using real Meltano executor."""
        cmd = ["invoke", "dbt:run"]

        if models:
            cmd.extend(["--models", " ".join(models)])
        elif select:
            cmd.extend(["--select", select])

        if exclude:
            cmd.extend(["--exclude", exclude])

        # Execute using real Meltano command
        result = self.executor.run_command(cmd)

        if result.success:
            return FlextResult.ok(
                {
                    "models": models or [],
                    "command": " ".join(cmd),
                    "status": "success",
                    "output": result.data,
                },
            )
        return FlextResult.fail(f"DBT run failed: {result.error}")

    def test_models(
        self,
        models: list[str] | None = None,
        select: str | None = None,
    ) -> FlextResult[FlextTypes.Core.JsonDict]:
        """Test DBT models using real Meltano executor."""
        cmd = ["invoke", "dbt:test"]

        if models:
            cmd.extend(["--models", " ".join(models)])
        elif select:
            cmd.extend(["--select", select])

        result = self.executor.run_command(cmd)

        if result.success:
            return FlextResult.ok(
                {
                    "models": models or [],
                    "command": " ".join(cmd),
                    "status": "success",
                    "output": result.data,
                },
            )
        return FlextResult.fail(f"DBT test failed: {result.error}")

    def compile_models(
        self,
        models: list[str] | None = None,
        select: str | None = None,
    ) -> FlextResult[FlextTypes.Core.JsonDict]:
        """Compile DBT models using real Meltano executor."""
        cmd = ["invoke", "dbt:compile"]

        if models:
            cmd.extend(["--models", " ".join(models)])
        elif select:
            cmd.extend(["--select", select])

        result = self.executor.run_command(cmd)

        if result.success:
            return FlextResult.ok(
                {
                    "models": models or [],
                    "command": " ".join(cmd),
                    "status": "success",
                    "output": result.data,
                },
            )
        return FlextResult.fail(f"DBT compile failed: {result.error}")

    def generate_docs(self) -> FlextResult[FlextTypes.Core.JsonDict]:
        """Generate DBT documentation."""
        result = self.executor.run_command(["invoke", "dbt:docs:generate"])

        if result.success:
            return FlextResult.ok(
                {
                    "command": "dbt docs generate",
                    "status": "success",
                    "output": result.data,
                },
            )
        return FlextResult.fail(f"DBT docs generation failed: {result.error}")

    def serve_docs(self, port: int = 8080) -> FlextResult[FlextTypes.Core.JsonDict]:
        """Serve DBT documentation."""
        result = self.executor.run_command(
            [
                "invoke",
                "dbt:docs:serve",
                "--port",
                str(port),
            ],
        )

        if result.success:
            return FlextResult.ok(
                {
                    "command": f"dbt docs serve --port {port}",
                    "status": "success",
                    "port": port,
                    "output": result.data,
                },
            )
        return FlextResult.fail(f"DBT docs serve failed: {result.error}")


class FlextMeltanoDbtProject:
    """DBT Project management with real Meltano integration."""

    def __init__(
        self,
        project_dir: Path | str | None = None,
        executor: FlextMeltanoExecutor | None = None,
    ) -> None:
        """Initialize DBT project with real executor."""
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()

        if executor is not None:
            self.executor = executor
        else:
            self.executor = _get_default_executor()

    def initialize(self) -> FlextResult[None]:
        """Initialize DBT project using Meltano."""
        result = self.executor.run_command(["invoke", "dbt:initialize"])

        if result.success:
            return FlextResult.ok(None)
        return FlextResult.fail(f"DBT project initialization failed: {result.error}")

    def validate(self) -> FlextResult[None]:
        """Validate DBT project configuration."""
        # Check if dbt_project.yml exists
        dbt_project_file = self.project_dir / "dbt_project.yml"
        if not dbt_project_file.exists():
            return FlextResult.fail(f"DBT project file not found: {dbt_project_file}")

        # Run DBT parse to validate project
        result = self.executor.run_command(["invoke", "dbt:parse"])

        if result.success:
            return FlextResult.ok(None)
        return FlextResult.fail(f"DBT project validation failed: {result.error}")


class FlextMeltanoDbtRunner:
    """DBT Runner for executing DBT commands with real implementation."""

    def __init__(
        self,
        project_dir: Path | str | None = None,
        executor: FlextMeltanoExecutor | None = None,
    ) -> None:
        """Initialize DBT runner with real executor."""
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()

        if executor is not None:
            self.executor = executor
        else:
            self.executor = _get_default_executor()

    def run(
        self,
        command: str,
        args: list[str] | None = None,
    ) -> FlextResult[FlextTypes.Core.JsonDict]:
        """Run DBT command using Meltano executor."""
        cmd = ["invoke", f"dbt:{command}"]
        if args:
            cmd.extend(args)

        result = self.executor.run_command(cmd)

        if result.success:
            return FlextResult.ok(
                {
                    "command": " ".join(cmd),
                    "args": args or [],
                    "status": "success",
                    "output": result.data,
                },
            )
        return FlextResult.fail(f"DBT command failed: {result.error}")

    def run_models(
        self,
        models: list[str] | None = None,
    ) -> FlextResult[FlextTypes.Core.JsonDict]:
        """Run specific DBT models."""
        args = []
        if models:
            args.extend(["--models", " ".join(models)])

        return self.run("run", args)

    def test_models(
        self,
        models: list[str] | None = None,
    ) -> FlextResult[FlextTypes.Core.JsonDict]:
        """Test specific DBT models."""
        args = []
        if models:
            args.extend(["--models", " ".join(models)])

        return self.run("test", args)


# Export classes for Singer project imports
__all__: list[str] = [
    "FlextMeltanoDbtManager",
    "FlextMeltanoDbtProject",
    "FlextMeltanoDbtRunner",
]
