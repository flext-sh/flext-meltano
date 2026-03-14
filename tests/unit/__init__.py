# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Unit tests for flext-meltano package.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from tests.unit.pipeline_cli_managers_tests import (
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
        TestFlextMeltanoDataOperations,
        TestFlextMeltanoDbtOperations,
        TestFlextMeltanoELTPipeline,
        TestFlextMeltanoErrorHandling,
        TestFlextMeltanoExecuteMethod,
        TestFlextMeltanoInitialization,
        TestFlextMeltanoIntegration,
        TestFlextMeltanoPerformance,
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
        TestFlextMeltanoSettings,
        TestFlextMeltanoSettingsConstants,
        TestFlextMeltanoSettingsConstants as c,
        TestFlextMeltanoSettingsEdgeCases,
        TestFlextMeltanoSettingsEnums,
        TestFlextMeltanoSettingsIntegration,
    )
    from tests.unit.test_constants import Testc
    from tests.unit.test_execution_result import (
        TestFlextMeltanoExecutionResult,
        TestFlextMeltanoExecutionResult as r,
    )
    from tests.unit.test_executors import TestFlextMeltanoExecutorComplete
    from tests.unit.test_file_managers import TestFlextMeltanoFileManagersComprehensive
    from tests.unit.test_library_runner import (
        TestFlextDbtProgrammaticRunner,
        TestFlextMeltanoLibraryRunner,
        TestFlextSingerProtocolManager,
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
    from tests.unit.test_plugin_protocols import TestFlextMeltanoPluginProtocolsUnified
    from tests.unit.test_services import (
        TestDbtService,
        TestFlextMeltanoServiceInitialization,
        TestServiceArchitecture,
        TestServiceErrorHandling,
        TestServiceFactoryMethods,
        TestServiceGenericMethods,
        TestServiceIntegration,
        TestTapService,
        TestTapService as s,
        TestTargetService,
    )
    from tests.unit.test_singer_cli_translator import (
        TestFlextMeltanoSingerCliTranslatorDbtRun,
        TestFlextMeltanoSingerCliTranslatorExecuteCommand,
        TestFlextMeltanoSingerCliTranslatorPipelineRun,
        TestFlextMeltanoSingerCliTranslatorTapRun,
        TestFlextMeltanoSingerCliTranslatorTargetRun,
    )
    from tests.unit.test_singer_types import (
        TestFlextSingerTypes,
        TestFlextSingerTypes as t,
    )
    from tests.unit.test_tap_abstractions import TestFlextMeltanoTapAbstractionsComplete
    from tests.unit.test_target_abstractions import (
        TestFlextMeltanoTargetAbstractionsComplete,
        logger,
    )
    from tests.unit.test_typings import TestFlextMeltanoTypes
    from tests.unit.test_utilities import TestFlextMeltanoUtilitiesEnhanced
    from tests.unit.test_validators import TestFlextMeltanoValidatorsComprehensive

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestCliModelConverterWithDbtRunParams": (
        "tests.unit.test_cli_integration",
        "TestCliModelConverterWithDbtRunParams",
    ),
    "TestCliModelConverterWithPipelineRunParams": (
        "tests.unit.test_cli_integration",
        "TestCliModelConverterWithPipelineRunParams",
    ),
    "TestCliModelConverterWithTapRunParams": (
        "tests.unit.test_cli_integration",
        "TestCliModelConverterWithTapRunParams",
    ),
    "TestCliModelConverterWithTargetRunParams": (
        "tests.unit.test_cli_integration",
        "TestCliModelConverterWithTargetRunParams",
    ),
    "TestDbtProjectModelEnhanced": (
        "tests.unit.test_models",
        "TestDbtProjectModelEnhanced",
    ),
    "TestDbtService": ("tests.unit.test_services", "TestDbtService"),
    "TestFlextDbtProgrammaticRunner": (
        "tests.unit.test_library_runner",
        "TestFlextDbtProgrammaticRunner",
    ),
    "TestFlextMeltanoCatalogOperations": (
        "tests.unit.test_api",
        "TestFlextMeltanoCatalogOperations",
    ),
    "TestFlextMeltanoDataOperations": (
        "tests.unit.test_api",
        "TestFlextMeltanoDataOperations",
    ),
    "TestFlextMeltanoDbtOperations": (
        "tests.unit.test_api",
        "TestFlextMeltanoDbtOperations",
    ),
    "TestFlextMeltanoELTPipeline": (
        "tests.unit.test_api",
        "TestFlextMeltanoELTPipeline",
    ),
    "TestFlextMeltanoErrorHandling": (
        "tests.unit.test_api",
        "TestFlextMeltanoErrorHandling",
    ),
    "TestFlextMeltanoExecuteMethod": (
        "tests.unit.test_api",
        "TestFlextMeltanoExecuteMethod",
    ),
    "TestFlextMeltanoExecutionResult": (
        "tests.unit.test_execution_result",
        "TestFlextMeltanoExecutionResult",
    ),
    "TestFlextMeltanoExecutorComplete": (
        "tests.unit.test_executors",
        "TestFlextMeltanoExecutorComplete",
    ),
    "TestFlextMeltanoFileManagersComprehensive": (
        "tests.unit.test_file_managers",
        "TestFlextMeltanoFileManagersComprehensive",
    ),
    "TestFlextMeltanoInitialization": (
        "tests.unit.test_api",
        "TestFlextMeltanoInitialization",
    ),
    "TestFlextMeltanoIntegration": (
        "tests.unit.test_api",
        "TestFlextMeltanoIntegration",
    ),
    "TestFlextMeltanoLibraryRunner": (
        "tests.unit.test_library_runner",
        "TestFlextMeltanoLibraryRunner",
    ),
    "TestFlextMeltanoPerformance": (
        "tests.unit.test_api",
        "TestFlextMeltanoPerformance",
    ),
    "TestFlextMeltanoPluginOperations": (
        "tests.unit.test_api",
        "TestFlextMeltanoPluginOperations",
    ),
    "TestFlextMeltanoPluginProtocolsUnified": (
        "tests.unit.test_plugin_protocols",
        "TestFlextMeltanoPluginProtocolsUnified",
    ),
    "TestFlextMeltanoProjectOperations": (
        "tests.unit.test_api",
        "TestFlextMeltanoProjectOperations",
    ),
    "TestFlextMeltanoServiceInitialization": (
        "tests.unit.test_services",
        "TestFlextMeltanoServiceInitialization",
    ),
    "TestFlextMeltanoSettings": ("tests.unit.test_config", "TestFlextMeltanoSettings"),
    "TestFlextMeltanoSettingsConstants": (
        "tests.unit.test_config",
        "TestFlextMeltanoSettingsConstants",
    ),
    "TestFlextMeltanoSettingsEdgeCases": (
        "tests.unit.test_config",
        "TestFlextMeltanoSettingsEdgeCases",
    ),
    "TestFlextMeltanoSettingsEnums": (
        "tests.unit.test_config",
        "TestFlextMeltanoSettingsEnums",
    ),
    "TestFlextMeltanoSettingsIntegration": (
        "tests.unit.test_config",
        "TestFlextMeltanoSettingsIntegration",
    ),
    "TestFlextMeltanoSingerCliTranslatorDbtRun": (
        "tests.unit.test_singer_cli_translator",
        "TestFlextMeltanoSingerCliTranslatorDbtRun",
    ),
    "TestFlextMeltanoSingerCliTranslatorExecuteCommand": (
        "tests.unit.test_singer_cli_translator",
        "TestFlextMeltanoSingerCliTranslatorExecuteCommand",
    ),
    "TestFlextMeltanoSingerCliTranslatorPipelineRun": (
        "tests.unit.test_singer_cli_translator",
        "TestFlextMeltanoSingerCliTranslatorPipelineRun",
    ),
    "TestFlextMeltanoSingerCliTranslatorTapRun": (
        "tests.unit.test_singer_cli_translator",
        "TestFlextMeltanoSingerCliTranslatorTapRun",
    ),
    "TestFlextMeltanoSingerCliTranslatorTargetRun": (
        "tests.unit.test_singer_cli_translator",
        "TestFlextMeltanoSingerCliTranslatorTargetRun",
    ),
    "TestFlextMeltanoSuccessPaths": (
        "tests.unit.test_api",
        "TestFlextMeltanoSuccessPaths",
    ),
    "TestFlextMeltanoTapAbstractionsComplete": (
        "tests.unit.test_tap_abstractions",
        "TestFlextMeltanoTapAbstractionsComplete",
    ),
    "TestFlextMeltanoTargetAbstractionsComplete": (
        "tests.unit.test_target_abstractions",
        "TestFlextMeltanoTargetAbstractionsComplete",
    ),
    "TestFlextMeltanoTypes": ("tests.unit.test_typings", "TestFlextMeltanoTypes"),
    "TestFlextMeltanoUtilitiesEnhanced": (
        "tests.unit.test_utilities",
        "TestFlextMeltanoUtilitiesEnhanced",
    ),
    "TestFlextMeltanoValidatorsComprehensive": (
        "tests.unit.test_validators",
        "TestFlextMeltanoValidatorsComprehensive",
    ),
    "TestFlextSingerProtocolManager": (
        "tests.unit.test_library_runner",
        "TestFlextSingerProtocolManager",
    ),
    "TestFlextSingerTypes": ("tests.unit.test_singer_types", "TestFlextSingerTypes"),
    "TestMeltanoProjectModelEnhanced": (
        "tests.unit.test_models",
        "TestMeltanoProjectModelEnhanced",
    ),
    "TestModelIntegration": ("tests.unit.test_models", "TestModelIntegration"),
    "TestPluginModelEnhanced": ("tests.unit.test_models", "TestPluginModelEnhanced"),
    "TestProjectAdapterIntegration": (
        "tests.unit.test_library_runner",
        "TestProjectAdapterIntegration",
    ),
    "TestServiceArchitecture": ("tests.unit.test_services", "TestServiceArchitecture"),
    "TestServiceErrorHandling": (
        "tests.unit.test_services",
        "TestServiceErrorHandling",
    ),
    "TestServiceFactoryMethods": (
        "tests.unit.test_services",
        "TestServiceFactoryMethods",
    ),
    "TestServiceGenericMethods": (
        "tests.unit.test_services",
        "TestServiceGenericMethods",
    ),
    "TestServiceIntegration": ("tests.unit.test_services", "TestServiceIntegration"),
    "TestStreamInfoEnhanced": ("tests.unit.test_models", "TestStreamInfoEnhanced"),
    "TestTapConfigEnhanced": ("tests.unit.test_models", "TestTapConfigEnhanced"),
    "TestTapService": ("tests.unit.test_services", "TestTapService"),
    "TestTargetConfigEnhanced": ("tests.unit.test_models", "TestTargetConfigEnhanced"),
    "TestTargetService": ("tests.unit.test_services", "TestTargetService"),
    "Testc": ("tests.unit.test_constants", "Testc"),
    "c": ("tests.unit.test_config", "TestFlextMeltanoSettingsConstants"),
    "logger": ("tests.unit.test_target_abstractions", "logger"),
    "pytestmark": ("tests.unit.test_api", "pytestmark"),
    "r": ("tests.unit.test_execution_result", "TestFlextMeltanoExecutionResult"),
    "s": ("tests.unit.test_services", "TestTapService"),
    "t": ("tests.unit.test_singer_types", "TestFlextSingerTypes"),
    "test_create_pipeline_creates_directory_and_configuration": (
        "tests.unit.pipeline_cli_managers_tests",
        "test_create_pipeline_creates_directory_and_configuration",
    ),
    "test_create_pipeline_fails_without_configuration": (
        "tests.unit.pipeline_cli_managers_tests",
        "test_create_pipeline_fails_without_configuration",
    ),
    "test_delete_pipeline_removes_configuration_directory": (
        "tests.unit.pipeline_cli_managers_tests",
        "test_delete_pipeline_removes_configuration_directory",
    ),
    "test_execute_pipeline_fails_when_pipeline_execution_is_not_configured": (
        "tests.unit.pipeline_cli_managers_tests",
        "test_execute_pipeline_fails_when_pipeline_execution_is_not_configured",
    ),
    "test_execute_pipeline_runs_real_subprocess_contract": (
        "tests.unit.pipeline_cli_managers_tests",
        "test_execute_pipeline_runs_real_subprocess_contract",
    ),
    "test_get_pipeline_status_checks_process_state": (
        "tests.unit.pipeline_cli_managers_tests",
        "test_get_pipeline_status_checks_process_state",
    ),
    "test_pipeline_manager_lifecycle_commands_delegate_to_real_operations": (
        "tests.unit.pipeline_cli_managers_tests",
        "test_pipeline_manager_lifecycle_commands_delegate_to_real_operations",
    ),
}

__all__ = [
    "TestCliModelConverterWithDbtRunParams",
    "TestCliModelConverterWithPipelineRunParams",
    "TestCliModelConverterWithTapRunParams",
    "TestCliModelConverterWithTargetRunParams",
    "TestDbtProjectModelEnhanced",
    "TestDbtService",
    "TestFlextDbtProgrammaticRunner",
    "TestFlextMeltanoCatalogOperations",
    "TestFlextMeltanoDataOperations",
    "TestFlextMeltanoDbtOperations",
    "TestFlextMeltanoELTPipeline",
    "TestFlextMeltanoErrorHandling",
    "TestFlextMeltanoExecuteMethod",
    "TestFlextMeltanoExecutionResult",
    "TestFlextMeltanoExecutorComplete",
    "TestFlextMeltanoFileManagersComprehensive",
    "TestFlextMeltanoInitialization",
    "TestFlextMeltanoIntegration",
    "TestFlextMeltanoLibraryRunner",
    "TestFlextMeltanoPerformance",
    "TestFlextMeltanoPluginOperations",
    "TestFlextMeltanoPluginProtocolsUnified",
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
    "TestFlextMeltanoTapAbstractionsComplete",
    "TestFlextMeltanoTargetAbstractionsComplete",
    "TestFlextMeltanoTypes",
    "TestFlextMeltanoUtilitiesEnhanced",
    "TestFlextMeltanoValidatorsComprehensive",
    "TestFlextSingerProtocolManager",
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
    "logger",
    "pytestmark",
    "r",
    "s",
    "t",
    "test_create_pipeline_creates_directory_and_configuration",
    "test_create_pipeline_fails_without_configuration",
    "test_delete_pipeline_removes_configuration_directory",
    "test_execute_pipeline_fails_when_pipeline_execution_is_not_configured",
    "test_execute_pipeline_runs_real_subprocess_contract",
    "test_get_pipeline_status_checks_process_state",
    "test_pipeline_manager_lifecycle_commands_delegate_to_real_operations",
]


def __getattr__(name: str) -> t.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
