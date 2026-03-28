# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano models submodules."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_meltano._models.cli_params import FlextMeltanoModelsCliParams
    from flext_meltano._models.context import FlextMeltanoModelsContext
    from flext_meltano._models.core import FlextMeltanoModelsCore
    from flext_meltano._models.discovery import FlextMeltanoModelsDiscovery
    from flext_meltano._models.instances import FlextMeltanoModelsInstances
    from flext_meltano._models.instances_data import FlextMeltanoModelsInstancesData
    from flext_meltano._models.logging_config import FlextMeltanoModelsLogging
    from flext_meltano._models.payloads import FlextMeltanoModelsPayloads
    from flext_meltano._models.payloads_data import FlextMeltanoModelsPayloadsData
    from flext_meltano._models.projects import FlextMeltanoModelsProjects
    from flext_meltano._models.projects_plugin import FlextMeltanoModelsProjectsPlugin
    from flext_meltano._models.results import FlextMeltanoModelsResults
    from flext_meltano._models.results_dbt import FlextMeltanoModelsResultsDbt
    from flext_meltano._models.results_pipeline import FlextMeltanoModelsResultsPipeline
    from flext_meltano._models.singer import FlextMeltanoModelsSinger
    from flext_meltano._models.singer_catalog import FlextMeltanoModelsSingerCatalog
    from flext_meltano._models.sources import FlextMeltanoModelsSources
    from flext_meltano._models.sources_params import FlextMeltanoModelsSourcesParams
    from flext_meltano._models.transformations import FlextMeltanoModelsTransformations

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltanoModelsCliParams": [
        "flext_meltano._models.cli_params",
        "FlextMeltanoModelsCliParams",
    ],
    "FlextMeltanoModelsContext": [
        "flext_meltano._models.context",
        "FlextMeltanoModelsContext",
    ],
    "FlextMeltanoModelsCore": ["flext_meltano._models.core", "FlextMeltanoModelsCore"],
    "FlextMeltanoModelsDiscovery": [
        "flext_meltano._models.discovery",
        "FlextMeltanoModelsDiscovery",
    ],
    "FlextMeltanoModelsInstances": [
        "flext_meltano._models.instances",
        "FlextMeltanoModelsInstances",
    ],
    "FlextMeltanoModelsInstancesData": [
        "flext_meltano._models.instances_data",
        "FlextMeltanoModelsInstancesData",
    ],
    "FlextMeltanoModelsLogging": [
        "flext_meltano._models.logging_config",
        "FlextMeltanoModelsLogging",
    ],
    "FlextMeltanoModelsPayloads": [
        "flext_meltano._models.payloads",
        "FlextMeltanoModelsPayloads",
    ],
    "FlextMeltanoModelsPayloadsData": [
        "flext_meltano._models.payloads_data",
        "FlextMeltanoModelsPayloadsData",
    ],
    "FlextMeltanoModelsProjects": [
        "flext_meltano._models.projects",
        "FlextMeltanoModelsProjects",
    ],
    "FlextMeltanoModelsProjectsPlugin": [
        "flext_meltano._models.projects_plugin",
        "FlextMeltanoModelsProjectsPlugin",
    ],
    "FlextMeltanoModelsResults": [
        "flext_meltano._models.results",
        "FlextMeltanoModelsResults",
    ],
    "FlextMeltanoModelsResultsDbt": [
        "flext_meltano._models.results_dbt",
        "FlextMeltanoModelsResultsDbt",
    ],
    "FlextMeltanoModelsResultsPipeline": [
        "flext_meltano._models.results_pipeline",
        "FlextMeltanoModelsResultsPipeline",
    ],
    "FlextMeltanoModelsSinger": [
        "flext_meltano._models.singer",
        "FlextMeltanoModelsSinger",
    ],
    "FlextMeltanoModelsSingerCatalog": [
        "flext_meltano._models.singer_catalog",
        "FlextMeltanoModelsSingerCatalog",
    ],
    "FlextMeltanoModelsSources": [
        "flext_meltano._models.sources",
        "FlextMeltanoModelsSources",
    ],
    "FlextMeltanoModelsSourcesParams": [
        "flext_meltano._models.sources_params",
        "FlextMeltanoModelsSourcesParams",
    ],
    "FlextMeltanoModelsTransformations": [
        "flext_meltano._models.transformations",
        "FlextMeltanoModelsTransformations",
    ],
}

__all__ = [
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
    "FlextMeltanoModelsSources",
    "FlextMeltanoModelsSourcesParams",
    "FlextMeltanoModelsTransformations",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
