"""Base service for FLEXT target consumer projects.

Provides sink management, record processing, batch lifecycle, and connection
management via MRO. Consumer targets override ``create_sink()`` only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Annotated, override

from flext_meltano import FlextMeltanoServiceBase, c, m, p, r, t, u

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
        """Drain the Singer message stream from stdin into the sink registry.

        A Singer target owns no argument surface: messages arrive on stdin, so
        ``args`` is accepted for symmetry with the tap and dbt bases and never
        silently discarded. Dispatch runs through the canonical
        ``u.Meltano.process_stdin`` router over the handler methods below.
        """
        _ = args
        drain_result = u.Meltano.process_stdin(self)
        if drain_result.failure:
            self.logger.error("Target drain failed", error=str(drain_result.error))
            return 1
        flush_result = self.flush()
        if flush_result.failure:
            self.logger.error("Target flush failed", error=str(flush_result.error))
            return 1
        return 0

    def handle_schema(self, message: m.Meltano.SingerSchemaMessage) -> p.Result[bool]:
        """Register the stream sink declared by a SCHEMA message."""
        sink_result = self.fetch_or_create_sink(
            message.stream, message.schema_definition
        )
        if sink_result.failure:
            return r[bool].from_failure(sink_result)
        return r[bool].ok(True)

    def handle_record(self, message: m.Meltano.SingerRecordMessage) -> p.Result[bool]:
        """Route a RECORD message into its stream sink."""
        return self.process_record(message.stream, message.record, {})

    def handle_state(self, message: m.Meltano.SingerStateMessage) -> p.Result[bool]:
        """Persist every pending sink batch at a STATE boundary."""
        _ = message
        return self.flush()

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
            return r[p.Meltano.SingerDrainSink].fail(str(exc), exception=exc)

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
            return r[bool].fail(str(exc), exception=exc)

    # ------------------------------------------------------------------
    # Record processing
    # ------------------------------------------------------------------

    def process_record(
        self, stream_name: str, record: t.JsonMapping, schema: t.JsonMapping
    ) -> p.Result[bool]:
        """Process a single Singer RECORD message."""
        sink_result = self.fetch_or_create_sink(stream_name, schema)
        if sink_result.failure:
            return r[bool].from_failure(sink_result)
        try:
            record_dict = t.json_dict_adapter().validate_python(record)
            empty_context: t.MutableJsonMapping = {}
            sink_result.value.process_record(record_dict, empty_context)
            return r[bool].ok(value=True)
        except c.Meltano.OPERATION_ERRORS as exc:
            return r[bool].fail(str(exc), exception=exc)

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
                return r[int].from_failure(result)
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
