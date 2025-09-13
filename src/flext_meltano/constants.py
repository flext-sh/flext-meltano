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
    - FlextConstants is the SINGLE SOURCE OF TRUTH for ALL general constants
    - Contains ONLY Meltano-specific constants that cannot be found in FlextConstants
    - ALL timeout, batch size, port values MUST come from FlextConstants
    """

    # =========================================================================
    # FLEXT-CORE AS SOURCE OF TRUTH - Direct delegation to avoid duplication
    # =========================================================================

    # ALL FlextConstants available as single source of truth
    # Note: Access specific namespaces like FlextConstants.Defaults, FlextConstants.Performance, etc.

    # =========================================================================
    # VERSION METADATA (DOMAIN-SPECIFIC ONLY)
    # =========================================================================

    FLEXT_MELTANO_VERSION: Final[str] = "0.9.0"  # Domain-specific version

    # =========================================================================
    # DOMAIN-SPECIFIC CONSTANTS - Use FlextConstants for performance values
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
        DEFAULT_ENVIRONMENTS: Final[list[str]] = ["dev", "staging", "prod"]

    class Meltano:
        """Meltano constants using FlextConstants as SOURCE OF TRUTH."""

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

        # SOURCE OF TRUTH: ALL performance values from FlextConstants.Meltano
        DEFAULT_TIMEOUT: Final[int] = FlextConstants.Meltano.DEFAULT_TIMEOUT
        DISCOVERY_TIMEOUT: Final[int] = FlextConstants.Meltano.DISCOVERY_TIMEOUT
        EXTRACT_TIMEOUT: Final[int] = FlextConstants.Meltano.EXTRACT_TIMEOUT
        LOAD_TIMEOUT: Final[int] = FlextConstants.Meltano.LOAD_TIMEOUT
        DEFAULT_POSTGRES_PORT: Final[int] = FlextConstants.Meltano.DEFAULT_POSTGRES_PORT
        DEFAULT_MYSQL_PORT: Final[int] = FlextConstants.Meltano.DEFAULT_MYSQL_PORT
        DEFAULT_ORACLE_PORT: Final[int] = FlextConstants.Meltano.DEFAULT_ORACLE_PORT

    class Singer:
        """Singer constants using FlextConstants as SOURCE OF TRUTH."""

        # DOMAIN-SPECIFIC: Message types
        MESSAGE_TYPE_RECORD: Final[str] = "RECORD"
        MESSAGE_TYPE_SCHEMA: Final[str] = "SCHEMA"
        MESSAGE_TYPE_STATE: Final[str] = "STATE"
        MESSAGE_TYPE_METRIC: Final[str] = "METRIC"

        # DOMAIN-SPECIFIC: Version requirements
        SDK_VERSION_REQUIRED: Final[str] = "0.48.0"

        # SOURCE OF TRUTH: ALL performance values from FlextConstants.Singer
        DEFAULT_BATCH_SIZE: Final[int] = FlextConstants.Singer.DEFAULT_BATCH_SIZE
        DEFAULT_BUFFER_SIZE: Final[int] = FlextConstants.Singer.DEFAULT_BUFFER_SIZE
        MAX_BATCH_SIZE: Final[int] = FlextConstants.Singer.MAX_BATCH_SIZE
        DEFAULT_CONNECTION_TIMEOUT: Final[int] = (
            FlextConstants.Singer.DEFAULT_CONNECTION_TIMEOUT
        )
        DEFAULT_REQUEST_TIMEOUT: Final[int] = (
            FlextConstants.Singer.DEFAULT_REQUEST_TIMEOUT
        )
        DEFAULT_MAX_PARALLEL_STREAMS: Final[int] = (
            FlextConstants.Singer.DEFAULT_MAX_PARALLEL_STREAMS
        )

    class DBT:
        """DBT constants using FlextConstants as SOURCE OF TRUTH."""

        # DOMAIN-SPECIFIC: File names and commands
        PROJECT_FILE: Final[str] = "dbt_project.yml"
        PROFILES_FILE: Final[str] = "profiles.yml"
        MANIFEST_FILE: Final[str] = "manifest.json"
        COMMAND_RUN: Final[str] = "run"
        COMMAND_TEST: Final[str] = "test"
        COMMAND_BUILD: Final[str] = "build"
        COMMAND_COMPILE: Final[str] = "compile"

        # DOMAIN-SPECIFIC: Version requirements
        VERSION_REQUIRED: Final[str] = "1.10.5"

        # SOURCE OF TRUTH: ALL performance values from FlextConstants.DBT
        DEFAULT_BATCH_SIZE: Final[int] = FlextConstants.DBT.DEFAULT_BATCH_SIZE
        LARGE_BATCH_SIZE: Final[int] = FlextConstants.DBT.LARGE_BATCH_SIZE
        MAX_BATCH_SIZE: Final[int] = FlextConstants.DBT.MAX_BATCH_SIZE
        FRESHNESS_ERROR_AFTER: Final[int] = FlextConstants.DBT.FRESHNESS_ERROR_AFTER
        FRESHNESS_WARN_AFTER: Final[int] = FlextConstants.DBT.FRESHNESS_WARN_AFTER
        MATERIALIZATION_TABLE: Final[str] = FlextConstants.DBT.MATERIALIZATION_TABLE
        MATERIALIZATION_VIEW: Final[str] = FlextConstants.DBT.MATERIALIZATION_VIEW
        MATERIALIZATION_INCREMENTAL: Final[str] = (
            FlextConstants.DBT.MATERIALIZATION_INCREMENTAL
        )

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

        # Ultra-simple aliases for test compatibility
        TYPE_TAP: Final[str] = "extractor"
        TYPE_TARGET: Final[str] = "loader"
        TYPE_DBT: Final[str] = "transformer"

        # SOURCE OF TRUTH: Use FlextConstants.Defaults.TIMEOUT for installation
        INSTALLATION_TIMEOUT: Final[int] = (
            FlextConstants.Defaults.TIMEOUT * 10
        )  # 5 minutes

        # BUSINESS RULE CONSTANTS - Moved from validators.py (SOLID compliance)
        MIN_TARGET_PLUGIN_NAME_LENGTH: Final[int] = (
            8  # "target-" prefix + minimum 2 chars
        )
        MIN_TAP_PLUGIN_NAME_LENGTH: Final[int] = 5  # "tap-" prefix + minimum 1 char

    # =========================================================================
    # NESTED ENUMS - Using FlextConstants.Taps replication methods as SOURCE OF TRUTH
    # =========================================================================

    class PluginTypes(StrEnum):
        """DOMAIN-SPECIFIC plugin types - NOT available in FlextConstants."""

        EXTRACTORS = auto()
        LOADERS = auto()
        TRANSFORMS = auto()
        ORCHESTRATORS = auto()

    class ReplicationMethods(StrEnum):
        """Singer replication methods using FlextConstants.Taps as SOURCE OF TRUTH."""

        # Use FlextConstants.Taps values to avoid duplication
        FULL_TABLE = FlextConstants.Taps.FULL_REPLICATION
        INCREMENTAL = FlextConstants.Taps.INCREMENTAL_REPLICATION
        LOG_BASED = FlextConstants.Taps.LOG_BASED_REPLICATION


# Module-level aliases for nested enums to support imports
PluginTypes = FlextMeltanoConstants.PluginTypes
ReplicationMethods = FlextMeltanoConstants.ReplicationMethods


__all__ = [
    "FlextMeltanoConstants",
    "PluginTypes",
    "ReplicationMethods",
]
