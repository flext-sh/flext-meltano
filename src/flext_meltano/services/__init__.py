# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano.services package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano.services import consumer_bases
    from flext_meltano.services.abstractions import FlextMeltanoAbstractions
    from flext_meltano.services.adapters import FlextMeltanoAdapter
    from flext_meltano.services.bridge import FlextMeltanoBridge
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
    from flext_meltano.services.dbt_project import FlextMeltanoDbtProjectMixin
    from flext_meltano.services.dbt_runner import FlextMeltanoDbtRunnerMixin
    from flext_meltano.services.declarative_tap import FlextMeltanoDeclarativeTap
    from flext_meltano.services.executor import FlextMeltanoExecutor
    from flext_meltano.services.library_runner import FlextMeltanoLibraryRunner
    from flext_meltano.services.meltano_plugin_discovery import (
        FlextMeltanoPluginDiscoveryMixin,
    )
    from flext_meltano.services.meltano_plugins import FlextMeltanoComponentService
    from flext_meltano.services.meltano_project_sdk import FlextMeltanoProjectManager
    from flext_meltano.services.project_service import FlextMeltanoProjectService
    from flext_meltano.services.services import FlextMeltanoService
    from flext_meltano.services.singer_catalog import FlextMeltanoSingerCatalogMixin
    from flext_meltano.services.singer_sdk import (
        FlextMeltanoSingerTapAdapter,
        Sink,
        Stream,
        Tap,
        Target,
    )
    from flext_meltano.services.singer_state import FlextMeltanoSingerStateMixin
    from flext_meltano.services.singer_tap import FlextMeltanoTapAbstractions
    from flext_meltano.services.singer_target import FlextMeltanoTargetAbstractions
    from flext_meltano.services.singer_translator import FlextMeltanoSingerCliTranslator
    from flext_meltano.services.tap_source_mixin import FlextMeltanoTapSourceMixin
    from flext_meltano.services.validators import FlextMeltanoValidators


__all__: tuple[str, ...] = (
    "FlextMeltanoAbstractions",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoComponentService",
    "FlextMeltanoConsumerBases",
    "FlextMeltanoDbtProjectMixin",
    "FlextMeltanoDbtRunnerMixin",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoDeclarativeTap",
    "FlextMeltanoExecutor",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoPluginDiscoveryMixin",
    "FlextMeltanoProjectManager",
    "FlextMeltanoProjectService",
    "FlextMeltanoService",
    "FlextMeltanoSingerCatalogMixin",
    "FlextMeltanoSingerCliTranslator",
    "FlextMeltanoSingerStateMixin",
    "FlextMeltanoSingerTapAdapter",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTapSourceMixin",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTargetServiceBase",
    "FlextMeltanoValidators",
    "Sink",
    "Stream",
    "Tap",
    "Target",
    "consumer_bases",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextMeltanoAbstractions": ".abstractions",
        "FlextMeltanoAdapter": ".adapters",
        "FlextMeltanoBridge": ".bridge",
        "FlextMeltanoComponentService": ".meltano_plugins",
        "FlextMeltanoConsumerBases": ".consumer_bases.facade",
        "FlextMeltanoDbtProjectMixin": ".dbt_project",
        "FlextMeltanoDbtRunnerMixin": ".dbt_runner",
        "FlextMeltanoDbtServiceBase": ".consumer_bases.dbt_service_base",
        "FlextMeltanoDeclarativeTap": ".declarative_tap",
        "FlextMeltanoExecutor": ".executor",
        "FlextMeltanoLibraryRunner": ".library_runner",
        "FlextMeltanoPluginDiscoveryMixin": ".meltano_plugin_discovery",
        "FlextMeltanoProjectManager": ".meltano_project_sdk",
        "FlextMeltanoProjectService": ".project_service",
        "FlextMeltanoService": ".services",
        "FlextMeltanoSingerCatalogMixin": ".singer_catalog",
        "FlextMeltanoSingerCliTranslator": ".singer_translator",
        "FlextMeltanoSingerStateMixin": ".singer_state",
        "FlextMeltanoSingerTapAdapter": ".singer_sdk",
        "FlextMeltanoTapAbstractions": ".singer_tap",
        "FlextMeltanoTapServiceBase": ".consumer_bases.tap_service_base",
        "FlextMeltanoTapSourceMixin": ".tap_source_mixin",
        "FlextMeltanoTargetAbstractions": ".singer_target",
        "FlextMeltanoTargetServiceBase": ".consumer_bases.target_service_base",
        "FlextMeltanoValidators": ".validators",
        "Sink": ".singer_sdk",
        "Stream": ".singer_sdk",
        "Tap": ".singer_sdk",
        "Target": ".singer_sdk",
        "consumer_bases": ".consumer_bases",
    }),
    public_exports=__all__,
)
