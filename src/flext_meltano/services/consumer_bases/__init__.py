# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano.services.consumer Bases package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano.services.consumer_bases.dbt_service_base import (
        FlextMeltanoDbtServiceBase,
    )
    from flext_meltano.services.consumer_bases.facade import FlextMeltanoConsumerBases
    from flext_meltano.services.consumer_bases.tap_service_base import (
        FlextMeltanoTapServiceBase,
    )
    from flext_meltano.services.consumer_bases.target_service_base import (
        FlextMeltanoTargetServiceBase,
    )


__all__: tuple[str, ...] = (
    "FlextMeltanoConsumerBases",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTargetServiceBase",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".dbt_service_base": ("FlextMeltanoDbtServiceBase",),
            ".facade": ("FlextMeltanoConsumerBases",),
            ".tap_service_base": ("FlextMeltanoTapServiceBase",),
            ".target_service_base": ("FlextMeltanoTargetServiceBase",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
