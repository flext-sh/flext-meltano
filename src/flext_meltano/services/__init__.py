# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano.services package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano.services.abstractions import FlextMeltanoAbstractions
    from flext_meltano.services.consumer_bases import (
        FlextMeltanoConsumerBases,
        FlextMeltanoDbtServiceBase,
        FlextMeltanoTapServiceBase,
        FlextMeltanoTargetServiceBase,
    )
    from flext_meltano.services.declarative_tap import FlextMeltanoDeclarativeTap
    from flext_meltano.services.executor import FlextMeltanoExecutor
    from flext_meltano.services.executor_base import FlextMeltanoExecutorBase
    from flext_meltano.services.library_runner import FlextMeltanoLibraryRunner
    from flext_meltano.services.meltano_plugin_discovery import (
        FlextMeltanoPluginDiscoveryMixin,
    )
    from flext_meltano.services.project_service import FlextMeltanoProjectService
    from flext_meltano.services.service import FlextMeltanoService
    from flext_meltano.services.singer_sdk import FlextMeltanoSingerTapAdapter
    from flext_meltano.services.singer_target import FlextMeltanoTargetAbstractions


__all__: tuple[str, ...] = (
    "FlextMeltanoAbstractions",
    "FlextMeltanoConsumerBases",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoDeclarativeTap",
    "FlextMeltanoExecutor",
    "FlextMeltanoExecutorBase",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoPluginDiscoveryMixin",
    "FlextMeltanoProjectService",
    "FlextMeltanoService",
    "FlextMeltanoSingerTapAdapter",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTargetServiceBase",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextMeltanoAbstractions": ".abstractions",
        "FlextMeltanoConsumerBases": ".consumer_bases.facade",
        "FlextMeltanoDbtServiceBase": ".consumer_bases.dbt_service_base",
        "FlextMeltanoDeclarativeTap": ".declarative_tap",
        "FlextMeltanoExecutor": ".executor",
        "FlextMeltanoExecutorBase": ".executor_base",
        "FlextMeltanoLibraryRunner": ".library_runner",
        "FlextMeltanoPluginDiscoveryMixin": ".meltano_plugin_discovery",
        "FlextMeltanoProjectService": ".project_service",
        "FlextMeltanoService": ".service",
        "FlextMeltanoSingerTapAdapter": ".singer_sdk",
        "FlextMeltanoTapServiceBase": ".consumer_bases.tap_service_base",
        "FlextMeltanoTargetAbstractions": ".singer_target",
        "FlextMeltanoTargetServiceBase": ".consumer_bases.target_service_base",
    }),
    public_exports=__all__,
)
