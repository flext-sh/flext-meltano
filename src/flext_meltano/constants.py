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
    """DOMAIN-SPECIFIC Meltano constants."""

    # =========================================================================
    # VERSION METADATA (DOMAIN-SPECIFIC ONLY)
    # =========================================================================

    FLEXT_MELTANO_VERSION: Final[str] = "0.9.0"  # Domain-specific version

    # =========================================================================
    # DOMAIN-SPECIFIC CONSTANTS
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

    class MeltanoSpecific:
        """Meltano-specific constants moved from FlextConstants.Meltano."""

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

        # MOVED FROM FlextConstants.Meltano - Now the source of truth
        DEFAULT_TIMEOUT: Final[int] = 300  # Usage count: 2
        DISCOVERY_TIMEOUT: Final[int] = 60  # Usage count: 0
        EXTRACT_TIMEOUT: Final[int] = 1800  # Usage count: 0
        LOAD_TIMEOUT: Final[int] = 1800  # Usage count: 0
        DEFAULT_POSTGRES_PORT: Final[int] = 5432  # Usage count: 0
        DEFAULT_MYSQL_PORT: Final[int] = 3306  # Usage count: 0
        DEFAULT_ORACLE_PORT: Final[int] = 1521  # Usage count: 2

    class Singer:
        """Singer constants moved from FlextConstants.Singer."""

        # DOMAIN-SPECIFIC: Message types
        MESSAGE_TYPE_RECORD: Final[str] = "RECORD"
        MESSAGE_TYPE_SCHEMA: Final[str] = "SCHEMA"
        MESSAGE_TYPE_STATE: Final[str] = "STATE"
        MESSAGE_TYPE_METRIC: Final[str] = "METRIC"

        # DOMAIN-SPECIFIC: Version requirements
        SDK_VERSION_REQUIRED: Final[str] = "0.48.0"

        # MOVED FROM FlextConstants.Singer - Now the source of truth
        DEFAULT_BATCH_SIZE: Final[int] = 1000  # Usage count: 4
        DEFAULT_BUFFER_SIZE: Final[int] = 8192  # Usage count: 0
        MAX_BATCH_SIZE: Final[int] = 10000  # Usage count: 4
        DEFAULT_CONNECTION_TIMEOUT: Final[int] = 30  # Usage count: 0
        DEFAULT_REQUEST_TIMEOUT: Final[int] = 60  # Usage count: 0
        DEFAULT_MAX_PARALLEL_STREAMS: Final[int] = 4  # Usage count: 4

    class DBT:
        """DBT constants moved from FlextConstants.DBT."""

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

        # MOVED FROM FlextConstants.DBT - Now the source of truth
        DEFAULT_BATCH_SIZE: Final[int] = 1000  # Usage count: 1
        LARGE_BATCH_SIZE: Final[int] = 5000  # Usage count: 0
        MAX_BATCH_SIZE: Final[int] = 10000  # Usage count: 0
        FRESHNESS_ERROR_AFTER: Final[int] = 24  # Usage count: 1
        FRESHNESS_WARN_AFTER: Final[int] = 12  # Usage count: 0
        MATERIALIZATION_TABLE: Final[str] = "table"  # Usage count: 0
        MATERIALIZATION_VIEW: Final[str] = "view"  # Usage count: 0
        MATERIALIZATION_INCREMENTAL: Final[str] = "incremental"  # Usage count: 0

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

        # SOURCE OF TRUTH: Use FlextConstants.Defaults.TIMEOUT for installation
        INSTALLATION_TIMEOUT: Final[int] = (
            FlextConstants.Defaults.TIMEOUT * 10
        )  # 5 minutes

        # BUSINESS RULE CONSTANTS - Moved from validators.py (SOLID compliance)
        MIN_TARGET_PLUGIN_NAME_LENGTH: Final[int] = (
            8  # "target-" prefix + minimum 2 chars
        )
        MIN_TAP_PLUGIN_NAME_LENGTH: Final[int] = (
            5  # "tap-" prefix + minimum 1 char  # "tap-" prefix + minimum 1 char
        )

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
        """Singer replication methods moved from FlextConstants.Taps."""

        # MOVED FROM FlextConstants.Taps - Now the source of truth
        FULL_TABLE = "FULL_TABLE"  # Usage count: 2
        INCREMENTAL = "INCREMENTAL"  # Usage count: 0
        LOG_BASED = "LOG_BASED"  # Usage count: 0  # Usage count: 0


# Module-level aliases for nested enums to support imports
PluginTypes = FlextMeltanoConstants.PluginTypes
ReplicationMethods = FlextMeltanoConstants.ReplicationMethods


__all__ = [
    "FlextMeltanoConstants",
    "PluginTypes",
    "ReplicationMethods",
]
