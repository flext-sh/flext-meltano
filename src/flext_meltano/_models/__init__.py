# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Models package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_meltano import (
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
    from flext_meltano.cli_params import FlextMeltanoModelsCliParams
    from flext_meltano.context import FlextMeltanoModelsContext
    from flext_meltano.core import FlextMeltanoModelsCore
    from flext_meltano.discovery import FlextMeltanoModelsDiscovery
    from flext_meltano.instances import FlextMeltanoModelsInstances
    from flext_meltano.instances_data import FlextMeltanoModelsInstancesData
    from flext_meltano.logging_config import FlextMeltanoModelsLogging
    from flext_meltano.payloads import FlextMeltanoModelsPayloads
    from flext_meltano.payloads_data import FlextMeltanoModelsPayloadsData
    from flext_meltano.projects import FlextMeltanoModelsProjects
    from flext_meltano.projects_plugin import FlextMeltanoModelsProjectsPlugin
    from flext_meltano.results import FlextMeltanoModelsResults
    from flext_meltano.results_dbt import FlextMeltanoModelsResultsDbt
    from flext_meltano.results_pipeline import FlextMeltanoModelsResultsPipeline
    from flext_meltano.singer import FlextMeltanoModelsSinger
    from flext_meltano.singer_catalog import FlextMeltanoModelsSingerCatalog
    from flext_meltano.singer_sdk import FlextMeltanoModelsSingerSdk
    from flext_meltano.sources import FlextMeltanoModelsSources
    from flext_meltano.sources_params import FlextMeltanoModelsSourcesParams
    from flext_meltano.transformations import FlextMeltanoModelsTransformations

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextMeltanoModelsCliParams": "flext_meltano.cli_params",
    "FlextMeltanoModelsContext": "flext_meltano.context",
    "FlextMeltanoModelsCore": "flext_meltano.core",
    "FlextMeltanoModelsDiscovery": "flext_meltano.discovery",
    "FlextMeltanoModelsInstances": "flext_meltano.instances",
    "FlextMeltanoModelsInstancesData": "flext_meltano.instances_data",
    "FlextMeltanoModelsLogging": "flext_meltano.logging_config",
    "FlextMeltanoModelsPayloads": "flext_meltano.payloads",
    "FlextMeltanoModelsPayloadsData": "flext_meltano.payloads_data",
    "FlextMeltanoModelsProjects": "flext_meltano.projects",
    "FlextMeltanoModelsProjectsPlugin": "flext_meltano.projects_plugin",
    "FlextMeltanoModelsResults": "flext_meltano.results",
    "FlextMeltanoModelsResultsDbt": "flext_meltano.results_dbt",
    "FlextMeltanoModelsResultsPipeline": "flext_meltano.results_pipeline",
    "FlextMeltanoModelsSinger": "flext_meltano.singer",
    "FlextMeltanoModelsSingerCatalog": "flext_meltano.singer_catalog",
    "FlextMeltanoModelsSingerSdk": "flext_meltano.singer_sdk",
    "FlextMeltanoModelsSources": "flext_meltano.sources",
    "FlextMeltanoModelsSourcesParams": "flext_meltano.sources_params",
    "FlextMeltanoModelsTransformations": "flext_meltano.transformations",
    "cli_params": "flext_meltano.cli_params",
    "context": "flext_meltano.context",
    "core": "flext_meltano.core",
    "discovery": "flext_meltano.discovery",
    "instances": "flext_meltano.instances",
    "instances_data": "flext_meltano.instances_data",
    "logging_config": "flext_meltano.logging_config",
    "payloads": "flext_meltano.payloads",
    "payloads_data": "flext_meltano.payloads_data",
    "projects": "flext_meltano.projects",
    "projects_plugin": "flext_meltano.projects_plugin",
    "results": "flext_meltano.results",
    "results_dbt": "flext_meltano.results_dbt",
    "results_pipeline": "flext_meltano.results_pipeline",
    "singer": "flext_meltano.singer",
    "singer_catalog": "flext_meltano.singer_catalog",
    "singer_sdk": "flext_meltano.singer_sdk",
    "sources": "flext_meltano.sources",
    "sources_params": "flext_meltano.sources_params",
    "transformations": "flext_meltano.transformations",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
