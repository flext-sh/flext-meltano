# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

TESTS_FLEXT_MELTANO_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        ".base": ("TestsFlextMeltanoServiceBase",),
        ".conftest": ("conftest",),
        ".constants": (
            "TestsFlextMeltanoConstants",
            "c",
        ),
        ".integration": ("integration",),
        ".integration.test_docker_integration": ("TestsFlextMeltanoDockerIntegration",),
        ".models": ("TestsFlextMeltanoModels",),
        ".protocols": ("TestsFlextMeltanoProtocols",),
        ".settings": ("TestsFlextMeltanoSettings",),
        ".typings": ("TestsFlextMeltanoTypes",),
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
        ".utilities": ("TestsFlextMeltanoUtilities",),
        "flext_tests": (
            "d",
            "e",
            "h",
        ),
    },
)

__all__: list[str] = ["TESTS_FLEXT_MELTANO_LAZY_IMPORTS_PART_01"]
