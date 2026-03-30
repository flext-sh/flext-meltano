# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano models submodules."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._models import (
        cli_params as cli_params,
        context as context,
        core as core,
        discovery as discovery,
        instances as instances,
        instances_data as instances_data,
        logging_config as logging_config,
        payloads as payloads,
        payloads_data as payloads_data,
        projects as projects,
        projects_plugin as projects_plugin,
        results as results,
        results_dbt as results_dbt,
        results_pipeline as results_pipeline,
        singer as singer,
        singer_catalog as singer_catalog,
        singer_sdk as singer_sdk,
        sources as sources,
        sources_params as sources_params,
        transformations as transformations,
    )
    from flext_meltano._models.cli_params import (
        FlextMeltanoModelsCliParams as FlextMeltanoModelsCliParams,
    )
    from flext_meltano._models.context import (
        FlextMeltanoModelsContext as FlextMeltanoModelsContext,
    )
    from flext_meltano._models.core import (
        FlextMeltanoModelsCore as FlextMeltanoModelsCore,
    )
    from flext_meltano._models.discovery import (
        FlextMeltanoModelsDiscovery as FlextMeltanoModelsDiscovery,
    )
    from flext_meltano._models.instances import (
        FlextMeltanoModelsInstances as FlextMeltanoModelsInstances,
    )
    from flext_meltano._models.instances_data import (
        FlextMeltanoModelsInstancesData as FlextMeltanoModelsInstancesData,
    )
    from flext_meltano._models.logging_config import (
        FlextMeltanoModelsLogging as FlextMeltanoModelsLogging,
    )
    from flext_meltano._models.payloads import (
        FlextMeltanoModelsPayloads as FlextMeltanoModelsPayloads,
    )
    from flext_meltano._models.payloads_data import (
        FlextMeltanoModelsPayloadsData as FlextMeltanoModelsPayloadsData,
    )
    from flext_meltano._models.projects import (
        FlextMeltanoModelsProjects as FlextMeltanoModelsProjects,
    )
    from flext_meltano._models.projects_plugin import (
        FlextMeltanoModelsProjectsPlugin as FlextMeltanoModelsProjectsPlugin,
    )
    from flext_meltano._models.results import (
        FlextMeltanoModelsResults as FlextMeltanoModelsResults,
    )
    from flext_meltano._models.results_dbt import (
        FlextMeltanoModelsResultsDbt as FlextMeltanoModelsResultsDbt,
    )
    from flext_meltano._models.results_pipeline import (
        FlextMeltanoModelsResultsPipeline as FlextMeltanoModelsResultsPipeline,
    )
    from flext_meltano._models.singer import (
        FlextMeltanoModelsSinger as FlextMeltanoModelsSinger,
    )
    from flext_meltano._models.singer_catalog import (
        FlextMeltanoModelsSingerCatalog as FlextMeltanoModelsSingerCatalog,
    )
    from flext_meltano._models.singer_sdk import (
        FlextMeltanoModelsSingerSdk as FlextMeltanoModelsSingerSdk,
    )
    from flext_meltano._models.sources import (
        FlextMeltanoModelsSources as FlextMeltanoModelsSources,
    )
    from flext_meltano._models.sources_params import (
        FlextMeltanoModelsSourcesParams as FlextMeltanoModelsSourcesParams,
    )
    from flext_meltano._models.transformations import (
        FlextMeltanoModelsTransformations as FlextMeltanoModelsTransformations,
    )

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
    "FlextMeltanoModelsSingerSdk": [
        "flext_meltano._models.singer_sdk",
        "FlextMeltanoModelsSingerSdk",
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
    "cli_params": ["flext_meltano._models.cli_params", ""],
    "context": ["flext_meltano._models.context", ""],
    "core": ["flext_meltano._models.core", ""],
    "discovery": ["flext_meltano._models.discovery", ""],
    "instances": ["flext_meltano._models.instances", ""],
    "instances_data": ["flext_meltano._models.instances_data", ""],
    "logging_config": ["flext_meltano._models.logging_config", ""],
    "payloads": ["flext_meltano._models.payloads", ""],
    "payloads_data": ["flext_meltano._models.payloads_data", ""],
    "projects": ["flext_meltano._models.projects", ""],
    "projects_plugin": ["flext_meltano._models.projects_plugin", ""],
    "results": ["flext_meltano._models.results", ""],
    "results_dbt": ["flext_meltano._models.results_dbt", ""],
    "results_pipeline": ["flext_meltano._models.results_pipeline", ""],
    "singer": ["flext_meltano._models.singer", ""],
    "singer_catalog": ["flext_meltano._models.singer_catalog", ""],
    "singer_sdk": ["flext_meltano._models.singer_sdk", ""],
    "sources": ["flext_meltano._models.sources", ""],
    "sources_params": ["flext_meltano._models.sources_params", ""],
    "transformations": ["flext_meltano._models.transformations", ""],
}

_EXPORTS: Sequence[str] = [
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
    "cli_params",
    "context",
    "core",
    "discovery",
    "instances",
    "instances_data",
    "logging_config",
    "payloads",
    "payloads_data",
    "projects",
    "projects_plugin",
    "results",
    "results_dbt",
    "results_pipeline",
    "singer",
    "singer_catalog",
    "singer_sdk",
    "sources",
    "sources_params",
    "transformations",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
