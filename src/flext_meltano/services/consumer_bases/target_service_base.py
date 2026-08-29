"""Base service for FLEXT target consumer projects.

Provides sink management, record processing, batch lifecycle, and connection
management via MRO. Consumer targets override ``create_sink()`` only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Annotated, override

from flext_meltano import FlextMeltanoServiceBase, c, p, r, t, u

if TYPE_CHECKING:
    from collections.abc import MutableMapping


class FlextMeltanoTargetServiceBase(FlextMeltanoServiceBase, ABC):
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
        t.NonEmptyStr, u.Field(description="Canonical target name (e.g. target-oracle)")
    ] = "target"

    _sinks: MutableMapping[str, p.Meltano.SingerDrainSink] = u.PrivateAttr(
        default_factory=dict[str, p.Meltano.SingerDrainSink]
    )

    @abstractmethod
    def create_sink(
        self, stream_name: str, schema: t.JsonMapping
    ) -> p.Meltano.SingerDrainSink:
        """Create a Sink instance for a stream.

        Consumer implements this with domain-specific sink logic.
        """

    # ------------------------------------------------------------------
    # CLI dispatch
    # ------------------------------------------------------------------

    def cli_main(self, args: t.StrSequence | None = None) -> int:
        """Run the main CLI entry point for target."""
        try:
            command_args = list(args) if args else sys.argv[1:]
            _ = command_args
            self.logger.info("Target CLI started", target=self.target_name)
        except c.EXC_OS_RUNTIME_TYPE as exc:
            self.logger.exception("Target CLI failed", error=str(exc))
            return 1
        else:
            return 0

    # ------------------------------------------------------------------
    # Sink management
    # ------------------------------------------------------------------

    def fetch_or_create_sink(
        self, stream_name: str, schema: t.JsonMapping
    ) -> p.Result[p.Meltano.SingerDrainSink]:
        """Get existing sink or create new one for a stream."""
        try:
            if stream_name in self._sinks:
                return r[p.Meltano.SingerDrainSink].ok(self._sinks[stream_name])
            sink = self.create_sink(stream_name, schema)
            self._sinks[stream_name] = sink
            self.logger.debug("Sink created", stream=stream_name)
            return r[p.Meltano.SingerDrainSink].ok(sink)
        except c.Meltano.OPERATION_ERRORS as exc:
            return r[p.Meltano.SingerDrainSink].fail(str(exc))

    def flush(self, stream_name: str | None = None) -> p.Result[bool]:
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
            return r[bool].ok(True)
        except c.Meltano.OPERATION_ERRORS as exc:
            return r[bool].fail(str(exc))

    # ------------------------------------------------------------------
    # Record processing
    # ------------------------------------------------------------------

    def process_record(
        self, stream_name: str, record: t.JsonMapping, schema: t.JsonMapping
    ) -> p.Result[bool]:
        """Process a single Singer RECORD message."""
        sink_result = self.fetch_or_create_sink(stream_name, schema)
        if sink_result.failure:
            return r[bool].fail(sink_result.error or "Sink creation failed")
        try:
            record_dict = t.json_dict_adapter().validate_python(record)
            empty_context: t.MutableJsonMapping = {}
            sink_result.value.process_record(record_dict, empty_context)
            return r[bool].ok(value=True)
        except c.Meltano.OPERATION_ERRORS as exc:
            return r[bool].fail(str(exc))

    def process_batch(
        self,
        stream_name: str,
        records: t.SequenceOf[t.JsonMapping],
        schema: t.JsonMapping,
    ) -> p.Result[int]:
        """Process a batch of records."""
        processed = 0
        for record in records:
            result = self.process_record(stream_name, record, schema)
            if result.failure:
                return r[int].fail(result.error or "Batch processing failed")
            processed += 1
        return r[int].ok(processed)

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------

    def connect(self) -> p.Result[bool]:
        """Connect to the target data store. Override in consumer."""
        return r[bool].ok(value=True)

    def disconnect(self) -> p.Result[bool]:
        """Disconnect from the target data store. Override in consumer."""
        self._sinks.clear()
        return r[bool].ok(True)

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute target service — returns status."""
        return r[t.JsonMapping].ok({
            "service": self.target_name,
            "status": "active",
            "type": "target",
            "active_sinks": len(self._sinks),
        })


__all__: list[str] = ["FlextMeltanoTargetServiceBase"]
