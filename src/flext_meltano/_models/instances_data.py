"""FLEXT Meltano models - Data source and sink instance and config models."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from types import MappingProxyType
from typing import Annotated, Self

from flext_cli import m, u

from flext_meltano import c, t
from flext_meltano._models.core import FlextMeltanoModelsCore
from flext_meltano._models.sources import FlextMeltanoModelsSources
from flext_meltano._models.sources_params import FlextMeltanoModelsSourcesParams


class FlextMeltanoModelsInstancesData:
    """Data source and sink instance and config models."""

    class DataSinkConfig(m.Entity):
        """Generic data sink configuration with validation."""

        sink_type: Annotated[str, m.Field(description="Sink type identifier")]
        connection_config: Annotated[
            t.FlatContainerMapping,
            m.Field(description="Connection configuration dictionary"),
        ]
        batch_size: Annotated[
            t.BatchSize,
            m.Field(
                default=c.DEFAULT_SIZE, description="Batch size for record processing"
            ),
        ] = c.DEFAULT_SIZE
        max_batches: Annotated[
            t.PositiveInt,
            m.Field(default=c.DEFAULT_SIZE, description="Maximum number of batches"),
        ] = c.DEFAULT_SIZE

        @m.computed_field
        def max_records_capacity(self) -> int:
            """Maximum records capacity."""
            batch_size: int = self.batch_size
            max_batches: int = self.max_batches
            return batch_size * max_batches

        @m.computed_field
        def processing_efficiency(self) -> str:
            """Processing efficiency assessment."""
            if (
                self.batch_size
                >= c.Meltano.VALIDATION_EXECUTION_HIGH_PERFORMANCE_THRESHOLD
            ):
                return "high"
            if (
                self.batch_size
                >= c.Meltano.VALIDATION_EXECUTION_GOOD_PERFORMANCE_THRESHOLD
            ):
                return "medium"
            return "low"

        @m.computed_field
        def sink_identifier(self) -> str:
            """Unique sink identifier."""
            return f"{self.sink_type}:batch_{self.batch_size}"

        @u.field_serializer("connection_config")
        def serialize_connection_config(
            self, value: t.FlatContainerMapping
        ) -> t.FlatContainerMapping:
            """Serialize connection config with sensitive data protection."""
            return FlextMeltanoModelsCore.protect_sensitive_config(value)

        @u.model_validator(mode="after")
        def validate_sink_config(self) -> Self:
            """Validate sink configuration consistency."""
            if not self.sink_type or not self.sink_type.strip():
                msg = "Sink type must be non-empty string"
                raise ValueError(msg)
            threshold = c.Meltano.LOGGING_MELTANO_PERFORMANCE_THRESHOLD_CRITICAL
            if self.batch_size > threshold:
                msg = f"Batch size too large (max {threshold})"
                raise ValueError(msg)
            return self

    class DataSourceInstance(m.Entity):
        """Generic data source instance for pipeline operations."""

        model_config = m.ConfigDict(populate_by_name=True)

        source_type: Annotated[str, m.Field(description="Type of the data source")]
        settings: Annotated[
            FlextMeltanoModelsSources.DataSourceConfig,
            m.Field(alias="config", description="Source configuration"),
        ]
        adapter: Annotated[
            t.JsonValue | None, m.Field(default=None, description="Adapter instance")
        ] = None
        status: Annotated[
            str,
            m.Field(
                default=c.Meltano.StreamStatus.INITIALIZED, description="Current status"
            ),
        ] = c.Meltano.StreamStatus.INITIALIZED
        streams: Annotated[
            Mapping[str, FlextMeltanoModelsSourcesParams.StreamDefinition],
            m.Field(description="Discovered streams"),
        ] = m.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Discovered streams",
        )
        discovered: Annotated[
            bool,
            m.Field(default=False, description="Whether streams have been discovered"),
        ] = False
        metadata: Annotated[
            t.ConfigurationMapping, m.Field(description="Additional metadata")
        ] = m.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Additional metadata",
        )
        source_id: Annotated[str, m.Field(description="Unique source identifier")]

        @m.field_validator("streams", mode="after")
        @classmethod
        def freeze_streams(
            cls, value: Mapping[str, FlextMeltanoModelsSourcesParams.StreamDefinition]
        ) -> Mapping[str, FlextMeltanoModelsSourcesParams.StreamDefinition]:
            """Expose discovered streams as a read-only mapping."""
            return MappingProxyType(dict(value))

        @m.field_validator("metadata", mode="after")
        @classmethod
        def freeze_metadata(
            cls, value: t.ConfigurationMapping
        ) -> t.ConfigurationMapping:
            """Expose source metadata as a read-only mapping."""
            return MappingProxyType(dict(value))

        @m.computed_field
        def active_stream_count(self) -> int:
            """Number of active streams."""
            return len([
                stream
                for stream in self.streams.values()
                if stream.status in c.Meltano.ACTIVE_STATUSES
            ])

        @m.computed_field
        def is_ready_for_extraction(self) -> bool:
            """Check if source is ready for data extraction."""
            streams_list: Sequence[FlextMeltanoModelsSourcesParams.StreamDefinition] = (
                list(self.streams.values())
            )
            return (
                self.discovered
                and u.count(streams_list) > 0
                and self.status == "configured"
            )

        @m.computed_field
        def stream_count(self) -> int:
            """Number of discovered streams."""
            return len(self.streams)

        @m.computed_field
        def total_records_extracted(self) -> int:
            """Total records extracted across all streams."""
            streams_list: Sequence[FlextMeltanoModelsSourcesParams.StreamDefinition] = (
                list(self.streams.values())
            )
            result = u.agg(streams_list, "records_extracted", fn=sum)
            match result:
                case int():
                    return result
                case _:
                    return 0

        @u.model_validator(mode="after")
        def validate_source_instance(self) -> Self:
            """Validate source instance consistency."""
            if self.settings.source_type != self.source_type:
                msg = "Source type must match between instance and config"
                raise ValueError(msg)
            if self.discovered and not self.streams:
                msg = "Discovered source must have at least one stream"
                raise ValueError(msg)
            return self

    class DataSinkInstance(m.Entity):
        """Generic data sink instance for pipeline operations."""

        model_config = m.ConfigDict(populate_by_name=True)

        sink_id: Annotated[
            str | None, m.Field(default=None, description="Unique sink identifier")
        ] = None
        sink_type: Annotated[str, m.Field(description="Type of the data sink")]
        settings: Annotated[
            FlextMeltanoModelsInstancesData.DataSinkConfig,
            m.Field(alias="config", description="Sink configuration"),
        ]
        adapter: Annotated[
            t.JsonValue | None, m.Field(default=None, description="Adapter instance")
        ] = None
        status: Annotated[
            str,
            m.Field(
                default=c.Meltano.StreamStatus.INITIALIZED, description="Current status"
            ),
        ] = c.Meltano.StreamStatus.INITIALIZED
        batch_size: Annotated[
            t.BatchSize, m.Field(default=1000, description="Batch processing size")
        ] = 1000
        sink_count: Annotated[
            t.NonNegativeInt,
            m.Field(default=0, description="Number of configured sinks"),
        ] = 0

        @m.computed_field
        def is_ready(self) -> bool:
            """Check if sink is ready for processing."""
            return self.status == "configured" and self.adapter is not None
