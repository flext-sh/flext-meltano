# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Services package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from flext_meltano import (
        abstractions,
        adapter_extensions,
        adapters,
        bridge,
        cli_managers,
        consumer_bases,
        dbt_project,
        dbt_runner,
        dbt_service_base,
        executor,
        file_managers,
        library_runner,
        meltano_dbt_transformation,
        meltano_plugin_discovery,
        meltano_plugins,
        meltano_project_sdk,
        project_service,
        services,
        singer_catalog,
        singer_state,
        singer_tap,
        singer_target,
        singer_translator,
        tap_service_base,
        target_service_base,
        validators,
    )
    from flext_meltano.abstractions import FlextMeltanoAbstractions
    from flext_meltano.adapter_extensions import (
        FlextMeltanoDbtAdapter,
        FlextMeltanoPipelineAdapter,
    )
    from flext_meltano.adapters import FlextMeltanoAdapter
    from flext_meltano.bridge import FlextMeltanoBridge
    from flext_meltano.cli_managers import FlextMeltanoCommandRouter
    from flext_meltano.consumer_bases import (
        FlextMeltanoDbtServiceBase,
        FlextMeltanoTapServiceBase,
        FlextMeltanoTargetServiceBase,
    )
    from flext_meltano.dbt_project import FlextMeltanoDbtProjectMixin
    from flext_meltano.dbt_runner import FlextMeltanoDbtRunnerMixin
    from flext_meltano.executor import FlextMeltanoExecutor
    from flext_meltano.file_managers import FlextMeltanoFileManagers
    from flext_meltano.library_runner import FlextMeltanoLibraryRunner
    from flext_meltano.meltano_dbt_transformation import (
        FlextMeltanoDbtTransformationRunner,
    )
    from flext_meltano.meltano_plugin_discovery import FlextMeltanoPluginDiscoveryMixin
    from flext_meltano.meltano_plugins import FlextMeltanoComponentService
    from flext_meltano.meltano_project_sdk import FlextMeltanoProjectManager
    from flext_meltano.project_service import FlextMeltanoProjectService
    from flext_meltano.services import FlextMeltanoService
    from flext_meltano.singer_catalog import FlextMeltanoSingerCatalogMixin
    from flext_meltano.singer_state import FlextMeltanoSingerStateMixin
    from flext_meltano.singer_tap import (
        FlextMeltanoTapAbstractions,
        FlextMeltanoTapSourceMixin,
    )
    from flext_meltano.singer_target import FlextMeltanoTargetAbstractions
    from flext_meltano.singer_translator import FlextMeltanoSingerCliTranslator
    from flext_meltano.validators import FlextMeltanoValidators

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    ("flext_meltano.consumer_bases",),
    {
        "FlextMeltanoAbstractions": "flext_meltano.abstractions",
        "FlextMeltanoAdapter": "flext_meltano.adapters",
        "FlextMeltanoBridge": "flext_meltano.bridge",
        "FlextMeltanoCommandRouter": "flext_meltano.cli_managers",
        "FlextMeltanoComponentService": "flext_meltano.meltano_plugins",
        "FlextMeltanoDbtAdapter": "flext_meltano.adapter_extensions",
        "FlextMeltanoDbtProjectMixin": "flext_meltano.dbt_project",
        "FlextMeltanoDbtRunnerMixin": "flext_meltano.dbt_runner",
        "FlextMeltanoDbtTransformationRunner": "flext_meltano.meltano_dbt_transformation",
        "FlextMeltanoExecutor": "flext_meltano.executor",
        "FlextMeltanoFileManagers": "flext_meltano.file_managers",
        "FlextMeltanoLibraryRunner": "flext_meltano.library_runner",
        "FlextMeltanoPipelineAdapter": "flext_meltano.adapter_extensions",
        "FlextMeltanoPluginDiscoveryMixin": "flext_meltano.meltano_plugin_discovery",
        "FlextMeltanoProjectManager": "flext_meltano.meltano_project_sdk",
        "FlextMeltanoProjectService": "flext_meltano.project_service",
        "FlextMeltanoService": "flext_meltano.services",
        "FlextMeltanoSingerCatalogMixin": "flext_meltano.singer_catalog",
        "FlextMeltanoSingerCliTranslator": "flext_meltano.singer_translator",
        "FlextMeltanoSingerStateMixin": "flext_meltano.singer_state",
        "FlextMeltanoTapAbstractions": "flext_meltano.singer_tap",
        "FlextMeltanoTapSourceMixin": "flext_meltano.singer_tap",
        "FlextMeltanoTargetAbstractions": "flext_meltano.singer_target",
        "FlextMeltanoValidators": "flext_meltano.validators",
        "abstractions": "flext_meltano.abstractions",
        "adapter_extensions": "flext_meltano.adapter_extensions",
        "adapters": "flext_meltano.adapters",
        "bridge": "flext_meltano.bridge",
        "c": ("flext_core.constants", "FlextConstants"),
        "cli_managers": "flext_meltano.cli_managers",
        "consumer_bases": "flext_meltano.consumer_bases",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "dbt_project": "flext_meltano.dbt_project",
        "dbt_runner": "flext_meltano.dbt_runner",
        "dbt_service_base": "flext_meltano.dbt_service_base",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "executor": "flext_meltano.executor",
        "file_managers": "flext_meltano.file_managers",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "library_runner": "flext_meltano.library_runner",
        "m": ("flext_core.models", "FlextModels"),
        "meltano_dbt_transformation": "flext_meltano.meltano_dbt_transformation",
        "meltano_plugin_discovery": "flext_meltano.meltano_plugin_discovery",
        "meltano_plugins": "flext_meltano.meltano_plugins",
        "meltano_project_sdk": "flext_meltano.meltano_project_sdk",
        "p": ("flext_core.protocols", "FlextProtocols"),
        "project_service": "flext_meltano.project_service",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "services": "flext_meltano.services",
        "singer_catalog": "flext_meltano.singer_catalog",
        "singer_state": "flext_meltano.singer_state",
        "singer_tap": "flext_meltano.singer_tap",
        "singer_target": "flext_meltano.singer_target",
        "singer_translator": "flext_meltano.singer_translator",
        "t": ("flext_core.typings", "FlextTypes"),
        "tap_service_base": "flext_meltano.tap_service_base",
        "target_service_base": "flext_meltano.target_service_base",
        "u": ("flext_core.utilities", "FlextUtilities"),
        "validators": "flext_meltano.validators",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
