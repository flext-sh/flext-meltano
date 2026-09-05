# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Models package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .cli_inputs import FlextMeltanoModelsCliInputs
    from .cli_params import FlextMeltanoModelsCliParams
    from .context import FlextMeltanoModelsContext
    from .core import FlextMeltanoModelsCore
    from .discovery import FlextMeltanoModelsDiscovery
    from .instances import FlextMeltanoModelsInstances
    from .instances_data import FlextMeltanoModelsInstancesData
    from .logging_config import FlextMeltanoModelsLogging
    from .payloads import FlextMeltanoModelsPayloads
    from .payloads_data import FlextMeltanoModelsPayloadsData
    from .projects import FlextMeltanoModelsProjects
    from .projects_plugin import FlextMeltanoModelsProjectsPlugin
    from .results import FlextMeltanoModelsResults
    from .results_dbt import FlextMeltanoModelsResultsDbt
    from .results_pipeline import FlextMeltanoModelsResultsPipeline
    from .singer import FlextMeltanoModelsSinger
    from .singer_catalog import FlextMeltanoModelsSingerCatalog
    from .singer_sdk import FlextMeltanoModelsSingerSdk
    from .sources import FlextMeltanoModelsSources
    from .sources_params import FlextMeltanoModelsSourcesParams
    from .transformations import FlextMeltanoModelsTransformations
__all__: tuple[str, ...] = (
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

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
