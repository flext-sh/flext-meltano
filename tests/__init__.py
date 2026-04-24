# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_tests import td, tf, tk, tm, tv

    from flext_meltano import d, e, h, r, s, x
    from tests.conftest import MockMeltanoService, MockSingerTap, MockSingerTarget
    from tests.constants import TestsFlextMeltanoConstants, c
    from tests.integration.test_docker_integration import TestDockerIntegration
    from tests.models import TestsFlextMeltanoModels, m
    from tests.protocols import TestsFlextMeltanoProtocols, p
    from tests.typings import TestsFlextMeltanoTypes, t
    from tests.unit.test_api import TestFlextMeltanoApiFacade
    from tests.unit.test_cli_integration import TestFlextMeltanoCliModelConversion
    from tests.unit.test_cli_small_managers import TestFlextMeltanoCliSmallManagers
    from tests.unit.test_constants import Testc
    from tests.unit.test_execution_result import TestFlextMeltanoExecutionResult
    from tests.unit.test_executors import TestFlextMeltanoExecutorComplete
    from tests.unit.test_library_runner import TestFlextMeltanoLibraryRunner
    from tests.unit.test_models import TestFlextMeltanoModels
    from tests.unit.test_plugin_protocols import TestFlextMeltanoPluginProtocols
    from tests.unit.test_services import TestFlextMeltanoPublicFacade
    from tests.unit.test_singer_cli_translator import (
        TestFlextMeltanoSingerCliTranslator,
    )
    from tests.unit.test_singer_sdk_adapter import TestFlextMeltanoSingerSdkAdapter
    from tests.unit.test_singer_types import TestFlextSingerTypes
    from tests.unit.test_tap_abstractions import TestFlextMeltanoAbstractionsComplete
    from tests.unit.test_target_abstractions import (
        TestFlextMeltanoTargetAbstractionsComplete,
    )
    from tests.unit.test_typings import TestFlextMeltanoTypes
    from tests.unit.test_validators import TestFlextMeltanoValidatorsComprehensive
    from tests.unit.tests_pipeline_cli_managers import (
        TestFlextMeltanoPipelineCliManagers,
    )
    from tests.utilities import TestsFlextMeltanoUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".integration",
        ".unit",
    ),
    build_lazy_import_map(
        {
            ".conftest": (
                "MockMeltanoService",
                "MockSingerTap",
                "MockSingerTarget",
            ),
            ".constants": (
                "TestsFlextMeltanoConstants",
                "c",
            ),
            ".integration.test_docker_integration": ("TestDockerIntegration",),
            ".models": (
                "TestsFlextMeltanoModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextMeltanoProtocols",
                "p",
            ),
            ".typings": (
                "TestsFlextMeltanoTypes",
                "t",
            ),
            ".unit.test_api": ("TestFlextMeltanoApiFacade",),
            ".unit.test_cli_integration": ("TestFlextMeltanoCliModelConversion",),
            ".unit.test_cli_small_managers": ("TestFlextMeltanoCliSmallManagers",),
            ".unit.test_constants": ("Testc",),
            ".unit.test_execution_result": ("TestFlextMeltanoExecutionResult",),
            ".unit.test_executors": ("TestFlextMeltanoExecutorComplete",),
            ".unit.test_library_runner": ("TestFlextMeltanoLibraryRunner",),
            ".unit.test_models": ("TestFlextMeltanoModels",),
            ".unit.test_plugin_protocols": ("TestFlextMeltanoPluginProtocols",),
            ".unit.test_services": ("TestFlextMeltanoPublicFacade",),
            ".unit.test_singer_cli_translator": (
                "TestFlextMeltanoSingerCliTranslator",
            ),
            ".unit.test_singer_sdk_adapter": ("TestFlextMeltanoSingerSdkAdapter",),
            ".unit.test_singer_types": ("TestFlextSingerTypes",),
            ".unit.test_tap_abstractions": ("TestFlextMeltanoAbstractionsComplete",),
            ".unit.test_target_abstractions": (
                "TestFlextMeltanoTargetAbstractionsComplete",
            ),
            ".unit.test_typings": ("TestFlextMeltanoTypes",),
            ".unit.test_validators": ("TestFlextMeltanoValidatorsComprehensive",),
            ".unit.tests_pipeline_cli_managers": (
                "TestFlextMeltanoPipelineCliManagers",
            ),
            ".utilities": (
                "TestsFlextMeltanoUtilities",
                "u",
            ),
            "flext_meltano": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
            "flext_tests": (
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
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
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "MockMeltanoService",
    "MockSingerTap",
    "MockSingerTarget",
    "TestDockerIntegration",
    "TestFlextMeltanoAbstractionsComplete",
    "TestFlextMeltanoApiFacade",
    "TestFlextMeltanoCliModelConversion",
    "TestFlextMeltanoCliSmallManagers",
    "TestFlextMeltanoExecutionResult",
    "TestFlextMeltanoExecutorComplete",
    "TestFlextMeltanoLibraryRunner",
    "TestFlextMeltanoModels",
    "TestFlextMeltanoPipelineCliManagers",
    "TestFlextMeltanoPluginProtocols",
    "TestFlextMeltanoPublicFacade",
    "TestFlextMeltanoSingerCliTranslator",
    "TestFlextMeltanoSingerSdkAdapter",
    "TestFlextMeltanoTargetAbstractionsComplete",
    "TestFlextMeltanoTypes",
    "TestFlextMeltanoValidatorsComprehensive",
    "TestFlextSingerTypes",
    "Testc",
    "TestsFlextMeltanoConstants",
    "TestsFlextMeltanoModels",
    "TestsFlextMeltanoProtocols",
    "TestsFlextMeltanoTypes",
    "TestsFlextMeltanoUtilities",
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
]
