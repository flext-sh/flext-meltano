"""Domain entities for FLEXT-MELTANO.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Meltano-specific domain entities using flext-core patterns.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
from pydantic import BaseModel, Field

# Define domain types as BaseModel for now
DomainEntity = BaseModel
DomainEvent = BaseModel

# Initialize types via DI container
if TYPE_CHECKING:
    from flext_meltano.infrastructure.di_container import EntityId, UserId


# Meltano-specific constants
class MeltanoConstants:
    """Constants for Meltano domain."""

    MAX_PROJECT_NAME_LENGTH = 255
    MAX_PLUGIN_NAME_LENGTH = 100
    MAX_JOB_NAME_LENGTH = 100
    DEFAULT_ENVIRONMENT = "dev"
    FRAMEWORK_VERSION = "0.7.0"


class PluginType(StrEnum):
    """Meltano plugin types."""

    EXTRACTOR = "extractors"
    LOADER = "loaders"
    TRANSFORMER = "transformers"
    ORCHESTRATOR = "orchestrators"
    UTILITY = "utilities"
    FILE = "files"


class JobStatus(StrEnum):
    """Meltano job execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EnvironmentType(StrEnum):
    """Meltano environment types."""

    DEVELOPMENT = "dev"
    STAGING = "staging"
    PRODUCTION = "prod"
    TEST = "test"


class MeltanoProject(DomainEntity):
    """Meltano project domain entity."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=MeltanoConstants.MAX_PROJECT_NAME_LENGTH,
    )
    description: str | None = Field(None, max_length=1000)

    # Project paths
    project_root: str = Field(..., min_length=1)
    meltano_yml_path: str = Field(..., min_length=1)

    # Configuration
    meltano_version: str = Field(..., min_length=1)
    project_id: str = Field(..., min_length=1)

    # Environment management
    default_environment: EnvironmentType = Field(default=EnvironmentType.DEVELOPMENT)
    environments: list[str] = Field(default_factory=list)

    # State management
    state_backend: str = Field(default="systemdb")
    send_anonymous_usage_stats: bool = Field(default=True)

    # Metadata
    created_by: UserId | None = None
    project_url: str | None = None

    def add_environment(self, environment: str) -> None:
        """Add environment to project."""
        if environment not in self.environments:
            self.environments.append(environment)

    def remove_environment(self, environment: str) -> None:
        """Remove environment from project."""
        if environment in self.environments:
            self.environments.remove(environment)

    @property
    def is_initialized(self) -> bool:
        """Check if project is properly initialized."""
        return bool(self.project_root and self.meltano_yml_path)


class MeltanoPlugin(DomainEntity):
    """Meltano plugin domain entity."""

    project_id: EntityId = Field(..., description="Associated project ID")

    # Plugin identification
    name: str = Field(
        ...,
        min_length=1,
        max_length=MeltanoConstants.MAX_PLUGIN_NAME_LENGTH,
    )
    namespace: str = Field(..., min_length=1)
    plugin_type: PluginType = Field(...)
    variant: str = Field(default="original")

    # Installation details
    pip_url: str | None = None
    executable: str | None = None
    commands: dict[str, str] = Field(default_factory=dict)

    # Configuration
    settings: dict[str, Any] = Field(default_factory=dict)
    config: dict[str, Any] = Field(default_factory=dict)
    select: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    # Status
    installed: bool = Field(default=False)
    enabled: bool = Field(default=True)

    # Inheritance and extras
    inherit_from: str | None = None
    extras: dict[str, Any] = Field(default_factory=dict)

    def install(self) -> None:
        """Mark plugin as installed."""
        self.installed = True

    def uninstall(self) -> None:
        """Mark plugin as uninstalled and disable."""
        self.installed = False
        self.enabled = False

    def enable(self) -> None:
        """Enable plugin."""
        self.enabled = True

    def disable(self) -> None:
        """Disable plugin."""
        self.enabled = False

    def update_config(self, config: dict[str, Any]) -> None:
        """Update plugin configuration."""
        self.config.update(config)

    def update_settings(self, settings: dict[str, Any]) -> None:
        """Update plugin settings."""
        self.settings.update(settings)


class MeltanoJob(DomainEntity):
    """Meltano job domain entity."""

    project_id: EntityId = Field(..., description="Associated project ID")

    # Job identification
    name: str = Field(
        ...,
        min_length=1,
        max_length=MeltanoConstants.MAX_JOB_NAME_LENGTH,
    )
    description: str | None = Field(None, max_length=1000)

    # Job configuration
    tasks: list[str] = Field(default_factory=list)
    environment: EnvironmentType = Field(default=EnvironmentType.DEVELOPMENT)

    # Execution tracking
    status: JobStatus = Field(default=JobStatus.PENDING)
    run_id: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_seconds: float | None = None

    # Results
    exit_code: int | None = None
    stdout: str | None = None
    stderr: str | None = None
    state: dict[str, Any] = Field(default_factory=dict)

    # Context
    triggered_by: UserId | None = None
    trigger_type: str | None = None  # manual, schedule, webhook

    @property
    def is_running(self) -> bool:
        """Check if job is currently running."""
        return self.status == JobStatus.RUNNING

    @property
    def is_completed(self) -> bool:
        """Check if job execution is completed."""
        return self.status in {
            JobStatus.COMPLETED,
            JobStatus.FAILED,
            JobStatus.CANCELLED,
        }

    @property
    def is_successful(self) -> bool:
        """Check if job completed successfully."""
        return self.status == JobStatus.COMPLETED and self.exit_code == 0

    def start_execution(self) -> None:
        """Start job execution."""
        self.status = JobStatus.RUNNING
        self.started_at = datetime.now()

    def complete_execution(
        self,
        exit_code: int,
        stdout: str | None = None,
        stderr: str | None = None,
        state: dict[str, Any] | None = None,
    ) -> None:
        """Complete job execution."""
        self.status = JobStatus.COMPLETED if exit_code == 0 else JobStatus.FAILED
        self.exit_code = exit_code
        self.completed_at = datetime.now()
        self.stdout = stdout
        self.stderr = stderr

        if state:
            self.state = state

        if self.started_at:
            duration = self.completed_at - self.started_at
            self.duration_seconds = duration.total_seconds()

    def cancel_execution(self) -> None:
        """Cancel job execution."""
        self.status = JobStatus.CANCELLED
        self.completed_at = datetime.now()

        if self.started_at:
            duration = self.completed_at - self.started_at
            self.duration_seconds = duration.total_seconds()


class MeltanoSchedule(DomainEntity):
    """Meltano schedule domain entity."""

    project_id: EntityId = Field(..., description="Associated project ID")

    # Schedule identification
    name: str = Field(..., min_length=1, max_length=255)
    job: str = Field(..., min_length=1)  # Job name to execute

    # Schedule configuration
    interval: str = Field(..., min_length=1)  # Cron expression
    start_date: datetime | None = None
    end_date: datetime | None = None

    # Environment
    environment: EnvironmentType = Field(default=EnvironmentType.DEVELOPMENT)

    # Status
    enabled: bool = Field(default=True)

    # Execution tracking
    last_run_at: datetime | None = None
    next_run_at: datetime | None = None
    last_run_status: JobStatus | None = None

    def enable(self) -> None:
        """Enable schedule."""
        self.enabled = True

    def disable(self) -> None:
        """Disable schedule."""
        self.enabled = False

    def update_last_run(
        self,
        run_time: datetime,
        status: JobStatus,
    ) -> None:
        """Update last run information."""
        self.last_run_at = run_time
        self.last_run_status = status

    def update_next_run(self, next_run: datetime) -> None:
        """Update next scheduled run time."""
        self.next_run_at = next_run


class MeltanoEnvironment(DomainEntity):
    """Meltano environment domain entity."""

    project_id: EntityId = Field(..., description="Associated project ID")

    # Environment identification
    name: str = Field(..., min_length=1, max_length=255)
    env_type: EnvironmentType = Field(...)

    # Configuration
    config: dict[str, Any] = Field(default_factory=dict)
    env_vars: dict[str, str] = Field(default_factory=dict)

    # Plugin configurations
    plugin_configs: dict[str, dict[str, Any]] = Field(default_factory=dict)

    def update_config(self, config: dict[str, Any]) -> None:
        """Update environment configuration."""
        self.config.update(config)

    def update_env_vars(self, env_vars: dict[str, str]) -> None:
        """Update environment variables."""
        self.env_vars.update(env_vars)

    def update_plugin_config(
        self,
        plugin_name: str,
        config: dict[str, Any],
    ) -> None:
        """Update plugin-specific configuration."""
        if plugin_name not in self.plugin_configs:
            self.plugin_configs[plugin_name] = {}
        self.plugin_configs[plugin_name].update(config)


class MeltanoState(DomainEntity):
    """Meltano state domain entity."""

    project_id: EntityId = Field(..., description="Associated project ID")
    job_id: EntityId = Field(..., description="Associated job ID")

    # State identification
    state_id: str = Field(..., min_length=1)
    plugin_name: str = Field(..., min_length=1)

    # State data
    state_data: dict[str, Any] = Field(default_factory=dict)
    version: int = Field(default=1)

    # Environment context
    environment: EnvironmentType = Field(default=EnvironmentType.DEVELOPMENT)

    # Timestamps
    state_updated_at: datetime = Field(default_factory=datetime.now)

    def update_state(self, state_data: dict[str, Any]) -> None:
        """Update state data."""
        self.state_data = state_data
        self.state_updated_at = datetime.now()
        self.version += 1

    def merge_state(self, partial_state: dict[str, Any]) -> None:
        """Merge partial state data."""
        self.state_data.update(partial_state)
        self.state_updated_at = datetime.now()
        self.version += 1


# Domain Events
class ProjectCreatedEvent(DomainEvent):
    """Event raised when Meltano project is created."""

    project_id: EntityId = Field(..., description="Project ID")
    project_name: str | None = Field(None, description="Project name")
    environment: EnvironmentType = Field(default=EnvironmentType.DEVELOPMENT)


class PluginInstalledEvent(DomainEvent):
    """Event raised when plugin is installed."""

    project_id: EntityId = Field(..., description="Project ID")
    plugin_id: EntityId = Field(..., description="Plugin ID")
    plugin_name: str = Field(..., description="Plugin name")
    plugin_type: PluginType = Field(..., description="Plugin type")


class PluginUninstalledEvent(DomainEvent):
    """Event raised when plugin is uninstalled."""

    project_id: EntityId = Field(..., description="Project ID")
    plugin_id: EntityId = Field(..., description="Plugin ID")
    plugin_name: str = Field(..., description="Plugin name")


class JobStartedEvent(DomainEvent):
    """Event raised when job starts execution."""

    project_id: EntityId = Field(..., description="Project ID")
    job_id: EntityId = Field(..., description="Job ID")
    job_name: str = Field(..., description="Job name")
    run_id: str | None = Field(None, description="Run ID")
    environment: EnvironmentType = Field(default=EnvironmentType.DEVELOPMENT)


class JobCompletedEvent(DomainEvent):
    """Event raised when job completes execution."""

    project_id: EntityId = Field(..., description="Project ID")
    job_id: EntityId = Field(..., description="Job ID")
    job_name: str = Field(..., description="Job name")
    success: bool = Field(..., description="Success status")
    duration_seconds: float | None = Field(None, description="Execution duration")


class JobFailedEvent(DomainEvent):
    """Event raised when job fails."""

    project_id: EntityId = Field(..., description="Project ID")
    job_id: EntityId = Field(..., description="Job ID")
    job_name: str = Field(..., description="Job name")
    error_message: str | None = Field(None, description="Error message")


class ScheduleTriggeredEvent(DomainEvent):
    """Event raised when schedule triggers job execution."""

    project_id: EntityId = Field(..., description="Project ID")
    schedule_id: EntityId = Field(..., description="Schedule ID")
    schedule_name: str = Field(..., description="Schedule name")
    job_name: str = Field(..., description="Job name")
    triggered_at: datetime = Field(default_factory=datetime.now)


class StateUpdatedEvent(DomainEvent):
    """Event raised when plugin state is updated."""

    project_id: EntityId = Field(..., description="Project ID")
    job_id: EntityId = Field(..., description="Job ID")
    state_id: str = Field(..., description="State ID")
    plugin_name: str = Field(..., description="Plugin name")
    version: int = Field(..., description="State version")
    environment: EnvironmentType = Field(default=EnvironmentType.DEVELOPMENT)


class EnvironmentCreatedEvent(DomainEvent):
    """Event raised when environment is created."""

    project_id: EntityId = Field(..., description="Project ID")
    environment_id: EntityId = Field(..., description="Environment ID")
    environment_name: str = Field(..., description="Environment name")
    env_type: EnvironmentType = Field(..., description="Environment type")
