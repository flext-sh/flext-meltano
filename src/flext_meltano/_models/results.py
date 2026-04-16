"""FLEXT Meltano models - Execution result models."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Self

from flext_cli import m, u

from flext_meltano import c, t


class FlextMeltanoModelsResults:
    """Execution result models."""

    class ExecutionResult(m.TimestampedModel):
        """Generic execution result tracking with validation."""

        operation: Annotated[str, u.Field(description="Operation performed")]
        status: Annotated[str, u.Field(description="Execution status")]
        start_time: Annotated[datetime, u.Field(description="Execution start time")] = (
            u.Field(
                default_factory=lambda: datetime.now(tz=UTC),
                description="Execution start time",
            )
        )
        end_time: Annotated[
            datetime | None, u.Field(default=None, description="Execution end time")
        ] = None
        duration_seconds: Annotated[
            float | None,
            u.Field(default=None, description="Execution duration in seconds"),
        ] = None
        records_processed: Annotated[
            t.NonNegativeInt,
            u.Field(default=0, description="Number of records processed"),
        ] = 0
        error_message: Annotated[
            str | None, u.Field(default=None, description="Error message if failed")
        ] = None
        metadata: Annotated[
            t.ConfigurationMapping, u.Field(description="Additional execution metadata")
        ] = u.Field(default_factory=dict, description="Additional execution metadata")

        @u.computed_field()
        @property
        def execution_rate_per_second(self) -> float:
            """Execution rate (records/second)."""
            if not self.duration_seconds or self.duration_seconds <= 0:
                return 0.0
            return self.records_processed / self.duration_seconds

        @u.computed_field()
        @property
        def is_completed(self) -> bool:
            """Check if execution is completed."""
            return self.end_time is not None

        @u.computed_field()
        @property
        def is_successful(self) -> bool:
            """Check if execution was successful."""
            return (
                self.status == c.Meltano.OperationStatus.SUCCESS
                and self.error_message is None
            )

        @u.computed_field()
        @property
        def performance_category(self) -> str:
            """Performance categorization."""
            if not self.duration_seconds or self.duration_seconds <= 0:
                rate = 0.0
            else:
                rate = self.records_processed / self.duration_seconds

            if rate >= c.Meltano.VALIDATION_EXECUTION_HIGH_PERFORMANCE_THRESHOLD:
                return "high_performance"
            if rate >= c.Meltano.VALIDATION_EXECUTION_GOOD_PERFORMANCE_THRESHOLD:
                return "good_performance"
            if rate >= c.Meltano.VALIDATION_EXECUTION_MODERATE_PERFORMANCE_THRESHOLD:
                return "moderate_performance"
            return "low_performance"

        @u.field_validator("status", mode="before")
        @classmethod
        def validate_status(cls, v: str) -> str:
            """Validate execution status."""
            valid_statuses = [
                c.Meltano.OperationStatus.PENDING,
                c.Meltano.OperationStatus.RUNNING,
                c.Meltano.OperationStatus.SUCCESS,
                c.Meltano.OperationStatus.ERROR,
                c.Meltano.OperationStatus.TIMEOUT,
            ]
            if v not in valid_statuses:
                msg = f"Status must be one of: {', '.join(valid_statuses)}"
                raise ValueError(msg)
            return v

        @u.model_validator(mode="after")
        def validate_execution_result(self) -> Self:
            """Validate execution result consistency."""
            if self.start_time and self.end_time:
                calculated_duration = (self.end_time - self.start_time).total_seconds()
                if self.duration_seconds is None:
                    self.duration_seconds = calculated_duration
                elif abs(self.duration_seconds - calculated_duration) > 1.0:
                    msg = "Duration inconsistent with start/end times"
                    raise ValueError(msg)

            if (
                self.status == c.Meltano.OperationStatus.ERROR
                and not self.error_message
            ):
                msg = "Error status requires error message"
                raise ValueError(msg)

            return self
