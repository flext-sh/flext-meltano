"""FLEXT Meltano models - Instance and stream models."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Annotated, Self

from flext_cli import m, u
from pydantic import Field, computed_field, model_validator

from flext_meltano import c, t
from flext_meltano._models.sources import FlextMeltanoModelsSources


class FlextMeltanoModelsInstances:
    """Instance and stream models."""

    class DataSinkDefinition(m.Entity):
        """Generic data sink definition for pipeline operations."""

        sink_name: Annotated[str, Field(description="Name of the sink")]
        sink_type: Annotated[str, Field(description="Type of the sink")]
        config: Annotated[
            t.ConfigurationMapping, Field(description="Sink configuration")
        ] = Field(default_factory=dict, description="Sink configuration")
        sink_schema: Annotated[
            t.FlatContainerMapping, Field(description="Sink schema")
        ] = Field(default_factory=dict, description="Sink schema")
        status: Annotated[
            str,
            Field(
                default=c.Meltano.StreamStatus.INITIALIZED, description="Current status"
            ),
        ] = c.Meltano.StreamStatus.INITIALIZED

        @computed_field
        def config_keys_count(self) -> int:
            """Number of config keys."""
            return u.count(list(self.config.keys()))

        @model_validator(mode="after")
        def validate_sink_definition(self) -> Self:
            """Validate sink definition consistency."""
            valid_statuses = {
                c.Meltano.StreamStatus.INITIALIZED,
                "configured",
                "running",
                c.Meltano.StreamStatus.COMPLETED,
                c.Meltano.StreamStatus.ERROR,
            }
            if self.status not in valid_statuses:
                msg = f"Status must be one of: {', '.join(valid_statuses)}"
                raise ValueError(msg)
            return self

    class StreamInfo(m.Entity):
        """Generic stream information for data pipeline operations."""

        stream_name: Annotated[
            t.NonEmptyStr, Field(description="Stream name identifier")
        ]
        stream_schema: Annotated[
            Mapping[str, t.Scalar | t.ScalarMapping],
            Field(description="Stream schema definition"),
        ]
        key_properties: Annotated[
            t.StrSequence, Field(description="Primary key properties for the stream")
        ] = Field(default_factory=list, description="Primary key properties")
        replication_method: Annotated[
            str, Field(default="FULL_TABLE", description="Replication method")
        ] = "FULL_TABLE"
        replication_key: Annotated[
            str | None, Field(default=None, description="Incremental replication field")
        ] = None
        status: Annotated[
            str,
            Field(
                default=c.Meltano.StreamStatus.INITIALIZED,
                description="Stream processing status",
            ),
        ] = c.Meltano.StreamStatus.INITIALIZED
        records_loaded: Annotated[
            t.NonNegativeInt, Field(default=0, description="Number of records loaded")
        ] = 0
        batches_processed: Annotated[
            t.NonNegativeInt,
            Field(default=0, description="Number of batches processed"),
        ] = 0
        stream_created_at: Annotated[str, Field(description="Creation timestamp")]

        @computed_field
        def average_records_per_batch(self) -> float:
            """Average records per batch."""
            return (
                0.0
                if self.batches_processed == 0
                else self.records_loaded / self.batches_processed
            )

        @computed_field
        def has_processed_data(self) -> bool:
            """Check if stream has processed data."""
            return self.records_loaded > 0 or self.batches_processed > 0

        @computed_field
        def processing_status(self) -> str:
            """Processing status assessment."""
            if (
                self.status == c.Meltano.StreamStatus.COMPLETED
                and self.records_loaded > 0
            ):
                return c.Meltano.StreamStatus.SUCCESS
            if self.status == c.Meltano.StreamStatus.ERROR:
                return c.Meltano.StreamStatus.FAILED
            if self.records_loaded > 0:
                return c.Meltano.StreamStatus.IN_PROGRESS
            return c.Meltano.StreamStatus.PENDING

        @model_validator(mode="after")
        def validate_stream_info(self) -> Self:
            """Validate stream information consistency."""
            if self.records_loaded > 0 and self.batches_processed == 0:
                msg = "Records loaded but no batches processed"
                raise ValueError(msg)
            if self.status not in c.Meltano.VALID_STATUSES:
                msg = f"Status must be one of: {', '.join(c.Meltano.VALID_STATUSES)}"
                raise ValueError(msg)
            return self

    class TapInstance(m.Entity):
        """Generic tap instance for data extraction."""

        tap_id: Annotated[
            str | None, Field(default=None, description="Unique tap identifier")
        ] = None
        tap_type: Annotated[str, Field(description="Type of the tap")]
        config: Annotated[
            FlextMeltanoModelsSources.TapConfig, Field(description="Tap configuration")
        ]
        adapter: Annotated[
            t.JsonValue | None,
            Field(default=None, description="Tap adapter instance"),
        ] = None
        streams: Sequence[FlextMeltanoModelsInstances.StreamInfo] = Field(
            default_factory=lambda: list[FlextMeltanoModelsInstances.StreamInfo](),
            description="Available streams",
        )
        status: Annotated[
            str,
            Field(default=c.Meltano.StreamStatus.INITIALIZED, description="Tap status"),
        ] = c.Meltano.StreamStatus.INITIALIZED

        @computed_field
        def active_streams(self) -> Sequence[FlextMeltanoModelsInstances.StreamInfo]:
            """Active streams for extraction."""
            return [s for s in self.streams if s.status in c.Meltano.ACTIVE_STATUSES]

        @computed_field
        def stream_count(self) -> int:
            """Number of available streams."""
            return len(self.streams)
