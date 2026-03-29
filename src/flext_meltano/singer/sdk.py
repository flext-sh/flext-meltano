"""Singer SDK bridge — delegates to m.Meltano.Singer* namespace classes.

Kept as thin re-export module for backward compatibility during migration.
Canonical access is via m.Meltano.SingerTapBase, m.Meltano.SingerTargetBase, etc.
"""

from __future__ import annotations

from collections.abc import Sequence

from flext_meltano._models.singer_sdk import FlextMeltanoModelsSingerSdk

FlextMeltanoSingerContext = FlextMeltanoModelsSingerSdk.SingerContext
FlextMeltanoSingerRecord = FlextMeltanoModelsSingerSdk.SingerRecord
FlextMeltanoSingerSinkBase = FlextMeltanoModelsSingerSdk.SingerSinkBase
FlextMeltanoSingerStreamBase = FlextMeltanoModelsSingerSdk.SingerStreamBase
FlextMeltanoSingerTapBase = FlextMeltanoModelsSingerSdk.SingerTapBase
FlextMeltanoSingerTargetBase = FlextMeltanoModelsSingerSdk.SingerTargetBase

__all__: Sequence[str] = [
    "FlextMeltanoSingerContext",
    "FlextMeltanoSingerRecord",
    "FlextMeltanoSingerSinkBase",
    "FlextMeltanoSingerStreamBase",
    "FlextMeltanoSingerTapBase",
    "FlextMeltanoSingerTargetBase",
]
