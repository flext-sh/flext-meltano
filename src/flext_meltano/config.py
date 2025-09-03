"""Flext Meltano Configuration - Unified configuration management.

This module provides complete Meltano configuration functionality following flext-core
single-class-per-module pattern. Consolidates all configuration, constants, and enums
in a unified class.

Architecture:
    Core: Unified FlextMeltanoConfig class handling all functionality
    Constants: All Meltano constants and configuration values
    Enums: All enumerated types and status definitions
    Configuration: Pydantic-based configuration models
    Validation: Configuration validation and type checking

Features:
    - Single unified class following flext-core patterns
    - Complete Meltano configuration abstraction
    - Pydantic-based validation and type safety
    - Comprehensive constants and enums management
    - FlextResult integration for error handling

Examples:
    Create configuration:
        >>> config = FlextMeltanoConfig(
        ...     project_root="/path/to/project", meltano_version="3.9.1"
        ... )
        >>> validation_result = config.validate()

    Access constants:
        >>> version = config.get_version()
        >>> default_timeout = config.get_default_timeout()

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import contextlib
from enum import StrEnum
from pathlib import Path
from typing import ClassVar

from flext_core import FlextExceptions, FlextResult
from pydantic import BaseModel, Field, field_validator


class FlextMeltanoConfig(BaseModel):
    """Unified Meltano configuration management.

    Consolidated class providing complete FlextMeltano configuration functionality
    following flext-core single-class-per-module pattern. Includes constants, enums,
    configuration models, and validation.
    """

    # ============================================================================
    # CONSTANTS - All Meltano constants as class attributes
    # ============================================================================

    # Version and metadata
    VERSION: ClassVar[str] = "2.0.0-enterprise"
    NAME: ClassVar[str] = "flext-meltano"
    DESCRIPTION: ClassVar[str] = "Enterprise Meltano/Singer SDK/DBT integration library"
    AUTHOR: ClassVar[str] = "FLEXT Team"
    LICENSE: ClassVar[str] = "MIT"

    # Meltano-specific constants
    DEFAULT_MELTANO_VERSION: ClassVar[str] = "3.9.1"
    DEFAULT_SINGER_SDK_VERSION: ClassVar[str] = "0.48.0"
    DEFAULT_DBT_VERSION: ClassVar[str] = "1.10.5"

    # File and directory constants
    DEFAULT_PROJECT_FILE: ClassVar[str] = "meltano.yml"
    DEFAULT_CONFIG_DIR: ClassVar[str] = ".meltano"
    DEFAULT_LOGS_DIR: ClassVar[str] = "logs"
    DEFAULT_VENV_DIR: ClassVar[str] = ".meltano/python"

    # Command and operation constants
    DEFAULT_TIMEOUT_SECONDS: ClassVar[int] = 300
    DEFAULT_RETRY_COUNT: ClassVar[int] = 3
    DEFAULT_BATCH_SIZE: ClassVar[int] = 1000
    MAX_CONCURRENT_JOBS: ClassVar[int] = 4

    # Environment constants
    MELTANO_PROJECT_ROOT_ENV: ClassVar[str] = "MELTANO_PROJECT_ROOT"
    MELTANO_ENVIRONMENT_ENV: ClassVar[str] = "MELTANO_ENVIRONMENT"
    MELTANO_LOG_LEVEL_ENV: ClassVar[str] = "MELTANO_LOG_LEVEL"

    # Plugin type constants
    PLUGIN_TYPE_EXTRACTORS: ClassVar[str] = "extractors"
    PLUGIN_TYPE_LOADERS: ClassVar[str] = "loaders"
    PLUGIN_TYPE_TRANSFORMERS: ClassVar[str] = "transformers"
    PLUGIN_TYPE_ORCHESTRATORS: ClassVar[str] = "orchestrators"
    PLUGIN_TYPE_FILES: ClassVar[str] = "files"

    # Status constants
    STATUS_SUCCESS: ClassVar[str] = "success"
    STATUS_ERROR: ClassVar[str] = "error"
    STATUS_RUNNING: ClassVar[str] = "running"
    STATUS_COMPLETED: ClassVar[str] = "completed"
    STATUS_FAILED: ClassVar[str] = "failed"

    # ============================================================================
    # ENUMS - All enumerated types as class enums
    # ============================================================================

    class PluginType(StrEnum):
        """Plugin type enumeration."""

        EXTRACTORS = "extractors"
        LOADERS = "loaders"
        TRANSFORMERS = "transformers"
        ORCHESTRATORS = "orchestrators"
        FILES = "files"
        UTILITIES = "utilities"

    class EnvironmentType(StrEnum):
        """Environment type enumeration."""

        DEV = "dev"
        STAGING = "staging"
        PROD = "prod"
        TEST = "test"

    class LogLevel(StrEnum):
        """Log level enumeration."""

        DEBUG = "debug"
        INFO = "info"
        WARNING = "warning"
        ERROR = "error"
        CRITICAL = "critical"

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

    # ============================================================================
    # CONFIGURATION FIELDS - Pydantic model fields
    # ============================================================================

    # Core project configuration
    project_root: Path = Field(
        default_factory=Path.cwd, description="Root directory of the Meltano project"
    )

    meltano_version: str = Field(
        default=DEFAULT_MELTANO_VERSION, description="Meltano version to use"
    )

    singer_sdk_version: str = Field(
        default=DEFAULT_SINGER_SDK_VERSION, description="Singer SDK version to use"
    )

    dbt_version: str = Field(
        default=DEFAULT_DBT_VERSION, description="DBT version to use"
    )

    # Environment and execution configuration
    environment: EnvironmentType = Field(
        default=EnvironmentType.DEV, description="Target environment for operations"
    )

    log_level: LogLevel = Field(
        default=LogLevel.INFO, description="Logging level for operations"
    )

    timeout_seconds: int = Field(
        default=DEFAULT_TIMEOUT_SECONDS,
        ge=1,
        le=3600,
        description="Timeout for operations in seconds",
    )

    retry_count: int = Field(
        default=DEFAULT_RETRY_COUNT,
        ge=0,
        le=10,
        description="Number of retries for failed operations",
    )

    batch_size: int = Field(
        default=DEFAULT_BATCH_SIZE,
        ge=1,
        le=10000,
        description="Batch size for data processing",
    )

    # Plugin and execution configuration
    max_concurrent_jobs: int = Field(
        default=MAX_CONCURRENT_JOBS,
        ge=1,
        le=16,
        description="Maximum number of concurrent jobs",
    )

    run_mode: RunMode = Field(
        default=RunMode.FULL, description="Execution mode for operations"
    )

    # Directory configuration
    config_dir: Path = Field(
        default_factory=lambda: Path(".meltano"), description="Configuration directory"
    )

    logs_dir: Path = Field(
        default_factory=lambda: Path("logs"), description="Logs directory"
    )

    venv_dir: Path = Field(
        default_factory=lambda: Path(".meltano/python"),
        description="Virtual environment directory",
    )

    # ============================================================================
    # FIELD VALIDATORS - Pydantic validation methods
    # ============================================================================

    @field_validator("project_root", "config_dir", "logs_dir", "venv_dir")
    @classmethod
    def validate_paths(cls, v: Path) -> Path:
        """Validate and convert path fields."""
        if isinstance(v, str):
            v = Path(v)
        return v.expanduser().resolve()

    @field_validator("meltano_version", "singer_sdk_version", "dbt_version")
    @classmethod
    def validate_versions(cls, v: str) -> str:
        """Validate version strings."""
        if not v or not isinstance(v, str):
            error_msg = "Version must be non-empty string"
            raise FlextExceptions.FlextValidationError(error_msg)
        return v.strip()

    # ============================================================================
    # CONFIGURATION METHODS - Business logic methods
    # ============================================================================

    def get_project_file(self) -> Path:
        """Get full path to meltano project file."""
        return self.project_root / self.DEFAULT_PROJECT_FILE

    def get_absolute_config_dir(self) -> Path:
        """Get absolute path to config directory."""
        if self.config_dir.is_absolute():
            return self.config_dir
        return self.project_root / self.config_dir

    def get_absolute_logs_dir(self) -> Path:
        """Get absolute path to logs directory."""
        if self.logs_dir.is_absolute():
            return self.logs_dir
        return self.project_root / self.logs_dir

    def get_absolute_venv_dir(self) -> Path:
        """Get absolute path to virtual environment directory."""
        if self.venv_dir.is_absolute():
            return self.venv_dir
        return self.project_root / self.venv_dir

    def validate_project_structure(self) -> FlextResult[bool]:
        """Validate Meltano project directory structure."""
        try:
            # Check if project root exists
            if not self.project_root.exists():
                return FlextResult[bool].fail(
                    f"Project root does not exist: {self.project_root}"
                )

            # Check for meltano.yml
            project_file = self.get_project_file()
            if not project_file.exists():
                return FlextResult[bool].fail(
                    f"Meltano project file not found: {project_file}"
                )

            # Ensure required directories exist
            config_dir = self.get_absolute_config_dir()
            logs_dir = self.get_absolute_logs_dir()

            with contextlib.suppress(OSError):
                config_dir.mkdir(parents=True, exist_ok=True)
                logs_dir.mkdir(parents=True, exist_ok=True)

            success = True
            return FlextResult[bool].ok(success)

        except Exception as e:
            return FlextResult[bool].fail(f"Project validation failed: {e}")

    def get_environment_variables(self) -> dict[str, str]:
        """Get environment variables for Meltano operations."""
        return {
            self.MELTANO_PROJECT_ROOT_ENV: str(self.project_root),
            self.MELTANO_ENVIRONMENT_ENV: self.environment.value,
            self.MELTANO_LOG_LEVEL_ENV: self.log_level.value.upper(),
        }

    # ============================================================================
    # CONSTANTS ACCESS METHODS - Utility methods for constants
    # ============================================================================

    @classmethod
    def get_version(cls) -> str:
        """Get FlextMeltano version."""
        return cls.VERSION

    @classmethod
    def get_name(cls) -> str:
        """Get FlextMeltano name."""
        return cls.NAME

    @classmethod
    def get_default_timeout(cls) -> int:
        """Get default timeout in seconds."""
        return cls.DEFAULT_TIMEOUT_SECONDS

    @classmethod
    def get_default_batch_size(cls) -> int:
        """Get default batch size."""
        return cls.DEFAULT_BATCH_SIZE

    @classmethod
    def get_supported_plugin_types(cls) -> list[str]:
        """Get list of supported plugin types."""
        return [plugin_type.value for plugin_type in cls.PluginType]

    @classmethod
    def get_supported_environments(cls) -> list[str]:
        """Get list of supported environments."""
        return [env.value for env in cls.EnvironmentType]

    @classmethod
    def get_supported_log_levels(cls) -> list[str]:
        """Get list of supported log levels."""
        return [level.value for level in cls.LogLevel]

    # ============================================================================
    # FACTORY METHODS - Instance creation and validation
    # ============================================================================

    @classmethod
    def create_from_project_root(
        cls, project_root: str | Path
    ) -> FlextResult[FlextMeltanoConfig]:
        """Create configuration from project root directory."""
        try:
            config = cls(project_root=Path(project_root))
            validation_result = config.validate_project_structure()

            if validation_result.failure:
                return FlextResult["FlextMeltanoConfig"].fail(
                    validation_result.error or "Project validation failed"
                )

            return FlextResult["FlextMeltanoConfig"].ok(config)

        except Exception as e:
            return FlextResult["FlextMeltanoConfig"].fail(
                f"Config creation failed: {e}"
            )

    @classmethod
    def create_for_environment(
        cls, environment: str, **kwargs
    ) -> FlextResult[FlextMeltanoConfig]:
        """Create configuration for specific environment."""
        try:
            # Validate environment
            try:
                env_type = cls.EnvironmentType(environment)
            except ValueError:
                return FlextResult["FlextMeltanoConfig"].fail(
                    f"Invalid environment: {environment}"
                )

            # Filter kwargs to valid fields only
            valid_fields = cls.model_fields.keys()
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_fields}
            config = cls(environment=env_type, **filtered_kwargs)
            return FlextResult["FlextMeltanoConfig"].ok(config)

        except Exception as e:
            return FlextResult["FlextMeltanoConfig"].fail(
                f"Environment config creation failed: {e}"
            )

    # ============================================================================
    # CLASS CONFIGURATION - Pydantic model configuration
    # ============================================================================

    class Config:
        """Pydantic model configuration."""

        extra = "forbid"
        validate_assignment = True
        use_enum_values = True
        arbitrary_types_allowed = True


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "FlextMeltanoConfig",
]
