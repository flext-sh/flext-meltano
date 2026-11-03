# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_meltano/_protocols/results_dbt
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_meltano import t


class FlextMeltanoProtocolsResultsDbt:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class CommandExecutionResult(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        command: Sequence[str]
        success: bool
        exit_code: int
        output: str
        error: str
        execution_time: t.NonNegativeFloat

        @property
        def timestamp(self) -> str:
            """ISO timestamp of when the result was generated."""
            ...


__all__: list[str] = [
    "FlextMeltanoProtocolsResultsDbt",
]
