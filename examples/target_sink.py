"""In-memory Singer drain sink for the flext-meltano target example - REAL usage.

The sink constructor matches ``p.Meltano.SinkFactory``, so a target service binds
the class itself as its ``sink_factory``.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import t


class ExamplesFlextMeltanoTargetSink:
    """Drain sink keeping every record of one stream in memory."""

    def __init__(
        self,
        *,
        stream_name: str,
        schema: t.JsonMapping,
        target_config: t.JsonMapping,
    ) -> None:
        """Bind the sink to one stream, its schema and the target configuration."""
        self.stream_name = stream_name
        self.schema = schema
        self.target_config = target_config
        self.records: t.MutableSequenceOf[t.Meltano.MutableContainerValueMapping] = []
        self.drained = False

    @staticmethod
    def start_drain() -> t.Meltano.MutableContainerValueMapping:
        """Open a drain cycle.

        Returns:
            The drain context passed to ``process_batch``.

        """
        return {}

    @staticmethod
    def process_batch(context: t.Meltano.MutableContainerValueMapping) -> None:
        """Accept the drained batch; the records are already kept in memory."""
        _ = context

    def mark_drained(self) -> None:
        """Record that the pending batch was drained."""
        self.drained = True

    def process_record(
        self,
        record: t.Meltano.MutableContainerValueMapping,
        context: t.Meltano.MutableContainerValueMapping,
    ) -> None:
        """Keep one record of the stream."""
        _ = context
        self.records.append(record)


__all__: list[str] = ["ExamplesFlextMeltanoTargetSink"]
