# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
from flext_meltano.__version__ import *

if _t.TYPE_CHECKING:
    from _constants.base import FlextMeltanoConstantsBase
    from _constants.config import FlextMeltanoConstantsSettings
    from _constants.enums import FlextMeltanoConstantsEnums
    from _models.cli_params import FlextMeltanoModelsCliParams
    from _models.context import FlextMeltanoModelsContext
    from _models.core import FlextMeltanoModelsCore
    from _models.discovery import FlextMeltanoModelsDiscovery
    from _models.instances import FlextMeltanoModelsInstances
    from _models.instances_data import FlextMeltanoModelsInstancesData
    from _models.logging_config import FlextMeltanoModelsLogging
    from _models.payloads import FlextMeltanoModelsPayloads
    from _models.payloads_data import FlextMeltanoModelsPayloadsData
    from _models.projects import FlextMeltanoModelsProjects
    from _models.projects_plugin import FlextMeltanoModelsProjectsPlugin
    from _models.results import FlextMeltanoModelsResults
    from _models.results_dbt import FlextMeltanoModelsResultsDbt
    from _models.results_pipeline import FlextMeltanoModelsResultsPipeline
    from _models.singer import FlextMeltanoModelsSinger
    from _models.singer_catalog import FlextMeltanoModelsSingerCatalog
    from _models.singer_sdk import FlextMeltanoModelsSingerSdk
    from _models.sources import FlextMeltanoModelsSources
    from _models.sources_params import FlextMeltanoModelsSourcesParams
    from _models.transformations import FlextMeltanoModelsTransformations
    from _protocols.cli import FlextMeltanoProtocolsBase
    from _protocols.plugin import FlextMeltanoProtocolsPlugin
    from _protocols.project import FlextMeltanoProtocolsProject
    from _protocols.services import FlextMeltanoProtocolsServices
    from _protocols.singer import FlextMeltanoProtocolsSinger
    from _typings.base import FlextMeltanoTypingsBase
    from _typings.domains import FlextMeltanoTypingsDomains
    from _typings.singer import FlextMeltanoTypingsSinger
    from _utilities.runtime import FlextMeltanoUtilitiesRuntime
    from _utilities.singer import FlextMeltanoUtilitiesSinger
    from flext_cli.base import s
    from singer_sdk.sinks.core import Sink
    from singer_sdk.streams.core import Stream
    from singer_sdk.tap_base import Tap
    from singer_sdk.target_base import Target

    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.result import r
    from flext_meltano.abstractions import FlextMeltanoAbstractions
    from flext_meltano.adapter_extensions import (
        FlextMeltanoDbtAdapter,
        FlextMeltanoPipelineAdapter,
    )
    from flext_meltano.adapters import FlextMeltanoAdapter
    from flext_meltano.api import FlextMeltano, meltano
    from flext_meltano.base import FlextMeltanoServiceBase
    from flext_meltano.bridge import FlextMeltanoBridge
    from flext_meltano.cli import FlextMeltanoCLI, main
    from flext_meltano.cli_managers import (
        FlextMeltanoCommandRouter,
        FlextMeltanoSingerManager,
    )
    from flext_meltano.constants import FlextMeltanoConstants, c
    from flext_meltano.dbt_project import FlextMeltanoDbtProjectMixin
    from flext_meltano.dbt_runner import FlextMeltanoDbtRunnerMixin
    from flext_meltano.dbt_service_base import FlextMeltanoDbtServiceBase
    from flext_meltano.executor import FlextMeltanoExecutor
    from flext_meltano.library_runner import FlextMeltanoLibraryRunner
    from flext_meltano.meltano_dbt_transformation import (
        FlextMeltanoDbtTransformationRunner,
    )
    from flext_meltano.meltano_plugin_discovery import FlextMeltanoPluginDiscoveryMixin
    from flext_meltano.meltano_plugins import FlextMeltanoComponentService
    from flext_meltano.meltano_project_sdk import FlextMeltanoProjectManager
    from flext_meltano.models import FlextMeltanoModels, m
    from flext_meltano.project_service import FlextMeltanoProjectService
    from flext_meltano.protocols import FlextMeltanoProtocols, p
    from flext_meltano.services import FlextMeltanoService
    from flext_meltano.services._cli_small_managers import (
        FlextMeltanoDbtManager,
        FlextMeltanoPluginManager,
        FlextMeltanoStatusManager,
    )
    from flext_meltano.services._pipeline_mgr import FlextMeltanoPipelineManager
    from flext_meltano.settings import FlextMeltanoSettings
    from flext_meltano.singer_catalog import FlextMeltanoSingerCatalogMixin
    from flext_meltano.singer_sdk import Context, FlextMeltanoSingerTapAdapter, Record
    from flext_meltano.singer_state import FlextMeltanoSingerStateMixin
    from flext_meltano.singer_tap import (
        FlextMeltanoTapAbstractions,
        FlextMeltanoTapSourceMixin,
    )
    from flext_meltano.singer_target import FlextMeltanoTargetAbstractions
    from flext_meltano.singer_translator import FlextMeltanoSingerCliTranslator
    from flext_meltano.tap_service_base import FlextMeltanoTapServiceBase
    from flext_meltano.target_service_base import FlextMeltanoTargetServiceBase
    from flext_meltano.typings import FlextMeltanoTypes, t
    from flext_meltano.utilities import FlextMeltanoUtilities, u
    from flext_meltano.validators import FlextMeltanoValidators
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
            ".abstractions": ("FlextMeltanoAbstractions",),
            ".adapter_extensions": (
                "FlextMeltanoDbtAdapter",
                "FlextMeltanoPipelineAdapter",
            ),
            ".adapters": ("FlextMeltanoAdapter",),
            ".api": (
                "FlextMeltano",
                "meltano",
            ),
            ".base": ("FlextMeltanoServiceBase",),
            ".bridge": ("FlextMeltanoBridge",),
            ".cli": (
                "FlextMeltanoCLI",
                "main",
            ),
            ".cli_managers": (
                "FlextMeltanoCommandRouter",
                "FlextMeltanoSingerManager",
            ),
            ".constants": (
                "FlextMeltanoConstants",
                "c",
            ),
            ".dbt_project": ("FlextMeltanoDbtProjectMixin",),
            ".dbt_runner": ("FlextMeltanoDbtRunnerMixin",),
            ".dbt_service_base": ("FlextMeltanoDbtServiceBase",),
            ".executor": ("FlextMeltanoExecutor",),
            ".library_runner": ("FlextMeltanoLibraryRunner",),
            ".meltano_dbt_transformation": ("FlextMeltanoDbtTransformationRunner",),
            ".meltano_plugin_discovery": ("FlextMeltanoPluginDiscoveryMixin",),
            ".meltano_plugins": ("FlextMeltanoComponentService",),
            ".meltano_project_sdk": ("FlextMeltanoProjectManager",),
            ".models": (
                "FlextMeltanoModels",
                "m",
            ),
            ".project_service": ("FlextMeltanoProjectService",),
            ".protocols": (
                "FlextMeltanoProtocols",
                "p",
            ),
            ".services": ("FlextMeltanoService",),
            ".settings": ("FlextMeltanoSettings",),
            ".singer_catalog": ("FlextMeltanoSingerCatalogMixin",),
            ".singer_sdk": (
                "Context",
                "FlextMeltanoSingerTapAdapter",
                "Record",
            ),
            ".singer_state": ("FlextMeltanoSingerStateMixin",),
            ".singer_tap": (
                "FlextMeltanoTapAbstractions",
                "FlextMeltanoTapSourceMixin",
            ),
            ".singer_target": ("FlextMeltanoTargetAbstractions",),
            ".singer_translator": ("FlextMeltanoSingerCliTranslator",),
            ".tap_service_base": ("FlextMeltanoTapServiceBase",),
            ".target_service_base": ("FlextMeltanoTargetServiceBase",),
            ".typings": (
                "FlextMeltanoTypes",
                "t",
            ),
            ".utilities": (
                "FlextMeltanoUtilities",
                "u",
            ),
            ".validators": ("FlextMeltanoValidators",),
            "_constants.base": ("FlextMeltanoConstantsBase",),
            "_constants.config": ("FlextMeltanoConstantsSettings",),
            "_constants.enums": ("FlextMeltanoConstantsEnums",),
            "_models.cli_params": ("FlextMeltanoModelsCliParams",),
            "_models.context": ("FlextMeltanoModelsContext",),
            "_models.core": ("FlextMeltanoModelsCore",),
            "_models.discovery": ("FlextMeltanoModelsDiscovery",),
            "_models.instances": ("FlextMeltanoModelsInstances",),
            "_models.instances_data": ("FlextMeltanoModelsInstancesData",),
            "_models.logging_config": ("FlextMeltanoModelsLogging",),
            "_models.payloads": ("FlextMeltanoModelsPayloads",),
            "_models.payloads_data": ("FlextMeltanoModelsPayloadsData",),
            "_models.projects": ("FlextMeltanoModelsProjects",),
            "_models.projects_plugin": ("FlextMeltanoModelsProjectsPlugin",),
            "_models.results": ("FlextMeltanoModelsResults",),
            "_models.results_dbt": ("FlextMeltanoModelsResultsDbt",),
            "_models.results_pipeline": ("FlextMeltanoModelsResultsPipeline",),
            "_models.singer": ("FlextMeltanoModelsSinger",),
            "_models.singer_catalog": ("FlextMeltanoModelsSingerCatalog",),
            "_models.singer_sdk": ("FlextMeltanoModelsSingerSdk",),
            "_models.sources": ("FlextMeltanoModelsSources",),
            "_models.sources_params": ("FlextMeltanoModelsSourcesParams",),
            "_models.transformations": ("FlextMeltanoModelsTransformations",),
            "_protocols.cli": ("FlextMeltanoProtocolsBase",),
            "_protocols.plugin": ("FlextMeltanoProtocolsPlugin",),
            "_protocols.project": ("FlextMeltanoProtocolsProject",),
            "_protocols.services": ("FlextMeltanoProtocolsServices",),
            "_protocols.singer": ("FlextMeltanoProtocolsSinger",),
            "_typings.base": ("FlextMeltanoTypingsBase",),
            "_typings.domains": ("FlextMeltanoTypingsDomains",),
            "_typings.singer": ("FlextMeltanoTypingsSinger",),
            "_utilities.runtime": ("FlextMeltanoUtilitiesRuntime",),
            "_utilities.singer": ("FlextMeltanoUtilitiesSinger",),
            "flext_cli.base": ("s",),
            "flext_core.decorators": ("d",),
            "flext_core.exceptions": ("e",),
            "flext_core.handlers": ("h",),
            "flext_core.mixins": ("x",),
            "flext_core.result": ("r",),
            "singer_sdk.sinks.core": ("Sink",),
            "singer_sdk.streams.core": ("Stream",),
            "singer_sdk.tap_base": ("Tap",),
            "singer_sdk.target_base": ("Target",),
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
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
    "Context",
    "FlextMeltano",
    "FlextMeltanoAbstractions",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCLI",
    "FlextMeltanoCommandRouter",
    "FlextMeltanoComponentService",
    "FlextMeltanoConstants",
    "FlextMeltanoConstantsBase",
    "FlextMeltanoConstantsEnums",
    "FlextMeltanoConstantsSettings",
    "FlextMeltanoDbtAdapter",
    "FlextMeltanoDbtManager",
    "FlextMeltanoDbtProjectMixin",
    "FlextMeltanoDbtRunnerMixin",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoDbtTransformationRunner",
    "FlextMeltanoExecutor",
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
    "FlextMeltanoPipelineManager",
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
