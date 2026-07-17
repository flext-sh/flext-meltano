"""FLEXT Meltano Library Runner - Unified library runner for Meltano operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

# NOTE (multi-agent, bead mro-wfc8.3): m only annotates the typed dbt return; runtime
# import not needed (from __future__ import annotations makes the annotation lazy).
from flext_meltano import FlextMeltanoServiceBase, c, p, r, settings, t, u
from flext_meltano.services.executor import FlextMeltanoExecutor


class FlextMeltanoLibraryRunner(FlextMeltanoServiceBase):
    """Unified library runner mixin for MRO composition on FlextMeltano.

    Provides ELT pipeline execution and DBT transformation orchestration.
    """

    _elt_executor: p.Meltano.Executor = u.PrivateAttr(
        default_factory=FlextMeltanoExecutor,
    )

    def execute_complete_elt_pipeline(
        self,
        tap_name: str,
        target_name: str,
        dbt_models: t.StrSequence | None = None,
        settings: t.JsonMapping | None = None,
    ) -> p.Result[t.JsonMapping]:
        """Execute complete ELT pipeline with optional DBT transformations."""

        def _run_execute_complete_elt_pipeline() -> p.Result[t.JsonMapping]:
            self.logger.info(
                "Starting complete ELT pipeline",
                tap_name=tap_name,
                target_name=target_name,
                dbt_models=str(dbt_models or []),
            )
            result = self._elt_executor.execute_pipeline(
                tap_name,
                target_name,
                settings,
            )
            if result.failure:
                return r[t.JsonMapping].fail(
                    result.error or "EL pipeline execution failed",
                )
            execution_result = result.value
            elt_result = u.Meltano.build_mutable_command_execution_payload(
                execution_result,
                extra_fields={
                    "tap_name": tap_name,
                    "target_name": target_name,
                },
                duration_field="execution_time",
            )
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
            return r[t.JsonMapping].ok(elt_result)

        try:
            return _run_execute_complete_elt_pipeline()
        except c.Meltano.OPERATION_ERRORS as e:
            error_msg = f"Complete ELT pipeline execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.JsonMapping].fail(error_msg)

    def run_dbt_transformation(
        self,
        models: t.StrSequence | None = None,
        project_dir: Path | None = None,
    ) -> p.Result[p.Meltano.CommandExecutionResult]:
        """Run DBT transformation using the configured Meltano executor.

        Returns the executor's typed CommandExecutionResult directly (SSOT). Callers
        read its fields (success/output/error/exit_code/execution_time) — no dict
        degradation (# NOTE multi-agent, bead mro-wfc8.3: was r[t.JsonMapping] via
        build_mutable_command_execution_payload; that flattened the typed model to a
        dict whose models_run/execution_method keys never existed).
        """
        executor = (
            FlextMeltanoExecutor(
                settings=settings.model_copy(update={"project_root": project_dir}),
            )
            if project_dir is not None
            else self._elt_executor
        )
        return executor.execute_dbt_command(
            c.Meltano.DbtCommand.RUN,
            models,
        )

    def run_elt_pipeline(
        self,
        tap: p.Meltano.SingerTap,
        target: p.Meltano.SingerTarget,
        settings: t.JsonMapping | None = None,
    ) -> p.Result[t.JsonMapping]:
        """Run a complete ELT pipeline from tap to target."""
        try:
            self.logger.info(
                "Starting ELT pipeline",
                tap_name=tap.name,
                target_name=target.name,
            )
            result = self._elt_executor.execute_pipeline(
                tap.name,
                target.name,
                settings,
            )
            if result.failure:
                return r[t.JsonMapping].fail(
                    result.error or "Pipeline execution failed",
                )
            execution_result = result.value
            elt_result = u.Meltano.build_mutable_command_execution_payload(
                execution_result,
                extra_fields={
                    "tap_name": tap.name,
                    "target_name": target.name,
                },
                duration_field="execution_time",
            )
            return r[t.JsonMapping].ok(elt_result)
        except c.Meltano.OPERATION_ERRORS as e:
            error_msg = f"ELT pipeline execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.JsonMapping].fail(error_msg)


__all__: list[str] = ["FlextMeltanoLibraryRunner"]
