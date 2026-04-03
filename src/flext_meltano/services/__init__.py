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
    from flext_meltano.services import (
        _abstractions_base,
        _cli_small_managers,
        _executor_base,
        _pipeline_lifecycle,
        _pipeline_mgr,
        _pipeline_ops,
        abstractions,
        adapter_extensions,
        adapters,
        bridge,
        cli_managers,
        consumer_bases,
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
        services,
        singer_catalog,
        singer_state,
        singer_tap,
        singer_target,
        singer_translator,
        validators,
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
    from flext_meltano.services.consumer_bases import (
        FlextMeltanoDbtServiceBase,
        FlextMeltanoTapServiceBase,
        FlextMeltanoTargetServiceBase,
        dbt_service_base,
        tap_service_base,
        target_service_base,
    )
    from flext_meltano.services.dbt_project import FlextMeltanoDbtProjectMixin
    from flext_meltano.services.dbt_runner import FlextMeltanoDbtRunnerMixin
    from flext_meltano.services.executor import FlextMeltanoExecutor
    from flext_meltano.services.file_managers import FlextMeltanoFileManagers
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
    from flext_meltano.services.singer_state import FlextMeltanoSingerStateMixin
    from flext_meltano.services.singer_tap import (
        FlextMeltanoTapAbstractions,
        FlextMeltanoTapSourceMixin,
    )
    from flext_meltano.services.singer_target import FlextMeltanoTargetAbstractions
    from flext_meltano.services.singer_translator import FlextMeltanoSingerCliTranslator
    from flext_meltano.services.validators import FlextMeltanoValidators

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    ("flext_meltano.services.consumer_bases",),
    {
        "FlextMeltanoAbstractions": "flext_meltano.services.abstractions",
        "FlextMeltanoAbstractionsBase": "flext_meltano.services._abstractions_base",
        "FlextMeltanoAdapter": "flext_meltano.services.adapters",
        "FlextMeltanoBridge": "flext_meltano.services.bridge",
        "FlextMeltanoCommandRouter": "flext_meltano.services.cli_managers",
        "FlextMeltanoComponentService": "flext_meltano.services.meltano_plugins",
        "FlextMeltanoDbtAdapter": "flext_meltano.services.adapter_extensions",
        "FlextMeltanoDbtManager": "flext_meltano.services._cli_small_managers",
        "FlextMeltanoDbtProjectMixin": "flext_meltano.services.dbt_project",
        "FlextMeltanoDbtRunnerMixin": "flext_meltano.services.dbt_runner",
        "FlextMeltanoDbtTransformationRunner": "flext_meltano.services.meltano_dbt_transformation",
        "FlextMeltanoExecutor": "flext_meltano.services.executor",
        "FlextMeltanoExecutorBase": "flext_meltano.services._executor_base",
        "FlextMeltanoFileManagers": "flext_meltano.services.file_managers",
        "FlextMeltanoLibraryRunner": "flext_meltano.services.library_runner",
        "FlextMeltanoPipelineAdapter": "flext_meltano.services.adapter_extensions",
        "FlextMeltanoPipelineCrudOperations": "flext_meltano.services._pipeline_ops",
        "FlextMeltanoPipelineLifecycleOperations": "flext_meltano.services._pipeline_lifecycle",
        "FlextMeltanoPipelineManager": "flext_meltano.services._pipeline_mgr",
        "FlextMeltanoPipelinePaths": "flext_meltano.services._pipeline_ops",
        "FlextMeltanoPluginDiscoveryMixin": "flext_meltano.services.meltano_plugin_discovery",
        "FlextMeltanoPluginManager": "flext_meltano.services._cli_small_managers",
        "FlextMeltanoProjectManager": "flext_meltano.services.meltano_project_sdk",
        "FlextMeltanoProjectService": "flext_meltano.services.project_service",
        "FlextMeltanoService": "flext_meltano.services.services",
        "FlextMeltanoSingerCatalogMixin": "flext_meltano.services.singer_catalog",
        "FlextMeltanoSingerCliTranslator": "flext_meltano.services.singer_translator",
        "FlextMeltanoSingerManager": "flext_meltano.services.cli_managers",
        "FlextMeltanoSingerStateMixin": "flext_meltano.services.singer_state",
        "FlextMeltanoStatusManager": "flext_meltano.services._cli_small_managers",
        "FlextMeltanoTapAbstractions": "flext_meltano.services.singer_tap",
        "FlextMeltanoTapSourceMixin": "flext_meltano.services.singer_tap",
        "FlextMeltanoTargetAbstractions": "flext_meltano.services.singer_target",
        "FlextMeltanoValidators": "flext_meltano.services.validators",
        "OPERATION_ERRORS": "flext_meltano.services._abstractions_base",
        "_abstractions_base": "flext_meltano.services._abstractions_base",
        "_cli_small_managers": "flext_meltano.services._cli_small_managers",
        "_executor_base": "flext_meltano.services._executor_base",
        "_pipeline_lifecycle": "flext_meltano.services._pipeline_lifecycle",
        "_pipeline_mgr": "flext_meltano.services._pipeline_mgr",
        "_pipeline_ops": "flext_meltano.services._pipeline_ops",
        "abstractions": "flext_meltano.services.abstractions",
        "adapter_extensions": "flext_meltano.services.adapter_extensions",
        "adapters": "flext_meltano.services.adapters",
        "bridge": "flext_meltano.services.bridge",
        "c": ("flext_core.constants", "FlextConstants"),
        "cli_managers": "flext_meltano.services.cli_managers",
        "consumer_bases": "flext_meltano.services.consumer_bases",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "dbt_project": "flext_meltano.services.dbt_project",
        "dbt_runner": "flext_meltano.services.dbt_runner",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "executor": "flext_meltano.services.executor",
        "file_managers": "flext_meltano.services.file_managers",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "library_runner": "flext_meltano.services.library_runner",
        "m": ("flext_core.models", "FlextModels"),
        "meltano_dbt_transformation": "flext_meltano.services.meltano_dbt_transformation",
        "meltano_plugin_discovery": "flext_meltano.services.meltano_plugin_discovery",
        "meltano_plugins": "flext_meltano.services.meltano_plugins",
        "meltano_project_sdk": "flext_meltano.services.meltano_project_sdk",
        "p": ("flext_core.protocols", "FlextProtocols"),
        "project_service": "flext_meltano.services.project_service",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "services": "flext_meltano.services.services",
        "singer_catalog": "flext_meltano.services.singer_catalog",
        "singer_state": "flext_meltano.services.singer_state",
        "singer_tap": "flext_meltano.services.singer_tap",
        "singer_target": "flext_meltano.services.singer_target",
        "singer_translator": "flext_meltano.services.singer_translator",
        "t": ("flext_core.typings", "FlextTypes"),
        "u": ("flext_core.utilities", "FlextUtilities"),
        "validators": "flext_meltano.services.validators",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
