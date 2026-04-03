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
    from tests.unit.pipeline_cli_managers_tests import (
        create_pipeline,
        delete_pipeline,
        execute_pipeline,
        get_pipeline_status,
        list_pipelines,
        test_create_pipeline_creates_directory_and_configuration,
        test_create_pipeline_fails_without_configuration,
        test_delete_pipeline_removes_configuration_directory,
        test_execute_pipeline_fails_when_pipeline_execution_is_not_configured,
        test_execute_pipeline_runs_real_subprocess_contract,
        test_get_pipeline_status_checks_process_state,
        test_pipeline_manager_lifecycle_commands_delegate_to_real_operations,
    )

    test_api = _tests_unit_test_api
    import tests.unit.test_cli_integration as _tests_unit_test_cli_integration
    from tests.unit.test_api import (
        TestFlextMeltanoCatalogOperations,
        TestFlextMeltanoErrorHandling,
        TestFlextMeltanoExecuteMethod,
        TestFlextMeltanoInitialization,
        TestFlextMeltanoIntegration,
        TestFlextMeltanoPerformance,
        TestFlextMeltanoPipelineOperations,
        TestFlextMeltanoPluginOperations,
        TestFlextMeltanoProjectOperations,
        TestFlextMeltanoSuccessPaths,
        pytestmark,
    )

    test_cli_integration = _tests_unit_test_cli_integration
    import tests.unit.test_config as _tests_unit_test_config
    from tests.unit.test_cli_integration import (
        TestCliModelConverterWithDbtRunParams,
        TestCliModelConverterWithPipelineRunParams,
        TestCliModelConverterWithTapRunParams,
        TestCliModelConverterWithTargetRunParams,
    )

    test_config = _tests_unit_test_config
    import tests.unit.test_constants as _tests_unit_test_constants
    from tests.unit.test_config import (
        LogLevel,
        TestFlextMeltanoSettings,
        TestFlextMeltanoSettingsConstants,
        TestFlextMeltanoSettingsEdgeCases,
        TestFlextMeltanoSettingsEnums,
        TestFlextMeltanoSettingsIntegration,
    )

    test_constants = _tests_unit_test_constants
    import tests.unit.test_execution_result as _tests_unit_test_execution_result
    from tests.unit.test_constants import Testc

    test_execution_result = _tests_unit_test_execution_result
    import tests.unit.test_executors as _tests_unit_test_executors
    from tests.unit.test_execution_result import TestFlextMeltanoExecutionResult

    test_executors = _tests_unit_test_executors
    import tests.unit.test_file_managers as _tests_unit_test_file_managers
    from tests.unit.test_executors import TestFlextMeltanoExecutorComplete

    test_file_managers = _tests_unit_test_file_managers
    import tests.unit.test_library_runner as _tests_unit_test_library_runner
    from tests.unit.test_file_managers import TestFlextMeltanoFileManagersComprehensive

    test_library_runner = _tests_unit_test_library_runner
    import tests.unit.test_models as _tests_unit_test_models
    from tests.unit.test_library_runner import (
        TestFlextMeltanoLibraryRunner,
        TestProjectAdapterIntegration,
    )

    test_models = _tests_unit_test_models
    import tests.unit.test_plugin_protocols as _tests_unit_test_plugin_protocols
    from tests.unit.test_models import (
        TestDbtProjectModelEnhanced,
        TestMeltanoProjectModelEnhanced,
        TestModelIntegration,
        TestPluginModelEnhanced,
        TestStreamInfoEnhanced,
        TestTapConfigEnhanced,
        TestTargetConfigEnhanced,
    )

    test_plugin_protocols = _tests_unit_test_plugin_protocols
    import tests.unit.test_services as _tests_unit_test_services
    from tests.unit.test_plugin_protocols import TestFlextMeltanoPluginProtocols

    test_services = _tests_unit_test_services
    import tests.unit.test_singer_cli_translator as _tests_unit_test_singer_cli_translator
    from tests.unit.test_services import (
        TestDbtService,
        TestFlextMeltanoServiceInitialization,
        TestServiceArchitecture,
        TestServiceErrorHandling,
        TestServiceFactoryMethods,
        TestServiceGenericMethods,
        TestServiceIntegration,
        TestTapService,
        TestTargetService,
    )

    test_singer_cli_translator = _tests_unit_test_singer_cli_translator
    import tests.unit.test_singer_types as _tests_unit_test_singer_types
    from tests.unit.test_singer_cli_translator import (
        TestFlextMeltanoSingerCliTranslatorDbtRun,
        TestFlextMeltanoSingerCliTranslatorExecuteCommand,
        TestFlextMeltanoSingerCliTranslatorPipelineRun,
        TestFlextMeltanoSingerCliTranslatorTapRun,
        TestFlextMeltanoSingerCliTranslatorTargetRun,
    )

    test_singer_types = _tests_unit_test_singer_types
    import tests.unit.test_tap_abstractions as _tests_unit_test_tap_abstractions
    from tests.unit.test_singer_types import TestFlextSingerTypes

    test_tap_abstractions = _tests_unit_test_tap_abstractions
    import tests.unit.test_target_abstractions as _tests_unit_test_target_abstractions
    from tests.unit.test_tap_abstractions import TestFlextMeltanoAbstractionsComplete

    test_target_abstractions = _tests_unit_test_target_abstractions
    import tests.unit.test_typings as _tests_unit_test_typings
    from tests.unit.test_target_abstractions import (
        TestFlextMeltanoTargetAbstractionsComplete,
        logger,
    )

    test_typings = _tests_unit_test_typings
    import tests.unit.test_utilities as _tests_unit_test_utilities
    from tests.unit.test_typings import TestFlextMeltanoTypes

    test_utilities = _tests_unit_test_utilities
    import tests.unit.test_validators as _tests_unit_test_validators
    from tests.unit.test_utilities import TestFlextMeltanoUtilitiesEnhanced

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
    from tests.unit.test_validators import TestFlextMeltanoValidatorsComprehensive
_LAZY_IMPORTS = {
    "LogLevel": "tests.unit.test_config",
    "TestCliModelConverterWithDbtRunParams": "tests.unit.test_cli_integration",
    "TestCliModelConverterWithPipelineRunParams": "tests.unit.test_cli_integration",
    "TestCliModelConverterWithTapRunParams": "tests.unit.test_cli_integration",
    "TestCliModelConverterWithTargetRunParams": "tests.unit.test_cli_integration",
    "TestDbtProjectModelEnhanced": "tests.unit.test_models",
    "TestDbtService": "tests.unit.test_services",
    "TestFlextMeltanoAbstractionsComplete": "tests.unit.test_tap_abstractions",
    "TestFlextMeltanoCatalogOperations": "tests.unit.test_api",
    "TestFlextMeltanoErrorHandling": "tests.unit.test_api",
    "TestFlextMeltanoExecuteMethod": "tests.unit.test_api",
    "TestFlextMeltanoExecutionResult": "tests.unit.test_execution_result",
    "TestFlextMeltanoExecutorComplete": "tests.unit.test_executors",
    "TestFlextMeltanoFileManagersComprehensive": "tests.unit.test_file_managers",
    "TestFlextMeltanoInitialization": "tests.unit.test_api",
    "TestFlextMeltanoIntegration": "tests.unit.test_api",
    "TestFlextMeltanoLibraryRunner": "tests.unit.test_library_runner",
    "TestFlextMeltanoPerformance": "tests.unit.test_api",
    "TestFlextMeltanoPipelineOperations": "tests.unit.test_api",
    "TestFlextMeltanoPluginOperations": "tests.unit.test_api",
    "TestFlextMeltanoPluginProtocols": "tests.unit.test_plugin_protocols",
    "TestFlextMeltanoProjectOperations": "tests.unit.test_api",
    "TestFlextMeltanoServiceInitialization": "tests.unit.test_services",
    "TestFlextMeltanoSettings": "tests.unit.test_config",
    "TestFlextMeltanoSettingsConstants": "tests.unit.test_config",
    "TestFlextMeltanoSettingsEdgeCases": "tests.unit.test_config",
    "TestFlextMeltanoSettingsEnums": "tests.unit.test_config",
    "TestFlextMeltanoSettingsIntegration": "tests.unit.test_config",
    "TestFlextMeltanoSingerCliTranslatorDbtRun": "tests.unit.test_singer_cli_translator",
    "TestFlextMeltanoSingerCliTranslatorExecuteCommand": "tests.unit.test_singer_cli_translator",
    "TestFlextMeltanoSingerCliTranslatorPipelineRun": "tests.unit.test_singer_cli_translator",
    "TestFlextMeltanoSingerCliTranslatorTapRun": "tests.unit.test_singer_cli_translator",
    "TestFlextMeltanoSingerCliTranslatorTargetRun": "tests.unit.test_singer_cli_translator",
    "TestFlextMeltanoSuccessPaths": "tests.unit.test_api",
    "TestFlextMeltanoTargetAbstractionsComplete": "tests.unit.test_target_abstractions",
    "TestFlextMeltanoTypes": "tests.unit.test_typings",
    "TestFlextMeltanoUtilitiesEnhanced": "tests.unit.test_utilities",
    "TestFlextMeltanoValidatorsComprehensive": "tests.unit.test_validators",
    "TestFlextSingerTypes": "tests.unit.test_singer_types",
    "TestMeltanoProjectModelEnhanced": "tests.unit.test_models",
    "TestModelIntegration": "tests.unit.test_models",
    "TestPluginModelEnhanced": "tests.unit.test_models",
    "TestProjectAdapterIntegration": "tests.unit.test_library_runner",
    "TestServiceArchitecture": "tests.unit.test_services",
    "TestServiceErrorHandling": "tests.unit.test_services",
    "TestServiceFactoryMethods": "tests.unit.test_services",
    "TestServiceGenericMethods": "tests.unit.test_services",
    "TestServiceIntegration": "tests.unit.test_services",
    "TestStreamInfoEnhanced": "tests.unit.test_models",
    "TestTapConfigEnhanced": "tests.unit.test_models",
    "TestTapService": "tests.unit.test_services",
    "TestTargetConfigEnhanced": "tests.unit.test_models",
    "TestTargetService": "tests.unit.test_services",
    "Testc": "tests.unit.test_constants",
    "c": ("flext_core.constants", "FlextConstants"),
    "create_pipeline": "tests.unit.pipeline_cli_managers_tests",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "delete_pipeline": "tests.unit.pipeline_cli_managers_tests",
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "execute_pipeline": "tests.unit.pipeline_cli_managers_tests",
    "get_pipeline_status": "tests.unit.pipeline_cli_managers_tests",
    "h": ("flext_core.handlers", "FlextHandlers"),
    "list_pipelines": "tests.unit.pipeline_cli_managers_tests",
    "logger": "tests.unit.test_target_abstractions",
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "pipeline_cli_managers_tests": "tests.unit.pipeline_cli_managers_tests",
    "pytestmark": "tests.unit.test_api",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "test_api": "tests.unit.test_api",
    "test_cli_integration": "tests.unit.test_cli_integration",
    "test_config": "tests.unit.test_config",
    "test_constants": "tests.unit.test_constants",
    "test_create_pipeline_creates_directory_and_configuration": "tests.unit.pipeline_cli_managers_tests",
    "test_create_pipeline_fails_without_configuration": "tests.unit.pipeline_cli_managers_tests",
    "test_delete_pipeline_removes_configuration_directory": "tests.unit.pipeline_cli_managers_tests",
    "test_execute_pipeline_fails_when_pipeline_execution_is_not_configured": "tests.unit.pipeline_cli_managers_tests",
    "test_execute_pipeline_runs_real_subprocess_contract": "tests.unit.pipeline_cli_managers_tests",
    "test_execution_result": "tests.unit.test_execution_result",
    "test_executors": "tests.unit.test_executors",
    "test_file_managers": "tests.unit.test_file_managers",
    "test_get_pipeline_status_checks_process_state": "tests.unit.pipeline_cli_managers_tests",
    "test_library_runner": "tests.unit.test_library_runner",
    "test_models": "tests.unit.test_models",
    "test_pipeline_manager_lifecycle_commands_delegate_to_real_operations": "tests.unit.pipeline_cli_managers_tests",
    "test_plugin_protocols": "tests.unit.test_plugin_protocols",
    "test_services": "tests.unit.test_services",
    "test_singer_cli_translator": "tests.unit.test_singer_cli_translator",
    "test_singer_types": "tests.unit.test_singer_types",
    "test_tap_abstractions": "tests.unit.test_tap_abstractions",
    "test_target_abstractions": "tests.unit.test_target_abstractions",
    "test_typings": "tests.unit.test_typings",
    "test_utilities": "tests.unit.test_utilities",
    "test_validators": "tests.unit.test_validators",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "LogLevel",
    "TestCliModelConverterWithDbtRunParams",
    "TestCliModelConverterWithPipelineRunParams",
    "TestCliModelConverterWithTapRunParams",
    "TestCliModelConverterWithTargetRunParams",
    "TestDbtProjectModelEnhanced",
    "TestDbtService",
    "TestFlextMeltanoAbstractionsComplete",
    "TestFlextMeltanoCatalogOperations",
    "TestFlextMeltanoErrorHandling",
    "TestFlextMeltanoExecuteMethod",
    "TestFlextMeltanoExecutionResult",
    "TestFlextMeltanoExecutorComplete",
    "TestFlextMeltanoFileManagersComprehensive",
    "TestFlextMeltanoInitialization",
    "TestFlextMeltanoIntegration",
    "TestFlextMeltanoLibraryRunner",
    "TestFlextMeltanoPerformance",
    "TestFlextMeltanoPipelineOperations",
    "TestFlextMeltanoPluginOperations",
    "TestFlextMeltanoPluginProtocols",
    "TestFlextMeltanoProjectOperations",
    "TestFlextMeltanoServiceInitialization",
    "TestFlextMeltanoSettings",
    "TestFlextMeltanoSettingsConstants",
    "TestFlextMeltanoSettingsEdgeCases",
    "TestFlextMeltanoSettingsEnums",
    "TestFlextMeltanoSettingsIntegration",
    "TestFlextMeltanoSingerCliTranslatorDbtRun",
    "TestFlextMeltanoSingerCliTranslatorExecuteCommand",
    "TestFlextMeltanoSingerCliTranslatorPipelineRun",
    "TestFlextMeltanoSingerCliTranslatorTapRun",
    "TestFlextMeltanoSingerCliTranslatorTargetRun",
    "TestFlextMeltanoSuccessPaths",
    "TestFlextMeltanoTargetAbstractionsComplete",
    "TestFlextMeltanoTypes",
    "TestFlextMeltanoUtilitiesEnhanced",
    "TestFlextMeltanoValidatorsComprehensive",
    "TestFlextSingerTypes",
    "TestMeltanoProjectModelEnhanced",
    "TestModelIntegration",
    "TestPluginModelEnhanced",
    "TestProjectAdapterIntegration",
    "TestServiceArchitecture",
    "TestServiceErrorHandling",
    "TestServiceFactoryMethods",
    "TestServiceGenericMethods",
    "TestServiceIntegration",
    "TestStreamInfoEnhanced",
    "TestTapConfigEnhanced",
    "TestTapService",
    "TestTargetConfigEnhanced",
    "TestTargetService",
    "Testc",
    "c",
    "create_pipeline",
    "d",
    "delete_pipeline",
    "e",
    "execute_pipeline",
    "get_pipeline_status",
    "h",
    "list_pipelines",
    "logger",
    "m",
    "p",
    "pipeline_cli_managers_tests",
    "pytestmark",
    "r",
    "s",
    "t",
    "test_api",
    "test_cli_integration",
    "test_config",
    "test_constants",
    "test_create_pipeline_creates_directory_and_configuration",
    "test_create_pipeline_fails_without_configuration",
    "test_delete_pipeline_removes_configuration_directory",
    "test_execute_pipeline_fails_when_pipeline_execution_is_not_configured",
    "test_execute_pipeline_runs_real_subprocess_contract",
    "test_execution_result",
    "test_executors",
    "test_file_managers",
    "test_get_pipeline_status_checks_process_state",
    "test_library_runner",
    "test_models",
    "test_pipeline_manager_lifecycle_commands_delegate_to_real_operations",
    "test_plugin_protocols",
    "test_services",
    "test_singer_cli_translator",
    "test_singer_types",
    "test_tap_abstractions",
    "test_target_abstractions",
    "test_typings",
    "test_utilities",
    "test_validators",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
