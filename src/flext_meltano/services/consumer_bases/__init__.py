# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Consumer bases package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextMeltanoDbtServiceBase": (
        "flext_meltano.services.consumer_bases.dbt_service_base",
        "FlextMeltanoDbtServiceBase",
    ),
    "FlextMeltanoTapServiceBase": (
        "flext_meltano.services.consumer_bases.tap_service_base",
        "FlextMeltanoTapServiceBase",
    ),
    "FlextMeltanoTargetServiceBase": (
        "flext_meltano.services.consumer_bases.target_service_base",
        "FlextMeltanoTargetServiceBase",
    ),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
