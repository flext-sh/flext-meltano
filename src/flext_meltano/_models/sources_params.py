"""FLEXT Meltano models - Run parameters and stream definitions."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, Self

from flext_cli import m, u
from flext_meltano import FlextMeltanoConstants as c, FlextMeltanoTypes as t


class FlextMeltanoModelsSourcesParams:
    """Run parameters and stream definition models."""

    class TapRunParams(m.Entity):
        """Generic parameters for tap run operations."""

        tap_name: Annotated[str, u.Field(description="Name of the tap to run")]
        discover: Annotated[
            bool,
            u.Field(default=False, description="Run tap in discover mode"),
        ] = False
        config_file: Annotated[
            str | None,
            u.Field(default=None, description="Path to tap configuration file"),
        ] = None
        catalog_file: Annotated[
            str | None,
            u.Field(default=None, description="Path to Singer catalog file"),
        ] = None
        state_file: Annotated[
            str | None,
            u.Field(default=None, description="Path to Singer state file"),
        ] = None
        properties_file: Annotated[
            str | None,
            u.Field(default=None, description="Path to Singer properties file"),
        ] = None

    class StreamDefinition(m.Entity):
        """Generic stream definition for data pipeline operations."""

        stream_name: Annotated[str, u.Field(description="Name of the stream")]
        stream_schema: Annotated[
            t.JsonMapping,
            u.Field(description="JSON schema for the stream"),
        ]
        source_type: Annotated[
            str,
            u.Field(description="Type of source this stream belongs to"),
        ]
        status: Annotated[
            str,
            u.Field(
                default=c.Meltano.StreamStatus.DISCOVERED,
                description="Current status of the stream",
            ),
        ] = c.Meltano.StreamStatus.DISCOVERED
        records_extracted: Annotated[
            t.NonNegativeInt,
            u.Field(default=0, description="Number of records extracted"),
        ] = 0

        @u.computed_field()
        @property
        def has_data(self) -> bool:
            """Check if stream has extracted data."""
            has: bool = self.records_extracted > 0
            return has

        @u.computed_field()
        @property
        def is_active(self) -> bool:
            """Check if stream is active."""
            return self.status in c.Meltano.ACTIVE_STATUSES

        @u.computed_field()
        @property
        def schema_properties_count(self) -> int:
            """Number of schema properties."""
            properties = self.stream_schema[c.Meltano.SchemaKey.PROPERTIES]
            return len(properties) if isinstance(properties, Mapping) else 0

        @u.field_validator("stream_schema", mode="before")
        @classmethod
        def normalize_stream_schema(
            cls,
            value: t.Meltano.ValidatorInput,
        ) -> t.JsonMapping:
            """Normalize stream schema once at model boundary."""
            schema = t.json_dict_adapter().validate_python(value)
            properties_raw = schema.get(c.Meltano.SchemaKey.PROPERTIES, {})
            properties = (
                t.json_dict_adapter().validate_python(properties_raw)
                if isinstance(properties_raw, Mapping)
                else {}
            )
            return {
                **schema,
                c.Meltano.SchemaKey.PROPERTIES: properties,
                c.Meltano.SchemaKey.TYPE: schema.get(
                    c.Meltano.SchemaKey.TYPE,
                    c.Meltano.SchemaKey.OBJECT,
                ),
            }

        @u.model_validator(mode="after")
        def validate_stream_definition(self) -> Self:
            """Validate stream definition consistency."""
            if c.Meltano.SchemaKey.PROPERTIES not in self.stream_schema:
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

    class StreamSpec(m.BaseModel):
        """Declarative Singer stream contract supplied by a consumer tap.

        Pure data: the consumer declares each stream's identity, JSON schema and
        keys; ``flext-meltano`` builds the real Singer stream and delegates record
        fetching to the consumer's ``p.Meltano.RecordFetcher``. Consumers never
        import ``singer_sdk``.
        """

        name: Annotated[str, u.Field(description="Singer stream identifier")]
        json_schema: Annotated[
            t.JsonMapping,
            u.Field(description="Singer stream JSON schema"),
        ]
        primary_keys: Annotated[
            t.StrSequence,
            u.Field(default=(), description="Record primary key properties"),
        ] = ()
        replication_key: Annotated[
            str | None,
            u.Field(default=None, description="Incremental replication key"),
        ] = None

    class TapSpec(m.BaseModel):
        """Declarative Singer tap contract supplied by a consumer tap.

        Bundles the tap identity, its Singer ``config_jsonschema`` and the ordered
        set of ``StreamSpec`` streams. ``flext-meltano`` turns this into a real
        ``singer_sdk`` tap with a working flat Singer CLI.
        """

        tap_name: Annotated[str, u.Field(description="Canonical Singer tap name")]
        config_jsonschema: Annotated[
            t.JsonMapping,
            u.Field(description="Singer tap config JSON schema"),
        ]
        streams: Annotated[
            t.SequenceOf[FlextMeltanoModelsSourcesParams.StreamSpec],
            u.Field(description="Declarative stream specs for this tap"),
        ]

    class FetchRequest(m.BaseModel):
        """Typed transport from ``flext-meltano`` to a consumer record fetcher.

        Standardized so every ``flext-(tap|target|dbt)-*`` consumer receives one
        model at the boundary instead of loose args — the config is unpacked once
        by ``flext-meltano`` and passed through without further round trips.
        """

        stream_name: Annotated[str, u.Field(description="Stream being fetched")]
        config: Annotated[
            t.JsonMapping,
            u.Field(description="Validated tap runtime config (settings transport)"),
        ]

    class FetchResult(m.BaseModel):
        """Typed transport of fetched records back to ``flext-meltano``.

        Records stay in the Singer-native ``JsonMapping`` shape (the wire format)
        so they flow straight to output with no dump/revalidate round trip.
        """

        records: Annotated[
            t.SequenceOf[t.JsonMapping],
            u.Field(default=(), description="Records for the requested stream"),
        ] = ()
