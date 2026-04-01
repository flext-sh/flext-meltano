"""FLEXT Meltano Library Runner - Unified library runner for Meltano operations.

This module provides the FlextMeltanoLibraryRunner class for complete Meltano
functionality including ELT pipelines and DBT transformations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import MutableSequence
from pathlib import Path
from typing import override

from flext_core import r, s

from flext_meltano import FlextMeltanoBridge, FlextMeltanoExecutor, c, p, t, u


class FlextMeltanoDbtTransformationRunner:
    """Execute DBT transformations through the Meltano executor."""

    @staticmethod
    def execute_dbt_transformation(
        executor: FlextMeltanoExecutor,
        logger: p.Logger,
        models: t.StrSequence | None = None,
        project_dir: Path | None = None,
    ) -> r[t.Meltano.Processing.DbtTransformationResult]:
        """Run DBT `run` and normalize output into transformation contract."""
        try:
            args: MutableSequence[str] = []
            if models:
                args.extend([c.Meltano.Commands.MODELS_OPTION, *models])
            result = executor.execute_dbt_command(c.Meltano.Dbt.COMMAND_RUN, args)
            if result.is_failure:
                return r[t.Meltano.Processing.DbtTransformationResult].fail(
                    result.error or "DBT transformation failed",
                )
            execution_result = result.value
            dbt_result: t.Meltano.Processing.DbtTransformationResult = (
                u.Meltano.build_command_execution_payload(
                    execution_result,
                    extra_fields={
                        "models_run": u.join(models, separator=",")
                        if models
                        else "all",
                        "execution_method": "library_runner",
                        "project_dir": str(project_dir) if project_dir else "",
                    },
                    duration_field="execution_time",
                )
            )
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
        """Execute library runner — returns executor status."""
        return r[t.Meltano.ExecutionResultDict].fail(
            "Library runner execution requires meltano-core SDK integration"
        )

    def execute_complete_elt_pipeline(
        self,
        tap_name: str,
        target_name: str,
        dbt_models: t.StrSequence | None = None,
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
            elt_result: t.Meltano.Processing.EltPipelineResult = (
                u.Meltano.build_command_execution_payload(
                    execution_result,
                    extra_fields={
                        "tap_name": tap_name,
                        "target_name": target_name,
                    },
                    duration_field="execution_time",
                )
            )
            if dbt_models:
                dbt_result = self.run_dbt_transformation(dbt_models)
                if dbt_result.is_failure:
                    elt_result["dbt_success"] = False
                    elt_result["dbt_error"] = dbt_result.error or ""
                else:
                    elt_result["dbt_success"] = True
                    elt_result["dbt_models_run"] = u.join(
                        dbt_models,
                        separator=",",
                    )
            return r[t.Meltano.Processing.EltPipelineResult].ok(elt_result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Complete ELT pipeline execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.Meltano.Processing.EltPipelineResult].fail(error_msg)

    def run_dbt_transformation(
        self,
        models: t.StrSequence | None = None,
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
            elt_result: t.Meltano.Processing.EltPipelineResult = (
                u.Meltano.build_command_execution_payload(
                    execution_result,
                    extra_fields={
                        "tap_name": tap.name,
                        "target_name": target.name,
                    },
                    duration_field="execution_time",
                )
            )
            return r[t.Meltano.Processing.EltPipelineResult].ok(elt_result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"ELT pipeline execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.Meltano.Processing.EltPipelineResult].fail(error_msg)


__all__ = [
    "FlextMeltanoDbtTransformationRunner",
    "FlextMeltanoLibraryRunner",
]
