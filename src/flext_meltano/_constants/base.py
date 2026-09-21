"""FLEXT Meltano base constants — project metadata, paths, network, plugins."""

from __future__ import annotations

from typing import ClassVar

from flext_cli import c

from .enums import FlextMeltanoConstantsEnums


class FlextMeltanoConstantsBase:
    """Base meltano constants: metadata, versions, paths, network, plugins.

    All constants are flat with descriptive prefixes to explain their usage.
    """

    CONSTANTS_VERSION: ClassVar[str] = "1.0.0"
    DBT_BINARY: ClassVar[str] = "dbt"
    DEFAULT_VARIANT: ClassVar[str] = "meltano"
    FLEXT_MELTANO_VERSION: ClassVar[str] = "0.9.0"
    PROJECT_NAME: ClassVar[str] = "FLEXT Meltano"
    PROJECT_PREFIX: ClassVar[str] = "flext-meltano"

    # Metadata
    METADATA_APPLICATION_DESCRIPTION: ClassVar[str] = (
        "FLEXT Generic Data Pipeline Framework"
    )
    METADATA_APPLICATION_NAME: ClassVar[str] = "flext-pipeline"
    METADATA_DEFAULT_ENVIRONMENTS: ClassVar[
        tuple[FlextMeltanoConstantsEnums.ProjectEnvironment, ...]
    ] = (
        FlextMeltanoConstantsEnums.ProjectEnvironment.DEV,
        FlextMeltanoConstantsEnums.ProjectEnvironment.STAGING,
        FlextMeltanoConstantsEnums.ProjectEnvironment.PROD,
    )

    # Versions
    VERSION_MELTANO_REQUIRED: ClassVar[str] = "3.9.1"
    VERSION_MELTANO_REQUIREMENT: ClassVar[str] = f">={VERSION_MELTANO_REQUIRED}"
    VERSION_SINGER_SDK_REQUIRED: ClassVar[str] = "0.48.0"

    SDK_VERSION_REQUIRED: ClassVar[str] = VERSION_SINGER_SDK_REQUIRED

    # Paths
    PATH_MELTANO_PROJECT_FILE: ClassVar[str] = "meltano.yml"
    PATH_PROJECT_FILE: ClassVar[str] = PATH_MELTANO_PROJECT_FILE
    PATH_CONFIG_DIR: ClassVar[str] = ".meltano"
    PATH_STATE_DIR: ClassVar[str] = ".pipeline"
    PATH_LOGS_DIR: ClassVar[str] = "logs"
    PATH_OUTPUT_DIR: ClassVar[str] = "output"
    PATH_TRANSFORM_DIR: ClassVar[str] = "transform"
    PATH_VENV_DIR: ClassVar[str] = ".meltano/python"

    # Commands
    CMD_BINARY: ClassVar[str] = "meltano"
    CMD_ALL_OPTION: ClassVar[str] = "--all"
    CMD_CWD_OPTION: ClassVar[str] = "--cwd"
    CMD_ENVIRONMENT_OPTION: ClassVar[str] = "--environment"
    CMD_HELP_OPTION: ClassVar[str] = "--help"
    CMD_LIST_OPTION: ClassVar[str] = "--list"
    CMD_MODELS_OPTION: ClassVar[str] = "--models"
    CMD_NO_ENVIRONMENT_OPTION: ClassVar[str] = "--no-environment"
    CMD_SELECT_OPTION: ClassVar[str] = "--select"
    CMD_SHORT_HELP_OPTION: ClassVar[str] = "-h"
    CMD_VERSION_OPTION: ClassVar[str] = "--version"
    CMD_ADD: ClassVar[str] = "add"
    CMD_ELT: ClassVar[str] = "elt"
    CMD_INVOKE: ClassVar[str] = "invoke"
    CMD_SELECT: ClassVar[str] = "select"
    PIPELINE_STAGE_RESOLVE_COMMAND: ClassVar[str] = "resolve_command"
    PIPELINE_STAGE_EXECUTE_COMMAND: ClassVar[str] = "execute_command"
    PIPELINE_SHARED_KEY_COMMAND: ClassVar[str] = "command"
    PIPELINE_SHARED_KEY_COMMAND_RESULT: ClassVar[str] = "command_result"
    PAYLOAD_STREAM_ENTITY: ClassVar[str] = "Stream"
    PAYLOAD_TAP_ID_AUTO_SUFFIX: ClassVar[str] = "auto"
    PAYLOAD_SINGER_CATALOG_VERSION: ClassVar[int] = 1

    # Operation labels and failure messages
    ERROR_CATALOG_GENERATION_FAILED: ClassVar[str] = "Catalog generation failed"
    ERROR_DISCOVERY_FAILED: ClassVar[str] = "Discovery failed"
    ERROR_STREAM_DISCOVERY_FAILED: ClassVar[str] = "Stream discovery failed"
    ERROR_STREAM_SYNC_FAILED: ClassVar[str] = "Stream sync failed"
    LOG_MESSAGE_DISCOVER_STREAMS_FAILED: ClassVar[str] = "Failed to discover streams"
    LOG_MESSAGE_SYNC_STREAM_FAILED: ClassVar[str] = "Failed to sync stream"
    OPERATION_CREATE_TAP: ClassVar[str] = "create tap"
    OPERATION_DISCOVER_STREAMS: ClassVar[str] = "discover streams"
    OPERATION_SYNC_STREAM: ClassVar[str] = "sync stream"

    # Network
    NETWORK_DEFAULT_TIMEOUT: ClassVar[int] = c.DEFAULT_TIMEOUT_SECONDS
    NETWORK_MELTANO_DEFAULT_TIMEOUT: ClassVar[int] = 300

    # DatabasePorts

    # Plugin
    PLUGIN_CONFIG_VERSION: ClassVar[int] = 1
    PLUGIN_DBT_DEFAULT_NAME: ClassVar[str] = "dbt-postgres"
    PLUGIN_INSTALLATION_TIMEOUT: ClassVar[int] = 300
    PLUGIN_INFO_ARG_COUNT: ClassVar[int] = 2
    "Expected number of arguments (plugin type and name) for plugin info command."
    PLUGIN_MIN_TAP_PLUGIN_NAME_LENGTH: ClassVar[int] = 5
    PLUGIN_MIN_TARGET_PLUGIN_NAME_LENGTH: ClassVar[int] = 8
    PREFIX_DBT: ClassVar[str] = "dbt"
    PREFIX_TARGET: ClassVar[str] = "target"

    # EnvironmentVariables
    ENV_VAR_ENVIRONMENT: ClassVar[str] = "MELTANO_ENVIRONMENT"
    ENV_VAR_LOG_LEVEL: ClassVar[str] = "MELTANO_LOG_LEVEL"
    ENV_VAR_PROJECT_ROOT: ClassVar[str] = "MELTANO_PROJECT_ROOT"
    OPERATION_ERRORS: ClassVar[tuple[type[Exception], ...]] = (
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
    )

    # Singer
    SINGER_MESSAGE_TYPE_RECORD: ClassVar[str] = (
        FlextMeltanoConstantsEnums.SingerMessageType.RECORD
    )
    SINGER_MESSAGE_TYPE_SCHEMA: ClassVar[str] = (
        FlextMeltanoConstantsEnums.SingerMessageType.SCHEMA
    )
    SINGER_SAFE_EXCEPTIONS: ClassVar[tuple[type[Exception], ...]] = (
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
        RuntimeError,
        ImportError,
        c.ValidationError,
    )

    # Dbt
    DBT_COMMAND_RUN: ClassVar[str] = FlextMeltanoConstantsEnums.DbtCommand.RUN
    DBT_COMMAND_TEST: ClassVar[str] = FlextMeltanoConstantsEnums.DbtCommand.TEST
    DBT_MANIFEST_FILE: ClassVar[str] = FlextMeltanoConstantsEnums.DbtFileName.MANIFEST
    DBT_MATERIALIZATION_TABLE: ClassVar[str] = "table"
    DBT_MATERIALIZATION_VIEW: ClassVar[str] = "view"
    DBT_PROJECT_FILE: ClassVar[str] = FlextMeltanoConstantsEnums.DbtFileName.PROJECT
    DBT_PROJECT_DEFAULT_VERSION: ClassVar[str] = "1.0.0"

    # ModelValidation
    VALIDATION_COMPLEXITY_MINIMAL_SETTINGS: ClassVar[int] = 0
    VALIDATION_COMPLEXITY_SIMPLE_MAX_SETTINGS: ClassVar[int] = 5
    VALIDATION_COMPLEXITY_MODERATE_MAX_SETTINGS: ClassVar[int] = 20
    VALIDATION_DBT_SIMPLE_EXECUTION_THRESHOLD: ClassVar[int] = 10
    VALIDATION_MAX_WORKERS_THRESHOLD: ClassVar[int] = 100
    VALIDATION_EXECUTION_GOOD_PERFORMANCE_THRESHOLD: ClassVar[int] = 100
    VALIDATION_EXECUTION_HIGH_PERFORMANCE_THRESHOLD: ClassVar[int] = 1000
    VALIDATION_EXECUTION_MODERATE_PERFORMANCE_THRESHOLD: ClassVar[int] = 10
    VALIDATION_MATURITY_DEVELOPING_ENV_COUNT: ClassVar[int] = 2
    VALIDATION_MATURITY_MATURE_ENV_COUNT: ClassVar[int] = 3
    VALIDATION_STRUCTURE_MODERATE_MAX_PATHS: ClassVar[int] = 10
    VALIDATION_STRUCTURE_SIMPLE_MAX_PATHS: ClassVar[int] = 5
