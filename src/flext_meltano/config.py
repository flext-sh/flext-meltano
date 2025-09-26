"""FLEXT Meltano Configuration Management - Enterprise ELT configuration patterns.

This module provides configuration management for Meltano ELT operations
following FLEXT architectural patterns with Pydantic validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

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


class FlextMeltanoLoggingConstants(FlextConstants):
    """Meltano-specific logging constants for FLEXT Meltano module.

    Provides domain-specific logging defaults, levels, and configuration
    options tailored for Meltano operations, data pipeline execution,
    and ETL process monitoring.
    """

    # Meltano-specific log levels
    DEFAULT_LEVEL = FlextConstants.Config.LogLevel.INFO
    PIPELINE_LEVEL = FlextConstants.Config.LogLevel.INFO
    EXTRACT_LEVEL = FlextConstants.Config.LogLevel.INFO
    LOAD_LEVEL = FlextConstants.Config.LogLevel.INFO
    TRANSFORM_LEVEL = FlextConstants.Config.LogLevel.INFO
    ERROR_LEVEL = FlextConstants.Config.LogLevel.ERROR
    PERFORMANCE_LEVEL = FlextConstants.Config.LogLevel.WARNING

    # Pipeline execution logging
    LOG_PIPELINE_START = True
    LOG_PIPELINE_END = True
    LOG_PIPELINE_PROGRESS = True
    LOG_PIPELINE_ERRORS = True
    LOG_PIPELINE_STATS = True
    LOG_PIPELINE_DURATION = True

    # Extract operations logging
    LOG_EXTRACT_START = True
    LOG_EXTRACT_END = True
    LOG_EXTRACT_RECORDS = True
    LOG_EXTRACT_ERRORS = True
    LOG_EXTRACT_DURATION = True
    LOG_EXTRACT_SOURCE_INFO = True

    # Load operations logging
    LOG_LOAD_START = True
    LOG_LOAD_END = True
    LOG_LOAD_RECORDS = True
    LOG_LOAD_ERRORS = True
    LOG_LOAD_DURATION = True
    LOG_LOAD_TARGET_INFO = True

    # Transform operations logging
    LOG_TRANSFORM_START = True
    LOG_TRANSFORM_END = True
    LOG_TRANSFORM_RECORDS = True
    LOG_TRANSFORM_ERRORS = True
    LOG_TRANSFORM_DURATION = True
    LOG_TRANSFORM_SQL = False  # Don't log SQL by default (privacy/security)

    # Performance tracking
    TRACK_MELTANO_PERFORMANCE = True
    MELTANO_PERFORMANCE_THRESHOLD_WARNING = 5000  # 5 seconds default
    MELTANO_PERFORMANCE_THRESHOLD_CRITICAL = 10000  # 10 seconds default
    TRACK_RECORD_COUNTS = True
    TRACK_MEMORY_USAGE = True
    HIGH_MEMORY_THRESHOLD = FlextConstants.Performance.HIGH_MEMORY_THRESHOLD_BYTES

    # Data quality logging
    LOG_DATA_QUALITY_ISSUES = True
    LOG_VALIDATION_ERRORS = True
    LOG_SCHEMA_CHANGES = True
    LOG_DATA_TYPE_CONVERSIONS = True
    LOG_NULL_VALUE_HANDLING = True

    # Error handling and recovery
    LOG_ERROR_RECOVERY = True
    LOG_RETRY_ATTEMPTS = True
    LOG_FALLBACK_OPERATIONS = True
    LOG_PARTIAL_FAILURES = True
    LOG_CRITICAL_FAILURES = True

    # Context information to include
    INCLUDE_PIPELINE_ID = True
    INCLUDE_JOB_ID = True
    INCLUDE_RUN_ID = True
    INCLUDE_SOURCE_NAME = True
    INCLUDE_TARGET_NAME = True
    INCLUDE_TRANSFORM_NAME = True
    INCLUDE_RECORD_COUNT = True
    INCLUDE_DURATION = True

    # Message templates for Meltano operations
    class MeltanoMessages:
        """Meltano-specific log message templates."""

        # Pipeline messages
        PIPELINE_STARTED = "Meltano pipeline started: {pipeline_name} run_id: {run_id}"
        PIPELINE_COMPLETED = "Meltano pipeline completed: {pipeline_name} run_id: {run_id} duration: {duration}ms"
        PIPELINE_FAILED = (
            "Meltano pipeline failed: {pipeline_name} run_id: {run_id} error: {error}"
        )
        PIPELINE_CANCELLED = (
            "Meltano pipeline cancelled: {pipeline_name} run_id: {run_id}"
        )

        # Extract messages
        EXTRACT_STARTED = "Meltano extract started: {source_name} run_id: {run_id}"
        EXTRACT_COMPLETED = "Meltano extract completed: {source_name} {record_count} records in {duration}ms"
        EXTRACT_FAILED = "Meltano extract failed: {source_name} error: {error}"
        EXTRACT_PROGRESS = (
            "Meltano extract progress: {source_name} {current}/{total} records"
        )

        # Load messages
        LOAD_STARTED = "Meltano load started: {target_name} run_id: {run_id}"
        LOAD_COMPLETED = "Meltano load completed: {target_name} {record_count} records in {duration}ms"
        LOAD_FAILED = "Meltano load failed: {target_name} error: {error}"
        LOAD_PROGRESS = "Meltano load progress: {target_name} {current}/{total} records"

        # Transform messages
        TRANSFORM_STARTED = (
            "Meltano transform started: {transform_name} run_id: {run_id}"
        )
        TRANSFORM_COMPLETED = "Meltano transform completed: {transform_name} {record_count} records in {duration}ms"
        TRANSFORM_FAILED = "Meltano transform failed: {transform_name} error: {error}"
        TRANSFORM_PROGRESS = (
            "Meltano transform progress: {transform_name} {current}/{total} records"
        )

        # Performance messages
        SLOW_PIPELINE = "Slow Meltano pipeline: {pipeline_name} took {duration}ms"
        SLOW_EXTRACT = "Slow Meltano extract: {source_name} took {duration}ms"
        SLOW_LOAD = "Slow Meltano load: {target_name} took {duration}ms"
        SLOW_TRANSFORM = "Slow Meltano transform: {transform_name} took {duration}ms"
        HIGH_MEMORY_USAGE = (
            "High memory usage in Meltano pipeline: {pipeline_name} {memory}MB"
        )

        # Data quality messages
        DATA_QUALITY_ISSUE = (
            "Data quality issue: {issue_type} in {source_name}: {details}"
        )
        VALIDATION_ERROR = "Meltano validation error: {field} {error} in {source_name}"
        SCHEMA_CHANGE = "Schema change detected: {source_name} {change_type}: {details}"
        DATA_TYPE_CONVERSION = (
            "Data type conversion: {field} {from_type} -> {to_type} in {source_name}"
        )
        NULL_VALUE_HANDLED = "Null value handled: {field} {strategy} in {source_name}"

        # Error messages
        PIPELINE_ERROR = "Meltano pipeline error: {pipeline_name} {error}"
        EXTRACT_ERROR = "Meltano extract error: {source_name} {error}"
        LOAD_ERROR = "Meltano load error: {target_name} {error}"
        TRANSFORM_ERROR = "Meltano transform error: {transform_name} {error}"
        CONFIGURATION_ERROR = "Meltano configuration error: {error}"

        # Recovery messages
        ERROR_RECOVERY = (
            "Meltano error recovery: {operation} retry {attempt}/{max_attempts}"
        )
        RETRY_ATTEMPT = (
            "Meltano retry attempt: {operation} attempt {attempt}/{max_attempts}"
        )
        FALLBACK_OPERATION = (
            "Meltano fallback operation: {operation} using {fallback_strategy}"
        )
        PARTIAL_FAILURE = (
            "Meltano partial failure: {operation} {failed_count}/{total_count} failed"
        )
        CRITICAL_FAILURE = "Meltano critical failure: {operation} {error}"

        # Statistics messages
        PIPELINE_STATS = "Meltano pipeline statistics: {pipeline_name} records: {total_records} duration: {duration}ms"
        EXTRACT_STATS = "Meltano extract statistics: {source_name} records: {record_count} duration: {duration}ms"
        LOAD_STATS = "Meltano load statistics: {target_name} records: {record_count} duration: {duration}ms"
        TRANSFORM_STATS = "Meltano transform statistics: {transform_name} records: {record_count} duration: {duration}ms"

    # Environment-specific overrides for Meltano logging
    class MeltanoEnvironment:
        """Environment-specific Meltano logging configuration."""

        DEVELOPMENT: ClassVar[FlextTypes.Core.Dict] = {
            "log_transform_sql": "True",  # Log SQL in dev
            "log_source_info": "True",  # Log source info in dev
            "log_target_info": "True",  # Log target info in dev
            "audit_log_level": FlextConstants.Config.LogLevel.DEBUG,
        }

        STAGING: ClassVar[FlextTypes.Core.Dict] = {
            "log_transform_sql": "False",
            "log_source_info": "True",
            "log_target_info": "True",
            "audit_log_level": FlextConstants.Config.LogLevel.INFO,
        }

        PRODUCTION: ClassVar[FlextTypes.Core.Dict] = {
            "log_transform_sql": "False",
            "log_source_info": "False",
            "log_target_info": "False",
            "audit_log_level": FlextConstants.Config.LogLevel.WARNING,
        }

        TESTING: ClassVar[FlextTypes.Core.Dict] = {
            "log_transform_sql": "True",
            "log_source_info": "True",
            "log_target_info": "True",
            "audit_log_level": FlextConstants.Config.LogLevel.DEBUG,
        }

    # Singleton pattern attributes
    _global_instance: ClassVar[FlextMeltanoConfig | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    model_config = SettingsConfigDict(
        env_prefix=FLEXT_MELTANO_,
        case_sensitive=False,
        extra=ignore,
        env_file=".env",
        env_file_encoding="utf-8",
        use_enum_values=True,
        validate_assignment=True,
        validate_default=True,
        frozen=False,
        str_strip_whitespace=True,
    )


import threading


class FlextMeltanoConfig(FlextConfig):
    """Meltano ELT configuration management with enterprise-grade validation.

    Extends FlextConfig to provide comprehensive Meltano-specific configuration
    with validation using flext-core patterns. This class serves as the single
    source of truth for all Meltano configuration across the application.

    """

    # ============================================================================
    # MELTANO-SPECIFIC CONSTANTS - Using FlextMeltanoConstants as SOURCE OF TRUTH
    # ============================================================================

    # Use FlextMeltanoConstants for all version constants (SOURCE OF TRUTH)
    MELTANO_VERSION: ClassVar[str] = FlextMeltanoConstants.MELTANO_VERSION_REQUIRED
    SINGER_SDK_VERSION: ClassVar[str] = (
        FlextMeltanoConstants.SINGER_SDK_VERSION_REQUIRED
    )
    DBT_VERSION: ClassVar[str] = FlextMeltanoConstants.DBT_VERSION_REQUIRED

    # Use FlextMeltanoConstants for file constants (SOURCE OF TRUTH)
    PROJECT_FILE: ClassVar[str] = FlextMeltanoConstants.MELTANO_PROJECT_FILE
    STATE_DIR: ClassVar[str] = FlextMeltanoConstants.MELTANO_STATE_DIR
    VENV_DIR: ClassVar[str] = ".meltano/python"

    # Meltano environment variables (Meltano-specific)
    MELTANO_PROJECT_ROOT_ENV: ClassVar[str] = "MELTANO_PROJECT_ROOT"
    MELTANO_ENVIRONMENT_ENV: ClassVar[str] = "MELTANO_ENVIRONMENT"
    MELTANO_LOG_LEVEL_ENV: ClassVar[str] = "MELTANO_LOG_LEVEL"

    # ============================================================================
    # ENUMS - All enumerated types as class enums
    # ============================================================================

    # ALL ENUMS MUST COME FROM FlextConstants or FlextMeltanoConstants - NO ALIASES
    PluginType: type = FlextMeltanoConstants.PluginTypes  # Domain-specific constants
    EnvironmentType: type = (
        FlextConstants.Environment.ConfigEnvironment
    )  # Core constants
    LogLevel: type = FlextConstants.Config.LogLevel  # Core constants
    OperationStatus: type = (
        FlextMeltanoConstants.OperationStatus
    )  # Domain-specific constants
    RunMode: type = FlextMeltanoConstants.RunMode  # Domain-specific constants

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

    log_level: str = Field(
        default=FlextConstants.Config.LogLevel.INFO,  # SOURCE OF TRUTH
        description="Logging level for operations",
    )

    timeout_seconds: int = Field(
        default=FlextConstants.Network.DEFAULT_TIMEOUT,  # SOURCE OF TRUTH
        ge=1,
        le=3600,
        description="Timeout for operations in seconds",
    )

    # Meltano-specific logging configuration using FlextMeltanoLoggingConstants
    log_pipeline_execution: bool = Field(
        default=True,
        description="Log pipeline execution details",
    )

    log_pipeline_stages: bool = Field(
        default=True,
        description="Log pipeline stage execution",
    )

    log_pipeline_progress: bool = Field(
        default=FlextMeltanoLoggingConstants.LOG_PIPELINE_PROGRESS,
        description="Log pipeline progress updates",
    )

    log_pipeline_errors: bool = Field(
        default=FlextMeltanoLoggingConstants.LOG_PIPELINE_ERRORS,
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
        default=FlextMeltanoLoggingConstants.LOG_EXTRACT_ERRORS,
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
        default=FlextMeltanoLoggingConstants.LOG_LOAD_ERRORS,
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
        default=FlextMeltanoLoggingConstants.LOG_TRANSFORM_SQL,
        description="Log transform SQL queries",
    )

    log_transform_results: bool = Field(
        default=True,
        description="Log transform results",
    )

    log_transform_errors: bool = Field(
        default=FlextMeltanoLoggingConstants.LOG_TRANSFORM_ERRORS,
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
        default=FlextMeltanoLoggingConstants.TRACK_MELTANO_PERFORMANCE,
        description="Track Meltano performance metrics",
    )

    meltano_performance_threshold_warning: float = Field(
        default=True,
        description="Meltano performance warning threshold in milliseconds",
    )

    meltano_performance_threshold_critical: float = Field(
        default=True,
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
        default=INFO,
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
        default=FlextConstants.Performance.DEFAULT_BATCH_SIZE,  # SOURCE OF TRUTH
        ge=1,
        le=10000,
        description="Batch size for data processing",
    )

    # Plugin and execution configuration
    max_concurrent_jobs: int = Field(
        default=FlextConstants.Container.MAX_WORKERS,  # SOURCE OF TRUTH
        ge=1,
        le=16,
        description="Maximum number of concurrent jobs",
    )

    run_mode: str = Field(
        default=FULL,
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

        """
        try:
            config = cls(project_root=Path(project_root))
            validation_result = config.validate_project_structure()

            if validation_result.is_failure:
                return FlextResult[FlextMeltanoConfig].fail(
                    validation_result.error or "Project validation failed",
                )

            return FlextResult[FlextMeltanoConfig].ok(config)

        except Exception as e:  # pragma: no cover
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
        # Validate environment using FlextConstants
        try:
            env_type = FlextConstants.Environment.ConfigEnvironment(environment)
        except ValueError as e:
            msg = f"Invalid environment: {environment}"
            raise ValueError(msg) from e

        # Filter and type-cast kwargs to valid fields only
        valid_fields = cls.model_fields.keys()
        filtered_kwargs: FlextTypes.Core.Dict = {
            k: v for k, v in kwargs.items() if k in valid_fields
        }

        # Create config data with environment
        config_data: FlextTypes.Core.Dict = {"environment": env_type.value}

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
            config_data["log_level"] = FlextConstants.Config.LogLevel(
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

        """
        # Always get fresh base configuration from FlextConfig singleton
        base_config = FlextConfig.get_global_instance()

        # Convert base config to dict for processing
        base_data: FlextTypes.Core.Dict = base_config.model_dump()

        # Apply overrides with highest priority
        base_data.update(overrides)

        # Handle debug/environment conflict: production cannot have debug=True
        if (
            base_data.get("environment") == "production"
            and base_data.get("debug") is True
        ):
            base_data["debug"] = False

        # Create Meltano config instance with all data
        return cls(**base_data)

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
            raise TypeError(error_msg)

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
        return FlextConstants.Performance.DEFAULT_BATCH_SIZE

    @classmethod
    def get_supported_plugin_types(cls) -> list[str]:
        """Get list of supported plugin types."""
        return [
            FlextMeltanoConstants.PluginTypes.EXTRACTORS.value,
            FlextMeltanoConstants.PluginTypes.LOADERS.value,
            FlextMeltanoConstants.PluginTypes.TRANSFORMS.value,
            FlextMeltanoConstants.PluginTypes.ORCHESTRATORS.value,
        ]

    @classmethod
    def get_supported_environments(cls) -> list[str]:
        """Get list of supported environments."""
        return ["development", "staging", "production"]

    @classmethod
    def get_supported_log_levels(cls) -> list[str]:
        """Get list of supported log levels."""
        return [
            FlextConstants.Config.LogLevel.DEBUG.value,
            FlextConstants.Config.LogLevel.INFO.value,
            FlextConstants.Config.LogLevel.WARNING.value,
            FlextConstants.Config.LogLevel.ERROR.value,
        ]

    @classmethod
    def clear_global_instance(cls) -> None:
        """Clear the global instance (useful for testing).

        Removes the current global configuration instance, allowing for
        fresh configuration in test scenarios.

        """
        # Clear the instance if it exists
        if hasattr(cls, "_global_instance"):
            cls._global_instance = None

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

    def get_meltano_logging_config(self) -> FlextTypes.Core.Dict:
        """Get Meltano-specific logging configuration dictionary.

        Returns:
            FlextTypes.Core.Dict: Dictionary containing Meltano logging configuration.

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

    def get_metadata(self) -> dict[str, object]:
        """Get configuration metadata including override tracking.

        Returns:
            FlextTypes.Core.Dict: Configuration metadata dictionary.

        """
        # Get base metadata from FlextConfig
        base_metadata = super().get_metadata()

        # Add extra metadata if it exists
        if hasattr(self, "_metadata_extra"):
            base_metadata.update(self._metadata_extra)

        return base_metadata

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        {
            "extra": "ignore",  # Allow extra fields from environment variables
            "validate_assignment": "True",
            "use_enum_values": "True",
            "arbitrary_types_allowed": "True",
        },
    )


__all__ = [
    "FlextMeltanoConfig",
]
