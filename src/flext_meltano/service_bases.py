"""Root re-exports of the Singer/dbt service classes consumers build on.

Consumer packages import these from ``flext_meltano`` (package root ABI).
Implementations live under ``flext_meltano.services``.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano.services.abstractions import FlextMeltanoAbstractions
from flext_meltano.services.consumer_bases.dbt_service_base import (
    FlextMeltanoDbtServiceBase,
)
from flext_meltano.services.consumer_bases.tap_service_base import (
    FlextMeltanoTapServiceBase,
)
from flext_meltano.services.consumer_bases.target_service_base import (
    FlextMeltanoTargetServiceBase,
)
from flext_meltano.services.library_runner import FlextMeltanoLibraryRunner
from flext_meltano.services.singer_sdk import FlextMeltanoSingerTapAdapter
from flext_meltano.services.singer_target import FlextMeltanoTargetAbstractions

__all__: list[str] = [
    "FlextMeltanoAbstractions",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoSingerTapAdapter",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTargetServiceBase",
]
