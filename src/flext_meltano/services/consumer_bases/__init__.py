# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Consumer bases package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_meltano.services.consumer_bases.dbt_service_base as _flext_meltano_services_consumer_bases_dbt_service_base

    dbt_service_base = _flext_meltano_services_consumer_bases_dbt_service_base
    import flext_meltano.services.consumer_bases.tap_service_base as _flext_meltano_services_consumer_bases_tap_service_base
    from flext_meltano.services.consumer_bases.dbt_service_base import (
        FlextMeltanoDbtServiceBase,
    )

    tap_service_base = _flext_meltano_services_consumer_bases_tap_service_base
    import flext_meltano.services.consumer_bases.target_service_base as _flext_meltano_services_consumer_bases_target_service_base
    from flext_meltano.services.consumer_bases.tap_service_base import (
        FlextMeltanoTapServiceBase,
    )

    target_service_base = _flext_meltano_services_consumer_bases_target_service_base
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from flext_meltano.services.consumer_bases.target_service_base import (
        FlextMeltanoTargetServiceBase,
    )
_LAZY_IMPORTS = {
    "FlextMeltanoDbtServiceBase": "flext_meltano.services.consumer_bases.dbt_service_base",
    "FlextMeltanoTapServiceBase": "flext_meltano.services.consumer_bases.tap_service_base",
    "FlextMeltanoTargetServiceBase": "flext_meltano.services.consumer_bases.target_service_base",
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

__all__ = [
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTargetServiceBase",
    "c",
    "d",
    "dbt_service_base",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "tap_service_base",
    "target_service_base",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
