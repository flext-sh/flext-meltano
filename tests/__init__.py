# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x

    from . import helpers as helpers, integration as integration, unit as unit
    from .conftest import (
        CliRunner,
        MockCliResult,
        MockCliRunner,
        MockMeltanoService,
        MockSingerTap,
        MockSingerTarget,
        job_run_config,
        meltano_cli_runner,
        meltano_invoke_args,
        meltano_project,
        meltano_service,
        meltano_yml_config,
        mock_meltano_service,
        mock_singer_tap,
        mock_singer_target,
        pipeline_execution_config,
        postgres_service,
        pytest_configure,
        redis_service,
        sample_csv_data,
        sample_schedule_config,
        set_test_environment,
        singer_records,
        singer_schema,
        singer_state,
        tap_csv_config,
        target_csv_config,
        test_environment_config,
        test_meltano_project_dir,
    )
    from .constants import FlextMeltanoTestConstants, FlextMeltanoTestConstants as c
    from .helpers.docker_test_manager import (
        ContainerManager,
        Tk,
        docker_manager,
        docker_services,
    )
    from .integration.test_docker_integration import TestDockerIntegration
    from .models import FlextMeltanoTestModels, FlextMeltanoTestModels as m
    from .protocols import FlextMeltanoTestProtocols, FlextMeltanoTestProtocols as p
    from .typings import FlextMeltanoTestTypes, FlextMeltanoTestTypes as t
    from .unit.pipeline_cli_managers_tests import (
        test_create_pipeline_creates_directory_and_configuration,
        test_create_pipeline_fails_without_configuration,
        test_delete_pipeline_removes_configuration_directory,
        test_execute_pipeline_fails_when_pipeline_execution_is_not_configured,
        test_execute_pipeline_runs_real_subprocess_contract,
        test_get_pipeline_status_checks_process_state,
        test_pipeline_manager_lifecycle_commands_delegate_to_real_operations,
    )
    from .unit.test_api import (
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
    from .unit.test_cli_integration import (
        TestCliModelConverterWithDbtRunParams,
        TestCliModelConverterWithPipelineRunParams,
        TestCliModelConverterWithTapRunParams,
        TestCliModelConverterWithTargetRunParams,
    )
    from .unit.test_config import (
        TestFlextMeltanoSettings,
        TestFlextMeltanoSettingsConstants,
        TestFlextMeltanoSettingsEdgeCases,
        TestFlextMeltanoSettingsEnums,
        TestFlextMeltanoSettingsIntegration,
    )
    from .unit.test_constants import Testc
    from .unit.test_execution_result import TestFlextMeltanoExecutionResult, tm
    from .unit.test_executors import TestFlextMeltanoExecutorComplete
    from .unit.test_file_managers import TestFlextMeltanoFileManagersComprehensive
    from .unit.test_library_runner import (
        TestFlextDbtProgrammaticRunner,
        TestFlextMeltanoLibraryRunner,
        TestFlextSingerProtocolManager,
        TestProjectAdapterIntegration,
    )
    from .unit.test_models import (
        TestDbtProjectModelEnhanced,
        TestMeltanoProjectModelEnhanced,
        TestModelIntegration,
        TestPluginModelEnhanced,
        TestStreamInfoEnhanced,
        TestTapConfigEnhanced,
        TestTargetConfigEnhanced,
    )
    from .unit.test_plugin_protocols import TestFlextMeltanoPluginProtocolsUnified
    from .unit.test_services import (
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
    from .unit.test_singer_cli_translator import (
        TestFlextMeltanoSingerCliTranslatorDbtRun,
        TestFlextMeltanoSingerCliTranslatorExecuteCommand,
        TestFlextMeltanoSingerCliTranslatorPipelineRun,
        TestFlextMeltanoSingerCliTranslatorTapRun,
        TestFlextMeltanoSingerCliTranslatorTargetRun,
    )
    from .unit.test_singer_types import TestFlextSingerTypes
    from .unit.test_tap_abstractions import TestFlextMeltanoTapAbstractionsComplete
    from .unit.test_target_abstractions import (
        TestFlextMeltanoTargetAbstractionsComplete,
        logger,
    )
    from .unit.test_typings import TestFlextMeltanoTypes
    from .unit.test_utilities import TestFlextMeltanoUtilitiesEnhanced
    from .unit.test_validators import TestFlextMeltanoValidatorsComprehensive
    from .utilities import FlextMeltanoTestUtilities, FlextMeltanoTestUtilities as u

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "CliRunner": ("tests.conftest", "CliRunner"),
    "ContainerManager": ("tests.helpers.docker_test_manager", "ContainerManager"),
    "FlextMeltanoTestConstants": ("tests.constants", "FlextMeltanoTestConstants"),
    "FlextMeltanoTestModels": ("tests.models", "FlextMeltanoTestModels"),
    "FlextMeltanoTestProtocols": ("tests.protocols", "FlextMeltanoTestProtocols"),
    "FlextMeltanoTestTypes": ("tests.typings", "FlextMeltanoTestTypes"),
    "FlextMeltanoTestUtilities": ("tests.utilities", "FlextMeltanoTestUtilities"),
    "MockCliResult": ("tests.conftest", "MockCliResult"),
    "MockCliRunner": ("tests.conftest", "MockCliRunner"),
    "MockMeltanoService": ("tests.conftest", "MockMeltanoService"),
    "MockSingerTap": ("tests.conftest", "MockSingerTap"),
    "MockSingerTarget": ("tests.conftest", "MockSingerTarget"),
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
    "TestDockerIntegration": (
        "tests.integration.test_docker_integration",
        "TestDockerIntegration",
    ),
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
    "Tk": ("tests.helpers.docker_test_manager", "Tk"),
    "c": ("tests.constants", "FlextMeltanoTestConstants"),
    "d": ("flext_tests", "d"),
    "docker_manager": ("tests.helpers.docker_test_manager", "docker_manager"),
    "docker_services": ("tests.helpers.docker_test_manager", "docker_services"),
    "e": ("flext_tests", "e"),
    "h": ("flext_tests", "h"),
    "helpers": ("tests.helpers", ""),
    "integration": ("tests.integration", ""),
    "job_run_config": ("tests.conftest", "job_run_config"),
    "logger": ("tests.unit.test_target_abstractions", "logger"),
    "m": ("tests.models", "FlextMeltanoTestModels"),
    "meltano_cli_runner": ("tests.conftest", "meltano_cli_runner"),
    "meltano_invoke_args": ("tests.conftest", "meltano_invoke_args"),
    "meltano_project": ("tests.conftest", "meltano_project"),
    "meltano_service": ("tests.conftest", "meltano_service"),
    "meltano_yml_config": ("tests.conftest", "meltano_yml_config"),
    "mock_meltano_service": ("tests.conftest", "mock_meltano_service"),
    "mock_singer_tap": ("tests.conftest", "mock_singer_tap"),
    "mock_singer_target": ("tests.conftest", "mock_singer_target"),
    "p": ("tests.protocols", "FlextMeltanoTestProtocols"),
    "pipeline_execution_config": ("tests.conftest", "pipeline_execution_config"),
    "postgres_service": ("tests.conftest", "postgres_service"),
    "pytest_configure": ("tests.conftest", "pytest_configure"),
    "pytestmark": ("tests.unit.test_api", "pytestmark"),
    "r": ("flext_tests", "r"),
    "redis_service": ("tests.conftest", "redis_service"),
    "s": ("flext_tests", "s"),
    "sample_csv_data": ("tests.conftest", "sample_csv_data"),
    "sample_schedule_config": ("tests.conftest", "sample_schedule_config"),
    "set_test_environment": ("tests.conftest", "set_test_environment"),
    "singer_records": ("tests.conftest", "singer_records"),
    "singer_schema": ("tests.conftest", "singer_schema"),
    "singer_state": ("tests.conftest", "singer_state"),
    "t": ("tests.typings", "FlextMeltanoTestTypes"),
    "tap_csv_config": ("tests.conftest", "tap_csv_config"),
    "target_csv_config": ("tests.conftest", "target_csv_config"),
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
    "test_environment_config": ("tests.conftest", "test_environment_config"),
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
    "test_meltano_project_dir": ("tests.conftest", "test_meltano_project_dir"),
    "test_pipeline_manager_lifecycle_commands_delegate_to_real_operations": (
        "tests.unit.pipeline_cli_managers_tests",
        "test_pipeline_manager_lifecycle_commands_delegate_to_real_operations",
    ),
    "tm": ("tests.unit.test_execution_result", "tm"),
    "u": ("tests.utilities", "FlextMeltanoTestUtilities"),
    "unit": ("tests.unit", ""),
    "x": ("flext_tests", "x"),
}

__all__ = [
    "CliRunner",
    "ContainerManager",
    "FlextMeltanoTestConstants",
    "FlextMeltanoTestModels",
    "FlextMeltanoTestProtocols",
    "FlextMeltanoTestTypes",
    "FlextMeltanoTestUtilities",
    "MockCliResult",
    "MockCliRunner",
    "MockMeltanoService",
    "MockSingerTap",
    "MockSingerTarget",
    "TestCliModelConverterWithDbtRunParams",
    "TestCliModelConverterWithPipelineRunParams",
    "TestCliModelConverterWithTapRunParams",
    "TestCliModelConverterWithTargetRunParams",
    "TestDbtProjectModelEnhanced",
    "TestDbtService",
    "TestDockerIntegration",
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
    "Tk",
    "c",
    "d",
    "docker_manager",
    "docker_services",
    "e",
    "h",
    "helpers",
    "integration",
    "job_run_config",
    "logger",
    "m",
    "meltano_cli_runner",
    "meltano_invoke_args",
    "meltano_project",
    "meltano_service",
    "meltano_yml_config",
    "mock_meltano_service",
    "mock_singer_tap",
    "mock_singer_target",
    "p",
    "pipeline_execution_config",
    "postgres_service",
    "pytest_configure",
    "pytestmark",
    "r",
    "redis_service",
    "s",
    "sample_csv_data",
    "sample_schedule_config",
    "set_test_environment",
    "singer_records",
    "singer_schema",
    "singer_state",
    "t",
    "tap_csv_config",
    "target_csv_config",
    "test_create_pipeline_creates_directory_and_configuration",
    "test_create_pipeline_fails_without_configuration",
    "test_delete_pipeline_removes_configuration_directory",
    "test_environment_config",
    "test_execute_pipeline_fails_when_pipeline_execution_is_not_configured",
    "test_execute_pipeline_runs_real_subprocess_contract",
    "test_get_pipeline_status_checks_process_state",
    "test_meltano_project_dir",
    "test_pipeline_manager_lifecycle_commands_delegate_to_real_operations",
    "tm",
    "u",
    "unit",
    "x",
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
