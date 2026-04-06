# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Services package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    import flext_meltano.services._abstractions_base as _flext_meltano_services__abstractions_base

    _abstractions_base = _flext_meltano_services__abstractions_base
    import flext_meltano.services._cli_small_managers as _flext_meltano_services__cli_small_managers
    from flext_meltano.services._abstractions_base import FlextMeltanoAbstractionsBase

    _cli_small_managers = _flext_meltano_services__cli_small_managers
    import flext_meltano.services._executor_base as _flext_meltano_services__executor_base
    from flext_meltano.services._cli_small_managers import (
        FlextMeltanoDbtManager,
        FlextMeltanoPluginManager,
        FlextMeltanoStatusManager,
    )

    _executor_base = _flext_meltano_services__executor_base
    import flext_meltano.services._pipeline_lifecycle as _flext_meltano_services__pipeline_lifecycle
    from flext_meltano.services._executor_base import FlextMeltanoExecutorBase

    _pipeline_lifecycle = _flext_meltano_services__pipeline_lifecycle
    import flext_meltano.services._pipeline_mgr as _flext_meltano_services__pipeline_mgr
    from flext_meltano.services._pipeline_lifecycle import (
        FlextMeltanoPipelineLifecycleOperations,
    )

    _pipeline_mgr = _flext_meltano_services__pipeline_mgr
    import flext_meltano.services._pipeline_ops as _flext_meltano_services__pipeline_ops
    from flext_meltano.services._pipeline_mgr import FlextMeltanoPipelineManager

    _pipeline_ops = _flext_meltano_services__pipeline_ops
    import flext_meltano.services.abstractions as _flext_meltano_services_abstractions
    from flext_meltano.services._pipeline_ops import (
        FlextMeltanoPipelineCrudOperations,
        FlextMeltanoPipelinePaths,
    )

    abstractions = _flext_meltano_services_abstractions
    import flext_meltano.services.adapter_extensions as _flext_meltano_services_adapter_extensions
    from flext_meltano.services.abstractions import FlextMeltanoAbstractions

    adapter_extensions = _flext_meltano_services_adapter_extensions
    import flext_meltano.services.adapters as _flext_meltano_services_adapters
    from flext_meltano.services.adapter_extensions import (
        FlextMeltanoDbtAdapter,
        FlextMeltanoPipelineAdapter,
    )

    adapters = _flext_meltano_services_adapters
    import flext_meltano.services.bridge as _flext_meltano_services_bridge
    from flext_meltano.services.adapters import FlextMeltanoAdapter

    bridge = _flext_meltano_services_bridge
    import flext_meltano.services.cli_managers as _flext_meltano_services_cli_managers
    from flext_meltano.services.bridge import FlextMeltanoBridge

    cli_managers = _flext_meltano_services_cli_managers
    import flext_meltano.services.consumer_bases as _flext_meltano_services_consumer_bases
    from flext_meltano.services.cli_managers import (
        FlextMeltanoCommandRouter,
        FlextMeltanoSingerManager,
    )

    consumer_bases = _flext_meltano_services_consumer_bases
    import flext_meltano.services.dbt_project as _flext_meltano_services_dbt_project
    from flext_meltano.services.consumer_bases import (
        FlextMeltanoDbtServiceBase,
        FlextMeltanoTapServiceBase,
        FlextMeltanoTargetServiceBase,
        dbt_service_base,
        tap_service_base,
        target_service_base,
    )

    dbt_project = _flext_meltano_services_dbt_project
    import flext_meltano.services.dbt_runner as _flext_meltano_services_dbt_runner
    from flext_meltano.services.dbt_project import FlextMeltanoDbtProjectMixin

    dbt_runner = _flext_meltano_services_dbt_runner
    import flext_meltano.services.executor as _flext_meltano_services_executor
    from flext_meltano.services.dbt_runner import FlextMeltanoDbtRunnerMixin

    executor = _flext_meltano_services_executor
    import flext_meltano.services.library_runner as _flext_meltano_services_library_runner
    from flext_meltano.services.executor import FlextMeltanoExecutor

    library_runner = _flext_meltano_services_library_runner
    import flext_meltano.services.meltano_dbt_transformation as _flext_meltano_services_meltano_dbt_transformation
    from flext_meltano.services.library_runner import FlextMeltanoLibraryRunner

    meltano_dbt_transformation = _flext_meltano_services_meltano_dbt_transformation
    import flext_meltano.services.meltano_plugin_discovery as _flext_meltano_services_meltano_plugin_discovery
    from flext_meltano.services.meltano_dbt_transformation import (
        FlextMeltanoDbtTransformationRunner,
    )

    meltano_plugin_discovery = _flext_meltano_services_meltano_plugin_discovery
    import flext_meltano.services.meltano_plugins as _flext_meltano_services_meltano_plugins
    from flext_meltano.services.meltano_plugin_discovery import (
        FlextMeltanoPluginDiscoveryMixin,
    )

    meltano_plugins = _flext_meltano_services_meltano_plugins
    import flext_meltano.services.meltano_project_sdk as _flext_meltano_services_meltano_project_sdk
    from flext_meltano.services.meltano_plugins import FlextMeltanoComponentService

    meltano_project_sdk = _flext_meltano_services_meltano_project_sdk
    import flext_meltano.services.project_service as _flext_meltano_services_project_service
    from flext_meltano.services.meltano_project_sdk import FlextMeltanoProjectManager

    project_service = _flext_meltano_services_project_service
    import flext_meltano.services.services as _flext_meltano_services_services
    from flext_meltano.services.project_service import FlextMeltanoProjectService

    services = _flext_meltano_services_services
    import flext_meltano.services.singer_catalog as _flext_meltano_services_singer_catalog
    from flext_meltano.services.services import FlextMeltanoService

    singer_catalog = _flext_meltano_services_singer_catalog
    import flext_meltano.services.singer_sdk as _flext_meltano_services_singer_sdk
    from flext_meltano.services.singer_catalog import FlextMeltanoSingerCatalogMixin

    singer_sdk = _flext_meltano_services_singer_sdk
    import flext_meltano.services.singer_state as _flext_meltano_services_singer_state
    from flext_meltano.services.singer_sdk import (
        Context,
        FlextMeltanoSingerTapAdapter,
        Record,
        Sink,
        Stream,
        Tap,
        Target,
    )

    singer_state = _flext_meltano_services_singer_state
    import flext_meltano.services.singer_tap as _flext_meltano_services_singer_tap
    from flext_meltano.services.singer_state import FlextMeltanoSingerStateMixin

    singer_tap = _flext_meltano_services_singer_tap
    import flext_meltano.services.singer_target as _flext_meltano_services_singer_target
    from flext_meltano.services.singer_tap import (
        FlextMeltanoTapAbstractions,
        FlextMeltanoTapSourceMixin,
    )

    singer_target = _flext_meltano_services_singer_target
    import flext_meltano.services.singer_translator as _flext_meltano_services_singer_translator
    from flext_meltano.services.singer_target import FlextMeltanoTargetAbstractions

    singer_translator = _flext_meltano_services_singer_translator
    import flext_meltano.services.validators as _flext_meltano_services_validators
    from flext_meltano.services.singer_translator import FlextMeltanoSingerCliTranslator

    validators = _flext_meltano_services_validators
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
    from flext_meltano.services.validators import FlextMeltanoValidators
_LAZY_IMPORTS = merge_lazy_imports(
    ("flext_meltano.services.consumer_bases",),
    {
        "FlextMeltanoAbstractions": (
            "flext_meltano.services.abstractions",
            "FlextMeltanoAbstractions",
        ),
        "FlextMeltanoAbstractionsBase": (
            "flext_meltano.services._abstractions_base",
            "FlextMeltanoAbstractionsBase",
        ),
        "FlextMeltanoAdapter": (
            "flext_meltano.services.adapters",
            "FlextMeltanoAdapter",
        ),
        "FlextMeltanoBridge": ("flext_meltano.services.bridge", "FlextMeltanoBridge"),
        "FlextMeltanoCommandRouter": (
            "flext_meltano.services.cli_managers",
            "FlextMeltanoCommandRouter",
        ),
        "FlextMeltanoComponentService": (
            "flext_meltano.services.meltano_plugins",
            "FlextMeltanoComponentService",
        ),
        "FlextMeltanoDbtAdapter": (
            "flext_meltano.services.adapter_extensions",
            "FlextMeltanoDbtAdapter",
        ),
        "FlextMeltanoDbtManager": (
            "flext_meltano.services._cli_small_managers",
            "FlextMeltanoDbtManager",
        ),
        "FlextMeltanoDbtProjectMixin": (
            "flext_meltano.services.dbt_project",
            "FlextMeltanoDbtProjectMixin",
        ),
        "FlextMeltanoDbtRunnerMixin": (
            "flext_meltano.services.dbt_runner",
            "FlextMeltanoDbtRunnerMixin",
        ),
        "FlextMeltanoDbtTransformationRunner": (
            "flext_meltano.services.meltano_dbt_transformation",
            "FlextMeltanoDbtTransformationRunner",
        ),
        "FlextMeltanoExecutor": (
            "flext_meltano.services.executor",
            "FlextMeltanoExecutor",
        ),
        "FlextMeltanoExecutorBase": (
            "flext_meltano.services._executor_base",
            "FlextMeltanoExecutorBase",
        ),
        "FlextMeltanoLibraryRunner": (
            "flext_meltano.services.library_runner",
            "FlextMeltanoLibraryRunner",
        ),
        "FlextMeltanoPipelineAdapter": (
            "flext_meltano.services.adapter_extensions",
            "FlextMeltanoPipelineAdapter",
        ),
        "FlextMeltanoPipelineCrudOperations": (
            "flext_meltano.services._pipeline_ops",
            "FlextMeltanoPipelineCrudOperations",
        ),
        "FlextMeltanoPipelineLifecycleOperations": (
            "flext_meltano.services._pipeline_lifecycle",
            "FlextMeltanoPipelineLifecycleOperations",
        ),
        "FlextMeltanoPipelineManager": (
            "flext_meltano.services._pipeline_mgr",
            "FlextMeltanoPipelineManager",
        ),
        "FlextMeltanoPipelinePaths": (
            "flext_meltano.services._pipeline_ops",
            "FlextMeltanoPipelinePaths",
        ),
        "FlextMeltanoPluginDiscoveryMixin": (
            "flext_meltano.services.meltano_plugin_discovery",
            "FlextMeltanoPluginDiscoveryMixin",
        ),
        "FlextMeltanoPluginManager": (
            "flext_meltano.services._cli_small_managers",
            "FlextMeltanoPluginManager",
        ),
        "FlextMeltanoProjectManager": (
            "flext_meltano.services.meltano_project_sdk",
            "FlextMeltanoProjectManager",
        ),
        "FlextMeltanoProjectService": (
            "flext_meltano.services.project_service",
            "FlextMeltanoProjectService",
        ),
        "FlextMeltanoService": (
            "flext_meltano.services.services",
            "FlextMeltanoService",
        ),
        "FlextMeltanoSingerCatalogMixin": (
            "flext_meltano.services.singer_catalog",
            "FlextMeltanoSingerCatalogMixin",
        ),
        "FlextMeltanoSingerCliTranslator": (
            "flext_meltano.services.singer_translator",
            "FlextMeltanoSingerCliTranslator",
        ),
        "Context": (
            "flext_meltano.services.singer_sdk",
            "Context",
        ),
        "FlextMeltanoSingerManager": (
            "flext_meltano.services.cli_managers",
            "FlextMeltanoSingerManager",
        ),
        "Record": (
            "flext_meltano.services.singer_sdk",
            "Record",
        ),
        "Sink": (
            "flext_meltano.services.singer_sdk",
            "Sink",
        ),
        "FlextMeltanoSingerStateMixin": (
            "flext_meltano.services.singer_state",
            "FlextMeltanoSingerStateMixin",
        ),
        "Stream": (
            "flext_meltano.services.singer_sdk",
            "Stream",
        ),
        "FlextMeltanoSingerTapAdapter": (
            "flext_meltano.services.singer_sdk",
            "FlextMeltanoSingerTapAdapter",
        ),
        "Tap": (
            "flext_meltano.services.singer_sdk",
            "Tap",
        ),
        "Target": (
            "flext_meltano.services.singer_sdk",
            "Target",
        ),
        "FlextMeltanoStatusManager": (
            "flext_meltano.services._cli_small_managers",
            "FlextMeltanoStatusManager",
        ),
        "FlextMeltanoTapAbstractions": (
            "flext_meltano.services.singer_tap",
            "FlextMeltanoTapAbstractions",
        ),
        "FlextMeltanoTapSourceMixin": (
            "flext_meltano.services.singer_tap",
            "FlextMeltanoTapSourceMixin",
        ),
        "FlextMeltanoTargetAbstractions": (
            "flext_meltano.services.singer_target",
            "FlextMeltanoTargetAbstractions",
        ),
        "FlextMeltanoValidators": (
            "flext_meltano.services.validators",
            "FlextMeltanoValidators",
        ),
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
        "singer_sdk": "flext_meltano.services.singer_sdk",
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
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
    "Context",
    "FlextMeltanoAbstractions",
    "FlextMeltanoAbstractionsBase",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCommandRouter",
    "FlextMeltanoComponentService",
    "FlextMeltanoDbtAdapter",
    "FlextMeltanoDbtManager",
    "FlextMeltanoDbtProjectMixin",
    "FlextMeltanoDbtRunnerMixin",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoDbtTransformationRunner",
    "FlextMeltanoExecutor",
    "FlextMeltanoExecutorBase",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoPipelineAdapter",
    "FlextMeltanoPipelineCrudOperations",
    "FlextMeltanoPipelineLifecycleOperations",
    "FlextMeltanoPipelineManager",
    "FlextMeltanoPipelinePaths",
    "FlextMeltanoPluginDiscoveryMixin",
    "FlextMeltanoPluginManager",
    "FlextMeltanoProjectManager",
    "FlextMeltanoProjectService",
    "FlextMeltanoService",
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
    "FlextMeltanoValidators",
    "Record",
    "Sink",
    "Stream",
    "Tap",
    "Target",
    "_abstractions_base",
    "_cli_small_managers",
    "_executor_base",
    "_pipeline_lifecycle",
    "_pipeline_mgr",
    "_pipeline_ops",
    "abstractions",
    "adapter_extensions",
    "adapters",
    "bridge",
    "c",
    "cli_managers",
    "consumer_bases",
    "d",
    "dbt_project",
    "dbt_runner",
    "dbt_service_base",
    "e",
    "executor",
    "h",
    "library_runner",
    "m",
    "meltano_dbt_transformation",
    "meltano_plugin_discovery",
    "meltano_plugins",
    "meltano_project_sdk",
    "p",
    "project_service",
    "r",
    "s",
    "services",
    "singer_catalog",
    "singer_sdk",
    "singer_state",
    "singer_tap",
    "singer_target",
    "singer_translator",
    "t",
    "tap_service_base",
    "target_service_base",
    "u",
    "validators",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
