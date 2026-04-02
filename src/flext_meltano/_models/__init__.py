# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano models submodules."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_meltano._models import (
        cli_params,
        context,
        core,
        discovery,
        instances,
        instances_data,
        logging_config,
        payloads,
        payloads_data,
        projects,
        projects_plugin,
        results,
        results_dbt,
        results_pipeline,
        singer,
        singer_catalog,
        singer_sdk,
        sources,
        sources_params,
        transformations,
    )
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
    from flext_meltano._models.singer_sdk import FlextMeltanoModelsSingerSdk
    from flext_meltano._models.sources import FlextMeltanoModelsSources
    from flext_meltano._models.sources_params import FlextMeltanoModelsSourcesParams
    from flext_meltano._models.transformations import FlextMeltanoModelsTransformations

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextMeltanoModelsCliParams": "flext_meltano._models.cli_params",
    "FlextMeltanoModelsContext": "flext_meltano._models.context",
    "FlextMeltanoModelsCore": "flext_meltano._models.core",
    "FlextMeltanoModelsDiscovery": "flext_meltano._models.discovery",
    "FlextMeltanoModelsInstances": "flext_meltano._models.instances",
    "FlextMeltanoModelsInstancesData": "flext_meltano._models.instances_data",
    "FlextMeltanoModelsLogging": "flext_meltano._models.logging_config",
    "FlextMeltanoModelsPayloads": "flext_meltano._models.payloads",
    "FlextMeltanoModelsPayloadsData": "flext_meltano._models.payloads_data",
    "FlextMeltanoModelsProjects": "flext_meltano._models.projects",
    "FlextMeltanoModelsProjectsPlugin": "flext_meltano._models.projects_plugin",
    "FlextMeltanoModelsResults": "flext_meltano._models.results",
    "FlextMeltanoModelsResultsDbt": "flext_meltano._models.results_dbt",
    "FlextMeltanoModelsResultsPipeline": "flext_meltano._models.results_pipeline",
    "FlextMeltanoModelsSinger": "flext_meltano._models.singer",
    "FlextMeltanoModelsSingerCatalog": "flext_meltano._models.singer_catalog",
    "FlextMeltanoModelsSingerSdk": "flext_meltano._models.singer_sdk",
    "FlextMeltanoModelsSources": "flext_meltano._models.sources",
    "FlextMeltanoModelsSourcesParams": "flext_meltano._models.sources_params",
    "FlextMeltanoModelsTransformations": "flext_meltano._models.transformations",
    "cli_params": "flext_meltano._models.cli_params",
    "context": "flext_meltano._models.context",
    "core": "flext_meltano._models.core",
    "discovery": "flext_meltano._models.discovery",
    "instances": "flext_meltano._models.instances",
    "instances_data": "flext_meltano._models.instances_data",
    "logging_config": "flext_meltano._models.logging_config",
    "payloads": "flext_meltano._models.payloads",
    "payloads_data": "flext_meltano._models.payloads_data",
    "projects": "flext_meltano._models.projects",
    "projects_plugin": "flext_meltano._models.projects_plugin",
    "results": "flext_meltano._models.results",
    "results_dbt": "flext_meltano._models.results_dbt",
    "results_pipeline": "flext_meltano._models.results_pipeline",
    "singer": "flext_meltano._models.singer",
    "singer_catalog": "flext_meltano._models.singer_catalog",
    "singer_sdk": "flext_meltano._models.singer_sdk",
    "sources": "flext_meltano._models.sources",
    "sources_params": "flext_meltano._models.sources_params",
    "transformations": "flext_meltano._models.transformations",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
