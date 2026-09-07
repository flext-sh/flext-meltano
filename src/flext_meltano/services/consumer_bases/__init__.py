# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano.services.consumer Bases package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .dbt_service_base import FlextMeltanoDbtServiceBase
    from .facade import FlextMeltanoConsumerBases
    from .tap_service_base import FlextMeltanoTapServiceBase
    from .target_service_base import FlextMeltanoTargetServiceBase
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
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
