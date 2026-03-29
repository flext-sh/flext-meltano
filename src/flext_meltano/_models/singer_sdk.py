"""Singer SDK base class re-exports inside m.Meltano namespace.

Absorbs the loose module-level aliases from singer/sdk.py into a proper
namespace class per AGENTS.md §2.2. Follows the same flat naming pattern
as FlextMeltanoModelsSinger (SingerSchemaMessage, SingerRecordMessage, etc.)

Access pattern: m.Meltano.SingerTapBase, m.Meltano.SingerTargetBase, etc.
"""

from __future__ import annotations

from singer_sdk import Sink
from singer_sdk.helpers.types import Context, Record
from singer_sdk.streams import Stream
from singer_sdk.tap_base import Tap
from singer_sdk.target_base import Target


class FlextMeltanoModelsSingerSdk:
    """Singer SDK framework base classes for tap/target/stream implementations.

    Provides type-safe access to Singer SDK framework classes through
    the canonical m.Meltano.Singer* namespace. Consumers subclass these
    instead of importing singer_sdk directly.
    """

    SingerTapBase = Tap
    SingerSinkBase = Sink
    SingerStreamBase = Stream
    SingerTargetBase = Target
    SingerContext = Context
    SingerRecord = Record
