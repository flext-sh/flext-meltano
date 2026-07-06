# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if TYPE_CHECKING:
    from flext_tests import d, e, h, r, td, tf, tk, tm, tv, x

    from tests.base import TestsFlextMeltanoServiceBase, s
    from tests.constants import TestsFlextMeltanoConstants, c
    from tests.integration.test_docker_integration import (
        TestsFlextMeltanoDockerIntegration,
    )
    from tests.models import TestsFlextMeltanoModels, m
    from tests.protocols import TestsFlextMeltanoProtocols, p
    from tests.settings import TestsFlextMeltanoSettings
    from tests.typings import TestsFlextMeltanoTypes, t
    from tests.unit.test_api import TestsFlextMeltanoApi
    from tests.unit.test_cli_integration import TestsFlextMeltanoCliIntegration
    from tests.unit.test_cli_small_managers import TestsFlextMeltanoCliSmallManagers
    from tests.unit.test_constants import TestsFlextMeltanoConstantsUnit
    from tests.unit.test_execution_result import TestsFlextMeltanoExecutionResult
    from tests.unit.test_executors import TestsFlextMeltanoExecutors
    from tests.unit.test_library_runner import TestsFlextMeltanoLibraryRunner
    from tests.unit.test_models import TestsFlextMeltanoModelsUnit
    from tests.unit.test_plugin_protocols import TestsFlextMeltanoPluginProtocols
    from tests.unit.test_services import TestsFlextMeltanoServices
    from tests.unit.test_singer_cli_translator import (
        TestsFlextMeltanoSingerCliTranslator,
    )
    from tests.unit.test_singer_sdk_adapter import TestsFlextMeltanoSingerSdkAdapter
    from tests.unit.test_singer_types import TestsFlextMeltanoSingerTypes
    from tests.unit.test_tap_abstractions import TestsFlextMeltanoTapAbstractions
    from tests.unit.test_target_abstractions import TestsFlextMeltanoTargetAbstractions
    from tests.unit.test_typings import TestsFlextMeltanoTypingsUnit
    from tests.unit.test_validators import TestsFlextMeltanoValidators
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
            ".base": (
                "TestsFlextMeltanoServiceBase",
                "s",
            ),
            ".conftest": ("conftest",),
            ".constants": (
                "TestsFlextMeltanoConstants",
                "c",
            ),
            ".integration": ("integration",),
            ".integration.test_docker_integration": (
                "TestsFlextMeltanoDockerIntegration",
            ),
            ".models": (
                "TestsFlextMeltanoModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextMeltanoProtocols",
                "p",
            ),
            ".settings": ("TestsFlextMeltanoSettings",),
            ".typings": (
                "TestsFlextMeltanoTypes",
                "t",
            ),
            ".unit": ("unit",),
            ".unit.test_api": ("TestsFlextMeltanoApi",),
            ".unit.test_cli_integration": ("TestsFlextMeltanoCliIntegration",),
            ".unit.test_cli_small_managers": ("TestsFlextMeltanoCliSmallManagers",),
            ".unit.test_constants": ("TestsFlextMeltanoConstantsUnit",),
            ".unit.test_execution_result": ("TestsFlextMeltanoExecutionResult",),
            ".unit.test_executors": ("TestsFlextMeltanoExecutors",),
            ".unit.test_library_runner": ("TestsFlextMeltanoLibraryRunner",),
            ".unit.test_models": ("TestsFlextMeltanoModelsUnit",),
            ".unit.test_plugin_protocols": ("TestsFlextMeltanoPluginProtocols",),
            ".unit.test_services": ("TestsFlextMeltanoServices",),
            ".unit.test_singer_cli_translator": (
                "TestsFlextMeltanoSingerCliTranslator",
            ),
            ".unit.test_singer_sdk_adapter": ("TestsFlextMeltanoSingerSdkAdapter",),
            ".unit.test_singer_types": ("TestsFlextMeltanoSingerTypes",),
            ".unit.test_tap_abstractions": ("TestsFlextMeltanoTapAbstractions",),
            ".unit.test_target_abstractions": ("TestsFlextMeltanoTargetAbstractions",),
            ".unit.test_typings": ("TestsFlextMeltanoTypingsUnit",),
            ".unit.test_validators": ("TestsFlextMeltanoValidators",),
            ".unit.tests_pipeline_cli_managers": (
                "TestFlextMeltanoPipelineCliManagers",
            ),
            ".utilities": (
                "TestsFlextMeltanoUtilities",
                "u",
            ),
            "flext_tests": (
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
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
    publish_all=False,
)
