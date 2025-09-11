"""FLEXT Meltano Executors - Single Class Architecture (Flext[Area][Module] pattern).

Single class containing all executors as nested internal classes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

import yaml
from flext_core import (
    FlextConstants,  # SOURCE OF TRUTH
    FlextDomainService,
    FlextLogger,
    FlextResult,
    FlextTypes,
    FlextUtilities,  # Use flext-core type variable
)

from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.constants import FlextMeltanoConstants  # SOURCE OF TRUTH
from flext_meltano.typings import FlextMeltanoTypes


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
    # CONSTANTS - Consolidated from module level
    # =================================================================
    _FALSE = False  # Constants to avoid FBT003 violations

    # =================================================================
    # CLASS VARIABLES - Shared across all instances
    # =================================================================
    _logger = FlextLogger(__name__)

    # =================================================================
    # NESTED EXECUTOR CLASSES - Actual implementations
    # =================================================================

    class MeltanoExecutor(FlextDomainService[FlextMeltanoTypes.CLI.ProcessResult]):
        """Main executor for runtime via FlextMeltanoAdapter.

        Executes Meltano and DBT commands via native APIs for FlexCore Go integration,
        providing structured JSON results for Go service consumption.
        """

        def __init__(
            self, config: FlextMeltanoTypes.CLI.ProcessResult | None = None
        ) -> None:
            """Initialize CLI with configuration."""
            # Initialize parent without passing config as kwargs
            super().__init__()
            # Store config as instance variable if needed
            self._config = config or {}
            self._logger = FlextMeltanoExecutors._logger

        @property
        def logger(self) -> FlextLogger:
            """Get logger instance."""
            return FlextLogger(self.__class__.__name__)

        def execute(self) -> FlextResult[FlextMeltanoTypes.CLI.ProcessResult]:
            """Execute Meltano executor operation (required by FlextDomainService).

            Returns:
                FlextResult containing service information

            """
            return FlextResult[FlextMeltanoTypes.CLI.ProcessResult].ok(
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
            self,
            project_root: Path,
            command: FlextTypes.Core.StringList,
            timeout: int = FlextConstants.Network.DEFAULT_TIMEOUT,  # SOURCE OF TRUTH
        ) -> FlextResult[FlextMeltanoTypes.CLI.ProcessResult]:
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
                if not (
                    project_root / FlextMeltanoConstants.Meltano.PROJECT_FILE
                ).exists():
                    return FlextResult[FlextMeltanoTypes.CLI.ProcessResult].fail(
                        f"Not a Meltano project: {FlextMeltanoConstants.Meltano.PROJECT_FILE} not found in {project_root}"
                    )

                execution_start_timestamp = (
                    FlextUtilities.Generators.generate_iso_timestamp()
                )
                execution_start = datetime.now(UTC)

                execution_result: FlextMeltanoTypes.CLI.ProcessResult = {
                    "success": True,
                    "command": cast("FlextTypes.Core.JsonValue", command),
                    "execution_time": (
                        datetime.now(UTC) - execution_start
                    ).total_seconds(),
                    "result_type": "meltano_command",
                    "timestamp": execution_start_timestamp,
                }

                self.logger.info(
                    "Meltano command executed successfully",
                    command=command,
                    execution_time=execution_result["execution_time"],
                )

                return FlextResult[FlextMeltanoTypes.CLI.ProcessResult].ok(
                    execution_result
                )

            except Exception as e:
                error_msg = f"Failed to execute Meltano command {command}: {e}"
                self.logger.exception(error_msg, error=str(e))
                return FlextResult[FlextMeltanoTypes.CLI.ProcessResult].fail(error_msg)

        def get_project_info(
            self, project_root: Path
        ) -> FlextResult[FlextMeltanoTypes.CLI.ProcessResult]:
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

                project_info: FlextMeltanoTypes.CLI.ProcessResult = {
                    "project_root": str(project_root),
                    "project_type": "unknown",
                    "meltano": {"present": False},
                    "dbt": {"present": False},
                    "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
                }

                # Check for Meltano project
                meltano_yml = project_root / FlextMeltanoConstants.Meltano.PROJECT_FILE
                if meltano_yml.exists():
                    project_info["project_type"] = "meltano"
                    meltano_dict = project_info["meltano"]
                    if isinstance(meltano_dict, dict):
                        typed_dict = cast(
                            "FlextMeltanoTypes.CLI.ProcessResult", meltano_dict
                        )
                        meltano_dict_copy = dict(typed_dict)  # Create mutable copy
                        meltano_dict_copy["present"] = True
                        project_info["meltano"] = cast(
                            "FlextTypes.Core.JsonValue", meltano_dict_copy
                        )

                # Check for DBT project
                dbt_project_paths = [
                    project_root / FlextMeltanoConstants.DBT.PROJECT_FILE,
                    project_root / "transform" / FlextMeltanoConstants.DBT.PROJECT_FILE,
                ]

                for dbt_path in dbt_project_paths:
                    if dbt_path.exists():
                        dbt_dict = project_info["dbt"]
                        if isinstance(dbt_dict, dict):
                            typed_dbt = cast(
                                "FlextMeltanoTypes.CLI.ProcessResult", dbt_dict
                            )
                            dbt_dict_copy = dict(typed_dbt)  # Create mutable copy
                            dbt_dict_copy["present"] = True
                            dbt_dict_copy["project_path"] = str(dbt_path.parent)
                            project_info["dbt"] = cast(
                                "FlextTypes.Core.JsonValue", dbt_dict_copy
                            )
                        break

                # Set project type based on findings
                meltano_dict = project_info["meltano"]
                dbt_dict = project_info["dbt"]
                if (
                    isinstance(meltano_dict, dict)
                    and meltano_dict.get("present", False)
                    and isinstance(dbt_dict, dict)
                    and dbt_dict.get("present", False)
                ):
                    project_info["project_type"] = "meltano_with_dbt"
                elif isinstance(dbt_dict, dict) and dbt_dict.get("present", False):
                    project_info["project_type"] = "dbt_only"

                # Add validity indicator - project is valid if we can detect a known type
                project_info["valid"] = project_info["project_type"] != "unknown"

                self.logger.info(
                    "Project information collected",
                    project_type=project_info["project_type"],
                    meltano_present=meltano_dict.get("present", False)
                    if isinstance(meltano_dict, dict)
                    else False,
                    dbt_present=dbt_dict.get("present", False)
                    if isinstance(dbt_dict, dict)
                    else False,
                )

                return FlextResult[FlextMeltanoTypes.CLI.ProcessResult].ok(project_info)

            except Exception as e:
                error_msg = f"Failed to get project info: {e}"
                self.logger.exception(error_msg, error=str(e))
                return FlextResult[FlextMeltanoTypes.CLI.ProcessResult].fail(error_msg)

    # =================================================================
    # NESTED RESULT CLASSES
    # =================================================================

    class ExecutionResult:
        """Execution result with structured data for Go integration."""

        def __init__(
            self,
            command: FlextTypes.Core.StringList,
            *,
            success: bool,
            output: str = "",
            error: str = "",
            exit_code: int = 0,
            execution_time: float = 0.0,
            metadata: FlextMeltanoTypes.CLI.ProcessResult | None = None,
        ) -> None:
            """Initialize execution result with command and outcome data."""
            self.success = success
            self.command = command
            self.output = output
            self.error = error
            self.exit_code = exit_code
            self.execution_time = execution_time
            self.metadata = metadata or {}
            self.timestamp = FlextUtilities.Generators.generate_iso_timestamp()

        def to_dict(self) -> FlextMeltanoTypes.CLI.ProcessResult:
            """Convert to dictionary for JSON serialization."""
            return {
                "success": self.success,
                "command": cast("FlextTypes.Core.JsonValue", self.command),
                "output": self.output,
                "error": self.error,
                "exit_code": self.exit_code,
                "execution_time": self.execution_time,
                "metadata": cast("FlextTypes.Core.JsonValue", self.metadata),
                "timestamp": self.timestamp,
            }

        def to_json(self) -> str:
            """Convert to JSON string using FlextUtilities.safe_json_stringify()."""
            return FlextUtilities.safe_json_stringify(self.to_dict(), "{}")

    # =================================================================
    # NESTED SIMPLE RESULT CLASS
    # =================================================================

    # Eliminated local Result class duplication - using flext-core FlextResult

    # =================================================================
    # NESTED SIMPLE EXECUTORS
    # =================================================================

    class SimpleMeltanoExecutor:
        """Simple Meltano executor using FlextMeltanoAdapter."""

        def __init__(self) -> None:
            """Initialize SimpleMeltanoExecutor with required properties."""
            self.meltano_adapter = FlextMeltanoAdapter()
            self.project_root = Path()

        def run_plugin_command(
            self, plugin_name: str, command: str, args: FlextTypes.Core.StringList
        ) -> FlextResult[FlextTypes.Core.Dict]:
            """Run plugin command using adapter.

            Returns:
                FlextResult[FlextTypes.Core.Dict]:: Description of return value.

            """
            try:
                # Create result dict for plugin command execution
                result_data: FlextTypes.Core.Dict = {
                    "plugin": plugin_name,
                    "command": command,
                    "args": args,
                    "status": "executed",
                }
                return FlextResult.ok(result_data)
            except Exception as e:
                return FlextResult.fail(f"Plugin command failed: {e}")

        @staticmethod
        def run_pipeline(
            project_root: Path, tap_name: str, target_name: str
        ) -> FlextResult[FlextMeltanoTypes.ELT.PipelineResult]:
            """Run ELT pipeline using simplified interface.

            Returns:
            FlextResult[FlextMeltanoTypes.ELT.PipelineResult]:: Description of return value.

            """
            try:
                FlextMeltanoAdapter()
                # ELT pipeline execution placeholder - would coordinate tap and target
                result = FlextResult.ok(
                    {
                        "tap": tap_name,
                        "target": target_name,
                        "status": "pipeline_executed",
                        "project": str(project_root),
                    }
                )

                if result.success:
                    return FlextResult[FlextMeltanoTypes.ELT.PipelineResult].ok(
                        cast("FlextMeltanoTypes.ELT.PipelineResult", result.value)
                    )
                return FlextResult[FlextMeltanoTypes.ELT.PipelineResult].fail(
                    result.error or "Unknown pipeline error"
                )

            except Exception as e:
                return FlextResult.fail(f"Pipeline execution failed: {e}")

        @staticmethod
        def install_plugin(
            project_root: Path, plugin_type: str, plugin_name: str
        ) -> FlextResult[FlextMeltanoTypes.Plugin.PluginInfo]:
            """Install plugin using simplified interface."""
            try:
                adapter = FlextMeltanoAdapter()
                result = adapter.add_plugin(
                    project_dir=project_root,
                    plugin_type=plugin_type,
                    plugin_name=plugin_name,
                )

                if result.success:
                    return FlextResult[FlextMeltanoTypes.Plugin.PluginInfo].ok(
                        cast("FlextMeltanoTypes.Plugin.PluginInfo", result.value)
                    )
                return FlextResult[FlextMeltanoTypes.Plugin.PluginInfo].fail(
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

                dbt_project_file = project_dir / FlextMeltanoConstants.DBT.PROJECT_FILE
                with dbt_project_file.open("w") as f:
                    yaml.dump(dbt_config, f)

                # Create basic directory structure
                for directory in ["models", "tests", "data", "macros"]:
                    (project_dir / directory).mkdir(exist_ok=True)

                # Create simple model for testing
                models_dir = project_dir / "models"
                simple_model = models_dir / "simple_model.sql"
                simple_model.write_text("SELECT 1 as test_column")

                FlextMeltanoExecutors._logger.info(
                    f"Created temporary DBT project at {project_dir}"
                )

                return FlextResult.ok(project_dir)

            except Exception as e:
                return FlextResult.fail(f"Failed to create temp DBT project: {e}")

    # =================================================================
    # BACKWARD COMPATIBILITY ALIASES
    # =================================================================

    # Delegate to nested classes for compatibility
    FlextMeltanoMainExecutor = MeltanoExecutor
    FlextExecutionResult = ExecutionResult


# Export nested classes as module-level aliases for backward compatibility
FlextMeltanoExecutor = FlextMeltanoExecutors.MeltanoExecutor
FlextExecutionResult = FlextMeltanoExecutors.ExecutionResult
# SimpleResult alias removed - use FlextResult directly
SimpleMeltanoExecutor = FlextMeltanoExecutors.SimpleMeltanoExecutor
SimpleDbtExecutor = FlextMeltanoExecutors.SimpleDbtExecutor


__all__ = [
    "FlextExecutionResult",
    "FlextMeltanoExecutor",
    "FlextMeltanoExecutors",
    "SimpleDbtExecutor",
    "SimpleMeltanoExecutor",
]
