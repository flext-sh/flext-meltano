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
    import flext_meltano._models as _flext_meltano__models
    from flext_meltano._constants import (
        FlextMeltanoConstantsBase,
        FlextMeltanoConstantsConfig,
        FlextMeltanoConstantsEnums,
        config,
        enums,
    )

    _models = _flext_meltano__models
    import flext_meltano._protocols as _flext_meltano__protocols
    from flext_meltano._models import (
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

    _protocols = _flext_meltano__protocols
    import flext_meltano._typings as _flext_meltano__typings
    from flext_meltano._protocols import (
        FlextMeltanoProtocolsBase,
        FlextMeltanoProtocolsPlugin,
        FlextMeltanoProtocolsProject,
        FlextMeltanoProtocolsServices,
        FlextMeltanoProtocolsSinger,
        plugin,
        project,
        services,
    )

    _typings = _flext_meltano__typings
    import flext_meltano._utilities as _flext_meltano__utilities
    from flext_meltano._typings import (
        FlextMeltanoTypingsBase,
        FlextMeltanoTypingsDomains,
        FlextMeltanoTypingsSinger,
        domains,
    )

    _utilities = _flext_meltano__utilities
    import flext_meltano.api as _flext_meltano_api
    from flext_meltano._utilities import (
        FlextMeltanoUtilitiesConfig,
        FlextMeltanoUtilitiesProject,
        FlextMeltanoUtilitiesRuntime,
        FlextMeltanoUtilitiesSinger,
        FlextMeltanoUtilitiesYaml,
        SingerTargetHandler,
        runtime,
        yaml,
    )

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
    import flext_meltano.services.consumer_bases as _flext_meltano_services_consumer_bases
    from flext_meltano.protocols import (
        FlextMeltanoProtocols,
        FlextMeltanoProtocols as p,
    )
    from flext_meltano.services import (
        OPERATION_ERRORS,
        FlextMeltanoAbstractions,
        FlextMeltanoAbstractionsBase,
        FlextMeltanoAdapter,
        FlextMeltanoBridge,
        FlextMeltanoCommandRouter,
        FlextMeltanoComponentService,
        FlextMeltanoDbtAdapter,
        FlextMeltanoDbtManager,
        FlextMeltanoDbtProjectMixin,
        FlextMeltanoDbtRunnerMixin,
        FlextMeltanoDbtTransformationRunner,
        FlextMeltanoExecutor,
        FlextMeltanoExecutorBase,
        FlextMeltanoFileManagers,
        FlextMeltanoLibraryRunner,
        FlextMeltanoPipelineAdapter,
        FlextMeltanoPipelineCrudOperations,
        FlextMeltanoPipelineLifecycleOperations,
        FlextMeltanoPipelineManager,
        FlextMeltanoPipelinePaths,
        FlextMeltanoPluginDiscoveryMixin,
        FlextMeltanoPluginManager,
        FlextMeltanoProjectManager,
        FlextMeltanoProjectService,
        FlextMeltanoService,
        FlextMeltanoSingerCatalogMixin,
        FlextMeltanoSingerCliTranslator,
        FlextMeltanoSingerManager,
        FlextMeltanoSingerStateMixin,
        FlextMeltanoStatusManager,
        FlextMeltanoTapAbstractions,
        FlextMeltanoTapSourceMixin,
        FlextMeltanoTargetAbstractions,
        FlextMeltanoValidators,
        abstractions,
        adapter_extensions,
        adapters,
        bridge,
        cli_managers,
        dbt_project,
        dbt_runner,
        executor,
        file_managers,
        library_runner,
        meltano_dbt_transformation,
        meltano_plugin_discovery,
        meltano_plugins,
        meltano_project_sdk,
        project_service,
        singer_state,
        singer_tap,
        singer_target,
        singer_translator,
        validators,
    )

    consumer_bases = _flext_meltano_services_consumer_bases
    import flext_meltano.settings as _flext_meltano_settings
    from flext_meltano.services.consumer_bases import (
        FlextMeltanoDbtServiceBase,
        FlextMeltanoTapServiceBase,
        FlextMeltanoTargetServiceBase,
        dbt_service_base,
        tap_service_base,
        target_service_base,
    )

    settings = _flext_meltano_settings
    import flext_meltano.typings as _flext_meltano_typings
    from flext_meltano.settings import FlextMeltanoSettings
    from flext_meltano.singer import (
        FlextMeltanoSingerContext,
        FlextMeltanoSingerRecord,
        FlextMeltanoSingerSinkBase,
        FlextMeltanoSingerStreamBase,
        FlextMeltanoSingerTapBase,
        FlextMeltanoSingerTargetBase,
        sdk,
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
