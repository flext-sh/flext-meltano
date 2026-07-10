"""FLEXT Meltano base constants — project metadata, paths, network, plugins."""

from __future__ import annotations

from typing import Final

from flext_cli import c
from flext_meltano._constants.enums import FlextMeltanoConstantsEnums


class FlextMeltanoConstantsBase:
    """Base meltano constants: metadata, versions, paths, network, plugins.

    All constants are flat with descriptive prefixes to explain their usage.
    """

    CONSTANTS_VERSION: Final[str] = "1.0.0"
    DBT_BINARY: Final[str] = "dbt"
    DEFAULT_VARIANT: Final[str] = "meltano"
    FLEXT_MELTANO_VERSION: Final[str] = "0.9.0"
    PROJECT_NAME: Final[str] = "FLEXT Meltano"
    PROJECT_PREFIX: Final[str] = "flext-meltano"

    # Metadata
    METADATA_APPLICATION_DESCRIPTION: Final[str] = (
        "FLEXT Generic Data Pipeline Framework"
    )
    METADATA_APPLICATION_NAME: Final[str] = "flext-pipeline"
    METADATA_DEFAULT_ENVIRONMENTS: Final[
        tuple[FlextMeltanoConstantsEnums.ProjectEnvironment, ...]
    ] = (
        FlextMeltanoConstantsEnums.ProjectEnvironment.DEV,
        FlextMeltanoConstantsEnums.ProjectEnvironment.STAGING,
        FlextMeltanoConstantsEnums.ProjectEnvironment.PROD,
    )

    # Versions
    VERSION_MELTANO_REQUIRED: Final[str] = "3.9.1"
    VERSION_MELTANO_REQUIREMENT: Final[str] = f">={VERSION_MELTANO_REQUIRED}"
    VERSION_SINGER_SDK_REQUIRED: Final[str] = "0.48.0"
    VERSION_DBT_REQUIRED: Final[str] = "1.10.5"

    SDK_VERSION_REQUIRED: Final[str] = VERSION_SINGER_SDK_REQUIRED

    # Paths
    PATH_MELTANO_PROJECT_FILE: Final[str] = "meltano.yml"
    PATH_PROJECT_FILE: Final[str] = PATH_MELTANO_PROJECT_FILE
    PATH_CONFIG_DIR: Final[str] = ".meltano"
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
    CMD_INVOKE: Final[str] = "invoke"
    CMD_SELECT: Final[str] = "select"
    PIPELINE_STAGE_RESOLVE_COMMAND: Final[str] = "resolve_command"
    PIPELINE_STAGE_EXECUTE_COMMAND: Final[str] = "execute_command"
    PIPELINE_SHARED_KEY_COMMAND: Final[str] = "command"
    PIPELINE_SHARED_KEY_COMMAND_RESULT: Final[str] = "command_result"
    PAYLOAD_STREAM_ENTITY: Final[str] = "Stream"
    PAYLOAD_TAP_ID_AUTO_SUFFIX: Final[str] = "auto"
    PAYLOAD_SINGER_CATALOG_VERSION: Final[int] = 1

    # Operation labels and failure messages
    ERROR_CATALOG_GENERATION_FAILED: Final[str] = "Catalog generation failed"
    ERROR_DISCOVERY_FAILED: Final[str] = "Discovery failed"
    ERROR_STREAM_DISCOVERY_FAILED: Final[str] = "Stream discovery failed"
    ERROR_STREAM_SYNC_FAILED: Final[str] = "Stream sync failed"
    LOG_MESSAGE_DISCOVER_STREAMS_FAILED: Final[str] = "Failed to discover streams"
    LOG_MESSAGE_SYNC_STREAM_FAILED: Final[str] = "Failed to sync stream"
    OPERATION_CREATE_TAP: Final[str] = "create tap"
    OPERATION_DISCOVER_STREAMS: Final[str] = "discover streams"
    OPERATION_SYNC_STREAM: Final[str] = "sync stream"

    # Network
    NETWORK_DEFAULT_TIMEOUT: Final[int] = c.DEFAULT_TIMEOUT_SECONDS
    NETWORK_MELTANO_DEFAULT_TIMEOUT: Final[int] = 300

    # DatabasePorts

    # Plugin
    PLUGIN_CONFIG_VERSION: Final[int] = 1
    PLUGIN_DBT_DEFAULT_NAME: Final[str] = "dbt-postgres"
    PLUGIN_INSTALLATION_TIMEOUT: Final[int] = 300
    PLUGIN_INFO_ARG_COUNT: Final[int] = 2
    "Expected number of arguments (plugin type and name) for plugin info command."
    PLUGIN_MIN_TAP_PLUGIN_NAME_LENGTH: Final[int] = 5
    PLUGIN_MIN_TARGET_PLUGIN_NAME_LENGTH: Final[int] = 8
    PREFIX_DBT: Final[str] = "dbt"
    PREFIX_TARGET: Final[str] = "target"

    # EnvironmentVariables
    ENV_VAR_ENVIRONMENT: Final[str] = "MELTANO_ENVIRONMENT"
    ENV_VAR_LOG_LEVEL: Final[str] = "MELTANO_LOG_LEVEL"
    ENV_VAR_PROJECT_ROOT: Final[str] = "MELTANO_PROJECT_ROOT"
    OPERATION_ERRORS: Final[tuple[type[Exception], ...]] = (
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
    )

    # Singer
    SINGER_MESSAGE_TYPE_RECORD: Final[str] = (
        FlextMeltanoConstantsEnums.SingerMessageType.RECORD
    )
    SINGER_MESSAGE_TYPE_SCHEMA: Final[str] = (
        FlextMeltanoConstantsEnums.SingerMessageType.SCHEMA
    )
    SINGER_SAFE_EXCEPTIONS: Final[tuple[type[Exception], ...]] = (
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
    DBT_COMMAND_RUN: Final[str] = FlextMeltanoConstantsEnums.DbtCommand.RUN
    DBT_COMMAND_TEST: Final[str] = FlextMeltanoConstantsEnums.DbtCommand.TEST
    DBT_MANIFEST_FILE: Final[str] = FlextMeltanoConstantsEnums.DbtFileName.MANIFEST
    DBT_MATERIALIZATION_TABLE: Final[str] = "table"
    DBT_MATERIALIZATION_VIEW: Final[str] = "view"
    DBT_PROJECT_FILE: Final[str] = FlextMeltanoConstantsEnums.DbtFileName.PROJECT

    # ModelValidation
    VALIDATION_COMPLEXITY_MINIMAL_SETTINGS: Final[int] = 0
    VALIDATION_COMPLEXITY_SIMPLE_MAX_SETTINGS: Final[int] = 5
    VALIDATION_EXECUTION_GOOD_PERFORMANCE_THRESHOLD: Final[int] = 100
    VALIDATION_EXECUTION_HIGH_PERFORMANCE_THRESHOLD: Final[int] = 1000
    VALIDATION_EXECUTION_MODERATE_PERFORMANCE_THRESHOLD: Final[int] = 10
    VALIDATION_MATURITY_DEVELOPING_ENV_COUNT: Final[int] = 2
    VALIDATION_MATURITY_MATURE_ENV_COUNT: Final[int] = 3
    VALIDATION_STRUCTURE_MODERATE_MAX_PATHS: Final[int] = 10
    VALIDATION_STRUCTURE_SIMPLE_MAX_PATHS: Final[int] = 5
