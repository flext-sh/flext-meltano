"""FLEXT Meltano job models."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from flext_meltano.constants import FlextMeltanoJobStatus


class FlextMeltanoJob(BaseModel):
    """FLEXT Meltano job configuration."""

    id: str = Field(..., description="Job ID")
    name: str = Field(..., description="Job name")
    status: FlextMeltanoJobStatus = Field(
        default=FlextMeltanoJobStatus.PENDING, description="Job status",
    )
    config: dict[str, Any] = Field(
        default_factory=dict, description="Job configuration",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Creation time",
    )
    started_at: datetime | None = Field(default=None, description="Start time")
    completed_at: datetime | None = Field(default=None, description="Completion time")
    error: str | None = Field(default=None, description="Error message")

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
        validate_assignment = True
