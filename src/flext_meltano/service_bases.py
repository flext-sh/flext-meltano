"""Root re-exports of Singer/dbt consumer service bases.

Consumer packages import these from ``flext_meltano`` (package root ABI).
Implementations live under ``flext_meltano.services.consumer_bases``.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano.services import FlextMeltanoLibraryRunner
    from flext_meltano.services.consumer_bases import (
        FlextMeltanoDbtServiceBase,
        FlextMeltanoTapServiceBase,
        FlextMeltanoTargetServiceBase,
    )

__all__: list[str] = [
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTargetServiceBase",
]

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextMeltanoDbtServiceBase": (
            "flext_meltano.services.consumer_bases.dbt_service_base"
        ),
        "FlextMeltanoLibraryRunner": "flext_meltano.services",
        "FlextMeltanoTapServiceBase": (
            "flext_meltano.services.consumer_bases.tap_service_base"
        ),
        "FlextMeltanoTargetServiceBase": (
            "flext_meltano.services.consumer_bases.target_service_base"
        ),
    }),
    public_exports=__all__,
)
