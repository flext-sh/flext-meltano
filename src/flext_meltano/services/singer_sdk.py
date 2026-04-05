"""Singer SDK bridge — canonical re-exports for consumer projects.

Module-level aliases exist for lazy-import registration: the root __init__.py
and singer/__init__.py both reference ``flext_meltano.singer.sdk.<Name>`` in
their _LAZY_IMPORTS tables.

These are direct re-exports from singer_sdk (allowed in flext-meltano/src/)
so that mypy recognizes them as valid types for subclassing.
"""

from __future__ import annotations

from singer_sdk import Sink
from singer_sdk.helpers.types import Context, Record
from singer_sdk.streams import Stream
from singer_sdk.tap_base import Tap
from singer_sdk.target_base import Target

from flext_meltano import t

FlextMeltanoSingerContext = Context
FlextMeltanoSingerRecord = Record
FlextMeltanoSingerSinkBase = Sink
FlextMeltanoSingerStreamBase = Stream
FlextMeltanoSingerTapBase = Tap
FlextMeltanoSingerTargetBase = Target

__all__: t.StrSequence = [
    "FlextMeltanoSingerContext",
    "FlextMeltanoSingerRecord",
    "FlextMeltanoSingerSinkBase",
    "FlextMeltanoSingerStreamBase",
    "FlextMeltanoSingerTapBase",
    "FlextMeltanoSingerTargetBase",
]
