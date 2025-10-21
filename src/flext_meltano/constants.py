"""FLEXT Meltano Constants - Generic pipeline constants following SOLID principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum
from typing import Final, Literal

from flext_core import FlextConstants


class FlextMeltanoConstants(FlextConstants):
    """Generic pipeline constants following SOLID principles.

    Single responsibility: Pipeline domain constants only.
    Uses FlextConstants as source of truth for base values.
    No legacy code, no aliases, no fallbacks - clean, direct implementation.
    """

    # ============================================================================
    # TOP-LEVEL VERSION - Direct access for convenience
    # ============================================================================

    FLEXT_MELTANO_VERSION: Final[str] = "0.9.0"

    # ============================================================================
    # TOP-LEVEL PLUGIN CONSTANTS - Direct access for convenience
    # ============================================================================

    DEFAULT_VARIANT: Final[str] = "meltanolabs"
    HUB_URL: Final[str] = "https://hub.meltano.com"

    # ============================================================================
    # PIPELINE DOMAIN CONSTANTS - Generic and reusable
    # ============================================================================

    # Pipeline-specific constants are now in the Meltano nested class

    # ============================================================================
    # MELTANO-SPECIFIC CONSTANTS - Meltano framework constants
    # ============================================================================

    class Meltano:
        """Meltano-specific constants namespace."""

        # Version metadata
        VERSION: Final[str] = "0.9.0"
        APPLICATION_NAME: Final[str] = "flext-pipeline"
        APPLICATION_DESCRIPTION: Final[str] = "FLEXT Generic Data Pipeline Framework"
        APPLICATION_AUTHOR: Final[str] = "FLEXT Team"
        APPLICATION_LICENSE: Final[str] = "MIT"

        # Metadata constants
        METADATA_CREATED_BY: Final[str] = "flext-pipeline"
        METADATA_DEFAULT_ENVIRONMENTS: Final[tuple[str, ...]] = (
            "dev",
            "staging",
            "prod",
        )

        # File constants
        PROJECT_FILE: Final[str] = "pipeline.yml"
        MELTANO_PROJECT_FILE: Final[str] = "pipeline.yml"
        STATE_DIR: Final[str] = ".pipeline"
        LOGS_DIR: Final[str] = "logs"
        OUTPUT_DIR: Final[str] = "output"

        # Command constants
        COMMAND_INSTALL: Final[str] = "install"
        COMMAND_RUN: Final[str] = "run"
        COMMAND_PIPELINE: Final[str] = "pipeline"

        # Version requirements
        VERSION_REQUIRED: Final[str] = "3.9.1"
        FLEXT_MELTANO_VERSION: Final[str] = "0.9.0"

        # Default timeout constants
        MELTANO_DEFAULT_TIMEOUT: Final[int] = (
            FlextConstants.Performance.DEFAULT_TIMEOUT_LIMIT
        )  # 5 minutes

        # Database ports
        DEFAULT_POSTGRES_PORT: Final[int] = 5432
        DEFAULT_MYSQL_PORT: Final[int] = 3306
        DEFAULT_ORACLE_PORT: Final[int] = 1521

    # ============================================================================
    # SINGER PROTOCOL CONSTANTS - Generic Singer protocol
    # ============================================================================

    # Message types - generic Singer protocol
    MESSAGE_TYPE_RECORD: Final[str] = "RECORD"
    MESSAGE_TYPE_SCHEMA: Final[str] = "SCHEMA"
    MESSAGE_TYPE_STATE: Final[str] = "STATE"
    MESSAGE_TYPE_METRIC: Final[str] = "METRIC"

    # Version requirements - uses FlextConstants as base
    SDK_VERSION_REQUIRED: Final[str] = "0.48.0"

    # Batch sizes - derived from FlextConstants
    DEFAULT_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 10  # 1000
    MAX_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 100  # 10000
    DEFAULT_BUFFER_SIZE: Final[int] = 8192

    # Timeouts - derived from FlextConstants
    DEFAULT_CONNECTION_TIMEOUT: Final[int] = FlextConstants.Defaults.TIMEOUT  # 30
    DEFAULT_REQUEST_TIMEOUT: Final[int] = FlextConstants.Defaults.TIMEOUT * 2  # 60
    DEFAULT_MAX_PARALLEL_STREAMS: Final[int] = 4

    # ============================================================================
    # DBT TRANSFORMATION CONSTANTS - Generic DBT project structure
    # ============================================================================

    # File constants - generic DBT project structure
    PROJECT_FILE_DBT: Final[str] = "dbt_project.yml"
    PROFILES_FILE: Final[str] = "profiles.yml"
    MANIFEST_FILE: Final[str] = "manifest.json"

    # Command constants - generic DBT CLI interface
    COMMAND_RUN_DBT: Final[str] = "run"
    COMMAND_TEST: Final[str] = "test"
    COMMAND_BUILD: Final[str] = "build"
    COMMAND_COMPILE: Final[str] = "compile"

    # Version requirements - uses FlextConstants as base
    VERSION_REQUIRED_DBT: Final[str] = "1.10.5"

    # Batch processing - derived from FlextConstants
    DEFAULT_BATCH_SIZE_DBT: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 10  # 1000
    LARGE_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 50  # 5000
    MAX_BATCH_SIZE_DBT: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 100  # 10000

    # Freshness timeouts (hours) - generic data freshness management
    FRESHNESS_ERROR_AFTER: Final[int] = 24
    FRESHNESS_WARN_AFTER: Final[int] = 12

    # Materialization strategies - generic transformation patterns
    MATERIALIZATION_TABLE: Final[str] = "table"
    MATERIALIZATION_VIEW: Final[str] = "view"
    MATERIALIZATION_INCREMENTAL: Final[str] = "incremental"

    # ============================================================================
    # PLUGIN MANAGEMENT CONSTANTS - Generic plugin management
    # ============================================================================

    class Plugin:
        """Plugin management constants namespace."""

        # Configuration constants - generic plugin configuration
        CONFIG_VERSION: Final[int] = 1
        DISCOVERY_FILENAME: Final[str] = "catalog.json"
        STATE_FILENAME: Final[str] = "state.json"
        DEFAULT_VARIANT: Final[str] = "meltanolabs"
        HUB_URL: Final[str] = "https://hub.meltano.com"

        # Prefixes - generic plugin naming
        PREFIX_TAP: Final[str] = "tap"
        PREFIX_TARGET: Final[str] = "target"

        # Types - generic plugin types
        TYPE_TAP: Final[str] = "extractor"
        TYPE_TARGET: Final[str] = "loader"
        TYPE_DBT: Final[str] = "transformer"

        # Installation timeout - derived from FlextConstants
        INSTALLATION_TIMEOUT: Final[int] = (
            FlextConstants.Defaults.TIMEOUT * 10
        )  # 300 seconds

        # Validation rules - generic plugin validation
        MIN_TARGET_PLUGIN_NAME_LENGTH: Final[int] = (
            8  # "target-" prefix + minimum 2 chars
        )
        MIN_TAP_PLUGIN_NAME_LENGTH: Final[int] = 5  # "tap-" prefix + minimum 1 char

    # ============================================================================
    # SERVICE MANAGEMENT CONSTANTS - Generic service validation
    # ============================================================================

    class Service:
        """Service management constants namespace."""

        # Validation rules - generic service validation
        MIN_NAME_LENGTH: Final[int] = 3  # Minimum service name length

    # ============================================================================
    # MODEL VALIDATION CONSTANTS - Generic model validation
    # ============================================================================

    class Model:
        """Model validation constants namespace."""

        # Project maturity thresholds - generic project assessment
        MATURITY_MATURE_ENV_COUNT: Final[int] = 3
        MATURITY_DEVELOPING_ENV_COUNT: Final[int] = 2

        # Plugin complexity thresholds - generic complexity assessment
        COMPLEXITY_MINIMAL_SETTINGS: Final[int] = 0
        COMPLEXITY_SIMPLE_MAX_SETTINGS: Final[int] = 5
        COMPLEXITY_MODERATE_MAX_SETTINGS: Final[int] = 15

        # Project structure thresholds - generic structure assessment
        STRUCTURE_SIMPLE_MAX_PATHS: Final[int] = 5
        STRUCTURE_MODERATE_MAX_PATHS: Final[int] = 10

        # DBT version validation - generic version handling
        VERSION_PARTS_COUNT: Final[int] = 3

        # Tap/Target configuration thresholds - generic configuration assessment
        TAP_SIMPLE_CONFIG_THRESHOLD: Final[int] = 3
        TAP_MODERATE_CONFIG_THRESHOLD: Final[int] = 8

        # Target processing efficiency thresholds - generic efficiency assessment
        TARGET_HIGH_EFFICIENCY_THRESHOLD: Final[int] = 1000
        TARGET_MEDIUM_EFFICIENCY_THRESHOLD: Final[int] = 100

        # DBT execution complexity thresholds - generic execution assessment
        DBT_SIMPLE_EXECUTION_THRESHOLD: Final[int] = 5
        DBT_MODERATE_EXECUTION_THRESHOLD: Final[int] = 20

        # Execution result performance thresholds - generic performance assessment
        EXECUTION_HIGH_PERFORMANCE_THRESHOLD: Final[int] = 1000
        EXECUTION_GOOD_PERFORMANCE_THRESHOLD: Final[int] = 100
        EXECUTION_MODERATE_PERFORMANCE_THRESHOLD: Final[int] = 10

    # ============================================================================
    # LOGGING CONFIGURATION CONSTANTS - Generic logging configuration
    # ============================================================================

    class Logging:
        """Logging configuration constants namespace."""

        # Log levels - uses FlextConstants as source of truth
        DEFAULT_LEVEL = FlextConstants.Configuration.LogLevel.INFO
        PIPELINE_LEVEL = FlextConstants.Configuration.LogLevel.INFO
        EXTRACT_LEVEL = FlextConstants.Configuration.LogLevel.INFO
        LOAD_LEVEL = FlextConstants.Configuration.LogLevel.INFO
        TRANSFORM_LEVEL = FlextConstants.Configuration.LogLevel.INFO
        ERROR_LEVEL = FlextConstants.Configuration.LogLevel.ERROR
        PERFORMANCE_LEVEL = FlextConstants.Configuration.LogLevel.WARNING

        # Pipeline execution logging - generic pipeline logging
        LOG_PIPELINE_START = True
        LOG_PIPELINE_END = True
        LOG_PIPELINE_PROGRESS = True
        LOG_PIPELINE_ERRORS = True
        LOG_PIPELINE_STATS = True
        LOG_PIPELINE_DURATION = True

        # Extract operations logging - generic extraction logging
        LOG_EXTRACT_START = True
        LOG_EXTRACT_END = True
        LOG_EXTRACT_RECORDS = True
        LOG_EXTRACT_ERRORS = True
        LOG_EXTRACT_DURATION = True
        LOG_EXTRACT_SOURCE_INFO = True

        # Load operations logging - generic loading logging
        LOG_LOAD_START = True
        LOG_LOAD_END = True
        LOG_LOAD_RECORDS = True
        LOG_LOAD_ERRORS = True
        LOG_LOAD_DURATION = True
        LOG_LOAD_TARGET_INFO = True

        # Transform operations logging - generic transformation logging
        LOG_TRANSFORM_START = True
        LOG_TRANSFORM_END = True
        LOG_TRANSFORM_RECORDS = True
        LOG_TRANSFORM_ERRORS = True
        LOG_TRANSFORM_DURATION = True
        LOG_TRANSFORM_SQL = False  # Don't log SQL by default (privacy/security)

        # Performance tracking - generic performance monitoring
        TRACK_MELTANO_PERFORMANCE = True
        MELTANO_PERFORMANCE_THRESHOLD_WARNING: Final[int] = 5000  # 5 seconds
        MELTANO_PERFORMANCE_THRESHOLD_CRITICAL: Final[int] = 10000  # 10 seconds
        TRACK_RECORD_COUNTS = True
        TRACK_MEMORY_USAGE = True
        HIGH_MEMORY_THRESHOLD: Final[int] = 1073741824  # 1 GB in bytes

        # Data quality logging - generic data quality monitoring
        LOG_DATA_QUALITY_ISSUES = True
        LOG_VALIDATION_ERRORS = True
        LOG_SCHEMA_CHANGES = True
        LOG_DATA_TYPE_CONVERSIONS = True
        LOG_NULL_VALUE_HANDLING = True

        # Error handling and recovery - generic error management
        LOG_ERROR_RECOVERY = True
        LOG_RETRY_ATTEMPTS = True
        LOG_FALLBACK_OPERATIONS = True
        LOG_PARTIAL_FAILURES = True
        LOG_CRITICAL_FAILURES = True

        # Context information to include - generic context logging
        INCLUDE_PIPELINE_ID = True
        INCLUDE_JOB_ID = True
        INCLUDE_RUN_ID = True
        INCLUDE_SOURCE_NAME = True
        INCLUDE_TARGET_NAME = True
        INCLUDE_TRANSFORM_NAME = True
        INCLUDE_RECORD_COUNT = True
        INCLUDE_DURATION = True

    # ============================================================================
    # ENUMERATIONS - Domain-specific enumerations following SOLID principles
    # ============================================================================

    class PluginTypes(StrEnum):
        """Plugin types enumeration."""

        EXTRACTORS = "extractors"
        LOADERS = "loaders"
        TRANSFORMS = "transforms"
        ORCHESTRATORS = "orchestrators"

        @classmethod
        def get_all_plugins(cls) -> list[dict[str, str]]:
            """Get all available plugin types as plugin dictionaries."""
            return [{"type": member.value, "name": member.value} for member in cls]

    class ReplicationMethods(StrEnum):
        """Singer replication methods enumeration."""

        FULL_TABLE = "FULL_TABLE"
        INCREMENTAL = "INCREMENTAL"
        LOG_BASED = "LOG_BASED"

    class OperationStatus(StrEnum):
        """Operation status enumeration."""

        PENDING = "pending"
        RUNNING = "running"
        SUCCESS = "success"
        ERROR = "error"
        TIMEOUT = "timeout"
        CANCELLED = "cancelled"

    class RunMode(StrEnum):
        """Run mode enumeration."""

        FULL = "full"
        INCREMENTAL = "incremental"
        DRY_RUN = "dry_run"
        TEST = "test"

    class Environment(StrEnum):
        """Environment types enumeration."""

        DEVELOPMENT = "development"
        STAGING = "staging"
        PRODUCTION = "production"
        TESTING = "testing"
        LOCAL = "local"

    # ============================================================================
    # LITERAL TYPES - Python 3.13+ type aliases
    # ============================================================================

    # Plugin type literals
    PluginType = Literal["extractors", "loaders", "transforms", "orchestrators"]
    ReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL", "LOG_BASED"]
    SingerVersion = Literal["0.44.0", "0.45.0", "0.46.0", "0.47.0", "0.48.0"]


# Export aliases for backward compatibility - no legacy code, just clean interfaces
SingerConstants = FlextMeltanoConstants  # Main export for ecosystem use


__all__ = [
    "FlextMeltanoConstants",
    "SingerConstants",
]
