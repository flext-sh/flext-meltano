"""Singer SDK compatibility layer for consolidated plugins."""

from __future__ import annotations

from typing import TYPE_CHECKING

# Re-export Singer SDK classes with consistent naming
try:
    from singer_sdk import (
        Stream as FlextMeltanoStream,
        Tap as FlextMeltanoTap,
        Target as FlextMeltanoTarget,
    )
    from singer_sdk.sinks import (
        Sink as FlextMeltanoSink,
        SQLSink as FlextMeltanoSQLSink,
    )
    SINGER_AVAILABLE = True
except ImportError:
    FlextMeltanoStream = None  # type: ignore[assignment,misc]
    FlextMeltanoTap = None  # type: ignore[assignment,misc]
    FlextMeltanoTarget = None  # type: ignore[assignment,misc]
    FlextMeltanoSink = None  # type: ignore[assignment,misc]
    FlextMeltanoSQLSink = None  # type: ignore[assignment,misc]
    SINGER_AVAILABLE = False

if TYPE_CHECKING and SINGER_AVAILABLE:
    from singer_sdk import Stream, Tap, Target
    from singer_sdk.sinks import Sink, SQLSink
else:
    Stream = None  # type: ignore[assignment,misc]
    Tap = None  # type: ignore[assignment,misc]
    Target = None  # type: ignore[assignment,misc]
    Sink = None  # type: ignore[assignment,misc]
    SQLSink = None  # type: ignore[assignment,misc]

__all__ = [
    "SINGER_AVAILABLE",
    "FlextMeltanoSQLSink",
    "FlextMeltanoSink",
    "FlextMeltanoStream",
    "FlextMeltanoTap",
    "FlextMeltanoTarget",
]
