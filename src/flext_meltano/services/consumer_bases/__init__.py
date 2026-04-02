# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Consumer base classes for flext-(tap|target|dbt)-* projects."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_meltano.services.consumer_bases import (
        dbt_service_base,
        tap_service_base,
        target_service_base,
    )
    from flext_meltano.services.consumer_bases.dbt_service_base import (
        FlextMeltanoDbtServiceBase,
    )
    from flext_meltano.services.consumer_bases.tap_service_base import (
        FlextMeltanoTapServiceBase,
    )
    from flext_meltano.services.consumer_bases.target_service_base import (
        FlextMeltanoTargetServiceBase,
    )

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextMeltanoDbtServiceBase": "flext_meltano.services.consumer_bases.dbt_service_base",
    "FlextMeltanoTapServiceBase": "flext_meltano.services.consumer_bases.tap_service_base",
    "FlextMeltanoTargetServiceBase": "flext_meltano.services.consumer_bases.target_service_base",
    "dbt_service_base": "flext_meltano.services.consumer_bases.dbt_service_base",
    "tap_service_base": "flext_meltano.services.consumer_bases.tap_service_base",
    "target_service_base": "flext_meltano.services.consumer_bases.target_service_base",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
