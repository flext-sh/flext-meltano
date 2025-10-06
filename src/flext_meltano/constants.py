"""FLEXT Meltano Constants - Domain-specific Meltano constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final, Literal

from flext_core import FlextConstants


class FlextMeltanoConstants(FlextConstants):
    """Single unified meltano constants class following FLEXT standards.

    Contains all constants for meltano domain operations.
    Follows FLEXT pattern: one class per module with nested subclasses.
    All constants are flat class attributes inheriting from FlextConstants.
    """

    # =========================================================================
    # MELTANO DOMAIN NAMESPACES - Following FLEXT pattern
    # =========================================================================

    class Meltano:
        """Meltano-specific constants namespace."""

        # Version metadata
        VERSION: Final[str] = "0.9.0"
        APPLICATION_NAME: Final[str] = "flext-meltano"
        APPLICATION_DESCRIPTION: Final[str] = "FLEXT Meltano ELT Pipeline Foundation"
        APPLICATION_AUTHOR: Final[str] = "FLEXT Team"
        APPLICATION_LICENSE: Final[str] = "MIT"

        # Metadata constants
        METADATA_CREATED_BY: Final[str] = "flext-meltano"
        METADATA_DEFAULT_ENVIRONMENTS: Final[tuple[str, ...]] = ("dev", "staging", "prod")

        # File constants
        PROJECT_FILE: Final[str] = "meltano.yml"
        MELTANO_PROJECT_FILE: Final[str] = "meltano.yml"
        STATE_DIR: Final[str] = ".meltano"
        LOGS_DIR: Final[str] = "logs"
        OUTPUT_DIR: Final[str] = "output"

        # Command constants
        COMMAND_INSTALL: Final[str] = "install"
        COMMAND_RUN: Final[str] = "run"
        COMMAND_ELT: Final[str] = "elt"

        # Version requirements
        VERSION_REQUIRED: Final[str] = "3.9.1"

        # FLEXT Meltano version
        FLEXT_MELTANO_VERSION: Final[str] = "0.9.0"

        # Default timeout constants
        MELTANO_DEFAULT_TIMEOUT: Final[int] = 300  # 5 minutes

        # Timeout constants (using FlextConstants as base)
        DEFAULT_TIMEOUT: Final[int] = (
            FlextConstants.Defaults.TIMEOUT * 10
        )  # 300 seconds
        DISCOVERY_TIMEOUT: Final[int] = (
            FlextConstants.Defaults.TIMEOUT * 2
        )  # 60 seconds
        EXTRACT_TIMEOUT: Final[int] = (
            FlextConstants.Defaults.TIMEOUT * 60
        )  # 1800 seconds
        LOAD_TIMEOUT: Final[int] = FlextConstants.Defaults.TIMEOUT * 60  # 1800 seconds

        # Database ports
        DEFAULT_POSTGRES_PORT: Final[int] = 5432
        DEFAULT_MYSQL_PORT: Final[int] = 3306
        DEFAULT_ORACLE_PORT: Final[int] = 1521

    class Singer:
        """Singer protocol constants namespace."""

        # Message types
        MESSAGE_TYPE_RECORD: Final[str] = "RECORD"
        MESSAGE_TYPE_SCHEMA: Final[str] = "SCHEMA"
        MESSAGE_TYPE_STATE: Final[str] = "STATE"
        MESSAGE_TYPE_METRIC: Final[str] = "METRIC"

        # Version requirements
        SDK_VERSION_REQUIRED: Final[str] = "0.48.0"

        # Batch sizes (using FlextConstants as base)
        DEFAULT_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 10  # 1000
        MAX_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 100  # 10000
        DEFAULT_BUFFER_SIZE: Final[int] = 8192

        # Timeouts (using FlextConstants as base)
        DEFAULT_CONNECTION_TIMEOUT: Final[int] = FlextConstants.Defaults.TIMEOUT  # 30
        DEFAULT_REQUEST_TIMEOUT: Final[int] = FlextConstants.Defaults.TIMEOUT * 2  # 60
        DEFAULT_MAX_PARALLEL_STREAMS: Final[int] = 4

    class Dbt:
        """DBT transformation constants namespace."""

        # File constants
        PROJECT_FILE: Final[str] = "dbt_project.yml"
        PROFILES_FILE: Final[str] = "profiles.yml"
        MANIFEST_FILE: Final[str] = "manifest.json"

        # Command constants
        COMMAND_RUN: Final[str] = "run"
        COMMAND_TEST: Final[str] = "test"
        COMMAND_BUILD: Final[str] = "build"
        COMMAND_COMPILE: Final[str] = "compile"

        # Version requirements
        VERSION_REQUIRED: Final[str] = "1.10.5"

        # Batch processing (using FlextConstants as base)
        DEFAULT_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 10  # 1000
        LARGE_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 50  # 5000
        MAX_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 100  # 10000

        # Freshness timeouts (hours)
        FRESHNESS_ERROR_AFTER: Final[int] = 24
        FRESHNESS_WARN_AFTER: Final[int] = 12

        # Materialization strategies
        MATERIALIZATION_TABLE: Final[str] = "table"
        MATERIALIZATION_VIEW: Final[str] = "view"
        MATERIALIZATION_INCREMENTAL: Final[str] = "incremental"

    class Plugin:
        """Plugin management constants namespace."""

        # Configuration constants
        CONFIG_VERSION: Final[int] = 1
        DISCOVERY_FILENAME: Final[str] = "catalog.json"
        STATE_FILENAME: Final[str] = "state.json"
        DEFAULT_VARIANT: Final[str] = "meltanolabs"
        HUB_URL: Final[str] = "https://hub.meltano.com"

        # Prefixes
        PREFIX_TAP: Final[str] = "tap"
        PREFIX_TARGET: Final[str] = "target"

        # Types
        TYPE_TAP: Final[str] = "extractor"
        TYPE_TARGET: Final[str] = "loader"
        TYPE_DBT: Final[str] = "transformer"

        # Installation timeout (using FlextConstants as base)
        INSTALLATION_TIMEOUT: Final[int] = (
            FlextConstants.Defaults.TIMEOUT * 10
        )  # 300 seconds

        # Validation rules
        MIN_TARGET_PLUGIN_NAME_LENGTH: Final[int] = (
            8  # "target-" prefix + minimum 2 chars
        )
        MIN_TAP_PLUGIN_NAME_LENGTH: Final[int] = 5  # "tap-" prefix + minimum 1 char

    class Service:
        """Service management constants namespace."""

        # Validation rules
        MIN_NAME_LENGTH: Final[int] = 3  # Minimum service name length

    class Model:
        """Model validation constants namespace."""

        # Project maturity thresholds
        MATURITY_MATURE_ENV_COUNT: Final[int] = 3
        MATURITY_DEVELOPING_ENV_COUNT: Final[int] = 2
        PROJECT_MATURITY_MATURE_ENV_COUNT: Final[int] = 3
        PROJECT_MATURITY_DEVELOPING_ENV_COUNT: Final[int] = 2

        # Plugin complexity thresholds
        COMPLEXITY_MINIMAL_SETTINGS: Final[int] = 0
        COMPLEXITY_SIMPLE_MAX_SETTINGS: Final[int] = 5
        COMPLEXITY_MODERATE_MAX_SETTINGS: Final[int] = 15

        # Project structure thresholds
        STRUCTURE_SIMPLE_MAX_PATHS: Final[int] = 5
        STRUCTURE_MODERATE_MAX_PATHS: Final[int] = 10

        # DBT version validation
        VERSION_PARTS_COUNT: Final[int] = 3

    # =========================================================================
    # ENUMS - Domain-specific enumerations
    # =========================================================================

    class PluginTypes(StrEnum):
        """Plugin types enumeration."""

        EXTRACTORS = "extractors"
        LOADERS = "loaders"
        TRANSFORMS = "transforms"
        ORCHESTRATORS = "orchestrators"

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

    # =========================================================================
    # LITERAL TYPES - Python 3.13+ type aliases
    # =========================================================================

    # Plugin type literals
    PluginType = Literal["extractors", "loaders", "transforms", "orchestrators"]
    ReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL", "LOG_BASED"]
    SingerVersion = Literal["0.44.0", "0.45.0", "0.46.0", "0.47.0", "0.48.0"]

    class MeltanoLogging:
        """Meltano-specific logging configuration constants namespace."""

        # Log levels (using FlextConstants as source)
        DEFAULT_LEVEL = FlextConstants.Config.LogLevel.INFO
        PIPELINE_LEVEL = FlextConstants.Config.LogLevel.INFO
        EXTRACT_LEVEL = FlextConstants.Config.LogLevel.INFO
        LOAD_LEVEL = FlextConstants.Config.LogLevel.INFO
        TRANSFORM_LEVEL = FlextConstants.Config.LogLevel.INFO
        ERROR_LEVEL = FlextConstants.Config.LogLevel.ERROR
        PERFORMANCE_LEVEL = FlextConstants.Config.LogLevel.WARNING

        # Pipeline execution logging
        LOG_PIPELINE_START = True
        LOG_PIPELINE_END = True
        LOG_PIPELINE_PROGRESS = True
        LOG_PIPELINE_ERRORS = True
        LOG_PIPELINE_STATS = True
        LOG_PIPELINE_DURATION = True

        # Extract operations logging
        LOG_EXTRACT_START = True
        LOG_EXTRACT_END = True
        LOG_EXTRACT_RECORDS = True
        LOG_EXTRACT_ERRORS = True
        LOG_EXTRACT_DURATION = True
        LOG_EXTRACT_SOURCE_INFO = True

        # Load operations logging
        LOG_LOAD_START = True
        LOG_LOAD_END = True
        LOG_LOAD_RECORDS = True
        LOG_LOAD_ERRORS = True
        LOG_LOAD_DURATION = True
        LOG_LOAD_TARGET_INFO = True

        # Transform operations logging
        LOG_TRANSFORM_START = True
        LOG_TRANSFORM_END = True
        LOG_TRANSFORM_RECORDS = True
        LOG_TRANSFORM_ERRORS = True
        LOG_TRANSFORM_DURATION = True
        LOG_TRANSFORM_SQL = False  # Don't log SQL by default (privacy/security)

        # Performance tracking
        TRACK_MELTANO_PERFORMANCE = True
        MELTANO_PERFORMANCE_THRESHOLD_WARNING: Final[int] = 5000  # 5 seconds
        MELTANO_PERFORMANCE_THRESHOLD_CRITICAL: Final[int] = 10000  # 10 seconds
        TRACK_RECORD_COUNTS = True
        TRACK_MEMORY_USAGE = True
        HIGH_MEMORY_THRESHOLD = FlextConstants.Performance.HIGH_MEMORY_THRESHOLD_BYTES

        # Data quality logging
        LOG_DATA_QUALITY_ISSUES = True
        LOG_VALIDATION_ERRORS = True
        LOG_SCHEMA_CHANGES = True
        LOG_DATA_TYPE_CONVERSIONS = True
        LOG_NULL_VALUE_HANDLING = True

        # Error handling and recovery
        LOG_ERROR_RECOVERY = True
        LOG_RETRY_ATTEMPTS = True
        LOG_FALLBACK_OPERATIONS = True
        LOG_PARTIAL_FAILURES = True
        LOG_CRITICAL_FAILURES = True

        # Context information to include
        INCLUDE_PIPELINE_ID = True
        INCLUDE_JOB_ID = True
        INCLUDE_RUN_ID = True
        INCLUDE_SOURCE_NAME = True
        INCLUDE_TARGET_NAME = True
        INCLUDE_TRANSFORM_NAME = True
        INCLUDE_RECORD_COUNT = True
        INCLUDE_DURATION = True


__all__ = [
    "FlextMeltanoConstants",
    "PluginTypes",
]

# Export nested classes for easier access
PluginTypes = FlextMeltanoConstants.PluginTypes
