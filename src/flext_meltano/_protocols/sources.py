# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_meltano/_protocols/sources
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_cli import p

    from flext_meltano import t


class FlextMeltanoProtocolsSources:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class TapConfig(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        connection_config: t.FlatContainerMapping
        stream_config: t.FlatContainerMapping
        tap_type: str
        tap_version: str

    @runtime_checkable
    class TargetConfig(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        target_type: str
        connection_config: t.FlatContainerMapping
        batch_size: int | None
        batch_wait_limit: float | None
        target_version: str


__all__: list[str] = [
    "FlextMeltanoProtocolsSources",
]
