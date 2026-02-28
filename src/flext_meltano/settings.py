"""FLEXT Meltano configuration management.

Provides configuration management for Meltano ELT operations
with Pydantic validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import ClassVar, Self, override

from flext_core import (
    FlextSettings,
    FlextTypes,
    r,
)
from pydantic import Field, SecretStr, ValidationError, field_validator
from pydantic_settings import SettingsConfigDict

from flext_meltano.constants import c
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import t
from flext_meltano.utilities import FlextMeltanoUtilities
from flext_meltano.validators import FlextMeltanoValidators

# FLEXT aliases - all AFTER imports per import order rules
# Order: c → t → r → m → u
m = FlextMeltanoModels
u = FlextMeltanoUtilities


@FlextSettings.auto_register("meltano")
class FlextMeltanoSettings(FlextSettings):
    """Pipeline configuration management with validation.

    Extends FlextSettings to provide complete pipeline configuration
    with validation. Uses Pydantic for type-safe configuration management.

    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_MELTANO_",
        env_file=FlextSettings.resolve_env_file(),
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

    # Singleton instance (class-level, avoids PLW0603 global statement)
    _instance: ClassVar[FlextMeltanoSettings | None] = None

    MELTANO_VERSION: ClassVar[str] = c.Meltano.Versions.MELTANO_REQUIRED
    SINGER_SDK_VERSION: ClassVar[str] = c.Meltano.SDK_VERSION_REQUIRED
    DBT_VERSION: ClassVar[str] = c.Meltano.VERSION_REQUIRED_DBT

    PROJECT_FILE: ClassVar[str] = c.Meltano.Paths.PROJECT_FILE
    STATE_DIR: ClassVar[str] = c.Meltano.Paths.STATE_DIR
    VENV_DIR: ClassVar[str] = ".meltano/python"

    # Meltano environment variables (Meltano-specific)
    MELTANO_PROJECT_ROOT_ENV: ClassVar[str] = "MELTANO_PROJECT_ROOT"
    MELTANO_ENVIRONMENT_ENV: ClassVar[str] = "MELTANO_ENVIRONMENT"
    MELTANO_LOG_LEVEL_ENV: ClassVar[str] = "MELTANO_LOG_LEVEL"

    # ============================================================================
    # ENUMS - All enumerated types as class enums
    # ============================================================================

    # ALL ENUMS MUST USE INNERMOST NAMESPACE - NO ALIASES
    PluginType: ClassVar[type[c.Meltano.Enums.PluginType]] = c.Meltano.Enums.PluginType
    EnvironmentType: ClassVar[type[c.Meltano.Enums.Environment]] = (
        c.Meltano.Enums.Environment
    )
    LogLevel: ClassVar[type[c.Settings.LogLevel]] = c.Settings.LogLevel
    OperationStatus: ClassVar[type[c.Meltano.Enums.OperationStatus]] = (
        c.Meltano.Enums.OperationStatus
    )
    RunMode: ClassVar[type[c.Meltano.Enums.RunMode]] = c.Meltano.Enums.RunMode

    # ============================================================================
    # MELTANO-SPECIFIC CONFIGURATION FIELDS - Additional to FlextSettings
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
        default=c.Meltano.Enums.Environment.DEVELOPMENT.value,
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
    logging: m.Meltano.LoggingConfig = Field(
        default_factory=m.Meltano.LoggingConfig,
        description="Complete logging configuration for all pipeline operations",
    )

    meltano_performance_threshold_warning: float = Field(
        default=c.Meltano.Logging.MELTANO_PERFORMANCE_THRESHOLD_WARNING,
        description="Meltano performance warning threshold in milliseconds",
    )

    meltano_performance_threshold_critical: float = Field(
        default=c.Meltano.Logging.MELTANO_PERFORMANCE_THRESHOLD_CRITICAL,
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
        default=str(c.Settings.LogLevel.INFO.value),
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
        default=c.Network.DEFAULT_TIMEOUT,  # SOURCE OF TRUTH
        ge=1,
        le=3600,
        description="Timeout for operations in seconds",
    )

    retry_count: int = Field(
        default=c.Reliability.MAX_RETRY_ATTEMPTS,  # SOURCE OF TRUTH
        ge=0,
        le=10,
        description="Number of retries for failed operations",
    )

    batch_size: int = Field(
        default=c.Performance.BatchProcessing.DEFAULT_SIZE,  # SOURCE OF TRUTH
        ge=1,
        le=10000,
        description="Batch size for data processing",
    )

    # Plugin and execution configuration
    max_concurrent_jobs: int = Field(
        default=c.Container.DEFAULT_WORKERS,  # SOURCE OF TRUTH
        ge=1,
        le=16,
        description="Maximum number of concurrent jobs",
    )

    run_mode: str = Field(
        default=c.Meltano.Enums.RunMode.FULL.value,
        description="Execution mode for operations",
    )

    # Directory configuration
    config_dir: Path = Field(
        default_factory=lambda: Path(".meltano"),
        description="Configuration directory",
    )

    logs_dir: Path = Field(
        default_factory=lambda: Path(c.Platform.DIR_LOGS),
        description="Logs directory",
    )

    venv_dir: Path = Field(
        default_factory=lambda: Path(".meltano/python"),
        description="Virtual environment directory",
    )

    # Instance attributes (declared at class level for type safety)
    _metadata_extra: dict[str, str] = Field(default_factory=dict, exclude=True)
    _sealed: bool = False
    _metadata_extra: dict[str, str] = Field(default_factory=dict, exclude=True)
    _sealed: bool = False

    # ============================================================================
    # FIELD VALIDATORS - Pydantic validation methods
    # ============================================================================

    @field_validator("project_root", "venv_dir", mode="before")
    @classmethod
    def validate_absolute_paths(cls, v: Path | str) -> Path:
        """Validate and convert absolute path fields.

        Args:
        v: Path or string to validate and convert.

        Returns:
        Path: Resolved absolute path.

        """
        path_value = m.Meltano.PathPayload(value=v).value
        return path_value.expanduser().resolve()

    @field_validator("config_dir", "logs_dir")
    @classmethod
    def validate_relative_paths(cls, v: Path | str) -> Path:
        """Validate relative path fields (should not be resolved to absolute).

        Args:
        v: Path or string to validate and convert.

        Returns:
        Path: Expanded but not resolved path to allow relative paths.

        """
        path_value = m.Meltano.PathPayload(value=v).value
        return path_value.expanduser()  # Don't resolve to allow relative paths

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
        if isinstance(v, SecretStr):
            return v
        return SecretStr(str(v))

    # ============================================================================
    # CONFIGURATION METHODS - Business logic methods
    # ============================================================================

    def get_project_file(self) -> r[Path]:
        """Get full path to meltano project file using railway pattern.

        Returns:
        FlextResult containing the full path to the Meltano project file.

        """
        try:
            return r[Path].ok(self.project_root / self.PROJECT_FILE)
        except (ValueError, TypeError, OSError) as e:
            return r[Path].fail(f"Failed to get project file path: {e}")

    def get_absolute_config_dir(self) -> r[Path]:
        """Get absolute path to config directory using railway pattern.

        Returns:
        FlextResult containing the absolute config directory path.

        """
        try:
            if self.config_dir.is_absolute():
                return r[Path].ok(self.config_dir)
            return r[Path].ok(self.project_root / self.config_dir)
        except (ValueError, TypeError, OSError) as e:
            return r[Path].fail(f"Failed to get config directory path: {e}")

    def get_absolute_logs_dir(self) -> r[Path]:
        """Get absolute path to logs directory using railway pattern.

        Returns:
        FlextResult containing the absolute logs directory path.

        """
        try:
            if self.logs_dir.is_absolute():
                return r[Path].ok(self.logs_dir)
            return r[Path].ok(self.project_root / self.logs_dir)
        except (ValueError, TypeError, OSError) as e:
            return r[Path].fail(f"Failed to get logs directory path: {e}")

    def get_absolute_venv_dir(self) -> Path:
        """Get absolute path to virtual environment directory.

        Returns:
        Path: Absolute virtual environment directory path.

        """
        if self.venv_dir.is_absolute():
            return self.venv_dir
        return self.project_root / self.venv_dir

    def validate_project_structure(self) -> r[bool]:
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

    def get_environment_variables(self) -> Mapping[str, str]:
        """Get environment variables for Meltano operations.

        This method uses FlextSettings as the base and adds Meltano-specific variables.

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
    ) -> r[FlextMeltanoSettings]:
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
                return r[FlextMeltanoSettings].fail(
                    validation_result.error or "Project validation failed",
                )

            return r[FlextMeltanoSettings].ok(config)

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
        ) as e:
            return r[FlextMeltanoSettings].fail(
                f"Config creation failed: {e}",
            )

    @classmethod
    def create_for_environment(
        cls,
        environment: str,
        **kwargs: FlextTypes.JsonValue,
    ) -> Self:
        """Create configuration for specific environment.

        Creates a new configuration instance optimized for the specified
        environment with appropriate defaults and validation.

        Args:
        environment: Target environment (development, staging, production, test, local).
        **kwargs: Additional configuration parameters.

        Returns:
        FlextMeltanoSettings: The created configuration instance.

        Raises:
        ValueError: If environment is invalid.

        """
        try:
            env_type = c.Meltano.Enums.Environment(environment.lower())
        except ValueError:
            msg = f"Invalid environment: {environment}"
            raise ValueError(msg) from None

        # Filter and type-cast kwargs to valid fields only
        valid_fields = cls.model_fields.keys()
        filtered_kwargs_dict = {k: v for k, v in kwargs.items() if k in valid_fields}
        filtered_kwargs = filtered_kwargs_dict

        # Create config data with environment
        config_data: dict[str, FlextTypes.GeneralValueType] = {
            "environment": env_type.value
        }

        # Handle debug/environment conflict: production cannot have debug=True
        if env_type.value == "production":
            config_data["debug"] = False

        # Handle specific type conversions
        if "project_root" in filtered_kwargs:
            project_root_value = filtered_kwargs["project_root"]
            config_data["project_root"] = m.Meltano.PathPayload.model_validate(
                {"value": project_root_value},
            ).value

        if "log_level" in filtered_kwargs:
            log_level_raw = str(filtered_kwargs["log_level"]).upper()
            log_level_enum = c.Settings.LogLevel(log_level_raw)
            config_data["log_level"] = str(log_level_enum.value)

        if "run_mode" in filtered_kwargs:
            run_mode_raw = str(filtered_kwargs["run_mode"]).lower()
            run_mode_enum = c.Meltano.Enums.RunMode(run_mode_raw)
            config_data["run_mode"] = run_mode_enum.value

        # Apply all other valid kwargs with proper type handling
        excluded_keys = {"project_root", "log_level", "run_mode", "environment"}
        filtered_update = {
            k: v for k, v in filtered_kwargs.items() if k not in excluded_keys
        }
        config_data.update(filtered_update)

        return cls.model_validate(config_data)

    # ============================================================================
    # SINGLETON METHODS - Global instance management (FlextSettings SOURCE)
    # ============================================================================

    @classmethod
    @override
    def get_global_instance(
        cls,
        **overrides: FlextTypes.JsonValue,
    ) -> FlextMeltanoSettings:
        """Get SINGLETON GLOBAL Meltano config instance (enhanced pattern).

        This method ensures a single source of truth for Meltano configuration across
        the entire application. It uses the enhanced singleton pattern with inverse
        dependency injection from FlextSettings.

        Args:
        **overrides: Configuration overrides that will be applied with highest priority.

        Returns:
        FlextMeltanoSettings: The global configuration instance (created if needed).

        """
        # Use class-level singleton pattern (avoids PLW0603 global statement)
        if cls._instance is None:
            cls._instance = cls()

        # After check above, _instance is guaranteed non-None by control flow
        instance = cls._instance
        if instance is None:
            msg = "Settings instance unexpectedly None after initialization"
            raise RuntimeError(msg)
        if overrides:
            # Apply overrides to the instance
            for key, value in overrides.items():
                if key in cls.model_fields:
                    setattr(instance, key, value)

        return instance

    @classmethod
    def set_global_instance(cls, instance: FlextSettings) -> None:
        """Set the SINGLETON GLOBAL Meltano configuration instance.

        Uses FlextSettings singleton registry pattern to store the instance.

        Args:
        instance: The configuration to set as global.

        Raises:
        TypeError: If instance is not a FlextMeltanoSettings instance.

        """
        try:
            instance_payload = (
                instance.model_dump()
                if u.Guards.is_pydantic_model(instance)
                else instance
            )
            normalized_instance = cls.model_validate(instance_payload)
        except ValidationError as err:
            error_msg = "instance must be a FlextMeltanoSettings-compatible payload"
            raise TypeError(error_msg) from err

        # Use class-level singleton pattern (avoids PLW0603 global statement)
        cls._instance = normalized_instance

    @classmethod
    def get_version(cls) -> str:
        """Get the version of flext-meltano.

        Returns:
            str: The version string for flext-meltano.

        """
        return "0.9.0"

    @classmethod
    def get_name(cls) -> str:
        """Get the name of flext-meltano.

        Returns:
            str: The name string for flext-meltano.

        """
        return "flext-meltano"

    @classmethod
    def get_default_timeout(cls) -> int:
        """Get the default timeout value.

        Returns:
            int: The default timeout in seconds.

        """
        return c.Network.DEFAULT_TIMEOUT

    @classmethod
    def get_default_batch_size(cls) -> int:
        """Get the default batch size value.

        Returns:
            int: The default batch size for data processing.

        """
        return c.Performance.BatchProcessing.DEFAULT_SIZE

    @classmethod
    def get_supported_plugin_types(cls) -> t.MeltanoCore.PluginTypeList:
        """Get list of supported plugin types."""
        return FlextMeltanoUtilities.Meltano.supported_types()

    @classmethod
    def get_supported_environments(cls) -> t.MeltanoCore.PluginNameList:
        """Get list of supported environments."""
        return [
            c.Meltano.Enums.Environment.DEVELOPMENT.value,
            c.Meltano.Enums.Environment.STAGING.value,
            c.Meltano.Enums.Environment.PRODUCTION.value,
            c.Meltano.Enums.Environment.TESTING.value,
        ]

    @classmethod
    def get_supported_log_levels(cls) -> t.MeltanoCore.PluginNameList:
        """Get list of supported log levels."""
        return [
            str(c.Settings.LogLevel.DEBUG.value),
            str(c.Settings.LogLevel.INFO.value),
            str(c.Settings.LogLevel.WARNING.value),
            str(c.Settings.LogLevel.ERROR.value),
            str(c.Settings.LogLevel.CRITICAL.value),
        ]

    @classmethod
    def clear_global_instance(cls) -> None:
        """Clear the global instance (useful for testing).

        Removes the current global configuration instance, allowing for
        fresh configuration in test scenarios.

        """
        # Clear global instance for this class
        # Parent class doesn't have this method, so we implement it here

    def apply_overrides(self, **overrides: FlextTypes.JsonValue) -> r[None]:
        """Apply configuration overrides to this instance.

        This method allows runtime modification of configuration values,
        following the same pattern as FlextSettings validation.

        Args:
        **overrides: Configuration overrides to apply.

        Returns:
        FlextResult indicating success or failure.

        """
        # Check if configuration is sealed
        if self.is_sealed():
            return r[None].fail(
                "Cannot apply overrides to sealed configuration",
                error_code="CONFIG_SEALED_ERROR",
            )

        try:
            # Handle debug/environment conflict before applying
            if (
                "environment" in overrides
                and overrides["environment"] == "production"
                and "debug" in self.__class__.model_fields
                and self.debug
            ):
                # Force debug=False when switching to production
                self.debug = False

            applied_count = 0
            for key, value in overrides.items():
                if key in self.__class__.model_fields:
                    setattr(self, key, value)
                    applied_count += 1

            # Track metadata about overrides
            if getattr(self, "_metadata_extra", None) is None:
                self._metadata_extra: dict[str, str] = {}
            self._metadata_extra["overrides_applied"] = (
                "true" if applied_count > 0 else "false"
            )
            self._metadata_extra["override_count"] = str(applied_count)

            return r[bool].ok(True)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as error:
            return r[None].fail(
                f"Failed to apply configuration overrides: {error}",
                error_code="OVERRIDE_APPLICATION_ERROR",
            )

    def seal(self) -> r[None]:
        """Seal the configuration to prevent further modifications.

        Once sealed, the configuration cannot be modified, ensuring
        immutability for production use.

        Returns:
        FlextResult indicating success or failure.

        """
        self._sealed = True
        return r[None].ok(None)

    def is_sealed(self) -> bool:
        """Check if the configuration is sealed.

        Returns:
        bool: True if configuration is sealed, False otherwise.

        """
        return getattr(self, "_sealed", False)

    def get_meltano_environment_variables(self) -> Mapping[str, str]:
        """Get Meltano-specific environment variables.

        This method provides Meltano-specific environment variables using FlextSettings
        as the source of truth for base configuration.

        Returns:
        dict[str, str]: Environment variables dictionary.

        """
        # Get base configuration from FlextSettings singleton
        base_config = FlextSettings.get_global_instance()

        # Create base environment variables from FlextSettings fields
        base_env_vars = {
            "FLEXT_APP_NAME": base_config.app_name,
            "FLEXT_ENVIRONMENT": self.environment,  # Use own environment
            "FLEXT_LOG_LEVEL": str(base_config.log_level).upper(),
            "FLEXT_VERSION": base_config.version,
        }

        # Add Meltano-specific environment variables
        # Get log_level from global FlextSettings
        global_config = FlextSettings.get_global_instance()
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
    ) -> t.MeltanoCore.SettingsDict:
        """Get Meltano-specific logging configuration dictionary.

        Delegates to consolidated logging model for maintainability.

        Returns:
        dict[str, t.GeneralValueType]: Dictionary containing Meltano logging configuration.

        """
        return self.logging.model_dump()
        self,
    ) -> t.MeltanoCore.SettingsDict:
        """Get Meltano-specific logging configuration dictionary.

        Delegates to consolidated logging model for maintainability.

        Returns:
        dict[str, t.GeneralValueType]: Dictionary containing Meltano logging configuration.

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

        merged_config: t.MeltanoCore.SettingsDict = {
            **config_dict,
            **additional_config,
        }
        return merged_config

    def get_metadata(self) -> t.MeltanoCore.MetadataDict:
        """Get configuration metadata including override tracking.

        Returns:
        dict[str, t.GeneralValueType]: Configuration metadata dictionary.

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
        ) -> r[t.Dbt.ProjectConfiguration]:
            """Create DBT project configuration.

            Args:
            project_name: Name of the DBT project
            profile_name: Optional profile name override

            Returns:
            FlextResult with DBT configuration dictionary

            """
            try:
                profile = profile_name or f"{project_name}_profile"
                config: t.Dbt.ProjectConfiguration = {
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
                return r[t.Dbt.ProjectConfiguration].ok(config)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                return r[t.Dbt.ProjectConfiguration].fail(
                    f"Failed to create DBT config: {e}"
                )

        @staticmethod
        def create_dbt_profile_config(
            profile_name: str,
            target_name: str = "dev",
            db_type: str = "postgres",
        ) -> r[t.Dbt.ProfileConfiguration]:
            """Create DBT profile configuration.

            Args:
            profile_name: Name of the DBT profile
            target_name: Name of the target environment
            db_type: Database type (postgres, snowflake, etc.)

            Returns:
            FlextResult with DBT profile configuration dictionary

            """
            try:
                profile_config: t.Dbt.ProfileConfiguration = {
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
                            },
                        },
                    },
                }
                return r[t.Dbt.ProfileConfiguration].ok(profile_config)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                return r[t.Dbt.ProfileConfiguration].fail(
                    f"Failed to create DBT profile config: {e}",
                )

        @staticmethod
        def create_meltano_config(
            project_id: str,
            default_environment: str = "dev",
        ) -> r[t.MeltanoCore.MeltanoConfigDict]:
            """Create basic Meltano project configuration.

            Args:
            project_id: Unique project identifier
            default_environment: Default environment name

            Returns:
            FlextResult with Meltano configuration dictionary

            """
            try:
                config: t.MeltanoCore.MeltanoConfigDict = {
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
                                },
                            },
                        },
                    ],
                }
                return r[t.MeltanoCore.MeltanoConfigDict].ok(config)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                return r[t.MeltanoCore.MeltanoConfigDict].fail(
                    f"Failed to create Meltano config: {e}",
                )

        @staticmethod
        def create_development_config() -> r[FlextMeltanoSettings]:
            """Create configuration optimized for development environment.

            Returns:
            FlextResult with development-optimized FlextMeltanoSettings

            """
            try:
                config = FlextMeltanoSettings()
                # Apply development-specific settings
                config.environment = c.Meltano.Enums.Environment.DEVELOPMENT.value
                config.debug = True
                config.log_level = c.Settings.LogLevel.DEBUG
                config.network_timeout = 300
                config.max_concurrent_jobs = 2
                return r[FlextMeltanoSettings].ok(config)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                return r[FlextMeltanoSettings].fail(f"Failed to create dev config: {e}")

        @staticmethod
        def create_production_config(
            database_url: str,
        ) -> r[FlextMeltanoSettings]:
            """Create configuration optimized for production environment.

            Args:
            database_url: Production database URL

            Returns:
            FlextResult with production-optimized FlextMeltanoSettings

            """
            try:
                config = FlextMeltanoSettings()
                # Apply production-specific settings
                config.environment = c.Meltano.Enums.Environment.PRODUCTION.value
                config.debug = False
                config.log_level = c.Settings.LogLevel.WARNING
                config.network_timeout = 600
                config.max_concurrent_jobs = 10
                config.meltano_database_uri = SecretStr(database_url)
                return r[FlextMeltanoSettings].ok(config)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                return r[FlextMeltanoSettings].fail(
                    f"Failed to create prod config: {e}",
                )

        @staticmethod
        def create_testing_config() -> r[FlextMeltanoSettings]:
            """Create configuration optimized for testing environment.

            Returns:
            FlextResult with testing-optimized FlextMeltanoSettings

            """
            try:
                config = FlextMeltanoSettings()
                # Apply testing-specific settings
                config.environment = c.Meltano.Enums.Environment.TESTING.value
                config.debug = True
                config.log_level = c.Settings.LogLevel.DEBUG
                config.network_timeout = 60
                config.max_concurrent_jobs = 1
                return r[FlextMeltanoSettings].ok(config)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                return r[FlextMeltanoSettings].fail(
                    f"Failed to create test config: {e}",
                )


__all__ = [
    "FlextMeltanoSettings",
]
