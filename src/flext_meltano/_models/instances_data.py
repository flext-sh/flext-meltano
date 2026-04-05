"""FLEXT Meltano models - Data source and sink instance and config models."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Annotated, Self

from flext_cli import FlextCliModels, u
from pydantic import Field, computed_field, field_serializer, model_validator

from flext_meltano import (
    FlextMeltanoModelsCore,
    FlextMeltanoModelsSources,
    FlextMeltanoModelsSourcesParams,
    c,
    t,
)

_INITIALIZED = c.Meltano.Enums.StreamStatus.INITIALIZED


class FlextMeltanoModelsInstancesData:
    """Data source and sink instance and config models."""

    class DataSinkConfig(FlextCliModels.Entity):
        """Generic data sink configuration with validation."""

        sink_type: Annotated[str, Field(description="Sink type identifier")]
        connection_config: Annotated[
            t.ContainerMapping, Field(description="Connection configuration dictionary")
        ]
        batch_size: Annotated[
            t.BatchSize,
            Field(
                default=c.DEFAULT_SIZE,
                description="Batch size for record processing",
            ),
        ] = c.DEFAULT_SIZE
        max_batches: Annotated[
            t.PositiveInt,
            Field(
                default=c.DEFAULT_SIZE,
                description="Maximum number of batches",
            ),
        ] = c.DEFAULT_SIZE

        @computed_field
        def max_records_capacity(self) -> int:
            """Maximum records capacity."""
            return self.batch_size * self.max_batches

        @computed_field
        def processing_efficiency(self) -> str:
            """Processing efficiency assessment."""
            if (
                self.batch_size
                >= c.Meltano.ModelValidation.EXECUTION_HIGH_PERFORMANCE_THRESHOLD
            ):
                return "high"
            if (
                self.batch_size
                >= c.Meltano.ModelValidation.EXECUTION_GOOD_PERFORMANCE_THRESHOLD
            ):
                return "medium"
            return "low"

        @computed_field
        def sink_identifier(self) -> str:
            """Unique sink identifier."""
            return f"{self.sink_type}:batch_{self.batch_size}"

        @field_serializer("connection_config")
        def serialize_connection_config(
            self, value: t.ContainerMapping
        ) -> t.ContainerMapping:
            """Serialize connection config with sensitive data protection."""
            return FlextMeltanoModelsCore.protect_sensitive_config(value)

        @model_validator(mode="after")
        def validate_sink_config(self) -> Self:
            """Validate sink configuration consistency."""
            if not self.sink_type or not self.sink_type.strip():
                msg = "Sink type must be non-empty string"
                raise ValueError(msg)
            max_reasonable = c.Meltano.Logging.MELTANO_PERFORMANCE_THRESHOLD_CRITICAL
            if self.batch_size > max_reasonable:
                msg = f"Batch size too large (max {max_reasonable})"
                raise ValueError(msg)
            return self

    class DataSourceInstance(FlextCliModels.Entity):
        """Generic data source instance for pipeline operations."""

        source_type: Annotated[str, Field(description="Type of the data source")]
        config: Annotated[
            FlextMeltanoModelsSources.DataSourceConfig,
            Field(description="Source configuration"),
        ]
        adapter: Annotated[
            t.ContainerValue | None, Field(default=None, description="Adapter instance")
        ] = None
        status: Annotated[
            str,
            Field(default=_INITIALIZED, description="Current status"),
        ] = _INITIALIZED
        streams: Annotated[
            Mapping[str, FlextMeltanoModelsSourcesParams.StreamDefinition],
            Field(description="Discovered streams"),
        ] = Field(default_factory=dict, description="Discovered streams")
        discovered: Annotated[
            bool,
            Field(default=False, description="Whether streams have been discovered"),
        ] = False
        metadata: Annotated[
            t.ConfigurationMapping, Field(description="Additional metadata")
        ] = Field(default_factory=dict, description="Additional metadata")
        source_id: Annotated[str, Field(description="Unique source identifier")]

        @computed_field
        def active_stream_count(self) -> int:
            """Number of active streams."""
            return len([
                stream
                for stream in self.streams.values()
                if stream.status in c.Meltano.Enums.ACTIVE_STATUSES
            ])

        @computed_field
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

        @computed_field
        def stream_count(self) -> int:
            """Number of discovered streams."""
            return len(self.streams)

        @computed_field
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

        @model_validator(mode="after")
        def validate_source_instance(self) -> Self:
            """Validate source instance consistency."""
            if self.config.source_type != self.source_type:
                msg = "Source type must match between instance and config"
                raise ValueError(msg)
            if self.discovered and not self.streams:
                msg = "Discovered source must have at least one stream"
                raise ValueError(msg)
            return self

    class DataSinkInstance(FlextCliModels.Entity):
        """Generic data sink instance for pipeline operations."""

        sink_id: Annotated[
            str | None, Field(default=None, description="Unique sink identifier")
        ] = None
        sink_type: Annotated[str, Field(description="Type of the data sink")]
        config: FlextMeltanoModelsInstancesData.DataSinkConfig = Field(
            description="Sink configuration"
        )
        adapter: Annotated[
            t.ContainerValue | None, Field(default=None, description="Adapter instance")
        ] = None
        status: Annotated[
            str,
            Field(default=_INITIALIZED, description="Current status"),
        ] = _INITIALIZED
        batch_size: Annotated[
            t.BatchSize, Field(default=1000, description="Batch processing size")
        ] = 1000
        sink_count: Annotated[
            t.NonNegativeInt, Field(default=0, description="Number of configured sinks")
        ] = 0

        @computed_field
        def is_ready(self) -> bool:
            """Check if sink is ready for processing."""
            return self.status == "configured" and self.adapter is not None
