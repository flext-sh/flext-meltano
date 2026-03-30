# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit tests for flext-meltano package.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests.unit import (
        pipeline_cli_managers_tests as pipeline_cli_managers_tests,
        test_api as test_api,
        test_cli_integration as test_cli_integration,
        test_config as test_config,
        test_constants as test_constants,
        test_execution_result as test_execution_result,
        test_executors as test_executors,
        test_file_managers as test_file_managers,
        test_library_runner as test_library_runner,
        test_models as test_models,
        test_plugin_protocols as test_plugin_protocols,
        test_services as test_services,
        test_singer_cli_translator as test_singer_cli_translator,
        test_singer_types as test_singer_types,
        test_tap_abstractions as test_tap_abstractions,
        test_target_abstractions as test_target_abstractions,
        test_typings as test_typings,
        test_utilities as test_utilities,
        test_validators as test_validators,
    )
    from tests.unit.pipeline_cli_managers_tests import (
        create_pipeline as create_pipeline,
        delete_pipeline as delete_pipeline,
        execute_pipeline as execute_pipeline,
        get_pipeline_status as get_pipeline_status,
        list_pipelines as list_pipelines,
        test_create_pipeline_creates_directory_and_configuration as test_create_pipeline_creates_directory_and_configuration,
        test_create_pipeline_fails_without_configuration as test_create_pipeline_fails_without_configuration,
        test_delete_pipeline_removes_configuration_directory as test_delete_pipeline_removes_configuration_directory,
        test_execute_pipeline_fails_when_pipeline_execution_is_not_configured as test_execute_pipeline_fails_when_pipeline_execution_is_not_configured,
        test_execute_pipeline_runs_real_subprocess_contract as test_execute_pipeline_runs_real_subprocess_contract,
        test_get_pipeline_status_checks_process_state as test_get_pipeline_status_checks_process_state,
        test_pipeline_manager_lifecycle_commands_delegate_to_real_operations as test_pipeline_manager_lifecycle_commands_delegate_to_real_operations,
    )
    from tests.unit.test_api import (
        TestFlextMeltanoCatalogOperations as TestFlextMeltanoCatalogOperations,
        TestFlextMeltanoErrorHandling as TestFlextMeltanoErrorHandling,
        TestFlextMeltanoExecuteMethod as TestFlextMeltanoExecuteMethod,
        TestFlextMeltanoInitialization as TestFlextMeltanoInitialization,
        TestFlextMeltanoIntegration as TestFlextMeltanoIntegration,
        TestFlextMeltanoPerformance as TestFlextMeltanoPerformance,
        TestFlextMeltanoPipelineOperations as TestFlextMeltanoPipelineOperations,
        TestFlextMeltanoPluginOperations as TestFlextMeltanoPluginOperations,
        TestFlextMeltanoProjectOperations as TestFlextMeltanoProjectOperations,
        TestFlextMeltanoSuccessPaths as TestFlextMeltanoSuccessPaths,
        pytestmark as pytestmark,
    )
    from tests.unit.test_cli_integration import (
        TestCliModelConverterWithDbtRunParams as TestCliModelConverterWithDbtRunParams,
        TestCliModelConverterWithPipelineRunParams as TestCliModelConverterWithPipelineRunParams,
        TestCliModelConverterWithTapRunParams as TestCliModelConverterWithTapRunParams,
        TestCliModelConverterWithTargetRunParams as TestCliModelConverterWithTargetRunParams,
    )
    from tests.unit.test_config import (
        LogLevel as LogLevel,
        TestFlextMeltanoSettings as TestFlextMeltanoSettings,
        TestFlextMeltanoSettingsConstants as TestFlextMeltanoSettingsConstants,
        TestFlextMeltanoSettingsEdgeCases as TestFlextMeltanoSettingsEdgeCases,
        TestFlextMeltanoSettingsEnums as TestFlextMeltanoSettingsEnums,
        TestFlextMeltanoSettingsIntegration as TestFlextMeltanoSettingsIntegration,
    )
    from tests.unit.test_constants import Testc as Testc
    from tests.unit.test_execution_result import (
        TestFlextMeltanoExecutionResult as TestFlextMeltanoExecutionResult,
    )
    from tests.unit.test_executors import (
        TestFlextMeltanoExecutorComplete as TestFlextMeltanoExecutorComplete,
    )
    from tests.unit.test_file_managers import (
        TestFlextMeltanoFileManagersComprehensive as TestFlextMeltanoFileManagersComprehensive,
    )
    from tests.unit.test_library_runner import (
        TestFlextMeltanoLibraryRunner as TestFlextMeltanoLibraryRunner,
        TestProjectAdapterIntegration as TestProjectAdapterIntegration,
    )
    from tests.unit.test_models import (
        TestDbtProjectModelEnhanced as TestDbtProjectModelEnhanced,
        TestMeltanoProjectModelEnhanced as TestMeltanoProjectModelEnhanced,
        TestModelIntegration as TestModelIntegration,
        TestPluginModelEnhanced as TestPluginModelEnhanced,
        TestStreamInfoEnhanced as TestStreamInfoEnhanced,
        TestTapConfigEnhanced as TestTapConfigEnhanced,
        TestTargetConfigEnhanced as TestTargetConfigEnhanced,
    )
    from tests.unit.test_plugin_protocols import (
        TestFlextMeltanoPluginProtocols as TestFlextMeltanoPluginProtocols,
    )
    from tests.unit.test_services import (
        TestDbtService as TestDbtService,
        TestFlextMeltanoServiceInitialization as TestFlextMeltanoServiceInitialization,
        TestServiceArchitecture as TestServiceArchitecture,
        TestServiceErrorHandling as TestServiceErrorHandling,
        TestServiceFactoryMethods as TestServiceFactoryMethods,
        TestServiceGenericMethods as TestServiceGenericMethods,
        TestServiceIntegration as TestServiceIntegration,
        TestTapService as TestTapService,
        TestTargetService as TestTargetService,
    )
    from tests.unit.test_singer_cli_translator import (
        TestFlextMeltanoSingerCliTranslatorDbtRun as TestFlextMeltanoSingerCliTranslatorDbtRun,
        TestFlextMeltanoSingerCliTranslatorExecuteCommand as TestFlextMeltanoSingerCliTranslatorExecuteCommand,
        TestFlextMeltanoSingerCliTranslatorPipelineRun as TestFlextMeltanoSingerCliTranslatorPipelineRun,
        TestFlextMeltanoSingerCliTranslatorTapRun as TestFlextMeltanoSingerCliTranslatorTapRun,
        TestFlextMeltanoSingerCliTranslatorTargetRun as TestFlextMeltanoSingerCliTranslatorTargetRun,
    )
    from tests.unit.test_singer_types import (
        TestFlextSingerTypes as TestFlextSingerTypes,
    )
    from tests.unit.test_tap_abstractions import (
        TestFlextMeltanoAbstractionsComplete as TestFlextMeltanoAbstractionsComplete,
    )
    from tests.unit.test_target_abstractions import (
        TestFlextMeltanoTargetAbstractionsComplete as TestFlextMeltanoTargetAbstractionsComplete,
        logger as logger,
    )
    from tests.unit.test_typings import TestFlextMeltanoTypes as TestFlextMeltanoTypes
    from tests.unit.test_utilities import (
        TestFlextMeltanoUtilitiesEnhanced as TestFlextMeltanoUtilitiesEnhanced,
    )
    from tests.unit.test_validators import (
        TestFlextMeltanoValidatorsComprehensive as TestFlextMeltanoValidatorsComprehensive,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "LogLevel": ["tests.unit.test_config", "LogLevel"],
    "TestCliModelConverterWithDbtRunParams": [
        "tests.unit.test_cli_integration",
        "TestCliModelConverterWithDbtRunParams",
    ],
    "TestCliModelConverterWithPipelineRunParams": [
        "tests.unit.test_cli_integration",
        "TestCliModelConverterWithPipelineRunParams",
    ],
    "TestCliModelConverterWithTapRunParams": [
        "tests.unit.test_cli_integration",
        "TestCliModelConverterWithTapRunParams",
    ],
    "TestCliModelConverterWithTargetRunParams": [
        "tests.unit.test_cli_integration",
        "TestCliModelConverterWithTargetRunParams",
    ],
    "TestDbtProjectModelEnhanced": [
        "tests.unit.test_models",
        "TestDbtProjectModelEnhanced",
    ],
    "TestDbtService": ["tests.unit.test_services", "TestDbtService"],
    "TestFlextMeltanoAbstractionsComplete": [
        "tests.unit.test_tap_abstractions",
        "TestFlextMeltanoAbstractionsComplete",
    ],
    "TestFlextMeltanoCatalogOperations": [
        "tests.unit.test_api",
        "TestFlextMeltanoCatalogOperations",
    ],
    "TestFlextMeltanoErrorHandling": [
        "tests.unit.test_api",
        "TestFlextMeltanoErrorHandling",
    ],
    "TestFlextMeltanoExecuteMethod": [
        "tests.unit.test_api",
        "TestFlextMeltanoExecuteMethod",
    ],
    "TestFlextMeltanoExecutionResult": [
        "tests.unit.test_execution_result",
        "TestFlextMeltanoExecutionResult",
    ],
    "TestFlextMeltanoExecutorComplete": [
        "tests.unit.test_executors",
        "TestFlextMeltanoExecutorComplete",
    ],
    "TestFlextMeltanoFileManagersComprehensive": [
        "tests.unit.test_file_managers",
        "TestFlextMeltanoFileManagersComprehensive",
    ],
    "TestFlextMeltanoInitialization": [
        "tests.unit.test_api",
        "TestFlextMeltanoInitialization",
    ],
    "TestFlextMeltanoIntegration": [
        "tests.unit.test_api",
        "TestFlextMeltanoIntegration",
    ],
    "TestFlextMeltanoLibraryRunner": [
        "tests.unit.test_library_runner",
        "TestFlextMeltanoLibraryRunner",
    ],
    "TestFlextMeltanoPerformance": [
        "tests.unit.test_api",
        "TestFlextMeltanoPerformance",
    ],
    "TestFlextMeltanoPipelineOperations": [
        "tests.unit.test_api",
        "TestFlextMeltanoPipelineOperations",
    ],
    "TestFlextMeltanoPluginOperations": [
        "tests.unit.test_api",
        "TestFlextMeltanoPluginOperations",
    ],
    "TestFlextMeltanoPluginProtocols": [
        "tests.unit.test_plugin_protocols",
        "TestFlextMeltanoPluginProtocols",
    ],
    "TestFlextMeltanoProjectOperations": [
        "tests.unit.test_api",
        "TestFlextMeltanoProjectOperations",
    ],
    "TestFlextMeltanoServiceInitialization": [
        "tests.unit.test_services",
        "TestFlextMeltanoServiceInitialization",
    ],
    "TestFlextMeltanoSettings": ["tests.unit.test_config", "TestFlextMeltanoSettings"],
    "TestFlextMeltanoSettingsConstants": [
        "tests.unit.test_config",
        "TestFlextMeltanoSettingsConstants",
    ],
    "TestFlextMeltanoSettingsEdgeCases": [
        "tests.unit.test_config",
        "TestFlextMeltanoSettingsEdgeCases",
    ],
    "TestFlextMeltanoSettingsEnums": [
        "tests.unit.test_config",
        "TestFlextMeltanoSettingsEnums",
    ],
    "TestFlextMeltanoSettingsIntegration": [
        "tests.unit.test_config",
        "TestFlextMeltanoSettingsIntegration",
    ],
    "TestFlextMeltanoSingerCliTranslatorDbtRun": [
        "tests.unit.test_singer_cli_translator",
        "TestFlextMeltanoSingerCliTranslatorDbtRun",
    ],
    "TestFlextMeltanoSingerCliTranslatorExecuteCommand": [
        "tests.unit.test_singer_cli_translator",
        "TestFlextMeltanoSingerCliTranslatorExecuteCommand",
    ],
    "TestFlextMeltanoSingerCliTranslatorPipelineRun": [
        "tests.unit.test_singer_cli_translator",
        "TestFlextMeltanoSingerCliTranslatorPipelineRun",
    ],
    "TestFlextMeltanoSingerCliTranslatorTapRun": [
        "tests.unit.test_singer_cli_translator",
        "TestFlextMeltanoSingerCliTranslatorTapRun",
    ],
    "TestFlextMeltanoSingerCliTranslatorTargetRun": [
        "tests.unit.test_singer_cli_translator",
        "TestFlextMeltanoSingerCliTranslatorTargetRun",
    ],
    "TestFlextMeltanoSuccessPaths": [
        "tests.unit.test_api",
        "TestFlextMeltanoSuccessPaths",
    ],
    "TestFlextMeltanoTargetAbstractionsComplete": [
        "tests.unit.test_target_abstractions",
        "TestFlextMeltanoTargetAbstractionsComplete",
    ],
    "TestFlextMeltanoTypes": ["tests.unit.test_typings", "TestFlextMeltanoTypes"],
    "TestFlextMeltanoUtilitiesEnhanced": [
        "tests.unit.test_utilities",
        "TestFlextMeltanoUtilitiesEnhanced",
    ],
    "TestFlextMeltanoValidatorsComprehensive": [
        "tests.unit.test_validators",
        "TestFlextMeltanoValidatorsComprehensive",
    ],
    "TestFlextSingerTypes": ["tests.unit.test_singer_types", "TestFlextSingerTypes"],
    "TestMeltanoProjectModelEnhanced": [
        "tests.unit.test_models",
        "TestMeltanoProjectModelEnhanced",
    ],
    "TestModelIntegration": ["tests.unit.test_models", "TestModelIntegration"],
    "TestPluginModelEnhanced": ["tests.unit.test_models", "TestPluginModelEnhanced"],
    "TestProjectAdapterIntegration": [
        "tests.unit.test_library_runner",
        "TestProjectAdapterIntegration",
    ],
    "TestServiceArchitecture": ["tests.unit.test_services", "TestServiceArchitecture"],
    "TestServiceErrorHandling": [
        "tests.unit.test_services",
        "TestServiceErrorHandling",
    ],
    "TestServiceFactoryMethods": [
        "tests.unit.test_services",
        "TestServiceFactoryMethods",
    ],
    "TestServiceGenericMethods": [
        "tests.unit.test_services",
        "TestServiceGenericMethods",
    ],
    "TestServiceIntegration": ["tests.unit.test_services", "TestServiceIntegration"],
    "TestStreamInfoEnhanced": ["tests.unit.test_models", "TestStreamInfoEnhanced"],
    "TestTapConfigEnhanced": ["tests.unit.test_models", "TestTapConfigEnhanced"],
    "TestTapService": ["tests.unit.test_services", "TestTapService"],
    "TestTargetConfigEnhanced": ["tests.unit.test_models", "TestTargetConfigEnhanced"],
    "TestTargetService": ["tests.unit.test_services", "TestTargetService"],
    "Testc": ["tests.unit.test_constants", "Testc"],
    "create_pipeline": ["tests.unit.pipeline_cli_managers_tests", "create_pipeline"],
    "delete_pipeline": ["tests.unit.pipeline_cli_managers_tests", "delete_pipeline"],
    "execute_pipeline": ["tests.unit.pipeline_cli_managers_tests", "execute_pipeline"],
    "get_pipeline_status": [
        "tests.unit.pipeline_cli_managers_tests",
        "get_pipeline_status",
    ],
    "list_pipelines": ["tests.unit.pipeline_cli_managers_tests", "list_pipelines"],
    "logger": ["tests.unit.test_target_abstractions", "logger"],
    "pipeline_cli_managers_tests": ["tests.unit.pipeline_cli_managers_tests", ""],
    "pytestmark": ["tests.unit.test_api", "pytestmark"],
    "test_api": ["tests.unit.test_api", ""],
    "test_cli_integration": ["tests.unit.test_cli_integration", ""],
    "test_config": ["tests.unit.test_config", ""],
    "test_constants": ["tests.unit.test_constants", ""],
    "test_create_pipeline_creates_directory_and_configuration": [
        "tests.unit.pipeline_cli_managers_tests",
        "test_create_pipeline_creates_directory_and_configuration",
    ],
    "test_create_pipeline_fails_without_configuration": [
        "tests.unit.pipeline_cli_managers_tests",
        "test_create_pipeline_fails_without_configuration",
    ],
    "test_delete_pipeline_removes_configuration_directory": [
        "tests.unit.pipeline_cli_managers_tests",
        "test_delete_pipeline_removes_configuration_directory",
    ],
    "test_execute_pipeline_fails_when_pipeline_execution_is_not_configured": [
        "tests.unit.pipeline_cli_managers_tests",
        "test_execute_pipeline_fails_when_pipeline_execution_is_not_configured",
    ],
    "test_execute_pipeline_runs_real_subprocess_contract": [
        "tests.unit.pipeline_cli_managers_tests",
        "test_execute_pipeline_runs_real_subprocess_contract",
    ],
    "test_execution_result": ["tests.unit.test_execution_result", ""],
    "test_executors": ["tests.unit.test_executors", ""],
    "test_file_managers": ["tests.unit.test_file_managers", ""],
    "test_get_pipeline_status_checks_process_state": [
        "tests.unit.pipeline_cli_managers_tests",
        "test_get_pipeline_status_checks_process_state",
    ],
    "test_library_runner": ["tests.unit.test_library_runner", ""],
    "test_models": ["tests.unit.test_models", ""],
    "test_pipeline_manager_lifecycle_commands_delegate_to_real_operations": [
        "tests.unit.pipeline_cli_managers_tests",
        "test_pipeline_manager_lifecycle_commands_delegate_to_real_operations",
    ],
    "test_plugin_protocols": ["tests.unit.test_plugin_protocols", ""],
    "test_services": ["tests.unit.test_services", ""],
    "test_singer_cli_translator": ["tests.unit.test_singer_cli_translator", ""],
    "test_singer_types": ["tests.unit.test_singer_types", ""],
    "test_tap_abstractions": ["tests.unit.test_tap_abstractions", ""],
    "test_target_abstractions": ["tests.unit.test_target_abstractions", ""],
    "test_typings": ["tests.unit.test_typings", ""],
    "test_utilities": ["tests.unit.test_utilities", ""],
    "test_validators": ["tests.unit.test_validators", ""],
}

_EXPORTS: Sequence[str] = [
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
    "create_pipeline",
    "delete_pipeline",
    "execute_pipeline",
    "get_pipeline_status",
    "list_pipelines",
    "logger",
    "pipeline_cli_managers_tests",
    "pytestmark",
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
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
