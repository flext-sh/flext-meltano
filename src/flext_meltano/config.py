"""FLEXT Meltano Configuration Management - Enterprise ELT configuration patterns.

This module provides configuration management for Meltano ELT operations
following FLEXT architectural patterns with Pydantic validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import ClassVar

from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict

from flext_core import (
    FlextConfig,
    FlextConstants,
    FlextExceptions,
    FlextResult,
    FlextTypes,
)
from flext_meltano.constants import FlextMeltanoConstants  # SOURCE OF TRUTH
from flext_meltano.validators import FlextMeltanoValidators


class FlextMeltanoConfig(FlextConfig):
    """Meltano ELT configuration management with enterprise-grade validation.

    Extends FlextConfig to provide comprehensive Meltano-specific configuration
    with validation using flext-core patterns. This class serves as the single
    source of truth for all Meltano configuration across the application.

    The configuration includes support for:
    - Multiple service types (extractors, loaders, transformers)
    - Environment-specific settings (development, staging, production)
    - Plugin management and validation
    - Directory structure management
    - Execution parameters and timeouts

    Attributes:
        MELTANO_VERSION: Required Meltano version for compatibility.
        SINGER_SDK_VERSION: Required Singer SDK version.
        DBT_VERSION: Required DBT version.
        PROJECT_FILE: Default Meltano project file name.
        STATE_DIR: Directory for Meltano state files.
        VENV_DIR: Directory for Python virtual environments.

    Example:
        >>> config = FlextMeltanoConfig(
        ...     project_root="/path/to/project",
        ...     environment="development",
        ...     log_level="INFO",
        ... )
        >>> validation_result = config.validate_project_structure()
        >>> if validation_result.is_success:
        ...     print("Configuration is valid")

    """

    # ============================================================================
    # MELTANO-SPECIFIC CONSTANTS - Using FlextMeltanoConstants as SOURCE OF TRUTH
    # ============================================================================

    # Use FlextMeltanoConstants for all version constants (SOURCE OF TRUTH)
    MELTANO_VERSION: ClassVar[str] = (
        FlextMeltanoConstants.MeltanoSpecific.VERSION_REQUIRED
    )
    SINGER_SDK_VERSION: ClassVar[str] = (
        FlextMeltanoConstants.Singer.SDK_VERSION_REQUIRED
    )
    DBT_VERSION: ClassVar[str] = FlextMeltanoConstants.DBT.VERSION_REQUIRED

    # Use FlextMeltanoConstants for file constants (SOURCE OF TRUTH)
    PROJECT_FILE: ClassVar[str] = FlextMeltanoConstants.MeltanoSpecific.PROJECT_FILE
    STATE_DIR: ClassVar[str] = FlextMeltanoConstants.MeltanoSpecific.STATE_DIR
    VENV_DIR: ClassVar[str] = ".meltano/python"

    # Meltano environment variables (Meltano-specific)
    MELTANO_PROJECT_ROOT_ENV: ClassVar[str] = "MELTANO_PROJECT_ROOT"
    MELTANO_ENVIRONMENT_ENV: ClassVar[str] = "MELTANO_ENVIRONMENT"
    MELTANO_LOG_LEVEL_ENV: ClassVar[str] = "MELTANO_LOG_LEVEL"

    # ============================================================================
    # ENUMS - All enumerated types as class enums
    # ============================================================================

    class PluginType(StrEnum):
        """Plugin type enumeration for Meltano services."""

        EXTRACTORS = "extractors"
        LOADERS = "loaders"
        TRANSFORMERS = "transformers"
        ORCHESTRATORS = "orchestrators"
        FILES = "files"
        UTILITIES = "utilities"

    class EnvironmentType(StrEnum):
        """Environment type enumeration for deployment contexts."""

        DEV = "development"
        STAGING = "staging"
        PROD = "production"
        TEST = "test"
        LOCAL = "local"

    class LogLevel(StrEnum):
        """Log level enumeration for application logging."""

        DEBUG = "DEBUG"
        INFO = "INFO"
        WARNING = "WARNING"
        ERROR = "ERROR"
        CRITICAL = "CRITICAL"

    class OperationStatus(StrEnum):
        """Operation status enumeration for tracking execution states."""

        PENDING = "pending"
        RUNNING = "running"
        SUCCESS = "success"
        ERROR = "error"
        TIMEOUT = "timeout"
        CANCELLED = "cancelled"

    class RunMode(StrEnum):
        """Run mode enumeration for execution strategies."""

        FULL = "full"
        INCREMENTAL = "incremental"
        DRY_RUN = "dry_run"
        TEST = "test"

    # ============================================================================
    # MELTANO-SPECIFIC CONFIGURATION FIELDS - Additional to FlextConfig
    # ============================================================================

    # Core project configuration
    project_root: Path = Field(
        default=Path(),
        description="Root directory of the Meltano project",
    )

    meltano_version: str = Field(
        default=MELTANO_VERSION,
        description="Meltano version to use",
    )

    singer_sdk_version: str = Field(
        default=SINGER_SDK_VERSION,
        description="Singer SDK version to use",
    )

    dbt_version: str = Field(default=DBT_VERSION, description="DBT version to use")

    # Environment and execution configuration - environment field inherited from FlextConfig

    log_level: str = Field(default="INFO", description="Logging level for operations")

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
        default=RunMode.FULL,
        description="Execution mode for operations",
    )

    # Directory configuration
    config_dir: Path = Field(
        default_factory=lambda: Path(".meltano"),
        description="Configuration directory",
    )

    logs_dir: Path = Field(
        default_factory=lambda: Path("logs"),
        description="Logs directory",
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
        """Validate and convert absolute path fields.

        Args:
            v: Path or string to validate and convert.

        Returns:
            Path: Resolved absolute path.

        Raises:
            ValidationError: If path validation fails.

        """
        if isinstance(v, str):
            v = Path(v)
        return v.expanduser().resolve()

    @field_validator("config_dir", "logs_dir")
    @classmethod
    def validate_relative_paths(cls, v: Path | str) -> Path:
        """Validate relative path fields (should not be resolved to absolute).

        Args:
            v: Path or string to validate and convert.

        Returns:
            Path: Expanded but not resolved path to allow relative paths.

        """
        if isinstance(v, str):
            v = Path(v)
        return v.expanduser()  # Don't resolve to allow relative paths

    @field_validator("meltano_version", "singer_sdk_version", "dbt_version")
    @classmethod
    def validate_versions(cls, v: str) -> str:
        """Validate version strings.

        Args:
            v: Version string to validate.

        Returns:
            str: Validated and stripped version string.

        Raises:
            ValidationError: If version string is invalid.

        """
        if not v or not isinstance(v, str):
            error_msg = "Version must be non-empty string"
            raise FlextExceptions.ValidationError(error_msg)
        return v.strip()

    # ============================================================================
    # CONFIGURATION METHODS - Business logic methods
    # ============================================================================

    def get_project_file(self) -> Path:
        """Get full path to meltano project file.

        Returns:
            Path: Full path to the Meltano project file.

        """
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
        """Get absolute path to logs directory.

        Returns:
            Path: Absolute logs directory path.

        """
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
        """Validate Meltano project directory structure.

        Performs comprehensive validation of the Meltano project structure,
        checking for required directories, files, and configuration.

        Returns:
            FlextResult containing boolean validation result or error details.

        Example:
            >>> config = FlextMeltanoConfig(project_root="/path/to/project")
            >>> result = config.validate_project_structure()
            >>> if result.is_success and result.unwrap():
            ...     print("Project structure is valid")

        """
        # Use centralized validator to eliminate duplication
        return FlextMeltanoValidators.validate_meltano_project_structure(
            self.project_root,
        )

    def get_environment_variables(self) -> FlextTypes.Core.Headers:
        """Get environment variables for Meltano operations.

        This method uses FlextConfig as the base and adds Meltano-specific variables.

        Returns:
            FlextTypes.Core.Headers: Environment variables dictionary.

        Example:
            >>> config = FlextMeltanoConfig()
            >>> env_vars = config.get_environment_variables()
            >>> print(f"Meltano project root: {env_vars['MELTANO_PROJECT_ROOT']}")

        """
        return self.get_meltano_environment_variables()

    # ============================================================================
    # CONSTANTS ACCESS METHODS - Utility methods for constants
    # ============================================================================

    # ============================================================================
    # FACTORY METHODS - Instance creation and validation
    # ============================================================================

    @classmethod
    def create_from_project_root(
        cls,
        project_root: str | Path,
    ) -> FlextResult[FlextMeltanoConfig]:
        """Create configuration from project root directory.

        Creates a new configuration instance from the specified project root
        directory and validates the project structure.

        Args:
            project_root: Path to the Meltano project root directory.

        Returns:
            FlextResult containing the created configuration or error details.

        Example:
            >>> result = FlextMeltanoConfig.create_from_project_root("/path/to/project")
            >>> if result.is_success:
            ...     config = result.unwrap()
            ...     print(f"Created config for project: {config.project_root}")

        """
        try:
            config = cls(project_root=Path(project_root))
            validation_result = config.validate_project_structure()

            if validation_result.is_failure:
                return FlextResult["FlextMeltanoConfig"].fail(
                    validation_result.error or "Project validation failed",
                )

            return FlextResult["FlextMeltanoConfig"].ok(data=config)

        except Exception as e:  # pragma: no cover
            return FlextResult["FlextMeltanoConfig"].fail(
                f"Config creation failed: {e}",
            )

    @classmethod
    def create_for_environment(
        cls,
        environment: str,
        **kwargs: object,
    ) -> FlextResult[FlextMeltanoConfig]:
        """Create configuration for specific environment.

        Creates a new configuration instance optimized for the specified
        environment with appropriate defaults and validation.

        Args:
            environment: Target environment (development, staging, production, test, local).
            **kwargs: Additional configuration parameters.

        Returns:
            FlextResult containing the created configuration or error details.

        Example:
            >>> result = FlextMeltanoConfig.create_for_environment(
            ...     "production", project_root="/prod/project", log_level="WARNING"
            ... )
            >>> if result.is_success:
            ...     config = result.unwrap()
            ...     print(f"Created {config.environment} config")

        """
        try:
            # Validate environment
            try:
                env_type = cls.EnvironmentType(environment)
            except ValueError:
                return FlextResult["FlextMeltanoConfig"].fail(
                    f"Invalid environment: {environment}",
                )

            # Filter and type-cast kwargs to valid fields only
            valid_fields = cls.model_fields.keys()
            filtered_kwargs: FlextTypes.Core.Dict = {
                k: v for k, v in kwargs.items() if k in valid_fields
            }

            # Create config data with environment
            config_data: dict[str, object] = {"environment": env_type.value}

            # Handle specific type conversions
            if "project_root" in filtered_kwargs:
                project_root_value = filtered_kwargs["project_root"]
                if isinstance(project_root_value, str):
                    config_data["project_root"] = Path(project_root_value)
                elif isinstance(project_root_value, Path):
                    config_data["project_root"] = project_root_value
                else:
                    config_data["project_root"] = Path()

            if "log_level" in filtered_kwargs:
                config_data["log_level"] = cls.LogLevel(
                    str(filtered_kwargs["log_level"]),
                )

            if "run_mode" in filtered_kwargs:
                config_data["run_mode"] = cls.RunMode(str(filtered_kwargs["run_mode"]))

            # Apply all other valid kwargs with proper type handling
            excluded_keys = {"project_root", "log_level", "run_mode", "environment"}
            config_data.update(
                {
                    key: value
                    for key, value in filtered_kwargs.items()
                    if key not in excluded_keys
                },
            )

            config = cls.model_validate(config_data)
            return FlextResult["FlextMeltanoConfig"].ok(data=config)

        except Exception as e:
            return FlextResult["FlextMeltanoConfig"].fail(
                f"Environment config creation failed: {e}",
            )

    # ============================================================================
    # SINGLETON METHODS - Global instance management using FlextConfig as SOURCE OF TRUTH
    # ============================================================================

    @classmethod
    def get_global_instance(cls, **overrides: object) -> FlextMeltanoConfig:
        """Get the SINGLETON GLOBAL Meltano configuration instance.

        This method ensures a single source of truth for Meltano configuration across
        the entire application. It uses FlextConfig.get_global_instance() as the base
        and adds Meltano-specific fields. Parameters passed will override existing values.

        Args:
            **overrides: Configuration overrides that will be applied with highest priority.

        Returns:
            FlextMeltanoConfig: The global configuration instance (created if needed).

        Example:
            >>> config = FlextMeltanoConfig.get_global_instance(
            ...     project_root="/current/project", log_level="DEBUG"
            ... )
            >>> print(f"Global config: {config.project_root}")

        """
        # Always get fresh base configuration from FlextConfig singleton
        base_config = FlextConfig.get_global_instance()

        # Convert base config to dict for processing
        base_data = base_config.model_dump()

        # Apply overrides with highest priority
        base_data.update(overrides)

        # Create Meltano config instance with all data
        return cls(**base_data)

    @classmethod
    def set_global_instance(cls, config: FlextConfig) -> None:
        """Set the SINGLETON GLOBAL Meltano configuration instance.

        This method delegates to FlextConfig.set_global_instance() since FlextConfig
        is the source of truth for all configuration.

        Args:
            config: The configuration to set as global.

        Raises:
            TypeError: If config is not a FlextMeltanoConfig instance.

        Example:
            >>> config = FlextMeltanoConfig(project_root="/new/project")
            >>> FlextMeltanoConfig.set_global_instance(config)

        """
        if not isinstance(config, FlextMeltanoConfig):
            error_msg = "config must be a FlextMeltanoConfig instance"
            raise TypeError(error_msg)

        # Delegate to FlextConfig since it's the source of truth
        FlextConfig.set_global_instance(config)

    @classmethod
    def clear_global_instance(cls) -> None:
        """Clear the global instance (useful for testing).

        Removes the current global configuration instance, allowing for
        fresh configuration in test scenarios.

        Example:
            >>> FlextMeltanoConfig.clear_global_instance()
            >>> # Now get_global_instance() will create a new instance

        """
        # Delegate to FlextConfig since it's the source of truth
        FlextConfig.clear_global_instance()
        if hasattr(cls, "_global_instance"):
            cls._global_instance = None

    def apply_overrides(self, **overrides: object) -> FlextResult[None]:
        """Apply configuration overrides to this instance.

        This method allows runtime modification of configuration values,
        following the same pattern as FlextConfig.apply_environment_overrides().

        Args:
            **overrides: Configuration overrides to apply.

        Returns:
            FlextResult indicating success or failure.

        Example:
            >>> config = FlextMeltanoConfig()
            >>> result = config.apply_overrides(log_level="DEBUG", timeout_seconds=60)
            >>> if result.is_success:
            ...     print("Overrides applied successfully")

        """
        # Check if configuration is sealed
        if self.is_sealed():
            return FlextResult[None].fail(
                "Cannot apply overrides to sealed configuration",
                error_code="CONFIG_SEALED_ERROR",
            )

        try:
            for key, value in overrides.items():
                if hasattr(self, key) and key in self.__class__.model_fields:
                    setattr(self, key, value)

            # Track the override in metadata
            self.set_metadata("overrides_applied", "true")
            self.set_metadata("override_count", str(len(overrides)))

            return FlextResult[None].ok(data=None)

        except Exception as error:
            return FlextResult[None].fail(
                f"Failed to apply configuration overrides: {error}",
                error_code="OVERRIDE_APPLICATION_ERROR",
            )

    def seal(self) -> FlextResult[None]:
        """Seal the configuration to prevent further modifications.

        Once sealed, the configuration cannot be modified, ensuring
        immutability for production use.

        Returns:
            FlextResult indicating success or failure.

        Example:
            >>> config = FlextMeltanoConfig()
            >>> result = config.seal()
            >>> if result.is_success:
            ...     print("Configuration is now sealed")

        """
        self._sealed = True
        return FlextResult[None].ok(data=None)

    def is_sealed(self) -> bool:
        """Check if the configuration is sealed.

        Returns:
            bool: True if configuration is sealed, False otherwise.

        """
        return getattr(self, "_sealed", False)

    def get_meltano_environment_variables(self) -> FlextTypes.Core.Headers:
        """Get Meltano-specific environment variables.

        This method provides Meltano-specific environment variables using FlextConfig
        as the source of truth for base configuration.

        Returns:
            FlextTypes.Core.Headers: Environment variables dictionary.

        Example:
            >>> config = FlextMeltanoConfig(project_root="/my/project")
            >>> env_vars = config.get_meltano_environment_variables()
            >>> print(f"Project root: {env_vars['MELTANO_PROJECT_ROOT']}")

        """
        # Get base configuration from FlextConfig singleton
        base_config = FlextConfig.get_global_instance()

        # Create base environment variables from FlextConfig fields
        base_env_vars = {
            "FLEXT_APP_NAME": base_config.app_name,
            "FLEXT_ENVIRONMENT": str(base_config.environment),
            "FLEXT_LOG_LEVEL": str(base_config.log_level).upper(),
            "FLEXT_VERSION": "0.9.0",  # Use FlextConstants.Core.VERSION
        }

        # Add Meltano-specific environment variables
        meltano_env_vars = {
            self.MELTANO_PROJECT_ROOT_ENV: str(self.project_root),
            self.MELTANO_ENVIRONMENT_ENV: str(self.environment),
            self.MELTANO_LOG_LEVEL_ENV: str(self.log_level).upper(),
        }

        # Merge base and Meltano environment variables
        return {**base_env_vars, **meltano_env_vars}

    # ============================================================================
    # MODEL CONFIGURATION - Pydantic v2 model configuration
    # ============================================================================

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        {
            "extra": "ignore",  # Allow extra fields from environment variables
            "validate_assignment": True,
            "use_enum_values": True,
            "arbitrary_types_allowed": True,
        },
    )


__all__ = [
    "FlextMeltanoConfig",
]
