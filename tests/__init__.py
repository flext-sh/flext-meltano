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
    from flext_tests import td as td, tf as tf, tk as tk, tm as tm, tv as tv

    from flext_meltano import d as d, e as e, h as h, r as r, x as x
    from tests.base import (
        TestsFlextMeltanoServiceBase as TestsFlextMeltanoServiceBase,
        s as s,
    )
    from tests.constants import (
        TestsFlextMeltanoConstants as TestsFlextMeltanoConstants,
        c as c,
    )
    from tests.integration.test_docker_integration import (
        TestsFlextMeltanoDockerIntegration as TestsFlextMeltanoDockerIntegration,
    )
    from tests.models import TestsFlextMeltanoModels as TestsFlextMeltanoModels, m as m
    from tests.protocols import (
        TestsFlextMeltanoProtocols as TestsFlextMeltanoProtocols,
        p as p,
    )
    from tests.settings import TestsFlextMeltanoSettings as TestsFlextMeltanoSettings
    from tests.typings import TestsFlextMeltanoTypes as TestsFlextMeltanoTypes, t as t
    from tests.unit.test_api import TestsFlextMeltanoApi as TestsFlextMeltanoApi
    from tests.unit.test_cli_integration import (
        TestsFlextMeltanoCliIntegration as TestsFlextMeltanoCliIntegration,
    )
    from tests.unit.test_cli_small_managers import (
        TestsFlextMeltanoCliSmallManagers as TestsFlextMeltanoCliSmallManagers,
    )
    from tests.unit.test_constants import (
        TestsFlextMeltanoConstantsUnit as TestsFlextMeltanoConstantsUnit,
    )
    from tests.unit.test_execution_result import (
        TestsFlextMeltanoExecutionResult as TestsFlextMeltanoExecutionResult,
    )
    from tests.unit.test_executors import (
        TestsFlextMeltanoExecutors as TestsFlextMeltanoExecutors,
    )
    from tests.unit.test_library_runner import (
        TestsFlextMeltanoLibraryRunner as TestsFlextMeltanoLibraryRunner,
    )
    from tests.unit.test_models import (
        TestsFlextMeltanoModelsUnit as TestsFlextMeltanoModelsUnit,
    )
    from tests.unit.test_plugin_protocols import (
        TestsFlextMeltanoPluginProtocols as TestsFlextMeltanoPluginProtocols,
    )
    from tests.unit.test_services import (
        TestsFlextMeltanoServices as TestsFlextMeltanoServices,
    )
    from tests.unit.test_singer_cli_translator import (
        TestsFlextMeltanoSingerCliTranslator as TestsFlextMeltanoSingerCliTranslator,
    )
    from tests.unit.test_singer_sdk_adapter import (
        TestsFlextMeltanoSingerSdkAdapter as TestsFlextMeltanoSingerSdkAdapter,
    )
    from tests.unit.test_singer_types import (
        TestsFlextMeltanoSingerTypes as TestsFlextMeltanoSingerTypes,
    )
    from tests.unit.test_tap_abstractions import (
        TestsFlextMeltanoTapAbstractions as TestsFlextMeltanoTapAbstractions,
    )
    from tests.unit.test_target_abstractions import (
        TestsFlextMeltanoTargetAbstractions as TestsFlextMeltanoTargetAbstractions,
    )
    from tests.unit.test_typings import (
        TestsFlextMeltanoTypingsUnit as TestsFlextMeltanoTypingsUnit,
    )
    from tests.unit.test_validators import (
        TestsFlextMeltanoValidators as TestsFlextMeltanoValidators,
    )
    from tests.unit.tests_pipeline_cli_managers import (
        TestFlextMeltanoPipelineCliManagers as TestFlextMeltanoPipelineCliManagers,
    )
    from tests.utilities import (
        TestsFlextMeltanoUtilities as TestsFlextMeltanoUtilities,
        u as u,
    )
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
            ".constants": (
                "TestsFlextMeltanoConstants",
                "c",
            ),
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
            "flext_meltano": (
                "d",
                "e",
                "h",
                "r",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "TestFlextMeltanoPipelineCliManagers",
    "TestsFlextMeltanoApi",
    "TestsFlextMeltanoCliIntegration",
    "TestsFlextMeltanoCliSmallManagers",
    "TestsFlextMeltanoConstants",
    "TestsFlextMeltanoConstantsUnit",
    "TestsFlextMeltanoDockerIntegration",
    "TestsFlextMeltanoExecutionResult",
    "TestsFlextMeltanoExecutors",
    "TestsFlextMeltanoLibraryRunner",
    "TestsFlextMeltanoModels",
    "TestsFlextMeltanoModelsUnit",
    "TestsFlextMeltanoPluginProtocols",
    "TestsFlextMeltanoProtocols",
    "TestsFlextMeltanoServiceBase",
    "TestsFlextMeltanoServices",
    "TestsFlextMeltanoSettings",
    "TestsFlextMeltanoSingerCliTranslator",
    "TestsFlextMeltanoSingerSdkAdapter",
    "TestsFlextMeltanoSingerTypes",
    "TestsFlextMeltanoTapAbstractions",
    "TestsFlextMeltanoTargetAbstractions",
    "TestsFlextMeltanoTypes",
    "TestsFlextMeltanoTypingsUnit",
    "TestsFlextMeltanoUtilities",
    "TestsFlextMeltanoValidators",
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
