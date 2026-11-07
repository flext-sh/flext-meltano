# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_meltano/_protocols/instances
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_cli import p

    from flext_meltano import t
    from flext_meltano._protocols import FlextMeltanoProtocolsSources


class FlextMeltanoProtocolsInstances:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class StreamInfo(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        version: t.NonNegativeInt
        unique_id: t.NonEmptyStr

        @property
        def created_at(self) -> datetime:
            """Creation timestamp (configured timezone)."""
            ...

        updated_at: datetime | None

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        stream_name: t.NonEmptyStr
        stream_schema: Mapping[str, t.Scalar | Mapping[str, t.Scalar]]
        key_properties: t.StrTuple
        replication_method: str
        replication_key: str | None
        status: str
        records_loaded: t.NonNegativeInt
        batches_processed: t.NonNegativeInt
        stream_created_at: str

    @runtime_checkable
    class TapInstance(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        version: t.NonNegativeInt
        unique_id: t.NonEmptyStr

        @property
        def created_at(self) -> datetime:
            """Creation timestamp (configured timezone)."""
            ...

        updated_at: datetime | None

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        tap_id: str | None
        tap_type: str

        @property
        def settings(self) -> FlextMeltanoProtocolsSources.TapConfig:
            """Tap configuration."""
            ...

        adapter: t.JsonValue | None

        @property
        def streams(self) -> tuple[FlextMeltanoProtocolsInstances.StreamInfo, ...]:
            """Available streams."""
            ...

        status: str


__all__: list[str] = [
    "FlextMeltanoProtocolsInstances",
]
