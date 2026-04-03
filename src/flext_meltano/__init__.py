# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext meltano package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_meltano.__version__ import *

if _t.TYPE_CHECKING:
    import flext_meltano._constants as _flext_meltano__constants
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

    _constants = _flext_meltano__constants
    import flext_meltano._constants.config as _flext_meltano__constants_config
    from flext_meltano._constants.base import FlextMeltanoConstantsBase

    config = _flext_meltano__constants_config
    import flext_meltano._constants.enums as _flext_meltano__constants_enums
    from flext_meltano._constants.config import FlextMeltanoConstantsConfig

    enums = _flext_meltano__constants_enums
    import flext_meltano._models as _flext_meltano__models
    from flext_meltano._constants.enums import FlextMeltanoConstantsEnums

    _models = _flext_meltano__models
    import flext_meltano._models.cli_params as _flext_meltano__models_cli_params

    cli_params = _flext_meltano__models_cli_params
    import flext_meltano._models.context as _flext_meltano__models_context
    from flext_meltano._models.cli_params import FlextMeltanoModelsCliParams

    context = _flext_meltano__models_context
    import flext_meltano._models.core as _flext_meltano__models_core
    from flext_meltano._models.context import FlextMeltanoModelsContext

    core = _flext_meltano__models_core
    import flext_meltano._models.discovery as _flext_meltano__models_discovery
    from flext_meltano._models.core import FlextMeltanoModelsCore

    discovery = _flext_meltano__models_discovery
    import flext_meltano._models.instances as _flext_meltano__models_instances
    from flext_meltano._models.discovery import FlextMeltanoModelsDiscovery

    instances = _flext_meltano__models_instances
    import flext_meltano._models.instances_data as _flext_meltano__models_instances_data
    from flext_meltano._models.instances import FlextMeltanoModelsInstances

    instances_data = _flext_meltano__models_instances_data
    import flext_meltano._models.logging_config as _flext_meltano__models_logging_config
    from flext_meltano._models.instances_data import FlextMeltanoModelsInstancesData

    logging_config = _flext_meltano__models_logging_config
    import flext_meltano._models.payloads as _flext_meltano__models_payloads
    from flext_meltano._models.logging_config import FlextMeltanoModelsLogging

    payloads = _flext_meltano__models_payloads
    import flext_meltano._models.payloads_data as _flext_meltano__models_payloads_data
    from flext_meltano._models.payloads import FlextMeltanoModelsPayloads

    payloads_data = _flext_meltano__models_payloads_data
    import flext_meltano._models.projects as _flext_meltano__models_projects
    from flext_meltano._models.payloads_data import FlextMeltanoModelsPayloadsData

    projects = _flext_meltano__models_projects
    import flext_meltano._models.projects_plugin as _flext_meltano__models_projects_plugin
    from flext_meltano._models.projects import FlextMeltanoModelsProjects

    projects_plugin = _flext_meltano__models_projects_plugin
    import flext_meltano._models.results as _flext_meltano__models_results
    from flext_meltano._models.projects_plugin import FlextMeltanoModelsProjectsPlugin

    results = _flext_meltano__models_results
    import flext_meltano._models.results_dbt as _flext_meltano__models_results_dbt
    from flext_meltano._models.results import FlextMeltanoModelsResults

    results_dbt = _flext_meltano__models_results_dbt
    import flext_meltano._models.results_pipeline as _flext_meltano__models_results_pipeline
    from flext_meltano._models.results_dbt import FlextMeltanoModelsResultsDbt

    results_pipeline = _flext_meltano__models_results_pipeline
    import flext_meltano._models.singer as _flext_meltano__models_singer
    from flext_meltano._models.results_pipeline import FlextMeltanoModelsResultsPipeline

    singer = _flext_meltano__models_singer
    import flext_meltano._models.singer_catalog as _flext_meltano__models_singer_catalog
    from flext_meltano._models.singer import FlextMeltanoModelsSinger

    singer_catalog = _flext_meltano__models_singer_catalog
    import flext_meltano._models.singer_sdk as _flext_meltano__models_singer_sdk
    from flext_meltano._models.singer_catalog import FlextMeltanoModelsSingerCatalog

    singer_sdk = _flext_meltano__models_singer_sdk
    import flext_meltano._models.sources as _flext_meltano__models_sources
    from flext_meltano._models.singer_sdk import FlextMeltanoModelsSingerSdk

    sources = _flext_meltano__models_sources
    import flext_meltano._models.sources_params as _flext_meltano__models_sources_params
    from flext_meltano._models.sources import FlextMeltanoModelsSources

    sources_params = _flext_meltano__models_sources_params
    import flext_meltano._models.transformations as _flext_meltano__models_transformations
    from flext_meltano._models.sources_params import FlextMeltanoModelsSourcesParams

    transformations = _flext_meltano__models_transformations
    import flext_meltano._protocols as _flext_meltano__protocols
    from flext_meltano._models.transformations import FlextMeltanoModelsTransformations

    _protocols = _flext_meltano__protocols
    import flext_meltano._protocols.plugin as _flext_meltano__protocols_plugin
    from flext_meltano._protocols.cli import FlextMeltanoProtocolsBase

    plugin = _flext_meltano__protocols_plugin
    import flext_meltano._protocols.project as _flext_meltano__protocols_project
    from flext_meltano._protocols.plugin import FlextMeltanoProtocolsPlugin

    project = _flext_meltano__protocols_project
    import flext_meltano._protocols.services as _flext_meltano__protocols_services
    from flext_meltano._protocols.project import FlextMeltanoProtocolsProject

    services = _flext_meltano__protocols_services
    import flext_meltano._typings as _flext_meltano__typings
    from flext_meltano._protocols.services import FlextMeltanoProtocolsServices
    from flext_meltano._protocols.singer import FlextMeltanoProtocolsSinger

    _typings = _flext_meltano__typings
    import flext_meltano._typings.domains as _flext_meltano__typings_domains
    from flext_meltano._typings.base import FlextMeltanoTypingsBase

    domains = _flext_meltano__typings_domains
    import flext_meltano._utilities as _flext_meltano__utilities
    from flext_meltano._typings.domains import FlextMeltanoTypingsDomains
    from flext_meltano._typings.singer import FlextMeltanoTypingsSinger

    _utilities = _flext_meltano__utilities
    import flext_meltano._utilities.runtime as _flext_meltano__utilities_runtime
    from flext_meltano._utilities.config import FlextMeltanoUtilitiesConfig
    from flext_meltano._utilities.project import FlextMeltanoUtilitiesProject

    runtime = _flext_meltano__utilities_runtime
    import flext_meltano._utilities.yaml as _flext_meltano__utilities_yaml
    from flext_meltano._utilities.runtime import FlextMeltanoUtilitiesRuntime
    from flext_meltano._utilities.singer import (
        FlextMeltanoUtilitiesSinger,
        SingerTargetHandler,
    )

    yaml = _flext_meltano__utilities_yaml
    import flext_meltano.api as _flext_meltano_api
    from flext_meltano._utilities.yaml import FlextMeltanoUtilitiesYaml

    api = _flext_meltano_api
    import flext_meltano.base as _flext_meltano_base
    from flext_meltano.api import FlextMeltano, meltano

    base = _flext_meltano_base
    import flext_meltano.cli as _flext_meltano_cli
    from flext_meltano.base import FlextMeltanoServiceBase

    cli = _flext_meltano_cli
    import flext_meltano.constants as _flext_meltano_constants
    from flext_meltano.cli import FlextMeltanoCLI, main

    constants = _flext_meltano_constants
    import flext_meltano.models as _flext_meltano_models
    from flext_meltano.constants import (
        FlextMeltanoConstants,
        FlextMeltanoConstants as c,
    )

    models = _flext_meltano_models
    import flext_meltano.protocols as _flext_meltano_protocols
    from flext_meltano.models import FlextMeltanoModels, FlextMeltanoModels as m

    protocols = _flext_meltano_protocols
    import flext_meltano.services.abstractions as _flext_meltano_services_abstractions
    from flext_meltano.protocols import (
        FlextMeltanoProtocols,
        FlextMeltanoProtocols as p,
    )
    from flext_meltano.services._abstractions_base import (
        OPERATION_ERRORS,
        FlextMeltanoAbstractionsBase,
    )
    from flext_meltano.services._cli_small_managers import (
        FlextMeltanoDbtManager,
        FlextMeltanoPluginManager,
        FlextMeltanoStatusManager,
    )
    from flext_meltano.services._executor_base import FlextMeltanoExecutorBase
    from flext_meltano.services._pipeline_lifecycle import (
        FlextMeltanoPipelineLifecycleOperations,
    )
    from flext_meltano.services._pipeline_mgr import FlextMeltanoPipelineManager
    from flext_meltano.services._pipeline_ops import (
        FlextMeltanoPipelineCrudOperations,
        FlextMeltanoPipelinePaths,
    )

    abstractions = _flext_meltano_services_abstractions
    import flext_meltano.services.adapter_extensions as _flext_meltano_services_adapter_extensions
    from flext_meltano.services.abstractions import FlextMeltanoAbstractions

    adapter_extensions = _flext_meltano_services_adapter_extensions
    import flext_meltano.services.adapters as _flext_meltano_services_adapters
    from flext_meltano.services.adapter_extensions import (
        FlextMeltanoDbtAdapter,
        FlextMeltanoPipelineAdapter,
    )

    adapters = _flext_meltano_services_adapters
    import flext_meltano.services.bridge as _flext_meltano_services_bridge
    from flext_meltano.services.adapters import FlextMeltanoAdapter

    bridge = _flext_meltano_services_bridge
    import flext_meltano.services.cli_managers as _flext_meltano_services_cli_managers
    from flext_meltano.services.bridge import FlextMeltanoBridge

    cli_managers = _flext_meltano_services_cli_managers
    import flext_meltano.services.consumer_bases as _flext_meltano_services_consumer_bases
    from flext_meltano.services.cli_managers import (
        FlextMeltanoCommandRouter,
        FlextMeltanoSingerManager,
    )

    consumer_bases = _flext_meltano_services_consumer_bases
    import flext_meltano.services.consumer_bases.dbt_service_base as _flext_meltano_services_consumer_bases_dbt_service_base

    dbt_service_base = _flext_meltano_services_consumer_bases_dbt_service_base
    import flext_meltano.services.consumer_bases.tap_service_base as _flext_meltano_services_consumer_bases_tap_service_base
    from flext_meltano.services.consumer_bases.dbt_service_base import (
        FlextMeltanoDbtServiceBase,
    )

    tap_service_base = _flext_meltano_services_consumer_bases_tap_service_base
    import flext_meltano.services.consumer_bases.target_service_base as _flext_meltano_services_consumer_bases_target_service_base
    from flext_meltano.services.consumer_bases.tap_service_base import (
        FlextMeltanoTapServiceBase,
    )

    target_service_base = _flext_meltano_services_consumer_bases_target_service_base
    import flext_meltano.services.dbt_project as _flext_meltano_services_dbt_project
    from flext_meltano.services.consumer_bases.target_service_base import (
        FlextMeltanoTargetServiceBase,
    )

    dbt_project = _flext_meltano_services_dbt_project
    import flext_meltano.services.dbt_runner as _flext_meltano_services_dbt_runner
    from flext_meltano.services.dbt_project import FlextMeltanoDbtProjectMixin

    dbt_runner = _flext_meltano_services_dbt_runner
    import flext_meltano.services.executor as _flext_meltano_services_executor
    from flext_meltano.services.dbt_runner import FlextMeltanoDbtRunnerMixin

    executor = _flext_meltano_services_executor
    import flext_meltano.services.file_managers as _flext_meltano_services_file_managers
    from flext_meltano.services.executor import FlextMeltanoExecutor

    file_managers = _flext_meltano_services_file_managers
    import flext_meltano.services.library_runner as _flext_meltano_services_library_runner
    from flext_meltano.services.file_managers import FlextMeltanoFileManagers

    library_runner = _flext_meltano_services_library_runner
    import flext_meltano.services.meltano_dbt_transformation as _flext_meltano_services_meltano_dbt_transformation
    from flext_meltano.services.library_runner import FlextMeltanoLibraryRunner

    meltano_dbt_transformation = _flext_meltano_services_meltano_dbt_transformation
    import flext_meltano.services.meltano_plugin_discovery as _flext_meltano_services_meltano_plugin_discovery
    from flext_meltano.services.meltano_dbt_transformation import (
        FlextMeltanoDbtTransformationRunner,
    )

    meltano_plugin_discovery = _flext_meltano_services_meltano_plugin_discovery
    import flext_meltano.services.meltano_plugins as _flext_meltano_services_meltano_plugins
    from flext_meltano.services.meltano_plugin_discovery import (
        FlextMeltanoPluginDiscoveryMixin,
    )

    meltano_plugins = _flext_meltano_services_meltano_plugins
    import flext_meltano.services.meltano_project_sdk as _flext_meltano_services_meltano_project_sdk
    from flext_meltano.services.meltano_plugins import FlextMeltanoComponentService

    meltano_project_sdk = _flext_meltano_services_meltano_project_sdk
    import flext_meltano.services.project_service as _flext_meltano_services_project_service
    from flext_meltano.services.meltano_project_sdk import FlextMeltanoProjectManager

    project_service = _flext_meltano_services_project_service
    import flext_meltano.services.singer_state as _flext_meltano_services_singer_state
    from flext_meltano.services.project_service import FlextMeltanoProjectService
    from flext_meltano.services.services import FlextMeltanoService
    from flext_meltano.services.singer_catalog import FlextMeltanoSingerCatalogMixin

    singer_state = _flext_meltano_services_singer_state
    import flext_meltano.services.singer_tap as _flext_meltano_services_singer_tap
    from flext_meltano.services.singer_state import FlextMeltanoSingerStateMixin

    singer_tap = _flext_meltano_services_singer_tap
    import flext_meltano.services.singer_target as _flext_meltano_services_singer_target
    from flext_meltano.services.singer_tap import (
        FlextMeltanoTapAbstractions,
        FlextMeltanoTapSourceMixin,
    )

    singer_target = _flext_meltano_services_singer_target
    import flext_meltano.services.singer_translator as _flext_meltano_services_singer_translator
    from flext_meltano.services.singer_target import FlextMeltanoTargetAbstractions

    singer_translator = _flext_meltano_services_singer_translator
    import flext_meltano.services.validators as _flext_meltano_services_validators
    from flext_meltano.services.singer_translator import FlextMeltanoSingerCliTranslator

    validators = _flext_meltano_services_validators
    import flext_meltano.settings as _flext_meltano_settings
    from flext_meltano.services.validators import FlextMeltanoValidators

    settings = _flext_meltano_settings
    import flext_meltano.singer.sdk as _flext_meltano_singer_sdk
    from flext_meltano.settings import FlextMeltanoSettings

    sdk = _flext_meltano_singer_sdk
    import flext_meltano.typings as _flext_meltano_typings
    from flext_meltano.singer.sdk import (
        FlextMeltanoSingerContext,
        FlextMeltanoSingerRecord,
        FlextMeltanoSingerSinkBase,
        FlextMeltanoSingerStreamBase,
        FlextMeltanoSingerTapBase,
        FlextMeltanoSingerTargetBase,
    )

    typings = _flext_meltano_typings
    import flext_meltano.utilities as _flext_meltano_utilities
    from flext_meltano.typings import FlextMeltanoTypes, FlextMeltanoTypes as t

    utilities = _flext_meltano_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_meltano.utilities import (
        FlextMeltanoUtilities,
        FlextMeltanoUtilities as u,
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
