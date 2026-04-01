# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano Services - Service mixins for the Meltano facade.

This package contains service mixin classes that compose via MRO
to form the FlextMeltano public facade in api.py.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

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
        dbt_orchestration,
        dbt_project,
        dbt_runner,
        executor,
        file_managers,
        library_runner,
        project_service,
        services,
        singer_catalog,
        singer_orchestration,
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
    from flext_meltano.services.dbt_orchestration import (
        FlextMeltanoDbtOrchestrationMixin,
    )
    from flext_meltano.services.dbt_project import FlextMeltanoDbtProjectMixin
    from flext_meltano.services.dbt_runner import FlextMeltanoDbtRunnerMixin
    from flext_meltano.services.executor import FlextMeltanoExecutor
    from flext_meltano.services.file_managers import FlextMeltanoFileManagers
    from flext_meltano.services.library_runner import FlextMeltanoLibraryRunner
    from flext_meltano.services.project_service import FlextMeltanoProjectService
    from flext_meltano.services.services import FlextMeltanoService
    from flext_meltano.services.singer_catalog import FlextMeltanoSingerCatalogMixin
    from flext_meltano.services.singer_orchestration import (
        FlextMeltanoSingerOrchestrationMixin,
    )
    from flext_meltano.services.singer_state import FlextMeltanoSingerStateMixin
    from flext_meltano.services.singer_tap import (
        FlextMeltanoTapAbstractions,
        FlextMeltanoTapSourceMixin,
    )
    from flext_meltano.services.singer_target import FlextMeltanoTargetAbstractions
    from flext_meltano.services.singer_translator import FlextMeltanoSingerCliTranslator
    from flext_meltano.services.validators import FlextMeltanoValidators

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextMeltanoAbstractions": "flext_meltano.services.abstractions",
    "FlextMeltanoAbstractionsBase": "flext_meltano.services._abstractions_base",
    "FlextMeltanoAdapter": "flext_meltano.services.adapters",
    "FlextMeltanoBridge": "flext_meltano.services.bridge",
    "FlextMeltanoCommandRouter": "flext_meltano.services.cli_managers",
    "FlextMeltanoDbtAdapter": "flext_meltano.services.adapter_extensions",
    "FlextMeltanoDbtManager": "flext_meltano.services._cli_small_managers",
    "FlextMeltanoDbtOrchestrationMixin": "flext_meltano.services.dbt_orchestration",
    "FlextMeltanoDbtProjectMixin": "flext_meltano.services.dbt_project",
    "FlextMeltanoDbtRunnerMixin": "flext_meltano.services.dbt_runner",
    "FlextMeltanoExecutor": "flext_meltano.services.executor",
    "FlextMeltanoExecutorBase": "flext_meltano.services._executor_base",
    "FlextMeltanoFileManagers": "flext_meltano.services.file_managers",
    "FlextMeltanoLibraryRunner": "flext_meltano.services.library_runner",
    "FlextMeltanoPipelineAdapter": "flext_meltano.services.adapter_extensions",
    "FlextMeltanoPipelineCrudOperations": "flext_meltano.services._pipeline_ops",
    "FlextMeltanoPipelineLifecycleOperations": "flext_meltano.services._pipeline_lifecycle",
    "FlextMeltanoPipelineManager": "flext_meltano.services._pipeline_mgr",
    "FlextMeltanoPipelinePaths": "flext_meltano.services._pipeline_ops",
    "FlextMeltanoPluginManager": "flext_meltano.services._cli_small_managers",
    "FlextMeltanoProjectService": "flext_meltano.services.project_service",
    "FlextMeltanoService": "flext_meltano.services.services",
    "FlextMeltanoSingerCatalogMixin": "flext_meltano.services.singer_catalog",
    "FlextMeltanoSingerCliTranslator": "flext_meltano.services.singer_translator",
    "FlextMeltanoSingerManager": "flext_meltano.services.cli_managers",
    "FlextMeltanoSingerOrchestrationMixin": "flext_meltano.services.singer_orchestration",
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
    "cli_managers": "flext_meltano.services.cli_managers",
    "dbt_orchestration": "flext_meltano.services.dbt_orchestration",
    "dbt_project": "flext_meltano.services.dbt_project",
    "dbt_runner": "flext_meltano.services.dbt_runner",
    "executor": "flext_meltano.services.executor",
    "file_managers": "flext_meltano.services.file_managers",
    "library_runner": "flext_meltano.services.library_runner",
    "project_service": "flext_meltano.services.project_service",
    "services": "flext_meltano.services.services",
    "singer_catalog": "flext_meltano.services.singer_catalog",
    "singer_orchestration": "flext_meltano.services.singer_orchestration",
    "singer_state": "flext_meltano.services.singer_state",
    "singer_tap": "flext_meltano.services.singer_tap",
    "singer_target": "flext_meltano.services.singer_target",
    "singer_translator": "flext_meltano.services.singer_translator",
    "validators": "flext_meltano.services.validators",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
