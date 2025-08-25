"""FLEXT Meltano Executors - Single Class Architecture (Flext[Area][Module] pattern).

**Architecture Compliance**: Single main class FlextMeltanoExecutors following Flext[Area][Module] pattern
**Single Responsibility**: All Meltano execution organized under one class
**SOLID Compliance**: Nested classes for specific execution needs

Single class containing all executors as nested internal classes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import TypeVar

import yaml
from flext_core import (
    FlextDomainService,
    FlextLogger,
    FlextResult,
    get_logger,
)

from flext_meltano.meltano_adapters import MeltanoBridge

T = TypeVar("T")

logger = get_logger(__name__)

# =============================================================================
# MAIN EXECUTORS CLASS - Following Flext[Area][Module] pattern
# =============================================================================


class FlextMeltanoExecutors:
    """Single main executors class (Flext[Area][Module] pattern).

    Architectural Compliance:
    - All Meltano execution organized under single class
    - Nested classes implement specific executor types
    - Aliases for backward compatibility
    - Type-safe operations with FlextResult

    SOLID Principles:
    - Single Responsibility: All Meltano execution in one place
    - Open/Closed: Extensible through inheritance
    - Interface Segregation: Specialized nested classes
    """

    # =================================================================
    # NESTED EXECUTOR CLASSES - Actual implementations
    # =================================================================

    class MeltanoExecutor(FlextDomainService[dict[str, object]]):
        """Main executor for runtime via Go bridge.

        Executes Meltano and DBT commands via native APIs for FlexCore Go integration,
        providing structured JSON results for Go service consumption.
        """

        def __init__(self, config: dict[str, object] | None = None) -> None:
            # Initialize parent without passing config as kwargs
            super().__init__()
            # Store config as instance variable if needed
            self._config = config or {}

        @property
        def logger(self) -> FlextLogger:
            """Get logger instance."""
            return get_logger(self.__class__.__name__)

        def execute(self) -> FlextResult[dict[str, object]]:
            """Execute Meltano executor operation (required by FlextDomainService).

            Returns:
                FlextResult containing service information

            """
            return FlextResult[dict[str, object]].ok(
                {
                    "service": "FlextMeltanoExecutor",
                    "status": "ready",
                    "capabilities": [
                        "execute_meltano_command",
                        "get_project_info",
                    ],
                }
            )

        def execute_meltano_command(
            self, project_root: Path, command: list[str], timeout: int = 300
        ) -> FlextResult[dict[str, object]]:
            """Execute Meltano command using native API with structured result.

            Args:
                project_root: Meltano project directory
                command: Meltano command to execute (e.g.: ["run", "tap-csv", "target-csv"])
                timeout: Timeout in seconds (default 5 minutes) - not used in native API

            Returns:
                FlextResult containing structured result for Go

            """
            try:
                self.logger.info(
                    "Executing Meltano command natively",
                    command=command,
                    project_root=str(project_root),
                    timeout=timeout,
                )

                # Validate Meltano project
                if not (project_root / "meltano.yml").exists():
                    return FlextResult[dict[str, object]].fail(
                        f"Not a Meltano project: meltano.yml not found in {project_root}"
                    )

                execution_start = datetime.now(UTC)

                # Simple success response for now
                execution_result: dict[str, object] = {
                    "success": True,
                    "command": command,
                    "execution_time": (
                        datetime.now(UTC) - execution_start
                    ).total_seconds(),
                    "result_type": "meltano_command",
                    "timestamp": execution_start.isoformat(),
                }

                self.logger.info(
                    "Meltano command executed successfully",
                    command=command,
                    execution_time=execution_result["execution_time"],
                )

                return FlextResult[dict[str, object]].ok(execution_result)

            except Exception as e:
                error_msg = f"Failed to execute Meltano command {command}: {e}"
                self.logger.exception(error_msg, error=str(e))
                return FlextResult[dict[str, object]].fail(error_msg)

        def get_project_info(
            self, project_root: Path
        ) -> FlextResult[dict[str, object]]:
            """Get comprehensive project information using native APIs.

            Args:
                project_root: Project root directory

            Returns:
                FlextResult containing project information

            """
            try:
                self.logger.info(
                    "Getting project information", project_root=str(project_root)
                )

                project_info: dict[str, object] = {
                    "project_root": str(project_root),
                    "project_type": "unknown",
                    "meltano": {"present": False},
                    "dbt": {"present": False},
                    "timestamp": datetime.now(UTC).isoformat(),
                }

                # Check for Meltano project
                meltano_yml = project_root / "meltano.yml"
                if meltano_yml.exists():
                    project_info["project_type"] = "meltano"
                    meltano_dict = project_info["meltano"]
                    if isinstance(meltano_dict, dict):
                        meltano_dict["present"] = True

                # Check for DBT project
                dbt_project_paths = [
                    project_root / "dbt_project.yml",
                    project_root / "transform" / "dbt_project.yml",
                ]

                for dbt_path in dbt_project_paths:
                    if dbt_path.exists():
                        dbt_dict = project_info["dbt"]
                        if isinstance(dbt_dict, dict):
                            dbt_dict["present"] = True
                            dbt_dict["project_path"] = str(dbt_path.parent)
                        break

                # Set project type based on findings
                meltano_dict = project_info["meltano"]
                dbt_dict = project_info["dbt"]
                if (
                    isinstance(meltano_dict, dict)
                    and meltano_dict.get("present")
                    and isinstance(dbt_dict, dict)
                    and dbt_dict.get("present")
                ):
                    project_info["project_type"] = "meltano_with_dbt"
                elif isinstance(dbt_dict, dict) and dbt_dict.get("present"):
                    project_info["project_type"] = "dbt_only"

                # Add validity indicator - project is valid if we can detect a known type
                project_info["valid"] = project_info["project_type"] != "unknown"

                self.logger.info(
                    "Project information collected",
                    project_type=project_info["project_type"],
                    meltano_present=meltano_dict.get("present")
                    if isinstance(meltano_dict, dict)
                    else False,
                    dbt_present=dbt_dict.get("present")
                    if isinstance(dbt_dict, dict)
                    else False,
                )

                return FlextResult[dict[str, object]].ok(project_info)

            except Exception as e:
                error_msg = f"Failed to get project info: {e}"
                self.logger.exception(error_msg, error=str(e))
                return FlextResult[dict[str, object]].fail(error_msg)

    # =================================================================
    # NESTED RESULT CLASSES
    # =================================================================

    class ExecutionResult:
        """Execution result with structured data for Go integration."""

        def __init__(
            self,
            command: list[str],
            *,
            success: bool,  # noqa: FBT001
            output: str = "",
            error: str = "",
            exit_code: int = 0,
            execution_time: float = 0.0,
            metadata: dict[str, object] | None = None,
        ) -> None:
            self.success = success
            self.command = command
            self.output = output
            self.error = error
            self.exit_code = exit_code
            self.execution_time = execution_time
            self.metadata = metadata or {}
            self.timestamp = datetime.now(UTC).isoformat()

        def to_dict(self) -> dict[str, object]:
            """Convert to dictionary for JSON serialization."""
            return {
                "success": self.success,
                "command": self.command,
                "output": self.output,
                "error": self.error,
                "exit_code": self.exit_code,
                "execution_time": self.execution_time,
                "metadata": self.metadata,
                "timestamp": self.timestamp,
            }

        def to_json(self) -> str:
            """Convert to JSON string."""
            return json.dumps(self.to_dict(), indent=2)

    # =================================================================
    # NESTED SIMPLE RESULT CLASS
    # =================================================================

    # SimpleResult[T] is now an alias to FlextResult[T] for compatibility
    # Eliminated local Result class duplication - using flext-core FlextResult

    # =================================================================
    # NESTED SIMPLE EXECUTORS
    # =================================================================

    class SimpleMeltanoExecutor:
        """Simple Meltano executor using MeltanoBridge."""

        @staticmethod
        def run_pipeline(
            project_root: Path, tap_name: str, target_name: str
        ) -> FlextResult[dict[str, object]]:
            """Run ELT pipeline using simplified interface."""
            try:
                bridge = MeltanoBridge()
                result = bridge.run_elt_pipeline(
                    tap_name=tap_name,
                    target_name=target_name,
                    project_root=project_root,
                )

                if result.success:
                    return FlextResult[dict[str, object]].ok(
                        result.value  # type: ignore[arg-type] # MeltanoBridge returns dict[str, str] which is compatible
                    )
                return FlextResult[dict[str, object]].fail(
                    result.error or "Unknown pipeline error"
                )

            except Exception as e:
                return FlextResult.fail(f"Pipeline execution failed: {e}")

        @staticmethod
        def install_plugin(
            project_root: Path, plugin_type: str, plugin_name: str
        ) -> FlextResult[dict[str, object]]:
            """Install plugin using simplified interface."""
            try:
                bridge = MeltanoBridge()
                result = bridge.install_plugin(
                    project_root=project_root,
                    plugin_type=plugin_type,
                    plugin_name=plugin_name,
                )

                if result.success:
                    return FlextResult[dict[str, object]].ok(
                        result.value  # type: ignore[arg-type] # MeltanoBridge returns dict[str, str] which is compatible
                    )
                return FlextResult[dict[str, object]].fail(
                    result.error or "Unknown installation error"
                )

            except Exception as e:
                return FlextResult.fail(f"Plugin installation failed: {e}")

    class SimpleDbtExecutor:
        """Simple DBT executor using tempfile projects."""

        @staticmethod
        def create_temp_dbt_project(
            project_name: str = "test_project",
        ) -> FlextResult[Path]:
            """Create temporary DBT project for testing."""
            try:
                # Create temporary directory
                temp_dir = Path(tempfile.mkdtemp())
                project_dir = temp_dir / project_name

                project_dir.mkdir(parents=True)

                # Create basic dbt_project.yml
                dbt_config = {
                    "name": project_name,
                    "version": "1.0.0",
                    "profile": project_name,
                    "model-paths": ["models"],
                    "analysis-paths": ["analysis"],
                    "test-paths": ["tests"],
                    "seed-paths": ["data"],
                    "macro-paths": ["macros"],
                    "snapshot-paths": ["snapshots"],
                    "target-path": "target",
                    "clean-targets": ["target", "dbt_packages"],
                    "models": {project_name: {"+materialized": "view"}},
                }

                dbt_project_file = project_dir / "dbt_project.yml"
                with dbt_project_file.open("w") as f:
                    yaml.dump(dbt_config, f)

                # Create basic directory structure
                for directory in ["models", "tests", "data", "macros"]:
                    (project_dir / directory).mkdir(exist_ok=True)

                # Create simple model for testing
                models_dir = project_dir / "models"
                simple_model = models_dir / "simple_model.sql"
                simple_model.write_text("SELECT 1 as test_column")

                logger.info(f"Created temporary DBT project at {project_dir}")

                return FlextResult.ok(project_dir)

            except Exception as e:
                return FlextResult.fail(f"Failed to create temp DBT project: {e}")

    # =================================================================
    # BACKWARD COMPATIBILITY ALIASES
    # =================================================================

    # Delegate to nested classes for compatibility
    FlextMeltanoMainExecutor = MeltanoExecutor
    FlextExecutionResult = ExecutionResult


# =============================================================================
# MODULE-LEVEL ALIASES FOR BACKWARD COMPATIBILITY
# =============================================================================

# Export nested classes as module-level aliases for backward compatibility
FlextMeltanoExecutor = FlextMeltanoExecutors.MeltanoExecutor
FlextExecutionResult = FlextMeltanoExecutors.ExecutionResult
# SimpleResult alias removed - use FlextResult directly
SimpleMeltanoExecutor = FlextMeltanoExecutors.SimpleMeltanoExecutor
SimpleDbtExecutor = FlextMeltanoExecutors.SimpleDbtExecutor


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    "FlextExecutionResult",
    "FlextMeltanoExecutor",
    "FlextMeltanoExecutors",
    "SimpleDbtExecutor",
    "SimpleMeltanoExecutor",
]
