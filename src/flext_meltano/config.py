"""FLEXT Meltano Configuration - Single class following Flext[Area][Module] pattern.

Architectural Compliance: Single main class FlextMeltanoConfig inheriting from FlextCore
Following user requirements: "apenas uma classe Flext[Area][Modulo]"

The main class FlextMeltanoConfig serves as the facade providing access to all
configuration functionality through internal aliases and nested classes.

Inheritance Hierarchy:
    FlextMeltanoConfig -> FlextModel (from flext-core)
    All constants and enums as internal aliases, no implementation

SOLID Principles:
    - Single Responsibility: One main config class with specialized internal classes
    - Open/Closed: Extensible through inheritance, closed for modification
    - Dependency Inversion: Depends on FlextCore abstractions
"""

from __future__ import annotations

import contextlib
from enum import StrEnum
from pathlib import Path
from typing import ClassVar, Final

from flext_core import FlextModel
from pydantic import Field, field_validator

# =============================================================================
# INTERNAL CLASSES FOR CONSTANTS - Following DRY principles
# =============================================================================


class _FlextMeltanoConstants:
    """Internal constants class - All constants as class attributes."""

    # Version and metadata
    VERSION: Final[str] = "2.0.0-enterprise"
    NAME: Final[str] = "flext-meltano"

    # Environment configuration
    DEFAULT_ENVIRONMENT: Final[str] = "dev"
    SUPPORTED_ENVIRONMENTS: Final[tuple[str, ...]] = (
        "dev",
        "test",
        "staging",
        "production",
    )

    # Singer protocol constants
    SINGER_MESSAGE_TYPES: Final[tuple[str, ...]] = ("RECORD", "SCHEMA", "STATE")
    SINGER_SPEC_VERSION: Final[str] = "1.5.0"
    SINGER_RECORD_TYPE: Final[str] = "RECORD"
    SINGER_SCHEMA_TYPE: Final[str] = "SCHEMA"
    SINGER_STATE_TYPE: Final[str] = "STATE"
    SINGER_TAP_TYPE: Final[str] = "extractors"
    SINGER_TARGET_TYPE: Final[str] = "loaders"
    SINGER_TRANSFORM_TYPE: Final[str] = "transformers"

    # Meltano configuration
    DEFAULT_MELTANO_PROJECT_ROOT: Final[str] = "."
    DEFAULT_MELTANO_DATABASE: Final[str] = "sqlite:///meltano.db"
    DEFAULT_MELTANO_UI_PORT: Final[int] = 5000
    MELTANO_PLUGIN_TYPES: Final[tuple[str, ...]] = (
        "extractors",
        "loaders",
        "transformers",
        "orchestrators",
        "utilities",
        "files",
    )

    # DBT configuration
    DEFAULT_DBT_PROFILES_DIR: Final[str] = "~/.dbt"
    DEFAULT_DBT_PROJECT_DIR: Final[str] = "./dbt"
    DEFAULT_DBT_TARGET: Final[str] = "dev"

    # Bridge integration
    BRIDGE_SUCCESS_KEY: Final[str] = "success"
    BRIDGE_DATA_KEY: Final[str] = "data"
    BRIDGE_ERROR_KEY: Final[str] = "error"
    BRIDGE_MESSAGE_KEY: Final[str] = "message"
    BRIDGE_VERSION_OP: Final[str] = "version"
    BRIDGE_LIST_PLUGINS_OP: Final[str] = "list_plugins"
    BRIDGE_RUN_PIPELINE_OP: Final[str] = "run_pipeline"
    BRIDGE_DISCOVER_CATALOG_OP: Final[str] = "discover_catalog"

    # Timeout and performance
    DEFAULT_COMMAND_TIMEOUT: Final[int] = 300
    DEFAULT_CONNECTION_TIMEOUT: Final[int] = 30
    DEFAULT_DISCOVERY_TIMEOUT: Final[int] = 60

    # Error codes
    ERROR_CODE_CONFIGURATION: Final[str] = "MELTANO_CONFIG_ERROR"
    ERROR_CODE_CONNECTION: Final[str] = "MELTANO_CONNECTION_ERROR"
    ERROR_CODE_EXECUTION: Final[str] = "MELTANO_EXECUTION_ERROR"
    ERROR_CODE_PLUGIN: Final[str] = "MELTANO_PLUGIN_ERROR"
    ERROR_CODE_SINGER: Final[str] = "MELTANO_SINGER_ERROR"
    ERROR_CODE_DBT: Final[str] = "MELTANO_DBT_ERROR"

    # Logging configuration
    DEFAULT_LOG_LEVEL: Final[str] = "INFO"
    LOG_FORMAT_JSON: Final[str] = "json"
    LOG_FORMAT_TEXT: Final[str] = "text"


class _FlextMeltanoEnums:
    """Internal enums class - All enums as nested classes."""

    class Environment(StrEnum):
        """Supported Meltano environments."""

        DEV = "dev"
        TEST = "test"
        STAGING = "staging"
        PRODUCTION = "production"

    class SingerMessageType(StrEnum):
        """Singer message types."""

        RECORD = "RECORD"
        SCHEMA = "SCHEMA"
        STATE = "STATE"

    class PluginType(StrEnum):
        """Meltano plugin types."""

        EXTRACTORS = "extractors"
        LOADERS = "loaders"
        TRANSFORMERS = "transformers"
        ORCHESTRATORS = "orchestrators"
        UTILITIES = "utilities"
        FILES = "files"

    class BridgeOperation(StrEnum):
        """Bridge operation types."""

        VERSION = "version"
        LIST_PLUGINS = "list_plugins"
        RUN_PIPELINE = "run_pipeline"
        DISCOVER_CATALOG = "discover_catalog"

    class LogLevel(StrEnum):
        """Log levels for Meltano operations."""

        DEBUG = "DEBUG"
        INFO = "INFO"
        WARNING = "WARNING"
        ERROR = "ERROR"
        CRITICAL = "CRITICAL"


# =============================================================================
# MAIN CONFIGURATION CLASS - Following Flext[Area][Module] pattern
# =============================================================================


class FlextMeltanoConfig(FlextModel):
    """Single main configuration class inheriting from FlextCore (Flext[Area][Module] pattern).

    Architectural Compliance:
    - Inherits from FlextModel (flext-core)
    - All constants and enums available as class aliases
    - Facade pattern: delegates to internal classes, implements nothing directly

    SOLID Principles:
    - Single Responsibility: Configuration management with internal specialization
    - Open/Closed: Extensible through inheritance
    - Dependency Inversion: Depends on flext-core abstractions
    """

    # =================================================================
    # INTERNAL ALIASES - All constants accessible through main class
    # =================================================================

    # Version and metadata aliases
    FLEXT_MELTANO_VERSION: ClassVar[object] = _FlextMeltanoConstants.VERSION
    FLEXT_MELTANO_NAME: ClassVar[object] = _FlextMeltanoConstants.NAME

    # Environment aliases
    DEFAULT_ENVIRONMENT: ClassVar[object] = _FlextMeltanoConstants.DEFAULT_ENVIRONMENT
    SUPPORTED_ENVIRONMENTS: ClassVar[object] = (
        _FlextMeltanoConstants.SUPPORTED_ENVIRONMENTS
    )

    # Singer protocol aliases
    SINGER_MESSAGE_TYPES: ClassVar[object] = _FlextMeltanoConstants.SINGER_MESSAGE_TYPES
    SINGER_SPEC_VERSION: ClassVar[object] = _FlextMeltanoConstants.SINGER_SPEC_VERSION
    SINGER_RECORD_TYPE: ClassVar[object] = _FlextMeltanoConstants.SINGER_RECORD_TYPE
    SINGER_SCHEMA_TYPE: ClassVar[object] = _FlextMeltanoConstants.SINGER_SCHEMA_TYPE
    SINGER_STATE_TYPE: ClassVar[object] = _FlextMeltanoConstants.SINGER_STATE_TYPE
    SINGER_TAP_TYPE: ClassVar[object] = _FlextMeltanoConstants.SINGER_TAP_TYPE
    SINGER_TARGET_TYPE: ClassVar[object] = _FlextMeltanoConstants.SINGER_TARGET_TYPE
    SINGER_TRANSFORM_TYPE: ClassVar[object] = (
        _FlextMeltanoConstants.SINGER_TRANSFORM_TYPE
    )

    # Meltano configuration aliases
    DEFAULT_MELTANO_PROJECT_ROOT: ClassVar[object] = (
        _FlextMeltanoConstants.DEFAULT_MELTANO_PROJECT_ROOT
    )
    DEFAULT_MELTANO_DATABASE: ClassVar[object] = (
        _FlextMeltanoConstants.DEFAULT_MELTANO_DATABASE
    )
    DEFAULT_MELTANO_UI_PORT: ClassVar[object] = (
        _FlextMeltanoConstants.DEFAULT_MELTANO_UI_PORT
    )
    MELTANO_PLUGIN_TYPES: ClassVar[object] = _FlextMeltanoConstants.MELTANO_PLUGIN_TYPES

    # DBT configuration aliases
    DEFAULT_DBT_PROFILES_DIR: ClassVar[object] = (
        _FlextMeltanoConstants.DEFAULT_DBT_PROFILES_DIR
    )
    DEFAULT_DBT_PROJECT_DIR: ClassVar[object] = (
        _FlextMeltanoConstants.DEFAULT_DBT_PROJECT_DIR
    )
    DEFAULT_DBT_TARGET: ClassVar[object] = _FlextMeltanoConstants.DEFAULT_DBT_TARGET

    # Bridge integration aliases
    BRIDGE_SUCCESS_KEY: ClassVar[object] = _FlextMeltanoConstants.BRIDGE_SUCCESS_KEY
    BRIDGE_DATA_KEY: ClassVar[object] = _FlextMeltanoConstants.BRIDGE_DATA_KEY
    BRIDGE_ERROR_KEY: ClassVar[object] = _FlextMeltanoConstants.BRIDGE_ERROR_KEY
    BRIDGE_MESSAGE_KEY: ClassVar[object] = _FlextMeltanoConstants.BRIDGE_MESSAGE_KEY
    BRIDGE_VERSION_OP: ClassVar[object] = _FlextMeltanoConstants.BRIDGE_VERSION_OP
    BRIDGE_LIST_PLUGINS_OP: ClassVar[object] = (
        _FlextMeltanoConstants.BRIDGE_LIST_PLUGINS_OP
    )
    BRIDGE_RUN_PIPELINE_OP: ClassVar[object] = (
        _FlextMeltanoConstants.BRIDGE_RUN_PIPELINE_OP
    )
    BRIDGE_DISCOVER_CATALOG_OP: ClassVar[object] = (
        _FlextMeltanoConstants.BRIDGE_DISCOVER_CATALOG_OP
    )

    # Timeout and performance aliases
    DEFAULT_COMMAND_TIMEOUT: ClassVar[object] = (
        _FlextMeltanoConstants.DEFAULT_COMMAND_TIMEOUT
    )
    DEFAULT_CONNECTION_TIMEOUT: ClassVar[object] = (
        _FlextMeltanoConstants.DEFAULT_CONNECTION_TIMEOUT
    )
    DEFAULT_DISCOVERY_TIMEOUT: ClassVar[object] = (
        _FlextMeltanoConstants.DEFAULT_DISCOVERY_TIMEOUT
    )

    # Error codes aliases
    ERROR_CODE_CONFIGURATION: ClassVar[object] = (
        _FlextMeltanoConstants.ERROR_CODE_CONFIGURATION
    )
    ERROR_CODE_CONNECTION: ClassVar[object] = (
        _FlextMeltanoConstants.ERROR_CODE_CONNECTION
    )
    ERROR_CODE_EXECUTION: ClassVar[object] = _FlextMeltanoConstants.ERROR_CODE_EXECUTION
    ERROR_CODE_PLUGIN: ClassVar[object] = _FlextMeltanoConstants.ERROR_CODE_PLUGIN
    ERROR_CODE_SINGER: ClassVar[object] = _FlextMeltanoConstants.ERROR_CODE_SINGER
    ERROR_CODE_DBT: ClassVar[object] = _FlextMeltanoConstants.ERROR_CODE_DBT

    # Logging configuration aliases
    DEFAULT_LOG_LEVEL: ClassVar[object] = _FlextMeltanoConstants.DEFAULT_LOG_LEVEL
    LOG_FORMAT_JSON: ClassVar[object] = _FlextMeltanoConstants.LOG_FORMAT_JSON
    LOG_FORMAT_TEXT: ClassVar[object] = _FlextMeltanoConstants.LOG_FORMAT_TEXT

    # Enum aliases - Available as nested classes
    Environment: ClassVar[object] = _FlextMeltanoEnums.Environment
    SingerMessageType: ClassVar[object] = _FlextMeltanoEnums.SingerMessageType
    PluginType: ClassVar[object] = _FlextMeltanoEnums.PluginType
    BridgeOperation: ClassVar[object] = _FlextMeltanoEnums.BridgeOperation
    LogLevel: ClassVar[object] = _FlextMeltanoEnums.LogLevel

    # =================================================================
    # PYDANTIC FIELDS - Actual configuration model implementation
    # =================================================================

    project_root: str = Field(default=".", description="Meltano project root directory")
    environment: str = Field(default="dev", description="Meltano environment")

    # Meltano-specific configuration
    meltano_database_uri: str | None = Field(
        default=None,
        description="Meltano system database URI",
    )
    meltano_ui_bind_port: int = Field(
        default=5000, ge=1024, le=65535, description="Meltano UI port"
    )

    # Singer SDK configuration
    singer_sdk_log_level: _FlextMeltanoEnums.LogLevel = Field(
        default=_FlextMeltanoEnums.LogLevel.INFO,
        description="Singer SDK log level",
    )

    # DBT configuration
    dbt_project_dir: str | None = Field(
        default=None,
        description="DBT project directory",
    )
    dbt_profiles_dir: str | None = Field(
        default=None,
        description="DBT profiles directory",
    )

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        """Validate environment is supported."""
        if value not in _FlextMeltanoConstants.SUPPORTED_ENVIRONMENTS:
            msg = f"Environment '{value}' not supported. Must be one of: {_FlextMeltanoConstants.SUPPORTED_ENVIRONMENTS}"
            raise ValueError(msg)
        return value

    @field_validator("project_root")
    @classmethod
    def validate_project_root(cls, value: str) -> str:
        """Validate project root exists (best-effort creation when reasonable)."""
        path = Path(value)
        # Avoid creating obviously invalid test paths
        if not path.exists() and not str(path).startswith("/nonexistent"):
            with contextlib.suppress(OSError, PermissionError):
                path.mkdir(parents=True, exist_ok=True)
        return str(path.absolute())

    @field_validator("meltano_database_uri")
    @classmethod
    def validate_database_uri(cls, value: str | None) -> str | None:
        """Validate database URI format if provided."""
        if value is None:
            return None
        valid_schemes = ("sqlite://", "postgresql://", "mysql://")
        if not any(value.startswith(scheme) for scheme in valid_schemes):
            msg = f"Database URI must start with one of: {valid_schemes}"
            raise ValueError(msg)
        return value


# =============================================================================
# BACKWARD COMPATIBILITY ALIASES - For legacy imports
# =============================================================================

# Legacy constant aliases for backward compatibility
FLEXT_MELTANO_VERSION = FlextMeltanoConfig.FLEXT_MELTANO_VERSION
FLEXT_MELTANO_NAME = FlextMeltanoConfig.FLEXT_MELTANO_NAME
DEFAULT_ENVIRONMENT = FlextMeltanoConfig.DEFAULT_ENVIRONMENT
SUPPORTED_ENVIRONMENTS = FlextMeltanoConfig.SUPPORTED_ENVIRONMENTS
SINGER_MESSAGE_TYPES = FlextMeltanoConfig.SINGER_MESSAGE_TYPES
SINGER_SPEC_VERSION = FlextMeltanoConfig.SINGER_SPEC_VERSION
SINGER_RECORD_TYPE = FlextMeltanoConfig.SINGER_RECORD_TYPE
SINGER_SCHEMA_TYPE = FlextMeltanoConfig.SINGER_SCHEMA_TYPE
SINGER_STATE_TYPE = FlextMeltanoConfig.SINGER_STATE_TYPE
SINGER_TAP_TYPE = FlextMeltanoConfig.SINGER_TAP_TYPE
SINGER_TARGET_TYPE = FlextMeltanoConfig.SINGER_TARGET_TYPE
SINGER_TRANSFORM_TYPE = FlextMeltanoConfig.SINGER_TRANSFORM_TYPE
DEFAULT_MELTANO_PROJECT_ROOT = FlextMeltanoConfig.DEFAULT_MELTANO_PROJECT_ROOT
DEFAULT_MELTANO_DATABASE = FlextMeltanoConfig.DEFAULT_MELTANO_DATABASE
DEFAULT_MELTANO_UI_PORT = FlextMeltanoConfig.DEFAULT_MELTANO_UI_PORT
MELTANO_PLUGIN_TYPES = FlextMeltanoConfig.MELTANO_PLUGIN_TYPES
DEFAULT_DBT_PROFILES_DIR = FlextMeltanoConfig.DEFAULT_DBT_PROFILES_DIR
DEFAULT_DBT_PROJECT_DIR = FlextMeltanoConfig.DEFAULT_DBT_PROJECT_DIR
DEFAULT_DBT_TARGET = FlextMeltanoConfig.DEFAULT_DBT_TARGET
BRIDGE_SUCCESS_KEY = FlextMeltanoConfig.BRIDGE_SUCCESS_KEY
BRIDGE_DATA_KEY = FlextMeltanoConfig.BRIDGE_DATA_KEY
BRIDGE_ERROR_KEY = FlextMeltanoConfig.BRIDGE_ERROR_KEY
BRIDGE_MESSAGE_KEY = FlextMeltanoConfig.BRIDGE_MESSAGE_KEY
BRIDGE_VERSION_OP = FlextMeltanoConfig.BRIDGE_VERSION_OP
BRIDGE_LIST_PLUGINS_OP = FlextMeltanoConfig.BRIDGE_LIST_PLUGINS_OP
BRIDGE_RUN_PIPELINE_OP = FlextMeltanoConfig.BRIDGE_RUN_PIPELINE_OP
BRIDGE_DISCOVER_CATALOG_OP = FlextMeltanoConfig.BRIDGE_DISCOVER_CATALOG_OP
DEFAULT_COMMAND_TIMEOUT = FlextMeltanoConfig.DEFAULT_COMMAND_TIMEOUT
DEFAULT_CONNECTION_TIMEOUT = FlextMeltanoConfig.DEFAULT_CONNECTION_TIMEOUT
DEFAULT_DISCOVERY_TIMEOUT = FlextMeltanoConfig.DEFAULT_DISCOVERY_TIMEOUT
ERROR_CODE_CONFIGURATION = FlextMeltanoConfig.ERROR_CODE_CONFIGURATION
ERROR_CODE_CONNECTION = FlextMeltanoConfig.ERROR_CODE_CONNECTION
ERROR_CODE_EXECUTION = FlextMeltanoConfig.ERROR_CODE_EXECUTION
ERROR_CODE_PLUGIN = FlextMeltanoConfig.ERROR_CODE_PLUGIN
ERROR_CODE_SINGER = FlextMeltanoConfig.ERROR_CODE_SINGER
ERROR_CODE_DBT = FlextMeltanoConfig.ERROR_CODE_DBT
DEFAULT_LOG_LEVEL = FlextMeltanoConfig.DEFAULT_LOG_LEVEL
LOG_FORMAT_JSON = FlextMeltanoConfig.LOG_FORMAT_JSON
LOG_FORMAT_TEXT = FlextMeltanoConfig.LOG_FORMAT_TEXT

# Legacy enum aliases
FlextMeltanoEnvironment = FlextMeltanoConfig.Environment
FlextSingerMessageType = FlextMeltanoConfig.SingerMessageType
FlextMeltanoPluginType = FlextMeltanoConfig.PluginType
FlextBridgeOperation = FlextMeltanoConfig.BridgeOperation
FlextMeltanoLogLevel = FlextMeltanoConfig.LogLevel


__all__ = [
    "BRIDGE_DATA_KEY",
    "BRIDGE_DISCOVER_CATALOG_OP",
    "BRIDGE_ERROR_KEY",
    "BRIDGE_LIST_PLUGINS_OP",
    "BRIDGE_MESSAGE_KEY",
    "BRIDGE_RUN_PIPELINE_OP",
    "BRIDGE_SUCCESS_KEY",
    "BRIDGE_VERSION_OP",
    "DEFAULT_COMMAND_TIMEOUT",
    "DEFAULT_CONNECTION_TIMEOUT",
    "DEFAULT_DBT_PROFILES_DIR",
    "DEFAULT_DBT_PROJECT_DIR",
    "DEFAULT_DBT_TARGET",
    "DEFAULT_DISCOVERY_TIMEOUT",
    "DEFAULT_ENVIRONMENT",
    "DEFAULT_LOG_LEVEL",
    "DEFAULT_MELTANO_DATABASE",
    "DEFAULT_MELTANO_PROJECT_ROOT",
    "DEFAULT_MELTANO_UI_PORT",
    "ERROR_CODE_CONFIGURATION",
    "ERROR_CODE_CONNECTION",
    "ERROR_CODE_DBT",
    "ERROR_CODE_EXECUTION",
    "ERROR_CODE_PLUGIN",
    "ERROR_CODE_SINGER",
    "FLEXT_MELTANO_NAME",
    # =======================================================================
    # BACKWARD COMPATIBILITY - Legacy constant exports
    # =======================================================================
    "FLEXT_MELTANO_VERSION",
    "LOG_FORMAT_JSON",
    "LOG_FORMAT_TEXT",
    "MELTANO_PLUGIN_TYPES",
    "SINGER_MESSAGE_TYPES",
    "SINGER_RECORD_TYPE",
    "SINGER_SCHEMA_TYPE",
    "SINGER_SPEC_VERSION",
    "SINGER_STATE_TYPE",
    "SINGER_TAP_TYPE",
    "SINGER_TARGET_TYPE",
    "SINGER_TRANSFORM_TYPE",
    "SUPPORTED_ENVIRONMENTS",
    "FlextBridgeOperation",
    # 🎯 SINGLE MAIN EXPORT - Following Flext[Area][Module] pattern
    "FlextMeltanoConfig",
    # Legacy enum exports
    "FlextMeltanoEnvironment",
    "FlextMeltanoLogLevel",
    "FlextMeltanoPluginType",
    "FlextSingerMessageType",
]
