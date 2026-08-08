"""FLEXT Meltano models - Instance and stream models."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Annotated, Self

from flext_cli import m, u

from flext_meltano import c, t
from flext_meltano._models.sources import FlextMeltanoModelsSources


class FlextMeltanoModelsInstances:
    """Instance and stream models."""

    class DataSinkDefinition(m.Entity):
        """Generic data sink definition for pipeline operations."""

        sink_name: Annotated[str, m.Field(description="Name of the sink")]
        sink_type: Annotated[str, m.Field(description="Type of the sink")]
        config: Annotated[
            t.ConfigurationMapping, m.Field(description="Sink configuration")
        ] = m.Field(default_factory=dict, description="Sink configuration")
        sink_schema: Annotated[
            t.FlatContainerMapping, m.Field(description="Sink schema")
        ] = m.Field(default_factory=dict, description="Sink schema")
        settings: Annotated[
            t.FlatContainerMapping, m.Field(description="Sink settings")
        ] = m.Field(default_factory=dict, description="Sink settings")
        status: Annotated[
            str,
            m.Field(
                default=c.Meltano.StreamStatus.INITIALIZED, description="Current status"
            ),
        ] = c.Meltano.StreamStatus.INITIALIZED

        @m.computed_field
        def config_keys_count(self) -> int:
            """Number of config keys."""
            return u.count(list(self.config.keys()))

        @u.model_validator(mode="after")
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
            t.NonEmptyStr, m.Field(description="Stream name identifier")
        ]
        stream_schema: Annotated[
            Mapping[str, t.Scalar | t.ScalarMapping],
            m.Field(description="Stream schema definition"),
        ]
        key_properties: Annotated[
            t.StrSequence, m.Field(description="Primary key properties for the stream")
        ] = m.Field(default_factory=list, description="Primary key properties")
        replication_method: Annotated[
            str, m.Field(default="FULL_TABLE", description="Replication method")
        ] = "FULL_TABLE"
        replication_key: Annotated[
            str | None,
            m.Field(default=None, description="Incremental replication field"),
        ] = None
        status: Annotated[
            str,
            m.Field(
                default=c.Meltano.StreamStatus.INITIALIZED,
                description="Stream processing status",
            ),
        ] = c.Meltano.StreamStatus.INITIALIZED
        records_loaded: Annotated[
            t.NonNegativeInt, m.Field(default=0, description="Number of records loaded")
        ] = 0
        batches_processed: Annotated[
            t.NonNegativeInt,
            m.Field(default=0, description="Number of batches processed"),
        ] = 0
        stream_created_at: Annotated[str, m.Field(description="Creation timestamp")]

        @m.computed_field
        def average_records_per_batch(self) -> float:
            """Average records per batch."""
            return (
                0.0
                if self.batches_processed == 0
                else self.records_loaded / self.batches_processed
            )

        @m.computed_field
        def has_processed_data(self) -> bool:
            """Check if stream has processed data."""
            records_loaded: int = self.records_loaded
            batches_processed: int = self.batches_processed
            return records_loaded > 0 or batches_processed > 0

        @m.computed_field
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

        @u.model_validator(mode="after")
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

        model_config = m.ConfigDict(populate_by_name=True)

        tap_id: Annotated[
            str | None, m.Field(default=None, description="Unique tap identifier")
        ] = None
        tap_type: Annotated[str, m.Field(description="Type of the tap")]
        settings: Annotated[
            FlextMeltanoModelsSources.TapConfig,
            m.Field(alias="config", description="Tap configuration"),
        ]
        adapter: Annotated[
            t.JsonValue | None,
            m.Field(default=None, description="Tap adapter instance"),
        ] = None
        streams: Sequence[FlextMeltanoModelsInstances.StreamInfo] = m.Field(
            default_factory=list, description="Available streams"
        )
        status: Annotated[
            str,
            m.Field(
                default=c.Meltano.StreamStatus.INITIALIZED, description="Tap status"
            ),
        ] = c.Meltano.StreamStatus.INITIALIZED

        @m.computed_field
        def active_streams(self) -> Sequence[FlextMeltanoModelsInstances.StreamInfo]:
            """Active streams for extraction."""
            return [s for s in self.streams if s.status in c.Meltano.ACTIVE_STATUSES]

        @m.computed_field
        def stream_count(self) -> int:
            """Number of available streams."""
            return len(self.streams)
