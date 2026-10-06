# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports
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
    from flext_meltano.services.service import FlextMeltanoService
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

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextMeltano": ".api",
        "FlextMeltanoAbstractions": ".services.abstractions",
        "FlextMeltanoAdapter": ".services.adapters",
        "FlextMeltanoBridge": ".services.bridge",
        "FlextMeltanoCli": ".cli",
        "FlextMeltanoComponentService": ".services.meltano_plugins",
        "FlextMeltanoConfig": "._config",
        "FlextMeltanoConstants": ".constants",
        "FlextMeltanoConsumerBases": ".services.consumer_bases.facade",
        "FlextMeltanoDbtProjectMixin": ".services.dbt_project",
        "FlextMeltanoDbtRunnerMixin": ".services.dbt_runner",
        "FlextMeltanoDbtServiceBase": ".service_bases",
        "FlextMeltanoDeclarativeTap": ".services.declarative_tap",
        "FlextMeltanoExecutor": ".services.executor",
        "FlextMeltanoLibraryRunner": ".service_bases",
        "FlextMeltanoModels": ".models",
        "FlextMeltanoPipelineManager": ".pipeline_mgr",
        "FlextMeltanoPluginDiscoveryMixin": ".services.meltano_plugin_discovery",
        "FlextMeltanoProjectManager": ".services.meltano_project_sdk",
        "FlextMeltanoProjectService": ".services.project_service",
        "FlextMeltanoProtocols": ".protocols",
        "FlextMeltanoService": ".services.service",
        "FlextMeltanoServiceBase": ".base",
        "FlextMeltanoSettings": "._settings",
        "FlextMeltanoSingerCatalogMixin": ".services.singer_catalog",
        "FlextMeltanoSingerCliTranslator": ".services.singer_translator",
        "FlextMeltanoSingerStateMixin": ".services.singer_state",
        "FlextMeltanoSingerTapAdapter": ".services.singer_sdk",
        "FlextMeltanoTapAbstractions": ".services.singer_tap",
        "FlextMeltanoTapServiceBase": ".service_bases",
        "FlextMeltanoTapSourceMixin": ".services.tap_source_mixin",
        "FlextMeltanoTargetAbstractions": ".services.singer_target",
        "FlextMeltanoTargetServiceBase": ".service_bases",
        "FlextMeltanoTypes": ".typings",
        "FlextMeltanoUtilities": ".utilities",
        "FlextMeltanoValidators": ".services.validators",
        "Sink": ".services.singer_sdk",
        "Stream": ".services.singer_sdk",
        "Tap": ".services.singer_sdk",
        "Target": ".services.singer_sdk",
        "c": ".constants",
        "config": "._config",
        "d": "flext_cli",
        "e": "flext_cli",
        "h": "flext_cli",
        "m": ".models",
        "main": ".cli",
        "meltano": ".api",
        "p": ".protocols",
        "r": "flext_cli",
        "s": ".base",
        "services": ".services",
        "settings": "._settings",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_cli",
    }),
    public_exports=__all__,
)
