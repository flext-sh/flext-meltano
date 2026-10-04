"""Root re-exports of Singer/dbt consumer service bases.

Consumer packages import these from ``flext_meltano`` (package root ABI).
Implementations live under ``flext_meltano.services.consumer_bases``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

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

__all__: list[str] = [
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTargetServiceBase",
]
