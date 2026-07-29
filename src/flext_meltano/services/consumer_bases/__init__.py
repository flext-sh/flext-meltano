# AUTO-GENERATED FILE — Regenerate with: make gen
"""Consumer Bases package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano.services.consumer_bases.dbt_service_base import (
        FlextMeltanoDbtServiceBase as FlextMeltanoDbtServiceBase,
    )
    from flext_meltano.services.consumer_bases.tap_service_base import (
        FlextMeltanoTapServiceBase as FlextMeltanoTapServiceBase,
    )
    from flext_meltano.services.consumer_bases.target_service_base import (
        FlextMeltanoTargetServiceBase as FlextMeltanoTargetServiceBase,
    )
_LAZY_IMPORTS = build_lazy_import_map({
    ".dbt_service_base": ("FlextMeltanoDbtServiceBase",),
    ".tap_service_base": ("FlextMeltanoTapServiceBase",),
    ".target_service_base": ("FlextMeltanoTargetServiceBase",),
})


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
