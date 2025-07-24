"""FLEXT Meltano Constants - Advanced Constants System.

Unified constants for entire Meltano ecosystem integration built on
flext-core patterns.
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Final

from flext_core import FlextConstants


class FlextMeltanoEnvironmentType(str, Enum):
    """Environment types for FLEXT Meltano platform."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class FlextMeltanoPluginType(str, Enum):
    """Plugin types supported by FLEXT Meltano."""

    EXTRACTOR = "extractors"
    LOADER = "loaders"
    TRANSFORMER = "transformers"
    ORCHESTRATOR = "orchestrators"
    FILE_BUNDLE = "file_bundles"
    UTILITY = "utilities"


class FlextMeltanoJobStatus(str, Enum):
    """Job execution status types."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class FlextMeltanoSingerMessageType(str, Enum):
    """Singer protocol message types."""

    RECORD = "RECORD"
    SCHEMA = "SCHEMA"
    STATE = "STATE"
    METRIC = "METRIC"
    LOG = "LOG"
    BATCH = "BATCH"


class FlextMeltanoDbtResourceType(str, Enum):
    """dbt resource types."""

    MODEL = "model"
    SNAPSHOT = "snapshot"
    SEED = "seed"
    TEST = "test"
    MACRO = "macro"
    SOURCE = "source"


class FlextMeltanoConstants:
    """Unified constants for FLEXT Meltano platform.

    Extends FlextConstants with Meltano-specific configuration.
    This class should NEVER be instantiated - use class attributes.
    """

    # ================================================================
    # PLATFORM METADATA
    # ================================================================

    PLATFORM_NAME: Final[str] = "flext-meltano"
    PLATFORM_VERSION: Final[str] = "0.7.0"
    PLATFORM_DESCRIPTION: Final[str] = "Unified Data Integration Platform"

    # ================================================================
    # MELTANO CONFIGURATION
    # ================================================================

    DEFAULT_MELTANO_CONFIG_FILE: Final[str] = "meltano.yml"
    DEFAULT_MELTANO_STATE_DIR: Final[str] = ".meltano"
    DEFAULT_MELTANO_LOG_DIR: Final[str] = "logs"
    DEFAULT_MELTANO_RUN_DIR: Final[str] = "run"

    MELTANO_PROJECT_FILES: Final[frozenset[str]] = frozenset(
        {
            "meltano.yml",
            "requirements.txt",
            ".env",
            ".gitignore",
        },
    )

    # ================================================================
    # SINGER SDK CONFIGURATION
    # ================================================================

    SINGER_BATCH_SIZE_DEFAULT: Final[int] = 10000
    SINGER_BUFFER_SIZE_DEFAULT: Final[int] = 10485760  # 10MB
    SINGER_TIMEOUT_DEFAULT: Final[int] = 3600  # 1 hour

    SINGER_REQUIRED_CONFIGS: Final[frozenset[str]] = frozenset(
        {
            "config.json",
            "catalog.json",
        },
    )

    # ================================================================
    # DBT CONFIGURATION
    # ================================================================

    DBT_PROJECT_FILE: Final[str] = "dbt_project.yml"
    DBT_PROFILES_FILE: Final[str] = "profiles.yml"
    DBT_DEFAULT_TARGET: Final[str] = "dev"
    DBT_DEFAULT_THREADS: Final[int] = 4

    DBT_ARTIFACT_FILES: Final[frozenset[str]] = frozenset(
        {
            "manifest.json",
            "catalog.json",
            "run_results.json",
            "sources.json",
        },
    )

    # ================================================================
    # MELTANO EDK CONFIGURATION
    # ================================================================

    EDK_EXTENSION_TYPES: Final[frozenset[str]] = frozenset(
        {
            "tap",
            "target",
            "transform",
            "orchestrate",
            "file",
            "utility",
        },
    )

    EDK_PYTHON_VERSION: Final[str] = "3.13"
    EDK_REQUIREMENTS_FILE: Final[str] = "requirements.txt"

    # ================================================================
    # FLEXCORE GO RUNTIME CONFIGURATION
    # ================================================================

    FLEXCORE_DEFAULT_HOST: Final[str] = "localhost"
    FLEXCORE_DEFAULT_PORT: Final[int] = 8080
    FLEXCORE_DEFAULT_GRPC_PORT: Final[int] = 50051
    FLEXCORE_HEALTH_ENDPOINT: Final[str] = "/health"
    FLEXCORE_METRICS_ENDPOINT: Final[str] = "/metrics"

    # ================================================================
    # PERFORMANCE LIMITS
    # ================================================================

    MAX_CONCURRENT_JOBS: Final[int] = 10
    MAX_PLUGIN_INSTALL_TIME: Final[int] = 1800  # 30 minutes
    MAX_JOB_EXECUTION_TIME: Final[int] = 7200  # 2 hours
    MAX_LOG_FILE_SIZE: Final[int] = 104857600  # 100MB

    # ================================================================
    # VALIDATION PATTERNS
    # ================================================================

    PLUGIN_NAME_PATTERN: Final[str] = r"^[a-zA-Z0-9_-]+$"
    ENVIRONMENT_NAME_PATTERN: Final[str] = r"^[a-zA-Z][a-zA-Z0-9_-]*$"
    JOB_NAME_PATTERN: Final[str] = r"^[a-zA-Z][a-zA-Z0-9_.-]*$"

    # Compiled regex patterns for performance
    PLUGIN_NAME_REGEX: Final[re.Pattern[str]] = re.compile(PLUGIN_NAME_PATTERN)
    ENVIRONMENT_NAME_REGEX: Final[re.Pattern[str]] = re.compile(
        ENVIRONMENT_NAME_PATTERN,
    )
    JOB_NAME_REGEX: Final[re.Pattern[str]] = re.compile(JOB_NAME_PATTERN)

    # ================================================================
    # ERROR CODES
    # ================================================================

    ERROR_PLUGIN_NOT_FOUND: Final[str] = "PLUGIN_NOT_FOUND"
    ERROR_INVALID_CONFIG: Final[str] = "INVALID_CONFIG"
    ERROR_EXECUTION_FAILED: Final[str] = "EXECUTION_FAILED"
    ERROR_TIMEOUT: Final[str] = "TIMEOUT"
    ERROR_DEPENDENCY_MISSING: Final[str] = "DEPENDENCY_MISSING"

    # ================================================================
    # DEFAULT CONFIGURATIONS
    # ================================================================

    DEFAULT_ENVIRONMENT: Final[FlextMeltanoEnvironmentType] = (
        FlextMeltanoEnvironmentType.DEVELOPMENT
    )
    DEFAULT_LOG_LEVEL: Final[str] = FlextConstants.LOG_INFO.value
    DEFAULT_RETRY_COUNT: Final[int] = FlextConstants.DEFAULT_RETRY_COUNT
    DEFAULT_TIMEOUT: Final[int] = FlextConstants.DEFAULT_TIMEOUT

    # ================================================================
    # VALIDATION METHODS
    # ================================================================

    @classmethod
    def is_valid_plugin_name(cls, name: str) -> bool:
        """Check if plugin name is valid.

        Args:
            name: Plugin name to validate

        Returns:
            True if valid, False otherwise

        """
        if not (1 <= len(name) <= 100):
            return False
        return cls.PLUGIN_NAME_REGEX.match(name) is not None

    @classmethod
    def is_valid_environment_name(cls, name: str) -> bool:
        """Check if environment name is valid.

        Args:
            name: Environment name to validate

        Returns:
            True if valid, False otherwise

        """
        if not (1 <= len(name) <= 50):
            return False
        return cls.ENVIRONMENT_NAME_REGEX.match(name) is not None

    @classmethod
    def is_valid_job_name(cls, name: str) -> bool:
        """Check if job name is valid.

        Args:
            name: Job name to validate

        Returns:
            True if valid, False otherwise

        """
        if not (1 <= len(name) <= 100):
            return False
        return cls.JOB_NAME_REGEX.match(name) is not None

    @classmethod
    def get_all_plugin_types(cls) -> list[FlextMeltanoPluginType]:
        """Get all available plugin types."""
        return [
            FlextMeltanoPluginType.EXTRACTOR,
            FlextMeltanoPluginType.LOADER,
            FlextMeltanoPluginType.TRANSFORMER,
            FlextMeltanoPluginType.ORCHESTRATOR,
            FlextMeltanoPluginType.FILE_BUNDLE,
            FlextMeltanoPluginType.UTILITY,
        ]

    @classmethod
    def get_all_job_statuses(cls) -> list[FlextMeltanoJobStatus]:
        """Get all available job statuses."""
        return [
            FlextMeltanoJobStatus.PENDING,
            FlextMeltanoJobStatus.RUNNING,
            FlextMeltanoJobStatus.COMPLETED,
            FlextMeltanoJobStatus.FAILED,
            FlextMeltanoJobStatus.CANCELLED,
            FlextMeltanoJobStatus.TIMEOUT,
        ]

    @classmethod
    def get_all_environment_types(cls) -> list[FlextMeltanoEnvironmentType]:
        """Get all available environment types."""
        return [
            FlextMeltanoEnvironmentType.DEVELOPMENT,
            FlextMeltanoEnvironmentType.TESTING,
            FlextMeltanoEnvironmentType.STAGING,
            FlextMeltanoEnvironmentType.PRODUCTION,
        ]

    @classmethod
    def get_all_singer_message_types(
        cls,
    ) -> list[FlextMeltanoSingerMessageType]:
        """Get all Singer protocol message types."""
        return [
            FlextMeltanoSingerMessageType.RECORD,
            FlextMeltanoSingerMessageType.SCHEMA,
            FlextMeltanoSingerMessageType.STATE,
            FlextMeltanoSingerMessageType.METRIC,
            FlextMeltanoSingerMessageType.LOG,
            FlextMeltanoSingerMessageType.BATCH,
        ]

    @classmethod
    def is_production_environment(cls, env: FlextMeltanoEnvironmentType) -> bool:
        """Check if environment is production.

        Args:
            env: Environment to check

        Returns:
            True if production environment

        """
        return env == FlextMeltanoEnvironmentType.PRODUCTION

    @classmethod
    def is_final_job_status(cls, status: FlextMeltanoJobStatus) -> bool:
        """Check if job status is final (non-transitional).

        Args:
            status: Job status to check

        Returns:
            True if status is final

        """
        return status in {
            FlextMeltanoJobStatus.COMPLETED,
            FlextMeltanoJobStatus.FAILED,
            FlextMeltanoJobStatus.CANCELLED,
            FlextMeltanoJobStatus.TIMEOUT,
        }

    def __init__(self) -> None:
        """Prevent instantiation of FlextMeltanoConstants.

        Raises:
            TypeError: Always raised to prevent instantiation

        """
        msg = (
            "FlextMeltanoConstants should not be instantiated - use class attributes"
        )
        raise TypeError(msg)
