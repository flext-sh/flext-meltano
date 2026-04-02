"""FLEXT Meltano Protocols - Singer Tap, Target, and DbtRunner protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, override, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_core import r
from flext_meltano import m, t


class FlextMeltanoProtocolsSinger:
    """Singer Tap, Target, and DbtRunner protocol definitions."""

    @runtime_checkable
    class Tap(FlextCliProtocols.Service[t.Meltano.ResultDict], Protocol):
        """Singer Tap protocol extending Service for ELT operations."""

        def discover(self) -> FlextCliProtocols.Result[t.Meltano.ResultDict]:
            """Discover catalog with r."""
            ...

        @override
        def execute(self) -> FlextCliProtocols.Result[t.Meltano.ResultDict]:
            """Execute the tap extraction (implements Service)."""
            ...

        def sync(
            self,
            catalog: t.FlatContainerMapping,
        ) -> FlextCliProtocols.Result[t.Meltano.ResultDict]:
            """Sync data from source with r."""
            ...

    @runtime_checkable
    class Target(FlextCliProtocols.Service[t.Meltano.ResultDict], Protocol):
        """Singer Target protocol extending Service for ELT operations."""

        @override
        def execute(self) -> FlextCliProtocols.Result[t.Meltano.ResultDict]:
            """Execute the target loading (implements Service)."""
            ...

        def handle_batch(
            self,
            records: Sequence[t.Meltano.RecordDict],
        ) -> FlextCliProtocols.Result[t.Meltano.ResultDict]:
            """Handle a batch of records with r."""
            ...

        def handle_record(
            self,
            record: t.Meltano.RecordDict,
        ) -> FlextCliProtocols.Result[t.Meltano.ResultDict]:
            """Handle a single record with r."""
            ...

    @runtime_checkable
    class DbtRunner(
        FlextCliProtocols.Service[t.Meltano.MeltanoConfigDict],
        Protocol,
    ):
        """DBT Runner protocol extending Service for ELT operations."""

        @override
        def execute(self) -> FlextCliProtocols.Result[t.Meltano.MeltanoConfigDict]:
            """Execute DBT transformations (implements Service)."""
            ...

        def run(
            self,
            models: t.StrSequence,
        ) -> FlextCliProtocols.Result[t.Meltano.MeltanoConfigDict]:
            """Run DBT models with r."""
            ...

        def test(
            self,
            models: t.StrSequence,
        ) -> FlextCliProtocols.Result[t.Meltano.MeltanoConfigDict]:
            """Test DBT models with r."""
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
            self,
            stream_name: str,
        ) -> Sequence[m.Meltano.SingerRecordMessage]:
            """Get records for a specific stream."""
            ...

        def get_state(self) -> m.Meltano.SingerStateMessage:
            """Get current state."""
            ...

        def sync(
            self,
            catalog: m.Meltano.SingerCatalog,
            state: m.Meltano.SingerStateMessage,
        ) -> None:
            """Synchronize data from source to stdout."""
            ...

    class SingerTarget(Protocol):
        """Singer Target protocol definition for data loading.

        Defines the interface for Singer data loading (target) components
        that implement the Singer protocol for data sink integration.
        """

        name: str
        config: m.Meltano.TargetConfig

        def consume(self, records: Sequence[m.Meltano.SingerRecordMessage]) -> int:
            """Consume records batch.

            Args:
            records: Batch of records to consume

            Returns:
            Number of records consumed

            """
            ...

    @runtime_checkable
    class SingerTargetHandler(Protocol):
        """Protocol for Singer target message handlers.

        Consumers implement this protocol to handle Singer messages
        routed by process_stdin(). Domain-specific logic stays in
        the consumer; generic stdin parsing stays here.
        """

        def handle_schema(self, message: m.Meltano.SingerSchemaMessage) -> r[None]:
            """Handle a SCHEMA message."""
            ...

        def handle_record(self, message: m.Meltano.SingerRecordMessage) -> r[None]:
            """Handle a RECORD message."""
            ...

        def handle_state(self, message: m.Meltano.SingerStateMessage) -> r[None]:
            """Handle a STATE message."""
            ...
