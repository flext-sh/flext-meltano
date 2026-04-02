"""DBT Transformation Runner — executes dbt via Meltano executor.

Moved from meltano/runner.py. Provides static transformation execution
used by FlextMeltanoLibraryRunner (services/library_runner.py).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableSequence
from pathlib import Path

from flext_core import r

from flext_meltano import FlextMeltanoExecutor, c, p, t, u


class FlextMeltanoDbtTransformationRunner:
    """Execute DBT transformations through the Meltano executor."""

    @staticmethod
    def execute_dbt_transformation(
        executor: FlextMeltanoExecutor,
        logger: p.Logger,
        models: t.StrSequence | None = None,
        project_dir: Path | None = None,
    ) -> r[t.Meltano.Processing.DbtTransformationResult]:
        """Run DBT ``run`` and normalize output into transformation contract."""
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
            payload = u.Meltano.build_command_execution_payload(
                execution_result,
                extra_fields={
                    "models_run": u.join(models, separator=",") if models else "all",
                    "execution_method": "library_runner",
                    "project_dir": str(project_dir) if project_dir else "",
                },
                duration_field="execution_time",
            )
            dbt_result: t.Meltano.Processing.DbtTransformationResult = {
                str(k): str(v) if not isinstance(v, (str, int, float, bool)) else v
                for k, v in payload.items()
            }
            return r[t.Meltano.Processing.DbtTransformationResult].ok(dbt_result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"DBT transformation failed: {e}"
            logger.exception(error_msg)
            return r[t.Meltano.Processing.DbtTransformationResult].fail(error_msg)


__all__ = ["FlextMeltanoDbtTransformationRunner"]
