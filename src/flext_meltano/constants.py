"""Constants for flext-meltano.

Single place for constant values used across the library.
All constants follow SCREAMING_SNAKE_CASE naming convention.
"""
from __future__ import annotations

from enum import Enum
from typing import Final

# =============================================================================
# VERSION AND METADATA
# =============================================================================

FLEXT_MELTANO_VERSION: Final[str] = "2.0.0-enterprise"
FLEXT_MELTANO_NAME: Final[str] = "flext-meltano"

# =============================================================================
# ENVIRONMENT CONFIGURATION
# =============================================================================

DEFAULT_ENVIRONMENT: Final[str] = "dev"
SUPPORTED_ENVIRONMENTS: Final[tuple[str, ...]] = (
    "dev",
    "test",
    "staging",
    "production",
)

# =============================================================================
# SINGER PROTOCOL CONSTANTS
# =============================================================================

SINGER_MESSAGE_TYPES: Final[tuple[str, ...]] = ("RECORD", "SCHEMA", "STATE")
SINGER_SPEC_VERSION: Final[str] = "1.5.0"

# Singer message type constants
SINGER_RECORD_TYPE: Final[str] = "RECORD"
SINGER_SCHEMA_TYPE: Final[str] = "SCHEMA"
SINGER_STATE_TYPE: Final[str] = "STATE"

# Singer tap/target types
SINGER_TAP_TYPE: Final[str] = "extractors"
SINGER_TARGET_TYPE: Final[str] = "loaders"
SINGER_TRANSFORM_TYPE: Final[str] = "transformers"

# =============================================================================
# MELTANO CONFIGURATION
# =============================================================================

DEFAULT_MELTANO_PROJECT_ROOT: Final[str] = "."
DEFAULT_MELTANO_DATABASE: Final[str] = "sqlite:///meltano.db"
DEFAULT_MELTANO_UI_PORT: Final[int] = 5000

# Meltano plugin types
MELTANO_PLUGIN_TYPES: Final[tuple[str, ...]] = (
    "extractors",
    "loaders",
    "transformers",
    "orchestrators",
    "utilities",
    "files",
)

# =============================================================================
# DBT CONFIGURATION
# =============================================================================

DEFAULT_DBT_PROFILES_DIR: Final[str] = "~/.dbt"
DEFAULT_DBT_PROJECT_DIR: Final[str] = "./dbt"
DEFAULT_DBT_TARGET: Final[str] = "dev"

# =============================================================================
# BRIDGE INTEGRATION
# =============================================================================

# JSON response keys for Go integration
BRIDGE_SUCCESS_KEY: Final[str] = "success"
BRIDGE_DATA_KEY: Final[str] = "data"
BRIDGE_ERROR_KEY: Final[str] = "error"
BRIDGE_MESSAGE_KEY: Final[str] = "message"

# Bridge operation types
BRIDGE_VERSION_OP: Final[str] = "version"
BRIDGE_LIST_PLUGINS_OP: Final[str] = "list_plugins"
BRIDGE_RUN_PIPELINE_OP: Final[str] = "run_pipeline"
BRIDGE_DISCOVER_CATALOG_OP: Final[str] = "discover_catalog"

# =============================================================================
# TIMEOUT AND PERFORMANCE
# =============================================================================

DEFAULT_COMMAND_TIMEOUT: Final[int] = 300  # 5 minutes
DEFAULT_CONNECTION_TIMEOUT: Final[int] = 30  # 30 seconds
DEFAULT_DISCOVERY_TIMEOUT: Final[int] = 60  # 1 minute

# =============================================================================
# ERROR CODES AND MESSAGES
# =============================================================================

ERROR_CODE_CONFIGURATION: Final[str] = "MELTANO_CONFIG_ERROR"
ERROR_CODE_CONNECTION: Final[str] = "MELTANO_CONNECTION_ERROR"
ERROR_CODE_EXECUTION: Final[str] = "MELTANO_EXECUTION_ERROR"
ERROR_CODE_PLUGIN: Final[str] = "MELTANO_PLUGIN_ERROR"
ERROR_CODE_SINGER: Final[str] = "MELTANO_SINGER_ERROR"
ERROR_CODE_DBT: Final[str] = "MELTANO_DBT_ERROR"

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

DEFAULT_LOG_LEVEL: Final[str] = "INFO"
LOG_FORMAT_JSON: Final[str] = "json"
LOG_FORMAT_TEXT: Final[str] = "text"

# =============================================================================
# ENUMS FOR TYPE SAFETY
# =============================================================================


class FlextMeltanoEnvironment(str, Enum):
    """Supported Meltano environments."""

    DEV = "dev"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class FlextSingerMessageType(str, Enum):
    """Singer message types."""

    RECORD = "RECORD"
    SCHEMA = "SCHEMA"
    STATE = "STATE"


class FlextMeltanoPluginType(str, Enum):
    """Meltano plugin types."""

    EXTRACTORS = "extractors"
    LOADERS = "loaders"
    TRANSFORMERS = "transformers"
    ORCHESTRATORS = "orchestrators"
    UTILITIES = "utilities"
    FILES = "files"


class FlextBridgeOperation(str, Enum):
    """Bridge operation types."""

    VERSION = "version"
    LIST_PLUGINS = "list_plugins"
    RUN_PIPELINE = "run_pipeline"
    DISCOVER_CATALOG = "discover_catalog"


class FlextMeltanoLogLevel(str, Enum):
    """Log levels for Meltano operations."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


__all__ = [
    # Bridge integration
    "BRIDGE_DATA_KEY",
    "BRIDGE_DISCOVER_CATALOG_OP",
    "BRIDGE_ERROR_KEY",
    "BRIDGE_LIST_PLUGINS_OP",
    "BRIDGE_MESSAGE_KEY",
    "BRIDGE_RUN_PIPELINE_OP",
    "BRIDGE_SUCCESS_KEY",
    "BRIDGE_VERSION_OP",
    # Timeouts
    "DEFAULT_COMMAND_TIMEOUT",
    "DEFAULT_CONNECTION_TIMEOUT",
    # DBT configuration
    "DEFAULT_DBT_PROFILES_DIR",
    "DEFAULT_DBT_PROJECT_DIR",
    "DEFAULT_DBT_TARGET",
    "DEFAULT_DISCOVERY_TIMEOUT",
    # Environment
    "DEFAULT_ENVIRONMENT",
    # Logging
    "DEFAULT_LOG_LEVEL",
    # Meltano configuration
    "DEFAULT_MELTANO_DATABASE",
    "DEFAULT_MELTANO_PROJECT_ROOT",
    "DEFAULT_MELTANO_UI_PORT",
    # Error codes
    "ERROR_CODE_CONFIGURATION",
    "ERROR_CODE_CONNECTION",
    "ERROR_CODE_DBT",
    "ERROR_CODE_EXECUTION",
    "ERROR_CODE_PLUGIN",
    "ERROR_CODE_SINGER",
    # Version and metadata
    "FLEXT_MELTANO_NAME",
    "FLEXT_MELTANO_VERSION",
    # Logging
    "LOG_FORMAT_JSON",
    "LOG_FORMAT_TEXT",
    # Meltano configuration
    "MELTANO_PLUGIN_TYPES",
    # Singer protocol
    "SINGER_MESSAGE_TYPES",
    "SINGER_RECORD_TYPE",
    "SINGER_SCHEMA_TYPE",
    "SINGER_SPEC_VERSION",
    "SINGER_STATE_TYPE",
    "SINGER_TAP_TYPE",
    "SINGER_TARGET_TYPE",
    "SINGER_TRANSFORM_TYPE",
    # Environment
    "SUPPORTED_ENVIRONMENTS",
    # Enums
    "FlextBridgeOperation",
    "FlextMeltanoEnvironment",
    "FlextMeltanoLogLevel",
    "FlextMeltanoPluginType",
    "FlextSingerMessageType",
]
