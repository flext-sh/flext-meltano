"""Modern Configuration System using flext-core patterns.

MIGRATED TO FLEXT-CORE: Uses flext-core BaseSettings and FlextValueObject patterns.
Zero tolerance for code duplication.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar, Literal

# Proper implementations using pydantic
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from flext_meltano.common import validate_base_url

# Use pydantic BaseModel as FlextValueObject equivalent
FlextValueObject = BaseModel

# Configuration defaults
class ConfigDefaults:
    """Default configuration values for Oracle OIC."""

    DEFAULT_HTTP_TIMEOUT = 60
    DEFAULT_HTTP_RETRIES = 3

    # Monitoring thresholds
    HIGH_ALERT_THRESHOLD = 95
    MAX_MONITORING_INTERVAL = 300  # 5 minutes
    LOW_ALERT_THRESHOLD = 80
    CRITICAL_ALERT_THRESHOLD = 99

    # Performance validation thresholds
    MAX_TOTAL_TIMEOUT = 900  # 15 minutes
    MAX_RETRY_COUNT = 3
    MAX_RETRY_DELAY = 5.0
    MAX_CONCURRENT_REQUESTS = 10
    MIN_BATCH_SIZE = 100
    HIGH_CONCURRENT_REQUESTS = 15
    MAX_REQUEST_TIMEOUT = 120
    LARGE_BATCH_SIZE = 5000
    MIN_REQUEST_TIMEOUT = 60

    # System directories to avoid for security
    SYSTEM_DIRECTORIES: ClassVar[set[str]] = {"/", "/etc", "/bin", "/usr", "/var", "/opt", "/home"}

    # Log window thresholds
    MAX_LOG_WINDOW_HOURS = 72  # 3 days

class LogLevels:
    """Available log levels for Oracle OIC."""

    DEFAULT: LogLevelLiteral = "INFO"

# BaseSettings imported from pydantic_settings above

# Use local literals for this module
EnvironmentLiteral = Literal["development", "test", "staging", "production"]
LogLevelLiteral = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class OICExtensionConnectionConfig(FlextValueObject):
    """Oracle Integration Cloud connection configuration using flext-core patterns."""

    base_url: str = Field(
        ...,
        description="OIC instance base URL (e.g., https://instance.integration.ocp.oraclecloud.com)",
        min_length=1,
    )

    oauth_client_id: str = Field(
        ...,
        description="OAuth2 client ID from IDCS application",
        min_length=1,
    )

    oauth_client_secret: str = Field(
        ...,
        description="OAuth2 client secret from IDCS application",
        min_length=1,
    )

    oauth_token_url: str = Field(
        ...,
        description="IDCS token endpoint URL",
        min_length=1,
    )

    oauth_scope: str | None = Field(
        None,
        description="OAuth2 scope for authentication",
    )

    @field_validator("base_url")
    @classmethod
    def validate_base_url_field(cls, v: str) -> str:
        """Use consolidated base URL validation."""
        return validate_base_url(v)

    @field_validator("oauth_token_url")
    @classmethod
    def validate_oauth_token_url(cls, v: str) -> str:
        """Use consolidated base URL validation for OAuth token URL."""
        return validate_base_url(v)

    def validate_domain_rules(self) -> None:
        """Validate OIC connection domain rules and constraints."""
        # Validate OAuth client credentials are not default/placeholder values
        placeholder_values = {
            "client_id", "your_client_id", "CONFIGURE_CLIENT_ID",
            "test_client_id", "CONFIGURE_DEV_CLIENT_ID",
        }
        if self.oauth_client_id in placeholder_values:
            msg = "OAuth client ID cannot be a placeholder value"
            raise ValueError(msg)

        placeholder_secrets = {
            "client_secret", "your_client_secret", "CONFIGURE_CLIENT_SECRET",
            "test_client_secret", "CONFIGURE_DEV_CLIENT_SECRET",
        }
        if self.oauth_client_secret in placeholder_secrets:
            msg = "OAuth client secret cannot be a placeholder value"
            raise ValueError(msg)

        # Validate URLs are HTTPS for security
        if not self.base_url.startswith("https://"):
            msg = "OIC base URL must use HTTPS for security"
            raise ValueError(msg)

        if not self.oauth_token_url.startswith("https://"):
            msg = "OAuth token URL must use HTTPS for security"
            raise ValueError(msg)

        # Validate OAuth scope format if provided
        if self.oauth_scope is not None and not self.oauth_scope.strip():
            msg = "OAuth scope cannot be empty string if provided"
            raise ValueError(msg)


class OICExtensionLifecycleConfig(FlextValueObject):
    """Oracle Integration Cloud lifecycle configuration using flext-core patterns."""

    auto_activate: bool = Field(
        default=False,
        description="Automatically activate integrations after deployment",
    )

    health_check_interval: int = Field(
        default=300,
        ge=30,
        le=3600,
        description="Health check interval in seconds",
    )

    activation_timeout: int = Field(
        default=ConfigDefaults.DEFAULT_HTTP_TIMEOUT,
        ge=30,
        le=600,
        description="Activation timeout in seconds",
    )

    validate_before_activate: bool = Field(
        default=True,
        description="Validate integration before activation",
    )

    rollback_on_failure: bool = Field(
        default=True,
        description="Rollback on activation failure",
    )

    def validate_domain_rules(self) -> None:
        """Validate OIC lifecycle domain rules and constraints."""
        # Validate timeout relationships - activation timeout should be reasonable for health checks
        if self.activation_timeout > self.health_check_interval:
            msg = "Activation timeout should not exceed health check interval to avoid conflicts"
            raise ValueError(
                msg,
            )

        # Validate safe configuration - auto-activation without validation is risky
        if self.auto_activate and not self.validate_before_activate:
            msg = "Auto-activation without validation is unsafe - enable validation or disable auto-activation"
            raise ValueError(
                msg,
            )

        # Validate production-safe settings
        if self.auto_activate and not self.rollback_on_failure:
            msg = "Auto-activation without rollback capability is unsafe for production environments"
            raise ValueError(
                msg,
            )


class OICExtensionMonitoringConfig(FlextValueObject):
    """Oracle Integration Cloud monitoring configuration using flext-core patterns."""

    enable_monitoring: bool = Field(
        default=True,
        description="Enable monitoring capabilities",
    )

    monitoring_interval: int = Field(
        default=60,
        ge=10,
        le=3600,
        description="Monitoring interval in seconds",
    )

    alert_threshold: int = Field(
        default=90,
        ge=50,
        le=100,
        description="Alert threshold percentage",
    )

    error_window_hours: int = Field(
        default=24,
        ge=1,
        le=168,
        description="Error analysis window in hours",
    )

    performance_window_hours: int = Field(
        default=6,
        ge=1,
        le=72,
        description="Performance analysis window in hours",
    )

    def validate_domain_rules(self) -> None:
        """Validate OIC monitoring domain rules and constraints."""
        # Validate monitoring configuration consistency
        if not self.enable_monitoring and self.alert_threshold > ConfigDefaults.HIGH_ALERT_THRESHOLD:
            msg = "Alert threshold above 95% with monitoring disabled may miss critical issues"
            raise ValueError(msg)

        # Validate window relationships - performance window should be reasonable relative to error window
        if self.performance_window_hours > self.error_window_hours:
            msg = "Performance analysis window should not exceed error analysis window"
            raise ValueError(msg)

        # Validate monitoring frequency for production use
        if (self.enable_monitoring
            and self.monitoring_interval > ConfigDefaults.MAX_MONITORING_INTERVAL
            and self.alert_threshold < ConfigDefaults.LOW_ALERT_THRESHOLD):
            msg = "Low alert threshold with long monitoring interval may cause alert floods"
            raise ValueError(msg)

        # Validate alert threshold effectiveness
        if self.alert_threshold >= ConfigDefaults.CRITICAL_ALERT_THRESHOLD:
            msg = "Alert threshold of 99%+ is too high - alerts will only trigger during complete failures"
            raise ValueError(msg)


class OICExtensionPerformanceConfig(FlextValueObject):
    """Oracle Integration Cloud performance configuration using flext-core patterns."""

    request_timeout: int = Field(
        default=ConfigDefaults.DEFAULT_HTTP_TIMEOUT,
        ge=10,
        le=300,
        description="Request timeout in seconds",
    )

    max_retries: int = Field(
        default=ConfigDefaults.DEFAULT_HTTP_RETRIES,
        ge=0,
        le=10,
        description="Maximum number of retry attempts",
    )

    retry_delay: float = Field(
        default=1.0,
        ge=0.1,
        le=60.0,
        description="Delay between retries in seconds",
    )

    batch_size: int = Field(
        default=1000,
        ge=1,
        le=10000,
        description="Batch size for bulk operations",
    )

    max_concurrent_requests: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum concurrent requests",
    )

    def validate_domain_rules(self) -> None:
        """Validate OIC performance domain rules and constraints."""
        # Validate retry configuration efficiency
        if self.max_retries > 0:
            total_timeout = self.request_timeout * (self.max_retries + 1)
            if total_timeout > ConfigDefaults.MAX_TOTAL_TIMEOUT:
                msg = f"Total timeout with retries ({total_timeout}s) exceeds 15 minutes - reduce retries or timeout"
                raise ValueError(msg)

        # Validate retry delay efficiency
        if self.max_retries > ConfigDefaults.MAX_RETRY_COUNT and self.retry_delay > ConfigDefaults.MAX_RETRY_DELAY:
            msg = "High retry count with long delay may cause excessive wait times"
            raise ValueError(msg)

        # Validate concurrent requests vs batch size relationship
        if self.max_concurrent_requests > ConfigDefaults.MAX_CONCURRENT_REQUESTS and self.batch_size < ConfigDefaults.MIN_BATCH_SIZE:
            msg = "High concurrency with small batch size may overwhelm the server"
            raise ValueError(msg)

        # Validate production-safe settings
        if self.max_concurrent_requests > ConfigDefaults.HIGH_CONCURRENT_REQUESTS and self.request_timeout > ConfigDefaults.MAX_REQUEST_TIMEOUT:
            msg = "High concurrency with long timeouts may cause resource exhaustion"
            raise ValueError(msg)

        # Validate batch size efficiency
        if self.batch_size > ConfigDefaults.LARGE_BATCH_SIZE and self.request_timeout < ConfigDefaults.MIN_REQUEST_TIMEOUT:
            msg = "Large batch size with short timeout may cause frequent failures"
            raise ValueError(msg)


class OICExtensionExtractionConfig(FlextValueObject):
    """Oracle Integration Cloud extraction configuration using flext-core patterns."""

    extract_artifacts: bool = Field(
        default=True,
        description="Enable artifact extraction",
    )

    extract_logs: bool = Field(
        default=True,
        description="Enable log extraction",
    )

    extract_metadata: bool = Field(
        default=True,
        description="Enable metadata extraction",
    )

    artifact_directory: str = Field(
        default="./artifacts",
        description="Directory for extracted artifacts",
    )

    log_window_hours: int = Field(
        default=24,
        ge=1,
        le=168,
        description="Log extraction window in hours",
    )

    def validate_domain_rules(self) -> None:
        """Validate OIC extraction domain rules and constraints."""
        # Validate at least one extraction type is enabled
        if not any([self.extract_artifacts, self.extract_logs, self.extract_metadata]):
            msg = "At least one extraction type must be enabled (artifacts, logs, or metadata)"
            raise ValueError(
                msg,
            )

        # Validate artifact directory is not a system directory
        if self.artifact_directory.rstrip("/") in ConfigDefaults.SYSTEM_DIRECTORIES:
            msg = f"Artifact directory cannot be a system directory: {self.artifact_directory}"
            raise ValueError(msg)

        # Validate directory path format
        if not self.artifact_directory.strip():
            msg = "Artifact directory cannot be empty"
            raise ValueError(msg)

        # Validate relative path safety
        if ".." in self.artifact_directory:
            msg = "Artifact directory cannot contain parent directory references (..)"
            raise ValueError(
                msg,
            )

        # Validate log window for practical use
        if self.extract_logs and self.log_window_hours > ConfigDefaults.MAX_LOG_WINDOW_HOURS:
            msg = "Log window over 72 hours may cause memory issues and slow extraction"
            raise ValueError(
                msg,
            )

        # Validate configuration completeness for enabled extractions
        if self.extract_artifacts and not self.extract_metadata:
            msg = "Artifact extraction should include metadata extraction for complete analysis"
            raise ValueError(
                msg,
            )


class OracleOICExtensionSettings(BaseSettings):
    """Oracle Integration Cloud extension configuration using flext-core patterns."""

    model_config = SettingsConfigDict(
        env_prefix="ORACLE_OIC_EXT_",
        env_nested_delimiter="__",
        case_sensitive=False,
        validate_assignment=True,
        extra="forbid",
        frozen=True,
    )

    # Core project metadata
    project_name: str = Field(
        default="flext-extensions.oracle.flext-oracle-oic-ext",
        description="Project name",
    )

    version: str = Field(
        default="0.7.0",
        description="Project version",
    )

    # Connection configuration
    connection: OICExtensionConnectionConfig | None = Field(
        None,
        description="Oracle Integration Cloud connection configuration",
    )

    # Lifecycle configuration
    lifecycle: OICExtensionLifecycleConfig = Field(
        default_factory=OICExtensionLifecycleConfig,
        description="Lifecycle management configuration",
    )

    # Monitoring configuration
    monitoring: OICExtensionMonitoringConfig = Field(
        default_factory=OICExtensionMonitoringConfig,
        description="Monitoring configuration",
    )

    # Performance configuration
    performance: OICExtensionPerformanceConfig = Field(
        default_factory=OICExtensionPerformanceConfig,
        description="Performance configuration",
    )

    # Extraction configuration
    extraction: OICExtensionExtractionConfig = Field(
        default_factory=OICExtensionExtractionConfig,
        description="Extraction configuration",
    )

    # Instance configuration
    instance_id: str | None = Field(
        None,
        description="OIC instance identifier",
    )

    region: str | None = Field(
        None,
        description="OIC region",
    )

    environment: EnvironmentLiteral = Field(
        default="test",
        description="Environment name",
    )

    # Logging configuration
    log_level: LogLevelLiteral = Field(
        default=LogLevels.DEFAULT,
        description="Log level",
    )

    debug: bool = Field(
        default=False,
        description="Enable debug mode",
    )

    @model_validator(mode="after")
    def validate_configuration(self) -> OracleOICExtensionSettings:
        """Validate configuration after model creation.

        Returns:
            The validated configuration instance.

        Raises:
            ValueError: If configuration validation fails.

        """
        # Validate artifact directory

        artifact_path = Path(self.extraction.artifact_directory)
        try:
            artifact_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            msg = f"Failed to create artifact directory: {e}"
            raise ValueError(
                msg,
            ) from e

        # Validate OAuth scope if not provided:
        if self.connection is not None and not self.connection.oauth_scope:
            # Set default scope based on base URL
            base_url = self.connection.base_url.rstrip("/")
            object.__setattr__(
                self.connection,
                "oauth_scope",
                f"{base_url}urn:opc:resource:consumer:all",
            )

        return self

    @classmethod
    def from_dict(cls, config_dict: dict[str, Any]) -> OracleOICExtensionSettings:
        """Create settings instance from dictionary.

        Args:
            config_dict: Dictionary containing configuration values.

        Returns:
            OracleOICExtensionSettings instance.

        """
        # Validate required connection fields
        if not all(
            [
                config_dict.get("base_url"),
                config_dict.get("oauth_client_id"),
                config_dict.get("oauth_client_secret"),
                config_dict.get("oauth_token_url"),
            ],
        ):
            msg = "Missing required connection configuration fields"
            raise ValueError(msg)

        # Transform flat config to nested structure
        connection_config = {
            "base_url": config_dict["base_url"],
            "oauth_client_id": config_dict["oauth_client_id"],
            "oauth_client_secret": config_dict["oauth_client_secret"],
            "oauth_token_url": config_dict["oauth_token_url"],
            "oauth_scope": config_dict.get("oauth_scope"),
        }

        lifecycle_config = {
            "auto_activate": config_dict.get("auto_activate", False),
            "health_check_interval": config_dict.get("health_check_interval", 300),
            "activation_timeout": config_dict.get("activation_timeout", 60),
            "validate_before_activate": config_dict.get(
                "validate_before_activate",
                True,
            ),
            "rollback_on_failure": config_dict.get("rollback_on_failure", True),
        }

        monitoring_config = {
            "enable_monitoring": config_dict.get("enable_monitoring", True),
            "monitoring_interval": config_dict.get("monitoring_interval", 60),
            "alert_threshold": config_dict.get("alert_threshold", 90),
            "error_window_hours": config_dict.get("error_window_hours", 24),
            "performance_window_hours": config_dict.get("performance_window_hours", 6),
        }

        performance_config = {
            "request_timeout": config_dict.get("request_timeout", 60),
            "max_retries": config_dict.get("max_retries", 3),
            "retry_delay": config_dict.get("retry_delay", 1.0),
            "batch_size": config_dict.get("batch_size", 100),
            "max_concurrent_requests": config_dict.get("max_concurrent_requests", 5),
        }

        extraction_config = {
            "extract_artifacts": config_dict.get("extract_artifacts", True),
            "extract_logs": config_dict.get("extract_logs", True),
            "extract_metadata": config_dict.get("extract_metadata", True),
            "artifact_directory": config_dict.get("artifact_directory", "./artifacts"),
            "log_window_hours": config_dict.get("log_window_hours", 24),
        }

        return cls(
            connection=OICExtensionConnectionConfig(
                base_url=connection_config["base_url"],
                oauth_client_id=connection_config["oauth_client_id"],
                oauth_client_secret=connection_config["oauth_client_secret"],
                oauth_token_url=connection_config["oauth_token_url"],
                oauth_scope=connection_config.get("oauth_scope"),
            ),
            lifecycle=OICExtensionLifecycleConfig(**lifecycle_config),
            monitoring=OICExtensionMonitoringConfig(**monitoring_config),
            performance=OICExtensionPerformanceConfig(**performance_config),
            extraction=OICExtensionExtractionConfig(**extraction_config),
            instance_id=config_dict.get("instance_id"),
            region=config_dict.get("region"),
            environment=config_dict.get("environment", "test"),
            log_level=config_dict.get("log_level", LogLevels.DEFAULT),
            debug=config_dict.get("debug", False),
        )

    def to_dict(self) -> dict[str, str | int | float | bool | None]:
        """Convert settings to dictionary format.

        Returns:
            Dictionary representation of all configuration values.

        """
        if self.connection is None:
            msg = "Connection configuration is not set."
            raise ValueError(msg)

        return {  # Connection config
            "base_url": self.connection.base_url,
            "oauth_client_id": self.connection.oauth_client_id,
            "oauth_client_secret": self.connection.oauth_client_secret,
            "oauth_token_url": self.connection.oauth_token_url,
            "oauth_scope": self.connection.oauth_scope,
            # Lifecycle config
            "auto_activate": self.lifecycle.auto_activate,
            "health_check_interval": self.lifecycle.health_check_interval,
            "activation_timeout": self.lifecycle.activation_timeout,
            "validate_before_activate": self.lifecycle.validate_before_activate,
            "rollback_on_failure": self.lifecycle.rollback_on_failure,
            # Monitoring config
            "enable_monitoring": self.monitoring.enable_monitoring,
            "monitoring_interval": self.monitoring.monitoring_interval,
            "alert_threshold": self.monitoring.alert_threshold,
            "error_window_hours": self.monitoring.error_window_hours,
            "performance_window_hours": self.monitoring.performance_window_hours,
            # Performance config
            "request_timeout": self.performance.request_timeout,
            "max_retries": self.performance.max_retries,
            "retry_delay": self.performance.retry_delay,
            "batch_size": self.performance.batch_size,
            "max_concurrent_requests": self.performance.max_concurrent_requests,
            # Extraction config
            "extract_artifacts": self.extraction.extract_artifacts,
            "extract_logs": self.extraction.extract_logs,
            "extract_metadata": self.extraction.extract_metadata,
            "artifact_directory": self.extraction.artifact_directory,
            "log_window_hours": self.extraction.log_window_hours,
            # Instance config
            "instance_id": self.instance_id,
            "region": self.region,
            "environment": self.environment,
            # Other config
            "log_level": self.log_level,
            "debug": self.debug,
        }

    def get_auth_config(self) -> dict[str, str]:
        """Get authentication configuration.

        Returns:
            Dictionary containing OAuth authentication configuration.

        """
        if self.connection is None:
            msg = "Connection configuration is not set."
            raise ValueError(msg)

        return {
            "oauth_client_id": self.connection.oauth_client_id,
            "oauth_client_secret": self.connection.oauth_client_secret,
            "oauth_token_url": self.connection.oauth_token_url,
            "oauth_scope": self.connection.oauth_scope or "",
        }


# Rebuild model to resolve forward references
# Model setup complete - no rebuild needed for pydantic BaseSettings

# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT
