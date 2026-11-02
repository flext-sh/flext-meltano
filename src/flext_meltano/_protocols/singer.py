"""FLEXT Meltano Protocols - Singer tap and target runtime protocols.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flext_cli import p

    from flext_meltano._constants import FlextMeltanoConstantsEnums


from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_meltano import t


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
    class SingerSchemaMessage(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def type(self) -> FlextMeltanoConstantsEnums.SingerMessageType:
            """Singer message discriminator."""
            ...

        @property
        def stream(self) -> t.NonEmptyStr:
            """Singer stream name."""
            ...

        @property
        def schema_definition(self) -> t.FlatContainerMapping:
            """Singer JSON schema payload."""
            ...

        @property
        def key_properties(self) -> t.StrTuple:
            """Singer stream key properties."""
            ...

        @property
        def bookmark_properties(self) -> t.StrTuple:
            """Singer bookmark columns for incremental replication."""
            ...

        @property
        def intermediate_encodings(self) -> t.StrTuple:
            """Singer intermediate encodings (e.g. 'utf8')."""
            ...

    @runtime_checkable
    class SingerRecordMessage(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def type(self) -> FlextMeltanoConstantsEnums.SingerMessageType:
            """Singer message discriminator."""
            ...

        @property
        def stream(self) -> str:
            """Singer stream name."""
            ...

        @property
        def record(self) -> t.FlatContainerMapping:
            """Singer record payload."""
            ...

        @property
        def time_extracted(self) -> str | None:
            """ISO 8601 timestamp when the record was extracted."""
            ...

        @property
        def version(self) -> int | None:
            """Stream version number for activate_version protocol."""
            ...

    @runtime_checkable
    class SingerStateMessage(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def type(self) -> FlextMeltanoConstantsEnums.SingerMessageType:
            """Singer message discriminator."""
            ...

        @property
        def value(self) -> t.MutableFlatContainerMapping:
            """Singer state bookmark payload."""
            ...

    @runtime_checkable
    class SingerActivateVersionMessage(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def type(self) -> FlextMeltanoConstantsEnums.SingerMessageType:
            """Singer message discriminator."""
            ...

        @property
        def stream(self) -> str:
            """Singer stream name."""
            ...

        @property
        def version(self) -> t.PositiveInt:
            """Stream version to activate."""
            ...

    @runtime_checkable
    class StreamSpec(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        @property
        def name(self) -> str:
            """Stream name."""
            ...

        @property
        def json_schema(self) -> t.FlatContainerMapping:
            """JSON schema for the stream."""
            ...

        @property
        def primary_keys(self) -> t.StrTuple:
            """Primary key properties."""
            ...

        @property
        def replication_key(self) -> str | None:
            """Incremental replication key."""
            ...

    @runtime_checkable
    class TapSpec(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        @property
        def tap_name(self) -> str:
            """Tap name."""
            ...

        @property
        def config_jsonschema(self) -> t.FlatContainerMapping:
            """Tap config JSON schema."""
            ...

        @property
        def streams(self) -> tuple[FlextMeltanoProtocolsSinger.StreamSpec, ...]:
            """Declared tap streams."""
            ...

    @runtime_checkable
    class FetchRequest(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        @property
        def stream_name(self) -> str:
            """Stream name to fetch."""
            ...

        @property
        def config(self) -> t.JsonMapping:
            """Runtime tap configuration."""
            ...

    @runtime_checkable
    class FetchResult(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        @property
        def records(self) -> tuple[t.JsonMapping, ...]:
            """Fetched records."""
            ...


__all__: list[str] = ["FlextMeltanoProtocolsSinger"]
