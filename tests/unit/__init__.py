# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_api": ("TestFlextMeltanoApiFacade",),
        ".test_cli_integration": ("TestFlextMeltanoCliModelConversion",),
        ".test_cli_small_managers": ("TestFlextMeltanoCliSmallManagers",),
        ".test_constants": ("Testc",),
        ".test_execution_result": ("TestFlextMeltanoExecutionResult",),
        ".test_executors": ("TestFlextMeltanoExecutorComplete",),
        ".test_library_runner": ("TestFlextMeltanoLibraryRunner",),
        ".test_models": ("TestFlextMeltanoModels",),
        ".test_plugin_protocols": ("TestFlextMeltanoPluginProtocols",),
        ".test_services": ("TestFlextMeltanoPublicFacade",),
        ".test_singer_cli_translator": ("TestFlextMeltanoSingerCliTranslator",),
        ".test_singer_sdk_adapter": ("TestFlextMeltanoSingerSdkAdapter",),
        ".test_singer_types": ("TestFlextSingerTypes",),
        ".test_tap_abstractions": ("TestFlextMeltanoAbstractionsComplete",),
        ".test_target_abstractions": ("TestFlextMeltanoTargetAbstractionsComplete",),
        ".test_typings": ("TestFlextMeltanoTypes",),
        ".test_validators": ("TestFlextMeltanoValidatorsComprehensive",),
        ".tests_pipeline_cli_managers": ("TestFlextMeltanoPipelineCliManagers",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
