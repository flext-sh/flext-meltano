"""JobStatus enum for Meltano domain."""

from __future__ import annotations

from enum import StrEnum


class JobStatus(StrEnum):
    """Meltano job execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
