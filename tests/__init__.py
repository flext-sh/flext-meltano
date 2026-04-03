# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_meltano import (
        conftest,
        constants,
        docker_test_manager,
        helpers,
        integration,
        models,
        pipeline_cli_managers_tests,
        protocols,
        test_api,
        test_cli_integration,
        test_config,
        test_constants,
        test_docker_integration,
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
        typings,
        unit,
        utilities,
    )
    from flext_meltano.conftest import (
        MockCliResult,
        job_run_config,
        meltano_cli_runner,
        meltano_invoke_args,
        meltano_project,
        meltano_service,
        meltano_yml,
        meltano_yml_config,
        mock_meltano_service,
        mock_singer_tap,
        mock_singer_target,
        pipeline_execution_config,
        postgres_service,
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
    from flext_meltano.constants import (
        FlextMeltanoTestConstants,
        FlextMeltanoTestConstants as c,
    )
    from flext_meltano.helpers import ContainerManager, docker_manager, docker_services
    from flext_meltano.integration import TestDockerIntegration, psycopg2, redis
    from flext_meltano.models import FlextMeltanoTestModels, FlextMeltanoTestModels as m
    from flext_meltano.protocols import (
        FlextMeltanoTestProtocols,
        FlextMeltanoTestProtocols as p,
    )
    from flext_meltano.typings import FlextMeltanoTestTypes, FlextMeltanoTestTypes as t
    from flext_meltano.unit import (
        LogLevel,
        Testc,
        TestCliModelConverterWithTapRunParams,
        TestFlextMeltanoExecutionResult,
        TestFlextMeltanoExecutorComplete,
        TestFlextMeltanoFileManagersComprehensive,
        TestFlextMeltanoInitialization,
        TestFlextMeltanoLibraryRunner,
        TestFlextMeltanoPerformance,
        TestFlextMeltanoPluginProtocols,
        TestFlextMeltanoServiceInitialization,
        TestFlextMeltanoSingerCliTranslatorTapRun,
        TestFlextMeltanoSuccessPaths,
        TestFlextMeltanoTargetAbstractionsComplete,
        TestFlextMeltanoTypes,
        TestFlextMeltanoUtilitiesEnhanced,
        TestFlextMeltanoValidatorsComprehensive,
        TestFlextSingerTypes,
        TestTapConfigEnhanced,
        config_json,
        create_pipeline,
        create_result,
        delete_pipeline,
        delete_result,
        execute_pipeline,
        get_pipeline_status,
        list_pipelines,
        list_result,
        logger,
        manager,
        mock_command_result,
        pytestmark,
        result,
        return_value,
        run_result,
        test_get_pipeline_status_checks_process_state,
        values,
    )
    from flext_meltano.utilities import (
        FlextMeltanoTestUtilities,
        FlextMeltanoTestUtilities as u,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    (
        "flext_meltano.helpers",
        "flext_meltano.integration",
        "flext_meltano.unit",
    ),
    {
        "FlextMeltanoTestConstants": "flext_meltano.constants",
        "FlextMeltanoTestModels": "flext_meltano.models",
        "FlextMeltanoTestProtocols": "flext_meltano.protocols",
        "FlextMeltanoTestTypes": "flext_meltano.typings",
        "FlextMeltanoTestUtilities": "flext_meltano.utilities",
        "MockCliResult": "flext_meltano.conftest",
        "c": ("flext_meltano.constants", "FlextMeltanoTestConstants"),
        "conftest": "flext_meltano.conftest",
        "constants": "flext_meltano.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "docker_test_manager": "flext_meltano.docker_test_manager",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "helpers": "flext_meltano.helpers",
        "integration": "flext_meltano.integration",
        "job_run_config": "flext_meltano.conftest",
        "m": ("flext_meltano.models", "FlextMeltanoTestModels"),
        "meltano_cli_runner": "flext_meltano.conftest",
        "meltano_invoke_args": "flext_meltano.conftest",
        "meltano_project": "flext_meltano.conftest",
        "meltano_service": "flext_meltano.conftest",
        "meltano_yml": "flext_meltano.conftest",
        "meltano_yml_config": "flext_meltano.conftest",
        "mock_meltano_service": "flext_meltano.conftest",
        "mock_singer_tap": "flext_meltano.conftest",
        "mock_singer_target": "flext_meltano.conftest",
        "models": "flext_meltano.models",
        "p": ("flext_meltano.protocols", "FlextMeltanoTestProtocols"),
        "pipeline_cli_managers_tests": "flext_meltano.pipeline_cli_managers_tests",
        "pipeline_execution_config": "flext_meltano.conftest",
        "postgres_service": "flext_meltano.conftest",
        "protocols": "flext_meltano.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "redis_service": "flext_meltano.conftest",
        "s": ("flext_core.service", "FlextService"),
        "sample_csv_data": "flext_meltano.conftest",
        "sample_schedule_config": "flext_meltano.conftest",
        "set_test_environment": "flext_meltano.conftest",
        "singer_records": "flext_meltano.conftest",
        "singer_schema": "flext_meltano.conftest",
        "singer_state": "flext_meltano.conftest",
        "t": ("flext_meltano.typings", "FlextMeltanoTestTypes"),
        "tap_csv_config": "flext_meltano.conftest",
        "target_csv_config": "flext_meltano.conftest",
        "test_api": "flext_meltano.test_api",
        "test_cli_integration": "flext_meltano.test_cli_integration",
        "test_config": "flext_meltano.test_config",
        "test_constants": "flext_meltano.test_constants",
        "test_docker_integration": "flext_meltano.test_docker_integration",
        "test_environment_config": "flext_meltano.conftest",
        "test_execution_result": "flext_meltano.test_execution_result",
        "test_executors": "flext_meltano.test_executors",
        "test_file_managers": "flext_meltano.test_file_managers",
        "test_library_runner": "flext_meltano.test_library_runner",
        "test_meltano_project_dir": "flext_meltano.conftest",
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
        "typings": "flext_meltano.typings",
        "u": ("flext_meltano.utilities", "FlextMeltanoTestUtilities"),
        "unit": "flext_meltano.unit",
        "utilities": "flext_meltano.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
