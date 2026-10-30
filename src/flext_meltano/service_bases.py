"""Root re-exports of the Singer/dbt service classes consumers build on.

Consumer packages import these from ``flext_meltano`` (package root ABI).
Implementations live under ``flext_meltano.services``.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano.services import (
    FlextMeltanoAbstractions,
    FlextMeltanoLibraryRunner,
    FlextMeltanoSingerTapAdapter,
    FlextMeltanoTargetAbstractions,
)
from flext_meltano.services.consumer_bases import (
    FlextMeltanoDbtServiceBase,
    FlextMeltanoTapServiceBase,
    FlextMeltanoTargetServiceBase,
)

__all__: list[str] = [
    "FlextMeltanoAbstractions",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoSingerTapAdapter",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTargetServiceBase",
]
