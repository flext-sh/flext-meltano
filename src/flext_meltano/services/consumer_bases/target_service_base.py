"""Base service for FLEXT target consumer projects.

Provides sink management, record processing, batch lifecycle, and connection
management via MRO. Consumer targets override ``create_sink()`` only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from abc import abstractmethod
from collections.abc import MutableMapping, Sequence
from typing import Annotated, ClassVar, Self, override

from pydantic import Field, PrivateAttr

from flext_core import r
from flext_meltano import FlextMeltanoServiceBase, FlextMeltanoSingerSinkBase, c, t


class FlextMeltanoTargetServiceBase(FlextMeltanoServiceBase):
    """Base for all FLEXT target service projects.

    Subclasses MUST define:
    - ``target_name``: canonical target identifier (e.g. ``"target-oracle"``)
    - ``create_sink(stream_name, schema)``: factory returning a Sink instance

    This base provides via MRO:
    - CLI dispatch (``cli_main``)
    - Sink management (``get_or_create_sink``, ``flush``)
    - Record and batch processing
    - Connection lifecycle (``connect`` / ``disconnect``)
    - Singleton accessor (``get_instance``)
    """

    target_name: Annotated[
        t.NonEmptyStr,
        Field(description="Canonical target name (e.g. target-oracle)"),
    ] = "target"

    _sinks: MutableMapping[str, FlextMeltanoSingerSinkBase] = PrivateAttr(
        default_factory=dict,
    )
    _instance: ClassVar[Self | None] = None

    @classmethod
    def get_instance(cls) -> Self:
        """Return the shared facade instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @abstractmethod
    def create_sink(
        self,
        stream_name: str,
        schema: t.FlatContainerMapping,
    ) -> FlextMeltanoSingerSinkBase:
        """Create a Sink instance for a stream.

        Consumer implements this with domain-specific sink logic.
        """

    # ------------------------------------------------------------------
    # CLI dispatch
    # ------------------------------------------------------------------

    def cli_main(self, args: t.StrSequence | None = None) -> int:
        """Main CLI entry point for target."""
        try:
            command_args = list(args) if args else sys.argv[1:]
            _ = command_args
            self.logger.info("Target CLI started", target=self.target_name)
            return 0
        except (ValueError, TypeError, OSError, RuntimeError) as exc:
            self.logger.exception("Target CLI failed", error=str(exc))
            return 1

    # ------------------------------------------------------------------
    # Sink management
    # ------------------------------------------------------------------

    def get_or_create_sink(
        self,
        stream_name: str,
        schema: t.FlatContainerMapping,
    ) -> r[FlextMeltanoSingerSinkBase]:
        """Get existing sink or create new one for a stream."""
        try:
            if stream_name in self._sinks:
                return r[FlextMeltanoSingerSinkBase].ok(self._sinks[stream_name])
            sink = self.create_sink(stream_name, schema)
            self._sinks[stream_name] = sink
            self.logger.debug("Sink created", stream=stream_name)
            return r[FlextMeltanoSingerSinkBase].ok(sink)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as exc:
            return r[FlextMeltanoSingerSinkBase].fail(str(exc))

    def flush(self, stream_name: str | None = None) -> r[None]:
        """Flush records for a specific stream or all streams."""
        try:
            targets = (
                [self._sinks[stream_name]]
                if stream_name and stream_name in self._sinks
                else list(self._sinks.values())
            )
            for sink in targets:
                context = sink.start_drain()
                sink.process_batch(context)
                sink.mark_drained()
            return r[None].ok(None)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as exc:
            return r[None].fail(str(exc))

    # ------------------------------------------------------------------
    # Record processing
    # ------------------------------------------------------------------

    def process_record(
        self,
        stream_name: str,
        record: t.FlatContainerMapping,
        schema: t.FlatContainerMapping,
    ) -> r[bool]:
        """Process a single Singer RECORD message."""
        sink_result = self.get_or_create_sink(stream_name, schema)
        if sink_result.is_failure:
            return r[bool].fail(sink_result.error or "Sink creation failed")
        try:
            sink = sink_result.value
            sink.process_record(dict(record.items()), {})
            return r[bool].ok(value=True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as exc:
            return r[bool].fail(str(exc))

    def process_batch(
        self,
        stream_name: str,
        records: Sequence[t.FlatContainerMapping],
        schema: t.FlatContainerMapping,
    ) -> r[int]:
        """Process a batch of records."""
        processed = 0
        for record in records:
            result = self.process_record(stream_name, record, schema)
            if result.is_failure:
                return r[int].fail(result.error or "Batch processing failed")
            processed += 1
        return r[int].ok(processed)

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------

    def connect(self) -> r[bool]:
        """Connect to the target data store. Override in consumer."""
        return r[bool].ok(value=True)

    def disconnect(self) -> r[None]:
        """Disconnect from the target data store. Override in consumer."""
        self._sinks.clear()
        return r[None].ok(None)

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute target service — returns status."""
        return r[t.Meltano.MeltanoConfigDict].ok({
            "service": self.target_name,
            "status": c.CommonStatus.ACTIVE.value,
            "type": "target",
            "active_sinks": len(self._sinks),
        })


__all__ = ["FlextMeltanoTargetServiceBase"]
