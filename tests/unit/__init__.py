# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .fixtures import (
        MELTANO_COMPONENT_CASES,
        MELTANO_COMPONENT_IDS,
        docker_manager,
        docker_services,
        meltano_component_case,
        meltano_execute_field,
        meltano_project,
        meltano_service,
        meltano_yml_config,
        postgres_service,
        redis_service,
        require_docker_service,
        singer_state,
        test_meltano_project_dir,
    )
    from .test_api import TestsFlextMeltanoApi
    from .test_cli_integration import TestsFlextMeltanoCliIntegration
    from .test_cli_small_managers import TestsFlextMeltanoCliSmallManagers
    from .test_connection_profile_protocol import (
        test_dbt_connection_profile_accepts_typed_serializable_model,
    )
    from .test_constants import TestsFlextMeltanoConstantsUnit
    from .test_declarative_tap import TestsFlextMeltanoDeclarativeTap
    from .test_execution_result import TestsFlextMeltanoExecutionResult
    from .test_executors import TestsFlextMeltanoExecutors
    from .test_library_runner import TestsFlextMeltanoLibraryRunner
    from .test_models import TestsFlextMeltanoModelsUnit
    from .test_plugin_protocols import TestsFlextMeltanoPluginProtocols
    from .test_services import TestsFlextMeltanoServices
    from .test_singer_cli_translator import TestsFlextMeltanoSingerCliTranslator
    from .test_singer_sdk_adapter import TestsFlextMeltanoSingerSdkAdapter
    from .test_singer_types import TestsFlextMeltanoSingerTypes
    from .test_tap_abstractions import TestFlextMeltanoAbstractionsComplete
    from .test_target_abstractions import TestsFlextMeltanoTargetAbstractions
    from .test_typings import TestsFlextMeltanoTypingsUnit
    from .test_validators import TestsFlextMeltanoValidators
    from .tests_pipeline_cli_managers import TestFlextMeltanoPipelineCliManagers
__all__: tuple[str, ...] = (
    "MELTANO_COMPONENT_CASES",
    "MELTANO_COMPONENT_IDS",
    "TestFlextMeltanoAbstractionsComplete",
    "TestFlextMeltanoPipelineCliManagers",
    "TestsFlextMeltanoApi",
    "TestsFlextMeltanoCliIntegration",
    "TestsFlextMeltanoCliSmallManagers",
    "TestsFlextMeltanoConstantsUnit",
    "TestsFlextMeltanoDeclarativeTap",
    "TestsFlextMeltanoExecutionResult",
    "TestsFlextMeltanoExecutors",
    "TestsFlextMeltanoLibraryRunner",
    "TestsFlextMeltanoModelsUnit",
    "TestsFlextMeltanoPluginProtocols",
    "TestsFlextMeltanoServices",
    "TestsFlextMeltanoSingerCliTranslator",
    "TestsFlextMeltanoSingerSdkAdapter",
    "TestsFlextMeltanoSingerTypes",
    "TestsFlextMeltanoTargetAbstractions",
    "TestsFlextMeltanoTypingsUnit",
    "TestsFlextMeltanoValidators",
    "c",
    "d",
    "docker_manager",
    "docker_services",
    "e",
    "h",
    "m",
    "meltano_component_case",
    "meltano_execute_field",
    "meltano_project",
    "meltano_service",
    "meltano_yml_config",
    "p",
    "postgres_service",
    "r",
    "redis_service",
    "require_docker_service",
    "s",
    "singer_state",
    "t",
    "td",
    "test_dbt_connection_profile_accepts_typed_serializable_model",
    "test_meltano_project_dir",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".fixtures": (
                "MELTANO_COMPONENT_CASES",
                "MELTANO_COMPONENT_IDS",
                "docker_manager",
                "docker_services",
                "meltano_component_case",
                "meltano_execute_field",
                "meltano_project",
                "meltano_service",
                "meltano_yml_config",
                "postgres_service",
                "redis_service",
                "require_docker_service",
                "singer_state",
                "test_meltano_project_dir",
            ),
            ".test_api": ("TestsFlextMeltanoApi",),
            ".test_cli_integration": ("TestsFlextMeltanoCliIntegration",),
            ".test_cli_small_managers": ("TestsFlextMeltanoCliSmallManagers",),
            ".test_connection_profile_protocol": (
                "test_dbt_connection_profile_accepts_typed_serializable_model",
            ),
            ".test_constants": ("TestsFlextMeltanoConstantsUnit",),
            ".test_declarative_tap": ("TestsFlextMeltanoDeclarativeTap",),
            ".test_execution_result": ("TestsFlextMeltanoExecutionResult",),
            ".test_executors": ("TestsFlextMeltanoExecutors",),
            ".test_library_runner": ("TestsFlextMeltanoLibraryRunner",),
            ".test_models": ("TestsFlextMeltanoModelsUnit",),
            ".test_plugin_protocols": ("TestsFlextMeltanoPluginProtocols",),
            ".test_services": ("TestsFlextMeltanoServices",),
            ".test_singer_cli_translator": ("TestsFlextMeltanoSingerCliTranslator",),
            ".test_singer_sdk_adapter": ("TestsFlextMeltanoSingerSdkAdapter",),
            ".test_singer_types": ("TestsFlextMeltanoSingerTypes",),
            ".test_tap_abstractions": ("TestFlextMeltanoAbstractionsComplete",),
            ".test_target_abstractions": ("TestsFlextMeltanoTargetAbstractions",),
            ".test_typings": ("TestsFlextMeltanoTypingsUnit",),
            ".test_validators": ("TestsFlextMeltanoValidators",),
            ".tests_pipeline_cli_managers": ("TestFlextMeltanoPipelineCliManagers",),
            "flext_tests": (
                "c",
                "d",
                "e",
                "h",
                "m",
                "p",
                "r",
                "s",
                "t",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "u",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
