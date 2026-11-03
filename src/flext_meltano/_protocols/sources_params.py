# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_meltano/_protocols/sources_params
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_cli import p

    from flext_meltano import t


class FlextMeltanoProtocolsSourcesParams:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class StreamDefinition(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        stream_name: str
        stream_schema: t.FlatContainerMapping
        source_type: str
        status: str
        records_extracted: t.NonNegativeInt


__all__: list[str] = [
    "FlextMeltanoProtocolsSourcesParams",
]
