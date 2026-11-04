"""FLEXT Meltano Protocols - Singer tap and target runtime protocols.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flext_cli import p


from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_meltano import c, t


class FlextMeltanoProtocolsSinger:
    """Singer tap and target runtime protocol definitions."""

    @runtime_checkable
    class SingerTapInstance(Protocol):
        """Internal tap runtime contract consumed by tap service bases.

        Singer SDK details stay behind a bridge in ``flext-meltano`` so
        consumer projects depend only on FLEXT's own runtime surface.
        """

        def run_cli(self, args: Sequence[str], prog_name: str) -> int:
            """Execute the tap CLI and return a normalized exit code."""
            ...

    @runtime_checkable
    class RecordFetcher(Protocol):
        """Consumer-side fetcher contract for declarative Singer taps."""

        def fetch(
            self,
            request: FlextMeltanoProtocolsSinger.FetchRequest,
        ) -> p.Result[FlextMeltanoProtocolsSinger.FetchResult]:
            """Fetch records for one stream from the consumer domain."""
            ...

    @runtime_checkable
    class SingerDrainSink(Protocol):
        """Typed sink contract for target service drain and record operations.

        Used by ``FlextMeltanoTargetServiceBase.flush()`` to process
        batches through the Singer sink lifecycle.

        Context/Record types use ``t.Meltano.MutableContainerValueMapping`` — the
        canonical bridge from singer_sdk's ``dict[str, Any]`` to
        ``MutableMapping[str, ContainerValue]``.
        """

        def start_drain(self) -> t.Meltano.MutableContainerValueMapping: ...

        def process_batch(
            self,
            context: t.Meltano.MutableContainerValueMapping,
        ) -> None: ...

        def mark_drained(self) -> None: ...

        def process_record(
            self,
            record: t.Meltano.MutableContainerValueMapping,
            context: t.Meltano.MutableContainerValueMapping,
        ) -> None: ...

    @runtime_checkable
    class SinkFactory(Protocol):
        """Sink factory a target service declares instead of overriding a method.

        Target facades bind it to their stateless ``u.<Namespace>.create_sink``,
        so ``api.py`` stays a pure MRO facade.
        """

        def __call__(
            self,
            *,
            stream_name: str,
            schema: t.JsonMapping,
            target_config: t.JsonMapping,
        ) -> FlextMeltanoProtocolsSinger.SingerDrainSink:
            """Build the drain sink for one stream from its target config."""
            ...

    @runtime_checkable
    class SingerTargetHandler(Protocol):
        """Protocol for Singer target message handlers.

        Consumers implement this protocol to handle Singer messages
        routed by process_stdin(). Domain-specific logic stays in
        the consumer; generic stdin parsing stays here.
        """

        def handle_schema(
            self,
            message: FlextMeltanoProtocolsSinger.SingerSchemaMessage,
        ) -> p.Result[bool]:
            """Handle a SCHEMA message."""
            ...

        def handle_record(
            self,
            message: FlextMeltanoProtocolsSinger.SingerRecordMessage,
        ) -> p.Result[bool]:
            """Handle a RECORD message."""
            ...

        def handle_state(
            self, message: FlextMeltanoProtocolsSinger.SingerStateMessage
        ) -> p.Result[bool]:
            """Handle a STATE message."""
            ...

    @runtime_checkable
    class SingerSchemaMessage(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        type: c.Meltano.SingerMessageType
        stream: t.NonEmptyStr
        schema_definition: t.FlatContainerMapping
        key_properties: t.StrTuple
        bookmark_properties: t.StrTuple
        intermediate_encodings: t.StrTuple

    @runtime_checkable
    class SingerRecordMessage(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        type: c.Meltano.SingerMessageType
        stream: str
        record: t.FlatContainerMapping
        time_extracted: str | None
        version: int | None

    @runtime_checkable
    class SingerStateMessage(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        type: c.Meltano.SingerMessageType
        value: t.MutableFlatContainerMapping

    @runtime_checkable
    class SingerActivateVersionMessage(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        type: c.Meltano.SingerMessageType
        stream: str
        version: t.PositiveInt

    @runtime_checkable
    class StreamSpec(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        name: str
        json_schema: t.FlatContainerMapping
        primary_keys: t.StrTuple
        replication_key: str | None

    @runtime_checkable
    class TapSpec(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        tap_name: str
        config_jsonschema: t.FlatContainerMapping

        @property
        def streams(self) -> tuple[FlextMeltanoProtocolsSinger.StreamSpec, ...]:
            """Declared tap streams."""
            ...

    @runtime_checkable
    class FetchRequest(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        stream_name: str
        config: t.JsonMapping

    @runtime_checkable
    class FetchResult(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        records: tuple[t.JsonMapping, ...]


__all__: list[str] = ["FlextMeltanoProtocolsSinger"]
