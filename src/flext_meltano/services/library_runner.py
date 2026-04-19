"""FLEXT Meltano Library Runner - Unified library runner for Meltano operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_meltano import (
    FlextMeltanoDbtTransformationRunner,
    FlextMeltanoExecutor,
    FlextMeltanoServiceBase,
    c,
    p,
    r,
    t,
    u,
)


class FlextMeltanoLibraryRunner(
    FlextMeltanoDbtTransformationRunner, FlextMeltanoServiceBase
):
    """Unified library runner mixin for MRO composition on FlextMeltano.

    Provides ELT pipeline execution and DBT transformation orchestration.
    """

    _elt_executor: p.Meltano.MeltanoExecutor = u.PrivateAttr(
        default_factory=FlextMeltanoExecutor,
    )

    def execute_complete_elt_pipeline(
        self,
        tap_name: str,
        target_name: str,
        dbt_models: t.StrSequence | None = None,
        settings: Mapping[str, t.Container] | None = None,
    ) -> p.Result[t.MutableRecursiveContainerMapping]:
        """Execute complete ELT pipeline with optional DBT transformations."""
        try:
            self.logger.info(
                "Starting complete ELT pipeline",
                tap_name=tap_name,
                target_name=target_name,
                dbt_models=str(dbt_models or []),
            )
            result = self._elt_executor.execute_pipeline(
                tap_name, target_name, settings
            )
            if result.failure:
                return r[t.MutableRecursiveContainerMapping].fail(
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
            elt_result: t.MutableRecursiveContainerMapping = {
                str(k): str(v) if not isinstance(v, (str, int, float, bool)) else v
                for k, v in payload.items()
            }
            if dbt_models:
                dbt_result = self.run_dbt_transformation(dbt_models)
                if dbt_result.failure:
                    elt_result["dbt_success"] = False
                    elt_result["dbt_error"] = dbt_result.error or ""
                else:
                    elt_result["dbt_success"] = True
                    elt_result["dbt_models_run"] = u.join(
                        dbt_models,
                        separator=",",
                    )
            return r[t.MutableRecursiveContainerMapping].ok(elt_result)
        except c.Meltano.OPERATION_ERRORS as e:
            error_msg = f"Complete ELT pipeline execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.MutableRecursiveContainerMapping].fail(error_msg)

    def run_dbt_transformation(
        self,
        models: t.StrSequence | None = None,
        project_dir: Path | None = None,
    ) -> p.Result[t.MutableRecursiveContainerMapping]:
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
        settings: Mapping[str, t.Container] | None = None,
    ) -> p.Result[t.MutableRecursiveContainerMapping]:
        """Run a complete ELT pipeline from tap to target."""
        try:
            self.logger.info(
                "Starting ELT pipeline",
                tap_name=tap.name,
                target_name=target.name,
            )
            result = self._elt_executor.execute_pipeline(
                tap.name, target.name, settings
            )
            if result.failure:
                return r[t.MutableRecursiveContainerMapping].fail(
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
            elt_result: t.MutableRecursiveContainerMapping = {
                str(k): str(v) if not isinstance(v, (str, int, float, bool)) else v
                for k, v in payload.items()
            }
            return r[t.MutableRecursiveContainerMapping].ok(elt_result)
        except c.Meltano.OPERATION_ERRORS as e:
            error_msg = f"ELT pipeline execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.MutableRecursiveContainerMapping].fail(error_msg)


__all__: list[str] = ["FlextMeltanoLibraryRunner"]
