# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_api": ("test_api",),
        ".test_cli_integration": ("test_cli_integration",),
        ".test_cli_small_managers": ("test_cli_small_managers",),
        ".test_constants": ("test_constants",),
        ".test_execution_result": ("test_execution_result",),
        ".test_executors": ("test_executors",),
        ".test_library_runner": ("test_library_runner",),
        ".test_models": ("test_models",),
        ".test_plugin_protocols": ("test_plugin_protocols",),
        ".test_services": ("test_services",),
        ".test_singer_cli_translator": ("test_singer_cli_translator",),
        ".test_singer_sdk_adapter": ("test_singer_sdk_adapter",),
        ".test_singer_types": ("test_singer_types",),
        ".test_tap_abstractions": ("test_tap_abstractions",),
        ".test_target_abstractions": ("test_target_abstractions",),
        ".test_typings": ("test_typings",),
        ".test_validators": ("test_validators",),
        ".tests_pipeline_cli_managers": ("tests_pipeline_cli_managers",),
        "flext_meltano": (
            "c",
            "d",
            "e",
            "h",
            "m",
            "p",
            "r",
            "s",
            "t",
            "u",
            "x",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
