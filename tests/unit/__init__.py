# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_api": ("TestsFlextMeltanoApi",),
        ".test_cli_integration": ("TestsFlextMeltanoCliIntegration",),
        ".test_cli_small_managers": ("TestsFlextMeltanoCliSmallManagers",),
        ".test_constants": ("TestsFlextMeltanoConstantsUnit",),
        ".test_execution_result": ("TestsFlextMeltanoExecutionResult",),
        ".test_executors": ("TestsFlextMeltanoExecutors",),
        ".test_library_runner": ("TestsFlextMeltanoLibraryRunner",),
        ".test_models": ("TestsFlextMeltanoModelsUnit",),
        ".test_plugin_protocols": ("TestsFlextMeltanoPluginProtocols",),
        ".test_services": ("TestsFlextMeltanoServices",),
        ".test_singer_cli_translator": ("TestsFlextMeltanoSingerCliTranslator",),
        ".test_singer_sdk_adapter": ("TestsFlextMeltanoSingerSdkAdapter",),
        ".test_singer_types": ("TestsFlextMeltanoSingerTypes",),
        ".test_tap_abstractions": ("TestsFlextMeltanoTapAbstractions",),
        ".test_target_abstractions": ("TestsFlextMeltanoTargetAbstractions",),
        ".test_typings": ("TestsFlextMeltanoTypingsUnit",),
        ".test_validators": ("TestsFlextMeltanoValidators",),
        ".tests_pipeline_cli_managers": ("TestFlextMeltanoPipelineCliManagers",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
