# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_meltano/_protocols/results_dbt
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_meltano import t


class FlextMeltanoProtocolsResultsDbt:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class CommandExecutionResult(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def command(self) -> Sequence[str]:
            """Command that was executed."""
            ...

        @property
        def success(self) -> bool:
            """Whether the command succeeded."""
            ...

        @property
        def exit_code(self) -> int:
            """Process exit code."""
            ...

        @property
        def output(self) -> str:
            """Standard output."""
            ...

        @property
        def error(self) -> str:
            """Standard error."""
            ...

        @property
        def execution_time(self) -> t.NonNegativeFloat:
            """Execution time in seconds."""
            ...

        @property
        def timestamp(self) -> str:
            """ISO timestamp of when the result was generated."""
            ...


__all__: list[str] = [
    "FlextMeltanoProtocolsResultsDbt",
]
