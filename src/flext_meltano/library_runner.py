"""FLEXT Meltano Library Runner - Unified library runner for Meltano operations.

This module provides the FlextMeltanoLibraryRunner class for comprehensive Meltano
functionality including ELT pipelines and DBT transformations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextLogger, FlextResult, FlextTypes

# Use specific module imports to avoid circular dependencies
from flext_meltano.bridge import FlextMeltanoBridge
from flext_meltano.executor import FlextMeltanoExecutor
from flext_meltano.singer_protocols import SingerTap, SingerTarget
from flext_meltano.typings import FlextMeltanoTypes


class FlextMeltanoLibraryRunner:
    """Unified library runner providing comprehensive Meltano functionality.

    This class consolidates all Meltano operations (DBT transformations, Singer
    protocols, ELT pipelines) into a single, well-structured interface following
    ZERO TOLERANCE architectural principles.
    """

    def __init__(self) -> None:
        """Initialize the library runner."""
        self._logger: FlextLogger = FlextLogger(__name__)
        self._executor = FlextMeltanoExecutor()
        self._bridge = FlextMeltanoBridge()

    def run_elt_pipeline(
        self,
        tap: SingerTap,
        target: SingerTarget,
        config: dict[str, FlextTypes.JsonValue] | None = None,
    ) -> FlextResult[FlextMeltanoTypes.Processing.EltPipelineResult]:
        """Run a complete ELT pipeline from tap to target.

        Args:
            tap: Singer tap to extract data from
            target: Singer target to load data into
            config: Pipeline configuration

        Returns:
            FlextResult with ELT pipeline execution results

        """
        try:
            self._logger.info(
                "Starting ELT pipeline", tap_name=tap.name, target_name=target.name
            )

            # Execute the pipeline using the executor
            result = self._executor.execute_pipeline(tap.name, target.name, config)

            if result.is_failure:
                return FlextResult[FlextMeltanoTypes.Processing.EltPipelineResult].fail(
                    result.error or "Pipeline execution failed"
                )

            # Convert execution result to ELT pipeline result
            execution_result = result.unwrap()
            elt_result: FlextMeltanoTypes.Processing.EltPipelineResult = {
                "success": execution_result.success,
                "tap_name": tap.name,
                "target_name": target.name,
                "execution_time": execution_result.execution_time,
                "exit_code": execution_result.exit_code,
                "output": execution_result.output,
                "error": execution_result.error,
            }

            return FlextResult[FlextMeltanoTypes.Processing.EltPipelineResult].ok(
                elt_result
            )

        except Exception as e:
            error_msg = f"ELT pipeline execution failed: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextMeltanoTypes.Processing.EltPipelineResult].fail(
                error_msg
            )

    def run_dbt_transformation(
        self,
        models: list[str] | None = None,
        project_dir: Path | None = None,
    ) -> FlextResult[FlextMeltanoTypes.Processing.DbtTransformationResult]:
        """Run DBT transformations.

        Args:
            models: List of models to run (None for all)
            project_dir: DBT project directory

        Returns:
            FlextResult with DBT transformation results

        """
        try:
            args = []
            if models:
                args.extend(["--models"] + models)

            result = self._executor.execute_dbt_command("run", args)

            if result.is_failure:
                return FlextResult[
                    FlextMeltanoTypes.Processing.DbtTransformationResult
                ].fail(result.error or "DBT transformation failed")

            execution_result = result.unwrap()
            dbt_result: FlextMeltanoTypes.Processing.DbtTransformationResult = {
                "success": execution_result.success,
                "exit_code": execution_result.exit_code,
                "models_run": models or ["all"],
                "execution_method": "library_runner",
                "project_dir": str(project_dir) if project_dir else None,
                "execution_time": execution_result.execution_time,
                "output": execution_result.output,
                "error": execution_result.error,
            }

            return FlextResult[FlextMeltanoTypes.Processing.DbtTransformationResult].ok(
                dbt_result
            )

        except Exception as e:
            error_msg = f"DBT transformation failed: {e}"
            self._logger.exception(error_msg)
            return FlextResult[
                FlextMeltanoTypes.Processing.DbtTransformationResult
            ].fail(error_msg)

    def get_dbt_runner(self) -> FlextResult[FlextTypes.Dict]:
        """Get DBT runner instance for advanced DBT operations."""
        try:
            # Placeholder - real implementation would return DBT runner
            dbt_runner = {
                "type": "dbt_runner",
                "status": "available",
                "capabilities": ["run", "test", "docs", "seed"],
            }
            return FlextResult[FlextTypes.Dict].ok(dbt_runner)
        except Exception as e:
            return FlextResult[FlextTypes.Dict].fail(f"Failed to get DBT runner: {e}")

    def get_singer_manager(self) -> FlextResult[FlextTypes.Dict]:
        """Get Singer manager instance for advanced Singer operations."""
        try:
            # Placeholder - real implementation would return Singer manager
            singer_manager = {
                "type": "singer_manager",
                "status": "available",
                "capabilities": ["discover", "sync", "validate"],
            }
            return FlextResult[FlextTypes.Dict].ok(singer_manager)
        except Exception as e:
            return FlextResult[FlextTypes.Dict].fail(
                f"Failed to get Singer manager: {e}"
            )

    def execute_complete_elt_pipeline(
        self,
        tap_name: str,
        target_name: str,
        dbt_models: list[str] | None = None,
        config: dict[str, FlextTypes.JsonValue] | None = None,
    ) -> FlextResult[FlextMeltanoTypes.Processing.EltPipelineResult]:
        """Execute complete ELT pipeline with optional DBT transformations."""
        try:
            self._logger.info(
                "Starting complete ELT pipeline",
                tap_name=tap_name,
                target_name=target_name,
                dbt_models=dbt_models,
            )

            # Execute EL pipeline
            result = self._executor.execute_pipeline(tap_name, target_name, config)
            if result.is_failure:
                return FlextResult[FlextMeltanoTypes.Processing.EltPipelineResult].fail(
                    result.error or "EL pipeline execution failed"
                )

            execution_result = result.unwrap()
            elt_result: FlextMeltanoTypes.Processing.EltPipelineResult = {
                "success": execution_result.success,
                "tap_name": tap_name,
                "target_name": target_name,
                "execution_time": execution_result.execution_time,
                "exit_code": execution_result.exit_code,
                "output": execution_result.output,
                "error": execution_result.error,
            }

            # Execute DBT transformations if specified
            if dbt_models:
                dbt_result = self.run_dbt_transformation(dbt_models)
                if dbt_result.is_failure:
                    elt_result["dbt_success"] = False
                    elt_result["dbt_error"] = dbt_result.error
                else:
                    elt_result["dbt_success"] = True
                    elt_result["dbt_models_run"] = list(
                        dbt_models
                    )  # Convert to list[object]

            return FlextResult[FlextMeltanoTypes.Processing.EltPipelineResult].ok(
                elt_result
            )

        except Exception as e:
            error_msg = f"Complete ELT pipeline execution failed: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextMeltanoTypes.Processing.EltPipelineResult].fail(
                error_msg
            )


__all__ = ["FlextMeltanoLibraryRunner"]
