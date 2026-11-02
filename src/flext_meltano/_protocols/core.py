# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_meltano/_protocols/core
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_cli import FlextCliProtocols, t


class FlextMeltanoProtocolsCore:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class StringListValue(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def items(self) -> t.StrTuple:
            """Normalized tuple of string values."""
            ...


__all__: list[str] = [
    "FlextMeltanoProtocolsCore",
]
