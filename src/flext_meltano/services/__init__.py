# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano.services package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import consumer_bases as consumer_bases
    from .abstractions import FlextMeltanoAbstractions
    from .adapters import FlextMeltanoAdapter
    from .bridge import FlextMeltanoBridge
    from .consumer_bases.dbt_service_base import FlextMeltanoDbtServiceBase
    from .consumer_bases.facade import FlextMeltanoConsumerBases
    from .consumer_bases.tap_service_base import FlextMeltanoTapServiceBase
    from .consumer_bases.target_service_base import FlextMeltanoTargetServiceBase
    from .dbt_project import FlextMeltanoDbtProjectMixin
    from .dbt_runner import FlextMeltanoDbtRunnerMixin
    from .declarative_tap import FlextMeltanoDeclarativeTap
    from .executor import FlextMeltanoExecutor
    from .library_runner import FlextMeltanoLibraryRunner
    from .meltano_plugin_discovery import FlextMeltanoPluginDiscoveryMixin
    from .meltano_plugins import FlextMeltanoComponentService
    from .meltano_project_sdk import FlextMeltanoProjectManager
    from .project_service import FlextMeltanoProjectService
    from .services import FlextMeltanoService
    from .singer_catalog import FlextMeltanoSingerCatalogMixin
    from .singer_sdk import FlextMeltanoSingerTapAdapter, Sink, Stream, Tap, Target
    from .singer_state import FlextMeltanoSingerStateMixin
    from .singer_tap import FlextMeltanoTapAbstractions, FlextMeltanoTapSourceMixin
    from .singer_target import FlextMeltanoTargetAbstractions
    from .singer_translator import FlextMeltanoSingerCliTranslator
    from .validators import FlextMeltanoValidators
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
            ".singer_tap": (
                "FlextMeltanoTapAbstractions",
                "FlextMeltanoTapSourceMixin",
            ),
            ".singer_target": ("FlextMeltanoTargetAbstractions",),
            ".singer_translator": ("FlextMeltanoSingerCliTranslator",),
            ".validators": ("FlextMeltanoValidators",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
