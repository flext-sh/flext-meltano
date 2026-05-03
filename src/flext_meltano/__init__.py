# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_cli import d, e, h, r, s, x

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
    from flext_meltano._constants.base import FlextMeltanoConstantsBase
    from flext_meltano._constants.enums import FlextMeltanoConstantsEnums
    from flext_meltano._constants.settings import FlextMeltanoConstantsSettings
    from flext_meltano._models.cli_params import FlextMeltanoModelsCliParams
    from flext_meltano._models.context import FlextMeltanoModelsContext
    from flext_meltano._models.core import FlextMeltanoModelsCore
    from flext_meltano._models.discovery import FlextMeltanoModelsDiscovery
    from flext_meltano._models.instances import FlextMeltanoModelsInstances
    from flext_meltano._models.instances_data import FlextMeltanoModelsInstancesData
    from flext_meltano._models.logging_config import FlextMeltanoModelsLogging
    from flext_meltano._models.payloads_data import FlextMeltanoModelsPayloadsData
    from flext_meltano._models.projects import FlextMeltanoModelsProjects
    from flext_meltano._models.results import FlextMeltanoModelsResults
    from flext_meltano._models.results_dbt import FlextMeltanoModelsResultsDbt
    from flext_meltano._models.results_pipeline import FlextMeltanoModelsResultsPipeline
    from flext_meltano._models.singer import FlextMeltanoModelsSinger
    from flext_meltano._models.singer_catalog import FlextMeltanoModelsSingerCatalog
    from flext_meltano._models.singer_sdk import FlextMeltanoModelsSingerSdk
    from flext_meltano._models.sources import FlextMeltanoModelsSources
    from flext_meltano._models.sources_params import FlextMeltanoModelsSourcesParams
    from flext_meltano._models.transformations import FlextMeltanoModelsTransformations
    from flext_meltano._protocols.cli import FlextMeltanoProtocolsBase
    from flext_meltano._protocols.plugin import FlextMeltanoProtocolsPlugin
    from flext_meltano._protocols.project import FlextMeltanoProtocolsProject
    from flext_meltano._protocols.services import FlextMeltanoProtocolsServices
    from flext_meltano._protocols.singer import FlextMeltanoProtocolsSinger
    from flext_meltano._typings.base import FlextMeltanoTypingsBase
    from flext_meltano._typings.domains import FlextMeltanoTypingsDomains
    from flext_meltano._typings.singer import FlextMeltanoTypingsSinger
    from flext_meltano._utilities.runtime import FlextMeltanoUtilitiesRuntime
    from flext_meltano._utilities.singer import FlextMeltanoUtilitiesSinger
    from flext_meltano.api import FlextMeltano, meltano
    from flext_meltano.base import FlextMeltanoServiceBase
    from flext_meltano.cli import FlextMeltanoCLI, main
    from flext_meltano.constants import FlextMeltanoConstants, c
    from flext_meltano.models import FlextMeltanoModels, m
    from flext_meltano.protocols import FlextMeltanoProtocols, p
    from flext_meltano.services.abstractions import FlextMeltanoAbstractions
    from flext_meltano.services.abstractions_base import FlextMeltanoAbstractionsBase
    from flext_meltano.services.adapters import FlextMeltanoAdapter
    from flext_meltano.services.bridge import FlextMeltanoBridge
    from flext_meltano.services.cli_managers import (
        FlextMeltanoCommandRouter,
        FlextMeltanoSingerManager,
    )
    from flext_meltano.services.cli_small_managers import (
        FlextMeltanoDbtManager,
        FlextMeltanoPluginManager,
        FlextMeltanoStatusManager,
    )
    from flext_meltano.services.consumer_bases.dbt_service_base import (
        FlextMeltanoDbtServiceBase,
    )
    from flext_meltano.services.consumer_bases.tap_service_base import (
        FlextMeltanoTapServiceBase,
    )
    from flext_meltano.services.consumer_bases.target_service_base import (
        FlextMeltanoTargetServiceBase,
    )
    from flext_meltano.services.dbt_project import FlextMeltanoDbtProjectMixin
    from flext_meltano.services.dbt_runner import FlextMeltanoDbtRunnerMixin
    from flext_meltano.services.executor import FlextMeltanoExecutor
    from flext_meltano.services.executor_base import FlextMeltanoExecutorBase
    from flext_meltano.services.library_runner import FlextMeltanoLibraryRunner
    from flext_meltano.services.meltano_dbt_transformation import (
        FlextMeltanoDbtTransformationRunner,
    )
    from flext_meltano.services.meltano_plugin_discovery import (
        FlextMeltanoPluginDiscoveryMixin,
    )
    from flext_meltano.services.meltano_plugins import FlextMeltanoComponentService
    from flext_meltano.services.meltano_project_sdk import FlextMeltanoProjectManager
    from flext_meltano.services.pipeline_lifecycle import (
        FlextMeltanoPipelineLifecycleOperations,
    )
    from flext_meltano.services.pipeline_mgr import FlextMeltanoPipelineManager
    from flext_meltano.services.pipeline_ops import (
        FlextMeltanoPipelineCrudOperations,
        FlextMeltanoPipelinePaths,
    )
    from flext_meltano.services.project_service import FlextMeltanoProjectService
    from flext_meltano.services.services import FlextMeltanoService
    from flext_meltano.services.singer_catalog import FlextMeltanoSingerCatalogMixin
    from flext_meltano.services.singer_sdk import (
        Context,
        FlextMeltanoSingerTapAdapter,
        Record,
        Sink,
        Stream,
        Tap,
        Target,
    )
    from flext_meltano.services.singer_state import FlextMeltanoSingerStateMixin
    from flext_meltano.services.singer_tap import (
        FlextMeltanoTapAbstractions,
        FlextMeltanoTapSourceMixin,
    )
    from flext_meltano.services.singer_target import FlextMeltanoTargetAbstractions
    from flext_meltano.services.singer_translator import FlextMeltanoSingerCliTranslator
    from flext_meltano.services.validators import FlextMeltanoValidators
    from flext_meltano.settings import FlextMeltanoSettings
    from flext_meltano.typings import FlextMeltanoTypes, t
    from flext_meltano.utilities import FlextMeltanoUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._constants",
        "._models",
        "._protocols",
        "._typings",
        "._utilities",
        ".services",
    ),
    build_lazy_import_map(
        {
            ".__version__": (
                "__author__",
                "__author_email__",
                "__description__",
                "__license__",
                "__title__",
                "__url__",
                "__version__",
                "__version_info__",
            ),
            "._constants.base": ("FlextMeltanoConstantsBase",),
            "._constants.enums": ("FlextMeltanoConstantsEnums",),
            "._constants.settings": ("FlextMeltanoConstantsSettings",),
            "._models.cli_params": ("FlextMeltanoModelsCliParams",),
            "._models.context": ("FlextMeltanoModelsContext",),
            "._models.core": ("FlextMeltanoModelsCore",),
            "._models.discovery": ("FlextMeltanoModelsDiscovery",),
            "._models.instances": ("FlextMeltanoModelsInstances",),
            "._models.instances_data": ("FlextMeltanoModelsInstancesData",),
            "._models.logging_config": ("FlextMeltanoModelsLogging",),
            "._models.payloads_data": ("FlextMeltanoModelsPayloadsData",),
            "._models.projects": ("FlextMeltanoModelsProjects",),
            "._models.results": ("FlextMeltanoModelsResults",),
            "._models.results_dbt": ("FlextMeltanoModelsResultsDbt",),
            "._models.results_pipeline": ("FlextMeltanoModelsResultsPipeline",),
            "._models.singer": ("FlextMeltanoModelsSinger",),
            "._models.singer_catalog": ("FlextMeltanoModelsSingerCatalog",),
            "._models.singer_sdk": ("FlextMeltanoModelsSingerSdk",),
            "._models.sources": ("FlextMeltanoModelsSources",),
            "._models.sources_params": ("FlextMeltanoModelsSourcesParams",),
            "._models.transformations": ("FlextMeltanoModelsTransformations",),
            "._protocols.cli": ("FlextMeltanoProtocolsBase",),
            "._protocols.plugin": ("FlextMeltanoProtocolsPlugin",),
            "._protocols.project": ("FlextMeltanoProtocolsProject",),
            "._protocols.services": ("FlextMeltanoProtocolsServices",),
            "._protocols.singer": ("FlextMeltanoProtocolsSinger",),
            "._typings.base": ("FlextMeltanoTypingsBase",),
            "._typings.domains": ("FlextMeltanoTypingsDomains",),
            "._typings.singer": ("FlextMeltanoTypingsSinger",),
            "._utilities.runtime": ("FlextMeltanoUtilitiesRuntime",),
            "._utilities.singer": ("FlextMeltanoUtilitiesSinger",),
            ".api": (
                "FlextMeltano",
                "meltano",
            ),
            ".base": ("FlextMeltanoServiceBase",),
            ".cli": (
                "FlextMeltanoCLI",
                "main",
            ),
            ".constants": (
                "FlextMeltanoConstants",
                "c",
            ),
            ".models": (
                "FlextMeltanoModels",
                "m",
            ),
            ".protocols": (
                "FlextMeltanoProtocols",
                "p",
            ),
            ".services.abstractions": ("FlextMeltanoAbstractions",),
            ".services.abstractions_base": ("FlextMeltanoAbstractionsBase",),
            ".services.adapters": ("FlextMeltanoAdapter",),
            ".services.bridge": ("FlextMeltanoBridge",),
            ".services.cli_managers": (
                "FlextMeltanoCommandRouter",
                "FlextMeltanoSingerManager",
            ),
            ".services.cli_small_managers": (
                "FlextMeltanoDbtManager",
                "FlextMeltanoPluginManager",
                "FlextMeltanoStatusManager",
            ),
            ".services.consumer_bases.dbt_service_base": (
                "FlextMeltanoDbtServiceBase",
            ),
            ".services.consumer_bases.tap_service_base": (
                "FlextMeltanoTapServiceBase",
            ),
            ".services.consumer_bases.target_service_base": (
                "FlextMeltanoTargetServiceBase",
            ),
            ".services.dbt_project": ("FlextMeltanoDbtProjectMixin",),
            ".services.dbt_runner": ("FlextMeltanoDbtRunnerMixin",),
            ".services.executor": ("FlextMeltanoExecutor",),
            ".services.executor_base": ("FlextMeltanoExecutorBase",),
            ".services.library_runner": ("FlextMeltanoLibraryRunner",),
            ".services.meltano_dbt_transformation": (
                "FlextMeltanoDbtTransformationRunner",
            ),
            ".services.meltano_plugin_discovery": ("FlextMeltanoPluginDiscoveryMixin",),
            ".services.meltano_plugins": ("FlextMeltanoComponentService",),
            ".services.meltano_project_sdk": ("FlextMeltanoProjectManager",),
            ".services.pipeline_lifecycle": (
                "FlextMeltanoPipelineLifecycleOperations",
            ),
            ".services.pipeline_mgr": ("FlextMeltanoPipelineManager",),
            ".services.pipeline_ops": (
                "FlextMeltanoPipelineCrudOperations",
                "FlextMeltanoPipelinePaths",
            ),
            ".services.project_service": ("FlextMeltanoProjectService",),
            ".services.services": ("FlextMeltanoService",),
            ".services.singer_catalog": ("FlextMeltanoSingerCatalogMixin",),
            ".services.singer_sdk": (
                "Context",
                "FlextMeltanoSingerTapAdapter",
                "Record",
                "Sink",
                "Stream",
                "Tap",
                "Target",
            ),
            ".services.singer_state": ("FlextMeltanoSingerStateMixin",),
            ".services.singer_tap": (
                "FlextMeltanoTapAbstractions",
                "FlextMeltanoTapSourceMixin",
            ),
            ".services.singer_target": ("FlextMeltanoTargetAbstractions",),
            ".services.singer_translator": ("FlextMeltanoSingerCliTranslator",),
            ".services.validators": ("FlextMeltanoValidators",),
            ".settings": ("FlextMeltanoSettings",),
            ".typings": (
                "FlextMeltanoTypes",
                "t",
            ),
            ".utilities": (
                "FlextMeltanoUtilities",
                "u",
            ),
            "flext_cli": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "Context",
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
    "FlextMeltanoConstantsEnums",
    "FlextMeltanoConstantsSettings",
    "FlextMeltanoDbtManager",
    "FlextMeltanoDbtProjectMixin",
    "FlextMeltanoDbtRunnerMixin",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoDbtTransformationRunner",
    "FlextMeltanoExecutor",
    "FlextMeltanoExecutorBase",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoModels",
    "FlextMeltanoModelsCliParams",
    "FlextMeltanoModelsContext",
    "FlextMeltanoModelsCore",
    "FlextMeltanoModelsDiscovery",
    "FlextMeltanoModelsInstances",
    "FlextMeltanoModelsInstancesData",
    "FlextMeltanoModelsLogging",
    "FlextMeltanoModelsPayloadsData",
    "FlextMeltanoModelsProjects",
    "FlextMeltanoModelsResults",
    "FlextMeltanoModelsResultsDbt",
    "FlextMeltanoModelsResultsPipeline",
    "FlextMeltanoModelsSinger",
    "FlextMeltanoModelsSingerCatalog",
    "FlextMeltanoModelsSingerSdk",
    "FlextMeltanoModelsSources",
    "FlextMeltanoModelsSourcesParams",
    "FlextMeltanoModelsTransformations",
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
    "FlextMeltanoSingerManager",
    "FlextMeltanoSingerStateMixin",
    "FlextMeltanoSingerTapAdapter",
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
    "FlextMeltanoUtilitiesRuntime",
    "FlextMeltanoUtilitiesSinger",
    "FlextMeltanoValidators",
    "Record",
    "Sink",
    "Stream",
    "Tap",
    "Target",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "main",
    "meltano",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]
