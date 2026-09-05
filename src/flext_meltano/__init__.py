# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_cli import d, e, h, r, x

    from . import services as services
    from ._config import FlextMeltanoConfig, config
    from ._settings import FlextMeltanoSettings, settings
    from .api import FlextMeltano, meltano
    from .base import FlextMeltanoServiceBase, FlextMeltanoServiceBase as s
    from .cli import FlextMeltanoCli, main
    from .constants import FlextMeltanoConstants, FlextMeltanoConstants as c
    from .models import FlextMeltanoModels, FlextMeltanoModels as m
    from .pipeline_mgr import FlextMeltanoPipelineManager
    from .protocols import FlextMeltanoProtocols, FlextMeltanoProtocols as p
    from .service_bases import FlextMeltanoDbtServiceBase
    from .services.abstractions import FlextMeltanoAbstractions
    from .services.adapters import FlextMeltanoAdapter
    from .services.bridge import FlextMeltanoBridge
    from .services.consumer_bases.facade import FlextMeltanoConsumerBases
    from .services.consumer_bases.tap_service_base import FlextMeltanoTapServiceBase
    from .services.consumer_bases.target_service_base import (
        FlextMeltanoTargetServiceBase,
    )
    from .services.dbt_project import FlextMeltanoDbtProjectMixin
    from .services.dbt_runner import FlextMeltanoDbtRunnerMixin
    from .services.declarative_tap import FlextMeltanoDeclarativeTap
    from .services.executor import FlextMeltanoExecutor
    from .services.library_runner import FlextMeltanoLibraryRunner
    from .services.meltano_plugin_discovery import FlextMeltanoPluginDiscoveryMixin
    from .services.meltano_plugins import FlextMeltanoComponentService
    from .services.meltano_project_sdk import FlextMeltanoProjectManager
    from .services.project_service import FlextMeltanoProjectService
    from .services.services import FlextMeltanoService
    from .services.singer_catalog import FlextMeltanoSingerCatalogMixin
    from .services.singer_sdk import (
        FlextMeltanoSingerTapAdapter,
        Sink,
        Stream,
        Tap,
        Target,
    )
    from .services.singer_state import FlextMeltanoSingerStateMixin
    from .services.singer_tap import (
        FlextMeltanoTapAbstractions,
        FlextMeltanoTapSourceMixin,
    )
    from .services.singer_target import FlextMeltanoTargetAbstractions
    from .services.singer_translator import FlextMeltanoSingerCliTranslator
    from .services.validators import FlextMeltanoValidators
    from .typings import FlextMeltanoTypes, FlextMeltanoTypes as t
    from .utilities import FlextMeltanoUtilities, FlextMeltanoUtilities as u
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
            ".service_bases": ("FlextMeltanoDbtServiceBase",),
            ".services": ("services",),
            ".services.abstractions": ("FlextMeltanoAbstractions",),
            ".services.adapters": ("FlextMeltanoAdapter",),
            ".services.bridge": ("FlextMeltanoBridge",),
            ".services.consumer_bases.facade": ("FlextMeltanoConsumerBases",),
            ".services.consumer_bases.tap_service_base": (
                "FlextMeltanoTapServiceBase",
            ),
            ".services.consumer_bases.target_service_base": (
                "FlextMeltanoTargetServiceBase",
            ),
            ".services.dbt_project": ("FlextMeltanoDbtProjectMixin",),
            ".services.dbt_runner": ("FlextMeltanoDbtRunnerMixin",),
            ".services.declarative_tap": ("FlextMeltanoDeclarativeTap",),
            ".services.executor": ("FlextMeltanoExecutor",),
            ".services.library_runner": ("FlextMeltanoLibraryRunner",),
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
            ".services.singer_tap": (
                "FlextMeltanoTapAbstractions",
                "FlextMeltanoTapSourceMixin",
            ),
            ".services.singer_target": ("FlextMeltanoTargetAbstractions",),
            ".services.singer_translator": ("FlextMeltanoSingerCliTranslator",),
            ".services.validators": ("FlextMeltanoValidators",),
            ".typings": ("FlextMeltanoTypes", "t"),
            ".utilities": ("FlextMeltanoUtilities", "u"),
            "flext_cli": ("d", "e", "h", "r", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
