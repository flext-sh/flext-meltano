# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import tests.unit.pipeline_cli_managers_tests as _tests_unit_pipeline_cli_managers_tests

    pipeline_cli_managers_tests = _tests_unit_pipeline_cli_managers_tests
    import tests.unit.test_api as _tests_unit_test_api

    test_api = _tests_unit_test_api
    import tests.unit.test_cli_integration as _tests_unit_test_cli_integration

    test_cli_integration = _tests_unit_test_cli_integration
    import tests.unit.test_cli_small_managers as _tests_unit_test_cli_small_managers

    test_cli_small_managers = _tests_unit_test_cli_small_managers
    import tests.unit.test_constants as _tests_unit_test_constants

    test_constants = _tests_unit_test_constants
    import tests.unit.test_execution_result as _tests_unit_test_execution_result

    test_execution_result = _tests_unit_test_execution_result
    import tests.unit.test_executors as _tests_unit_test_executors

    test_executors = _tests_unit_test_executors
    import tests.unit.test_library_runner as _tests_unit_test_library_runner

    test_library_runner = _tests_unit_test_library_runner
    import tests.unit.test_models as _tests_unit_test_models

    test_models = _tests_unit_test_models
    import tests.unit.test_plugin_protocols as _tests_unit_test_plugin_protocols

    test_plugin_protocols = _tests_unit_test_plugin_protocols
    import tests.unit.test_services as _tests_unit_test_services

    test_services = _tests_unit_test_services
    import tests.unit.test_singer_cli_translator as _tests_unit_test_singer_cli_translator

    test_singer_cli_translator = _tests_unit_test_singer_cli_translator
    import tests.unit.test_singer_sdk_adapter as _tests_unit_test_singer_sdk_adapter

    test_singer_sdk_adapter = _tests_unit_test_singer_sdk_adapter
    import tests.unit.test_singer_types as _tests_unit_test_singer_types

    test_singer_types = _tests_unit_test_singer_types
    import tests.unit.test_tap_abstractions as _tests_unit_test_tap_abstractions

    test_tap_abstractions = _tests_unit_test_tap_abstractions
    import tests.unit.test_target_abstractions as _tests_unit_test_target_abstractions

    test_target_abstractions = _tests_unit_test_target_abstractions
    import tests.unit.test_typings as _tests_unit_test_typings

    test_typings = _tests_unit_test_typings
    import tests.unit.test_validators as _tests_unit_test_validators

    test_validators = _tests_unit_test_validators
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
_LAZY_IMPORTS = {
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "pipeline_cli_managers_tests": "tests.unit.pipeline_cli_managers_tests",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
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
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "pipeline_cli_managers_tests",
    "r",
    "s",
    "t",
    "test_api",
    "test_cli_integration",
    "test_cli_small_managers",
    "test_constants",
    "test_execution_result",
    "test_executors",
    "test_library_runner",
    "test_models",
    "test_plugin_protocols",
    "test_services",
    "test_singer_cli_translator",
    "test_singer_sdk_adapter",
    "test_singer_types",
    "test_tap_abstractions",
    "test_target_abstractions",
    "test_typings",
    "test_validators",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
