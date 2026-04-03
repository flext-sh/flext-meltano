# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
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
    from flext_meltano import (
        pipeline_cli_managers_tests,
        test_api,
        test_cli_integration,
        test_config,
        test_constants,
        test_execution_result,
        test_executors,
        test_file_managers,
        test_library_runner,
        test_models,
        test_plugin_protocols,
        test_services,
        test_singer_cli_translator,
        test_singer_types,
        test_tap_abstractions,
        test_target_abstractions,
        test_typings,
        test_utilities,
        test_validators,
    )
    from flext_meltano.pipeline_cli_managers_tests import (
        config_json,
        create_pipeline,
        create_result,
        delete_pipeline,
        delete_result,
        execute_pipeline,
        get_pipeline_status,
        list_pipelines,
        list_result,
        manager,
        mock_command_result,
        result,
        return_value,
        run_result,
        test_get_pipeline_status_checks_process_state,
        values,
    )
    from flext_meltano.test_api import (
        TestFlextMeltanoInitialization,
        TestFlextMeltanoPerformance,
        TestFlextMeltanoSuccessPaths,
        pytestmark,
    )
    from flext_meltano.test_cli_integration import TestCliModelConverterWithTapRunParams
    from flext_meltano.test_config import LogLevel
    from flext_meltano.test_constants import Testc
    from flext_meltano.test_execution_result import TestFlextMeltanoExecutionResult
    from flext_meltano.test_executors import TestFlextMeltanoExecutorComplete
    from flext_meltano.test_file_managers import (
        TestFlextMeltanoFileManagersComprehensive,
    )
    from flext_meltano.test_library_runner import TestFlextMeltanoLibraryRunner
    from flext_meltano.test_models import TestTapConfigEnhanced
    from flext_meltano.test_plugin_protocols import TestFlextMeltanoPluginProtocols
    from flext_meltano.test_services import TestFlextMeltanoServiceInitialization
    from flext_meltano.test_singer_cli_translator import (
        TestFlextMeltanoSingerCliTranslatorTapRun,
    )
    from flext_meltano.test_singer_types import TestFlextSingerTypes
    from flext_meltano.test_target_abstractions import (
        TestFlextMeltanoTargetAbstractionsComplete,
        logger,
    )
    from flext_meltano.test_typings import TestFlextMeltanoTypes
    from flext_meltano.test_utilities import TestFlextMeltanoUtilitiesEnhanced
    from flext_meltano.test_validators import TestFlextMeltanoValidatorsComprehensive

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "LogLevel": "flext_meltano.test_config",
    "TestCliModelConverterWithTapRunParams": "flext_meltano.test_cli_integration",
    "TestFlextMeltanoExecutionResult": "flext_meltano.test_execution_result",
    "TestFlextMeltanoExecutorComplete": "flext_meltano.test_executors",
    "TestFlextMeltanoFileManagersComprehensive": "flext_meltano.test_file_managers",
    "TestFlextMeltanoInitialization": "flext_meltano.test_api",
    "TestFlextMeltanoLibraryRunner": "flext_meltano.test_library_runner",
    "TestFlextMeltanoPerformance": "flext_meltano.test_api",
    "TestFlextMeltanoPluginProtocols": "flext_meltano.test_plugin_protocols",
    "TestFlextMeltanoServiceInitialization": "flext_meltano.test_services",
    "TestFlextMeltanoSingerCliTranslatorTapRun": "flext_meltano.test_singer_cli_translator",
    "TestFlextMeltanoSuccessPaths": "flext_meltano.test_api",
    "TestFlextMeltanoTargetAbstractionsComplete": "flext_meltano.test_target_abstractions",
    "TestFlextMeltanoTypes": "flext_meltano.test_typings",
    "TestFlextMeltanoUtilitiesEnhanced": "flext_meltano.test_utilities",
    "TestFlextMeltanoValidatorsComprehensive": "flext_meltano.test_validators",
    "TestFlextSingerTypes": "flext_meltano.test_singer_types",
    "TestTapConfigEnhanced": "flext_meltano.test_models",
    "Testc": "flext_meltano.test_constants",
    "c": ("flext_core.constants", "FlextConstants"),
    "config_json": "flext_meltano.pipeline_cli_managers_tests",
    "create_pipeline": "flext_meltano.pipeline_cli_managers_tests",
    "create_result": "flext_meltano.pipeline_cli_managers_tests",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "delete_pipeline": "flext_meltano.pipeline_cli_managers_tests",
    "delete_result": "flext_meltano.pipeline_cli_managers_tests",
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "execute_pipeline": "flext_meltano.pipeline_cli_managers_tests",
    "get_pipeline_status": "flext_meltano.pipeline_cli_managers_tests",
    "h": ("flext_core.handlers", "FlextHandlers"),
    "list_pipelines": "flext_meltano.pipeline_cli_managers_tests",
    "list_result": "flext_meltano.pipeline_cli_managers_tests",
    "logger": "flext_meltano.test_target_abstractions",
    "m": ("flext_core.models", "FlextModels"),
    "manager": "flext_meltano.pipeline_cli_managers_tests",
    "mock_command_result": "flext_meltano.pipeline_cli_managers_tests",
    "p": ("flext_core.protocols", "FlextProtocols"),
    "pipeline_cli_managers_tests": "flext_meltano.pipeline_cli_managers_tests",
    "pytestmark": "flext_meltano.test_api",
    "r": ("flext_core.result", "FlextResult"),
    "result": "flext_meltano.pipeline_cli_managers_tests",
    "return_value": "flext_meltano.pipeline_cli_managers_tests",
    "run_result": "flext_meltano.pipeline_cli_managers_tests",
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "test_api": "flext_meltano.test_api",
    "test_cli_integration": "flext_meltano.test_cli_integration",
    "test_config": "flext_meltano.test_config",
    "test_constants": "flext_meltano.test_constants",
    "test_execution_result": "flext_meltano.test_execution_result",
    "test_executors": "flext_meltano.test_executors",
    "test_file_managers": "flext_meltano.test_file_managers",
    "test_get_pipeline_status_checks_process_state": "flext_meltano.pipeline_cli_managers_tests",
    "test_library_runner": "flext_meltano.test_library_runner",
    "test_models": "flext_meltano.test_models",
    "test_plugin_protocols": "flext_meltano.test_plugin_protocols",
    "test_services": "flext_meltano.test_services",
    "test_singer_cli_translator": "flext_meltano.test_singer_cli_translator",
    "test_singer_types": "flext_meltano.test_singer_types",
    "test_tap_abstractions": "flext_meltano.test_tap_abstractions",
    "test_target_abstractions": "flext_meltano.test_target_abstractions",
    "test_typings": "flext_meltano.test_typings",
    "test_utilities": "flext_meltano.test_utilities",
    "test_validators": "flext_meltano.test_validators",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "values": "flext_meltano.pipeline_cli_managers_tests",
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
