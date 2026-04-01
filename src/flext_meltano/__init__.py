# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext meltano package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

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

if _TYPE_CHECKING:
    from flext_cli import d, e, h, r, s, x
    from flext_core import FlextTypes

    from flext_meltano import (
        _constants,
        _models,
        _protocols,
        _typings,
        _utilities,
        api,
        base,
        cli,
        constants,
        dbt,
        models,
        protocols,
        settings,
        typings,
        utilities,
    )
    from flext_meltano._constants import (
        FlextMeltanoConstantsBase,
        FlextMeltanoConstantsConfig,
        FlextMeltanoConstantsEnums,
        config,
        enums,
    )
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
    from flext_meltano._typings import (
        FlextMeltanoTypingsBase,
        FlextMeltanoTypingsDomains,
        FlextMeltanoTypingsSinger,
        domains,
    )
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
    from flext_meltano.api import FlextMeltano, meltano
    from flext_meltano.base import FlextMeltanoServiceBase
    from flext_meltano.cli import FlextMeltanoCLI, main
    from flext_meltano.constants import (
        FlextMeltanoConstants,
        FlextMeltanoConstants as c,
    )
    from flext_meltano.dbt import (
        FlextMeltanoDbtProjectManager,
        FlextMeltanoDbtRunner,
        FlextMeltanoDbtService,
        runner,
        service,
    )
    from flext_meltano.meltano import (
        FlextMeltanoComponentService,
        FlextMeltanoDbtTransformationRunner,
        FlextMeltanoLibraryRunner,
        FlextMeltanoMeltanoService,
        FlextMeltanoOrchestrationService,
        FlextMeltanoPluginDiscoveryMixin,
        FlextMeltanoProjectManager,
        pipelines,
        plugin_discovery,
        plugins,
    )
    from flext_meltano.models import FlextMeltanoModels, FlextMeltanoModels as m
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
        FlextMeltanoDbtAdapter,
        FlextMeltanoDbtManager,
        FlextMeltanoDbtOrchestrationMixin,
        FlextMeltanoDbtProjectMixin,
        FlextMeltanoDbtRunnerMixin,
        FlextMeltanoExecutor,
        FlextMeltanoExecutorBase,
        FlextMeltanoFileManagers,
        FlextMeltanoPipelineAdapter,
        FlextMeltanoPipelineCrudOperations,
        FlextMeltanoPipelineLifecycleOperations,
        FlextMeltanoPipelineManager,
        FlextMeltanoPipelinePaths,
        FlextMeltanoPluginManager,
        FlextMeltanoProjectService,
        FlextMeltanoService,
        FlextMeltanoSingerCatalogMixin,
        FlextMeltanoSingerCliTranslator,
        FlextMeltanoSingerManager,
        FlextMeltanoSingerOrchestrationMixin,
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
        dbt_orchestration,
        dbt_project,
        dbt_runner,
        executor,
        file_managers,
        library_runner,
        project_service,
        singer_orchestration,
        singer_state,
        singer_tap,
        singer_target,
        singer_translator,
        validators,
    )
    from flext_meltano.settings import FlextMeltanoSettings
    from flext_meltano.singer import (
        FlextMeltanoCatalogManager,
        FlextMeltanoSingerContext,
        FlextMeltanoSingerRecord,
        FlextMeltanoSingerService,
        FlextMeltanoSingerSinkBase,
        FlextMeltanoSingerStreamBase,
        FlextMeltanoSingerTapBase,
        FlextMeltanoSingerTargetBase,
        FlextMeltanoStateManager,
        catalog,
        sdk,
        state,
        tap,
        tap_source,
        target,
        translator,
    )
    from flext_meltano.typings import FlextMeltanoTypes, FlextMeltanoTypes as t
    from flext_meltano.utilities import (
        FlextMeltanoUtilities,
        FlextMeltanoUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    (
        "flext_meltano._constants",
        "flext_meltano._models",
        "flext_meltano._protocols",
        "flext_meltano._typings",
        "flext_meltano._utilities",
        "flext_meltano.dbt",
        "flext_meltano.meltano",
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
        "d": "flext_cli",
        "dbt": "flext_meltano.dbt",
        "e": "flext_cli",
        "h": "flext_cli",
        "m": ("flext_meltano.models", "FlextMeltanoModels"),
        "main": "flext_meltano.cli",
        "meltano": "flext_meltano.api",
        "models": "flext_meltano.models",
        "p": ("flext_meltano.protocols", "FlextMeltanoProtocols"),
        "protocols": "flext_meltano.protocols",
        "r": "flext_cli",
        "s": "flext_cli",
        "settings": "flext_meltano.settings",
        "t": ("flext_meltano.typings", "FlextMeltanoTypes"),
        "typings": "flext_meltano.typings",
        "u": ("flext_meltano.utilities", "FlextMeltanoUtilities"),
        "utilities": "flext_meltano.utilities",
        "x": "flext_cli",
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
        "__author__",
        "__author_email__",
        "__description__",
        "__license__",
        "__title__",
        "__url__",
        "__version__",
        "__version_info__",
    ],
)
