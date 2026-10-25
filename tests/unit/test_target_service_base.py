"""Behavioral tests for the declared sink factory of the target service base.

Drives the public ``FlextMeltanoTargetServiceBase`` surface through the runnable
example target of the ``examples`` tier: sinks come from ``sink_factory``, are
reused per stream, receive records and drain on flush.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from examples import ExamplesFlextMeltanoTargetService, ExamplesFlextMeltanoTargetSink

from tests import tm


class TestsFlextMeltanoTargetServiceBase:
    """Validate the sink lifecycle the base runs over the declared factory."""

    @staticmethod
    def test_declared_factory_builds_one_sink_per_stream() -> None:
        """The base builds the sink through sink_factory and reuses it per stream."""
        service = ExamplesFlextMeltanoTargetService()
        first = service.fetch_or_create_sink("orders", {"properties": {}})
        again = service.fetch_or_create_sink("orders", {"properties": {}})
        other = service.fetch_or_create_sink("items", {"properties": {}})

        tm.ok(first)
        tm.ok(again)
        tm.ok(other)
        tm.that(first.value, is_=ExamplesFlextMeltanoTargetSink)
        tm.that(again.value is first.value, eq=True)
        tm.that(other.value is first.value, eq=False)

    @staticmethod
    def test_records_reach_the_stream_sink_and_flush_drains_it() -> None:
        """process_record routes into the stream sink; flush marks it drained."""
        service = ExamplesFlextMeltanoTargetService()
        record = {"id": "order-1"}

        tm.ok(service.process_record("orders", record, {"properties": {}}))
        tm.ok(service.flush())

        sink = service.fetch_or_create_sink("orders", {"properties": {}}).value
        tm.that(sink, is_=ExamplesFlextMeltanoTargetSink)
        if isinstance(sink, ExamplesFlextMeltanoTargetSink):
            tm.that(sink.records, eq=[record])
            tm.that(sink.drained, eq=True)
