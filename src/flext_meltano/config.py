"""FLEXT Meltano Configuration - Modern Python 3.13 patterns.

REFACTORED:
    Uses flext-core BaseSettings with structured value objects.
Zero tolerance for duplication.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flext_core.config import BaseSettings
from flext_core.config import get_container
from flext_core.config import singleton
from flext_core.domain.pydantic_base import DomainValueObject
from flext_core.domain.pydantic_base import Field


class MeltanoProjectConfig(DomainValueObject):
    """Meltano project configuration value object."""

    project_root: Path = Field(
        default_factory=lambda: Path.cwd() / "meltano_projects",
        description="Root directory for Meltano projects",
    )
    default_environment: str = Field(
        "production",
        description="Default Meltano environment",
    )
    database_uri: str = Field(
        "sqlite:///meltano.db",
        description="Meltano database URI",
    )
    python_version: str = Field(
        "3.13",
        description="Python version for Meltano projects",
    )


class MeltanoExecutionConfig(DomainValueObject):
    """Meltano execution configuration value object."""

    max_concurrent_jobs: int = Field(
        5,
        ge=1,
        le=50,
        description="Maximum concurrent job executions",
    )
    job_timeout: int = Field(
        3600,
        ge=60,
        le=86400,
        description="Job execution timeout in seconds",
    )
    retry_attempts: int = Field(
        3,
        ge=0,
        le=10,
        description="Number of retry attempts for failed jobs",
    )
    retry_delay: int = Field(
        30,
        ge=1,
        le=300,
        description="Delay between retry attempts in seconds",
    )


class MeltanoStateConfig(DomainValueObject):
    """Meltano state management configuration value object."""

    state_backend: str = Field(
        "systemdb",
        description="State backend type (systemdb, filesystem, s3)",
    )
    backup_enabled: bool = Field(
        True,
        description="Enable automatic state backups",
    )
    backup_interval: int = Field(
        3600,
        ge=300,
        le=86400,
        description="State backup interval in seconds",
    )
    max_backups: int = Field(
        10,
        ge=1,
        le=100,
        description="Maximum number of state backups to keep",
    )


class MeltanoPluginConfig(DomainValueObject):
    """Meltano plugin configuration value object."""

    auto_install: bool = Field(
        True,
        description="Automatically install missing plugins",
    )
    plugin_cache_ttl: int = Field(
        86400,
        ge=300,
        le=604800,
        description="Plugin cache TTL in seconds",
    )
    discovery_url: str = Field(
        "https://hub.meltano.com/meltano/discovery.yml",
        description="Meltano Hub discovery URL",
    )
    default_variant: str = Field(
        "original",
        description="Default plugin variant to use",
    )


class MeltanoMonitoringConfig(DomainValueObject):
    """Meltano monitoring configuration value object."""

    metrics_enabled: bool = Field(
        True,
        description="Enable metrics collection",
    )
    health_check_interval: int = Field(
        60,
        ge=10,
        le=3600,
        description="Health check interval in seconds",
    )
    log_level: str = Field(
        "INFO",
        description="Logging level for Meltano operations",
    )
    event_publishing: bool = Field(
        True,
        description="Enable event publishing to FLEXT event bus",
    )


@singleton()
class MeltanoSettings(BaseSettings):
    """FLEXT Meltano configuration settings with environment variable support.

    All settings can be overridden via environment variables with the
    prefix FLEXT_MELTANO_ (e.g., FLEXT_MELTANO_PROJECT__PROJECT_ROOT).

    Uses flext-core BaseSettings foundation with DI support.
    """

    model_config = {
        "env_prefix": "FLEXT_MELTANO_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "env_nested_delimiter": "__",
        "case_sensitive": False,
        "extra": "forbid",
        "validate_assignment": True,
        "str_strip_whitespace": True,
        "use_enum_values": True,
    }

    # Project identification
    project_name: str = Field("flext-meltano", description="Project name")
    project_version: str = Field("0.7.0", description="Project version")

    # Configuration value objects
    project: MeltanoProjectConfig = Field(
        default_factory=MeltanoProjectConfig,
        description="Project configuration",
    )
    execution: MeltanoExecutionConfig = Field(
        default_factory=MeltanoExecutionConfig,
        description="Execution configuration",
    )
    state: MeltanoStateConfig = Field(
        default_factory=MeltanoStateConfig,
        description="State configuration",
    )
    plugins: MeltanoPluginConfig = Field(
        default_factory=MeltanoPluginConfig,
        description="Plugin configuration",
    )
    monitoring: MeltanoMonitoringConfig = Field(
        default_factory=MeltanoMonitoringConfig,
        description="Monitoring configuration",
    )

    # Environment and debugging
    environment: str = Field("development", description="Environment name")
    debug: bool = Field(False, description="Debug mode")

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

    @property
    def metrics_enabled(self) -> bool:
        """Check if metrics collection is enabled.

        Returns:
            True if metrics are enabled, False otherwise.

        """
        return self.monitoring.metrics_enabled

    def configure_dependencies(self, container: Any | None = None) -> None:
        """Configure dependency injection container.

        Args:
            container: Optional dependency injection container.

        """
        if container is None:
            container = get_container()

        # Register this settings instance
        container.register(MeltanoSettings, self)

        # Call parent configuration
        super().configure_dependencies(container)


# Convenience functions for getting settings
def get_meltano_settings() -> MeltanoSettings:
    return MeltanoSettings()


def create_development_meltano_config() -> MeltanoSettings:
    return MeltanoSettings(
        environment="development",
        debug=True,
        project=MeltanoProjectConfig(
            default_environment="dev",
            database_uri="sqlite:///dev_meltano.db",
        ),
        execution=MeltanoExecutionConfig(
            max_concurrent_jobs=2,
            job_timeout=1800,  # 30 minutes for development
            retry_attempts=1,
        ),
        state=MeltanoStateConfig(
            backup_enabled=False,  # Disable for development
            backup_interval=7200,  # 2 hours
        ),
        plugins=MeltanoPluginConfig(
            auto_install=True,
            plugin_cache_ttl=3600,  # 1 hour
        ),
        monitoring=MeltanoMonitoringConfig(
            log_level="DEBUG",
            health_check_interval=30,
            event_publishing=False,  # Disable for development
        ),
    )


def create_production_meltano_config() -> MeltanoSettings:
    return MeltanoSettings(
        environment="production",
        debug=False,
        project=MeltanoProjectConfig(
            default_environment="prod",
            database_uri="postgresql://localhost/meltano_prod",
        ),
        execution=MeltanoExecutionConfig(
            max_concurrent_jobs=10,
            job_timeout=7200,  # 2 hours for production
            retry_attempts=3,
            retry_delay=60,
        ),
        state=MeltanoStateConfig(
            state_backend="s3",
            backup_enabled=True,
            backup_interval=1800,  # 30 minutes
            max_backups=50,
        ),
        plugins=MeltanoPluginConfig(
            auto_install=False,  # Manual control in production
            plugin_cache_ttl=86400,  # 24 hours
            default_variant="meltanolabs",
        ),
        monitoring=MeltanoMonitoringConfig(
            log_level="WARNING",
            health_check_interval=120,
            event_publishing=True,
        ),
    )
