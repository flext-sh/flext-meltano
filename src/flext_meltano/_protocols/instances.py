# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_meltano/_protocols/instances
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_meltano import t

if TYPE_CHECKING:
    from flext_cli import p

    from flext_meltano._protocols import FlextMeltanoProtocolsSources


class FlextMeltanoProtocolsInstances:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class StreamInfo(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        @property
        def stream_name(self) -> t.NonEmptyStr:
            """Stream name identifier."""
            ...

        @property
        def stream_schema(self) -> Mapping[str, t.Scalar | Mapping[str, t.Scalar]]:
            """Stream schema definition."""
            ...

        @property
        def key_properties(self) -> t.StrTuple:
            """Primary key properties for the stream."""
            ...

        @property
        def replication_method(self) -> str:
            """Replication method."""
            ...

        @property
        def replication_key(self) -> str | None:
            """Incremental replication field."""
            ...

        @property
        def status(self) -> str:
            """Stream processing status."""
            ...

        @property
        def records_loaded(self) -> t.NonNegativeInt:
            """Number of records loaded."""
            ...

        @property
        def batches_processed(self) -> t.NonNegativeInt:
            """Number of batches processed."""
            ...

        @property
        def stream_created_at(self) -> str:
            """Creation timestamp."""
            ...

    @runtime_checkable
    class TapInstance(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        @property
        def tap_id(self) -> str | None:
            """Unique tap identifier."""
            ...

        @property
        def tap_type(self) -> str:
            """Type of the tap."""
            ...

        @property
        def settings(self) -> FlextMeltanoProtocolsSources.TapConfig:
            """Tap configuration."""
            ...

        @property
        def adapter(self) -> t.JsonValue | None:
            """Tap adapter instance."""
            ...

        @property
        def streams(self) -> tuple[FlextMeltanoProtocolsInstances.StreamInfo, ...]:
            """Available streams."""
            ...

        @property
        def status(self) -> str:
            """Tap status."""
            ...


__all__: list[str] = [
    "FlextMeltanoProtocolsInstances",
]
