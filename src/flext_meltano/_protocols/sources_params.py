# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_meltano/_protocols/sources_params
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols, t

if TYPE_CHECKING:
    from flext_cli import p


class FlextMeltanoProtocolsSourcesParams:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class StreamDefinition(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        @property
        def stream_name(self) -> str:
            """Name of the stream."""
            ...

        @property
        def stream_schema(self) -> t.FlatContainerMapping:
            """JSON schema for the stream."""
            ...

        @property
        def source_type(self) -> str:
            """Type of source this stream belongs to."""
            ...

        @property
        def status(self) -> str:
            """Current status of the stream."""
            ...

        @property
        def records_extracted(self) -> t.NonNegativeInt:
            """Number of records extracted."""
            ...


__all__: list[str] = [
    "FlextMeltanoProtocolsSourcesParams",
]
