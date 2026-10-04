"""FLEXT Meltano models - Run parameters and stream definitions.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, Self

from flext_cli import m, u

from flext_meltano import c, t


class FlextMeltanoModelsSourcesParams:
    """Run parameters and stream definition models."""

    class DbtRunParams(m.Entity):
        """Generic parameters for dbt run operations."""

        project_dir: Annotated[str, m.Field(description="dbt project directory")]
        models: Annotated[
            str | None,
            m.Field(default=None, description="Models to run"),
        ] = None
        select: Annotated[
            str | None,
            m.Field(default=None, description="Selection syntax"),
        ] = None
        exclude: Annotated[
            str | None,
            m.Field(default=None, description="Exclusion syntax"),
        ] = None
        full_refresh: Annotated[
            bool,
            m.Field(default=False, description="Full refresh flag"),
        ] = False
        vars: Annotated[
            t.ConfigurationMapping | None,
            m.Field(default=None, description="dbt variables"),
        ] = None

    class TapRunParams(m.Entity):
        """Generic parameters for tap run operations."""

        tap_name: Annotated[str, m.Field(description="Name of the tap to run")]
        discover: Annotated[
            bool,
            m.Field(default=False, description="Run tap in discover mode"),
        ] = False
        config_file: Annotated[
            str | None,
            m.Field(default=None, description="Path to tap configuration file"),
        ] = None
        catalog_file: Annotated[
            str | None,
            m.Field(default=None, description="Path to Singer catalog file"),
        ] = None
        state_file: Annotated[
            str | None,
            m.Field(default=None, description="Path to Singer state file"),
        ] = None
        properties_file: Annotated[
            str | None,
            m.Field(default=None, description="Path to Singer properties file"),
        ] = None

    class TargetRunParams(m.Entity):
        """Generic parameters for target run operations."""

        target_name: Annotated[str, m.Field(description="Name of the target to run")]
        config_file: Annotated[
            str | None,
            m.Field(default=None, description="Path to target configuration file"),
        ] = None
        input_file: Annotated[
            str | None,
            m.Field(default=None, description="Input file path for target loading"),
        ] = None
        batch_size: Annotated[
            t.BatchSize | None,
            m.Field(default=None, description="Batch size for target operations"),
        ] = None

    class StreamDefinition(m.Entity):
        """Generic stream definition for data pipeline operations."""

        stream_name: Annotated[str, m.Field(description="Name of the stream")]
        stream_schema: Annotated[
            t.FlatContainerMapping,
            m.Field(description="JSON schema for the stream"),
        ]
        source_type: Annotated[
            str,
            m.Field(description="Type of source this stream belongs to"),
        ]
        status: Annotated[
            str,
            m.Field(
                default=c.Meltano.StreamStatus.DISCOVERED,
                description="Current status of the stream",
            ),
        ] = c.Meltano.StreamStatus.DISCOVERED
        records_extracted: Annotated[
            t.NonNegativeInt,
            m.Field(default=0, description="Number of records extracted"),
        ] = 0

        @m.computed_field
        def has_data(self) -> bool:
            """Check if stream has extracted data.

            Returns:
                The resulting ``bool``.
            """
            records_extracted: int = self.records_extracted
            return records_extracted > 0

        @m.computed_field
        def is_active(self) -> bool:
            """Check if stream is active.

            Returns:
                The resulting ``bool``.
            """
            return self.status in c.Meltano.ACTIVE_STATUSES

        @m.computed_field
        def schema_properties_count(self) -> int:
            """Number of schema properties.

            Returns:
                The resulting ``int``.
            """
            properties = self.stream_schema.get("properties", {})
            match properties:
                case dict():
                    return len(properties)
                case _:
                    return 0

        @staticmethod
        @u.field_serializer("stream_schema")
        def serialize_stream_schema(
            value: t.FlatContainerMapping,
        ) -> t.FlatContainerMapping:
            """Normalize stream schema structure.

            Returns:
                The resulting ``t.FlatContainerMapping``.
            """
            result: t.JsonDict = dict(value)
            if "properties" not in result:
                empty: t.JsonDict = {}
                result["properties"] = empty
            if "type" not in result:
                result["type"] = "t.NormalizedValue"
            return result

        @u.model_validator(mode="after")
        def validate_stream_definition(self) -> Self:
            """Validate stream definition consistency.

            Returns:
                The resulting ``Self``.

            Raises:
                ValueError: If Stream schema must contain properties; or if Status must
                    be one of.
            """
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
