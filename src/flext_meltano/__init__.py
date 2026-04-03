# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext meltano package."""

from __future__ import annotations

import typing as _t

from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_core.mixins import FlextMixins as x
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s
from flext_meltano.__version__ import *
from flext_meltano.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if _t.TYPE_CHECKING:
    import flext_meltano._constants as _flext_meltano__constants

    _constants = _flext_meltano__constants
    import flext_meltano._constants.config as _flext_meltano__constants_config

    config = _flext_meltano__constants_config
    import flext_meltano._constants.enums as _flext_meltano__constants_enums

    enums = _flext_meltano__constants_enums
    import flext_meltano._models as _flext_meltano__models

    _models = _flext_meltano__models
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
    import flext_meltano._protocols as _flext_meltano__protocols

    _protocols = _flext_meltano__protocols
    import flext_meltano._protocols.plugin as _flext_meltano__protocols_plugin

    plugin = _flext_meltano__protocols_plugin
    import flext_meltano._protocols.project as _flext_meltano__protocols_project

    project = _flext_meltano__protocols_project
    import flext_meltano._protocols.services as _flext_meltano__protocols_services

    services = _flext_meltano__protocols_services
    import flext_meltano._typings as _flext_meltano__typings

    _typings = _flext_meltano__typings
    import flext_meltano._typings.domains as _flext_meltano__typings_domains

    domains = _flext_meltano__typings_domains
    import flext_meltano._utilities as _flext_meltano__utilities

    _utilities = _flext_meltano__utilities
    import flext_meltano._utilities.runtime as _flext_meltano__utilities_runtime

    runtime = _flext_meltano__utilities_runtime
    import flext_meltano._utilities.yaml as _flext_meltano__utilities_yaml

    yaml = _flext_meltano__utilities_yaml
    import flext_meltano.api as _flext_meltano_api

    api = _flext_meltano_api
    import flext_meltano.base as _flext_meltano_base

    base = _flext_meltano_base
    import flext_meltano.cli as _flext_meltano_cli

    cli = _flext_meltano_cli
    import flext_meltano.constants as _flext_meltano_constants

    constants = _flext_meltano_constants
    import flext_meltano.models as _flext_meltano_models

    models = _flext_meltano_models
    import flext_meltano.protocols as _flext_meltano_protocols

    protocols = _flext_meltano_protocols
    import flext_meltano.services.abstractions as _flext_meltano_services_abstractions

    abstractions = _flext_meltano_services_abstractions
    import flext_meltano.services.adapter_extensions as _flext_meltano_services_adapter_extensions

    adapter_extensions = _flext_meltano_services_adapter_extensions
    import flext_meltano.services.adapters as _flext_meltano_services_adapters

    adapters = _flext_meltano_services_adapters
    import flext_meltano.services.bridge as _flext_meltano_services_bridge

    bridge = _flext_meltano_services_bridge
    import flext_meltano.services.cli_managers as _flext_meltano_services_cli_managers

    cli_managers = _flext_meltano_services_cli_managers
    import flext_meltano.services.consumer_bases as _flext_meltano_services_consumer_bases

    consumer_bases = _flext_meltano_services_consumer_bases
    import flext_meltano.services.consumer_bases.dbt_service_base as _flext_meltano_services_consumer_bases_dbt_service_base

    dbt_service_base = _flext_meltano_services_consumer_bases_dbt_service_base
    import flext_meltano.services.consumer_bases.tap_service_base as _flext_meltano_services_consumer_bases_tap_service_base

    tap_service_base = _flext_meltano_services_consumer_bases_tap_service_base
    import flext_meltano.services.consumer_bases.target_service_base as _flext_meltano_services_consumer_bases_target_service_base

    target_service_base = _flext_meltano_services_consumer_bases_target_service_base
    import flext_meltano.services.dbt_project as _flext_meltano_services_dbt_project

    dbt_project = _flext_meltano_services_dbt_project
    import flext_meltano.services.dbt_runner as _flext_meltano_services_dbt_runner

    dbt_runner = _flext_meltano_services_dbt_runner
    import flext_meltano.services.executor as _flext_meltano_services_executor

    executor = _flext_meltano_services_executor
    import flext_meltano.services.file_managers as _flext_meltano_services_file_managers

    file_managers = _flext_meltano_services_file_managers
    import flext_meltano.services.library_runner as _flext_meltano_services_library_runner

    library_runner = _flext_meltano_services_library_runner
    import flext_meltano.services.meltano_dbt_transformation as _flext_meltano_services_meltano_dbt_transformation

    meltano_dbt_transformation = _flext_meltano_services_meltano_dbt_transformation
    import flext_meltano.services.meltano_plugin_discovery as _flext_meltano_services_meltano_plugin_discovery

    meltano_plugin_discovery = _flext_meltano_services_meltano_plugin_discovery
    import flext_meltano.services.meltano_plugins as _flext_meltano_services_meltano_plugins

    meltano_plugins = _flext_meltano_services_meltano_plugins
    import flext_meltano.services.meltano_project_sdk as _flext_meltano_services_meltano_project_sdk

    meltano_project_sdk = _flext_meltano_services_meltano_project_sdk
    import flext_meltano.services.project_service as _flext_meltano_services_project_service

    project_service = _flext_meltano_services_project_service
    import flext_meltano.services.singer_state as _flext_meltano_services_singer_state

    singer_state = _flext_meltano_services_singer_state
    import flext_meltano.services.singer_tap as _flext_meltano_services_singer_tap

    singer_tap = _flext_meltano_services_singer_tap
    import flext_meltano.services.singer_target as _flext_meltano_services_singer_target

    singer_target = _flext_meltano_services_singer_target
    import flext_meltano.services.singer_translator as _flext_meltano_services_singer_translator

    singer_translator = _flext_meltano_services_singer_translator
    import flext_meltano.services.validators as _flext_meltano_services_validators

    validators = _flext_meltano_services_validators
    import flext_meltano.settings as _flext_meltano_settings

    settings = _flext_meltano_settings
    import flext_meltano.singer.sdk as _flext_meltano_singer_sdk

    sdk = _flext_meltano_singer_sdk
    import flext_meltano.typings as _flext_meltano_typings

    typings = _flext_meltano_typings
    import flext_meltano.utilities as _flext_meltano_utilities

    utilities = _flext_meltano_utilities

    _ = (
        FlextMeltano,
        FlextMeltanoAbstractions,
        FlextMeltanoAbstractionsBase,
        FlextMeltanoAdapter,
        FlextMeltanoBridge,
        FlextMeltanoCLI,
        FlextMeltanoCommandRouter,
        FlextMeltanoComponentService,
        FlextMeltanoConstants,
        FlextMeltanoConstantsBase,
        FlextMeltanoConstantsConfig,
        FlextMeltanoConstantsEnums,
        FlextMeltanoDbtAdapter,
        FlextMeltanoDbtManager,
        FlextMeltanoDbtProjectMixin,
        FlextMeltanoDbtRunnerMixin,
        FlextMeltanoDbtServiceBase,
        FlextMeltanoDbtTransformationRunner,
        FlextMeltanoExecutor,
        FlextMeltanoExecutorBase,
        FlextMeltanoFileManagers,
        FlextMeltanoLibraryRunner,
        FlextMeltanoModels,
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
        FlextMeltanoPipelineAdapter,
        FlextMeltanoPipelineCrudOperations,
        FlextMeltanoPipelineLifecycleOperations,
        FlextMeltanoPipelineManager,
        FlextMeltanoPipelinePaths,
        FlextMeltanoPluginDiscoveryMixin,
        FlextMeltanoPluginManager,
        FlextMeltanoProjectManager,
        FlextMeltanoProjectService,
        FlextMeltanoProtocols,
        FlextMeltanoProtocolsBase,
        FlextMeltanoProtocolsPlugin,
        FlextMeltanoProtocolsProject,
        FlextMeltanoProtocolsServices,
        FlextMeltanoProtocolsSinger,
        FlextMeltanoService,
        FlextMeltanoServiceBase,
        FlextMeltanoSettings,
        FlextMeltanoSingerCatalogMixin,
        FlextMeltanoSingerCliTranslator,
        FlextMeltanoSingerContext,
        FlextMeltanoSingerManager,
        FlextMeltanoSingerRecord,
        FlextMeltanoSingerSinkBase,
        FlextMeltanoSingerStateMixin,
        FlextMeltanoSingerStreamBase,
        FlextMeltanoSingerTapBase,
        FlextMeltanoSingerTargetBase,
        FlextMeltanoStatusManager,
        FlextMeltanoTapAbstractions,
        FlextMeltanoTapServiceBase,
        FlextMeltanoTapSourceMixin,
        FlextMeltanoTargetAbstractions,
        FlextMeltanoTargetServiceBase,
        FlextMeltanoTypes,
        FlextMeltanoTypingsBase,
        FlextMeltanoTypingsDomains,
        FlextMeltanoTypingsSinger,
        FlextMeltanoUtilities,
        FlextMeltanoUtilitiesConfig,
        FlextMeltanoUtilitiesProject,
        FlextMeltanoUtilitiesRuntime,
        FlextMeltanoUtilitiesSinger,
        FlextMeltanoUtilitiesYaml,
        FlextMeltanoValidators,
        OPERATION_ERRORS,
        SingerTargetHandler,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
        _constants,
        _models,
        _protocols,
        _typings,
        _utilities,
        abstractions,
        adapter_extensions,
        adapters,
        api,
        base,
        bridge,
        c,
        cli,
        cli_managers,
        cli_params,
        config,
        constants,
        consumer_bases,
        context,
        core,
        d,
        dbt_project,
        dbt_runner,
        dbt_service_base,
        discovery,
        domains,
        e,
        enums,
        executor,
        file_managers,
        h,
        instances,
        instances_data,
        library_runner,
        logging_config,
        m,
        main,
        meltano,
        meltano_dbt_transformation,
        meltano_plugin_discovery,
        meltano_plugins,
        meltano_project_sdk,
        models,
        p,
        payloads,
        payloads_data,
        plugin,
        project,
        project_service,
        projects,
        projects_plugin,
        protocols,
        r,
        results,
        results_dbt,
        results_pipeline,
        runtime,
        s,
        sdk,
        services,
        settings,
        singer,
        singer_catalog,
        singer_sdk,
        singer_state,
        singer_tap,
        singer_target,
        singer_translator,
        sources,
        sources_params,
        t,
        tap_service_base,
        target_service_base,
        transformations,
        typings,
        u,
        utilities,
        validators,
        x,
        yaml,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "flext_meltano._constants",
        "flext_meltano._models",
        "flext_meltano._protocols",
        "flext_meltano._typings",
        "flext_meltano._utilities",
        "flext_meltano.services",
        "flext_meltano.singer",
    ),
    {
        "FlextMeltano": "flext_meltano.api",
        "FlextMeltanoCLI": "flext_meltano.cli",
        "FlextMeltanoConstants": "flext_meltano.constants",
        "FlextMeltanoModels": "flext_meltano.models",
        "FlextMeltanoProtocols": "flext_meltano.protocols",
        "FlextMeltanoServiceBase": "flext_meltano.base",
        "FlextMeltanoSettings": "flext_meltano.settings",
        "FlextMeltanoTypes": "flext_meltano.typings",
        "FlextMeltanoUtilities": "flext_meltano.utilities",
        "__author__": "flext_meltano.__version__",
        "__author_email__": "flext_meltano.__version__",
        "__description__": "flext_meltano.__version__",
        "__license__": "flext_meltano.__version__",
        "__title__": "flext_meltano.__version__",
        "__url__": "flext_meltano.__version__",
        "__version__": "flext_meltano.__version__",
        "__version_info__": "flext_meltano.__version__",
        "_constants": "flext_meltano._constants",
        "_models": "flext_meltano._models",
        "_protocols": "flext_meltano._protocols",
        "_typings": "flext_meltano._typings",
        "_utilities": "flext_meltano._utilities",
        "api": "flext_meltano.api",
        "base": "flext_meltano.base",
        "c": ("flext_meltano.constants", "FlextMeltanoConstants"),
        "cli": "flext_meltano.cli",
        "constants": "flext_meltano.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("flext_meltano.models", "FlextMeltanoModels"),
        "main": "flext_meltano.cli",
        "meltano": "flext_meltano.api",
        "models": "flext_meltano.models",
        "p": ("flext_meltano.protocols", "FlextMeltanoProtocols"),
        "protocols": "flext_meltano.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "settings": "flext_meltano.settings",
        "t": ("flext_meltano.typings", "FlextMeltanoTypes"),
        "typings": "flext_meltano.typings",
        "u": ("flext_meltano.utilities", "FlextMeltanoUtilities"),
        "utilities": "flext_meltano.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)

__all__ = [
    "OPERATION_ERRORS",
    "FlextMeltano",
    "FlextMeltanoAbstractions",
    "FlextMeltanoAbstractionsBase",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCLI",
    "FlextMeltanoCommandRouter",
    "FlextMeltanoComponentService",
    "FlextMeltanoConstants",
    "FlextMeltanoConstantsBase",
    "FlextMeltanoConstantsConfig",
    "FlextMeltanoConstantsEnums",
    "FlextMeltanoDbtAdapter",
    "FlextMeltanoDbtManager",
    "FlextMeltanoDbtProjectMixin",
    "FlextMeltanoDbtRunnerMixin",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoDbtTransformationRunner",
    "FlextMeltanoExecutor",
    "FlextMeltanoExecutorBase",
    "FlextMeltanoFileManagers",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoModels",
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
    "FlextMeltanoPipelineAdapter",
    "FlextMeltanoPipelineCrudOperations",
    "FlextMeltanoPipelineLifecycleOperations",
    "FlextMeltanoPipelineManager",
    "FlextMeltanoPipelinePaths",
    "FlextMeltanoPluginDiscoveryMixin",
    "FlextMeltanoPluginManager",
    "FlextMeltanoProjectManager",
    "FlextMeltanoProjectService",
    "FlextMeltanoProtocols",
    "FlextMeltanoProtocolsBase",
    "FlextMeltanoProtocolsPlugin",
    "FlextMeltanoProtocolsProject",
    "FlextMeltanoProtocolsServices",
    "FlextMeltanoProtocolsSinger",
    "FlextMeltanoService",
    "FlextMeltanoServiceBase",
    "FlextMeltanoSettings",
    "FlextMeltanoSingerCatalogMixin",
    "FlextMeltanoSingerCliTranslator",
    "FlextMeltanoSingerContext",
    "FlextMeltanoSingerManager",
    "FlextMeltanoSingerRecord",
    "FlextMeltanoSingerSinkBase",
    "FlextMeltanoSingerStateMixin",
    "FlextMeltanoSingerStreamBase",
    "FlextMeltanoSingerTapBase",
    "FlextMeltanoSingerTargetBase",
    "FlextMeltanoStatusManager",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTapSourceMixin",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTargetServiceBase",
    "FlextMeltanoTypes",
    "FlextMeltanoTypingsBase",
    "FlextMeltanoTypingsDomains",
    "FlextMeltanoTypingsSinger",
    "FlextMeltanoUtilities",
    "FlextMeltanoUtilitiesConfig",
    "FlextMeltanoUtilitiesProject",
    "FlextMeltanoUtilitiesRuntime",
    "FlextMeltanoUtilitiesSinger",
    "FlextMeltanoUtilitiesYaml",
    "FlextMeltanoValidators",
    "SingerTargetHandler",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "_constants",
    "_models",
    "_protocols",
    "_typings",
    "_utilities",
    "abstractions",
    "adapter_extensions",
    "adapters",
    "api",
    "base",
    "bridge",
    "c",
    "cli",
    "cli_managers",
    "cli_params",
    "config",
    "constants",
    "consumer_bases",
    "context",
    "core",
    "d",
    "dbt_project",
    "dbt_runner",
    "dbt_service_base",
    "discovery",
    "domains",
    "e",
    "enums",
    "executor",
    "file_managers",
    "h",
    "instances",
    "instances_data",
    "library_runner",
    "logging_config",
    "m",
    "main",
    "meltano",
    "meltano_dbt_transformation",
    "meltano_plugin_discovery",
    "meltano_plugins",
    "meltano_project_sdk",
    "models",
    "p",
    "payloads",
    "payloads_data",
    "plugin",
    "project",
    "project_service",
    "projects",
    "projects_plugin",
    "protocols",
    "r",
    "results",
    "results_dbt",
    "results_pipeline",
    "runtime",
    "s",
    "sdk",
    "services",
    "settings",
    "singer",
    "singer_catalog",
    "singer_sdk",
    "singer_state",
    "singer_tap",
    "singer_target",
    "singer_translator",
    "sources",
    "sources_params",
    "t",
    "tap_service_base",
    "target_service_base",
    "transformations",
    "typings",
    "u",
    "utilities",
    "validators",
    "x",
    "yaml",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
