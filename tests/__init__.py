# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_core.mixins import FlextMixins as x
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s
from tests.conftest import (
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
from tests.constants import (
    FlextMeltanoTestConstants,
    FlextMeltanoTestConstants as c,
)
from tests.helpers.docker_test_manager import (
    ContainerManager,
    Tk,
    docker_manager,
    docker_services,
)
from tests.integration.test_docker_integration import (
    TestDockerIntegration,
    psycopg2,
    redis,
)
from tests.models import FlextMeltanoTestModels, FlextMeltanoTestModels as m
from tests.protocols import (
    FlextMeltanoTestProtocols,
    FlextMeltanoTestProtocols as p,
)
from tests.typings import FlextMeltanoTestTypes, FlextMeltanoTestTypes as t
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
from tests.utilities import (
    FlextMeltanoTestUtilities,
    FlextMeltanoTestUtilities as u,
)

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.helpers as _tests_helpers

    helpers = _tests_helpers
    import tests.helpers.docker_test_manager as _tests_helpers_docker_test_manager

    docker_test_manager = _tests_helpers_docker_test_manager
    import tests.integration as _tests_integration

    integration = _tests_integration
    import tests.integration.test_docker_integration as _tests_integration_test_docker_integration

    test_docker_integration = _tests_integration_test_docker_integration
    import tests.models as _tests_models

    models = _tests_models
    import tests.protocols as _tests_protocols

    protocols = _tests_protocols
    import tests.typings as _tests_typings

    typings = _tests_typings
    import tests.unit as _tests_unit

    unit = _tests_unit
    import tests.unit.pipeline_cli_managers_tests as _tests_unit_pipeline_cli_managers_tests

    pipeline_cli_managers_tests = _tests_unit_pipeline_cli_managers_tests
    import tests.unit.test_api as _tests_unit_test_api

    test_api = _tests_unit_test_api
    import tests.unit.test_cli_integration as _tests_unit_test_cli_integration

    test_cli_integration = _tests_unit_test_cli_integration
    import tests.unit.test_config as _tests_unit_test_config

    test_config = _tests_unit_test_config
    import tests.unit.test_constants as _tests_unit_test_constants

    test_constants = _tests_unit_test_constants
    import tests.unit.test_execution_result as _tests_unit_test_execution_result

    test_execution_result = _tests_unit_test_execution_result
    import tests.unit.test_executors as _tests_unit_test_executors

    test_executors = _tests_unit_test_executors
    import tests.unit.test_file_managers as _tests_unit_test_file_managers

    test_file_managers = _tests_unit_test_file_managers
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
    import tests.unit.test_singer_types as _tests_unit_test_singer_types

    test_singer_types = _tests_unit_test_singer_types
    import tests.unit.test_tap_abstractions as _tests_unit_test_tap_abstractions

    test_tap_abstractions = _tests_unit_test_tap_abstractions
    import tests.unit.test_target_abstractions as _tests_unit_test_target_abstractions

    test_target_abstractions = _tests_unit_test_target_abstractions
    import tests.unit.test_typings as _tests_unit_test_typings

    test_typings = _tests_unit_test_typings
    import tests.unit.test_utilities as _tests_unit_test_utilities

    test_utilities = _tests_unit_test_utilities
    import tests.unit.test_validators as _tests_unit_test_validators

    test_validators = _tests_unit_test_validators
    import tests.utilities as _tests_utilities

    utilities = _tests_utilities

    _ = (
        CliRunner,
        ContainerManager,
        FlextMeltanoTestConstants,
        FlextMeltanoTestModels,
        FlextMeltanoTestProtocols,
        FlextMeltanoTestTypes,
        FlextMeltanoTestUtilities,
        LogLevel,
        MockCliResult,
        MockCliRunner,
        MockMeltanoService,
        MockSingerTap,
        MockSingerTarget,
        TestCliModelConverterWithDbtRunParams,
        TestCliModelConverterWithPipelineRunParams,
        TestCliModelConverterWithTapRunParams,
        TestCliModelConverterWithTargetRunParams,
        TestDbtProjectModelEnhanced,
        TestDbtService,
        TestDockerIntegration,
        TestFlextMeltanoAbstractionsComplete,
        TestFlextMeltanoCatalogOperations,
        TestFlextMeltanoErrorHandling,
        TestFlextMeltanoExecuteMethod,
        TestFlextMeltanoExecutionResult,
        TestFlextMeltanoExecutorComplete,
        TestFlextMeltanoFileManagersComprehensive,
        TestFlextMeltanoInitialization,
        TestFlextMeltanoIntegration,
        TestFlextMeltanoLibraryRunner,
        TestFlextMeltanoPerformance,
        TestFlextMeltanoPipelineOperations,
        TestFlextMeltanoPluginOperations,
        TestFlextMeltanoPluginProtocols,
        TestFlextMeltanoProjectOperations,
        TestFlextMeltanoServiceInitialization,
        TestFlextMeltanoSettings,
        TestFlextMeltanoSettingsConstants,
        TestFlextMeltanoSettingsEdgeCases,
        TestFlextMeltanoSettingsEnums,
        TestFlextMeltanoSettingsIntegration,
        TestFlextMeltanoSingerCliTranslatorDbtRun,
        TestFlextMeltanoSingerCliTranslatorExecuteCommand,
        TestFlextMeltanoSingerCliTranslatorPipelineRun,
        TestFlextMeltanoSingerCliTranslatorTapRun,
        TestFlextMeltanoSingerCliTranslatorTargetRun,
        TestFlextMeltanoSuccessPaths,
        TestFlextMeltanoTargetAbstractionsComplete,
        TestFlextMeltanoTypes,
        TestFlextMeltanoUtilitiesEnhanced,
        TestFlextMeltanoValidatorsComprehensive,
        TestFlextSingerTypes,
        TestMeltanoProjectModelEnhanced,
        TestModelIntegration,
        TestPluginModelEnhanced,
        TestProjectAdapterIntegration,
        TestServiceArchitecture,
        TestServiceErrorHandling,
        TestServiceFactoryMethods,
        TestServiceGenericMethods,
        TestServiceIntegration,
        TestStreamInfoEnhanced,
        TestTapConfigEnhanced,
        TestTapService,
        TestTargetConfigEnhanced,
        TestTargetService,
        Testc,
        Tk,
        c,
        conftest,
        constants,
        create_pipeline,
        d,
        delete_pipeline,
        docker_manager,
        docker_services,
        docker_test_manager,
        e,
        execute_pipeline,
        get_pipeline_status,
        h,
        helpers,
        integration,
        job_run_config,
        list_pipelines,
        logger,
        m,
        meltano_cli_runner,
        meltano_invoke_args,
        meltano_project,
        meltano_service,
        meltano_yml_config,
        mock_meltano_service,
        mock_singer_tap,
        mock_singer_target,
        models,
        p,
        pipeline_cli_managers_tests,
        pipeline_execution_config,
        postgres_service,
        protocols,
        psycopg2,
        pytest_configure,
        pytestmark,
        r,
        redis,
        redis_service,
        s,
        sample_csv_data,
        sample_schedule_config,
        set_test_environment,
        singer_records,
        singer_schema,
        singer_state,
        t,
        tap_csv_config,
        target_csv_config,
        test_api,
        test_cli_integration,
        test_config,
        test_constants,
        test_create_pipeline_creates_directory_and_configuration,
        test_create_pipeline_fails_without_configuration,
        test_delete_pipeline_removes_configuration_directory,
        test_docker_integration,
        test_environment_config,
        test_execute_pipeline_fails_when_pipeline_execution_is_not_configured,
        test_execute_pipeline_runs_real_subprocess_contract,
        test_execution_result,
        test_executors,
        test_file_managers,
        test_get_pipeline_status_checks_process_state,
        test_library_runner,
        test_meltano_project_dir,
        test_models,
        test_pipeline_manager_lifecycle_commands_delegate_to_real_operations,
        test_plugin_protocols,
        test_services,
        test_singer_cli_translator,
        test_singer_types,
        test_tap_abstractions,
        test_target_abstractions,
        test_typings,
        test_utilities,
        test_validators,
        typings,
        u,
        unit,
        utilities,
        x,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "tests.helpers",
        "tests.integration",
        "tests.unit",
    ),
    {
        "CliRunner": "tests.conftest",
        "FlextMeltanoTestConstants": "tests.constants",
        "FlextMeltanoTestModels": "tests.models",
        "FlextMeltanoTestProtocols": "tests.protocols",
        "FlextMeltanoTestTypes": "tests.typings",
        "FlextMeltanoTestUtilities": "tests.utilities",
        "MockCliResult": "tests.conftest",
        "MockCliRunner": "tests.conftest",
        "MockMeltanoService": "tests.conftest",
        "MockSingerTap": "tests.conftest",
        "MockSingerTarget": "tests.conftest",
        "c": ("tests.constants", "FlextMeltanoTestConstants"),
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "helpers": "tests.helpers",
        "integration": "tests.integration",
        "job_run_config": "tests.conftest",
        "m": ("tests.models", "FlextMeltanoTestModels"),
        "meltano_cli_runner": "tests.conftest",
        "meltano_invoke_args": "tests.conftest",
        "meltano_project": "tests.conftest",
        "meltano_service": "tests.conftest",
        "meltano_yml_config": "tests.conftest",
        "mock_meltano_service": "tests.conftest",
        "mock_singer_tap": "tests.conftest",
        "mock_singer_target": "tests.conftest",
        "models": "tests.models",
        "p": ("tests.protocols", "FlextMeltanoTestProtocols"),
        "pipeline_execution_config": "tests.conftest",
        "postgres_service": "tests.conftest",
        "protocols": "tests.protocols",
        "pytest_configure": "tests.conftest",
        "r": ("flext_core.result", "FlextResult"),
        "redis_service": "tests.conftest",
        "s": ("flext_core.service", "FlextService"),
        "sample_csv_data": "tests.conftest",
        "sample_schedule_config": "tests.conftest",
        "set_test_environment": "tests.conftest",
        "singer_records": "tests.conftest",
        "singer_schema": "tests.conftest",
        "singer_state": "tests.conftest",
        "t": ("tests.typings", "FlextMeltanoTestTypes"),
        "tap_csv_config": "tests.conftest",
        "target_csv_config": "tests.conftest",
        "test_environment_config": "tests.conftest",
        "test_meltano_project_dir": "tests.conftest",
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextMeltanoTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)

__all__ = [
    "CliRunner",
    "ContainerManager",
    "FlextMeltanoTestConstants",
    "FlextMeltanoTestModels",
    "FlextMeltanoTestProtocols",
    "FlextMeltanoTestTypes",
    "FlextMeltanoTestUtilities",
    "LogLevel",
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
    "Tk",
    "c",
    "conftest",
    "constants",
    "create_pipeline",
    "d",
    "delete_pipeline",
    "docker_manager",
    "docker_services",
    "docker_test_manager",
    "e",
    "execute_pipeline",
    "get_pipeline_status",
    "h",
    "helpers",
    "integration",
    "job_run_config",
    "list_pipelines",
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
    "models",
    "p",
    "pipeline_cli_managers_tests",
    "pipeline_execution_config",
    "postgres_service",
    "protocols",
    "psycopg2",
    "pytest_configure",
    "pytestmark",
    "r",
    "redis",
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
    "test_api",
    "test_cli_integration",
    "test_config",
    "test_constants",
    "test_create_pipeline_creates_directory_and_configuration",
    "test_create_pipeline_fails_without_configuration",
    "test_delete_pipeline_removes_configuration_directory",
    "test_docker_integration",
    "test_environment_config",
    "test_execute_pipeline_fails_when_pipeline_execution_is_not_configured",
    "test_execute_pipeline_runs_real_subprocess_contract",
    "test_execution_result",
    "test_executors",
    "test_file_managers",
    "test_get_pipeline_status_checks_process_state",
    "test_library_runner",
    "test_meltano_project_dir",
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
    "typings",
    "u",
    "unit",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
