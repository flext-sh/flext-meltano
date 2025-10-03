"""FLEXT Meltano Constants - Domain-specific Meltano constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final, Literal

from flext_core import FlextConstants, FlextTypes

# Python 3.13+ Type Aliases - ONLY Meltano-specific
type PluginType = Literal["extractors", "loaders", "transforms", "orchestrators"]
type ReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL", "LOG_BASED"]
type SingerVersion = Literal["0.44.0", "0.45.0", "0.46.0", "0.47.0", "0.48.0"]


class FlextMeltanoConstants(FlextConstants):
    """Single unified meltano constants class following FLEXT standards.

    Contains all constants for meltano domain operations.
    Follows FLEXT pattern: one class per module with nested subclasses.
    All constants are flat class attributes inheriting from FlextConstants.
    """

    # =========================================================================
    # VERSION METADATA (DOMAIN-SPECIFIC ONLY)
    # =========================================================================

    FLEXT_MELTANO_VERSION: Final[str] = "0.9.0"  # Domain-specific version

    # =========================================================================
    # DOMAIN-SPECIFIC CONSTANTS ONLY - FLAT CLASS STRUCTURE
    # =========================================================================

    # Application metadata constants
    APPLICATION_NAME: Final[str] = "flext-meltano"
    APPLICATION_DESCRIPTION: Final[str] = "FLEXT Meltano ELT Pipeline Foundation"
    APPLICATION_AUTHOR: Final[str] = "FLEXT Team"
    APPLICATION_LICENSE: Final[str] = "MIT"

    # Metadata constants
    METADATA_CREATED_BY: Final[str] = "flext-meltano"
    # Use FlextConstants.Config.ENVIRONMENTS instead of duplicating
    METADATA_DEFAULT_ENVIRONMENTS: Final[FlextTypes.StringList] = (
        FlextConstants.Config.ENVIRONMENTS
    )

    # Model validation constants - replace magic numbers in models.py
    PROJECT_MATURITY_MATURE_ENV_COUNT: Final[int] = 3
    PROJECT_MATURITY_DEVELOPING_ENV_COUNT: Final[int] = 2
    PLUGIN_COMPLEXITY_MINIMAL_SETTINGS: Final[int] = 0
    PLUGIN_COMPLEXITY_SIMPLE_MAX_SETTINGS: Final[int] = 5
    PLUGIN_COMPLEXITY_MODERATE_MAX_SETTINGS: Final[int] = 15
    PROJECT_STRUCTURE_SIMPLE_MAX_PATHS: Final[int] = 5
    PROJECT_STRUCTURE_MODERATE_MAX_PATHS: Final[int] = 10
    DBT_VERSION_PARTS_COUNT: Final[int] = 3

    # Meltano-specific file names and commands - cannot be generalized
    MELTANO_PROJECT_FILE: Final[str] = "meltano.yml"
    MELTANO_STATE_DIR: Final[str] = ".meltano"
    MELTANO_LOGS_DIR: Final[str] = "logs"
    MELTANO_OUTPUT_DIR: Final[str] = "output"
    MELTANO_COMMAND_INSTALL: Final[str] = "install"
    MELTANO_COMMAND_RUN: Final[str] = "run"
    MELTANO_COMMAND_ELT: Final[str] = "elt"

    # Meltano version requirements
    MELTANO_VERSION_REQUIRED: Final[str] = "3.9.1"

    # Meltano timeouts - USE FlextConstants as SOURCE OF TRUTH for generic timeouts
    MELTANO_DEFAULT_TIMEOUT: Final[int] = (
        FlextConstants.Defaults.TIMEOUT * 10
    )  # 300 seconds
    MELTANO_DISCOVERY_TIMEOUT: Final[int] = (
        FlextConstants.Defaults.TIMEOUT * 2
    )  # 60 seconds
    MELTANO_EXTRACT_TIMEOUT: Final[int] = (
        FlextConstants.Defaults.TIMEOUT * 60
    )  # 1800 seconds
    MELTANO_LOAD_TIMEOUT: Final[int] = (
        FlextConstants.Defaults.TIMEOUT * 60
    )  # 1800 seconds

    # Database ports - USE FlextConstants.Network defaults for standard ports
    MELTANO_DEFAULT_POSTGRES_PORT: Final[int] = 5432  # Standard PostgreSQL port
    MELTANO_DEFAULT_MYSQL_PORT: Final[int] = 3306  # Standard MySQL port
    MELTANO_DEFAULT_ORACLE_PORT: Final[int] = 1521  # Standard Oracle port

    # Singer protocol constants - domain-specific message types
    SINGER_MESSAGE_TYPE_RECORD: Final[str] = "RECORD"
    SINGER_MESSAGE_TYPE_SCHEMA: Final[str] = "SCHEMA"
    SINGER_MESSAGE_TYPE_STATE: Final[str] = "STATE"
    SINGER_MESSAGE_TYPE_METRIC: Final[str] = "METRIC"

    # Singer version requirements
    SINGER_SDK_VERSION_REQUIRED: Final[str] = "0.48.0"

    # Singer batch sizes - USE FlextConstants.Defaults.PAGE_SIZE as base
    SINGER_DEFAULT_BATCH_SIZE: Final[int] = (
        FlextConstants.Defaults.PAGE_SIZE * 10
    )  # 1000
    SINGER_MAX_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 100  # 10000
    SINGER_DEFAULT_BUFFER_SIZE: Final[int] = 8192  # Buffer size is Singer-specific

    # Singer timeouts - USE FlextConstants timeouts as base
    SINGER_DEFAULT_CONNECTION_TIMEOUT: Final[int] = (
        FlextConstants.Defaults.TIMEOUT
    )  # 30
    SINGER_DEFAULT_REQUEST_TIMEOUT: Final[int] = (
        FlextConstants.Defaults.TIMEOUT * 2
    )  # 60
    SINGER_DEFAULT_MAX_PARALLEL_STREAMS: Final[int] = 4  # Singer-specific parallelism

    # DBT file names and commands
    DBT_PROJECT_FILE: Final[str] = "dbt_project.yml"
    DBT_PROFILES_FILE: Final[str] = "profiles.yml"
    DBT_MANIFEST_FILE: Final[str] = "manifest.json"
    DBT_COMMAND_RUN: Final[str] = "run"
    DBT_COMMAND_TEST: Final[str] = "test"
    DBT_COMMAND_BUILD: Final[str] = "build"
    DBT_COMMAND_COMPILE: Final[str] = "compile"

    # DBT version requirements
    DBT_VERSION_REQUIRED: Final[str] = "1.10.5"

    # DBT batch processing - USE FlextConstants.Defaults.PAGE_SIZE as base
    DBT_DEFAULT_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 10  # 1000
    DBT_LARGE_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 50  # 5000
    DBT_MAX_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 100  # 10000

    # DBT freshness timeouts (hours)
    DBT_FRESHNESS_ERROR_AFTER: Final[int] = 24
    DBT_FRESHNESS_WARN_AFTER: Final[int] = 12

    # DBT materialization strategies
    DBT_MATERIALIZATION_TABLE: Final[str] = "table"
    DBT_MATERIALIZATION_VIEW: Final[str] = "view"
    DBT_MATERIALIZATION_INCREMENTAL: Final[str] = "incremental"

    # Plugin configuration constants
    PLUGIN_CONFIG_VERSION: Final[int] = 1
    PLUGIN_DISCOVERY_FILENAME: Final[str] = "catalog.json"
    PLUGIN_STATE_FILENAME: Final[str] = "state.json"
    PLUGIN_DEFAULT_VARIANT: Final[str] = "meltanolabs"
    PLUGIN_HUB_URL: Final[str] = "https://hub.meltano.com"
    PLUGIN_PREFIX_TAP: Final[str] = "tap"
    PLUGIN_PREFIX_TARGET: Final[str] = "target"

    # Plugin types (no legacy aliases)
    PLUGIN_TYPE_TAP: Final[str] = "extractor"
    PLUGIN_TYPE_TARGET: Final[str] = "loader"
    PLUGIN_TYPE_DBT: Final[str] = "transformer"

    # Plugin installation timeout - USE FlextConstants.Defaults.TIMEOUT as base
    PLUGIN_INSTALLATION_TIMEOUT: Final[int] = (
        FlextConstants.Defaults.TIMEOUT * 10
    )  # 300 seconds

    # Plugin validation rules - Domain-specific validation rules
    PLUGIN_MIN_TARGET_PLUGIN_NAME_LENGTH: Final[int] = (
        8  # "target-" prefix + minimum 2 chars
    )
    PLUGIN_MIN_TAP_PLUGIN_NAME_LENGTH: Final[int] = 5  # "tap-" prefix + minimum 1 char
    # Service validation rules
    SERVICE_MIN_NAME_LENGTH: Final[int] = 3  # Minimum service name length

    # =========================================================================
    # DOMAIN-SPECIFIC ENUMS - NOT available in FlextConstants
    # =========================================================================

    class PluginTypes(StrEnum):
        """DOMAIN-SPECIFIC plugin types - NOT available in FlextConstants."""

        EXTRACTORS = "extractors"
        LOADERS = "loaders"
        TRANSFORMS = "transforms"
        ORCHESTRATORS = "orchestrators"

    class ReplicationMethods(StrEnum):
        """Singer replication methods - domain-specific to data integration."""

        FULL_TABLE = "FULL_TABLE"
        INCREMENTAL = "INCREMENTAL"
        LOG_BASED = "LOG_BASED"

    class OperationStatus(StrEnum):
        """Operation status enumeration for tracking Meltano execution states."""

        PENDING = "pending"
        RUNNING = "running"
        SUCCESS = "success"
        ERROR = "error"
        TIMEOUT = "timeout"
        CANCELLED = "cancelled"

    class RunMode(StrEnum):
        """Run mode enumeration for Meltano execution strategies."""

        FULL = "full"
        INCREMENTAL = "incremental"
        DRY_RUN = "dry_run"
        TEST = "test"

    # =========================================================================
    # MELTANO-SPECIFIC LOGGING CONSTANTS
    # =========================================================================

    # Meltano-specific log levels - USE FlextConstants.Config.LogLevel as source
    LOGGING_DEFAULT_LEVEL = FlextConstants.Config.LogLevel.INFO
    LOGGING_PIPELINE_LEVEL = FlextConstants.Config.LogLevel.INFO
    LOGGING_EXTRACT_LEVEL = FlextConstants.Config.LogLevel.INFO
    LOGGING_LOAD_LEVEL = FlextConstants.Config.LogLevel.INFO
    LOGGING_TRANSFORM_LEVEL = FlextConstants.Config.LogLevel.INFO
    LOGGING_ERROR_LEVEL = FlextConstants.Config.LogLevel.ERROR
    LOGGING_PERFORMANCE_LEVEL = FlextConstants.Config.LogLevel.WARNING

    # Pipeline execution logging
    LOGGING_LOG_PIPELINE_START = True
    LOGGING_LOG_PIPELINE_END = True
    LOGGING_LOG_PIPELINE_PROGRESS = True
    LOGGING_LOG_PIPELINE_ERRORS = True
    LOGGING_LOG_PIPELINE_STATS = True
    LOGGING_LOG_PIPELINE_DURATION = True

    # Extract operations logging
    LOGGING_LOG_EXTRACT_START = True
    LOGGING_LOG_EXTRACT_END = True
    LOGGING_LOG_EXTRACT_RECORDS = True
    LOGGING_LOG_EXTRACT_ERRORS = True
    LOGGING_LOG_EXTRACT_DURATION = True
    LOGGING_LOG_EXTRACT_SOURCE_INFO = True

    # Load operations logging
    LOGGING_LOG_LOAD_START = True
    LOGGING_LOG_LOAD_END = True
    LOGGING_LOG_LOAD_RECORDS = True
    LOGGING_LOG_LOAD_ERRORS = True
    LOGGING_LOG_LOAD_DURATION = True
    LOGGING_LOG_LOAD_TARGET_INFO = True

    # Transform operations logging
    LOGGING_LOG_TRANSFORM_START = True
    LOGGING_LOG_TRANSFORM_END = True
    LOGGING_LOG_TRANSFORM_RECORDS = True
    LOGGING_LOG_TRANSFORM_ERRORS = True
    LOGGING_LOG_TRANSFORM_DURATION = True
    LOGGING_LOG_TRANSFORM_SQL = False  # Don't log SQL by default (privacy/security)

    # Performance tracking
    LOGGING_TRACK_MELTANO_PERFORMANCE = True
    LOGGING_MELTANO_PERFORMANCE_THRESHOLD_WARNING: Final[int] = (
        5000  # 5 seconds default
    )
    LOGGING_MELTANO_PERFORMANCE_THRESHOLD_CRITICAL: Final[int] = (
        10000  # 10 seconds default
    )
    LOGGING_TRACK_RECORD_COUNTS = True
    LOGGING_TRACK_MEMORY_USAGE = True
    LOGGING_HIGH_MEMORY_THRESHOLD = (
        FlextConstants.Performance.HIGH_MEMORY_THRESHOLD_BYTES
    )

    # Data quality logging
    LOGGING_LOG_DATA_QUALITY_ISSUES = True
    LOGGING_LOG_VALIDATION_ERRORS = True
    LOGGING_LOG_SCHEMA_CHANGES = True
    LOGGING_LOG_DATA_TYPE_CONVERSIONS = True
    LOGGING_LOG_NULL_VALUE_HANDLING = True

    # Error handling and recovery
    LOGGING_LOG_ERROR_RECOVERY = True
    LOGGING_LOG_RETRY_ATTEMPTS = True
    LOGGING_LOG_FALLBACK_OPERATIONS = True
    LOGGING_LOG_PARTIAL_FAILURES = True
    LOGGING_LOG_CRITICAL_FAILURES = True

    # Context information to include
    LOGGING_INCLUDE_PIPELINE_ID = True
    LOGGING_INCLUDE_JOB_ID = True
    LOGGING_INCLUDE_RUN_ID = True
    LOGGING_INCLUDE_SOURCE_NAME = True
    LOGGING_INCLUDE_TARGET_NAME = True
    LOGGING_INCLUDE_TRANSFORM_NAME = True
    LOGGING_INCLUDE_RECORD_COUNT = True
    LOGGING_INCLUDE_DURATION = True


__all__ = [
    "FlextMeltanoConstants",
]

# Export nested classes for easier access
PluginTypes = FlextMeltanoConstants.PluginTypes
