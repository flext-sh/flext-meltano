# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano.services package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

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

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".abstractions": ("FlextMeltanoAbstractions",),
            ".adapters": ("FlextMeltanoAdapter",),
            ".bridge": ("FlextMeltanoBridge",),
            ".consumer_bases": ("consumer_bases",),
            ".consumer_bases.dbt_service_base": ("FlextMeltanoDbtServiceBase",),
            ".consumer_bases.facade": ("FlextMeltanoConsumerBases",),
            ".consumer_bases.tap_service_base": ("FlextMeltanoTapServiceBase",),
            ".consumer_bases.target_service_base": ("FlextMeltanoTargetServiceBase",),
            ".dbt_project": ("FlextMeltanoDbtProjectMixin",),
            ".dbt_runner": ("FlextMeltanoDbtRunnerMixin",),
            ".declarative_tap": ("FlextMeltanoDeclarativeTap",),
            ".executor": ("FlextMeltanoExecutor",),
            ".library_runner": ("FlextMeltanoLibraryRunner",),
            ".meltano_plugin_discovery": ("FlextMeltanoPluginDiscoveryMixin",),
            ".meltano_plugins": ("FlextMeltanoComponentService",),
            ".meltano_project_sdk": ("FlextMeltanoProjectManager",),
            ".project_service": ("FlextMeltanoProjectService",),
            ".services": ("FlextMeltanoService",),
            ".singer_catalog": ("FlextMeltanoSingerCatalogMixin",),
            ".singer_sdk": (
                "FlextMeltanoSingerTapAdapter",
                "Sink",
                "Stream",
                "Tap",
                "Target",
            ),
            ".singer_state": ("FlextMeltanoSingerStateMixin",),
            ".singer_tap": ("FlextMeltanoTapAbstractions",),
            ".singer_target": ("FlextMeltanoTargetAbstractions",),
            ".singer_translator": ("FlextMeltanoSingerCliTranslator",),
            ".tap_source_mixin": ("FlextMeltanoTapSourceMixin",),
            ".validators": ("FlextMeltanoValidators",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
