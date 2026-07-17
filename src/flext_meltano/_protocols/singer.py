"""FLEXT Meltano Protocols - Singer Tap, Target, and DbtRunner protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Protocol, override, runtime_checkable

from flext_meltano import p, t


class FlextMeltanoProtocolsSinger:
    """Singer Tap, Target, and DbtRunner protocol definitions."""

    @runtime_checkable
    class Tap(p.Service[t.JsonMapping], Protocol):
        """Singer Tap protocol extending Service for ELT operations."""

        def discover(self) -> p.Result[t.JsonMapping]:
            """Discover catalog with r."""
            ...

        @override
        def execute(self) -> p.Result[t.JsonMapping]:
            """Execute the tap extraction (implements Service)."""
            ...

        def sync(
            self,
            catalog: t.JsonMapping,
        ) -> p.Result[t.JsonMapping]:
            """Sync data from source with r."""
            ...

    @runtime_checkable
    class Target(p.Service[t.JsonMapping], Protocol):
        """Singer Target protocol extending Service for ELT operations."""

        @override
        def execute(self) -> p.Result[t.JsonMapping]:
            """Execute the target loading (implements Service)."""
            ...

        def handle_batch(
            self,
            records: t.SequenceOf[t.Meltano.OptionalScalarMap],
        ) -> p.Result[t.JsonMapping]:
            """Handle a batch of records with r."""
            ...

        def handle_record(
            self,
            record: t.Meltano.OptionalScalarMap,
        ) -> p.Result[t.JsonMapping]:
            """Handle a single record with r."""
            ...

    @runtime_checkable
    class DbtRunner(
        p.Service[t.JsonMapping],
        Protocol,
    ):
        """DBT Runner protocol extending Service for ELT operations."""

        @override
        def execute(self) -> p.Result[t.JsonMapping]:
            """Execute DBT transformations (implements Service)."""
            ...

        def run(
            self,
            models: t.StrSequence,
        ) -> p.Result[t.JsonMapping]:
            """Run DBT models with r."""
            ...

        def test(
            self,
            models: t.StrSequence,
        ) -> p.Result[t.JsonMapping]:
            """Test DBT models with r."""
            ...

    # NOTE (multi-agent): mro-rn88 ADR-006 thin-driver — typed dbt connection profile.
    @runtime_checkable
    class DbtConnectionProfile(p.HasModelDump, Protocol):
        """Typed dbt connection profile contract (any FlextModel satisfies it)."""

        @property
        def type(self) -> str:
            """Dbt adapter type identifier."""
            ...

        @property
        def project(self) -> str:
            """Dbt project name owning this profile."""
            ...

    @runtime_checkable
    class SingerStreamInfo(Protocol):
        """Minimal protocol for stream objects returned by discover_streams."""

        @property
        def name(self) -> str: ...

    @runtime_checkable
    class SingerTapInstance(Protocol):
        """Internal tap runtime contract consumed by tap service bases.

        Singer SDK details stay behind a bridge in ``flext-meltano`` so
        consumer projects depend only on FLEXT's own runtime surface.
        """

        @property
        def settings(self) -> t.JsonMapping:
            """Tap configuration."""
            ...

        def run_cli(
            self,
            args: t.StrSequence,
            prog_name: str,
        ) -> int:
            """Execute the tap CLI and return a normalized exit code."""
            ...

        def discover_streams(
            self,
        ) -> t.SequenceOf[FlextMeltanoProtocolsSinger.SingerStreamInfo]:
            """Discover available streams."""
            ...

        def sync_all(self) -> None:
            """Execute Singer sync for all selected streams."""
            ...

    @runtime_checkable
    class RecordFetcher(Protocol):
        """Consumer contract that yields records for one declarative stream.

        A declarative consumer tap implements this so ``flext-meltano`` can build
        a real Singer tap without the consumer importing ``singer_sdk``. The
        consumer resolves records from the typed ``m.Meltano.FetchRequest`` using
        its own domain library (e.g. ``flext-ldap``) and returns a typed
        ``m.Meltano.FetchResult`` — one packed transport per boundary crossing.
        """

        def fetch(
            self,
            request: p.Meltano.FetchRequest,
        ) -> p.Result[p.Meltano.FetchResult]:
            """Return the records for one stream given the typed fetch request."""
            ...

    @runtime_checkable
    class SingerTap(Protocol):
        """Singer Tap protocol definition for data extraction.

        Defines the interface for Singer data extraction (tap) components
        that implement the Singer protocol for data source integration.
        """

        streams: t.StrSequence
        name: str
        state: p.Meltano.SingerStateMessage

        def discover(self) -> p.Meltano.SingerCatalog:
            """Discover available streams and schemas."""
            ...

        def get_records(
            self,
            stream_name: str,
        ) -> t.SequenceOf[p.Meltano.SingerRecordMessage]:
            """Get records for a specific stream."""
            ...

        def get_state(self) -> p.Meltano.SingerStateMessage:
            """Get current state."""
            ...

        def sync(
            self,
            catalog: p.Meltano.SingerCatalog,
            state: p.Meltano.SingerStateMessage,
        ) -> None:
            """Synchronize data from source to stdout."""
            ...

    @runtime_checkable
    class SingerTarget(Protocol):
        """Singer Target protocol definition for data loading.

        Defines the interface for Singer data loading (target) components
        that implement the Singer protocol for data sink integration.
        """

        name: str
        settings: t.JsonMapping

        def consume(self, records: t.SequenceOf[p.Meltano.SingerRecordMessage]) -> int:
            """Consume records batch.

            Args:
            records: Batch of records to consume

            Returns:
            Number of records consumed

            """
            ...

    @runtime_checkable
    class SingerDrainSink(Protocol):
        """Typed sink contract for target service drain and record operations.

        Used by ``FlextMeltanoTargetServiceBase.flush()`` to process
        batches through the Singer sink lifecycle.

        Context/Record types use ``t.MutableJsonMapping`` — the canonical
        bridge from singer_sdk's ``dict[str, Any]`` to ``MutableMapping[str, JsonValue]``.
        """

        def start_drain(self) -> t.MutableJsonMapping: ...

        def process_batch(self, context: t.MutableJsonMapping) -> None: ...

        def mark_drained(self) -> None: ...

        def process_record(
            self,
            record: t.MutableJsonMapping,
            context: t.MutableJsonMapping,
        ) -> None: ...

    @runtime_checkable
    class SingerTargetHandler(Protocol):
        """Protocol for Singer target message handlers.

        Consumers implement this protocol to handle Singer messages
        routed by process_stdin(). Domain-specific logic stays in
        the consumer; generic stdin parsing stays here.
        """

        def handle_schema(
            self,
            message: p.Meltano.SingerSchemaMessage,
        ) -> p.Result[None]:
            """Handle a SCHEMA message."""
            ...

        def handle_record(
            self,
            message: p.Meltano.SingerRecordMessage,
        ) -> p.Result[None]:
            """Handle a RECORD message."""
            ...

        def handle_state(self, message: p.Meltano.SingerStateMessage) -> p.Result[None]:
            """Handle a STATE message."""
            ...

    @runtime_checkable
    class SingerTapSdkBackend(Protocol):
        """Raw Singer SDK tap surface consumed by the FLEXT bridge."""

        @classmethod
        def get_singer_command(cls) -> p.Cli.ExternalCommand:
            """Return the Singer SDK command bound to the tap type."""
            ...

        @property
        def config(self) -> t.MappingKV[str, t.JsonPayload]:
            """Expose the raw tap configuration."""
            ...

        def discover_streams(
            self,
        ) -> t.SequenceOf[FlextMeltanoProtocolsSinger.SingerStreamInfo]:
            """Return the tap streams."""
            ...

        def sync_all(self) -> None:
            """Run a full Singer sync."""
            ...

    @runtime_checkable
    class SingerTapSettingsBackend(Protocol):
        """Legacy tap backend contract exposing ``settings`` only."""

        @classmethod
        def get_singer_command(cls) -> p.Cli.ExternalCommand:
            """Return the Singer SDK command bound to the tap type."""
            ...

        @property
        def settings(self) -> t.MappingKV[str, t.JsonPayload]:
            """Expose tap settings mapping."""
            ...

        def discover_streams(
            self,
        ) -> t.SequenceOf[FlextMeltanoProtocolsSinger.SingerStreamInfo]:
            """Return the tap streams."""
            ...

        def sync_all(self) -> None:
            """Run a full Singer sync."""
            ...
