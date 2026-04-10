"""FLEXT Meltano base constants — project metadata, paths, network, plugins."""

from __future__ import annotations

from typing import Final

from pydantic import ValidationError


class FlextMeltanoConstantsBase:
    """Base meltano constants: metadata, versions, paths, network, plugins.

    All constants are flat with descriptive prefixes to explain their usage.
    """

    CONSTANTS_VERSION: Final[str] = "1.0.0"
    PROJECT_PREFIX: Final[str] = "flext-meltano"
    PROJECT_NAME: Final[str] = "FLEXT Meltano"
    FLEXT_MELTANO_VERSION: Final[str] = "0.9.0"
    PROJECT_FILE_DBT: Final[str] = "dbt_project.yml"
    COMMAND_RUN_DBT: Final[str] = "dbt run"
    COMMAND_TEST: Final[str] = "dbt test"
    DEFAULT_VARIANT: Final[str] = "meltano"

    # Metadata
    METADATA_APPLICATION_NAME: Final[str] = "flext-pipeline"
    METADATA_APPLICATION_DESCRIPTION: Final[str] = (
        "FLEXT Generic Data Pipeline Framework"
    )
    METADATA_APPLICATION_AUTHOR: Final[str] = "FLEXT Team"
    METADATA_APPLICATION_LICENSE: Final[str] = "MIT"
    METADATA_CREATED_BY: Final[str] = "flext-pipeline"
    METADATA_DEFAULT_ENVIRONMENTS: Final[tuple[str, ...]] = ("dev", "staging", "prod")

    # Versions
    VERSION_MELTANO_REQUIRED: Final[str] = "3.9.1"
    VERSION_SINGER_SDK_REQUIRED: Final[str] = "0.48.0"
    VERSION_DBT_REQUIRED: Final[str] = "1.10.5"

    SDK_VERSION_REQUIRED: Final[str] = VERSION_SINGER_SDK_REQUIRED
    VERSION_REQUIRED_DBT: Final[str] = VERSION_DBT_REQUIRED

    # Paths
    PATH_PROJECT_FILE: Final[str] = "meltano.yml"
    PATH_MELTANO_PROJECT_FILE: Final[str] = "meltano.yml"
    PATH_STATE_DIR: Final[str] = ".pipeline"
    PATH_LOGS_DIR: Final[str] = "logs"
    PATH_OUTPUT_DIR: Final[str] = "output"
    PATH_TRANSFORM_DIR: Final[str] = "transform"
    PATH_VENV_DIR: Final[str] = ".meltano/python"

    # Commands
    CMD_BINARY: Final[str] = "meltano"
    CMD_ALL_OPTION: Final[str] = "--all"
    CMD_CWD_OPTION: Final[str] = "--cwd"
    CMD_ENVIRONMENT_OPTION: Final[str] = "--environment"
    CMD_HELP_OPTION: Final[str] = "--help"
    CMD_LIST_OPTION: Final[str] = "--list"
    CMD_MODELS_OPTION: Final[str] = "--models"
    CMD_NO_ENVIRONMENT_OPTION: Final[str] = "--no-environment"
    CMD_SELECT_OPTION: Final[str] = "--select"
    CMD_SHORT_HELP_OPTION: Final[str] = "-h"
    CMD_VERSION_OPTION: Final[str] = "--version"
    CMD_ADD: Final[str] = "add"
    CMD_ELT: Final[str] = "elt"
    CMD_INIT: Final[str] = "init"
    CMD_INSTALL: Final[str] = "install"
    CMD_INVOKE: Final[str] = "invoke"
    CMD_RUN: Final[str] = "run"
    CMD_SELECT: Final[str] = "select"
    CMD_PIPELINE: Final[str] = "pipeline"

    # Network
    NETWORK_MELTANO_DEFAULT_TIMEOUT: Final[int] = 300
    NETWORK_DEFAULT_TIMEOUT: Final[int] = 30
    NETWORK_DISCOVERY_TIMEOUT: Final[int] = 60
    NETWORK_REQUEST_TIMEOUT: Final[int] = 60
    NETWORK_CONNECTION_TIMEOUT: Final[int] = 30
    NETWORK_BUFFER_SIZE: Final[int] = 8192
    NETWORK_MAX_PARALLEL_STREAMS: Final[int] = 4

    # DatabasePorts
    DB_PORT_POSTGRES: Final[int] = 5432
    DB_PORT_MYSQL: Final[int] = 3306
    DB_PORT_ORACLE: Final[int] = 1521
    DB_PORT_HIGH_MEMORY_THRESHOLD: Final[int] = 1073741824

    # Plugin
    PLUGIN_CONFIG_VERSION: Final[int] = 1
    PLUGIN_DBT_DEFAULT_NAME: Final[str] = "dbt-postgres"
    PLUGIN_DISCOVERY_FILENAME: Final[str] = "catalog.json"
    PLUGIN_STATE_FILENAME: Final[str] = "state.json"
    PLUGIN_DEFAULT_VARIANT: Final[str] = "meltanolabs"
    PLUGIN_HUB_URL: Final[str] = "https://hub.meltano.com"
    PREFIX_TAP: Final[str] = "tap"
    PREFIX_TARGET: Final[str] = "target"
    PREFIX_DBT: Final[str] = "dbt"
    PUBLIC_FACTORY_TAP: Final[str] = "Tap"
    PUBLIC_FACTORY_TARGET: Final[str] = "Target"
    PUBLIC_FACTORY_DBT: Final[str] = "Dbt"
    PUBLIC_FACTORY_NAMES: Final[frozenset[str]] = frozenset({
        PUBLIC_FACTORY_TAP,
        PUBLIC_FACTORY_TARGET,
        PUBLIC_FACTORY_DBT,
    })
    PLUGIN_INSTALLATION_TIMEOUT: Final[int] = 300
    PLUGIN_MIN_TARGET_PLUGIN_NAME_LENGTH: Final[int] = 8
    PLUGIN_MIN_TAP_PLUGIN_NAME_LENGTH: Final[int] = 5

    # EnvironmentVariables
    ENV_VAR_PROJECT_ROOT: Final[str] = "MELTANO_PROJECT_ROOT"
    ENV_VAR_ENVIRONMENT: Final[str] = "MELTANO_ENVIRONMENT"
    ENV_VAR_LOG_LEVEL: Final[str] = "MELTANO_LOG_LEVEL"

    OPERATION_ERRORS: Final[tuple[type[Exception], ...]] = (
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
    )

    # Singer
    SINGER_MESSAGE_TYPE_RECORD: Final[str] = "RECORD"
    SINGER_MESSAGE_TYPE_SCHEMA: Final[str] = "SCHEMA"
    SINGER_MESSAGE_TYPE_STATE: Final[str] = "STATE"
    SINGER_MESSAGE_TYPE_ACTIVATE_VERSION: Final[str] = "ACTIVATE_VERSION"
    SINGER_MESSAGE_TYPE_METRIC: Final[str] = "METRIC"

    SINGER_SAFE_EXCEPTIONS: Final[tuple[type[Exception], ...]] = (
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
        RuntimeError,
        ImportError,
        ValidationError,
    )

    # Dbt
    DBT_PROJECT_FILE: Final[str] = "dbt_project.yml"
    DBT_PROFILES_FILE: Final[str] = "profiles.yml"
    DBT_MANIFEST_FILE: Final[str] = "manifest.json"
    DBT_COMMAND_RUN: Final[str] = "run"
    DBT_COMMAND_TEST: Final[str] = "test"
    DBT_COMMAND_BUILD: Final[str] = "build"
    DBT_COMMAND_COMPILE: Final[str] = "compile"
    DBT_FRESHNESS_ERROR_AFTER_HOURS: Final[int] = 24
    DBT_FRESHNESS_WARN_AFTER_HOURS: Final[int] = 12
    DBT_MATERIALIZATION_TABLE: Final[str] = "table"
    DBT_MATERIALIZATION_VIEW: Final[str] = "view"
    DBT_MATERIALIZATION_INCREMENTAL: Final[str] = "incremental"

    # ModelValidation
    VALIDATION_MATURITY_MATURE_ENV_COUNT: Final[int] = 3
    VALIDATION_MATURITY_DEVELOPING_ENV_COUNT: Final[int] = 2
    VALIDATION_COMPLEXITY_MINIMAL_SETTINGS: Final[int] = 0
    VALIDATION_COMPLEXITY_SIMPLE_MAX_SETTINGS: Final[int] = 5
    VALIDATION_COMPLEXITY_MODERATE_MAX_SETTINGS: Final[int] = 15
    VALIDATION_STRUCTURE_SIMPLE_MAX_PATHS: Final[int] = 5
    VALIDATION_STRUCTURE_MODERATE_MAX_PATHS: Final[int] = 10
    VALIDATION_VERSION_PARTS_COUNT: Final[int] = 3
    VALIDATION_TAP_SIMPLE_CONFIG_THRESHOLD: Final[int] = 3
    VALIDATION_TAP_MODERATE_CONFIG_THRESHOLD: Final[int] = 8
    VALIDATION_TARGET_HIGH_EFFICIENCY_THRESHOLD: Final[int] = 1000
    VALIDATION_TARGET_MEDIUM_EFFICIENCY_THRESHOLD: Final[int] = 100
    VALIDATION_DBT_SIMPLE_EXECUTION_THRESHOLD: Final[int] = 5
    VALIDATION_DBT_MODERATE_EXECUTION_THRESHOLD: Final[int] = 20
    VALIDATION_EXECUTION_HIGH_PERFORMANCE_THRESHOLD: Final[int] = 1000
    VALIDATION_EXECUTION_GOOD_PERFORMANCE_THRESHOLD: Final[int] = 100
    VALIDATION_EXECUTION_MODERATE_PERFORMANCE_THRESHOLD: Final[int] = 10
    VALIDATION_MAX_WORKERS_THRESHOLD: Final[int] = 50
