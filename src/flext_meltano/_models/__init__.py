# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Models package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_meltano._models.cli_params as _flext_meltano__models_cli_params

    cli_params = _flext_meltano__models_cli_params
    import flext_meltano._models.context as _flext_meltano__models_context

    context = _flext_meltano__models_context
    import flext_meltano._models.core as _flext_meltano__models_core

    core = _flext_meltano__models_core
    import flext_meltano._models.discovery as _flext_meltano__models_discovery

    discovery = _flext_meltano__models_discovery
    import flext_meltano._models.instances as _flext_meltano__models_instances

    instances = _flext_meltano__models_instances
    import flext_meltano._models.instances_data as _flext_meltano__models_instances_data

    instances_data = _flext_meltano__models_instances_data
    import flext_meltano._models.logging_config as _flext_meltano__models_logging_config

    logging_config = _flext_meltano__models_logging_config
    import flext_meltano._models.payloads as _flext_meltano__models_payloads

    payloads = _flext_meltano__models_payloads
    import flext_meltano._models.payloads_data as _flext_meltano__models_payloads_data

    payloads_data = _flext_meltano__models_payloads_data
    import flext_meltano._models.projects as _flext_meltano__models_projects

    projects = _flext_meltano__models_projects
    import flext_meltano._models.projects_plugin as _flext_meltano__models_projects_plugin

    projects_plugin = _flext_meltano__models_projects_plugin
    import flext_meltano._models.results as _flext_meltano__models_results

    results = _flext_meltano__models_results
    import flext_meltano._models.results_dbt as _flext_meltano__models_results_dbt

    results_dbt = _flext_meltano__models_results_dbt
    import flext_meltano._models.results_pipeline as _flext_meltano__models_results_pipeline

    results_pipeline = _flext_meltano__models_results_pipeline
    import flext_meltano._models.singer as _flext_meltano__models_singer

    singer = _flext_meltano__models_singer
    import flext_meltano._models.singer_catalog as _flext_meltano__models_singer_catalog

    singer_catalog = _flext_meltano__models_singer_catalog
    import flext_meltano._models.singer_sdk as _flext_meltano__models_singer_sdk

    singer_sdk = _flext_meltano__models_singer_sdk
    import flext_meltano._models.sources as _flext_meltano__models_sources

    sources = _flext_meltano__models_sources
    import flext_meltano._models.sources_params as _flext_meltano__models_sources_params

    sources_params = _flext_meltano__models_sources_params
    import flext_meltano._models.transformations as _flext_meltano__models_transformations

    transformations = _flext_meltano__models_transformations

    _ = (
        FlextMeltanoModelsCliParams,
        FlextMeltanoModelsContext,
        FlextMeltanoModelsCore,
        FlextMeltanoModelsDiscovery,
        FlextMeltanoModelsInstances,
        FlextMeltanoModelsInstancesData,
        FlextMeltanoModelsLogging,
        FlextMeltanoModelsPayloads,
        FlextMeltanoModelsPayloadsData,
        FlextMeltanoModelsProjects,
        FlextMeltanoModelsProjectsPlugin,
        FlextMeltanoModelsResults,
        FlextMeltanoModelsResultsDbt,
        FlextMeltanoModelsResultsPipeline,
        FlextMeltanoModelsSinger,
        FlextMeltanoModelsSingerCatalog,
        FlextMeltanoModelsSingerSdk,
        FlextMeltanoModelsSources,
        FlextMeltanoModelsSourcesParams,
        FlextMeltanoModelsTransformations,
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
_LAZY_IMPORTS = {
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
