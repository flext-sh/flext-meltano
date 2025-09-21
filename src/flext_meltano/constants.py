"""FLEXT Meltano Constants - Domain-specific Meltano constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum, auto
from typing import Final, Literal

from flext_core import FlextConstants

# Python 3.13+ Type Aliases - ONLY Meltano-specific
type PluginType = Literal["extractors", "loaders", "transforms", "orchestrators"]
type ReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL", "LOG_BASED"]
type SingerVersion = Literal["0.44.0", "0.45.0", "0.46.0", "0.47.0", "0.48.0"]


class FlextMeltanoConstants:
    """DOMAIN-SPECIFIC Meltano constants using FlextConstants as SOURCE OF TRUTH.

    ZERO DUPLICATION PRINCIPLE:
    - FlextConstants is SOURCE OF TRUTH for generic constants
    - Contains ONLY Meltano-specific constants that cannot be generalized
    - All timeouts, ports, and generic values use FlextConstants
    """

    # =========================================================================
    # VERSION METADATA (DOMAIN-SPECIFIC ONLY)
    # =========================================================================

    FLEXT_MELTANO_VERSION: Final[str] = "0.9.0"  # Domain-specific version

    # =========================================================================
    # DOMAIN-SPECIFIC CONSTANTS ONLY
    # =========================================================================

    class Application:
        """DOMAIN-SPECIFIC application metadata."""

        NAME: Final[str] = "flext-meltano"
        DESCRIPTION: Final[str] = "FLEXT Meltano ELT Pipeline Foundation"
        AUTHOR: Final[str] = "FLEXT Team"
        LICENSE: Final[str] = "MIT"

    class Metadata:
        """DOMAIN-SPECIFIC metadata constants."""

        CREATED_BY: Final[str] = "flext-meltano"
        # Use FlextConstants.Config.ENVIRONMENTS instead of duplicating
        DEFAULT_ENVIRONMENTS: Final[list[str]] = FlextConstants.Config.ENVIRONMENTS

    class MeltanoSpecific:
        """Meltano-specific file names and commands - cannot be generalized."""

        # DOMAIN-SPECIFIC: File and directory names
        PROJECT_FILE: Final[str] = "meltano.yml"
        STATE_DIR: Final[str] = ".meltano"
        LOGS_DIR: Final[str] = "logs"
        OUTPUT_DIR: Final[str] = "output"
        COMMAND_INSTALL: Final[str] = "install"
        COMMAND_RUN: Final[str] = "run"
        COMMAND_ELT: Final[str] = "elt"

        # DOMAIN-SPECIFIC: Version requirements
        VERSION_REQUIRED: Final[str] = "3.9.1"

        # USE FlextConstants as SOURCE OF TRUTH for generic timeouts
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

        # USE FlextConstants.Network defaults for standard ports
        DEFAULT_POSTGRES_PORT: Final[int] = 5432  # Standard PostgreSQL port
        DEFAULT_MYSQL_PORT: Final[int] = 3306  # Standard MySQL port
        DEFAULT_ORACLE_PORT: Final[int] = 1521  # Standard Oracle port

    class Singer:
        """Singer protocol constants - domain-specific message types."""

        # DOMAIN-SPECIFIC: Singer message types
        MESSAGE_TYPE_RECORD: Final[str] = "RECORD"
        MESSAGE_TYPE_SCHEMA: Final[str] = "SCHEMA"
        MESSAGE_TYPE_STATE: Final[str] = "STATE"
        MESSAGE_TYPE_METRIC: Final[str] = "METRIC"

        # DOMAIN-SPECIFIC: Version requirements
        SDK_VERSION_REQUIRED: Final[str] = "0.48.0"

        # USE FlextConstants.Defaults.PAGE_SIZE as base for batch sizes
        DEFAULT_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 10  # 1000
        MAX_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 100  # 10000
        DEFAULT_BUFFER_SIZE: Final[int] = 8192  # Buffer size is Singer-specific

        # USE FlextConstants timeouts as base
        DEFAULT_CONNECTION_TIMEOUT: Final[int] = FlextConstants.Defaults.TIMEOUT  # 30
        DEFAULT_REQUEST_TIMEOUT: Final[int] = FlextConstants.Defaults.TIMEOUT * 2  # 60
        DEFAULT_MAX_PARALLEL_STREAMS: Final[int] = 4  # Singer-specific parallelism

    class DBT:
        """DBT constants - domain-specific file names and commands."""

        # DOMAIN-SPECIFIC: DBT file names and commands
        PROJECT_FILE: Final[str] = "dbt_project.yml"
        PROFILES_FILE: Final[str] = "profiles.yml"
        MANIFEST_FILE: Final[str] = "manifest.json"
        COMMAND_RUN: Final[str] = "run"
        COMMAND_TEST: Final[str] = "test"
        COMMAND_BUILD: Final[str] = "build"
        COMMAND_COMPILE: Final[str] = "compile"

        # DOMAIN-SPECIFIC: Version requirements
        VERSION_REQUIRED: Final[str] = "1.10.5"

        # USE FlextConstants.Defaults.PAGE_SIZE as base for batch processing
        DEFAULT_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 10  # 1000
        LARGE_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 50  # 5000
        MAX_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 100  # 10000

        # DOMAIN-SPECIFIC: DBT freshness timeouts (hours)
        FRESHNESS_ERROR_AFTER: Final[int] = 24
        FRESHNESS_WARN_AFTER: Final[int] = 12

        # DOMAIN-SPECIFIC: DBT materialization strategies
        MATERIALIZATION_TABLE: Final[str] = "table"
        MATERIALIZATION_VIEW: Final[str] = "view"
        MATERIALIZATION_INCREMENTAL: Final[str] = "incremental"

    class Plugin:
        """Plugin constants using FlextConstants as SOURCE OF TRUTH."""

        # DOMAIN-SPECIFIC: Plugin configuration
        CONFIG_VERSION: Final[int] = 1
        DISCOVERY_FILENAME: Final[str] = "catalog.json"
        STATE_FILENAME: Final[str] = "state.json"
        DEFAULT_VARIANT: Final[str] = "meltanolabs"
        HUB_URL: Final[str] = "https://hub.meltano.com"
        PREFIX_TAP: Final[str] = "tap"
        PREFIX_TARGET: Final[str] = "target"

        # DOMAIN-SPECIFIC: Plugin types (no legacy aliases)
        TYPE_TAP: Final[str] = "extractor"
        TYPE_TARGET: Final[str] = "loader"
        TYPE_DBT: Final[str] = "transformer"

        # USE FlextConstants.Defaults.TIMEOUT as base for installation
        INSTALLATION_TIMEOUT: Final[int] = (
            FlextConstants.Defaults.TIMEOUT * 10
        )  # 300 seconds

        # BUSINESS RULE CONSTANTS - Domain-specific validation rules
        MIN_TARGET_PLUGIN_NAME_LENGTH: Final[int] = (
            8  # "target-" prefix + minimum 2 chars
        )
        MIN_TAP_PLUGIN_NAME_LENGTH: Final[int] = 5  # "tap-" prefix + minimum 1 char

    # =========================================================================
    # DOMAIN-SPECIFIC ENUMS - NOT available in FlextConstants
    # =========================================================================

    class PluginTypes(StrEnum):
        """DOMAIN-SPECIFIC plugin types - NOT available in FlextConstants."""

        EXTRACTORS = auto()
        LOADERS = auto()
        TRANSFORMS = auto()
        ORCHESTRATORS = auto()

    class ReplicationMethods(StrEnum):
        """Singer replication methods - domain-specific to data integration."""

        FULL_TABLE = "FULL_TABLE"
        INCREMENTAL = "INCREMENTAL"
        LOG_BASED = "LOG_BASED"  # Usage count: 0  # Usage count: 0

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


__all__ = [
    "FlextMeltanoConstants",
]

# Export nested classes for easier access
PluginTypes = FlextMeltanoConstants.PluginTypes
