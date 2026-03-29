"""Singer SDK bridge — delegates to m.Meltano.Singer* namespace classes.

Module-level aliases exist for lazy-import registration: the root __init__.py
and singer/__init__.py both reference ``flext_meltano.singer.sdk.<Name>`` in
their _LAZY_IMPORTS tables. Removing these aliases would break lazy loading.
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
