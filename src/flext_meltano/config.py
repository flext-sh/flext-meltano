"""FLEXT Meltano Configuration - Modern Python 3.13 with unified patterns.

REFACTORED:
    Uses flext-core unified configuration mixins with structured value objects.
Zero tolerance for duplication.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
from flext_meltano.infrastructure.di_container import (
    get_config_defaults,
    get_di_container,
    get_domain_entity,
)

# Initialize types via DI container
ConfigDefaults = get_config_defaults()
DomainValueObject = get_domain_entity()  # DomainEntity can be used as value object


# Define local base config mixins to avoid flext-core dependency
class FlextMeltanoBaseConfigMixin:
    """Local base config mixin."""


class FlextMeltanoDatabaseConfigMixin:
    """Local database config mixin."""


class FlextMeltanoLoggingConfigMixin:
    """Local logging config mixin."""


class FlextMeltanoMonitoringConfigMixin:
    """Local monitoring config mixin."""


class FlextMeltanoPerformanceConfigMixin:
    """Local performance config mixin."""


def get_container() -> Any:
    """Local container function."""
    return get_di_container()


class FlextMeltanoProjectConfig(DomainValueObject):
    """Meltano project configuration value object."""

    project_root: Path = Field(
        default_factory=lambda: Path.cwd() / "meltano_projects",
        description="Root directory for Meltano projects",
    )
    default_environment: str = Field(
        default="production",
        description="Default Meltano environment",
    )
    database_uri: str = Field(
        default="sqlite:///meltano.db",
        description="Meltano database URI",
    )
    python_version: str = Field(
        default="3.13",
        description="Python version for Meltano projects",
    )


class FlextMeltanoExecutionConfig(DomainValueObject):
    """Meltano execution configuration value object."""

    max_concurrent_jobs: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Maximum concurrent job executions",
    )
    job_timeout: int = Field(
        default=3600,
        ge=60,
        le=86400,
        description="Job execution timeout in seconds",
    )
    retry_attempts: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Number of retry attempts for failed jobs",
    )
    retry_delay: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Delay between retry attempts in seconds",
    )


class FlextMeltanoStateConfig(DomainValueObject):
    """Meltano state management configuration value object."""

    state_backend: str = Field(
        default="systemdb",
        description="State backend type (systemdb, filesystem, s3)",
    )
    backup_enabled: bool = Field(
        default=True,
        description="Enable automatic state backups",
    )
    backup_interval: int = Field(
        default=3600,
        ge=300,
        le=86400,
        description="State backup interval in seconds",
    )
    max_backups: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of state backups to keep",
    )


class FlextMeltanoBusinessConfig(DomainValueObject):
    """Meltano business logic configuration value object."""

    MINIMUM_MELTANO_COMMAND_COUNT: int = Field(
        default=2,
        ge=1,
        le=10,
        description="Minimum number of commands required for Meltano run blocks",
    )


class FlextMeltanoPluginConfig(DomainValueObject):
    """Meltano plugin configuration value object."""

    auto_install: bool = Field(
        default=True,
        description="Automatically install missing plugins",
    )
    plugin_cache_ttl: int = Field(
        default=86400,
        ge=300,
        le=604800,
        description="Plugin cache TTL in seconds",
    )
    discovery_url: str = Field(
        default="https://hub.meltano.com/meltano/discovery.yml",
        description="Meltano Hub discovery URL",
    )
    default_variant: str = Field(
        default="original",
        description="Default plugin variant to use",
    )


class FlextMeltanoMonitoringConfig(DomainValueObject):
    """Meltano monitoring configuration value object."""

    metrics_enabled: bool = Field(
        default=True,
        description="Enable metrics collection",
    )
    health_check_interval: int = Field(
        default=60,
        ge=10,
        le=3600,
        description="Health check interval in seconds",
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level for Meltano operations",
    )
    event_publishing: bool = Field(
        default=True,
        description="Enable event publishing to FLEXT event bus",
    )


class FlextMeltanoSettings(
    FlextMeltanoBaseConfigMixin,
    FlextMeltanoLoggingConfigMixin,
    FlextMeltanoMonitoringConfigMixin,
    FlextMeltanoPerformanceConfigMixin,
    FlextMeltanoDatabaseConfigMixin,
    BaseSettings,
):
    """FLEXT Meltano configuration settings using unified configuration mixins.

    All settings can be overridden via environment variables with the
    prefix FLEXT_MELTANO_ (e.g., FLEXT_MELTANO_PROJECT__PROJECT_ROOT).

    Uses flext-core unified configuration mixins with DI support.
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_MELTANO_",
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="allow",
        validate_assignment=True,
        str_strip_whitespace=True,
        use_enum_values=True,
    )

    # Project identification (inherits from BaseConfigMixin but override with
    # Meltano-specific values)
    project_name: str = Field(
        default="flext-infrastructure.plugins.flext-meltano",
        max_length=ConfigDefaults.MAX_ENTITY_NAME_LENGTH,
        description="Project name",
    )
    project_version: str = Field(default="0.7.0", description="Project version")

    # Configuration value objects
    project: FlextMeltanoProjectConfig = Field(
        default_factory=FlextMeltanoProjectConfig,
        description="Project configuration",
    )
    execution: FlextMeltanoExecutionConfig = Field(
        default_factory=FlextMeltanoExecutionConfig,
        description="Execution configuration",
    )
    state: FlextMeltanoStateConfig = Field(
        default_factory=FlextMeltanoStateConfig,
        description="State configuration",
    )
    plugins: FlextMeltanoPluginConfig = Field(
        default_factory=FlextMeltanoPluginConfig,
        description="Plugin configuration",
    )
    business: FlextMeltanoBusinessConfig = Field(
        default_factory=FlextMeltanoBusinessConfig,
        description="Business logic configuration",
    )
    # Note: monitoring inherited from MonitoringConfigMixin
    # Additional Meltano-specific monitoring configuration
    meltano_monitoring: FlextMeltanoMonitoringConfig = Field(
        default_factory=FlextMeltanoMonitoringConfig,
        description="Meltano-specific monitoring configuration",
    )

    # Environment and debug settings
    environment: str = Field(
        default="development",
        description="Current environment (development, testing, staging, production)",
    )
    debug: bool = Field(default=False, description="Enable debug mode")

    # Legacy properties for backward compatibility
    @property
    def project_root(self) -> Path:
        """Get the Meltano project root directory.

        Returns:
            Path to the project root directory.

        """
        return self.project.project_root

    @property
    def default_environment(self) -> str:
        """Get the default Meltano environment name.

        Returns:
            Default environment name.

        """
        return self.project.default_environment

    @property
    def database_uri(self) -> str:
        """Get the Meltano database URI.

        Returns:
            Database connection URI.

        """
        return self.project.database_uri

    @property
    def max_concurrent_jobs(self) -> int:
        """Get maximum number of concurrent jobs.

        Returns:
            Maximum concurrent job limit.

        """
        return self.execution.max_concurrent_jobs

    @property
    def job_timeout(self) -> int:
        """Get job execution timeout in seconds.

        Returns:
            Job timeout in seconds.

        """
        return self.execution.job_timeout

    @property
    def state_backend(self) -> str:
        """Get the Meltano state backend type.

        Returns:
            State backend identifier.

        """
        return self.state.state_backend

    @property
    def backup_enabled(self) -> bool:
        """Check if state backup is enabled.

        Returns:
            True if backup is enabled, False otherwise.

        """
        return self.state.backup_enabled

    @property
    def auto_install(self) -> bool:
        """Check if automatic plugin installation is enabled.

        Returns:
            True if auto-install is enabled, False otherwise.

        """
        return self.plugins.auto_install

    def configure_dependencies(self, container: Any | None = None) -> None:
        """Configure dependency injection container.

        Args:
            container: Optional dependency injection container.

        """
        if container is None:
            container = get_container()
        # Register this settings instance
        container.register(FlextMeltanoSettings, self)

        # Configure any other dependencies if needed
        # Note: mixins don't provide configure_dependencies method


# Convenience functions for getting settings
def flext_get_meltano_settings() -> FlextMeltanoSettings:
    return FlextMeltanoSettings(
        project_name="flext-infrastructure.plugins.flext-meltano",
        project_version="0.7.0",
        environment="development",
        debug=False,
    )


def flext_create_development_meltano_config() -> FlextMeltanoSettings:
    return FlextMeltanoSettings(
        project_name="flext-infrastructure.plugins.flext-meltano",
        project_version="0.7.0",
        environment="development",
        debug=True,
        project=FlextMeltanoProjectConfig(
            default_environment="dev",
            database_uri="sqlite:///dev_meltano.db",
        ),
        execution=FlextMeltanoExecutionConfig(
            max_concurrent_jobs=2,
            job_timeout=1800,  # 30 minutes for development
            retry_attempts=1,
        ),
    )


def flext_create_production_meltano_config() -> FlextMeltanoSettings:
    return FlextMeltanoSettings(
        project_name="flext-infrastructure.plugins.flext-meltano",
        project_version="0.7.0",
        environment="production",
        debug=False,
        project=FlextMeltanoProjectConfig(
            default_environment="prod",
            database_uri="postgresql://user:pass@localhost/meltano",
        ),
        execution=FlextMeltanoExecutionConfig(),
    )


__all__ = [
    "FlextMeltanoBusinessConfig",
    "FlextMeltanoExecutionConfig",
    "FlextMeltanoMonitoringConfig",
    "FlextMeltanoPluginConfig",
    "FlextMeltanoProjectConfig",
    "FlextMeltanoSettings",
    "FlextMeltanoStateConfig",
    "get_settings",
]


def get_settings() -> FlextMeltanoSettings:
    """Get global settings instance."""
    return FlextMeltanoSettings()
