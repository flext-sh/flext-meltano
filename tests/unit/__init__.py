# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "pipeline_cli_managers_tests": "tests.unit.pipeline_cli_managers_tests",
    "test_api": "tests.unit.test_api",
    "test_cli_integration": "tests.unit.test_cli_integration",
    "test_cli_small_managers": "tests.unit.test_cli_small_managers",
    "test_constants": "tests.unit.test_constants",
    "test_execution_result": "tests.unit.test_execution_result",
    "test_executors": "tests.unit.test_executors",
    "test_library_runner": "tests.unit.test_library_runner",
    "test_models": "tests.unit.test_models",
    "test_plugin_protocols": "tests.unit.test_plugin_protocols",
    "test_services": "tests.unit.test_services",
    "test_singer_cli_translator": "tests.unit.test_singer_cli_translator",
    "test_singer_sdk_adapter": "tests.unit.test_singer_sdk_adapter",
    "test_singer_types": "tests.unit.test_singer_types",
    "test_tap_abstractions": "tests.unit.test_tap_abstractions",
    "test_target_abstractions": "tests.unit.test_target_abstractions",
    "test_typings": "tests.unit.test_typings",
    "test_validators": "tests.unit.test_validators",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
