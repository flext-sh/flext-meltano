"""FLEXT Meltano Constants - Extensão das constantes do flext-core.

Constantes específicas do Meltano organizadas em uma classe unificada.
Estende FlextConstants do flext-core seguindo o mesmo padrão de construção.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

from flext_core import FlextConstants

# ==================================================================
# ENUMS - Meltano-specific enums
# ==================================================================


class MeltanoEnvironment(StrEnum):
    """Environment types for Meltano applications."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class MeltanoLogLevel(StrEnum):
    """Log levels for Meltano operations."""

    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    TRACE = "TRACE"


class MeltanoResultStatus(StrEnum):
    """Result status for Meltano operations."""

    SUCCESS = "success"
    FAILURE = "failure"


# ==================================================================
# UNIFIED CONSTANTS CLASS - Extends FlextConstants
# ==================================================================


class FlextMeltanoConstants(FlextConstants):
    """Unified constants class extending FlextConstants for Meltano.

    All Meltano-specific constants are organized as class attributes.
    This class should NEVER be instantiated - use class attributes.

    Usage:
        from flext_meltano.constants import FlextMeltanoConstants

        # Access Meltano constants directly
        timeout = FlextMeltanoConstants.DEFAULT_TIMEOUT
        port = FlextMeltanoConstants.DEFAULT_POSTGRES_PORT
        env = FlextMeltanoConstants.DEFAULT_MELTANO_ENVIRONMENT
    """

    # ================================================================
    # PROJECT METADATA
    # ================================================================

    VERSION: Final[str] = "0.7.0"
    NAME: Final[str] = "flext-meltano"
    DESCRIPTION: Final[str] = "Meltano Integration Framework"

    # ================================================================
    # MELTANO ENVIRONMENT CONSTANTS
    # ================================================================

    # Meltano environment enum values
    MELTANO_ENV_DEVELOPMENT = MeltanoEnvironment.DEVELOPMENT
    MELTANO_ENV_TESTING = MeltanoEnvironment.TESTING
    MELTANO_ENV_STAGING = MeltanoEnvironment.STAGING
    MELTANO_ENV_PRODUCTION = MeltanoEnvironment.PRODUCTION

    # Default Meltano environment
    DEFAULT_MELTANO_ENVIRONMENT: Final[MeltanoEnvironment] = (
        MeltanoEnvironment.DEVELOPMENT
    )

    # ================================================================
    # MELTANO LOGGING CONSTANTS
    # ================================================================

    # Meltano log level enum values
    MELTANO_LOG_CRITICAL = MeltanoLogLevel.CRITICAL
    MELTANO_LOG_ERROR = MeltanoLogLevel.ERROR
    MELTANO_LOG_WARNING = MeltanoLogLevel.WARNING
    MELTANO_LOG_INFO = MeltanoLogLevel.INFO
    MELTANO_LOG_DEBUG = MeltanoLogLevel.DEBUG
    MELTANO_LOG_TRACE = MeltanoLogLevel.TRACE

    # Default Meltano log level
    DEFAULT_MELTANO_LOG_LEVEL: Final[MeltanoLogLevel] = MeltanoLogLevel.INFO

    # ================================================================
    # MELTANO SYSTEM DEFAULTS
    # ================================================================

    # Timeout constants (in seconds)
    DEFAULT_TIMEOUT: Final[int] = 300  # 5 minutes
    DISCOVERY_TIMEOUT: Final[int] = 60  # 1 minute
    PIPELINE_TIMEOUT: Final[int] = 1800  # 30 minutes
    COMMAND_TIMEOUT: Final[int] = 300  # 5 minutes

    # Database port defaults
    DEFAULT_POSTGRES_PORT: Final[int] = 5432
    DEFAULT_ORACLE_PORT: Final[int] = 1521
    DEFAULT_MYSQL_PORT: Final[int] = 3306
    DEFAULT_SQLSERVER_PORT: Final[int] = 1433
    DEFAULT_SQLITE_PORT: Final[int] = 0  # SQLite doesn't use network ports

    # Retry and backoff constants
    BACKOFF_BASE: Final[int] = 2
    MAX_RETRY_ATTEMPTS: Final[int] = 3
    RETRY_DELAY: Final[int] = 1  # seconds

    # ================================================================
    # MELTANO PROJECT CONFIGURATION
    # ================================================================

    # Project structure
    MELTANO_PROJECT_FILE: Final[str] = "meltano.yml"
    MELTANO_ENV_FILE: Final[str] = ".env"
    MELTANO_CONFIG_DIR: Final[str] = "config"
    MELTANO_LOGS_DIR: Final[str] = "logs"
    MELTANO_DATA_DIR: Final[str] = "data"

    # Virtual environment
    VENV_DIR: Final[str] = ".venv"
    VENV_BIN_DIR: Final[str] = "bin"
    VENV_SCRIPTS_DIR: Final[str] = "Scripts"  # Windows

    # ================================================================
    # MELTANO PLUGIN CONSTANTS
    # ================================================================

    # Plugin types
    PLUGIN_TYPE_EXTRACTOR: Final[str] = "extractors"
    PLUGIN_TYPE_LOADER: Final[str] = "loaders"
    PLUGIN_TYPE_TRANSFORMER: Final[str] = "transformers"
    PLUGIN_TYPE_ORCHESTRATOR: Final[str] = "orchestrators"
    PLUGIN_TYPE_UTILITY: Final[str] = "utilities"

    # Plugin namespaces
    PLUGIN_NAMESPACE_TAP: Final[str] = "tap-"
    PLUGIN_NAMESPACE_TARGET: Final[str] = "target-"
    PLUGIN_NAMESPACE_DBT: Final[str] = "dbt-"

    # ================================================================
    # MELTANO COMMAND CONSTANTS
    # ================================================================

    # Common Meltano commands
    COMMAND_RUN: Final[str] = "run"
    COMMAND_INVOKE: Final[str] = "invoke"
    COMMAND_DISCOVER: Final[str] = "discover"
    COMMAND_TEST: Final[str] = "test"
    COMMAND_INSTALL: Final[str] = "install"
    COMMAND_UPGRADE: Final[str] = "upgrade"
    COMMAND_ADD: Final[str] = "add"
    COMMAND_REMOVE: Final[str] = "remove"
    COMMAND_CONFIG: Final[str] = "config"
    COMMAND_ELT: Final[str] = "elt"
    COMMAND_SCHEDULE: Final[str] = "schedule"

    # ================================================================
    # MELTANO RESULT STATUS CONSTANTS
    # ================================================================

    MELTANO_RESULT_SUCCESS = MeltanoResultStatus.SUCCESS
    MELTANO_RESULT_FAILURE = MeltanoResultStatus.FAILURE

    # ================================================================
    # MELTANO VALIDATION PATTERNS
    # ================================================================

    # Plugin name patterns
    VALID_TAP_NAME_PATTERN: Final[str] = r"^tap-[a-zA-Z0-9_-]+$"
    VALID_TARGET_NAME_PATTERN: Final[str] = r"^target-[a-zA-Z0-9_-]+$"
    VALID_DBT_NAME_PATTERN: Final[str] = r"^dbt-[a-zA-Z0-9_-]+$"

    # Project name patterns
    VALID_PROJECT_NAME_PATTERN: Final[str] = r"^[a-zA-Z0-9_-]+$"

    # ================================================================
    # MELTANO PERFORMANCE LIMITS
    # ================================================================

    # Pipeline limits
    MAX_STREAMS_PER_TAP: Final[int] = 1000
    MAX_RECORDS_PER_BATCH: Final[int] = 10000
    MAX_BATCH_SIZE_BYTES: Final[int] = 100 * 1024 * 1024  # 100MB

    # Connection limits
    MAX_CONCURRENT_CONNECTIONS: Final[int] = 10
    CONNECTION_TIMEOUT: Final[int] = 30
    READ_TIMEOUT: Final[int] = 300

    # ================================================================
    # MELTANO VALIDATION METHODS
    # ================================================================

    @classmethod
    def is_valid_tap_name(cls, name: str) -> bool:
        """Check if a tap name is valid.

        Args:
            name: Tap name to validate

        Returns:
            True if valid, False otherwise

        """
        import re

        pattern = re.compile(cls.VALID_TAP_NAME_PATTERN)
        return pattern.match(name) is not None

    @classmethod
    def is_valid_target_name(cls, name: str) -> bool:
        """Check if a target name is valid.

        Args:
            name: Target name to validate

        Returns:
            True if valid, False otherwise

        """
        import re

        pattern = re.compile(cls.VALID_TARGET_NAME_PATTERN)
        return pattern.match(name) is not None

    @classmethod
    def is_valid_project_name(cls, name: str) -> bool:
        """Check if a project name is valid.

        Args:
            name: Project name to validate

        Returns:
            True if valid, False otherwise

        """
        import re

        pattern = re.compile(cls.VALID_PROJECT_NAME_PATTERN)
        return pattern.match(name) is not None

    # ================================================================
    # MELTANO UTILITY METHODS
    # ================================================================

    @classmethod
    def get_all_meltano_environments(cls) -> list[MeltanoEnvironment]:
        """Get all available Meltano environments."""
        return [
            cls.MELTANO_ENV_DEVELOPMENT,
            cls.MELTANO_ENV_TESTING,
            cls.MELTANO_ENV_STAGING,
            cls.MELTANO_ENV_PRODUCTION,
        ]

    @classmethod
    def get_all_meltano_log_levels(cls) -> list[MeltanoLogLevel]:
        """Get all available Meltano log levels."""
        return [
            cls.MELTANO_LOG_CRITICAL,
            cls.MELTANO_LOG_ERROR,
            cls.MELTANO_LOG_WARNING,
            cls.MELTANO_LOG_INFO,
            cls.MELTANO_LOG_DEBUG,
            cls.MELTANO_LOG_TRACE,
        ]

    @classmethod
    def get_plugin_types(cls) -> list[str]:
        """Get all available plugin types."""
        return [
            cls.PLUGIN_TYPE_EXTRACTOR,
            cls.PLUGIN_TYPE_LOADER,
            cls.PLUGIN_TYPE_TRANSFORMER,
            cls.PLUGIN_TYPE_ORCHESTRATOR,
            cls.PLUGIN_TYPE_UTILITY,
        ]

    @classmethod
    def get_common_commands(cls) -> list[str]:
        """Get all common Meltano commands."""
        return [
            cls.COMMAND_RUN,
            cls.COMMAND_INVOKE,
            cls.COMMAND_DISCOVER,
            cls.COMMAND_TEST,
            cls.COMMAND_INSTALL,
            cls.COMMAND_UPGRADE,
            cls.COMMAND_ADD,
            cls.COMMAND_REMOVE,
            cls.COMMAND_CONFIG,
            cls.COMMAND_ELT,
            cls.COMMAND_SCHEDULE,
        ]

    # ================================================================
    # PREVENT INSTANTIATION - Use class attributes directly
    # ================================================================

    def __init__(self) -> None:
        """Prevent instantiation of FlextMeltanoConstants.

        This class should not be instantiated. Use class attributes directly.

        Raises:
            TypeError: Always raised to prevent instantiation

        """
        msg = "FlextMeltanoConstants should not be instantiated - use class attrs"
        raise TypeError(msg)


# ==================================================================
# EXPORTS - Clean public API
# ==================================================================

__all__ = [
    # Main constants class - PRIMARY INTERFACE
    "FlextMeltanoConstants",
    # Enums
    "MeltanoEnvironment",
    "MeltanoLogLevel",
    "MeltanoResultStatus",
]
