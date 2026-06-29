"""FLEXT Meltano models - Pipeline result models."""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated, Self

from flext_cli import m, u
from flext_meltano import c, t
from flext_meltano._models.results import FlextMeltanoModelsResults


class FlextMeltanoModelsResultsPipeline:
    """Pipeline result models."""

    class PipelineResult(m.TimestampedModel):
        """Generic pipeline execution result with complete validation."""

        pipeline_id: Annotated[str, u.Field(description="Pipeline identifier")]
        source_result: Annotated[
            FlextMeltanoModelsResults.ExecutionResult | None,
            u.Field(default=None, description="Source execution result"),
        ] = None
        sink_result: Annotated[
            FlextMeltanoModelsResults.ExecutionResult | None,
            u.Field(default=None, description="Sink execution result"),
        ] = None
        transformation_result: Annotated[
            FlextMeltanoModelsResults.ExecutionResult | None,
            u.Field(default=None, description="Transformation execution result"),
        ] = None
        overall_status: Annotated[
            str,
            u.Field(
                default=c.Meltano.OperationStatus.PENDING,
                description="Overall pipeline status",
            ),
        ] = c.Meltano.OperationStatus.PENDING
        total_records: Annotated[
            t.NonNegativeInt, u.Field(default=0, description="Total records processed")
        ] = 0
        pipeline_metadata: Annotated[
            t.ConfigurationMapping, u.Field(description="Pipeline execution metadata")
        ] = u.Field(default_factory=lambda: MappingProxyType({}))

        @u.computed_field()
        @property
        def completed_stages(self) -> t.StrSequence:
            """Completed pipeline stages."""
            return [
                stage
                for stage, result in (
                    ("extraction", self.source_result),
                    ("loading", self.sink_result),
                    ("transformation", self.transformation_result),
                )
                if result is not None and result.end_time is not None
            ]

        @u.computed_field()
        @property
        def completion_percentage(self) -> float:
            """Pipeline completion percentage."""
            total_stages = 3
            completed = 0
            src = self.source_result
            if src is not None and src.end_time is not None:
                completed += 1
            snk = self.sink_result
            if snk is not None and snk.end_time is not None:
                completed += 1
            trn = self.transformation_result
            if trn is not None and trn.end_time is not None:
                completed += 1
            return (completed / total_stages) * 100

        def _all_stages_successful(self) -> bool:
            """Check if all stages completed successfully."""
            s = c.Meltano.OperationStatus.SUCCESS
            return bool(
                self.source_result
                and self.source_result.status == s
                and self.source_result.error_message is None
                and self.sink_result
                and self.sink_result.status == s
                and self.sink_result.error_message is None
                and self.transformation_result
                and self.transformation_result.status == s
                and self.transformation_result.error_message is None,
            )

        @u.computed_field()
        @property
        def is_fully_successful(self) -> bool:
            """Check if all stages completed successfully."""
            return self._all_stages_successful()

        @u.computed_field()
        @property
        def total_duration_seconds(self) -> float:
            """Total pipeline duration."""
            total = 0.0
            if self.source_result and self.source_result.duration_seconds:
                total += self.source_result.duration_seconds
            if self.sink_result and self.sink_result.duration_seconds:
                total += self.sink_result.duration_seconds
            if (
                self.transformation_result
                and self.transformation_result.duration_seconds
            ):
                total += self.transformation_result.duration_seconds
            return total

        @u.field_validator("overall_status", mode="before")
        @classmethod
        def validate_overall_status(cls, v: str) -> str:
            """Validate overall pipeline status."""
            valid_statuses = [
                c.Meltano.OperationStatus.PENDING,
                c.Meltano.OperationStatus.RUNNING,
                c.Meltano.OperationStatus.SUCCESS,
                "partial",
                c.Meltano.OperationStatus.ERROR,
            ]
            if v not in valid_statuses:
                msg = f"Overall status must be one of: {', '.join(valid_statuses)}"
                raise ValueError(msg)
            return v

        @u.model_validator(mode="after")
        def validate_pipeline_result(self) -> Self:
            """Validate pipeline result consistency."""
            total_from_stages = 0
            if self.source_result:
                total_from_stages += self.source_result.records_processed

            if (
                self.total_records > 0
                and total_from_stages > 0
                and abs(self.total_records - total_from_stages)
                > (total_from_stages * 0.1)
            ):
                msg = "Total records inconsistent with stage results"
                raise ValueError(msg)

            if (
                self._all_stages_successful()
                and self.overall_status != c.Meltano.OperationStatus.SUCCESS
            ):
                self.overall_status = c.Meltano.OperationStatus.SUCCESS

            return self
