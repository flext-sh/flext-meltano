"""Extended adapter classes for pipeline and DBT operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import FlextSettings, r, s
from flext_meltano import FlextMeltanoExecutorBase, FlextMeltanoSettings, c, m, t, u


class FlextMeltanoPipelineAdapter(s[t.ContainerMapping]):
    """Focused adapter for Meltano pipeline execution following SOLID principles."""

    @classmethod
    @override
    def _get_service_config_type(cls) -> type[FlextSettings]:
        return FlextMeltanoSettings

    @override
    def execute(self) -> r[t.ContainerMapping]:
        """Execute default pipeline operation."""
        return r[t.ContainerMapping].ok({
            "status": c.Meltano.OperationStatus.READY,
        })

    def execute_pipeline(
        self,
        tap_name: str,
        target_name: str,
    ) -> r[t.ContainerMapping]:
        """Execute ELT pipeline using Meltano runtime."""
        try:
            if not tap_name.startswith(c.Meltano.PREFIX_TAP):
                return r[t.ContainerMapping].fail(
                    f"Invalid tap name format: {tap_name}"
                )
            if not target_name.startswith(c.Meltano.PREFIX_TARGET):
                return r[t.ContainerMapping].fail(
                    f"Invalid target name format: {target_name}"
                )
            executor = FlextMeltanoExecutorBase()
            execution_result = executor.execute_meltano_command(
                u.Meltano.build_pipeline_runtime_command(tap_name, target_name),
                _cwd=u.Meltano.resolve_project_root(self.settings.model_dump()),
            )
            if execution_result.is_failure:
                return r[t.ContainerMapping].fail(
                    execution_result.error or "Pipeline execution failed"
                )
            command_result: m.Meltano.CommandExecutionResult = execution_result.value
            pipeline_result: t.ContainerMapping = (
                u.Meltano.build_command_execution_payload(
                    command_result,
                    extra_fields={
                        "tap": tap_name,
                        "target": target_name,
                    },
                    success_status=c.Meltano.StreamStatus.COMPLETED,
                    failure_status=c.Meltano.StreamStatus.FAILED,
                    duration_field="execution_duration",
                )
            )
            return r[t.ContainerMapping].ok(pipeline_result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as ex:
            return r[t.ContainerMapping].fail(f"Pipeline execution failed: {ex}")


class FlextMeltanoDbtAdapter(s[t.ContainerMapping]):
    """Focused adapter for DBT operations following SOLID principles."""

    @override
    @classmethod
    def _get_service_config_type(cls) -> type[FlextSettings]:
        return FlextMeltanoSettings

    @override
    def execute(self) -> r[t.ContainerMapping]:
        """Execute default DBT operation."""
        return self.execute_dbt_operation()

    def execute_dbt_operation(self) -> r[t.ContainerMapping]:
        """Execute DBT operation via Meltano runtime."""
        try:
            executor = FlextMeltanoExecutorBase()
            execution_result = executor.execute_meltano_command(
                u.Meltano.build_dbt_runtime_command(c.Meltano.DBT_COMMAND_RUN),
                _cwd=u.Meltano.resolve_project_root(self.settings.model_dump()),
            )
            if execution_result.is_failure:
                return r[t.ContainerMapping].fail(
                    execution_result.error or "DBT operation failed"
                )
            command_result: m.Meltano.CommandExecutionResult = execution_result.value
            dbt_result: t.ContainerMapping = u.Meltano.build_command_execution_payload(
                command_result,
                success_status=c.Meltano.StreamStatus.COMPLETED,
                failure_status=c.Meltano.StreamStatus.FAILED,
                duration_field="execution_time",
            )
            return r[t.ContainerMapping].ok(dbt_result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as ex:
            return r[t.ContainerMapping].fail(f"DBT operation failed: {ex}")


__all__ = ["FlextMeltanoDbtAdapter", "FlextMeltanoPipelineAdapter"]
