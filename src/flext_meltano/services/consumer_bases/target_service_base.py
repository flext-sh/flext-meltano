"""Base service for FLEXT target consumer projects.

Provides sink management, record processing, and batch lifecycle via MRO.
Consumer targets declare ``sink_factory`` only.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableMapping, Sequence
from typing import Annotated, ClassVar, override

from flext_meltano import FlextMeltanoServiceBase, c, m, p, r, t, u


class FlextMeltanoTargetServiceBase(FlextMeltanoServiceBase):
    """Base for all FLEXT target service projects.

    Subclasses declare:
    - ``target_name``: canonical target identifier (e.g. ``"target-oracle"``)
    - ``sink_factory``: the member's stateless ``u.<Namespace>.create_sink``

    This base provides via MRO:
    - CLI dispatch (``cli_main``)
    - Sink management (``fetch_or_create_sink``, ``flush``)
    - Record processing
    """

    target_name: Annotated[
        t.NonEmptyStr,
        m.Field(description="Canonical target name (e.g. target-oracle)"),
    ] = "target"

    sink_factory: ClassVar[p.Meltano.SinkFactory]

    _sinks: MutableMapping[str, p.Meltano.SingerDrainSink] = m.PrivateAttr(
        default_factory=dict[str, p.Meltano.SingerDrainSink],
    )

    # ------------------------------------------------------------------
    # CLI dispatch
    # ------------------------------------------------------------------

    def cli_main(self, args: Sequence[str] | None = None) -> int:
        """Drain the Singer message stream from stdin into the sink registry.

        A Singer target owns no argument surface: messages arrive on stdin, so
        ``args`` is accepted for symmetry with the tap and dbt bases and never
        silently discarded. Dispatch runs through the canonical
        ``u.Meltano.process_stdin`` router over the handler methods below.

        Returns:
            The resulting ``int``.

        Raises:
            SystemExit: If ``drain_result.failure``; or if ``flush_result.failure``.

        """
        _ = args
        drain_result = u.Meltano.process_stdin(self)
        if drain_result.failure:
            self.logger.error("Target drain failed", error=str(drain_result.error))
            raise SystemExit(1)
        flush_result = self.flush()
        if flush_result.failure:
            self.logger.error("Target flush failed", error=str(flush_result.error))
            raise SystemExit(1)
        return 0

    def handle_schema(self, message: m.Meltano.SingerSchemaMessage) -> p.Result[bool]:
        """Register the stream sink declared by a SCHEMA message.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        sink_result = self.fetch_or_create_sink(
            message.stream,
            message.schema_definition,
        )
        if sink_result.failure:
            return r[bool].from_failure(sink_result)
        return r[bool].ok(value=True)

    def handle_record(self, message: m.Meltano.SingerRecordMessage) -> p.Result[bool]:
        """Route a RECORD message into its stream sink.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        return self.process_record(message.stream, message.record, {})

    def handle_state(self, message: m.Meltano.SingerStateMessage) -> p.Result[bool]:
        """Persist every pending sink batch at a STATE boundary.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        _ = message
        return self.flush()

    # ------------------------------------------------------------------
    # Sink management
    # ------------------------------------------------------------------

    def fetch_or_create_sink(
        self,
        stream_name: str,
        schema: t.JsonMapping,
    ) -> p.Result[p.Meltano.SingerDrainSink]:
        """Get existing sink or create new one for a stream.

        Returns:
            The resulting ``p.Result[p.Meltano.SingerDrainSink]``.

        """
        try:
            if stream_name in self._sinks:
                return r[p.Meltano.SingerDrainSink].ok(self._sinks[stream_name])
            sink = type(self).sink_factory(
                stream_name=stream_name,
                schema=schema,
                target_config=self.settings_overrides or {},
            )
            self._sinks[stream_name] = sink
            self.logger.debug("Sink created", stream=stream_name)
            return r[p.Meltano.SingerDrainSink].ok(sink)
        except c.EXC_ATTR_KEY_OS_TYPE_VALUE as exc:
            return r[p.Meltano.SingerDrainSink].fail(str(exc), exception=exc)

    def flush(self, stream_name: str | None = None) -> p.Result[bool]:
        """Flush records for a specific stream or all streams.

        Returns:
            The resulting ``p.Result[bool]``.

        """
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
            return r[bool].ok(value=True)
        except c.EXC_ATTR_KEY_OS_TYPE_VALUE as exc:
            return r[bool].fail(str(exc), exception=exc)

    # ------------------------------------------------------------------
    # Record processing
    # ------------------------------------------------------------------

    def process_record(
        self,
        stream_name: str,
        record: t.JsonMapping,
        schema: t.JsonMapping,
    ) -> p.Result[bool]:
        """Process a single Singer RECORD message.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        sink_result = self.fetch_or_create_sink(stream_name, schema)
        if sink_result.failure:
            return r[bool].from_failure(sink_result)
        try:
            record_dict = u.json_dict_adapter().validate_python(record)
            empty_context: t.MutableJsonMapping = {}
            sink_result.value.process_record(record_dict, empty_context)
            return r[bool].ok(value=True)
        except c.EXC_ATTR_KEY_OS_TYPE_VALUE as exc:
            return r[bool].fail(str(exc), exception=exc)

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute target service — returns status.

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """
        return r[t.JsonMapping].ok({
            "service": self.target_name,
            "status": "active",
            "type": "target",
            "active_sinks": len(self._sinks),
        })


__all__: list[str] = ["FlextMeltanoTargetServiceBase"]
