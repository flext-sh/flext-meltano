"""Canonical Singer SDK bridge owned by flext-meltano."""

from __future__ import annotations

from collections.abc import Sequence

from singer_sdk import Sink
from singer_sdk.helpers.types import Context, Record
from singer_sdk.streams import Stream
from singer_sdk.tap_base import Tap

FlextMeltanoSingerContext = Context
FlextMeltanoSingerRecord = Record
FlextMeltanoSingerSinkBase = Sink
FlextMeltanoSingerStreamBase = Stream
FlextMeltanoSingerTapBase = Tap

__all__: Sequence[str] = [
    "FlextMeltanoSingerContext",
    "FlextMeltanoSingerRecord",
    "FlextMeltanoSingerSinkBase",
    "FlextMeltanoSingerStreamBase",
    "FlextMeltanoSingerTapBase",
]
