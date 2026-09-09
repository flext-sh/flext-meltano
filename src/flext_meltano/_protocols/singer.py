"""FLEXT Meltano Protocols - Singer Tap, Target, and DbtRunner protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, override, runtime_checkable

from flext_cli import p

from flext_core import r
from flext_meltano import m, t


class FlextMeltanoProtocolsSinger:
    """Singer Tap, Target, and DbtRunner protocol definitions."""

    @runtime_checkable
    class Tap(p.Service[t.FlatContainerMapping], Protocol):
        """Singer Tap protocol extending Service for ELT operations."""

        def discover(self) -> p.Result[t.FlatContainerMapping]:
            """Discover catalog with r."""
            ...

        @override
        def execute(self) -> p.Result[t.FlatContainerMapping]:
            """Execute the tap extraction (implements Service)."""
            ...

        def sync(
            self, catalog: t.FlatContainerMapping
        ) -> p.Result[t.FlatContainerMapping]:
            """Sync data from source with r."""
            ...

    @runtime_checkable
    class Target(p.Service[t.FlatContainerMapping], Protocol):
        """Singer Target protocol extending Service for ELT operations."""

        @override
        def execute(self) -> p.Result[t.FlatContainerMapping]:
            """Execute the target loading (implements Service)."""
            ...

        def handle_batch(
            self, records: Sequence[t.Meltano.OptionalScalarMap]
        ) -> p.Result[t.FlatContainerMapping]:
            """Handle a batch of records with r."""
            ...

        def handle_record(
            self, record: t.Meltano.OptionalScalarMap
        ) -> p.Result[t.FlatContainerMapping]:
            """Handle a single record with r."""
            ...

    @runtime_checkable
    class DbtRunner(p.Service[t.FlatContainerMapping], Protocol):
        """DBT Runner protocol extending Service for ELT operations."""

        @override
        def execute(self) -> p.Result[t.FlatContainerMapping]:
            """Execute DBT transformations (implements Service)."""
            ...

        def run(self, models: t.StrSequence) -> p.Result[t.FlatContainerMapping]:
            """Run DBT models with r."""
            ...

        def test(self, models: t.StrSequence) -> p.Result[t.FlatContainerMapping]:
            """Test DBT models with r."""
            ...

    class SingerStreamInfo(Protocol):
        """Minimal protocol for stream objects returned by discover_streams."""

        @property
        def name(self) -> str: ...

    class SingerTapInstance(Protocol):
        """Internal tap runtime contract consumed by tap service bases.

        Singer SDK details stay behind a bridge in ``flext-meltano`` so
        consumer projects depend only on FLEXT's own runtime surface.
        """

        @property
        def settings(self) -> t.FlatContainerMapping:
            """Tap configuration."""
            ...

        def run_cli(self, args: t.StrSequence, prog_name: str) -> int:
            """Execute the tap CLI and return a normalized exit code."""
            ...

        def discover_streams(
            self,
        ) -> Sequence[FlextMeltanoProtocolsSinger.SingerStreamInfo]:
            """Discover available streams."""
            ...

        def sync_all(self) -> None:
            """Execute Singer sync for all selected streams."""
            ...

    class SingerTap(Protocol):
        """Singer Tap protocol definition for data extraction.

        Defines the interface for Singer data extraction (tap) components
        that implement the Singer protocol for data source integration.
        """

        streams: t.StrSequence
        name: str
        state: m.Meltano.SingerStateMessage

        def discover(self) -> m.Meltano.SingerCatalog:
            """Discover available streams and schemas."""
            ...

        def get_records(
            self, stream_name: str
        ) -> Sequence[m.Meltano.SingerRecordMessage]:
            """Get records for a specific stream."""
            ...

        def get_state(self) -> m.Meltano.SingerStateMessage:
            """Get current state."""
            ...

        def sync(
            self, catalog: m.Meltano.SingerCatalog, state: m.Meltano.SingerStateMessage
        ) -> None:
            """Synchronize data from source to stdout."""
            ...

    class SingerTarget(Protocol):
        """Singer Target protocol definition for data loading.

        Defines the interface for Singer data loading (target) components
        that implement the Singer protocol for data sink integration.
        """

        name: str
        config: t.FlatContainerMapping

        def consume(self, records: Sequence[m.Meltano.SingerRecordMessage]) -> int:
            """Consume records batch.

            Args:
            records: Batch of records to consume

            Returns:
            Number of records consumed

            """
            ...

    @runtime_checkable
    class RecordFetcher(Protocol):
        """Consumer-side fetcher contract for declarative Singer taps."""

        def fetch(
            self, request: m.Meltano.FetchRequest
        ) -> p.Result[m.Meltano.FetchResult]:
            """Fetch records for one stream from the consumer domain."""
            ...

    class SingerCommand(Protocol):
        """Opaque Singer CLI command object."""

        def main(self, *, args: t.StrSequence, prog_name: str) -> t.JsonValue | None:
            """Invoke the Singer CLI command and return its output."""
            ...

    @runtime_checkable
    class SingerTapBackend(Protocol):
        """Raw Singer SDK tap surface consumed by the internal adapter.

        Both the full SDK tap class and the settings-only backend are
        represented by the same canonical contract so consumer code can
        pass either without importing ``singer_sdk`` directly.
        """

        @property
        def config(self) -> t.FlatContainerMapping:
            """Tap runtime configuration mapping."""
            ...

        @classmethod
        def get_singer_command(cls) -> FlextMeltanoProtocolsSinger.SingerCommand:
            """Return the Singer CLI command object."""
            ...

        def discover_streams(
            self,
        ) -> Sequence[FlextMeltanoProtocolsSinger.SingerStreamInfo]:
            """Discover available streams."""
            ...

        def sync_all(self) -> None:
            """Execute sync for all selected streams."""
            ...

    SingerTapSdkBackend = SingerTapBackend
    SingerTapSettingsBackend = SingerTapBackend

    @runtime_checkable
    class SingerDrainSink(Protocol):
        """Typed sink contract for target service drain and record operations.

        Used by ``FlextMeltanoTargetServiceBase.flush()`` to process
        batches through the Singer sink lifecycle.

        Context/Record types use ``t.Meltano.MutableContainerValueMapping`` — the canonical
        bridge from singer_sdk's ``dict[str, Any]`` to ``MutableMapping[str, ContainerValue]``.
        """

        def start_drain(self) -> t.Meltano.MutableContainerValueMapping: ...

        def process_batch(
            self, context: t.Meltano.MutableContainerValueMapping
        ) -> None: ...

        def mark_drained(self) -> None: ...

        def process_record(
            self,
            record: t.Meltano.MutableContainerValueMapping,
            context: t.Meltano.MutableContainerValueMapping,
        ) -> None: ...

    @runtime_checkable
    class SingerTargetHandler(Protocol):
        """Protocol for Singer target message handlers.

        Consumers implement this protocol to handle Singer messages
        routed by process_stdin(). Domain-specific logic stays in
        the consumer; generic stdin parsing stays here.
        """

        def handle_schema(self, message: m.Meltano.SingerSchemaMessage) -> r[bool]:
            """Handle a SCHEMA message."""
            ...

        def handle_record(self, message: m.Meltano.SingerRecordMessage) -> r[bool]:
            """Handle a RECORD message."""
            ...

        def handle_state(self, message: m.Meltano.SingerStateMessage) -> r[bool]:
            """Handle a STATE message."""
            ...
