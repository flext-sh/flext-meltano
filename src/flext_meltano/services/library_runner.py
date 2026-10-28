"""FLEXT Meltano Library Runner - Unified library runner for Meltano operations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from flext_meltano import FlextMeltanoServiceBase, c, m, p, settings
from flext_meltano.services import FlextMeltanoExecutor

if TYPE_CHECKING:
    from pathlib import Path


class FlextMeltanoLibraryRunner(FlextMeltanoServiceBase):
    """Unified library runner mixin for MRO composition on FlextMeltano.

    Provides DBT transformation orchestration.
    """

    _elt_executor: p.Meltano.MeltanoExecutor = m.PrivateAttr(
        default_factory=FlextMeltanoExecutor,
    )

    def run_dbt_transformation(
        self,
        models: Sequence[str] | None = None,
        project_dir: Path | None = None,
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Run DBT transformation using the configured Meltano executor.

        Returns the executor's typed CommandExecutionResult directly (SSOT). Callers
        read its fields (success/output/error/exit_code/execution_time) — no dict
        degradation (# NOTE multi-agent, bead mro-wfc8.3: was r[t.JsonMapping] via
        build_mutable_command_execution_payload; that flattened the typed model to a
        dict whose models_run/execution_method keys never existed).

        Returns:
            The resulting ``p.Result[m.Meltano.CommandExecutionResult]``.

        """
        executor = (
            FlextMeltanoExecutor(
                runtime_settings=settings.model_copy(
                    update={"project_root": project_dir}
                ),
            )
            if project_dir is not None
            else self._elt_executor
        )
        return executor.execute_dbt_command(c.Meltano.DbtCommand.RUN, models)


__all__: list[str] = ["FlextMeltanoLibraryRunner"]
