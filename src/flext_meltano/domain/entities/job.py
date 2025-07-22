"""Meltano Job Domain Entity - NEW SEMANTIC ARCHITECTURE.

MeltanoJob represents a Meltano job execution with its state and business rules.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, ClassVar

from flext_core.domain.pydantic_base import DomainEntity
from flext_core.domain.shared_types import ServiceResult
from pydantic import Field, field_validator


class MeltanoJob(DomainEntity):
    """Meltano job domain entity with execution semantics."""

    # Identity
    job_id: str = Field(..., description="Unique job identifier")
    name: str = Field(..., description="Job name")

    # Job definition
    tasks: list[str] = Field(default_factory=list, description="Job tasks")
    environment: str = Field(default="dev", description="Target environment")

    # Execution state
    status: str = Field(default="pending", description="Job status")
    started_at: datetime | None = Field(default=None, description="Job start time")
    finished_at: datetime | None = Field(default=None, description="Job finish time")

    # Results
    exit_code: int | None = Field(default=None, description="Job exit code")
    output: str | None = Field(default=None, description="Job output")
    error_message: str | None = Field(
        default=None,
        description="Error message if failed",
    )

    # Configuration
    config: dict[str, Any] = Field(
        default_factory=dict,
        description="Job configuration",
    )
    timeout_seconds: int | None = Field(
        default=None,
        description="Job timeout in seconds",
    )

    # Metadata
    project_id: str | None = Field(default=None, description="Associated project ID")
    created_by: str | None = Field(default=None, description="Job creator")

    # Business rules
    VALID_STATUSES: ClassVar[set[str]] = {
        "pending",
        "running",
        "completed",
        "failed",
        "cancelled",
        "timeout",
    }

    TERMINAL_STATUSES: ClassVar[set[str]] = {
        "completed",
        "failed",
        "cancelled",
        "timeout",
    }

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate job status."""
        if v not in cls.VALID_STATUSES:
            msg = f"Invalid status '{v}'. Must be one of: {cls.VALID_STATUSES}"
            raise ValueError(msg)
        return v

    @field_validator("job_id")
    @classmethod
    def validate_job_id(cls, v: str) -> str:
        """Validate job ID."""
        if not v or len(v.strip()) == 0:
            msg = "Job ID cannot be empty"
            raise ValueError(msg)
        return v.strip()

    @field_validator("tasks")
    @classmethod
    def validate_tasks(cls, v: list[str]) -> list[str]:
        """Validate job tasks."""
        if not v:
            msg = "Job must have at least one task"
            raise ValueError(msg)

        # Remove empty tasks
        cleaned_tasks = [task.strip() for task in v if task.strip()]
        if not cleaned_tasks:
            msg = "Job must have at least one non-empty task"
            raise ValueError(msg)

        return cleaned_tasks

    def start(self) -> ServiceResult[None]:
        """Start job execution."""
        if self.status != "pending":
            return ServiceResult.fail(f"Cannot start job in '{self.status}' status")

        self.status = "running"
        self.started_at = datetime.now(UTC)
        self.finished_at = None
        self.exit_code = None
        self.error_message = None

        return ServiceResult.ok(None)

    def complete(
        self, exit_code: int = 0, output: str | None = None,
    ) -> ServiceResult[None]:
        """Mark job as completed."""
        if self.status != "running":
            return ServiceResult.fail(f"Cannot complete job in '{self.status}' status")

        self.status = "completed"
        self.finished_at = datetime.now(UTC)
        self.exit_code = exit_code
        self.output = output
        self.error_message = None

        return ServiceResult.ok(None)

    def fail(
        self,
        exit_code: int = 1,
        error_message: str | None = None,
    ) -> ServiceResult[dict[str, Any]]:
        """Mark job as failed."""
        if self.status not in {"running", "pending"}:
            return ServiceResult.fail(f"Cannot fail job in '{self.status}' status")

        self.status = "failed"
        self.finished_at = datetime.now(UTC)
        self.exit_code = exit_code
        self.error_message = error_message

        return ServiceResult.ok(None)

    def cancel(self) -> ServiceResult[None]:
        """Cancel job execution."""
        if self.status in self.TERMINAL_STATUSES:
            return ServiceResult.fail(
                f"Cannot cancel job in terminal status '{self.status}'",
            )

        self.status = "cancelled"
        self.finished_at = datetime.now(UTC)

        return ServiceResult.ok(None)

    def timeout(self) -> ServiceResult[None]:
        """Mark job as timed out."""
        if self.status != "running":
            return ServiceResult.fail(f"Cannot timeout job in '{self.status}' status")

        self.status = "timeout"
        self.finished_at = datetime.now(UTC)
        self.error_message = "Job execution timed out"

        return ServiceResult.ok(None)

    def is_terminal(self) -> bool:
        """Check if job is in a terminal state."""
        return self.status in self.TERMINAL_STATUSES

    def is_successful(self) -> bool:
        """Check if job completed successfully."""
        return self.status == "completed" and (
            self.exit_code is None or self.exit_code == 0
        )

    def get_duration_seconds(self) -> float | None:
        """Get job duration in seconds."""
        if not self.started_at:
            return None

        end_time = self.finished_at or datetime.now(UTC)
        return (end_time - self.started_at).total_seconds()

    def can_be_retried(self) -> bool:
        """Check if job can be retried."""
        return self.status in {"failed", "timeout", "cancelled"}

    def reset_for_retry(self) -> ServiceResult[None]:
        """Reset job state for retry."""
        if not self.can_be_retried():
            return ServiceResult.fail(f"Cannot retry job in '{self.status}' status")

        self.status = "pending"
        self.started_at = None
        self.finished_at = None
        self.exit_code = None
        self.output = None
        self.error_message = None

        return ServiceResult.ok(None)
