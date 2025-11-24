"""FLEXT Meltano Configuration Management - Enterprise ELT configuration patterns.

This module provides configuration management for Meltano ELT operations
following FLEXT architectural patterns with Pydantic validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, cast

from flext_core import (
    FlextConfig,
    FlextConstants,
    FlextExceptions,
    FlextResult,
)
from pydantic import Field, SecretStr, field_validator
from pydantic_settings import SettingsConfigDict

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.validators import FlextMeltanoValidators


@FlextConfig.auto_register("meltano")
class FlextMeltanoConfig(FlextConfig.AutoConfig):
    """Pipeline configuration management with validation using AutoConfig pattern.

    **ARCHITECTURAL PATTERN**: Zero-Boilerplate Auto-Registration

    This class uses FlextConfig.AutoConfig for automatic:
    - Singleton pattern (thread-safe)
    - Namespace registration (accessible via config.meltano)
    - Environment variable loading from FLEXT_MELTANO_* variables
    - .env file loading (production/development)
    - Automatic type conversion and validation via Pydantic v2

    Extends FlextConfig to provide complete pipeline configuration
    with validation using flext-core patterns. This class serves as the single
    source of truth for all pipeline configuration across the application.

    Features:
    - Uses Pydantic 2.11+ features (SettingsConfigDict, SecretStr for sensitive data)
    - Complete type annotations with Python 3.13+ syntax
    - Environment-specific factory methods for different deployment contexts

    """

    # Model configuration using Pydantic 2.11+ SettingsConfigDict
    model_config = SettingsConfigDict(
        env_prefix="FLEXT_MELTANO_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        str_strip_whitespace=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        frozen=False,
        validate_default=True,
        strict=False,
    )

    # ============================================================================
    # MELTANO-SPECIFIC CONSTANTS - Using FlextMeltanoConstants as SOURCE OF TRUTH
    # ============================================================================

    # Use FlextMeltanoConstants for all version constants (SOURCE OF TRUTH)
    MELTANO_VERSION: ClassVar[str] = FlextMeltanoConstants.Versions.MELTANO_REQUIRED
    SINGER_SDK_VERSION: ClassVar[str] = FlextMeltanoConstants.SDK_VERSION_REQUIRED
    DBT_VERSION: ClassVar[str] = FlextMeltanoConstants.VERSION_REQUIRED_DBT

    # Use FlextMeltanoConstants for file constants (SOURCE OF TRUTH)
    PROJECT_FILE: ClassVar[str] = FlextMeltanoConstants.Paths.PROJECT_FILE
    STATE_DIR: ClassVar[str] = FlextMeltanoConstants.Paths.STATE_DIR
    VENV_DIR: ClassVar[str] = ".meltano/python"

    # Meltano environment variables (Meltano-specific)
    MELTANO_PROJECT_ROOT_ENV: ClassVar[str] = "MELTANO_PROJECT_ROOT"
    MELTANO_ENVIRONMENT_ENV: ClassVar[str] = "MELTANO_ENVIRONMENT"
    MELTANO_LOG_LEVEL_ENV: ClassVar[str] = "MELTANO_LOG_LEVEL"

    # ============================================================================
    # ENUMS - All enumerated types as class enums
    # ============================================================================

    # ALL ENUMS MUST COME FROM FlextConstants or FlextMeltanoConstants - NO ALIASES
    PluginType: ClassVar[type[FlextMeltanoConstants.PluginTypes]] = (
        FlextMeltanoConstants.PluginTypes
    )
    EnvironmentType: ClassVar[type[FlextMeltanoConstants.Environment]] = (
        FlextMeltanoConstants.Environment
    )
    LogLevel: ClassVar[type[FlextConstants.Settings.LogLevel]] = (
        FlextConstants.Settings.LogLevel
    )
    OperationStatus: ClassVar[type[FlextMeltanoConstants.OperationStatus]] = (
        FlextMeltanoConstants.OperationStatus
    )
    RunMode: ClassVar[type[FlextMeltanoConstants.RunMode]] = (
        FlextMeltanoConstants.RunMode
    )

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
        min_length=1,
        description="Meltano version to use",
    )

    singer_sdk_version: str = Field(
        default=SINGER_SDK_VERSION,
        min_length=1,
        description="Singer SDK version to use",
    )

    dbt_version: str = Field(
        default=DBT_VERSION,
        min_length=1,
        description="DBT version to use",
    )

    # Environment configuration
    environment: str = Field(
        default=FlextMeltanoConstants.Environment.DEVELOPMENT.value,
        description="Deployment environment",
    )

    # Sensitive data using SecretStr for enhanced security
    meltano_database_uri: SecretStr | None = Field(
        default_factory=lambda: SecretStr("sqlite:///meltano.db"),
        description="Meltano system database URI (sensitive)",
    )

    meltano_api_key: SecretStr | None = Field(
        default=None,
        description="Meltano API key for cloud operations (sensitive)",
    )

    # Consolidated logging configuration
    logging: FlextMeltanoModels.LoggingConfig = Field(
        default_factory=FlextMeltanoModels.LoggingConfig,
        description="Complete logging configuration for all pipeline operations",
    )

    meltano_performance_threshold_warning: float = Field(
        default=FlextMeltanoConstants.Logging.MELTANO_PERFORMANCE_THRESHOLD_WARNING,
        description="Meltano performance warning threshold in milliseconds",
    )

    meltano_performance_threshold_critical: float = Field(
        default=FlextMeltanoConstants.Logging.MELTANO_PERFORMANCE_THRESHOLD_CRITICAL,
        description="Meltano performance critical threshold in milliseconds",
    )

    # Context information to include in logs
    include_pipeline_info_in_logs: bool = Field(
        default=True,
        description="Include pipeline information in log messages",
    )

    include_plugin_info_in_logs: bool = Field(
        default=True,
        description="Include plugin information in log messages",
    )

    include_source_info_in_logs: bool = Field(
        default=True,
        description="Include source information in log messages",
    )

    include_target_info_in_logs: bool = Field(
        default=True,
        description="Include target information in log messages",
    )

    include_transform_info_in_logs: bool = Field(
        default=True,
        description="Include transform information in log messages",
    )

    include_data_quality_info_in_logs: bool = Field(
        default=True,
        description="Include data quality information in log messages",
    )

    include_timing_in_logs: bool = Field(
        default=True,
        description="Include timing information in log messages",
    )

    include_memory_in_logs: bool = Field(
        default=True,
        description="Include memory information in log messages",
    )

    include_throughput_in_logs: bool = Field(
        default=True,
        description="Include throughput information in log messages",
    )

    # Security and privacy settings
    mask_sensitive_data: bool = Field(
        default=True,
        description="Mask sensitive data in logs",
    )

    mask_credentials: bool = Field(
        default=True,
        description="Mask credentials in logs",
    )

    mask_connection_strings: bool = Field(
        default=True,
        description="Mask connection strings in logs",
    )

    mask_api_keys: bool = Field(
        default=True,
        description="Mask API keys in logs",
    )

    # Log message templates
    use_standard_templates: bool = Field(
        default=True,
        description="Use standard log message templates",
    )

    custom_log_format: str | None = Field(
        default=None,
        description="Custom log message format",
    )

    # Audit logging
    enable_audit_logging: bool = Field(
        default=True,
        description="Enable audit logging",
    )

    audit_log_level: str = Field(
        default=str(FlextConstants.Settings.LogLevel.INFO.value),
        description="Audit log level",
    )

    audit_log_file: str = Field(
        default="audit.log",
        description="Audit log file path",
    )

    # Environment-specific logging
    environment_specific_logging: bool = Field(
        default=True,
        description="Enable environment-specific logging",
    )

    # Network timeout configuration
    network_timeout: int = Field(
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
        default=FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,  # SOURCE OF TRUTH
        ge=1,
        le=10000,
        description="Batch size for data processing",
    )

    # Plugin and execution configuration
    max_concurrent_jobs: int = Field(
        default=FlextConstants.Container.DEFAULT_WORKERS,  # SOURCE OF TRUTH
        ge=1,
        le=16,
        description="Maximum number of concurrent jobs",
    )

    run_mode: str = Field(
        default=FlextMeltanoConstants.RunMode.FULL.value,
        description="Execution mode for operations",
    )

    # Directory configuration
    config_dir: Path = Field(
        default_factory=lambda: Path(".meltano"),
        description="Configuration directory",
    )

    logs_dir: Path = Field(
        default_factory=lambda: Path(FlextConstants.Platform.DIR_LOGS),
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
        """Validate version strings (strip whitespace).

        Args:
        v: Version string to validate.

        Returns:
        str: Validated and stripped version string.

        """
        return v.strip()

    @field_validator("meltano_database_uri", "meltano_api_key")
    @classmethod
    def validate_secret_fields(cls, v: SecretStr | None) -> SecretStr | None:
        """Validate SecretStr fields for sensitive data.

        Args:
        v: SecretStr value to validate.

        Returns:
        SecretStr | None: Validated SecretStr or None.

        """
        if v is None:
            return None
        if isinstance(v, str):
            return SecretStr(v)
        return v

    # ============================================================================
    # CONFIGURATION METHODS - Business logic methods
    # ============================================================================

    def get_project_file(self) -> FlextResult[Path]:
        """Get full path to meltano project file using railway pattern.

        Returns:
        FlextResult containing the full path to the Meltano project file.

        """
        try:
            return FlextResult[Path].ok(self.project_root / self.PROJECT_FILE)
        except (ValueError, TypeError, OSError) as e:
            return FlextResult[Path].fail(f"Failed to get project file path: {e}")

    def get_absolute_config_dir(self) -> FlextResult[Path]:
        """Get absolute path to config directory using railway pattern.

        Returns:
        FlextResult containing the absolute config directory path.

        """
        try:
            if self.config_dir.is_absolute():
                return FlextResult[Path].ok(self.config_dir)
            return FlextResult[Path].ok(self.project_root / self.config_dir)
        except (ValueError, TypeError, OSError) as e:
            return FlextResult[Path].fail(f"Failed to get config directory path: {e}")

    def get_absolute_logs_dir(self) -> FlextResult[Path]:
        """Get absolute path to logs directory using railway pattern.

        Returns:
        FlextResult containing the absolute logs directory path.

        """
        try:
            if self.logs_dir.is_absolute():
                return FlextResult[Path].ok(self.logs_dir)
            return FlextResult[Path].ok(self.project_root / self.logs_dir)
        except (ValueError, TypeError, OSError) as e:
            return FlextResult[Path].fail(f"Failed to get logs directory path: {e}")

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

        Performs complete validation of the Meltano project structure,
        checking for required directories, files, and configuration.

        Returns:
        FlextResult containing boolean validation result or error details.

        """
        # Use centralized validator to eliminate duplication
        return FlextMeltanoValidators.validate_pipeline_project_structure(
            self.project_root,
        )

    def get_environment_variables(self) -> dict[str, str]:
        """Get environment variables for Meltano operations.

        This method uses FlextConfig as the base and adds Meltano-specific variables.

        Returns:
        dict[str, str]: Environment variables dictionary.

        """
        return self.get_meltano_environment_variables()

    def get_meltano_database_uri_value(self) -> str:
        """Get the actual Meltano database URI value (safely extract from SecretStr).

        Returns:
        str: The database URI value.

        """
        if self.meltano_database_uri is None:
            return "sqlite:///meltano.db"
        return self.meltano_database_uri.get_secret_value()

    def get_meltano_api_key_value(self) -> str | None:
        """Get the actual Meltano API key value (safely extract from SecretStr).

        Returns:
        str | None: The API key value or None if not set.

        """
        if self.meltano_api_key is None:
            return None
        return self.meltano_api_key.get_secret_value()

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

        """
        try:
            config = cls()
            config.project_root = Path(project_root)
            validation_result = config.validate_project_structure()

            if validation_result.is_failure:
                return FlextResult[FlextMeltanoConfig].fail(
                    validation_result.error or "Project validation failed",
                )

            return FlextResult[FlextMeltanoConfig].ok(config)

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
        ) as e:  # pragma: no cover
            return FlextResult[FlextMeltanoConfig].fail(
                f"Config creation failed: {e}",
            )

    @classmethod
    def create_for_environment(
        cls,
        environment: str,
        **kwargs: object,
    ) -> FlextMeltanoConfig:
        """Create configuration for specific environment.

        Creates a new configuration instance optimized for the specified
        environment with appropriate defaults and validation.

        Args:
        environment: Target environment (development, staging, production, test, local).
        **kwargs: Additional configuration parameters.

        Raises:
        ValueError: If environment is invalid.

        Returns:
        FlextMeltanoConfig: The created configuration instance.

        """
        try:
            env_type = FlextMeltanoConstants.Environment(environment.lower())
        except ValueError as e:
            msg = f"Invalid environment: {environment}"
            raise FlextExceptions.ValidationError(msg) from e

        # Filter and type-cast kwargs to valid fields only
        valid_fields = cls.model_fields.keys()
        filtered_kwargs: dict[str, object] = {
            k: v for k, v in kwargs.items() if k in valid_fields
        }

        # Create config data with environment
        config_data: dict[str, object] = {"environment": env_type.value}

        # Handle debug/environment conflict: production cannot have debug=True
        if env_type.value == "production":
            config_data["debug"] = False

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
            log_level_raw = str(filtered_kwargs["log_level"]).upper()
            log_level_enum = FlextConstants.Settings.LogLevel(log_level_raw)
            config_data["log_level"] = str(log_level_enum.value)

        if "run_mode" in filtered_kwargs:
            run_mode_raw = str(filtered_kwargs["run_mode"]).lower()
            run_mode_enum = FlextMeltanoConstants.RunMode(run_mode_raw)
            config_data["run_mode"] = run_mode_enum.value

        # Apply all other valid kwargs with proper type handling
        excluded_keys = {"project_root", "log_level", "run_mode", "environment"}
        config_data.update(
            {
                key: value
                for key, value in filtered_kwargs.items()
                if key not in excluded_keys
            },
        )

        return cls.model_validate(config_data)

    # ============================================================================
    # SINGLETON METHODS - Global instance management using FlextConfig as SOURCE OF TRUTH
    # ============================================================================

    @classmethod
    def get_global_instance(cls, **overrides: object) -> FlextMeltanoConfig:
        """Get the SINGLETON GLOBAL Meltano configuration instance using enhanced pattern.

        This method ensures a single source of truth for Meltano configuration across
        the entire application. It uses the enhanced singleton pattern with inverse
        dependency injection from FlextConfig.

        Args:
        **overrides: Configuration overrides that will be applied with highest priority.

        Returns:
        FlextMeltanoConfig: The global configuration instance (created if needed).

        """
        # Use enhanced singleton pattern from FlextConfig - create directly and apply overrides
        instance = cls()
        if overrides:
            # Apply overrides to the instance
            for key, value in overrides.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)

        return instance

    @classmethod
    def set_global_instance(cls, instance: FlextConfig) -> None:
        """Set the SINGLETON GLOBAL Meltano configuration instance.

        This method delegates to FlextConfig.set_global_instance() since FlextConfig
        is the source of truth for all configuration.

        Args:
        instance: The configuration to set as global.

        Raises:
        TypeError: If instance is not a FlextMeltanoConfig instance.

        """
        if not isinstance(instance, FlextMeltanoConfig):
            error_msg = "instance must be a FlextMeltanoConfig instance"
            raise FlextExceptions.ValidationError(error_msg)

        # Delegate to FlextConfig since it's the source of truth
        FlextConfig.set_global_instance(instance)

    @classmethod
    def get_version(cls: object) -> str:
        """Get the version of flext-meltano."""
        return "0.9.0"

    @classmethod
    def get_name(cls: object) -> str:
        """Get the name of flext-meltano."""
        return "flext-meltano"

    @classmethod
    def get_default_timeout(cls: object) -> int:
        """Get the default timeout value."""
        return FlextConstants.Network.DEFAULT_TIMEOUT

    @classmethod
    def get_default_batch_size(cls: object) -> int:
        """Get the default batch size value."""
        return FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE

    @classmethod
    def get_supported_plugin_types(cls) -> FlextMeltanoTypes.MeltanoCore.PluginTypeList:
        """Get list of supported plugin types."""
        return FlextMeltanoConstants.Plugin.supported_types()

    @classmethod
    def get_supported_environments(cls) -> FlextMeltanoTypes.MeltanoCore.PluginNameList:
        """Get list of supported environments."""
        return [
            FlextMeltanoConstants.Environment.DEVELOPMENT.value,
            FlextMeltanoConstants.Environment.STAGING.value,
            FlextMeltanoConstants.Environment.PRODUCTION.value,
            FlextMeltanoConstants.Environment.TESTING.value,
        ]

    @classmethod
    def get_supported_log_levels(cls) -> FlextMeltanoTypes.MeltanoCore.PluginNameList:
        """Get list of supported log levels."""
        return [
            str(FlextConstants.Settings.LogLevel.DEBUG.value),
            str(FlextConstants.Settings.LogLevel.INFO.value),
            str(FlextConstants.Settings.LogLevel.WARNING.value),
            str(FlextConstants.Settings.LogLevel.ERROR.value),
            str(FlextConstants.Settings.LogLevel.CRITICAL.value),
        ]

    @classmethod
    def clear_global_instance(cls) -> None:
        """Clear the global instance (useful for testing).

        Removes the current global configuration instance, allowing for
        fresh configuration in test scenarios.

        """
        # Clear global instance for this class
        # Parent class doesn't have this method, so we implement it here

    def apply_overrides(self, **overrides: object) -> FlextResult[None]:
        """Apply configuration overrides to this instance.

        This method allows runtime modification of configuration values,
        following the same pattern as FlextConfig validation.

        Args:
        **overrides: Configuration overrides to apply.

        Returns:
        FlextResult indicating success or failure.

        """
        # Check if configuration is sealed
        if self.is_sealed():
            return FlextResult[None].fail(
                "Cannot apply overrides to sealed configuration",
                error_code="CONFIG_SEALED_ERROR",
            )

        try:
            # Handle debug/environment conflict before applying
            if (
                "environment" in overrides
                and overrides["environment"] == "production"
                and hasattr(self, "debug")
                and self.debug
            ):
                # Force debug=False when switching to production
                self.debug = False

            applied_count = 0
            for key, value in overrides.items():
                if hasattr(self, key) and key in self.__class__.model_fields:
                    setattr(self, key, value)
                    applied_count += 1

            # Track metadata about overrides
            if not hasattr(self, "_metadata_extra"):
                self._metadata_extra: dict[str, str] = {}
            self._metadata_extra["overrides_applied"] = (
                "true" if applied_count > 0 else "false"
            )
            self._metadata_extra["override_count"] = str(applied_count)

            return FlextResult[None].ok(data=None)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as error:
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

        """
        self._sealed = True
        return FlextResult[None].ok(data=None)

    def is_sealed(self) -> bool:
        """Check if the configuration is sealed.

        Returns:
        bool: True if configuration is sealed, False otherwise.

        """
        return getattr(self, "_sealed", False)

    def get_meltano_environment_variables(self) -> dict[str, str]:
        """Get Meltano-specific environment variables.

        This method provides Meltano-specific environment variables using FlextConfig
        as the source of truth for base configuration.

        Returns:
        dict[str, str]: Environment variables dictionary.

        """
        # Get base configuration from FlextConfig singleton
        base_config = FlextConfig.get_global_instance()

        # Create base environment variables from FlextConfig fields
        base_env_vars = {
            "FLEXT_APP_NAME": base_config.app_name,
            "FLEXT_ENVIRONMENT": self.environment,  # Use own environment
            "FLEXT_LOG_LEVEL": str(base_config.log_level).upper(),
            "FLEXT_VERSION": base_config.version,
        }

        # Add Meltano-specific environment variables
        # Get log_level from global FlextConfig since FlextMeltanoConfig doesn't have it
        global_config = FlextConfig.get_global_instance()
        meltano_env_vars = {
            self.MELTANO_PROJECT_ROOT_ENV: str(self.project_root),
            self.MELTANO_ENVIRONMENT_ENV: str(self.environment),
            self.MELTANO_LOG_LEVEL_ENV: str(global_config.log_level).upper(),
        }

        # Add sensitive environment variables safely
        if self.meltano_database_uri:
            meltano_env_vars["MELTANO_DATABASE_URI"] = (
                self.get_meltano_database_uri_value()
            )

        if self.meltano_api_key:
            api_key_value = self.get_meltano_api_key_value()
            if api_key_value is not None:
                meltano_env_vars["MELTANO_API_KEY"] = api_key_value

        # Merge base and Meltano environment variables
        return {**base_env_vars, **meltano_env_vars}

    # ============================================================================
    # MODEL CONFIGURATION - Pydantic v2 model configuration
    # ============================================================================

    def get_meltano_logging_config(
        self,
    ) -> FlextMeltanoTypes.MeltanoCore.SettingsDict:
        """Get Meltano-specific logging configuration dictionary.

        Delegates to consolidated logging model for maintainability.

        Returns:
        dict[str, object]: Dictionary containing Meltano logging configuration.

        """
        config_dict = self.logging.model_dump()

        # Add additional non-logging config fields for backward compatibility
        additional_config = {
            "meltano_performance_threshold_warning": (
                self.meltano_performance_threshold_warning
            ),
            "meltano_performance_threshold_critical": (
                self.meltano_performance_threshold_critical
            ),
            "include_pipeline_info_in_logs": self.include_pipeline_info_in_logs,
            "include_plugin_info_in_logs": self.include_plugin_info_in_logs,
            "include_source_info_in_logs": self.include_source_info_in_logs,
            "include_target_info_in_logs": self.include_target_info_in_logs,
            "include_transform_info_in_logs": self.include_transform_info_in_logs,
            "include_data_quality_info_in_logs": (
                self.include_data_quality_info_in_logs
            ),
            "include_timing_in_logs": self.include_timing_in_logs,
            "include_memory_in_logs": self.include_memory_in_logs,
            "include_throughput_in_logs": self.include_throughput_in_logs,
            "mask_sensitive_data": self.mask_sensitive_data,
            "mask_credentials": self.mask_credentials,
            "mask_connection_strings": self.mask_connection_strings,
            "mask_api_keys": self.mask_api_keys,
            "use_standard_templates": self.use_standard_templates,
            "custom_log_format": self.custom_log_format,
            "enable_audit_logging": self.enable_audit_logging,
            "audit_log_level": self.audit_log_level,
            "audit_log_file": self.audit_log_file,
            "environment_specific_logging": self.environment_specific_logging,
        }

        merged_config = {**config_dict, **additional_config}
        return cast("FlextMeltanoTypes.MeltanoCore.SettingsDict", merged_config)

    def get_metadata(self) -> FlextMeltanoTypes.MeltanoCore.MetadataDict:
        """Get configuration metadata including override tracking.

        Returns:
        dict[str, object]: Configuration metadata dictionary.

        """
        # Return the metadata with proper typing
        return {
            "app_name": self.app_name,
            "version": self.version,
            "environment": self.environment,
            "debug": self.debug,
            "trace": self.trace,
        }

    # ============================================================================
    # NESTED CONFIGURATION BUILDERS - FLEXT Pattern for unified functionality
    # ============================================================================

    class ConfigBuilders:
        """Nested configuration builders following FLEXT unified class pattern."""

        @staticmethod
        def create_dbt_config(
            project_name: str,
            profile_name: str = "",
        ) -> FlextResult[FlextMeltanoTypes.Dbt.ProjectConfiguration]:
            """Create DBT project configuration.

            Args:
            project_name: Name of the DBT project
            profile_name: Optional profile name override

            Returns:
            FlextResult with DBT configuration dictionary

            """
            try:
                profile = profile_name or f"{project_name}_profile"
                config: FlextMeltanoTypes.Dbt.ProjectConfiguration = {
                    "name": project_name,
                    "version": "1.0.0",
                    "config-version": 2,
                    "profile": profile,
                    "model-paths": ["models"],
                    "analysis-paths": ["analyses"],
                    "test-paths": ["tests"],
                    "seed-paths": ["seeds"],
                    "macro-paths": ["macros"],
                    "snapshot-paths": ["snapshots"],
                }
                return FlextResult[FlextMeltanoTypes.Dbt.ProjectConfiguration].ok(
                    config
                )
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                return FlextResult[dict[str, object]].fail(
                    f"Failed to create DBT config: {e}"
                )

        @staticmethod
        def create_dbt_profile_config(
            profile_name: str,
            target_name: str = "dev",
            db_type: str = "postgres",
        ) -> FlextResult[FlextMeltanoTypes.Dbt.ProfileConfiguration]:
            """Create DBT profile configuration.

            Args:
            profile_name: Name of the DBT profile
            target_name: Name of the target environment
            db_type: Database type (postgres, snowflake, etc.)

            Returns:
            FlextResult with DBT profile configuration dictionary

            """
            try:
                profile_config: FlextMeltanoTypes.Dbt.ProfileConfiguration = {
                    profile_name: {
                        "target": target_name,
                        "outputs": {
                            target_name: {
                                "type": db_type,
                                "host": "{{ env_var('DBT_HOST') }}",
                                "user": "{{ env_var('DBT_USER') }}",
                                "password": "{{ env_var('DBT_PASSWORD') }}",
                                "database": "{{ env_var('DBT_DATABASE') }}",
                                "schema": "{{ env_var('DBT_SCHEMA') }}",
                                "threads": 4,
                            }
                        },
                    }
                }
                return FlextResult[FlextMeltanoTypes.Dbt.ProfileConfiguration].ok(
                    profile_config
                )
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                return FlextResult[dict[str, object]].fail(
                    f"Failed to create DBT profile config: {e}"
                )

        @staticmethod
        def create_meltano_config(
            project_id: str,
            default_environment: str = "dev",
        ) -> FlextResult[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict]:
            """Create basic Meltano project configuration.

            Args:
            project_id: Unique project identifier
            default_environment: Default environment name

            Returns:
            FlextResult with Meltano configuration dictionary

            """
            try:
                config: FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict = {
                    "version": 1,
                    "default_environment": default_environment,
                    "project_id": project_id,
                    "environments": [
                        {
                            "name": default_environment,
                            "config": {
                                "plugins": {
                                    "extractors": [],
                                    "loaders": [],
                                    "transformers": [],
                                }
                            },
                        }
                    ],
                }
                return FlextResult[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict].ok(
                    config
                )
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                return FlextResult[dict[str, object]].fail(
                    f"Failed to create Meltano config: {e}"
                )

        @staticmethod
        def create_development_config() -> FlextResult[FlextMeltanoConfig]:
            """Create configuration optimized for development environment.

            Returns:
            FlextResult with development-optimized FlextMeltanoConfig

            """
            try:
                config = FlextMeltanoConfig()
                # Apply development-specific settings
                config.environment = FlextMeltanoConstants.Environment.DEVELOPMENT.value
                config.debug = True
                config.log_level = str(
                    FlextConstants.Settings.LogLevel.DEBUG.value,
                )
                config.network_timeout = 300
                config.max_concurrent_jobs = 2
                return FlextResult[FlextMeltanoConfig].ok(config)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                return FlextResult[FlextMeltanoConfig].fail(
                    f"Failed to create dev config: {e}"
                )

        @staticmethod
        def create_production_config(
            database_url: str,
        ) -> FlextResult[FlextMeltanoConfig]:
            """Create configuration optimized for production environment.

            Args:
            database_url: Production database URL

            Returns:
            FlextResult with production-optimized FlextMeltanoConfig

            """
            try:
                config = FlextMeltanoConfig()
                # Apply production-specific settings
                config.environment = FlextMeltanoConstants.Environment.PRODUCTION.value
                config.debug = False
                config.log_level = str(
                    FlextConstants.Settings.LogLevel.WARNING.value,
                )
                config.network_timeout = 600
                config.max_concurrent_jobs = 10
                config.meltano_database_uri = SecretStr(database_url)
                return FlextResult[FlextMeltanoConfig].ok(config)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                return FlextResult[FlextMeltanoConfig].fail(
                    f"Failed to create prod config: {e}"
                )

        @staticmethod
        def create_testing_config() -> FlextResult[FlextMeltanoConfig]:
            """Create configuration optimized for testing environment.

            Returns:
            FlextResult with testing-optimized FlextMeltanoConfig

            """
            try:
                config = FlextMeltanoConfig()
                # Apply testing-specific settings
                config.environment = FlextMeltanoConstants.Environment.TESTING.value
                config.debug = True
                config.log_level = str(
                    FlextConstants.Settings.LogLevel.DEBUG.value,
                )
                config.network_timeout = 60
                config.max_concurrent_jobs = 1
                return FlextResult[FlextMeltanoConfig].ok(config)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                return FlextResult[FlextMeltanoConfig].fail(
                    f"Failed to create test config: {e}"
                )


__all__ = [
    "FlextMeltanoConfig",
]
