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
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "dbt_service_base": "flext_meltano.services.consumer_bases.dbt_service_base",
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "tap_service_base": "flext_meltano.services.consumer_bases.tap_service_base",
    "target_service_base": "flext_meltano.services.consumer_bases.target_service_base",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
