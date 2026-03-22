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
    from flext_core import FlextTypes

    from .pipeline_cli_managers_tests import (
        test_create_pipeline_creates_directory_and_configuration,
        test_create_pipeline_fails_without_configuration,
        test_delete_pipeline_removes_configuration_directory,
        test_execute_pipeline_fails_when_pipeline_execution_is_not_configured,
        test_execute_pipeline_runs_real_subprocess_contract,
        test_get_pipeline_status_checks_process_state,
        test_pipeline_manager_lifecycle_commands_delegate_to_real_operations,
    )
    from .test_api import (
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
    from .test_cli_integration import (
        TestCliModelConverterWithDbtRunParams,
        TestCliModelConverterWithPipelineRunParams,
        TestCliModelConverterWithTapRunParams,
        TestCliModelConverterWithTargetRunParams,
    )
    from .test_config import (
        TestFlextMeltanoSettings,
        TestFlextMeltanoSettingsConstants,
        TestFlextMeltanoSettingsEdgeCases,
        TestFlextMeltanoSettingsEnums,
        TestFlextMeltanoSettingsIntegration,
    )
    from .test_constants import Testc
    from .test_execution_result import TestFlextMeltanoExecutionResult, tm
    from .test_executors import TestFlextMeltanoExecutorComplete
    from .test_file_managers import TestFlextMeltanoFileManagersComprehensive
    from .test_library_runner import (
        TestFlextDbtProgrammaticRunner,
        TestFlextMeltanoLibraryRunner,
        TestFlextSingerProtocolManager,
        TestProjectAdapterIntegration,
    )
    from .test_models import (
        TestDbtProjectModelEnhanced,
        TestMeltanoProjectModelEnhanced,
        TestModelIntegration,
        TestPluginModelEnhanced,
        TestStreamInfoEnhanced,
        TestTapConfigEnhanced,
        TestTargetConfigEnhanced,
    )
    from .test_plugin_protocols import TestFlextMeltanoPluginProtocolsUnified, t
    from .test_services import (
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
    from .test_singer_cli_translator import (
        TestFlextMeltanoSingerCliTranslatorDbtRun,
        TestFlextMeltanoSingerCliTranslatorExecuteCommand,
        TestFlextMeltanoSingerCliTranslatorPipelineRun,
        TestFlextMeltanoSingerCliTranslatorTapRun,
        TestFlextMeltanoSingerCliTranslatorTargetRun,
    )
    from .test_singer_types import TestFlextSingerTypes
    from .test_tap_abstractions import TestFlextMeltanoTapAbstractionsComplete
    from .test_target_abstractions import (
        TestFlextMeltanoTargetAbstractionsComplete,
        logger,
    )
    from .test_typings import TestFlextMeltanoTypes
    from .test_utilities import TestFlextMeltanoUtilitiesEnhanced
    from .test_validators import TestFlextMeltanoValidatorsComprehensive

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
    "logger": ("tests.unit.test_target_abstractions", "logger"),
    "pytestmark": ("tests.unit.test_api", "pytestmark"),
    "t": ("tests.unit.test_plugin_protocols", "t"),
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
    "tm": ("tests.unit.test_execution_result", "tm"),
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
    "logger",
    "pytestmark",
    "t",
    "test_create_pipeline_creates_directory_and_configuration",
    "test_create_pipeline_fails_without_configuration",
    "test_delete_pipeline_removes_configuration_directory",
    "test_execute_pipeline_fails_when_pipeline_execution_is_not_configured",
    "test_execute_pipeline_runs_real_subprocess_contract",
    "test_get_pipeline_status_checks_process_state",
    "test_pipeline_manager_lifecycle_commands_delegate_to_real_operations",
    "tm",
]


_LAZY_CACHE: dict[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
