"""FLEXT Meltano models - Run parameters and stream definitions."""

from __future__ import annotations

from typing import Annotated, Self

from flext_cli import m
from pydantic import Field, computed_field, field_serializer, model_validator

from flext_meltano import c, t


class FlextMeltanoModelsSourcesParams:
    """Run parameters and stream definition models."""

    class DbtRunParams(m.Entity):
        """Generic parameters for dbt run operations."""

        project_dir: Annotated[str, Field(description="dbt project directory")]
        models: Annotated[
            str | None, Field(default=None, description="Models to run")
        ] = None
        select: Annotated[
            str | None, Field(default=None, description="Selection syntax")
        ] = None
        exclude: Annotated[
            str | None, Field(default=None, description="Exclusion syntax")
        ] = None
        full_refresh: Annotated[
            bool, Field(default=False, description="Full refresh flag")
        ] = False
        vars: Annotated[
            t.ConfigurationMapping | None,
            Field(default=None, description="dbt variables"),
        ] = None

    class TapRunParams(m.Entity):
        """Generic parameters for tap run operations."""

        tap_name: Annotated[str, Field(description="Name of the tap to run")]
        discover: Annotated[
            bool, Field(default=False, description="Run tap in discover mode")
        ] = False
        config_file: Annotated[
            str | None,
            Field(default=None, description="Path to tap configuration file"),
        ] = None
        catalog_file: Annotated[
            str | None, Field(default=None, description="Path to Singer catalog file")
        ] = None
        state_file: Annotated[
            str | None, Field(default=None, description="Path to Singer state file")
        ] = None
        properties_file: Annotated[
            str | None,
            Field(default=None, description="Path to Singer properties file"),
        ] = None

    class TargetRunParams(m.Entity):
        """Generic parameters for target run operations."""

        target_name: Annotated[str, Field(description="Name of the target to run")]
        config_file: Annotated[
            str | None,
            Field(default=None, description="Path to target configuration file"),
        ] = None
        input_file: Annotated[
            str | None,
            Field(default=None, description="Input file path for target loading"),
        ] = None
        batch_size: Annotated[
            t.BatchSize | None,
            Field(default=None, description="Batch size for target operations"),
        ] = None

    class StreamDefinition(m.Entity):
        """Generic stream definition for data pipeline operations."""

        stream_name: Annotated[str, Field(description="Name of the stream")]
        stream_schema: Annotated[
            t.ContainerMapping, Field(description="JSON schema for the stream")
        ]
        source_type: Annotated[
            str, Field(description="Type of source this stream belongs to")
        ]
        status: Annotated[
            str,
            Field(
                default=c.Meltano.StreamStatus.DISCOVERED,
                description="Current status of the stream",
            ),
        ] = c.Meltano.StreamStatus.DISCOVERED
        records_extracted: Annotated[
            t.NonNegativeInt,
            Field(default=0, description="Number of records extracted"),
        ] = 0

        @computed_field
        def has_data(self) -> bool:
            """Check if stream has extracted data."""
            return self.records_extracted > 0

        @computed_field
        def is_active(self) -> bool:
            """Check if stream is active."""
            return self.status in c.Meltano.ACTIVE_STATUSES

        @computed_field
        def schema_properties_count(self) -> int:
            """Number of schema properties."""
            properties = self.stream_schema.get("properties", {})
            match properties:
                case dict():
                    return len(properties)
                case _:
                    return 0

        @field_serializer("stream_schema")
        def serialize_stream_schema(
            self, value: t.ContainerMapping
        ) -> t.ContainerMapping:
            """Normalize stream schema structure."""
            result: t.MutableContainerMapping = dict(value)
            if "properties" not in result:
                empty: t.MutableContainerMapping = {}
                result["properties"] = empty
            if "type" not in result:
                result["type"] = "t.NormalizedValue"
            return result

        @model_validator(mode="after")
        def validate_stream_definition(self) -> Self:
            """Validate stream definition consistency."""
            if "properties" not in self.stream_schema:
                msg = "Stream schema must contain properties"
                raise ValueError(msg)
            valid_statuses = c.Meltano.ACTIVE_STATUSES | {
                c.Meltano.StreamStatus.COMPLETED,
                c.Meltano.StreamStatus.ERROR,
            }
            if self.status not in valid_statuses:
                msg = f"Status must be one of: {', '.join(valid_statuses)}"
                raise ValueError(msg)
            return self
