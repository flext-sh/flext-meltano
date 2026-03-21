"""FLEXT Meltano Library Runner - Unified library runner for Meltano operations.

This module provides the FlextMeltanoLibraryRunner class for complete Meltano
functionality including ELT pipelines and DBT transformations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_core import s
from flext_core.result import r

from flext_meltano.executor import FlextMeltanoExecutor
from flext_meltano.meltano.bridge import FlextMeltanoBridge
from flext_meltano.protocols import FlextMeltanoProtocols as p
from flext_meltano.typings import FlextMeltanoTypes as t


class FlextMeltanoDbtTransformationRunner:
    """Execute DBT transformations through the Meltano executor."""

    @staticmethod
    def execute_dbt_transformation(
        executor: FlextMeltanoExecutor,
        logger: p.Logger,
        models: list[str] | None = None,
        project_dir: Path | None = None,
    ) -> r[t.Meltano.Processing.DbtTransformationResult]:
        """Run DBT `run` and normalize output into transformation contract."""
        try:
            args: list[str] = []
            if models:
                args.extend(["--models"] + models)
            result = executor.execute_dbt_command("run", args)
            if result.is_failure:
                return r[t.Meltano.Processing.DbtTransformationResult].fail(
                    result.error or "DBT transformation failed",
                )
            execution_result = result.value
            dbt_result: t.Meltano.Processing.DbtTransformationResult = {
                "success": execution_result.success,
                "exit_code": execution_result.exit_code,
                "models_run": ",".join(models) if models else "all",
                "execution_method": "library_runner",
                "project_dir": str(project_dir) if project_dir else "",
                "execution_time": execution_result.execution_time,
                "output": execution_result.output or "",
                "error": execution_result.error or "",
            }
            return r[t.Meltano.Processing.DbtTransformationResult].ok(dbt_result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"DBT transformation failed: {e}"
            logger.exception(error_msg)
            return r[t.Meltano.Processing.DbtTransformationResult].fail(error_msg)


class FlextMeltanoLibraryRunner(
    FlextMeltanoDbtTransformationRunner,
    s[t.Meltano.ExecutionResultDict],
):
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

    @override
    def execute(self) -> r[t.Meltano.ExecutionResultDict]:
        """Execute library runner logic."""
        try:
            return r[t.Meltano.ExecutionResultDict].ok({"status": "ready"})
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            return r[t.Meltano.ExecutionResultDict].fail(
                f"Runner execution failed: {e}",
            )

    @staticmethod
    def get_dbt_runner() -> r[t.Meltano.ExecutionResultDict]:
        """Get DBT runner instance for DBT operations."""
        try:
            dbt_runner: t.Meltano.ExecutionResultDict = {
                "type": "dbt_runner",
                "status": "available",
                "capabilities": ["run", "test", "docs", "seed"],
            }
            return r[t.Meltano.ExecutionResultDict].ok(dbt_runner)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.Meltano.ExecutionResultDict].fail(
                f"Failed to get DBT runner: {e}",
            )

    @staticmethod
    def get_singer_manager() -> r[t.Meltano.ExecutionResultDict]:
        """Get Singer manager instance for Singer operations."""
        try:
            singer_manager: t.Meltano.ExecutionResultDict = {
                "type": "singer_manager",
                "status": "available",
                "capabilities": ["discover", "sync", "validate"],
            }
            return r[t.Meltano.ExecutionResultDict].ok(singer_manager)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.Meltano.ExecutionResultDict].fail(
                f"Failed to get Singer manager: {e}",
            )

    def execute_complete_elt_pipeline(
        self,
        tap_name: str,
        target_name: str,
        dbt_models: list[str] | None = None,
        config: t.Meltano.MeltanoConfigDict | None = None,
    ) -> r[t.Meltano.Processing.EltPipelineResult]:
        """Execute complete ELT pipeline with optional DBT transformations."""
        try:
            self.logger.info(
                "Starting complete ELT pipeline",
                tap_name=tap_name,
                target_name=target_name,
                dbt_models=str(dbt_models or []),
            )
            result = self._executor.execute_pipeline(tap_name, target_name, config)
            if result.is_failure:
                return r[t.Meltano.Processing.EltPipelineResult].fail(
                    result.error or "EL pipeline execution failed",
                )
            execution_result = result.value
            elt_result: dict[str, object] = {
                "success": execution_result.success,
                "tap_name": tap_name,
                "target_name": target_name,
                "execution_time": execution_result.execution_time,
                "exit_code": execution_result.exit_code,
                "output": execution_result.output or "",
                "error": execution_result.error or "",
            }
            if dbt_models:
                dbt_result = self.run_dbt_transformation(dbt_models)
                if dbt_result.is_failure:
                    elt_result["dbt_success"] = False
                    elt_result["dbt_error"] = dbt_result.error or ""
                else:
                    elt_result["dbt_success"] = True
                    elt_result["dbt_models_run"] = ",".join(dbt_models)
            return r[t.Meltano.Processing.EltPipelineResult].ok(elt_result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Complete ELT pipeline execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.Meltano.Processing.EltPipelineResult].fail(error_msg)

    def run_dbt_transformation(
        self,
        models: list[str] | None = None,
        project_dir: Path | None = None,
    ) -> r[t.Meltano.Processing.DbtTransformationResult]:
        """Run DBT transformation using the shared executor and logger."""
        return FlextMeltanoDbtTransformationRunner.execute_dbt_transformation(
            executor=self._executor,
            logger=self.logger,
            models=models,
            project_dir=project_dir,
        )

    def run_elt_pipeline(
        self,
        tap: p.Meltano.SingerTap,
        target: p.Meltano.SingerTarget,
        config: t.Meltano.MeltanoConfigDict | None = None,
    ) -> r[t.Meltano.Processing.EltPipelineResult]:
        """Run a complete ELT pipeline from tap to target.

        Args:
        tap: Singer tap to extract data from
        target: Singer target to load data into
        config: Pipeline configuration

        Returns:
        r with ELT pipeline execution results

        """
        try:
            self.logger.info(
                "Starting ELT pipeline",
                tap_name=tap.name,
                target_name=target.name,
            )
            result = self._executor.execute_pipeline(tap.name, target.name, config)
            if result.is_failure:
                return r[t.Meltano.Processing.EltPipelineResult].fail(
                    result.error or "Pipeline execution failed",
                )
            execution_result = result.value
            elt_result: dict[str, object] = {
                "success": execution_result.success,
                "tap_name": tap.name,
                "target_name": target.name,
                "execution_time": execution_result.execution_time,
                "exit_code": execution_result.exit_code,
                "output": execution_result.output,
                "error": execution_result.error,
            }
            return r[t.Meltano.Processing.EltPipelineResult].ok(elt_result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"ELT pipeline execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.Meltano.Processing.EltPipelineResult].fail(error_msg)


__all__ = [
    "FlextMeltanoDbtTransformationRunner",
    "FlextMeltanoLibraryRunner",
]
