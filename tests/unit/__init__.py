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
    import tests.unit.test_cli_small_managers as _tests_unit_test_cli_small_managers
    from tests.unit.test_cli_integration import (
        TestCliModelConversionWithDbtRunParams,
        TestCliModelConversionWithPipelineRunParams,
        TestCliModelConversionWithTapRunParams,
        TestCliModelConversionWithTargetRunParams,
    )

    test_cli_small_managers = _tests_unit_test_cli_small_managers
    import tests.unit.test_constants as _tests_unit_test_constants
    from tests.unit.test_cli_small_managers import (
        test_dbt_manager_fails_for_unsupported_operation,
        test_dbt_manager_routes_supported_operation_to_service,
        test_plugin_manager_routes_list_and_install,
        test_singer_manager_returns_failure_for_placeholder_tap_and_target_ops,
        test_status_manager_routes_show_health_and_version,
    )

    test_constants = _tests_unit_test_constants
    import tests.unit.test_execution_result as _tests_unit_test_execution_result
    from tests.unit.test_constants import Testc

    test_execution_result = _tests_unit_test_execution_result
    import tests.unit.test_executors as _tests_unit_test_executors
    from tests.unit.test_execution_result import TestFlextMeltanoExecutionResult

    test_executors = _tests_unit_test_executors
    import tests.unit.test_library_runner as _tests_unit_test_library_runner
    from tests.unit.test_executors import TestFlextMeltanoExecutorComplete

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
    import tests.unit.test_singer_sdk_adapter as _tests_unit_test_singer_sdk_adapter
    from tests.unit.test_singer_cli_translator import (
        TestFlextMeltanoSingerCliTranslatorDbtRun,
        TestFlextMeltanoSingerCliTranslatorExecuteCommand,
        TestFlextMeltanoSingerCliTranslatorPipelineRun,
        TestFlextMeltanoSingerCliTranslatorTapRun,
        TestFlextMeltanoSingerCliTranslatorTargetRun,
    )

    test_singer_sdk_adapter = _tests_unit_test_singer_sdk_adapter
    import tests.unit.test_singer_types as _tests_unit_test_singer_types
    from tests.unit.test_singer_sdk_adapter import (
        test_adapter_delegates_sync,
        test_adapter_exposes_config_and_streams,
        test_adapter_normalizes_successful_cli_exit_code,
        test_adapter_normalizes_system_exit,
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
    import tests.unit.test_validators as _tests_unit_test_validators
    from tests.unit.test_typings import TestFlextMeltanoTypes

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
    "TestCliModelConversionWithDbtRunParams": (
        "tests.unit.test_cli_integration",
        "TestCliModelConversionWithDbtRunParams",
    ),
    "TestCliModelConversionWithPipelineRunParams": (
        "tests.unit.test_cli_integration",
        "TestCliModelConversionWithPipelineRunParams",
    ),
    "TestCliModelConversionWithTapRunParams": (
        "tests.unit.test_cli_integration",
        "TestCliModelConversionWithTapRunParams",
    ),
    "TestCliModelConversionWithTargetRunParams": (
        "tests.unit.test_cli_integration",
        "TestCliModelConversionWithTargetRunParams",
    ),
    "TestDbtProjectModelEnhanced": (
        "tests.unit.test_models",
        "TestDbtProjectModelEnhanced",
    ),
    "TestDbtService": ("tests.unit.test_services", "TestDbtService"),
    "TestFlextMeltanoAbstractionsComplete": (
        "tests.unit.test_tap_abstractions",
        "TestFlextMeltanoAbstractionsComplete",
    ),
    "TestFlextMeltanoCatalogOperations": (
        "tests.unit.test_api",
        "TestFlextMeltanoCatalogOperations",
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
    "TestFlextMeltanoPipelineOperations": (
        "tests.unit.test_api",
        "TestFlextMeltanoPipelineOperations",
    ),
    "TestFlextMeltanoPluginOperations": (
        "tests.unit.test_api",
        "TestFlextMeltanoPluginOperations",
    ),
    "TestFlextMeltanoPluginProtocols": (
        "tests.unit.test_plugin_protocols",
        "TestFlextMeltanoPluginProtocols",
    ),
    "TestFlextMeltanoProjectOperations": (
        "tests.unit.test_api",
        "TestFlextMeltanoProjectOperations",
    ),
    "TestFlextMeltanoServiceInitialization": (
        "tests.unit.test_services",
        "TestFlextMeltanoServiceInitialization",
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
    "TestFlextMeltanoTargetAbstractionsComplete": (
        "tests.unit.test_target_abstractions",
        "TestFlextMeltanoTargetAbstractionsComplete",
    ),
    "TestFlextMeltanoTypes": ("tests.unit.test_typings", "TestFlextMeltanoTypes"),
    "TestFlextMeltanoValidatorsComprehensive": (
        "tests.unit.test_validators",
        "TestFlextMeltanoValidatorsComprehensive",
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
    "c": ("flext_core.constants", "FlextConstants"),
    "create_pipeline": ("tests.unit.pipeline_cli_managers_tests", "create_pipeline"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "delete_pipeline": ("tests.unit.pipeline_cli_managers_tests", "delete_pipeline"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "execute_pipeline": ("tests.unit.pipeline_cli_managers_tests", "execute_pipeline"),
    "get_pipeline_status": (
        "tests.unit.pipeline_cli_managers_tests",
        "get_pipeline_status",
    ),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "list_pipelines": ("tests.unit.pipeline_cli_managers_tests", "list_pipelines"),
    "logger": ("tests.unit.test_target_abstractions", "logger"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "pipeline_cli_managers_tests": "tests.unit.pipeline_cli_managers_tests",
    "pytestmark": ("tests.unit.test_api", "pytestmark"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "test_adapter_delegates_sync": (
        "tests.unit.test_singer_sdk_adapter",
        "test_adapter_delegates_sync",
    ),
    "test_adapter_exposes_config_and_streams": (
        "tests.unit.test_singer_sdk_adapter",
        "test_adapter_exposes_config_and_streams",
    ),
    "test_adapter_normalizes_successful_cli_exit_code": (
        "tests.unit.test_singer_sdk_adapter",
        "test_adapter_normalizes_successful_cli_exit_code",
    ),
    "test_adapter_normalizes_system_exit": (
        "tests.unit.test_singer_sdk_adapter",
        "test_adapter_normalizes_system_exit",
    ),
    "test_api": "tests.unit.test_api",
    "test_cli_integration": "tests.unit.test_cli_integration",
    "test_cli_small_managers": "tests.unit.test_cli_small_managers",
    "test_constants": "tests.unit.test_constants",
    "test_create_pipeline_creates_directory_and_configuration": (
        "tests.unit.pipeline_cli_managers_tests",
        "test_create_pipeline_creates_directory_and_configuration",
    ),
    "test_create_pipeline_fails_without_configuration": (
        "tests.unit.pipeline_cli_managers_tests",
        "test_create_pipeline_fails_without_configuration",
    ),
    "test_dbt_manager_fails_for_unsupported_operation": (
        "tests.unit.test_cli_small_managers",
        "test_dbt_manager_fails_for_unsupported_operation",
    ),
    "test_dbt_manager_routes_supported_operation_to_service": (
        "tests.unit.test_cli_small_managers",
        "test_dbt_manager_routes_supported_operation_to_service",
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
    "test_execution_result": "tests.unit.test_execution_result",
    "test_executors": "tests.unit.test_executors",
    "test_get_pipeline_status_checks_process_state": (
        "tests.unit.pipeline_cli_managers_tests",
        "test_get_pipeline_status_checks_process_state",
    ),
    "test_library_runner": "tests.unit.test_library_runner",
    "test_models": "tests.unit.test_models",
    "test_pipeline_manager_lifecycle_commands_delegate_to_real_operations": (
        "tests.unit.pipeline_cli_managers_tests",
        "test_pipeline_manager_lifecycle_commands_delegate_to_real_operations",
    ),
    "test_plugin_manager_routes_list_and_install": (
        "tests.unit.test_cli_small_managers",
        "test_plugin_manager_routes_list_and_install",
    ),
    "test_plugin_protocols": "tests.unit.test_plugin_protocols",
    "test_services": "tests.unit.test_services",
    "test_singer_cli_translator": "tests.unit.test_singer_cli_translator",
    "test_singer_manager_returns_failure_for_placeholder_tap_and_target_ops": (
        "tests.unit.test_cli_small_managers",
        "test_singer_manager_returns_failure_for_placeholder_tap_and_target_ops",
    ),
    "test_singer_sdk_adapter": "tests.unit.test_singer_sdk_adapter",
    "test_singer_types": "tests.unit.test_singer_types",
    "test_status_manager_routes_show_health_and_version": (
        "tests.unit.test_cli_small_managers",
        "test_status_manager_routes_show_health_and_version",
    ),
    "test_tap_abstractions": "tests.unit.test_tap_abstractions",
    "test_target_abstractions": "tests.unit.test_target_abstractions",
    "test_typings": "tests.unit.test_typings",
    "test_validators": "tests.unit.test_validators",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "TestCliModelConversionWithDbtRunParams",
    "TestCliModelConversionWithPipelineRunParams",
    "TestCliModelConversionWithTapRunParams",
    "TestCliModelConversionWithTargetRunParams",
    "TestDbtProjectModelEnhanced",
    "TestDbtService",
    "TestFlextMeltanoAbstractionsComplete",
    "TestFlextMeltanoCatalogOperations",
    "TestFlextMeltanoErrorHandling",
    "TestFlextMeltanoExecuteMethod",
    "TestFlextMeltanoExecutionResult",
    "TestFlextMeltanoExecutorComplete",
    "TestFlextMeltanoInitialization",
    "TestFlextMeltanoIntegration",
    "TestFlextMeltanoLibraryRunner",
    "TestFlextMeltanoPerformance",
    "TestFlextMeltanoPipelineOperations",
    "TestFlextMeltanoPluginOperations",
    "TestFlextMeltanoPluginProtocols",
    "TestFlextMeltanoProjectOperations",
    "TestFlextMeltanoServiceInitialization",
    "TestFlextMeltanoSingerCliTranslatorDbtRun",
    "TestFlextMeltanoSingerCliTranslatorExecuteCommand",
    "TestFlextMeltanoSingerCliTranslatorPipelineRun",
    "TestFlextMeltanoSingerCliTranslatorTapRun",
    "TestFlextMeltanoSingerCliTranslatorTargetRun",
    "TestFlextMeltanoSuccessPaths",
    "TestFlextMeltanoTargetAbstractionsComplete",
    "TestFlextMeltanoTypes",
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
    "test_adapter_delegates_sync",
    "test_adapter_exposes_config_and_streams",
    "test_adapter_normalizes_successful_cli_exit_code",
    "test_adapter_normalizes_system_exit",
    "test_api",
    "test_cli_integration",
    "test_cli_small_managers",
    "test_constants",
    "test_create_pipeline_creates_directory_and_configuration",
    "test_create_pipeline_fails_without_configuration",
    "test_dbt_manager_fails_for_unsupported_operation",
    "test_dbt_manager_routes_supported_operation_to_service",
    "test_delete_pipeline_removes_configuration_directory",
    "test_execute_pipeline_fails_when_pipeline_execution_is_not_configured",
    "test_execute_pipeline_runs_real_subprocess_contract",
    "test_execution_result",
    "test_executors",
    "test_get_pipeline_status_checks_process_state",
    "test_library_runner",
    "test_models",
    "test_pipeline_manager_lifecycle_commands_delegate_to_real_operations",
    "test_plugin_manager_routes_list_and_install",
    "test_plugin_protocols",
    "test_services",
    "test_singer_cli_translator",
    "test_singer_manager_returns_failure_for_placeholder_tap_and_target_ops",
    "test_singer_sdk_adapter",
    "test_singer_types",
    "test_status_manager_routes_show_health_and_version",
    "test_tap_abstractions",
    "test_target_abstractions",
    "test_typings",
    "test_validators",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
