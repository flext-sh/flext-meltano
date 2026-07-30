# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano.services package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import consumer_bases as consumer_bases
    from .abstractions import FlextMeltanoAbstractions as FlextMeltanoAbstractions
    from .abstractions_base import (
        FlextMeltanoAbstractionsBase as FlextMeltanoAbstractionsBase,
    )
    from .adapters import FlextMeltanoAdapter as FlextMeltanoAdapter
    from .bridge import FlextMeltanoBridge as FlextMeltanoBridge
    from .consumer_bases.dbt_service_base import (
        FlextMeltanoDbtServiceBase as FlextMeltanoDbtServiceBase,
    )
    from .consumer_bases.facade import (
        FlextMeltanoConsumerBases as FlextMeltanoConsumerBases,
    )
    from .consumer_bases.tap_service_base import (
        FlextMeltanoTapServiceBase as FlextMeltanoTapServiceBase,
    )
    from .consumer_bases.target_service_base import (
        FlextMeltanoTargetServiceBase as FlextMeltanoTargetServiceBase,
    )
    from .dbt_project import FlextMeltanoDbtProjectMixin as FlextMeltanoDbtProjectMixin
    from .dbt_runner import FlextMeltanoDbtRunnerMixin as FlextMeltanoDbtRunnerMixin
    from .declarative_tap import (
        FlextMeltanoDeclarativeTap as FlextMeltanoDeclarativeTap,
    )
    from .executor import FlextMeltanoExecutor as FlextMeltanoExecutor
    from .executor_base import FlextMeltanoExecutorBase as FlextMeltanoExecutorBase
    from .library_runner import FlextMeltanoLibraryRunner as FlextMeltanoLibraryRunner
    from .meltano_plugin_discovery import (
        FlextMeltanoPluginDiscoveryMixin as FlextMeltanoPluginDiscoveryMixin,
    )
    from .meltano_plugins import (
        FlextMeltanoComponentService as FlextMeltanoComponentService,
    )
    from .meltano_project_sdk import (
        FlextMeltanoProjectManager as FlextMeltanoProjectManager,
    )
    from .project_service import (
        FlextMeltanoProjectService as FlextMeltanoProjectService,
    )
    from .services import FlextMeltanoService as FlextMeltanoService
    from .singer_catalog import (
        FlextMeltanoSingerCatalogMixin as FlextMeltanoSingerCatalogMixin,
    )
    from .singer_sdk import FlextMeltanoSingerTapAdapter as FlextMeltanoSingerTapAdapter
    from .singer_sdk import Sink as Sink
    from .singer_sdk import Stream as Stream
    from .singer_sdk import Tap as Tap
    from .singer_sdk import Target as Target
    from .singer_state import (
        FlextMeltanoSingerStateMixin as FlextMeltanoSingerStateMixin,
    )
    from .singer_tap import FlextMeltanoTapAbstractions as FlextMeltanoTapAbstractions
    from .singer_tap import FlextMeltanoTapSourceMixin as FlextMeltanoTapSourceMixin
    from .singer_target import (
        FlextMeltanoTargetAbstractions as FlextMeltanoTargetAbstractions,
    )
    from .singer_translator import (
        FlextMeltanoSingerCliTranslator as FlextMeltanoSingerCliTranslator,
    )
    from .validators import FlextMeltanoValidators as FlextMeltanoValidators

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".abstractions": ("FlextMeltanoAbstractions",),
    ".abstractions_base": ("FlextMeltanoAbstractionsBase",),
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
    ".executor_base": ("FlextMeltanoExecutorBase",),
    ".library_runner": ("FlextMeltanoLibraryRunner",),
    ".meltano_plugin_discovery": ("FlextMeltanoPluginDiscoveryMixin",),
    ".meltano_plugins": ("FlextMeltanoComponentService",),
    ".meltano_project_sdk": ("FlextMeltanoProjectManager",),
    ".project_service": ("FlextMeltanoProjectService",),
    ".services": ("FlextMeltanoService",),
    ".singer_catalog": ("FlextMeltanoSingerCatalogMixin",),
    ".singer_sdk": ("FlextMeltanoSingerTapAdapter", "Sink", "Stream", "Tap", "Target"),
    ".singer_state": ("FlextMeltanoSingerStateMixin",),
    ".singer_tap": ("FlextMeltanoTapAbstractions", "FlextMeltanoTapSourceMixin"),
    ".singer_target": ("FlextMeltanoTargetAbstractions",),
    ".singer_translator": ("FlextMeltanoSingerCliTranslator",),
    ".validators": ("FlextMeltanoValidators",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextMeltanoAbstractions",
    "FlextMeltanoAbstractionsBase",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoComponentService",
    "FlextMeltanoConsumerBases",
    "FlextMeltanoDbtProjectMixin",
    "FlextMeltanoDbtRunnerMixin",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoDeclarativeTap",
    "FlextMeltanoExecutor",
    "FlextMeltanoExecutorBase",
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

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
