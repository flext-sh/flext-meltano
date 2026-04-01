"""FLEXT Meltano base constants — project metadata, paths, network, plugins."""

from __future__ import annotations

from typing import Final

from pydantic import ValidationError


class FlextMeltanoConstantsBase:
    """Base meltano constants: metadata, versions, paths, network, plugins."""

    CONSTANTS_VERSION: Final[str] = "1.0.0"
    PROJECT_PREFIX: Final[str] = "flext-meltano"
    PROJECT_NAME: Final[str] = "FLEXT Meltano"
    FLEXT_MELTANO_VERSION: Final[str] = "0.9.0"
    PROJECT_FILE_DBT: Final[str] = "dbt_project.yml"
    COMMAND_RUN_DBT: Final[str] = "dbt run"
    COMMAND_TEST: Final[str] = "dbt test"
    DEFAULT_VARIANT: Final[str] = "meltano"

    class Metadata:
        """Metadata describing the Meltano distribution."""

        APPLICATION_NAME: Final[str] = "flext-pipeline"
        APPLICATION_DESCRIPTION: Final[str] = "FLEXT Generic Data Pipeline Framework"
        APPLICATION_AUTHOR: Final[str] = "FLEXT Team"
        APPLICATION_LICENSE: Final[str] = "MIT"
        CREATED_BY: Final[str] = "flext-pipeline"
        DEFAULT_ENVIRONMENTS: Final[tuple[str, ...]] = ("dev", "staging", "prod")

    class Versions:
        """Version requirements for the Meltano toolchain."""

        MELTANO_REQUIRED: Final[str] = "3.9.1"
        SINGER_SDK_REQUIRED: Final[str] = "0.48.0"
        DBT_REQUIRED: Final[str] = "1.10.5"

    SDK_VERSION_REQUIRED: Final[str] = Versions.SINGER_SDK_REQUIRED
    VERSION_REQUIRED_DBT: Final[str] = Versions.DBT_REQUIRED

    class Paths:
        """Filesystem layout for Meltano projects."""

        PROJECT_FILE: Final[str] = "meltano.yml"
        MELTANO_PROJECT_FILE: Final[str] = "meltano.yml"
        STATE_DIR: Final[str] = ".pipeline"
        LOGS_DIR: Final[str] = "logs"
        OUTPUT_DIR: Final[str] = "output"
        TRANSFORM_DIR: Final[str] = "transform"
        VENV_DIR: Final[str] = ".meltano/python"

    class Commands:
        """CLI commands used by Meltano."""

        BINARY: Final[str] = "meltano"
        ALL_OPTION: Final[str] = "--all"
        CWD_OPTION: Final[str] = "--cwd"
        ENVIRONMENT_OPTION: Final[str] = "--environment"
        HELP_OPTION: Final[str] = "--help"
        LIST_OPTION: Final[str] = "--list"
        MODELS_OPTION: Final[str] = "--models"
        NO_ENVIRONMENT_OPTION: Final[str] = "--no-environment"
        SELECT_OPTION: Final[str] = "--select"
        SHORT_HELP_OPTION: Final[str] = "-h"
        VERSION_OPTION: Final[str] = "--version"
        ADD: Final[str] = "add"
        ELT: Final[str] = "elt"
        INIT: Final[str] = "init"
        INSTALL: Final[str] = "install"
        INVOKE: Final[str] = "invoke"
        RUN: Final[str] = "run"
        SELECT: Final[str] = "select"
        PIPELINE: Final[str] = "pipeline"

    class Network:
        """Network defaults derived from flext-core."""

        MELTANO_DEFAULT_TIMEOUT: Final[int] = 300
        DEFAULT_TIMEOUT: Final[int] = 30
        DISCOVERY_TIMEOUT: Final[int] = 60
        REQUEST_TIMEOUT: Final[int] = 60
        CONNECTION_TIMEOUT: Final[int] = 30
        BUFFER_SIZE: Final[int] = 8192
        MAX_PARALLEL_STREAMS: Final[int] = 4

    class DatabasePorts:
        """Default port assignments for supported databases."""

        POSTGRES: Final[int] = 5432
        MYSQL: Final[int] = 3306
        ORACLE: Final[int] = 1521
        HIGH_MEMORY_THRESHOLD: Final[int] = 1073741824

    class Plugin:
        """Plugin management constants."""

        CONFIG_VERSION: Final[int] = 1
        DBT_DEFAULT_NAME: Final[str] = "dbt-postgres"
        DISCOVERY_FILENAME: Final[str] = "catalog.json"
        STATE_FILENAME: Final[str] = "state.json"
        DEFAULT_VARIANT: Final[str] = "meltanolabs"
        HUB_URL: Final[str] = "https://hub.meltano.com"
        PREFIX_TAP: Final[str] = "tap"
        PREFIX_TARGET: Final[str] = "target"
        PREFIX_DBT: Final[str] = "dbt"
        INSTALLATION_TIMEOUT: Final[int] = 300
        MIN_TARGET_PLUGIN_NAME_LENGTH: Final[int] = 8
        MIN_TAP_PLUGIN_NAME_LENGTH: Final[int] = 5

    class EnvironmentVariables:
        """Environment variable names used by Meltano runtime settings."""

        PROJECT_ROOT: Final[str] = "MELTANO_PROJECT_ROOT"
        ENVIRONMENT: Final[str] = "MELTANO_ENVIRONMENT"
        LOG_LEVEL: Final[str] = "MELTANO_LOG_LEVEL"

    class Singer:
        """Singer protocol message metadata and shared constants."""

        MESSAGE_TYPE_RECORD: Final[str] = "RECORD"
        MESSAGE_TYPE_SCHEMA: Final[str] = "SCHEMA"
        MESSAGE_TYPE_STATE: Final[str] = "STATE"
        MESSAGE_TYPE_ACTIVATE_VERSION: Final[str] = "ACTIVATE_VERSION"
        MESSAGE_TYPE_METRIC: Final[str] = "METRIC"

        SAFE_EXCEPTIONS: Final[tuple[type[Exception], ...]] = (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
            ValidationError,
        )

    class Dbt:
        """DBT transformation constants."""

        PROJECT_FILE: Final[str] = "dbt_project.yml"
        PROFILES_FILE: Final[str] = "profiles.yml"
        MANIFEST_FILE: Final[str] = "manifest.json"
        COMMAND_RUN: Final[str] = "run"
        COMMAND_TEST: Final[str] = "test"
        COMMAND_BUILD: Final[str] = "build"
        COMMAND_COMPILE: Final[str] = "compile"
        FRESHNESS_ERROR_AFTER_HOURS: Final[int] = 24
        FRESHNESS_WARN_AFTER_HOURS: Final[int] = 12
        MATERIALIZATION_TABLE: Final[str] = "table"
        MATERIALIZATION_VIEW: Final[str] = "view"
        MATERIALIZATION_INCREMENTAL: Final[str] = "incremental"

    class ModelValidation:
        """Validation thresholds used by Meltano models."""

        MATURITY_MATURE_ENV_COUNT: Final[int] = 3
        MATURITY_DEVELOPING_ENV_COUNT: Final[int] = 2
        COMPLEXITY_MINIMAL_SETTINGS: Final[int] = 0
        COMPLEXITY_SIMPLE_MAX_SETTINGS: Final[int] = 5
        COMPLEXITY_MODERATE_MAX_SETTINGS: Final[int] = 15
        STRUCTURE_SIMPLE_MAX_PATHS: Final[int] = 5
        STRUCTURE_MODERATE_MAX_PATHS: Final[int] = 10
        VERSION_PARTS_COUNT: Final[int] = 3
        TAP_SIMPLE_CONFIG_THRESHOLD: Final[int] = 3
        TAP_MODERATE_CONFIG_THRESHOLD: Final[int] = 8
        TARGET_HIGH_EFFICIENCY_THRESHOLD: Final[int] = 1000
        TARGET_MEDIUM_EFFICIENCY_THRESHOLD: Final[int] = 100
        DBT_SIMPLE_EXECUTION_THRESHOLD: Final[int] = 5
        DBT_MODERATE_EXECUTION_THRESHOLD: Final[int] = 20
        EXECUTION_HIGH_PERFORMANCE_THRESHOLD: Final[int] = 1000
        EXECUTION_GOOD_PERFORMANCE_THRESHOLD: Final[int] = 100
        EXECUTION_MODERATE_PERFORMANCE_THRESHOLD: Final[int] = 10
        MAX_WORKERS_THRESHOLD: Final[int] = 50
