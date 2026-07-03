"""Singer SDK base class re-exports inside m.Meltano namespace.

Absorbs the loose module-level aliases from singer/sdk.py into a proper
namespace class per AGENTS.md §2.2.

Base classes (Tap, Sink, Stream, Target) are re-exported as-is via assignment
so consumers can subclass them. Type aliases (Context, Record) are also
direct assignments to preserve identity with singer_sdk originals.

Access pattern: m.Meltano.SingerTapBase, m.Meltano.SingerTargetBase, etc.
"""

from __future__ import annotations

import singer_sdk.typing as singer_sdk_typing
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
    SingerArrayType = singer_sdk_typing.ArrayType
    SingerBooleanType = singer_sdk_typing.BooleanType
    SingerCustomType = singer_sdk_typing.CustomType
    SingerDateTimeType = singer_sdk_typing.DateTimeType
    SingerDateType = singer_sdk_typing.DateType
    SingerDurationType = singer_sdk_typing.DurationType
    SingerIntegerType = singer_sdk_typing.IntegerType
    SingerNumberType = singer_sdk_typing.NumberType
    SingerObjectType = singer_sdk_typing.ObjectType
    SingerPropertiesList = singer_sdk_typing.PropertiesList
    SingerProperty = singer_sdk_typing.Property
    SingerStringType = singer_sdk_typing.StringType
    SingerTimeType = singer_sdk_typing.TimeType
