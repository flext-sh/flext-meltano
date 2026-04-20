"""Extended adapter classes for pipeline and DBT operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
)
from typing import override

from flext_core import FlextSettings
from flext_meltano import (
    FlextMeltanoExecutorBase,
    FlextMeltanoServiceBase,
    FlextMeltanoSettings,
    c,
    m,
    p,
    r,
    t,
    u,
)


class FlextMeltanoPipelineAdapter(FlextMeltanoServiceBase):
    """Focused adapter for Meltano pipeline execution following SOLID principles."""

    @classmethod
    def _get_service_config_type(cls) -> type[FlextSettings]:
        return FlextMeltanoSettings

    @override
    def execute(self) -> p.Result[Mapping[str, t.Container]]:
        """Execute default pipeline operation."""
        return r[Mapping[str, t.Container]].ok({
            "status": c.Meltano.OperationStatus.READY,
        })

    def execute_pipeline(
        self,
        tap_name: str,
        target_name: str,
    ) -> p.Result[Mapping[str, t.Container]]:
        """Execute ELT pipeline using Meltano runtime."""
        try:
            if not tap_name.startswith(c.Meltano.PREFIX_TAP):
                return r[Mapping[str, t.Container]].fail(
                    f"Invalid tap name format: {tap_name}"
                )
            if not target_name.startswith(c.Meltano.PREFIX_TARGET):
                return r[Mapping[str, t.Container]].fail(
                    f"Invalid target name format: {target_name}"
                )
            executor = FlextMeltanoExecutorBase()
            project_root = u.Meltano.resolve_project_root(self.settings)
            execution_result = executor.execute_meltano_command(
                [c.Meltano.CMD_RUN, tap_name, target_name],
                _cwd=project_root,
            )
            if execution_result.failure:
                return r[Mapping[str, t.Container]].fail(
                    execution_result.error or "Pipeline execution failed"
                )
            command_result: m.Meltano.CommandExecutionResult = execution_result.value
            pipeline_result: Mapping[str, t.Container] = {
                "status": c.Meltano.StreamStatus.COMPLETED
                if command_result.success
                else c.Meltano.StreamStatus.FAILED,
                "execution_duration": command_result.execution_time,
                "tap": tap_name,
                "target": target_name,
                "command": command_result.command,
                "output": command_result.output,
                "error": command_result.error,
            }
            return r[Mapping[str, t.Container]].ok(pipeline_result)
        except c.Meltano.OPERATION_ERRORS as ex:
            return r[Mapping[str, t.Container]].fail(f"Pipeline execution failed: {ex}")


class FlextMeltanoDbtAdapter(FlextMeltanoServiceBase):
    """Focused adapter for DBT operations following SOLID principles."""

    @classmethod
    def _get_service_config_type(cls) -> type[FlextSettings]:
        return FlextMeltanoSettings

    @override
    def execute(self) -> p.Result[Mapping[str, t.Container]]:
        """Execute default DBT operation."""
        return self.execute_dbt_operation()

    def execute_dbt_operation(self) -> p.Result[Mapping[str, t.Container]]:
        """Execute DBT operation via Meltano runtime."""
        try:
            executor = FlextMeltanoExecutorBase()
            project_root = u.Meltano.resolve_project_root(self.settings)
            execution_result = executor.execute_meltano_command(
                [
                    c.Meltano.CMD_INVOKE,
                    c.Meltano.PLUGIN_DBT_DEFAULT_NAME,
                    c.Meltano.DBT_COMMAND_RUN,
                ],
                _cwd=project_root,
            )
            if execution_result.failure:
                return r[Mapping[str, t.Container]].fail(
                    execution_result.error or "DBT operation failed"
                )
            command_result: m.Meltano.CommandExecutionResult = execution_result.value
            dbt_result: Mapping[str, t.Container] = {
                "status": c.Meltano.StreamStatus.COMPLETED
                if command_result.success
                else c.Meltano.StreamStatus.FAILED,
                "execution_time": command_result.execution_time,
                "command": command_result.command,
                "output": command_result.output,
                "error": command_result.error,
            }
            return r[Mapping[str, t.Container]].ok(dbt_result)
        except c.Meltano.OPERATION_ERRORS as ex:
            return r[Mapping[str, t.Container]].fail(f"DBT operation failed: {ex}")


__all__: list[str] = ["FlextMeltanoDbtAdapter", "FlextMeltanoPipelineAdapter"]
