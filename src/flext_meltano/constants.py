"""FLEXT Meltano Constants - Meltano-specific constants ONLY.

Provides ONLY Meltano-specific constants that extend FlextConstants.
Follows SOURCE OF TRUTH principle - use FlextConstants for common values.

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


class FlextMeltanoConstants(FlextConstants):
    """Meltano-specific constants ONLY extending FlextConstants.

    SOURCE OF TRUTH: Use FlextConstants for common values.
    This class contains ONLY Meltano/Singer/DBT specific constants.
    """

    # =========================================================================
    # MELTANO DOMAIN - Meltano-specific constants ONLY
    # =========================================================================

    class Meltano:
        """Meltano-specific constants - NOT duplicating FlextConstants."""

        # Meltano ecosystem versions (Meltano-specific)
        VERSION_REQUIRED: Final[str] = "3.9.1"
        PROJECT_FILE: Final[str] = "meltano.yml"
        STATE_DIR: Final[str] = ".meltano"
        
        # Meltano CLI commands (Meltano-specific)
        COMMAND_INSTALL: Final[str] = "install"
        COMMAND_RUN: Final[str] = "run"
        COMMAND_ELT: Final[str] = "elt"

    # =========================================================================
    # SINGER SDK DOMAIN - Singer-specific constants ONLY
    # =========================================================================

    class Singer:
        """Singer SDK constants - ONLY Singer-specific values."""

        # Singer-specific versions
        SDK_VERSION_REQUIRED: Final[str] = "0.48.0"
        
        # Singer message types (Singer-specific)
        MESSAGE_TYPE_RECORD: Final[str] = "RECORD"
        MESSAGE_TYPE_SCHEMA: Final[str] = "SCHEMA"
        MESSAGE_TYPE_STATE: Final[str] = "STATE"
        MESSAGE_TYPE_METRIC: Final[str] = "METRIC"
        
        # Singer stream processing (Singer-specific)
        MAX_CONCURRENT_STREAMS: Final[int] = 10

    # =========================================================================
    # DBT DOMAIN - DBT-specific constants ONLY
    # =========================================================================

    class DBT:
        """DBT constants - ONLY DBT-specific values."""

        # DBT-specific versions
        VERSION_REQUIRED: Final[str] = "1.10.5"
        
        # DBT files (DBT-specific)
        PROJECT_FILE: Final[str] = "dbt_project.yml"
        PROFILES_FILE: Final[str] = "profiles.yml"
        MANIFEST_FILE: Final[str] = "manifest.json"
        
        # DBT commands (DBT-specific)
        COMMAND_RUN: Final[str] = "run"
        COMMAND_TEST: Final[str] = "test"
        COMMAND_BUILD: Final[str] = "build"
        COMMAND_COMPILE: Final[str] = "compile"
        
        # DBT materializations (DBT-specific)
        MATERIALIZATION_TABLE: Final[str] = "table"
        MATERIALIZATION_VIEW: Final[str] = "view"
        MATERIALIZATION_INCREMENTAL: Final[str] = "incremental"

    # =========================================================================
    # PLUGIN DOMAIN - Meltano plugin constants ONLY
    # =========================================================================

    class Plugin:
        """Meltano plugin constants - ONLY plugin-specific values."""

        # Plugin types (Meltano-specific)
        TYPE_TAP: Final[PluginType] = "extractors"
        TYPE_TARGET: Final[PluginType] = "loaders"
        TYPE_TRANSFORM: Final[PluginType] = "transforms"
        
        # Plugin sources (Meltano-specific)
        DEFAULT_VARIANT: Final[str] = "meltanolabs"
        HUB_URL: Final[str] = "https://hub.meltano.com"
        
        # Plugin timeouts (use FlextConstants.Network.DEFAULT_TIMEOUT where possible)
        INSTALLATION_TIMEOUT: Final[int] = 300  # 5 minutes - plugin-specific


# =========================================================================
# ENUMS - Modern Python 3.13+ StrEnum for type safety
# =========================================================================

class PluginTypes(StrEnum):
    """Meltano plugin types - Modern StrEnum."""
    EXTRACTORS = auto()
    LOADERS = auto()
    TRANSFORMS = auto()
    ORCHESTRATORS = auto()

class ReplicationMethods(StrEnum):
    """Singer replication methods - Modern StrEnum."""
    FULL_TABLE = auto()
    INCREMENTAL = auto()
    LOG_BASED = auto()


__all__ = [
    "FlextMeltanoConstants",
    "PluginTypes", 
    "ReplicationMethods",
]
