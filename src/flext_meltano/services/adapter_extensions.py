"""Extended adapter classes for pipeline and DBT operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import subprocess
import time
from typing import override

from flext_core import FlextSettings, r, s

from flext_meltano import FlextMeltanoSettings, c, t


class FlextMeltanoPipelineAdapter(s[t.Meltano.ExecutionResultDict]):
    """Focused adapter for Meltano pipeline execution following SOLID principles."""

    @classmethod
    @override
    def _get_service_config_type(cls) -> type[FlextSettings]:
        return FlextMeltanoSettings

    @override
    def execute(self) -> r[t.Meltano.ExecutionResultDict]:
        """Execute default pipeline operation."""
        return r[t.Meltano.ExecutionResultDict].ok({
            "status": c.Meltano.Enums.OperationStatus.READY,
        })

    def execute_pipeline(
        self,
        tap_name: str,
        target_name: str,
    ) -> r[t.Meltano.ExecutionResultDict]:
        """Execute ELT pipeline using Meltano CLI."""
        try:
            if not tap_name.startswith("tap-"):
                return r[t.Meltano.ExecutionResultDict].fail(
                    f"Invalid tap name format: {tap_name}"
                )
            if not target_name.startswith("target-"):
                return r[t.Meltano.ExecutionResultDict].fail(
                    f"Invalid target name format: {target_name}"
                )
            start = time.monotonic()
            proc = subprocess.run(
                ["meltano", "elt", tap_name, target_name],  # noqa: S607
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )
            duration = time.monotonic() - start
            execution_result: t.Meltano.ExecutionResultDict = {
                "tap": tap_name,
                "target": target_name,
                "status": (
                    c.Meltano.Enums.StreamStatus.COMPLETED
                    if proc.returncode == 0
                    else c.Meltano.Enums.StreamStatus.FAILED
                ),
                "success": proc.returncode == 0,
                "output": proc.stdout,
                "error": proc.stderr,
                "execution_duration": duration,
            }
            return r[t.Meltano.ExecutionResultDict].ok(execution_result)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            subprocess.TimeoutExpired,
        ) as ex:
            return r[t.Meltano.ExecutionResultDict].fail(
                f"Pipeline execution failed: {ex}"
            )


class FlextMeltanoDbtAdapter(s[t.Meltano.DbtResultDict]):
    """Focused adapter for DBT operations following SOLID principles."""

    @override
    @classmethod
    def _get_service_config_type(cls) -> type[FlextSettings]:
        return FlextMeltanoSettings

    @override
    def execute(self) -> r[t.Meltano.DbtResultDict]:
        """Execute default DBT operation."""
        return self.execute_dbt_operation()

    def execute_dbt_operation(self) -> r[t.Meltano.DbtResultDict]:
        """Execute DBT operation via Meltano invoke."""
        try:
            start = time.monotonic()
            proc = subprocess.run(
                ["meltano", "invoke", "dbt-postgres:run"],  # noqa: S607
                capture_output=True,
                text=True,
                timeout=600,
                check=False,
            )
            duration = time.monotonic() - start
            dbt_result: t.Meltano.DbtResultDict = {
                "status": (
                    c.Meltano.Enums.StreamStatus.COMPLETED
                    if proc.returncode == 0
                    else c.Meltano.Enums.StreamStatus.FAILED
                ),
                "success": proc.returncode == 0,
                "output": proc.stdout,
                "error": proc.stderr,
                "execution_time": duration,
            }
            return r[t.Meltano.DbtResultDict].ok(dbt_result)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            subprocess.TimeoutExpired,
        ) as ex:
            return r[t.Meltano.DbtResultDict].fail(f"DBT operation failed: {ex}")


__all__ = ["FlextMeltanoDbtAdapter", "FlextMeltanoPipelineAdapter"]
