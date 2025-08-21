"""Core constants and enums for flext-meltano.

Follows the same pattern as flext-core constants.py for consistency
across the FLEXT ecosystem.
"""

from __future__ import annotations

from enum import StrEnum
from typing import ClassVar, Final

from flext_core.constants import FlextConstants as CoreConstants


class FlextMeltanoConstants(CoreConstants):
    """Central container for all flext-meltano constants.

    Extends flext-core constants and adds Meltano-specific ones.
    Organizes constants into logical categories with type safety.
    """

    # Class-level error codes mapping
    ERROR_CODES: ClassVar[dict[str, str]] = {}

    class MeltanoCore:
        """Meltano core constants."""

        NAME = "FLEXT-MELTANO"
        VERSION = "2.0.0-enterprise"
        DESCRIPTION = "Enterprise Data Integration Bridge"
        ARCHITECTURE = "bridge_pattern"

    class Environment:
        """Environment configuration constants."""

        DEFAULT = "dev"
        SUPPORTED = ("dev", "test", "staging", "production")
        VAR_PREFIX = "FLEXT_MELTANO"

    class Meltano:
        """Meltano-specific constants."""

        DEFAULT_PROJECT_NAME = "meltano_project"
        CONFIG_FILE = "meltano.yml"
        STATE_DIR = ".meltano"
        LOGS_DIR = "logs"

        # Plugin types
        EXTRACTOR = "extractor"
        LOADER = "loader"
        TRANSFORMER = "transformer"
        ORCHESTRATOR = "orchestrator"
        UTILITY = "utility"

        SUPPORTED_PLUGIN_TYPES = (
            EXTRACTOR,
            LOADER,
            TRANSFORMER,
            ORCHESTRATOR,
            UTILITY,
        )

    class Singer:
        """Singer protocol constants."""

        SCHEMA_MESSAGE = "SCHEMA"
        RECORD_MESSAGE = "RECORD"
        STATE_MESSAGE = "STATE"

        MESSAGE_TYPES = (
            SCHEMA_MESSAGE,
            RECORD_MESSAGE,
            STATE_MESSAGE,
        )

        # Stream selection modes
        ALL_STREAMS = "all"
        AUTOMATIC = "automatic"
        MANUAL = "manual"

    class DBT:
        """DBT integration constants."""

        PROJECT_FILE = "dbt_project.yml"
        PROFILES_FILE = "profiles.yml"
        PACKAGES_FILE = "packages.yml"

        # DBT directories
        MODELS_DIR = "models"
        MACROS_DIR = "macros"
        SEEDS_DIR = "seeds"
        SNAPSHOTS_DIR = "snapshots"
        TESTS_DIR = "tests"
        DOCS_DIR = "docs"

        # DBT commands
        RUN = "run"
        TEST = "test"
        BUILD = "build"
        COMPILE = "compile"
        PARSE = "parse"
        DOCS = "docs"

    class Execution:
        """Execution and pipeline constants."""

        DEFAULT_TIMEOUT = 300  # 5 minutes
        MAX_TIMEOUT = 3600  # 1 hour

        # Exit codes
        SUCCESS = 0
        GENERAL_ERROR = 1
        CONFIG_ERROR = 2
        CONNECTION_ERROR = 3
        VALIDATION_ERROR = 4

    class Bridge:
        """Bridge integration constants."""

        JSON_SUCCESS_KEY = "success"
        JSON_DATA_KEY = "data"
        JSON_ERROR_KEY = "error"
        JSON_MESSAGE_KEY = "message"

        DEFAULT_BRIDGE_PORT = 8080
        DEFAULT_TIMEOUT = 30


class PluginType(StrEnum):
    """Meltano plugin types enumeration."""

    EXTRACTOR = "extractor"
    LOADER = "loader"
    TRANSFORMER = "transformer"
    ORCHESTRATOR = "orchestrator"
    UTILITY = "utility"


class SingerMessageType(StrEnum):
    """Singer message types enumeration."""

    SCHEMA = "SCHEMA"
    RECORD = "RECORD"
    STATE = "STATE"


class ExecutionStatus(StrEnum):
    """Execution status enumeration."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


# Convenience aliases for backward compatibility
FlextConstants = FlextMeltanoConstants
FLEXT_MELTANO_VERSION: Final[str] = FlextMeltanoConstants.Core.VERSION
DEFAULT_ENVIRONMENT: Final[str] = FlextMeltanoConstants.Environment.DEFAULT
SUPPORTED_ENVIRONMENTS = FlextMeltanoConstants.Environment.SUPPORTED

# Type aliases expected by models
FlextMeltanoPluginType = PluginType
FlextSingerMessageType = SingerMessageType


__all__ = [
    # Aliases
    "DEFAULT_ENVIRONMENT",
    "FLEXT_MELTANO_VERSION",
    "SUPPORTED_ENVIRONMENTS",
    "ExecutionStatus",
    "FlextConstants",
    # Classes
    "FlextMeltanoConstants",
    "FlextMeltanoPluginType",
    "FlextSingerMessageType",
    "PluginType",
    "SingerMessageType",
]
