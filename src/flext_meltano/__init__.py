# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext meltano package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

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

if TYPE_CHECKING:
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
    from flext_meltano._constants import config, enums
    from flext_meltano._constants.base import FlextMeltanoConstantsBase
    from flext_meltano._constants.config import FlextMeltanoConstantsConfig
    from flext_meltano._constants.enums import FlextMeltanoConstantsEnums
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
    from flext_meltano._protocols import plugin, project, services
    from flext_meltano._protocols.cli import FlextMeltanoProtocolsBase
    from flext_meltano._protocols.plugin import FlextMeltanoProtocolsPlugin
    from flext_meltano._protocols.project import FlextMeltanoProtocolsProject
    from flext_meltano._protocols.services import FlextMeltanoProtocolsServices
    from flext_meltano._protocols.singer import FlextMeltanoProtocolsSinger
    from flext_meltano._typings import domains
    from flext_meltano._typings.base import FlextMeltanoTypingsBase
    from flext_meltano._typings.domains import FlextMeltanoTypingsDomains
    from flext_meltano._typings.singer import FlextMeltanoTypingsSinger
    from flext_meltano._utilities import yaml
    from flext_meltano._utilities.config import FlextMeltanoUtilitiesConfig
    from flext_meltano._utilities.project import FlextMeltanoUtilitiesProject
    from flext_meltano._utilities.singer import (
        FlextMeltanoUtilitiesSinger,
        SingerTargetHandler,
    )
    from flext_meltano._utilities.yaml import FlextMeltanoUtilitiesYaml
    from flext_meltano.api import FlextMeltano, meltano
    from flext_meltano.base import FlextMeltanoServiceBase
    from flext_meltano.cli import FlextMeltanoCLI, main
    from flext_meltano.constants import (
        FlextMeltanoConstants,
        FlextMeltanoConstants as c,
    )
    from flext_meltano.dbt import runner, service
    from flext_meltano.dbt.project import FlextMeltanoDbtProjectManager
    from flext_meltano.dbt.runner import FlextMeltanoDbtRunner
    from flext_meltano.dbt.service import FlextMeltanoDbtService
    from flext_meltano.meltano import pipelines, plugin_discovery, plugins
    from flext_meltano.meltano.pipelines import FlextMeltanoOrchestrationService
    from flext_meltano.meltano.plugin_discovery import FlextMeltanoPluginDiscoveryMixin
    from flext_meltano.meltano.plugins import FlextMeltanoComponentService
    from flext_meltano.meltano.project import FlextMeltanoProjectManager
    from flext_meltano.meltano.runner import (
        FlextMeltanoDbtTransformationRunner,
        FlextMeltanoLibraryRunner,
    )
    from flext_meltano.meltano.service import FlextMeltanoMeltanoService
    from flext_meltano.models import FlextMeltanoModels, FlextMeltanoModels as m
    from flext_meltano.protocols import (
        FlextMeltanoProtocols,
        FlextMeltanoProtocols as p,
    )
    from flext_meltano.services import (
        abstractions,
        adapter_extensions,
        adapters,
        bridge,
        cli_managers,
        executor,
        file_managers,
        library_runner,
        project_service,
        validators,
        yaml_operations,
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
    from flext_meltano.services.abstractions import FlextMeltanoAbstractions
    from flext_meltano.services.adapter_extensions import (
        FlextMeltanoDbtAdapter,
        FlextMeltanoPipelineAdapter,
    )
    from flext_meltano.services.adapters import FlextMeltanoAdapter
    from flext_meltano.services.bridge import FlextMeltanoBridge
    from flext_meltano.services.cli_managers import (
        FlextMeltanoCommandRouter,
        FlextMeltanoSingerManager,
    )
    from flext_meltano.services.executor import FlextMeltanoExecutor
    from flext_meltano.services.file_managers import FlextMeltanoFileManagers
    from flext_meltano.services.project_service import FlextMeltanoProjectService
    from flext_meltano.services.services import FlextMeltanoService
    from flext_meltano.services.validators import FlextMeltanoValidators
    from flext_meltano.services.yaml_operations import FlextMeltanoYamlOperationsMixin
    from flext_meltano.settings import FlextMeltanoSettings
    from flext_meltano.singer import (
        catalog,
        sdk,
        state,
        tap,
        tap_source,
        target,
        translator,
    )
    from flext_meltano.singer.catalog import FlextMeltanoCatalogManager
    from flext_meltano.singer.sdk import (
        FlextMeltanoSingerContext,
        FlextMeltanoSingerRecord,
        FlextMeltanoSingerSinkBase,
        FlextMeltanoSingerStreamBase,
        FlextMeltanoSingerTapBase,
        FlextMeltanoSingerTargetBase,
    )
    from flext_meltano.singer.service import FlextMeltanoSingerService
    from flext_meltano.singer.state import FlextMeltanoStateManager
    from flext_meltano.singer.tap import FlextMeltanoTapAbstractions
    from flext_meltano.singer.tap_source import FlextMeltanoTapSourceMixin
    from flext_meltano.singer.target import FlextMeltanoTargetAbstractions
    from flext_meltano.singer.translator import FlextMeltanoSingerCliTranslator
    from flext_meltano.typings import FlextMeltanoTypes, FlextMeltanoTypes as t
    from flext_meltano.utilities import (
        FlextMeltanoUtilities,
        FlextMeltanoUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltano": ["flext_meltano.api", "FlextMeltano"],
    "FlextMeltanoAbstractions": [
        "flext_meltano.services.abstractions",
        "FlextMeltanoAbstractions",
    ],
    "FlextMeltanoAbstractionsBase": [
        "flext_meltano.services._abstractions_base",
        "FlextMeltanoAbstractionsBase",
    ],
    "FlextMeltanoAdapter": ["flext_meltano.services.adapters", "FlextMeltanoAdapter"],
    "FlextMeltanoBridge": ["flext_meltano.services.bridge", "FlextMeltanoBridge"],
    "FlextMeltanoCLI": ["flext_meltano.cli", "FlextMeltanoCLI"],
    "FlextMeltanoCatalogManager": [
        "flext_meltano.singer.catalog",
        "FlextMeltanoCatalogManager",
    ],
    "FlextMeltanoCommandRouter": [
        "flext_meltano.services.cli_managers",
        "FlextMeltanoCommandRouter",
    ],
    "FlextMeltanoComponentService": [
        "flext_meltano.meltano.plugins",
        "FlextMeltanoComponentService",
    ],
    "FlextMeltanoConstants": ["flext_meltano.constants", "FlextMeltanoConstants"],
    "FlextMeltanoConstantsBase": [
        "flext_meltano._constants.base",
        "FlextMeltanoConstantsBase",
    ],
    "FlextMeltanoConstantsConfig": [
        "flext_meltano._constants.config",
        "FlextMeltanoConstantsConfig",
    ],
    "FlextMeltanoConstantsEnums": [
        "flext_meltano._constants.enums",
        "FlextMeltanoConstantsEnums",
    ],
    "FlextMeltanoDbtAdapter": [
        "flext_meltano.services.adapter_extensions",
        "FlextMeltanoDbtAdapter",
    ],
    "FlextMeltanoDbtManager": [
        "flext_meltano.services._cli_small_managers",
        "FlextMeltanoDbtManager",
    ],
    "FlextMeltanoDbtProjectManager": [
        "flext_meltano.dbt.project",
        "FlextMeltanoDbtProjectManager",
    ],
    "FlextMeltanoDbtRunner": ["flext_meltano.dbt.runner", "FlextMeltanoDbtRunner"],
    "FlextMeltanoDbtService": ["flext_meltano.dbt.service", "FlextMeltanoDbtService"],
    "FlextMeltanoDbtTransformationRunner": [
        "flext_meltano.meltano.runner",
        "FlextMeltanoDbtTransformationRunner",
    ],
    "FlextMeltanoExecutor": ["flext_meltano.services.executor", "FlextMeltanoExecutor"],
    "FlextMeltanoExecutorBase": [
        "flext_meltano.services._executor_base",
        "FlextMeltanoExecutorBase",
    ],
    "FlextMeltanoFileManagers": [
        "flext_meltano.services.file_managers",
        "FlextMeltanoFileManagers",
    ],
    "FlextMeltanoLibraryRunner": [
        "flext_meltano.meltano.runner",
        "FlextMeltanoLibraryRunner",
    ],
    "FlextMeltanoMeltanoService": [
        "flext_meltano.meltano.service",
        "FlextMeltanoMeltanoService",
    ],
    "FlextMeltanoModels": ["flext_meltano.models", "FlextMeltanoModels"],
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
    "FlextMeltanoOrchestrationService": [
        "flext_meltano.meltano.pipelines",
        "FlextMeltanoOrchestrationService",
    ],
    "FlextMeltanoPipelineAdapter": [
        "flext_meltano.services.adapter_extensions",
        "FlextMeltanoPipelineAdapter",
    ],
    "FlextMeltanoPipelineCrudOperations": [
        "flext_meltano.services._pipeline_ops",
        "FlextMeltanoPipelineCrudOperations",
    ],
    "FlextMeltanoPipelineLifecycleOperations": [
        "flext_meltano.services._pipeline_lifecycle",
        "FlextMeltanoPipelineLifecycleOperations",
    ],
    "FlextMeltanoPipelineManager": [
        "flext_meltano.services._pipeline_mgr",
        "FlextMeltanoPipelineManager",
    ],
    "FlextMeltanoPipelinePaths": [
        "flext_meltano.services._pipeline_ops",
        "FlextMeltanoPipelinePaths",
    ],
    "FlextMeltanoPluginDiscoveryMixin": [
        "flext_meltano.meltano.plugin_discovery",
        "FlextMeltanoPluginDiscoveryMixin",
    ],
    "FlextMeltanoPluginManager": [
        "flext_meltano.services._cli_small_managers",
        "FlextMeltanoPluginManager",
    ],
    "FlextMeltanoProjectManager": [
        "flext_meltano.meltano.project",
        "FlextMeltanoProjectManager",
    ],
    "FlextMeltanoProjectService": [
        "flext_meltano.services.project_service",
        "FlextMeltanoProjectService",
    ],
    "FlextMeltanoProtocols": ["flext_meltano.protocols", "FlextMeltanoProtocols"],
    "FlextMeltanoProtocolsBase": [
        "flext_meltano._protocols.cli",
        "FlextMeltanoProtocolsBase",
    ],
    "FlextMeltanoProtocolsPlugin": [
        "flext_meltano._protocols.plugin",
        "FlextMeltanoProtocolsPlugin",
    ],
    "FlextMeltanoProtocolsProject": [
        "flext_meltano._protocols.project",
        "FlextMeltanoProtocolsProject",
    ],
    "FlextMeltanoProtocolsServices": [
        "flext_meltano._protocols.services",
        "FlextMeltanoProtocolsServices",
    ],
    "FlextMeltanoProtocolsSinger": [
        "flext_meltano._protocols.singer",
        "FlextMeltanoProtocolsSinger",
    ],
    "FlextMeltanoService": ["flext_meltano.services.services", "FlextMeltanoService"],
    "FlextMeltanoServiceBase": ["flext_meltano.base", "FlextMeltanoServiceBase"],
    "FlextMeltanoSettings": ["flext_meltano.settings", "FlextMeltanoSettings"],
    "FlextMeltanoSingerCliTranslator": [
        "flext_meltano.singer.translator",
        "FlextMeltanoSingerCliTranslator",
    ],
    "FlextMeltanoSingerContext": [
        "flext_meltano.singer.sdk",
        "FlextMeltanoSingerContext",
    ],
    "FlextMeltanoSingerManager": [
        "flext_meltano.services.cli_managers",
        "FlextMeltanoSingerManager",
    ],
    "FlextMeltanoSingerRecord": [
        "flext_meltano.singer.sdk",
        "FlextMeltanoSingerRecord",
    ],
    "FlextMeltanoSingerService": [
        "flext_meltano.singer.service",
        "FlextMeltanoSingerService",
    ],
    "FlextMeltanoSingerSinkBase": [
        "flext_meltano.singer.sdk",
        "FlextMeltanoSingerSinkBase",
    ],
    "FlextMeltanoSingerStreamBase": [
        "flext_meltano.singer.sdk",
        "FlextMeltanoSingerStreamBase",
    ],
    "FlextMeltanoSingerTapBase": [
        "flext_meltano.singer.sdk",
        "FlextMeltanoSingerTapBase",
    ],
    "FlextMeltanoSingerTargetBase": [
        "flext_meltano.singer.sdk",
        "FlextMeltanoSingerTargetBase",
    ],
    "FlextMeltanoStateManager": [
        "flext_meltano.singer.state",
        "FlextMeltanoStateManager",
    ],
    "FlextMeltanoStatusManager": [
        "flext_meltano.services._cli_small_managers",
        "FlextMeltanoStatusManager",
    ],
    "FlextMeltanoTapAbstractions": [
        "flext_meltano.singer.tap",
        "FlextMeltanoTapAbstractions",
    ],
    "FlextMeltanoTapSourceMixin": [
        "flext_meltano.singer.tap_source",
        "FlextMeltanoTapSourceMixin",
    ],
    "FlextMeltanoTargetAbstractions": [
        "flext_meltano.singer.target",
        "FlextMeltanoTargetAbstractions",
    ],
    "FlextMeltanoTypes": ["flext_meltano.typings", "FlextMeltanoTypes"],
    "FlextMeltanoTypingsBase": [
        "flext_meltano._typings.base",
        "FlextMeltanoTypingsBase",
    ],
    "FlextMeltanoTypingsDomains": [
        "flext_meltano._typings.domains",
        "FlextMeltanoTypingsDomains",
    ],
    "FlextMeltanoTypingsSinger": [
        "flext_meltano._typings.singer",
        "FlextMeltanoTypingsSinger",
    ],
    "FlextMeltanoUtilities": ["flext_meltano.utilities", "FlextMeltanoUtilities"],
    "FlextMeltanoUtilitiesConfig": [
        "flext_meltano._utilities.config",
        "FlextMeltanoUtilitiesConfig",
    ],
    "FlextMeltanoUtilitiesProject": [
        "flext_meltano._utilities.project",
        "FlextMeltanoUtilitiesProject",
    ],
    "FlextMeltanoUtilitiesSinger": [
        "flext_meltano._utilities.singer",
        "FlextMeltanoUtilitiesSinger",
    ],
    "FlextMeltanoUtilitiesYaml": [
        "flext_meltano._utilities.yaml",
        "FlextMeltanoUtilitiesYaml",
    ],
    "FlextMeltanoValidators": [
        "flext_meltano.services.validators",
        "FlextMeltanoValidators",
    ],
    "FlextMeltanoYamlOperationsMixin": [
        "flext_meltano.services.yaml_operations",
        "FlextMeltanoYamlOperationsMixin",
    ],
    "OPERATION_ERRORS": [
        "flext_meltano.services._abstractions_base",
        "OPERATION_ERRORS",
    ],
    "SingerTargetHandler": ["flext_meltano._utilities.singer", "SingerTargetHandler"],
    "_constants": ["flext_meltano._constants", ""],
    "_models": ["flext_meltano._models", ""],
    "_protocols": ["flext_meltano._protocols", ""],
    "_typings": ["flext_meltano._typings", ""],
    "_utilities": ["flext_meltano._utilities", ""],
    "abstractions": ["flext_meltano.services.abstractions", ""],
    "adapter_extensions": ["flext_meltano.services.adapter_extensions", ""],
    "adapters": ["flext_meltano.services.adapters", ""],
    "api": ["flext_meltano.api", ""],
    "base": ["flext_meltano.base", ""],
    "bridge": ["flext_meltano.services.bridge", ""],
    "c": ["flext_meltano.constants", "FlextMeltanoConstants"],
    "catalog": ["flext_meltano.singer.catalog", ""],
    "cli": ["flext_meltano.cli", ""],
    "cli_managers": ["flext_meltano.services.cli_managers", ""],
    "cli_params": ["flext_meltano._models.cli_params", ""],
    "config": ["flext_meltano._constants.config", ""],
    "constants": ["flext_meltano.constants", ""],
    "context": ["flext_meltano._models.context", ""],
    "core": ["flext_meltano._models.core", ""],
    "d": ["flext_cli", "d"],
    "dbt": ["flext_meltano.dbt", ""],
    "discovery": ["flext_meltano._models.discovery", ""],
    "domains": ["flext_meltano._typings.domains", ""],
    "e": ["flext_cli", "e"],
    "enums": ["flext_meltano._constants.enums", ""],
    "executor": ["flext_meltano.services.executor", ""],
    "file_managers": ["flext_meltano.services.file_managers", ""],
    "h": ["flext_cli", "h"],
    "instances": ["flext_meltano._models.instances", ""],
    "instances_data": ["flext_meltano._models.instances_data", ""],
    "library_runner": ["flext_meltano.services.library_runner", ""],
    "logging_config": ["flext_meltano._models.logging_config", ""],
    "m": ["flext_meltano.models", "FlextMeltanoModels"],
    "main": ["flext_meltano.cli", "main"],
    "meltano": ["flext_meltano.api", "meltano"],
    "models": ["flext_meltano.models", ""],
    "p": ["flext_meltano.protocols", "FlextMeltanoProtocols"],
    "payloads": ["flext_meltano._models.payloads", ""],
    "payloads_data": ["flext_meltano._models.payloads_data", ""],
    "pipelines": ["flext_meltano.meltano.pipelines", ""],
    "plugin": ["flext_meltano._protocols.plugin", ""],
    "plugin_discovery": ["flext_meltano.meltano.plugin_discovery", ""],
    "plugins": ["flext_meltano.meltano.plugins", ""],
    "project": ["flext_meltano._protocols.project", ""],
    "project_service": ["flext_meltano.services.project_service", ""],
    "projects": ["flext_meltano._models.projects", ""],
    "projects_plugin": ["flext_meltano._models.projects_plugin", ""],
    "protocols": ["flext_meltano.protocols", ""],
    "r": ["flext_cli", "r"],
    "results": ["flext_meltano._models.results", ""],
    "results_dbt": ["flext_meltano._models.results_dbt", ""],
    "results_pipeline": ["flext_meltano._models.results_pipeline", ""],
    "runner": ["flext_meltano.dbt.runner", ""],
    "s": ["flext_cli", "s"],
    "sdk": ["flext_meltano.singer.sdk", ""],
    "service": ["flext_meltano.dbt.service", ""],
    "services": ["flext_meltano._protocols.services", ""],
    "settings": ["flext_meltano.settings", ""],
    "singer": ["flext_meltano._models.singer", ""],
    "singer_catalog": ["flext_meltano._models.singer_catalog", ""],
    "singer_sdk": ["flext_meltano._models.singer_sdk", ""],
    "sources": ["flext_meltano._models.sources", ""],
    "sources_params": ["flext_meltano._models.sources_params", ""],
    "state": ["flext_meltano.singer.state", ""],
    "t": ["flext_meltano.typings", "FlextMeltanoTypes"],
    "tap": ["flext_meltano.singer.tap", ""],
    "tap_source": ["flext_meltano.singer.tap_source", ""],
    "target": ["flext_meltano.singer.target", ""],
    "transformations": ["flext_meltano._models.transformations", ""],
    "translator": ["flext_meltano.singer.translator", ""],
    "typings": ["flext_meltano.typings", ""],
    "u": ["flext_meltano.utilities", "FlextMeltanoUtilities"],
    "utilities": ["flext_meltano.utilities", ""],
    "validators": ["flext_meltano.services.validators", ""],
    "x": ["flext_cli", "x"],
    "yaml": ["flext_meltano._utilities.yaml", ""],
    "yaml_operations": ["flext_meltano.services.yaml_operations", ""],
}

__all__ = [
    "OPERATION_ERRORS",
    "FlextMeltano",
    "FlextMeltanoAbstractions",
    "FlextMeltanoAbstractionsBase",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCLI",
    "FlextMeltanoCatalogManager",
    "FlextMeltanoCommandRouter",
    "FlextMeltanoComponentService",
    "FlextMeltanoConstants",
    "FlextMeltanoConstantsBase",
    "FlextMeltanoConstantsConfig",
    "FlextMeltanoConstantsEnums",
    "FlextMeltanoDbtAdapter",
    "FlextMeltanoDbtManager",
    "FlextMeltanoDbtProjectManager",
    "FlextMeltanoDbtRunner",
    "FlextMeltanoDbtService",
    "FlextMeltanoDbtTransformationRunner",
    "FlextMeltanoExecutor",
    "FlextMeltanoExecutorBase",
    "FlextMeltanoFileManagers",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoMeltanoService",
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
    "FlextMeltanoOrchestrationService",
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
    "FlextMeltanoSingerCliTranslator",
    "FlextMeltanoSingerContext",
    "FlextMeltanoSingerManager",
    "FlextMeltanoSingerRecord",
    "FlextMeltanoSingerService",
    "FlextMeltanoSingerSinkBase",
    "FlextMeltanoSingerStreamBase",
    "FlextMeltanoSingerTapBase",
    "FlextMeltanoSingerTargetBase",
    "FlextMeltanoStateManager",
    "FlextMeltanoStatusManager",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTapSourceMixin",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTypes",
    "FlextMeltanoTypingsBase",
    "FlextMeltanoTypingsDomains",
    "FlextMeltanoTypingsSinger",
    "FlextMeltanoUtilities",
    "FlextMeltanoUtilitiesConfig",
    "FlextMeltanoUtilitiesProject",
    "FlextMeltanoUtilitiesSinger",
    "FlextMeltanoUtilitiesYaml",
    "FlextMeltanoValidators",
    "FlextMeltanoYamlOperationsMixin",
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
    "catalog",
    "cli",
    "cli_managers",
    "cli_params",
    "config",
    "constants",
    "context",
    "core",
    "d",
    "dbt",
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
    "models",
    "p",
    "payloads",
    "payloads_data",
    "pipelines",
    "plugin",
    "plugin_discovery",
    "plugins",
    "project",
    "project_service",
    "projects",
    "projects_plugin",
    "protocols",
    "r",
    "results",
    "results_dbt",
    "results_pipeline",
    "runner",
    "s",
    "sdk",
    "service",
    "services",
    "settings",
    "singer",
    "singer_catalog",
    "singer_sdk",
    "sources",
    "sources_params",
    "state",
    "t",
    "tap",
    "tap_source",
    "target",
    "transformations",
    "translator",
    "typings",
    "u",
    "utilities",
    "validators",
    "x",
    "yaml",
    "yaml_operations",
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
