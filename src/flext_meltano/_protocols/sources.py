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

from flext_meltano import t

if TYPE_CHECKING:
    from flext_cli import p


class FlextMeltanoProtocolsSources:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class TapConfig(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        @property
        def connection_config(self) -> t.FlatContainerMapping:
            """Connection configuration."""
            ...

        @property
        def stream_config(self) -> t.FlatContainerMapping:
            """Stream-specific configuration."""
            ...

        @property
        def tap_type(self) -> str:
            """Type of the tap."""
            ...

        @property
        def tap_version(self) -> str:
            """Tap version."""
            ...

    @runtime_checkable
    class TargetConfig(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        @property
        def target_type(self) -> str:
            """Type of the target."""
            ...

        @property
        def connection_config(self) -> t.FlatContainerMapping:
            """Connection configuration."""
            ...

        @property
        def batch_size(self) -> int | None:
            """Batch size for data loading."""
            ...

        @property
        def batch_wait_limit(self) -> float | None:
            """Batch wait limit in seconds."""
            ...

        @property
        def target_version(self) -> str:
            """Target version."""
            ...


__all__: list[str] = [
    "FlextMeltanoProtocolsSources",
]
