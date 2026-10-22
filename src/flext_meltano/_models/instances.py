"""FLEXT Meltano models - Instance and stream models.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, Self

from flext_cli import m

from flext_meltano import c, t
from flext_meltano._models.sources import FlextMeltanoModelsSources


class FlextMeltanoModelsInstances:
    """Instance and stream models."""

    class StreamInfo(m.Entity):
        """Generic stream information for data pipeline operations."""

        stream_name: Annotated[
            t.NonEmptyStr,
            m.Field(description="Stream name identifier"),
        ]
        stream_schema: Annotated[
            Mapping[str, t.Scalar | t.ScalarMapping],
            m.Field(description="Stream schema definition"),
        ]
        key_properties: Annotated[
            t.StrTuple,
            m.Field(description="Primary key properties for the stream"),
        ] = m.Field(
            default_factory=tuple[str, ...],
            description="Primary key properties",
        )
        replication_method: Annotated[
            str,
            m.Field(default="FULL_TABLE", description="Replication method"),
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
            t.NonNegativeInt,
            m.Field(default=0, description="Number of records loaded"),
        ] = 0
        batches_processed: Annotated[
            t.NonNegativeInt,
            m.Field(default=0, description="Number of batches processed"),
        ] = 0
        stream_created_at: Annotated[str, m.Field(description="Creation timestamp")]

        @m.model_validator(mode="after")
        def validate_stream_info(self) -> Self:
            """Validate stream information consistency.

            Returns:
                The resulting ``Self``.

            Raises:
                ValueError: If records were loaded without processed batches, or the
                    status is not one of the valid statuses.

            """
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
            str | None,
            m.Field(default=None, description="Unique tap identifier"),
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
        # Why: the parameterized factory cannot reference the sibling nested
        # class before the namespace body finishes executing; the assigned
        # empty tuple keeps the same default with full checker visibility.
        streams: Annotated[
            t.VariadicTuple[FlextMeltanoModelsInstances.StreamInfo],
            m.Field(description="Available streams"),
        ] = ()
        status: Annotated[
            str,
            m.Field(
                default=c.Meltano.StreamStatus.INITIALIZED,
                description="Tap status",
            ),
        ] = c.Meltano.StreamStatus.INITIALIZED


__all__: list[str] = ["FlextMeltanoModelsInstances"]
