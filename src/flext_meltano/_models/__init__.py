# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Models package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .cli_inputs import FlextMeltanoModelsCliInputs as FlextMeltanoModelsCliInputs
    from .cli_params import FlextMeltanoModelsCliParams as FlextMeltanoModelsCliParams
    from .context import FlextMeltanoModelsContext as FlextMeltanoModelsContext
    from .core import FlextMeltanoModelsCore as FlextMeltanoModelsCore
    from .discovery import FlextMeltanoModelsDiscovery as FlextMeltanoModelsDiscovery
    from .instances import FlextMeltanoModelsInstances as FlextMeltanoModelsInstances
    from .instances_data import (
        FlextMeltanoModelsInstancesData as FlextMeltanoModelsInstancesData,
    )
    from .logging_config import FlextMeltanoModelsLogging as FlextMeltanoModelsLogging
    from .payloads import FlextMeltanoModelsPayloads as FlextMeltanoModelsPayloads
    from .payloads_data import (
        FlextMeltanoModelsPayloadsData as FlextMeltanoModelsPayloadsData,
    )
    from .projects import FlextMeltanoModelsProjects as FlextMeltanoModelsProjects
    from .projects_plugin import (
        FlextMeltanoModelsProjectsPlugin as FlextMeltanoModelsProjectsPlugin,
    )
    from .results import FlextMeltanoModelsResults as FlextMeltanoModelsResults
    from .results_dbt import (
        FlextMeltanoModelsResultsDbt as FlextMeltanoModelsResultsDbt,
    )
    from .results_pipeline import (
        FlextMeltanoModelsResultsPipeline as FlextMeltanoModelsResultsPipeline,
    )
    from .singer import FlextMeltanoModelsSinger as FlextMeltanoModelsSinger
    from .singer_catalog import (
        FlextMeltanoModelsSingerCatalog as FlextMeltanoModelsSingerCatalog,
    )
    from .singer_sdk import FlextMeltanoModelsSingerSdk as FlextMeltanoModelsSingerSdk
    from .sources import FlextMeltanoModelsSources as FlextMeltanoModelsSources
    from .sources_params import (
        FlextMeltanoModelsSourcesParams as FlextMeltanoModelsSourcesParams,
    )
    from .transformations import (
        FlextMeltanoModelsTransformations as FlextMeltanoModelsTransformations,
    )

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".cli_inputs": ("FlextMeltanoModelsCliInputs",),
    ".cli_params": ("FlextMeltanoModelsCliParams",),
    ".context": ("FlextMeltanoModelsContext",),
    ".core": ("FlextMeltanoModelsCore",),
    ".discovery": ("FlextMeltanoModelsDiscovery",),
    ".instances": ("FlextMeltanoModelsInstances",),
    ".instances_data": ("FlextMeltanoModelsInstancesData",),
    ".logging_config": ("FlextMeltanoModelsLogging",),
    ".payloads": ("FlextMeltanoModelsPayloads",),
    ".payloads_data": ("FlextMeltanoModelsPayloadsData",),
    ".projects": ("FlextMeltanoModelsProjects",),
    ".projects_plugin": ("FlextMeltanoModelsProjectsPlugin",),
    ".results": ("FlextMeltanoModelsResults",),
    ".results_dbt": ("FlextMeltanoModelsResultsDbt",),
    ".results_pipeline": ("FlextMeltanoModelsResultsPipeline",),
    ".singer": ("FlextMeltanoModelsSinger",),
    ".singer_catalog": ("FlextMeltanoModelsSingerCatalog",),
    ".singer_sdk": ("FlextMeltanoModelsSingerSdk",),
    ".sources": ("FlextMeltanoModelsSources",),
    ".sources_params": ("FlextMeltanoModelsSourcesParams",),
    ".transformations": ("FlextMeltanoModelsTransformations",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextMeltanoModelsCliInputs",
    "FlextMeltanoModelsCliParams",
    "FlextMeltanoModelsContext",
    "FlextMeltanoModelsCore",
    "FlextMeltanoModelsDiscovery",
    "FlextMeltanoModelsInstances",
    "FlextMeltanoModelsInstancesData",
    "FlextMeltanoModelsLogging",
    "FlextMeltanoModelsPayloads",
    "FlextMeltanoModelsPayloadsData",
    "FlextMeltanoModelsProjects",
    "FlextMeltanoModelsProjectsPlugin",
    "FlextMeltanoModelsResults",
    "FlextMeltanoModelsResultsDbt",
    "FlextMeltanoModelsResultsPipeline",
    "FlextMeltanoModelsSinger",
    "FlextMeltanoModelsSingerCatalog",
    "FlextMeltanoModelsSingerSdk",
    "FlextMeltanoModelsSources",
    "FlextMeltanoModelsSourcesParams",
    "FlextMeltanoModelsTransformations",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
