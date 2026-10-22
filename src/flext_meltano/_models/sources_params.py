"""FLEXT Meltano models - Stream definitions.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, Self

from flext_cli import m

from flext_meltano import c, t


class FlextMeltanoModelsSourcesParams:
    """Stream definition models."""

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

        @m.field_serializer("stream_schema")
        @staticmethod
        def serialize_stream_schema(
            value: t.FlatContainerMapping,
        ) -> t.FlatContainerMapping:
            """Normalize stream schema structure.

            Args:
                value: The stream schema mapping to normalize.

            Returns:
                The resulting ``t.FlatContainerMapping``.

            """
            result: t.JsonDict = dict(value)
            if "properties" not in result:
                empty: t.JsonDict = {}
                result["properties"] = empty
            if "type" not in result:
                result["type"] = "object"
            return result

        @m.model_validator(mode="after")
        def validate_stream_definition(self) -> Self:
            """Validate stream definition consistency.

            Returns:
                The resulting ``Self``.

            Raises:
                ValueError: If the stream schema has no properties, or the status is
                    not one of the valid statuses.

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


__all__: list[str] = ["FlextMeltanoModelsSourcesParams"]
