"""Meltano Job Domain Entity - NEW SEMANTIC ARCHITECTURE.

MeltanoJob represents a Meltano job execution with its state and business rules.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any, ClassVar

from flext_core import FlextResult
from pydantic import BaseModel, Field, field_validator

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports

DomainEntity = BaseModel


class FlextMeltanoJob(DomainEntity):
    """Meltano job domain entity with execution semantics."""

    # Primary identifier
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique job identifier")

    # Identity
    job_id: str = Field(..., description="Business job identifier")
    name: str = Field(..., description="Job name")
    project_id: Any = Field(..., description="Associated project ID")

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
    description: str | None = Field(default=None, description="Job description")
    triggered_by: Any | None = Field(default=None, description="Who/what triggered the job")
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

    def start(self) -> FlextResult[None]:
        """Start job execution."""
        if self.status != "pending":
            return FlextResult.fail(f"Cannot start job in '{self.status}' status")

        self.status = "running"
        self.started_at = datetime.now(UTC)
        self.finished_at = None
        self.exit_code = None
        self.error_message = None

        return FlextResult.ok(None)

    def complete(
        self,
        exit_code: int = 0,
        output: str | None = None,
    ) -> FlextResult[None]:
        """Mark job as completed."""
        if self.status != "running":
            return FlextResult.fail(f"Cannot complete job in '{self.status}' status")

        self.status = "completed"
        self.finished_at = datetime.now(UTC)
        self.exit_code = exit_code
        self.output = output
        self.error_message = None

        return FlextResult.ok(None)

    def fail(
        self,
        exit_code: int = 1,
        error_message: str | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Mark job as failed."""
        if self.status not in {"running", "pending"}:
            return FlextResult.fail(f"Cannot fail job in '{self.status}' status")

        self.status = "failed"
        self.finished_at = datetime.now(UTC)
        self.exit_code = exit_code
        self.error_message = error_message

        return FlextResult.ok(
            {
                "job_id": self.job_id,
                "status": self.status,
                "exit_code": exit_code,
                "error_message": error_message,
            },
        )

    def cancel(self) -> FlextResult[None]:
        """Cancel job execution."""
        if self.status in self.TERMINAL_STATUSES:
            return FlextResult.fail(
                f"Cannot cancel job in terminal status '{self.status}'",
            )

        self.status = "cancelled"
        self.finished_at = datetime.now(UTC)

        return FlextResult.ok(None)

    def timeout(self) -> FlextResult[None]:
        """Mark job as timed out."""
        if self.status != "running":
            return FlextResult.fail(f"Cannot timeout job in '{self.status}' status")

        self.status = "timeout"
        self.finished_at = datetime.now(UTC)
        self.error_message = "Job execution timed out"

        return FlextResult.ok(None)

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

    def reset_for_retry(self) -> FlextResult[None]:
        """Reset job state for retry."""
        if not self.can_be_retried():
            return FlextResult.fail(f"Cannot retry job in '{self.status}' status")

        self.status = "pending"
        self.started_at = None
        self.finished_at = None
        self.exit_code = None
        self.output = None
        self.error_message = None

        return FlextResult.ok(None)

    def start_execution(self) -> None:
        """Start job execution."""
        self.status = "running"
        self.started_at = datetime.now(UTC)

    def complete_execution(self, exit_code: int, stdout: str | None = None, stderr: str | None = None) -> None:
        """Complete job execution."""
        self.status = "completed" if exit_code == 0 else "failed"
        self.exit_code = exit_code
        self.finished_at = datetime.now(UTC)
        if stdout:
            self.output = stdout
        if stderr:
            self.error_message = stderr

    def cancel_execution(self) -> None:
        """Cancel job execution."""
        self.status = "cancelled"
        self.finished_at = datetime.now(UTC)
