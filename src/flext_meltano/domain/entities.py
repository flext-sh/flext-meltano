"""Domain entities for FLEXT-MELTANO v0.7.0.

REFACTORED:
- Using flext-core modern patterns - NO duplication.
All entities use mixins from flext-core for maximum code reduction.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING
from typing import Any

from flext_core.domain.pydantic_base import DomainEntity
from flext_core.domain.pydantic_base import DomainEvent
from flext_core.domain.pydantic_base import Field

# Import enum types from flext-core - NO duplication
from flext_core.domain.types import Status as PipelineStatus

if TYPE_CHECKING:
    from uuid import UUID


class JobType(StrEnum):
    """Meltano job types."""

    ELT = "elt"
    RUN = "run"
    TEST = "test"
    DESCRIBE = "describe"
    INVOKE = "invoke"
    SCHEDULE = "schedule"


class MeltanoPluginType(StrEnum):
    """Meltano plugin types."""

    EXTRACTORS = "extractors"
    LOADERS = "loaders"
    TRANSFORMS = "transforms"
    ORCHESTRATORS = "orchestrators"
    TRANSFORMERS = "transformers"
    FILES = "files"
    UTILITIES = "utilities"


class MeltanoProject(DomainEntity):
    """Meltano project domain entity."""

    # Project paths
    project_root: str = Field(..., min_length=1)
    meltano_file_path: str = Field(..., min_length=1)

    # Configuration
    meltano_version: str = Field(..., min_length=1)
    python_version: str = Field(default="3.13")

    # Environment
    default_environment: str = Field(default="dev")
    environments: list[str] = Field(default_factory=list)

    # State
    state_backend: str = Field(default="systemdb")

    # Status and metadata
    status: PipelineStatus = Field(default=PipelineStatus.ACTIVE)
    created_by: UUID | None = None

    def add_environment(self, environment: str) -> None:
        """Add environment to Meltano project.

        Args:
            environment: Environment name to add.

        """
        if environment not in self.environments:
            self.environments.append(environment)

    def remove_environment(self, environment: str) -> None:
        """Remove environment from Meltano project.

        Args:
            environment: Environment name to remove.

        """
        if environment in self.environments:
            self.environments.remove(environment)


class MeltanoPlugin(DomainEntity):
    """Meltano plugin domain entity."""

    project_id: UUID = Field(..., description="Associated project ID")

    # Plugin identification
    namespace: str = Field(..., min_length=1, max_length=255)
    plugin_type: MeltanoPluginType = Field(...)

    # Plugin details
    pip_url: str | None = None

    # Configuration
    select: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    # Status
    status: PipelineStatus = Field(default=PipelineStatus.ACTIVE)
    installed: bool = Field(default=False)
    enabled: bool = Field(default=True)

    def install(self) -> None:
        """Mark plugin as installed."""
        self.installed = True

    def uninstall(self) -> None:
        """Mark plugin as uninstalled."""
        self.installed = False

    def enable(self) -> None:
        """Enable plugin for execution."""
        self.enabled = True

    def disable(self) -> None:
        """Disable plugin from execution."""
        self.enabled = False

    def update_plugin_config(self, config: dict[str, Any]) -> None:
        """Update plugin configuration with new settings.

        Args:
            config: Dictionary of configuration key-value pairs.

        """
        # Update metadata instead of using non-existent set_config
        self.metadata.update(config)


class MeltanoJob(DomainEntity):
    """Meltano job domain entity."""

    project_id: UUID = Field(..., description="Associated project ID")

    # Job identification
    job_id: str = Field(..., min_length=1, max_length=255)
    job_type: JobType = Field(...)

    # Command details
    command: list[str] = Field(default_factory=list)
    environment: str = Field(default="dev")

    # Timing
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_seconds: float | None = None

    # Results
    exit_code: int | None = None
    stdout: str | None = None
    stderr: str | None = None

    # Status and context
    status: PipelineStatus = Field(default=PipelineStatus.PENDING)
    run_id: str | None = None
    triggered_by: UUID | None = None

    @property
    def is_completed(self) -> bool:
        """Check if Meltano job execution has completed.

        Returns:
            True if job is in a terminal state (completed, failed, or cancelled).

        """
        return self.status in {
            PipelineStatus.COMPLETED,
            PipelineStatus.FAILED,
            PipelineStatus.CANCELLED,
        }

    @property
    def is_successful(self) -> bool:
        """Check if Meltano job execution completed successfully.

        Returns:
            True if job completed with exit code 0.

        """
        return self.status == PipelineStatus.COMPLETED and self.exit_code == 0

    def start_execution(self) -> None:
        """Start Meltano job execution and update status."""
        self.status = PipelineStatus.PROCESSING
        self.started_at = datetime.now()

    def complete_execution(
        self, exit_code: int, stdout: str | None = None, stderr: str | None = None,
    ) -> None:
        """Complete Meltano job execution with results.

        Args:
            exit_code: Process exit code.
            stdout: Standard output from execution.
            stderr: Standard error from execution.

        """
        self.status = (
            PipelineStatus.COMPLETED if exit_code == 0 else PipelineStatus.FAILED
        )
        self.exit_code = exit_code
        self.completed_at = datetime.now()
        self.stdout = stdout
        self.stderr = stderr

        if self.started_at:
            duration = self.completed_at - self.started_at
            self.duration_seconds = duration.total_seconds()

    def cancel_execution(self) -> None:
        """Cancel ongoing Meltano job execution."""
        self.status = PipelineStatus.CANCELLED
        self.completed_at = datetime.now()

        if self.started_at:
            duration = self.completed_at - self.started_at
            self.duration_seconds = duration.total_seconds()


class MeltanoState(DomainEntity):
    """Meltano state domain entity."""

    project_id: UUID = Field(..., description="Associated project ID")
    job_id: UUID = Field(..., description="Associated job ID")

    # State identification
    state_id: str = Field(..., min_length=1, max_length=255)

    # State data
    state_data: dict[str, Any] = Field(default_factory=dict)

    # Metadata
    environment: str = Field(default="dev")

    # Timestamps
    state_updated_at: datetime = Field(default_factory=datetime.now)

    def update_state(self, state_data: dict[str, Any]) -> None:
        """Update Meltano plugin state data.

        Args:
            state_data: New state data to replace current state.

        """
        self.state_data = state_data
        self.state_updated_at = datetime.now()
        # Version management would be handled by versioning system if needed

    def merge_state(self, partial_state: dict[str, Any]) -> None:
        """Merge partial state data with existing state.

        Args:
            partial_state: Partial state data to merge.

        """
        self.state_data.update(partial_state)
        self.state_updated_at = datetime.now()
        # Version management would be handled by versioning system if needed


class MeltanoSchedule(DomainEntity):
    """Meltano schedule domain entity."""

    project_id: UUID = Field(..., description="Associated project ID")

    # Schedule configuration
    job: str = Field(..., min_length=1)
    interval: str = Field(..., min_length=1)  # cron format

    # Environment
    environment: str = Field(default="dev")

    # Status
    enabled: bool = Field(default=True)

    # Last run
    last_run_at: datetime | None = None
    next_run_at: datetime | None = None

    def enable_schedule(self) -> None:
        """Enable Meltano schedule for execution."""
        self.enabled = True

    def disable_schedule(self) -> None:
        """Disable Meltano schedule from execution."""
        self.enabled = False

    def update_last_run(self, run_time: datetime) -> None:
        """Update last run timestamp for schedule.

        Args:
            run_time: Timestamp of last execution.

        """
        self.last_run_at = run_time

    def update_next_run(self, run_time: datetime) -> None:
        """Update next run timestamp for schedule.

        Args:
            run_time: Timestamp of next scheduled execution.

        """
        self.next_run_at = run_time


class MeltanoEnvironment(DomainEntity):
    """Meltano environment domain entity."""

    project_id: UUID = Field(..., description="Associated project ID")

    # Environment variables
    env_vars: dict[str, str] = Field(default_factory=dict)

    def update_env_config(self, config: dict[str, Any]) -> None:
        """Update environment configuration settings.

        Args:
            config: Dictionary of configuration key-value pairs.

        """
        # Store in env_vars since we don't have set_config method
        for key, value in config.items():
            self.env_vars[key] = str(value)

    def update_env_vars(self, env_vars: dict[str, str]) -> None:
        """Update environment variables.

        Args:
            env_vars: Dictionary of environment variable key-value pairs.

        """
        self.env_vars.update(env_vars)


# Domain Events
class ProjectCreatedEvent(DomainEvent):
    """Event raised when Meltano project is created."""

    project_id: UUID
    project_name: str | None = None


class PluginInstalledEvent(DomainEvent):
    """Event raised when plugin is installed."""

    project_id: UUID
    plugin_id: UUID
    plugin_name: str
    plugin_type: MeltanoPluginType


class JobStartedEvent(DomainEvent):
    """Event raised when Meltano job starts."""

    project_id: UUID
    job_id: UUID
    job_type: JobType
    command: list[str]
    environment: str
    run_id: str | None = None


class JobCompletedEvent(DomainEvent):
    """Event raised when Meltano job completes."""

    project_id: UUID
    job_id: UUID | None = None
    duration_seconds: float | None = None


class StateUpdatedEvent(DomainEvent):
    """Event raised when state is updated."""

    project_id: UUID
    job_id: UUID
    state_id: str
    version: int
    environment: str


class ScheduleTriggeredEvent(DomainEvent):
    """Event raised when schedule is triggered."""

    project_id: UUID
    schedule_id: UUID
    schedule_name: str
    job: str
    environment: str
    triggered_at: datetime
