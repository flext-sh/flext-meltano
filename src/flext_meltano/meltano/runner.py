"""FLEXT Meltano Library Runner - Unified library runner for Meltano operations.

This module provides the FlextMeltanoLibraryRunner class for complete Meltano
functionality including ELT pipelines and DBT transformations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

from flext_core import (
    FlextResult,
    FlextService,
    t as t_core,
)

from flext_meltano.bridge import FlextMeltanoBridge
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.executor import FlextMeltanoExecutor
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.singer_protocols import SingerTap, SingerTarget
from flext_meltano.typings import FlextMeltanoTypes

# Import aliases for simplified usage
# u is already imported from flext_core
r = FlextResult
s = FlextService
t_base = t_core
t = FlextMeltanoTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels


class FlextMeltanoLibraryRunner(FlextService[t.MeltanoCore.ExecutionResultDict]):
    """Unified library runner providing complete Meltano functionality.

    This class consolidates all Meltano operations (DBT transformations, Singer
    protocols, ELT pipelines) into a single, well-structured interface following
    Zero Tolerance architectural principles.
    """

    def __init__(self) -> None:
        """Initialize the library runner."""
        super().__init__()
        self._executor = FlextMeltanoExecutor()
        self._bridge = FlextMeltanoBridge()

    def run_elt_pipeline(
        self,
        tap: SingerTap,
        target: SingerTarget,
        config: dict[str, t_base.JsonValue] | None = None,
    ) -> r[t.Processing.EltPipelineResult]:
        """Run a complete ELT pipeline from tap to target.

        Args:
        tap: Singer tap to extract data from
        target: Singer target to load data into
        config: Pipeline configuration

        Returns:
        FlextResult with ELT pipeline execution results

        """
        try:
            self.logger.info(
                "Starting ELT pipeline",
                tap_name=tap.name,
                target_name=target.name,
            )

            # Execute the pipeline using the executor
            result = self._executor.execute_pipeline(tap.name, target.name, config)

            if result.is_failure:
                return r[t.Processing.EltPipelineResult].fail(
                    result.error or "Pipeline execution failed",
                )

            # Convert execution result to ELT pipeline result
            execution_result = result.value
            elt_result: t.Processing.EltPipelineResult = {
                "success": execution_result.is_success,
                "tap_name": tap.name,
                "target_name": target.name,
                "execution_time": execution_result.execution_time,
                "exit_code": execution_result.exit_code,
                "output": execution_result.output,
                "error": execution_result.error,
            }

            return r[t.Processing.EltPipelineResult].ok(elt_result)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"ELT pipeline execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.Processing.EltPipelineResult].fail(error_msg)

    def run_dbt_transformation(
        self,
        models: list[str] | None = None,
        project_dir: Path | None = None,
    ) -> r[t.Processing.DbtTransformationResult]:
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
                return r[t.Processing.DbtTransformationResult].fail(
                    result.error or "DBT transformation failed",
                )

            execution_result = result.value
            dbt_result: t.Processing.DbtTransformationResult = {
                "success": execution_result.is_success,
                "exit_code": execution_result.exit_code,
                "models_run": models or ["all"],
                "execution_method": "library_runner",
                "project_dir": str(project_dir) if project_dir else None,
                "execution_time": execution_result.execution_time,
                "output": execution_result.output,
                "error": execution_result.error,
            }

            return r[t.Processing.DbtTransformationResult].ok(dbt_result)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"DBT transformation failed: {e}"
            self.logger.exception(error_msg)
            return r[t.Processing.DbtTransformationResult].fail(error_msg)

    @staticmethod
    def get_dbt_runner() -> r[t.MeltanoCore.ExecutionResultDict]:
        """Get DBT runner instance for DBT operations."""
        try:
            # Placeholder - real implementation would return DBT runner
            dbt_runner: t.MeltanoCore.ExecutionResultDict = {
                "type": "dbt_runner",
                "status": "available",
                "capabilities": ["run", "test", "docs", "seed"],
            }
            return r[t.MeltanoCore.ExecutionResultDict].ok(dbt_runner)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.MeltanoCore.ExecutionResultDict].fail(
                f"Failed to get DBT runner: {e}"
            )

    @staticmethod
    def get_singer_manager() -> r[t.MeltanoCore.ExecutionResultDict]:
        """Get Singer manager instance for Singer operations."""
        try:
            # Placeholder - real implementation would return Singer manager
            singer_manager: t.MeltanoCore.ExecutionResultDict = {
                "type": "singer_manager",
                "status": "available",
                "capabilities": ["discover", "sync", "validate"],
            }
            return r[t.MeltanoCore.ExecutionResultDict].ok(singer_manager)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.MeltanoCore.ExecutionResultDict].fail(
                f"Failed to get Singer manager: {e}"
            )

    def execute_complete_elt_pipeline(
        self,
        tap_name: str,
        target_name: str,
        dbt_models: list[str] | None = None,
        config: dict[str, t_base.JsonValue] | None = None,
    ) -> r[t.Processing.EltPipelineResult]:
        """Execute complete ELT pipeline with optional DBT transformations."""
        try:
            self.logger.info(
                "Starting complete ELT pipeline",
                tap_name=tap_name,
                target_name=target_name,
                dbt_models=dbt_models,
            )

            # Execute EL pipeline
            result = self._executor.execute_pipeline(tap_name, target_name, config)
            if result.is_failure:
                return r[t.Processing.EltPipelineResult].fail(
                    result.error or "EL pipeline execution failed",
                )

            execution_result = result.value
            elt_result: t.Processing.EltPipelineResult = {
                "success": execution_result.is_success,
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
                        dbt_models,
                    )  # Convert to list[t.GeneralValueType]

            return r[t.Processing.EltPipelineResult].ok(elt_result)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Complete ELT pipeline execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.Processing.EltPipelineResult].fail(error_msg)


__all__ = ["FlextMeltanoLibraryRunner"]
