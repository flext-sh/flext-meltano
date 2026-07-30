# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano.services.consumer Bases package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .dbt_service_base import (
        FlextMeltanoDbtServiceBase as FlextMeltanoDbtServiceBase,
    )
    from .facade import FlextMeltanoConsumerBases as FlextMeltanoConsumerBases
    from .tap_service_base import (
        FlextMeltanoTapServiceBase as FlextMeltanoTapServiceBase,
    )
    from .target_service_base import (
        FlextMeltanoTargetServiceBase as FlextMeltanoTargetServiceBase,
    )

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".dbt_service_base": ("FlextMeltanoDbtServiceBase",),
    ".facade": ("FlextMeltanoConsumerBases",),
    ".tap_service_base": ("FlextMeltanoTapServiceBase",),
    ".target_service_base": ("FlextMeltanoTargetServiceBase",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextMeltanoConsumerBases",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTargetServiceBase",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
