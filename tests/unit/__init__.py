# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit tests for flext-meltano package.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from tests.unit import (
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
    from tests.unit.test_cli_integration import (
        TestCliModelConverterWithDbtRunParams,
        TestCliModelConverterWithPipelineRunParams,
        TestCliModelConverterWithTapRunParams,
        TestCliModelConverterWithTargetRunParams,
    )
    from tests.unit.test_config import (
        LogLevel,
        TestFlextMeltanoSettings,
        TestFlextMeltanoSettingsConstants,
        TestFlextMeltanoSettingsEdgeCases,
        TestFlextMeltanoSettingsEnums,
        TestFlextMeltanoSettingsIntegration,
    )
    from tests.unit.test_constants import Testc
    from tests.unit.test_execution_result import TestFlextMeltanoExecutionResult
    from tests.unit.test_executors import TestFlextMeltanoExecutorComplete
    from tests.unit.test_file_managers import TestFlextMeltanoFileManagersComprehensive
    from tests.unit.test_library_runner import (
        TestFlextMeltanoLibraryRunner,
        TestProjectAdapterIntegration,
    )
    from tests.unit.test_models import (
        TestDbtProjectModelEnhanced,
        TestMeltanoProjectModelEnhanced,
        TestModelIntegration,
        TestPluginModelEnhanced,
        TestStreamInfoEnhanced,
        TestTapConfigEnhanced,
        TestTargetConfigEnhanced,
    )
    from tests.unit.test_plugin_protocols import TestFlextMeltanoPluginProtocols
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
    from tests.unit.test_singer_cli_translator import (
        TestFlextMeltanoSingerCliTranslatorDbtRun,
        TestFlextMeltanoSingerCliTranslatorExecuteCommand,
        TestFlextMeltanoSingerCliTranslatorPipelineRun,
        TestFlextMeltanoSingerCliTranslatorTapRun,
        TestFlextMeltanoSingerCliTranslatorTargetRun,
    )
    from tests.unit.test_singer_types import TestFlextSingerTypes
    from tests.unit.test_tap_abstractions import TestFlextMeltanoAbstractionsComplete
    from tests.unit.test_target_abstractions import (
        TestFlextMeltanoTargetAbstractionsComplete,
        logger,
    )
    from tests.unit.test_typings import TestFlextMeltanoTypes
    from tests.unit.test_utilities import TestFlextMeltanoUtilitiesEnhanced
    from tests.unit.test_validators import TestFlextMeltanoValidatorsComprehensive

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
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
    "create_pipeline": "tests.unit.pipeline_cli_managers_tests",
    "delete_pipeline": "tests.unit.pipeline_cli_managers_tests",
    "execute_pipeline": "tests.unit.pipeline_cli_managers_tests",
    "get_pipeline_status": "tests.unit.pipeline_cli_managers_tests",
    "list_pipelines": "tests.unit.pipeline_cli_managers_tests",
    "logger": "tests.unit.test_target_abstractions",
    "pipeline_cli_managers_tests": "tests.unit.pipeline_cli_managers_tests",
    "pytestmark": "tests.unit.test_api",
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
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
