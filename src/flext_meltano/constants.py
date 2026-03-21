"""FLEXT Meltano constants."""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final

from flext_cli import FlextCliConstants
from flext_core import FlextConstants


class FlextMeltanoConstants(FlextCliConstants):
    """Domain constants for the flext-meltano package."""

    class Meltano:
        """Meltano domain constants namespace.

        All meltano-specific constants are organized here for better namespace
        organization and to enable composition with other domain constants.
        """

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
            APPLICATION_DESCRIPTION: Final[str] = (
                "FLEXT Generic Data Pipeline Framework"
            )
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

            PROJECT_FILE: Final[str] = "pipeline.yml"
            MELTANO_PROJECT_FILE: Final[str] = "pipeline.yml"
            STATE_DIR: Final[str] = ".pipeline"
            LOGS_DIR: Final[str] = "logs"
            OUTPUT_DIR: Final[str] = "output"

        class Commands:
            """CLI commands used by Meltano."""

            INSTALL: Final[str] = "install"
            RUN: Final[str] = "run"
            PIPELINE: Final[str] = "pipeline"

        class Network:
            """Network defaults derived from flext-core."""

            MELTANO_DEFAULT_TIMEOUT: Final[int] = FlextConstants.DEFAULT_TIMEOUT_LIMIT
            DEFAULT_TIMEOUT: Final[int] = FlextConstants.DEFAULT_TIMEOUT_SECONDS
            DISCOVERY_TIMEOUT: Final[int] = FlextConstants.DEFAULT_TIMEOUT_SECONDS * 2
            REQUEST_TIMEOUT: Final[int] = FlextConstants.DEFAULT_TIMEOUT_SECONDS * 2
            CONNECTION_TIMEOUT: Final[int] = FlextConstants.DEFAULT_TIMEOUT_SECONDS
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
            DISCOVERY_FILENAME: Final[str] = "catalog.json"
            STATE_FILENAME: Final[str] = "state.json"
            DEFAULT_VARIANT: Final[str] = "meltanolabs"
            HUB_URL: Final[str] = "https://hub.meltano.com"
            PREFIX_TAP: Final[str] = "tap"
            PREFIX_TARGET: Final[str] = "target"
            PREFIX_DBT: Final[str] = "dbt"
            INSTALLATION_TIMEOUT: Final[int] = (
                FlextConstants.DEFAULT_TIMEOUT_SECONDS * 10
            )
            MIN_TARGET_PLUGIN_NAME_LENGTH: Final[int] = 8
            MIN_TAP_PLUGIN_NAME_LENGTH: Final[int] = 5

        class Singer:
            """Singer protocol message metadata."""

            MESSAGE_TYPE_RECORD: Final[str] = "RECORD"
            MESSAGE_TYPE_SCHEMA: Final[str] = "SCHEMA"
            MESSAGE_TYPE_STATE: Final[str] = "STATE"
            MESSAGE_TYPE_METRIC: Final[str] = "METRIC"

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

        class Enums:
            """Domain specific enumerations."""

            @unique
            class PluginType(StrEnum):
                """Supported Meltano plugin categories.

                DRY Pattern:
                    StrEnum is the single source of truth. Use PluginType.EXTRACTORS.value
                    or PluginType.EXTRACTORS directly - no base strings needed.
                """

                EXTRACTORS = "extractors"
                LOADERS = "loaders"
                TRANSFORMS = "transforms"
                ORCHESTRATORS = "orchestrators"

            @unique
            class ReplicationMethod(StrEnum):
                """Singer replication method identifiers.

                DRY Pattern:
                    StrEnum is the single source of truth. Use ReplicationMethod.FULL_TABLE.value
                    or ReplicationMethod.FULL_TABLE directly - no base strings needed.
                """

                FULL_TABLE = "FULL_TABLE"
                INCREMENTAL = "INCREMENTAL"
                LOG_BASED = "LOG_BASED"

            @unique
            class OperationStatus(StrEnum):
                """Operation execution lifecycle status values.

                DRY Pattern:
                    StrEnum is the single source of truth. Use OperationStatus.PENDING.value
                    or OperationStatus.PENDING directly - no base strings needed.
                """

                PENDING = "pending"
                RUNNING = "running"
                SUCCESS = "success"
                ERROR = "error"
                TIMEOUT = "timeout"
                CANCELLED = "cancelled"

            @unique
            class RunMode(StrEnum):
                """Execution modes for Meltano operations.

                DRY Pattern:
                    StrEnum is the single source of truth. Use RunMode.FULL.value
                    or RunMode.FULL directly - no base strings needed.
                """

                FULL = "full"
                INCREMENTAL = "incremental"
                DRY_RUN = "dry_run"
                TEST = "test"

            @unique
            class Environment(StrEnum):
                """Deployment environments for Meltano pipelines.

                DRY Pattern:
                    StrEnum is the single source of truth. Use Environment.DEVELOPMENT.value
                    or Environment.DEVELOPMENT directly - no base strings needed.
                """

                DEVELOPMENT = "development"
                STAGING = "staging"
                PRODUCTION = "production"
                TESTING = "testing"
                LOCAL = "local"

            @unique
            class StreamStatus(StrEnum):
                """Meltano stream statuses — single source of truth."""

                COMPLETED = "completed"
                ERROR = "error"
                SUCCESS = "success"
                FAILED = "failed"
                IN_PROGRESS = "in_progress"
                PENDING = "pending"
                INITIALIZED = "initialized"
                PROCESSING = "processing"
                DISCOVERED = "discovered"
                SELECTED = "selected"
                EXTRACTING = "extracting"

            VALID_STATUSES: Final[frozenset[str]] = frozenset({
                StreamStatus.INITIALIZED,
                StreamStatus.PROCESSING,
                StreamStatus.COMPLETED,
                StreamStatus.ERROR,
            })
            ACTIVE_STATUSES: Final[frozenset[str]] = frozenset({
                StreamStatus.DISCOVERED,
                StreamStatus.SELECTED,
                StreamStatus.EXTRACTING,
            })

        class Logging:
            """Logging configuration constants."""

            DEFAULT_LEVEL: Final[str] = "INFO"
            INCLUDE_TRANSFORM_NAME: Final[bool] = True
            INCLUDE_RECORD_COUNT: Final[bool] = True
            LOG_FORMAT: Final[str] = (
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            MELTANO_PERFORMANCE_THRESHOLD_WARNING: Final[int] = 5000
            MELTANO_PERFORMANCE_THRESHOLD_CRITICAL: Final[int] = 10000

        class Service:
            """Service validation constants."""

            MIN_NAME_LENGTH: Final[int] = 3
            MAX_NAME_LENGTH: Final[int] = 50
            VALID_NAME_PATTERN: Final[str] = "^[a-zA-Z0-9_-]+$"

    @unique
    class MeltanoProjectType(StrEnum):
        """Meltano project type enumeration."""

        LIBRARY = "library"
        APPLICATION = "application"
        SERVICE = "service"
        MELTANO_PROJECT = "meltano-project"
        ELT_PIPELINE = "elt-pipeline"
        DATA_PIPELINE = "data-pipeline"
        ETL_SERVICE = "etl-service"
        SINGER_TAP = "singer-tap"
        SINGER_TARGET = "singer-target"
        DBT_PROJECT = "dbt-project"
        DATA_INTEGRATION = "data-integration"
        PIPELINE_ORCHESTRATOR = "pipeline-orchestrator"
        DATA_EXTRACTOR = "data-extractor"
        DATA_LOADER = "data-loader"
        TRANSFORMATION_SERVICE = "transformation-service"


c = FlextMeltanoConstants
__all__ = ["FlextMeltanoConstants", "c"]
