"""FLEXT Meltano models - Instance and stream models."""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated, Self

from flext_cli import m, u
from flext_meltano._models.sources import FlextMeltanoModelsSources
from flext_meltano.constants import FlextMeltanoConstants as c
from flext_meltano.typings import FlextMeltanoTypes as t


class FlextMeltanoModelsInstances:
    """Instance and stream models."""

    class DataSinkDefinition(m.Entity):
        """Generic data sink definition for pipeline operations."""

        sink_name: Annotated[str, u.Field(description="Name of the sink")]
        sink_type: Annotated[str, u.Field(description="Type of the sink")]
        settings: Annotated[
            t.ConfigurationMapping,
            u.Field(description="Sink configuration"),
        ] = u.Field(default_factory=lambda: MappingProxyType({}))
        sink_schema: Annotated[t.JsonMapping, u.Field(description="Sink schema")] = (
            u.Field(default_factory=lambda: MappingProxyType({}))
        )
        status: Annotated[
            str,
            u.Field(
                default=c.Meltano.StreamStatus.INITIALIZED,
                description="Current status",
            ),
        ] = c.Meltano.StreamStatus.INITIALIZED

        @u.computed_field()
        @property
        def config_keys_count(self) -> int:
            """Number of settings keys."""
            return u.count(list(self.settings.keys()))

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
            t.NonEmptyStr,
            u.Field(description="Stream name identifier"),
        ]
        stream_schema: Annotated[
            t.MappingKV[str, t.Scalar | t.ScalarMapping],
            u.Field(description="Stream schema definition"),
        ]
        key_properties: Annotated[
            t.StrSequence,
            u.Field(description="Primary key properties for the stream"),
        ] = u.Field(default_factory=tuple)
        replication_method: Annotated[
            str,
            u.Field(default="FULL_TABLE", description="Replication method"),
        ] = "FULL_TABLE"
        replication_key: Annotated[
            str | None,
            u.Field(default=None, description="Incremental replication field"),
        ] = None
        status: Annotated[
            str,
            u.Field(
                default=c.Meltano.StreamStatus.INITIALIZED,
                description="Stream processing status",
            ),
        ] = c.Meltano.StreamStatus.INITIALIZED
        records_loaded: Annotated[
            t.NonNegativeInt,
            u.Field(default=0, description="Number of records loaded"),
        ] = 0
        batches_processed: Annotated[
            t.NonNegativeInt,
            u.Field(default=0, description="Number of batches processed"),
        ] = 0
        stream_created_at: Annotated[str, u.Field(description="Creation timestamp")]

        @u.computed_field()
        @property
        def average_records_per_batch(self) -> float:
            """Average records per batch."""
            return (
                0.0
                if self.batches_processed == 0
                else self.records_loaded / self.batches_processed
            )

        @u.computed_field()
        @property
        def has_processed_data(self) -> bool:
            """Check if stream has processed data."""
            has: bool = self.records_loaded > 0 or self.batches_processed > 0
            return has

        @u.computed_field()
        @property
        def processing_status(self) -> str:
            """Processing status assessment."""
            if (
                self.status == c.Meltano.StreamStatus.COMPLETED
                and self.records_loaded > 0
            ):
                return str(c.Meltano.StreamStatus.SUCCESS)
            if self.status == c.Meltano.StreamStatus.ERROR:
                return str(c.Meltano.StreamStatus.FAILED)
            if self.records_loaded > 0:
                return str(c.Meltano.StreamStatus.IN_PROGRESS)
            return str(c.Meltano.StreamStatus.PENDING)

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

        tap_id: Annotated[
            str | None,
            u.Field(default=None, description="Unique tap identifier"),
        ] = None
        tap_type: Annotated[str, u.Field(description="Type of the tap")]
        settings: Annotated[
            FlextMeltanoModelsSources.TapConfig,
            u.Field(description="Tap configuration"),
        ]
        adapter: Annotated[
            t.JsonValue | None,
            u.Field(default=None, description="Tap adapter instance"),
        ] = None
        streams: t.SequenceOf[FlextMeltanoModelsInstances.StreamInfo] = u.Field(
            default_factory=tuple,
            description="Available streams",
        )
        status: Annotated[
            str,
            u.Field(
                default=c.Meltano.StreamStatus.INITIALIZED,
                description="Tap status",
            ),
        ] = c.Meltano.StreamStatus.INITIALIZED

        @u.computed_field()
        @property
        def active_streams(
            self,
        ) -> t.SequenceOf[FlextMeltanoModelsInstances.StreamInfo]:
            """Active streams for extraction."""
            return [s for s in self.streams if s.status in c.Meltano.ACTIVE_STATUSES]

        @u.computed_field()
        @property
        def stream_count(self) -> int:
            """Number of available streams."""
            return len(self.streams)
