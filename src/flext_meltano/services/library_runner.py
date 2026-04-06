"""FLEXT Meltano Library Runner - Unified library runner for Meltano operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from pydantic import PrivateAttr

from flext_core import r
from flext_meltano import (
    FlextMeltanoBridge,
    FlextMeltanoDbtTransformationRunner,
    FlextMeltanoExecutor,
    FlextMeltanoServiceBase,
    c,
    p,
    t,
    u,
)


class FlextMeltanoLibraryRunner(
    FlextMeltanoDbtTransformationRunner, FlextMeltanoServiceBase
):
    """Unified library runner mixin for MRO composition on FlextMeltano.

    Provides ELT pipeline execution and DBT transformation orchestration.
    """

    _elt_executor: FlextMeltanoExecutor = PrivateAttr(
        default_factory=FlextMeltanoExecutor,
    )
    _elt_bridge: FlextMeltanoBridge = PrivateAttr(
        default_factory=FlextMeltanoBridge,
    )

    def execute_complete_elt_pipeline(
        self,
        tap_name: str,
        target_name: str,
        dbt_models: t.StrSequence | None = None,
        config: t.ContainerMapping | None = None,
    ) -> r[t.MutableContainerMapping]:
        """Execute complete ELT pipeline with optional DBT transformations."""
        try:
            self.logger.info(
                "Starting complete ELT pipeline",
                tap_name=tap_name,
                target_name=target_name,
                dbt_models=str(dbt_models or []),
            )
            result = self._elt_executor.execute_pipeline(tap_name, target_name, config)
            if result.is_failure:
                return r[t.MutableContainerMapping].fail(
                    result.error or "EL pipeline execution failed",
                )
            execution_result = result.value
            payload = u.Meltano.build_command_execution_payload(
                execution_result,
                extra_fields={
                    "tap_name": tap_name,
                    "target_name": target_name,
                },
                duration_field="execution_time",
            )
            elt_result: t.MutableContainerMapping = {
                str(k): str(v) if not isinstance(v, (str, int, float, bool)) else v
                for k, v in payload.items()
            }
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
            return r[t.MutableContainerMapping].ok(elt_result)
        except c.Meltano.OPERATION_ERRORS as e:
            error_msg = f"Complete ELT pipeline execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.MutableContainerMapping].fail(error_msg)

    def run_dbt_transformation(
        self,
        models: t.StrSequence | None = None,
        project_dir: Path | None = None,
    ) -> r[t.MutableContainerMapping]:
        """Run DBT transformation using the configured Meltano executor."""
        return FlextMeltanoDbtTransformationRunner.execute_dbt_transformation(
            executor=self._elt_executor,
            logger=self.logger,
            models=models,
            project_dir=project_dir,
        )

    def run_elt_pipeline(
        self,
        tap: p.Meltano.SingerTap,
        target: p.Meltano.SingerTarget,
        config: t.ContainerMapping | None = None,
    ) -> r[t.MutableContainerMapping]:
        """Run a complete ELT pipeline from tap to target."""
        try:
            self.logger.info(
                "Starting ELT pipeline",
                tap_name=tap.name,
                target_name=target.name,
            )
            result = self._elt_executor.execute_pipeline(tap.name, target.name, config)
            if result.is_failure:
                return r[t.MutableContainerMapping].fail(
                    result.error or "Pipeline execution failed",
                )
            execution_result = result.value
            payload = u.Meltano.build_command_execution_payload(
                execution_result,
                extra_fields={
                    "tap_name": tap.name,
                    "target_name": target.name,
                },
                duration_field="execution_time",
            )
            elt_result: t.MutableContainerMapping = {
                str(k): str(v) if not isinstance(v, (str, int, float, bool)) else v
                for k, v in payload.items()
            }
            return r[t.MutableContainerMapping].ok(elt_result)
        except c.Meltano.OPERATION_ERRORS as e:
            error_msg = f"ELT pipeline execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.MutableContainerMapping].fail(error_msg)


__all__ = ["FlextMeltanoLibraryRunner"]
