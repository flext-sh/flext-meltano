# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
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
    from flext_cli import d as d, e as e, h as h, r as r, s as s, x as x
    from flext_meltano._constants.base import (
        FlextMeltanoConstantsBase as FlextMeltanoConstantsBase,
    )
    from flext_meltano._constants.enums import (
        FlextMeltanoConstantsEnums as FlextMeltanoConstantsEnums,
    )
    from flext_meltano._constants.settings import (
        FlextMeltanoConstantsSettings as FlextMeltanoConstantsSettings,
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
    from flext_meltano._models.payloads_data import (
        FlextMeltanoModelsPayloadsData as FlextMeltanoModelsPayloadsData,
    )
    from flext_meltano._models.projects import (
        FlextMeltanoModelsProjects as FlextMeltanoModelsProjects,
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
    from flext_meltano._protocols.cli import (
        FlextMeltanoProtocolsBase as FlextMeltanoProtocolsBase,
    )
    from flext_meltano._protocols.plugin import (
        FlextMeltanoProtocolsPlugin as FlextMeltanoProtocolsPlugin,
    )
    from flext_meltano._protocols.project import (
        FlextMeltanoProtocolsProject as FlextMeltanoProtocolsProject,
    )
    from flext_meltano._protocols.services import (
        FlextMeltanoProtocolsServices as FlextMeltanoProtocolsServices,
    )
    from flext_meltano._protocols.singer import (
        FlextMeltanoProtocolsSinger as FlextMeltanoProtocolsSinger,
    )
    from flext_meltano._typings.base import (
        FlextMeltanoTypingsBase as FlextMeltanoTypingsBase,
    )
    from flext_meltano._typings.domains import (
        FlextMeltanoTypingsDomains as FlextMeltanoTypingsDomains,
    )
    from flext_meltano._typings.singer import (
        FlextMeltanoTypingsSinger as FlextMeltanoTypingsSinger,
    )
    from flext_meltano._utilities.runtime import (
        FlextMeltanoUtilitiesRuntime as FlextMeltanoUtilitiesRuntime,
    )
    from flext_meltano._utilities.singer import (
        FlextMeltanoUtilitiesSinger as FlextMeltanoUtilitiesSinger,
    )
    from flext_meltano.api import FlextMeltano as FlextMeltano, meltano as meltano
    from flext_meltano.base import FlextMeltanoServiceBase as FlextMeltanoServiceBase
    from flext_meltano.cli import (
        FlextMeltanoCLI as FlextMeltanoCLI,
        cli as cli,
        main as main,
    )
    from flext_meltano.constants import (
        FlextMeltanoConstants as FlextMeltanoConstants,
        c as c,
    )
    from flext_meltano.models import FlextMeltanoModels as FlextMeltanoModels, m as m
    from flext_meltano.pipeline_mgr import (
        FlextMeltanoPipelineManager as FlextMeltanoPipelineManager,
    )
    from flext_meltano.protocols import (
        FlextMeltanoProtocols as FlextMeltanoProtocols,
        p as p,
    )
    from flext_meltano.services.abstractions import (
        FlextMeltanoAbstractions as FlextMeltanoAbstractions,
    )
    from flext_meltano.services.abstractions_base import (
        FlextMeltanoAbstractionsBase as FlextMeltanoAbstractionsBase,
    )
    from flext_meltano.services.adapters import (
        FlextMeltanoAdapter as FlextMeltanoAdapter,
    )
    from flext_meltano.services.bridge import FlextMeltanoBridge as FlextMeltanoBridge
    from flext_meltano.services.consumer_bases.dbt_service_base import (
        FlextMeltanoDbtServiceBase as FlextMeltanoDbtServiceBase,
    )
    from flext_meltano.services.consumer_bases.tap_service_base import (
        FlextMeltanoTapServiceBase as FlextMeltanoTapServiceBase,
    )
    from flext_meltano.services.consumer_bases.target_service_base import (
        FlextMeltanoTargetServiceBase as FlextMeltanoTargetServiceBase,
    )
    from flext_meltano.services.dbt_project import (
        FlextMeltanoDbtProjectMixin as FlextMeltanoDbtProjectMixin,
    )
    from flext_meltano.services.dbt_runner import (
        FlextMeltanoDbtRunnerMixin as FlextMeltanoDbtRunnerMixin,
    )
    from flext_meltano.services.executor import (
        FlextMeltanoExecutor as FlextMeltanoExecutor,
    )
    from flext_meltano.services.executor_base import (
        FlextMeltanoExecutorBase as FlextMeltanoExecutorBase,
    )
    from flext_meltano.services.library_runner import (
        FlextMeltanoLibraryRunner as FlextMeltanoLibraryRunner,
    )
    from flext_meltano.services.meltano_plugin_discovery import (
        FlextMeltanoPluginDiscoveryMixin as FlextMeltanoPluginDiscoveryMixin,
    )
    from flext_meltano.services.meltano_plugins import (
        FlextMeltanoComponentService as FlextMeltanoComponentService,
    )
    from flext_meltano.services.meltano_project_sdk import (
        FlextMeltanoProjectManager as FlextMeltanoProjectManager,
    )
    from flext_meltano.services.project_service import (
        FlextMeltanoProjectService as FlextMeltanoProjectService,
    )
    from flext_meltano.services.services import (
        FlextMeltanoService as FlextMeltanoService,
    )
    from flext_meltano.services.singer_catalog import (
        FlextMeltanoSingerCatalogMixin as FlextMeltanoSingerCatalogMixin,
    )
    from flext_meltano.services.singer_sdk import (
        Context as Context,
        FlextMeltanoSingerTapAdapter as FlextMeltanoSingerTapAdapter,
        Record as Record,
        Sink as Sink,
        Stream as Stream,
        Tap as Tap,
        Target as Target,
    )
    from flext_meltano.services.singer_state import (
        FlextMeltanoSingerStateMixin as FlextMeltanoSingerStateMixin,
    )
    from flext_meltano.services.singer_tap import (
        FlextMeltanoTapAbstractions as FlextMeltanoTapAbstractions,
        FlextMeltanoTapSourceMixin as FlextMeltanoTapSourceMixin,
    )
    from flext_meltano.services.singer_target import (
        FlextMeltanoTargetAbstractions as FlextMeltanoTargetAbstractions,
    )
    from flext_meltano.services.singer_translator import (
        FlextMeltanoSingerCliTranslator as FlextMeltanoSingerCliTranslator,
    )
    from flext_meltano.services.validators import (
        FlextMeltanoValidators as FlextMeltanoValidators,
    )
    from flext_meltano.settings import FlextMeltanoSettings as FlextMeltanoSettings
    from flext_meltano.typings import FlextMeltanoTypes as FlextMeltanoTypes, t as t
    from flext_meltano.utilities import (
        FlextMeltanoUtilities as FlextMeltanoUtilities,
        u as u,
    )
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
                "cli",
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
            ".pipeline_mgr": ("FlextMeltanoPipelineManager",),
            ".protocols": (
                "FlextMeltanoProtocols",
                "p",
            ),
            ".services.abstractions": ("FlextMeltanoAbstractions",),
            ".services.abstractions_base": ("FlextMeltanoAbstractionsBase",),
            ".services.adapters": ("FlextMeltanoAdapter",),
            ".services.bridge": ("FlextMeltanoBridge",),
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
            ".services.meltano_plugin_discovery": ("FlextMeltanoPluginDiscoveryMixin",),
            ".services.meltano_plugins": ("FlextMeltanoComponentService",),
            ".services.meltano_project_sdk": ("FlextMeltanoProjectManager",),
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

__all__: list[str] = [
    "Context",
    "FlextMeltano",
    "FlextMeltanoAbstractions",
    "FlextMeltanoAbstractionsBase",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCLI",
    "FlextMeltanoComponentService",
    "FlextMeltanoConstants",
    "FlextMeltanoDbtProjectMixin",
    "FlextMeltanoDbtRunnerMixin",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoExecutor",
    "FlextMeltanoExecutorBase",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoModels",
    "FlextMeltanoPipelineManager",
    "FlextMeltanoPluginDiscoveryMixin",
    "FlextMeltanoProjectManager",
    "FlextMeltanoProjectService",
    "FlextMeltanoProtocols",
    "FlextMeltanoService",
    "FlextMeltanoServiceBase",
    "FlextMeltanoSettings",
    "FlextMeltanoSingerCatalogMixin",
    "FlextMeltanoSingerCliTranslator",
    "FlextMeltanoSingerStateMixin",
    "FlextMeltanoSingerTapAdapter",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTapSourceMixin",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTargetServiceBase",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
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
    "cli",
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
