# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export registry."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, merge_lazy_imports

_LOCAL_LAZY_IMPORTS = build_lazy_import_map(
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
        ".integration.test_docker_integration": ("TestsFlextMeltanoDockerIntegration",),
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
        ".unit.test_singer_cli_translator": ("TestsFlextMeltanoSingerCliTranslator",),
        ".unit.test_singer_sdk_adapter": ("TestsFlextMeltanoSingerSdkAdapter",),
        ".unit.test_singer_types": ("TestsFlextMeltanoSingerTypes",),
        ".unit.test_tap_abstractions": ("TestsFlextMeltanoTapAbstractions",),
        ".unit.test_target_abstractions": ("TestsFlextMeltanoTargetAbstractions",),
        ".unit.test_typings": ("TestsFlextMeltanoTypingsUnit",),
        ".unit.test_validators": ("TestsFlextMeltanoValidators",),
        ".unit.tests_pipeline_cli_managers": ("TestFlextMeltanoPipelineCliManagers",),
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
)

TESTS_FLEXT_MELTANO_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".integration",
        ".unit",
    ),
    _LOCAL_LAZY_IMPORTS,
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
    module_name="tests",
)

__all__: list[str] = ["TESTS_FLEXT_MELTANO_LAZY_IMPORTS"]
