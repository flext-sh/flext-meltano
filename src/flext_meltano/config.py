"""FLEXT Meltano Configuration Management - Enterprise ELT configuration patterns.

This module provides configuration management for Meltano ELT operations
following FLEXT architectural patterns with Pydantic validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from flext_core import FlextCore
from flext_core.constants import FlextCore
from pydantic import Field, SecretStr, field_validator
from pydantic_settings import SettingsConfigDict

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.validators import FlextMeltanoValidators


class FlextMeltanoConfig(FlextCore.Config):
    """Meltano ELT configuration management with enterprise-grade validation.

    Extends FlextCore.Config to provide comprehensive Meltano-specific configuration
    with validation using flext-core patterns. This class serves as the single
    source of truth for all Meltano configuration across the application.

    Features:
    - Uses Pydantic 2.11+ features (SettingsConfigDict, SecretStr for sensitive data)
    - Enhanced singleton pattern with get_or_create_shared_instance()
    - Complete type annotations with Python 3.13+ syntax
    - Environment-specific factory methods for different deployment contexts

    """

    # Model configuration using Pydantic 2.11+ SettingsConfigDict
    model_config = SettingsConfigDict(
        env_prefix="FLEXT_MELTANO_",
        case_sensitive=False,
        extra="ignore",
        str_strip_whitespace=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        frozen=False,
    )

    # ============================================================================
    # MELTANO-SPECIFIC CONSTANTS - Using FlextMeltanoConstants as SOURCE OF TRUTH
    # ============================================================================

    # Use FlextMeltanoConstants for all version constants (SOURCE OF TRUTH)
    MELTANO_VERSION: ClassVar[str] = FlextMeltanoConstants.Meltano.VERSION_REQUIRED
    SINGER_SDK_VERSION: ClassVar[str] = (
        FlextMeltanoConstants.Singer.SDK_VERSION_REQUIRED
    )
    DBT_VERSION: ClassVar[str] = FlextMeltanoConstants.Dbt.VERSION_REQUIRED

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

    # ALL ENUMS MUST COME FROM FlextCore.Constants or FlextMeltanoConstants - NO ALIASES
    PluginType: type = FlextMeltanoConstants.PluginTypes  # Domain-specific constants
    EnvironmentType: type = FlextCore.Constants.Config.Environment  # Core constants
    LogLevel: type = FlextCore.Constants.Config.LogLevel  # Core constants
    OperationStatus: type = (
        FlextMeltanoConstants.OperationStatus
    )  # Domain-specific constants
    RunMode: type = FlextMeltanoConstants.RunMode  # Domain-specific constants

    # ============================================================================
    # MELTANO-SPECIFIC CONFIGURATION FIELDS - Additional to FlextCore.Config
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

    # Environment configuration
    environment: str = Field(
        default=FlextCore.Constants.Config.Environment.DEVELOPMENT,
        description="Deployment environment",
    )

    log_level: str = Field(
        default=FlextCore.Constants.Config.LogLevel.INFO,  # SOURCE OF TRUTH
        description="Logging level for operations",
    )

    timeout_seconds: int = Field(
        default=FlextCore.Constants.Defaults.TIMEOUT,
        ge=1,
        le=3600,
        description="Timeout for operations in seconds",
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

    # Meltano-specific logging configuration using FlextMeltanoConstants
    log_pipeline_execution: bool = Field(
        default=True,
        description="Log pipeline execution details",
    )

    log_pipeline_stages: bool = Field(
        default=True,
        description="Log pipeline stage execution",
    )

    log_pipeline_progress: bool = Field(
        default=FlextMeltanoConstants.MeltanoLogging.LOG_PIPELINE_PROGRESS,
        description="Log pipeline progress updates",
    )

    log_pipeline_errors: bool = Field(
        default=FlextMeltanoConstants.MeltanoLogging.LOG_PIPELINE_ERRORS,
        description="Log pipeline errors",
    )

    log_pipeline_warnings: bool = Field(
        default=True,
        description="Log pipeline warnings",
    )

    log_pipeline_performance: bool = Field(
        default=True,
        description="Log pipeline performance metrics",
    )

    log_pipeline_timing: bool = Field(
        default=True,
        description="Log pipeline timing information",
    )

    log_pipeline_memory: bool = Field(
        default=True,
        description="Log pipeline memory usage",
    )

    log_pipeline_throughput: bool = Field(
        default=True,
        description="Log pipeline throughput metrics",
    )

    # Extract operations logging
    log_extract_operations: bool = Field(
        default=True,
        description="Log extract operations",
    )

    log_extract_queries: bool = Field(
        default=True,
        description="Log extract queries",
    )

    log_extract_results: bool = Field(
        default=True,
        description="Log extract results",
    )

    log_extract_errors: bool = Field(
        default=FlextMeltanoConstants.MeltanoLogging.LOG_EXTRACT_ERRORS,
        description="Log extract errors",
    )

    log_extract_performance: bool = Field(
        default=True,
        description="Log extract performance metrics",
    )

    log_extract_timing: bool = Field(
        default=True,
        description="Log extract timing information",
    )

    log_extract_memory: bool = Field(
        default=True,
        description="Log extract memory usage",
    )

    log_extract_throughput: bool = Field(
        default=True,
        description="Log extract throughput metrics",
    )

    # Load operations logging
    log_load_operations: bool = Field(
        default=True,
        description="Log load operations",
    )

    log_load_batches: bool = Field(
        default=True,
        description="Log load batches",
    )

    log_load_results: bool = Field(
        default=True,
        description="Log load results",
    )

    log_load_errors: bool = Field(
        default=FlextMeltanoConstants.MeltanoLogging.LOG_LOAD_ERRORS,
        description="Log load errors",
    )

    log_load_performance: bool = Field(
        default=True,
        description="Log load performance metrics",
    )

    log_load_timing: bool = Field(
        default=True,
        description="Log load timing information",
    )

    log_load_memory: bool = Field(
        default=True,
        description="Log load memory usage",
    )

    log_load_throughput: bool = Field(
        default=True,
        description="Log load throughput metrics",
    )

    # Transform operations logging
    log_transform_operations: bool = Field(
        default=True,
        description="Log transform operations",
    )

    log_transform_sql: bool = Field(
        default=FlextMeltanoConstants.MeltanoLogging.LOG_TRANSFORM_SQL,
        description="Log transform SQL queries",
    )

    log_transform_results: bool = Field(
        default=True,
        description="Log transform results",
    )

    log_transform_errors: bool = Field(
        default=FlextMeltanoConstants.MeltanoLogging.LOG_TRANSFORM_ERRORS,
        description="Log transform errors",
    )

    log_transform_performance: bool = Field(
        default=True,
        description="Log transform performance metrics",
    )

    log_transform_timing: bool = Field(
        default=True,
        description="Log transform timing information",
    )

    log_transform_memory: bool = Field(
        default=True,
        description="Log transform memory usage",
    )

    log_transform_throughput: bool = Field(
        default=True,
        description="Log transform throughput metrics",
    )

    # Data quality logging
    log_data_quality: bool = Field(
        default=True,
        description="Log data quality checks",
    )

    log_data_quality_checks: bool = Field(
        default=True,
        description="Log data quality check results",
    )

    log_data_quality_errors: bool = Field(
        default=True,
        description="Log data quality errors",
    )

    log_data_quality_warnings: bool = Field(
        default=True,
        description="Log data quality warnings",
    )

    log_data_quality_metrics: bool = Field(
        default=True,
        description="Log data quality metrics",
    )

    log_data_quality_timing: bool = Field(
        default=True,
        description="Log data quality timing information",
    )

    log_data_quality_memory: bool = Field(
        default=True,
        description="Log data quality memory usage",
    )

    log_data_quality_throughput: bool = Field(
        default=True,
        description="Log data quality throughput metrics",
    )

    # Plugin logging
    log_plugin_operations: bool = Field(
        default=True,
        description="Log plugin operations",
    )

    log_plugin_errors: bool = Field(
        default=True,
        description="Log plugin errors",
    )

    log_plugin_performance: bool = Field(
        default=True,
        description="Log plugin performance metrics",
    )

    log_plugin_timing: bool = Field(
        default=True,
        description="Log plugin timing information",
    )

    log_plugin_memory: bool = Field(
        default=True,
        description="Log plugin memory usage",
    )

    log_plugin_throughput: bool = Field(
        default=True,
        description="Log plugin throughput metrics",
    )

    # Source and target logging
    log_source_info: bool = Field(
        default=True,
        description="Log source information",
    )

    log_target_info: bool = Field(
        default=True,
        description="Log target information",
    )

    log_source_errors: bool = Field(
        default=True,
        description="Log source errors",
    )

    log_target_errors: bool = Field(
        default=True,
        description="Log target errors",
    )

    log_source_performance: bool = Field(
        default=True,
        description="Log source performance metrics",
    )

    log_target_performance: bool = Field(
        default=True,
        description="Log target performance metrics",
    )

    log_source_timing: bool = Field(
        default=True,
        description="Log source timing information",
    )

    log_target_timing: bool = Field(
        default=True,
        description="Log target timing information",
    )

    log_source_memory: bool = Field(
        default=True,
        description="Log source memory usage",
    )

    log_target_memory: bool = Field(
        default=True,
        description="Log target memory usage",
    )

    log_source_throughput: bool = Field(
        default=True,
        description="Log source throughput metrics",
    )

    log_target_throughput: bool = Field(
        default=True,
        description="Log target throughput metrics",
    )

    # Performance tracking for Meltano operations
    track_meltano_performance: bool = Field(
        default=FlextMeltanoConstants.MeltanoLogging.TRACK_MELTANO_PERFORMANCE,
        description="Track Meltano performance metrics",
    )

    meltano_performance_threshold_warning: float = Field(
        default=FlextMeltanoConstants.MeltanoLogging.MELTANO_PERFORMANCE_THRESHOLD_WARNING,
        description="Meltano performance warning threshold in milliseconds",
    )

    meltano_performance_threshold_critical: float = Field(
        default=FlextMeltanoConstants.MeltanoLogging.MELTANO_PERFORMANCE_THRESHOLD_CRITICAL,
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
        default="INFO",
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
        default=30,  # Default timeout in seconds
        ge=1,
        le=3600,
        description="Timeout for operations in seconds",
    )

    retry_count: int = Field(
        default=FlextCore.Constants.Reliability.MAX_RETRY_ATTEMPTS,  # SOURCE OF TRUTH
        ge=0,
        le=10,
        description="Number of retries for failed operations",
    )

    batch_size: int = Field(
        default=FlextCore.Constants.Performance.BatchProcessing.DEFAULT_SIZE,  # SOURCE OF TRUTH
        ge=1,
        le=10000,
        description="Batch size for data processing",
    )

    # Plugin and execution configuration
    max_concurrent_jobs: int = Field(
        default=FlextCore.Constants.Container.MAX_WORKERS,  # SOURCE OF TRUTH
        ge=1,
        le=16,
        description="Maximum number of concurrent jobs",
    )

    run_mode: str = Field(
        default="FULL",
        description="Execution mode for operations",
    )

    # Directory configuration
    config_dir: Path = Field(
        default_factory=lambda: Path(".meltano"),
        description="Configuration directory",
    )

    logs_dir: Path = Field(
        default_factory=lambda: Path(FlextCore.Constants.Platform.DIR_LOGS),
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
        """Validate version strings.

        Args:
            v: Version string to validate.

        Returns:
            str: Validated and stripped version string.

        Raises:
            ValidationError: If version string is invalid.

        """
        if not v:
            error_msg = "Version must be non-empty string"
            raise FlextCore.Exceptions.ValidationError(error_msg)
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

    def validate_project_structure(self) -> FlextCore.Result[bool]:
        """Validate Meltano project directory structure.

        Performs comprehensive validation of the Meltano project structure,
        checking for required directories, files, and configuration.

        Returns:
            FlextCore.Result containing boolean validation result or error details.

        """
        # Use centralized validator to eliminate duplication
        return FlextMeltanoValidators.validate_meltano_project_structure(
            self.project_root,
        )

    def get_environment_variables(self) -> FlextCore.Types.StringDict:
        """Get environment variables for Meltano operations.

        This method uses FlextCore.Config as the base and adds Meltano-specific variables.

        Returns:
            FlextCore.Types.StringDict: Environment variables dictionary.

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
    ) -> FlextCore.Result[FlextMeltanoConfig]:
        """Create configuration from project root directory.

        Creates a new configuration instance from the specified project root
        directory and validates the project structure.

        Args:
            project_root: Path to the Meltano project root directory.

        Returns:
            FlextCore.Result containing the created configuration or error details.

        """
        try:
            config = cls()
            config.project_root = Path(project_root)
            validation_result = config.validate_project_structure()

            if validation_result.is_failure:
                return FlextCore.Result[FlextMeltanoConfig].fail(
                    validation_result.error or "Project validation failed",
                )

            return FlextCore.Result[FlextMeltanoConfig].ok(config)

        except Exception as e:  # pragma: no cover
            return FlextCore.Result[FlextMeltanoConfig].fail(
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
        # Validate environment using FlextCore.Constants
        try:
            env_type = FlextCore.Constants.Config.Environment(environment)
        except ValueError as e:
            msg = f"Invalid environment: {environment}"
            raise ValueError(msg) from e

        # Filter and type-cast kwargs to valid fields only
        valid_fields = cls.model_fields.keys()
        filtered_kwargs: FlextCore.Types.Dict = {
            k: v for k, v in kwargs.items() if k in valid_fields
        }

        # Create config data with environment
        config_data: FlextCore.Types.Dict = {"environment": env_type.value}

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
            config_data["log_level"] = FlextCore.Constants.Config.LogLevel(
                str(filtered_kwargs["log_level"]),
            )

        if "run_mode" in filtered_kwargs:
            config_data["run_mode"] = FlextMeltanoConstants.RunMode(
                str(filtered_kwargs["run_mode"])
            )

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
    # SINGLETON METHODS - Global instance management using FlextCore.Config as SOURCE OF TRUTH
    # ============================================================================

    @classmethod
    def get_global_instance(cls, **overrides: object) -> FlextMeltanoConfig:
        """Get the SINGLETON GLOBAL Meltano configuration instance using enhanced pattern.

        This method ensures a single source of truth for Meltano configuration across
        the entire application. It uses the enhanced singleton pattern with inverse
        dependency injection from FlextCore.Config.

        Args:
            **overrides: Configuration overrides that will be applied with highest priority.

        Returns:
            FlextMeltanoConfig: The global configuration instance (created if needed).

        """
        # Use enhanced singleton pattern from FlextCore.Config - create directly and apply overrides
        instance = cls()
        if overrides:
            # Apply overrides to the instance
            for key, value in overrides.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)

        return instance

    @classmethod
    def set_global_instance(cls, instance: FlextCore.Config) -> None:
        """Set the SINGLETON GLOBAL Meltano configuration instance.

        This method delegates to FlextCore.Config.set_global_instance() since FlextCore.Config
        is the source of truth for all configuration.

        Args:
            instance: The configuration to set as global.

        Raises:
            TypeError: If instance is not a FlextMeltanoConfig instance.

        """
        if not isinstance(instance, FlextMeltanoConfig):
            error_msg = "instance must be a FlextMeltanoConfig instance"
            raise TypeError(error_msg)

        # Delegate to FlextCore.Config since it's the source of truth
        FlextCore.Config.set_global_instance(instance)

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
        return FlextCore.Constants.Network.DEFAULT_TIMEOUT

    @classmethod
    def get_default_batch_size(cls: object) -> int:
        """Get the default batch size value."""
        return FlextCore.Constants.Performance.BatchProcessing.DEFAULT_SIZE

    @classmethod
    def get_supported_plugin_types(cls) -> FlextMeltanoTypes.MeltanoCore.PluginTypeList:
        """Get list of supported plugin types."""
        return [
            "extractors",
            "loaders",
            "transformers",
            "orchestrators",
            "utilities",
            "files",
        ]

    @classmethod
    def get_supported_environments(cls) -> FlextMeltanoTypes.MeltanoCore.PluginNameList:
        """Get list of supported environments."""
        return ["development", "staging", "production", "test"]

    @classmethod
    def get_supported_log_levels(cls) -> FlextMeltanoTypes.MeltanoCore.PluginNameList:
        """Get list of supported log levels."""
        return ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    @classmethod
    def clear_global_instance(cls) -> None:
        """Clear the global instance (useful for testing).

        Removes the current global configuration instance, allowing for
        fresh configuration in test scenarios.

        """
        # Clear global instance for this class
        # Parent class doesn't have this method, so we implement it here

    def apply_overrides(self, **overrides: object) -> FlextCore.Result[None]:
        """Apply configuration overrides to this instance.

        This method allows runtime modification of configuration values,
        following the same pattern as FlextCore.Config validation.

        Args:
            **overrides: Configuration overrides to apply.

        Returns:
            FlextCore.Result indicating success or failure.

        """
        # Check if configuration is sealed
        if self.is_sealed():
            return FlextCore.Result[None].fail(
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
                setattr(self, "debug", False)

            applied_count = 0
            for key, value in overrides.items():
                if hasattr(self, key) and key in self.__class__.model_fields:
                    setattr(self, key, value)
                    applied_count += 1

            # Track metadata about overrides
            if not hasattr(self, "_metadata_extra"):
                self._metadata_extra = {}
            self._metadata_extra["overrides_applied"] = (
                "true" if applied_count > 0 else "false"
            )
            self._metadata_extra["override_count"] = str(applied_count)

            return FlextCore.Result[None].ok(data=None)

        except Exception as error:
            return FlextCore.Result[None].fail(
                f"Failed to apply configuration overrides: {error}",
                error_code="OVERRIDE_APPLICATION_ERROR",
            )

    def seal(self) -> FlextCore.Result[None]:
        """Seal the configuration to prevent further modifications.

        Once sealed, the configuration cannot be modified, ensuring
        immutability for production use.

        Returns:
            FlextCore.Result indicating success or failure.

        """
        self._sealed = True
        return FlextCore.Result[None].ok(data=None)

    def is_sealed(self) -> bool:
        """Check if the configuration is sealed.

        Returns:
            bool: True if configuration is sealed, False otherwise.

        """
        return getattr(self, "_sealed", False)

    def get_meltano_environment_variables(self) -> FlextCore.Types.StringDict:
        """Get Meltano-specific environment variables.

        This method provides Meltano-specific environment variables using FlextCore.Config
        as the source of truth for base configuration.

        Returns:
            FlextCore.Types.StringDict: Environment variables dictionary.

        """
        # Get base configuration from FlextCore.Config singleton
        base_config = FlextCore.Config.get_global_instance()

        # Create base environment variables from FlextCore.Config fields
        base_env_vars = {
            "FLEXT_APP_NAME": base_config.app_name,
            "FLEXT_ENVIRONMENT": self.environment,  # Use own environment
            "FLEXT_LOG_LEVEL": str(base_config.log_level).upper(),
            "FLEXT_VERSION": base_config.version,
        }

        # Add Meltano-specific environment variables
        meltano_env_vars = {
            self.MELTANO_PROJECT_ROOT_ENV: str(self.project_root),
            self.MELTANO_ENVIRONMENT_ENV: str(self.environment),
            self.MELTANO_LOG_LEVEL_ENV: str(self.log_level).upper(),
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

    def get_meltano_logging_config(self) -> FlextCore.Types.Dict:
        """Get Meltano-specific logging configuration dictionary.

        Returns:
            FlextCore.Types.Dict: Dictionary containing Meltano logging configuration.

        """
        return {
            "log_pipeline_execution": self.log_pipeline_execution,
            "log_pipeline_stages": self.log_pipeline_stages,
            "log_pipeline_progress": self.log_pipeline_progress,
            "log_pipeline_errors": self.log_pipeline_errors,
            "log_pipeline_warnings": self.log_pipeline_warnings,
            "log_pipeline_performance": self.log_pipeline_performance,
            "log_pipeline_timing": self.log_pipeline_timing,
            "log_pipeline_memory": self.log_pipeline_memory,
            "log_pipeline_throughput": self.log_pipeline_throughput,
            "log_extract_operations": self.log_extract_operations,
            "log_extract_queries": self.log_extract_queries,
            "log_extract_results": self.log_extract_results,
            "log_extract_errors": self.log_extract_errors,
            "log_extract_performance": self.log_extract_performance,
            "log_extract_timing": self.log_extract_timing,
            "log_extract_memory": self.log_extract_memory,
            "log_extract_throughput": self.log_extract_throughput,
            "log_load_operations": self.log_load_operations,
            "log_load_batches": self.log_load_batches,
            "log_load_results": self.log_load_results,
            "log_load_errors": self.log_load_errors,
            "log_load_performance": self.log_load_performance,
            "log_load_timing": self.log_load_timing,
            "log_load_memory": self.log_load_memory,
            "log_load_throughput": self.log_load_throughput,
            "log_transform_operations": self.log_transform_operations,
            "log_transform_sql": self.log_transform_sql,
            "log_transform_results": self.log_transform_results,
            "log_transform_errors": self.log_transform_errors,
            "log_transform_performance": self.log_transform_performance,
            "log_transform_timing": self.log_transform_timing,
            "log_transform_memory": self.log_transform_memory,
            "log_transform_throughput": self.log_transform_throughput,
            "log_data_quality": self.log_data_quality,
            "log_data_quality_checks": self.log_data_quality_checks,
            "log_data_quality_errors": self.log_data_quality_errors,
            "log_data_quality_warnings": self.log_data_quality_warnings,
            "log_data_quality_metrics": self.log_data_quality_metrics,
            "log_data_quality_timing": self.log_data_quality_timing,
            "log_data_quality_memory": self.log_data_quality_memory,
            "log_data_quality_throughput": self.log_data_quality_throughput,
            "log_plugin_operations": self.log_plugin_operations,
            "log_plugin_errors": self.log_plugin_errors,
            "log_plugin_performance": self.log_plugin_performance,
            "log_plugin_timing": self.log_plugin_timing,
            "log_plugin_memory": self.log_plugin_memory,
            "log_plugin_throughput": self.log_plugin_throughput,
            "log_source_info": self.log_source_info,
            "log_target_info": self.log_target_info,
            "log_source_errors": self.log_source_errors,
            "log_target_errors": self.log_target_errors,
            "log_source_performance": self.log_source_performance,
            "log_target_performance": self.log_target_performance,
            "log_source_timing": self.log_source_timing,
            "log_target_timing": self.log_target_timing,
            "log_source_memory": self.log_source_memory,
            "log_target_memory": self.log_target_memory,
            "log_source_throughput": self.log_source_throughput,
            "log_target_throughput": self.log_target_throughput,
            "track_meltano_performance": self.track_meltano_performance,
            "meltano_performance_threshold_warning": self.meltano_performance_threshold_warning,
            "meltano_performance_threshold_critical": self.meltano_performance_threshold_critical,
            "include_pipeline_info_in_logs": self.include_pipeline_info_in_logs,
            "include_plugin_info_in_logs": self.include_plugin_info_in_logs,
            "include_source_info_in_logs": self.include_source_info_in_logs,
            "include_target_info_in_logs": self.include_target_info_in_logs,
            "include_transform_info_in_logs": self.include_transform_info_in_logs,
            "include_data_quality_info_in_logs": self.include_data_quality_info_in_logs,
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

    def get_metadata(self) -> FlextCore.Types.Dict:
        """Get configuration metadata including override tracking.

        Returns:
            FlextCore.Types.Dict: Configuration metadata dictionary.

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
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Create DBT project configuration.

            Args:
                project_name: Name of the DBT project
                profile_name: Optional profile name override

            Returns:
                FlextCore.Result with DBT configuration dictionary

            """
            try:
                profile = profile_name or f"{project_name}_profile"
                config: FlextCore.Types.Dict = {
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
                return FlextCore.Result[FlextCore.Types.Dict].ok(config)
            except Exception as e:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"Failed to create DBT config: {e}"
                )

        @staticmethod
        def create_dbt_profile_config(
            profile_name: str,
            target_name: str = "dev",
            db_type: str = "postgres",
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Create DBT profile configuration.

            Args:
                profile_name: Name of the DBT profile
                target_name: Name of the target environment
                db_type: Database type (postgres, snowflake, etc.)

            Returns:
                FlextCore.Result with DBT profile configuration dictionary

            """
            try:
                profile_config: FlextCore.Types.Dict = {
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
                return FlextCore.Result[FlextCore.Types.Dict].ok(profile_config)
            except Exception as e:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"Failed to create DBT profile config: {e}"
                )

        @staticmethod
        def create_meltano_config(
            project_id: str,
            default_environment: str = "dev",
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Create basic Meltano project configuration.

            Args:
                project_id: Unique project identifier
                default_environment: Default environment name

            Returns:
                FlextCore.Result with Meltano configuration dictionary

            """
            try:
                config: FlextCore.Types.Dict = {
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
                return FlextCore.Result[FlextCore.Types.Dict].ok(config)
            except Exception as e:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"Failed to create Meltano config: {e}"
                )

        @staticmethod
        def create_development_config() -> FlextCore.Result[FlextMeltanoConfig]:
            """Create configuration optimized for development environment.

            Returns:
                FlextCore.Result with development-optimized FlextMeltanoConfig

            """
            try:
                config = FlextMeltanoConfig()
                # Apply development-specific settings
                config.environment = "development"
                config.debug = True
                config.log_level = "DEBUG"
                config.timeout_seconds = 300
                config.max_concurrent_jobs = 2
                return FlextCore.Result[FlextMeltanoConfig].ok(config)
            except Exception as e:
                return FlextCore.Result[FlextMeltanoConfig].fail(
                    f"Failed to create dev config: {e}"
                )

        @staticmethod
        def create_production_config(
            database_url: str,
        ) -> FlextCore.Result[FlextMeltanoConfig]:
            """Create configuration optimized for production environment.

            Args:
                database_url: Production database URL

            Returns:
                FlextCore.Result with production-optimized FlextMeltanoConfig

            """
            try:
                config = FlextMeltanoConfig()
                # Apply production-specific settings
                config.environment = "production"
                config.debug = False
                config.log_level = "WARNING"
                config.timeout_seconds = 600
                config.max_concurrent_jobs = 10
                config.meltano_database_uri = SecretStr(database_url)
                return FlextCore.Result[FlextMeltanoConfig].ok(config)
            except Exception as e:
                return FlextCore.Result[FlextMeltanoConfig].fail(
                    f"Failed to create prod config: {e}"
                )

        @staticmethod
        def create_testing_config() -> FlextCore.Result[FlextMeltanoConfig]:
            """Create configuration optimized for testing environment.

            Returns:
                FlextCore.Result with testing-optimized FlextMeltanoConfig

            """
            try:
                config = FlextMeltanoConfig()
                # Apply testing-specific settings
                config.environment = "testing"
                config.debug = True
                config.log_level = "DEBUG"
                config.timeout_seconds = 60
                config.max_concurrent_jobs = 1
                return FlextCore.Result[FlextMeltanoConfig].ok(config)
            except Exception as e:
                return FlextCore.Result[FlextMeltanoConfig].fail(
                    f"Failed to create test config: {e}"
                )


__all__ = [
    "FlextMeltanoConfig",
]
