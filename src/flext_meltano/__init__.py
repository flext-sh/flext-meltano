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
    from flext_cli.base import s

    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.result import r
    from flext_meltano._constants.base import FlextMeltanoConstantsBase
    from flext_meltano._constants.config import FlextMeltanoConstantsSettings
    from flext_meltano._constants.enums import FlextMeltanoConstantsEnums
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
    from flext_meltano.services._cli_small_managers import (
        FlextMeltanoDbtManager,
        FlextMeltanoPluginManager,
        FlextMeltanoStatusManager,
    )
    from flext_meltano.services._pipeline_mgr import FlextMeltanoPipelineManager
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
    from flext_meltano.services.library_runner import FlextMeltanoLibraryRunner
    from flext_meltano.services.meltano_dbt_transformation import (
        FlextMeltanoDbtTransformationRunner,
    )
    from flext_meltano.services.meltano_plugin_discovery import (
        FlextMeltanoPluginDiscoveryMixin,
    )
    from flext_meltano.services.meltano_plugins import FlextMeltanoComponentService
    from flext_meltano.services.meltano_project_sdk import FlextMeltanoProjectManager
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
            ".settings": ("FlextMeltanoSettings",),
            ".typings": (
                "FlextMeltanoTypes",
                "t",
            ),
            ".utilities": (
                "FlextMeltanoUtilities",
                "u",
            ),
            "flext_cli.base": ("s",),
            "flext_core.decorators": ("d",),
            "flext_core.exceptions": ("e",),
            "flext_core.handlers": ("h",),
            "flext_core.mixins": ("x",),
            "flext_core.result": ("r",),
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
