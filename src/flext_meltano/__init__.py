# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports
from flext_meltano.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_cli import d, e, h, r, x

    from flext_meltano import services
    from flext_meltano._config import FlextMeltanoConfig, config
    from flext_meltano._settings import FlextMeltanoSettings, settings
    from flext_meltano.api import FlextMeltano, meltano
    from flext_meltano.base import FlextMeltanoServiceBase, s
    from flext_meltano.cli import FlextMeltanoCli, main
    from flext_meltano.constants import FlextMeltanoConstants, c
    from flext_meltano.models import FlextMeltanoModels, m
    from flext_meltano.pipeline_mgr import FlextMeltanoPipelineManager
    from flext_meltano.protocols import FlextMeltanoProtocols, p
    from flext_meltano.service_bases import (
        FlextMeltanoDbtServiceBase,
        FlextMeltanoLibraryRunner,
        FlextMeltanoTapServiceBase,
        FlextMeltanoTargetServiceBase,
    )
    from flext_meltano.services.abstractions import FlextMeltanoAbstractions
    from flext_meltano.services.adapters import FlextMeltanoAdapter
    from flext_meltano.services.bridge import FlextMeltanoBridge
    from flext_meltano.services.consumer_bases.facade import FlextMeltanoConsumerBases
    from flext_meltano.services.dbt_project import FlextMeltanoDbtProjectMixin
    from flext_meltano.services.dbt_runner import FlextMeltanoDbtRunnerMixin
    from flext_meltano.services.declarative_tap import FlextMeltanoDeclarativeTap
    from flext_meltano.services.executor import FlextMeltanoExecutor
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
    from flext_meltano.typings import FlextMeltanoTypes, t
    from flext_meltano.utilities import FlextMeltanoUtilities, u


__all__: tuple[str, ...] = (
    "FlextMeltano",
    "FlextMeltanoAbstractions",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCli",
    "FlextMeltanoComponentService",
    "FlextMeltanoConfig",
    "FlextMeltanoConstants",
    "FlextMeltanoConsumerBases",
    "FlextMeltanoDbtProjectMixin",
    "FlextMeltanoDbtRunnerMixin",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoDeclarativeTap",
    "FlextMeltanoExecutor",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoModels",
    "FlextMeltanoPipelineManager",
    "FlextMeltanoPluginDiscoveryMixin",
    "FlextMeltanoProjectManager",
    "FlextMeltanoProjectService",
    "FlextMeltanoProtocols",
    "FlextMeltanoService",
    "FlextMeltanoServiceBase",
    "FlextMeltanoSettings",
    "FlextMeltanoSingerCatalogMixin",
    "FlextMeltanoSingerCliTranslator",
    "FlextMeltanoSingerStateMixin",
    "FlextMeltanoSingerTapAdapter",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTapSourceMixin",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTargetServiceBase",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
    "Sink",
    "Stream",
    "Tap",
    "Target",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "config",
    "d",
    "e",
    "h",
    "m",
    "main",
    "meltano",
    "p",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextMeltanoConfig", "config"),
            "._settings": ("FlextMeltanoSettings", "settings"),
            ".api": ("FlextMeltano", "meltano"),
            ".base": ("FlextMeltanoServiceBase", "s"),
            ".cli": ("FlextMeltanoCli", "main"),
            ".constants": ("FlextMeltanoConstants", "c"),
            ".models": ("FlextMeltanoModels", "m"),
            ".pipeline_mgr": ("FlextMeltanoPipelineManager",),
            ".protocols": ("FlextMeltanoProtocols", "p"),
            ".service_bases": (
                "FlextMeltanoDbtServiceBase",
                "FlextMeltanoLibraryRunner",
                "FlextMeltanoTapServiceBase",
                "FlextMeltanoTargetServiceBase",
            ),
            ".services": ("services",),
            ".services.abstractions": ("FlextMeltanoAbstractions",),
            ".services.adapters": ("FlextMeltanoAdapter",),
            ".services.bridge": ("FlextMeltanoBridge",),
            ".services.consumer_bases.facade": ("FlextMeltanoConsumerBases",),
            ".services.dbt_project": ("FlextMeltanoDbtProjectMixin",),
            ".services.dbt_runner": ("FlextMeltanoDbtRunnerMixin",),
            ".services.declarative_tap": ("FlextMeltanoDeclarativeTap",),
            ".services.executor": ("FlextMeltanoExecutor",),
            ".services.meltano_plugin_discovery": ("FlextMeltanoPluginDiscoveryMixin",),
            ".services.meltano_plugins": ("FlextMeltanoComponentService",),
            ".services.meltano_project_sdk": ("FlextMeltanoProjectManager",),
            ".services.project_service": ("FlextMeltanoProjectService",),
            ".services.services": ("FlextMeltanoService",),
            ".services.singer_catalog": ("FlextMeltanoSingerCatalogMixin",),
            ".services.singer_sdk": (
                "FlextMeltanoSingerTapAdapter",
                "Sink",
                "Stream",
                "Tap",
                "Target",
            ),
            ".services.singer_state": ("FlextMeltanoSingerStateMixin",),
            ".services.singer_tap": ("FlextMeltanoTapAbstractions",),
            ".services.singer_target": ("FlextMeltanoTargetAbstractions",),
            ".services.singer_translator": ("FlextMeltanoSingerCliTranslator",),
            ".services.tap_source_mixin": ("FlextMeltanoTapSourceMixin",),
            ".services.validators": ("FlextMeltanoValidators",),
            ".typings": ("FlextMeltanoTypes", "t"),
            ".utilities": ("FlextMeltanoUtilities", "u"),
            "flext_cli": ("d", "e", "h", "r", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
