"""FLEXT Meltano models - Data source and sink instance and settings models."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Annotated, Self

from flext_cli import m, u

from flext_meltano import c, t
from flext_meltano._models.core import FlextMeltanoModelsCore
from flext_meltano._models.sources import FlextMeltanoModelsSources
from flext_meltano._models.sources_params import FlextMeltanoModelsSourcesParams


class FlextMeltanoModelsInstancesData:
    """Data source and sink instance and settings models."""

    class DataSinkConfig(m.Entity):
        """Generic data sink configuration with validation."""

        sink_type: Annotated[str, u.Field(description="Sink type identifier")]
        connection_config: Annotated[
            t.RecursiveContainerMapping,
            u.Field(description="Connection configuration dictionary"),
        ]
        batch_size: Annotated[
            t.BatchSize,
            u.Field(
                default=c.DEFAULT_SIZE, description="Batch size for record processing"
            ),
        ] = c.DEFAULT_SIZE
        max_batches: Annotated[
            t.PositiveInt,
            u.Field(default=c.DEFAULT_SIZE, description="Maximum number of batches"),
        ] = c.DEFAULT_SIZE

        @u.computed_field
        def max_records_capacity(self) -> int:
            """Maximum records capacity."""
            return self.batch_size * self.max_batches

        @u.computed_field
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

        @u.computed_field
        def sink_identifier(self) -> str:
            """Unique sink identifier."""
            return f"{self.sink_type}:batch_{self.batch_size}"

        @u.field_serializer("connection_config")
        def serialize_connection_config(
            self, value: t.RecursiveContainerMapping
        ) -> t.RecursiveContainerMapping:
            """Serialize connection settings with sensitive data protection."""
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

        source_type: Annotated[str, u.Field(description="Type of the data source")]
        settings: Annotated[
            FlextMeltanoModelsSources.DataSourceConfig,
            u.Field(description="Source configuration"),
        ]
        adapter: Annotated[
            t.ContainerValue | None,
            u.Field(default=None, description="Adapter instance"),
        ] = None
        status: Annotated[
            str,
            u.Field(
                default=c.Meltano.StreamStatus.INITIALIZED, description="Current status"
            ),
        ] = c.Meltano.StreamStatus.INITIALIZED
        streams: Annotated[
            Mapping[str, FlextMeltanoModelsSourcesParams.StreamDefinition],
            u.Field(description="Discovered streams"),
        ] = u.Field(default_factory=dict, description="Discovered streams")
        discovered: Annotated[
            bool,
            u.Field(default=False, description="Whether streams have been discovered"),
        ] = False
        metadata: Annotated[
            t.ConfigurationMapping, u.Field(description="Additional metadata")
        ] = u.Field(default_factory=dict, description="Additional metadata")
        source_id: Annotated[str, u.Field(description="Unique source identifier")]

        @u.computed_field
        def active_stream_count(self) -> int:
            """Number of active streams."""
            return len([
                stream
                for stream in self.streams.values()
                if stream.status in c.Meltano.ACTIVE_STATUSES
            ])

        @u.computed_field
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

        @u.computed_field
        def stream_count(self) -> int:
            """Number of discovered streams."""
            return len(self.streams)

        @u.computed_field
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
                msg = "Source type must match between instance and settings"
                raise ValueError(msg)
            if self.discovered and not self.streams:
                msg = "Discovered source must have at least one stream"
                raise ValueError(msg)
            return self

    class DataSinkInstance(m.Entity):
        """Generic data sink instance for pipeline operations."""

        sink_id: Annotated[
            str | None, u.Field(default=None, description="Unique sink identifier")
        ] = None
        sink_type: Annotated[str, u.Field(description="Type of the data sink")]
        settings: FlextMeltanoModelsInstancesData.DataSinkConfig = u.Field(
            description="Sink configuration"
        )
        adapter: Annotated[
            t.ContainerValue | None,
            u.Field(default=None, description="Adapter instance"),
        ] = None
        status: Annotated[
            str,
            u.Field(
                default=c.Meltano.StreamStatus.INITIALIZED, description="Current status"
            ),
        ] = c.Meltano.StreamStatus.INITIALIZED
        batch_size: Annotated[
            t.BatchSize, u.Field(default=1000, description="Batch processing size")
        ] = 1000
        sink_count: Annotated[
            t.NonNegativeInt,
            u.Field(default=0, description="Number of configured sinks"),
        ] = 0

        @u.computed_field
        def is_ready(self) -> bool:
            """Check if sink is ready for processing."""
            return self.status == "configured" and self.adapter is not None
