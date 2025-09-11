"""Flext Meltano Configuration - Unified configuration management.

This module provides complete Meltano configuration functionality following flext-core
single-class-per-module pattern. Consolidates all configuration, constants, and enums
in a unified class.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import contextlib
from enum import StrEnum
from pathlib import Path
from typing import ClassVar

from flext_core import FlextConstants, FlextExceptions, FlextResult, FlextTypes
from pydantic import BaseModel, Field, field_validator

# Avoid circular import by importing constants after core
from flext_meltano.constants import FlextMeltanoConstants  # SOURCE OF TRUTH


class FlextMeltanoConfig(
    BaseModel
):  # Meltano-specific configuration, uses FlextConstants as SOURCE OF TRUTH
    """Meltano ELT configuration using FlextConstants as SOURCE OF TRUTH.

    Provides Meltano-specific configuration with validation using flext-core patterns.
    Uses FlextConstants for all common values (SOURCE OF TRUTH principle).
    """

    # ============================================================================
    # MELTANO-SPECIFIC CONSTANTS - Using FlextMeltanoConstants as SOURCE OF TRUTH
    # ============================================================================

    # Use FlextMeltanoConstants for all version constants (SOURCE OF TRUTH)
    MELTANO_VERSION: ClassVar[str] = FlextMeltanoConstants.Meltano.VERSION_REQUIRED
    SINGER_SDK_VERSION: ClassVar[str] = (
        FlextMeltanoConstants.Singer.SDK_VERSION_REQUIRED
    )
    DBT_VERSION: ClassVar[str] = FlextMeltanoConstants.DBT.VERSION_REQUIRED

    # Use FlextMeltanoConstants for file constants (SOURCE OF TRUTH)
    PROJECT_FILE: ClassVar[str] = FlextMeltanoConstants.Meltano.PROJECT_FILE
    STATE_DIR: ClassVar[str] = FlextMeltanoConstants.Meltano.STATE_DIR
    VENV_DIR: ClassVar[str] = ".meltano/python"

    # Meltano environment variables (Meltano-specific)
    MELTANO_PROJECT_ROOT_ENV: ClassVar[str] = "MELTANO_PROJECT_ROOT"
    MELTANO_ENVIRONMENT_ENV: ClassVar[str] = "MELTANO_ENVIRONMENT"
    MELTANO_LOG_LEVEL_ENV: ClassVar[str] = "MELTANO_LOG_LEVEL"

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
        default=MELTANO_VERSION, description="Meltano version to use"
    )

    singer_sdk_version: str = Field(
        default=SINGER_SDK_VERSION, description="Singer SDK version to use"
    )

    dbt_version: str = Field(default=DBT_VERSION, description="DBT version to use")

    # Environment and execution configuration
    environment: EnvironmentType = Field(
        default=EnvironmentType.DEV, description="Target environment for operations"
    )

    log_level: LogLevel = Field(
        default=LogLevel.INFO, description="Logging level for operations"
    )

    timeout_seconds: int = Field(
        default=FlextConstants.Network.DEFAULT_TIMEOUT,  # SOURCE OF TRUTH
        ge=1,
        le=3600,
        description="Timeout for operations in seconds",
    )

    retry_count: int = Field(
        default=FlextConstants.Reliability.MAX_RETRY_ATTEMPTS,  # SOURCE OF TRUTH
        ge=0,
        le=10,
        description="Number of retries for failed operations",
    )

    batch_size: int = Field(
        default=FlextConstants.Performance.DEFAULT_BATCH_SIZE,  # SOURCE OF TRUTH
        ge=1,
        le=10000,
        description="Batch size for data processing",
    )

    # Plugin and execution configuration
    max_concurrent_jobs: int = Field(
        default=4,  # Meltano-specific default (no FlextConstants equivalent)
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

    @field_validator("project_root", "venv_dir")
    @classmethod
    def validate_absolute_paths(cls, v: Path | str) -> Path:
        """Validate and convert absolute path fields."""
        if isinstance(v, str):
            v = Path(v)
        return v.expanduser().resolve()

    @field_validator("config_dir", "logs_dir")
    @classmethod
    def validate_relative_paths(cls, v: Path | str) -> Path:
        """Validate relative path fields (should not be resolved to absolute)."""
        if isinstance(v, str):
            v = Path(v)
        return v.expanduser()  # Don't resolve to allow relative paths

    @field_validator("meltano_version", "singer_sdk_version", "dbt_version")
    @classmethod
    def validate_versions(cls, v: str) -> str:
        """Validate version strings.

        Returns:
            Path: Validated version string.

        """
        if not v or not isinstance(v, str):
            error_msg = "Version must be non-empty string"
            raise FlextExceptions.FlextValidationError(error_msg)
        return v.strip()

    # ============================================================================
    # CONFIGURATION METHODS - Business logic methods
    # ============================================================================

    def get_project_file(self) -> Path:
        """Get full path to meltano project file."""
        return self.project_root / self.PROJECT_FILE

    def get_absolute_config_dir(self) -> Path:
        """Get absolute path to config directory.

        Returns:
            Path: Absolute config directory path.

        """
        if self.config_dir.is_absolute():
            return self.config_dir
        return self.project_root / self.config_dir

    def get_absolute_logs_dir(self) -> Path:
        """Get absolute path to logs directory."""
        if self.logs_dir.is_absolute():
            return self.logs_dir
        return self.project_root / self.logs_dir

    def get_absolute_venv_dir(self) -> Path:
        """Get absolute path to virtual environment directory.

        Returns:
            Path: Absolute virtual environment directory path.

        """
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
                return FlextResult[
                    bool
                ].fail(
                    f"meltano.yml not found in {project_file.parent}"  # Test expectation compliance
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

    def get_environment_variables(self) -> FlextTypes.Core.Headers:
        """Get environment variables for Meltano operations.

        Returns:
            FlextTypes.Core.Headers: Environment variables dictionary.

        """
        # Handle both enum and string values for environment and log_level
        environment_value = (
            self.environment.value
            if hasattr(self.environment, "value")
            else str(self.environment)
        )
        log_level_value = (
            self.log_level.value
            if hasattr(self.log_level, "value")
            else str(self.log_level)
        )

        return {
            self.MELTANO_PROJECT_ROOT_ENV: str(self.project_root),
            self.MELTANO_ENVIRONMENT_ENV: environment_value,
            self.MELTANO_LOG_LEVEL_ENV: log_level_value.upper(),
        }

    # ============================================================================
    # CONSTANTS ACCESS METHODS - Utility methods for constants
    # ============================================================================

    @classmethod
    def get_version(cls) -> str:
        """Get FlextMeltano version from constants (SOURCE OF TRUTH)."""
        return FlextMeltanoConstants.FLEXT_MELTANO_VERSION  # SOURCE OF TRUTH

    @classmethod
    def get_name(cls) -> str:
        """Get FlextMeltano name."""
        return FlextMeltanoConstants.Application.NAME  # SOURCE OF TRUTH

    @classmethod
    def get_default_timeout(cls) -> int:
        """Get default timeout in seconds from FlextConstants (SOURCE OF TRUTH)."""
        return FlextConstants.Network.DEFAULT_TIMEOUT  # SOURCE OF TRUTH

    @classmethod
    def get_default_batch_size(cls) -> int:
        """Get default batch size from FlextConstants (SOURCE OF TRUTH)."""
        return FlextConstants.Performance.DEFAULT_BATCH_SIZE  # SOURCE OF TRUTH

    @classmethod
    def get_supported_plugin_types(cls) -> FlextTypes.Core.StringList:
        """Get list of supported plugin types."""
        return [plugin_type.value for plugin_type in cls.PluginType]

    @classmethod
    def get_supported_environments(cls) -> FlextTypes.Core.StringList:
        """Get list of supported environments.

        Returns:
            FlextTypes.Core.StringList:: Description of return value.

        """
        return [env.value for env in cls.EnvironmentType]

    @classmethod
    def get_supported_log_levels(cls) -> FlextTypes.Core.StringList:
        """Get list of supported log levels."""
        return [level.value for level in cls.LogLevel]

    # ============================================================================
    # FACTORY METHODS - Instance creation and validation
    # ============================================================================

    @classmethod
    def create_from_project_root(
        cls, project_root: str | Path
    ) -> FlextResult[FlextMeltanoConfig]:
        """Create configuration from project root directory.

        Returns:
            FlextTypes.Core.StringList:: Description of return value.

        """
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
        cls, environment: str, **kwargs: object
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

            # Filter and type-cast kwargs to valid fields only
            valid_fields = cls.model_fields.keys()
            filtered_kwargs: FlextTypes.Core.Dict = {
                k: v for k, v in kwargs.items() if k in valid_fields
            }

            # Create config with proper type conversions
            project_root_value = filtered_kwargs.get("project_root", ".")
            if isinstance(project_root_value, str):
                project_root = Path(project_root_value)
            elif isinstance(project_root_value, Path):
                project_root = project_root_value
            else:
                project_root = Path()

            config = cls(
                environment=env_type,
                project_root=project_root,
                log_level=cls.LogLevel(
                    str(filtered_kwargs.get("log_level", cls.LogLevel.INFO))
                ),
                run_mode=cls.RunMode(
                    str(filtered_kwargs.get("run_mode", cls.RunMode.FULL))
                ),
            )
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


__all__ = [
    "FlextMeltanoConfig",
]
