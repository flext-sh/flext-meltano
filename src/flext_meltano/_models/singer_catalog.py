"""FLEXT Meltano models - Singer catalog and pipeline settings models."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, Annotated

from flext_cli import m, u
from flext_meltano.constants import FlextMeltanoConstants as c

if TYPE_CHECKING:
    from flext_meltano.typings import FlextMeltanoTypes as t


class FlextMeltanoModelsSingerCatalog:
    """Singer catalog, pipeline settings, and sync result models."""

    class SingerCatalogMetadata(m.ArbitraryTypesModel):
        """Singer catalog metadata block model."""

        breadcrumb: t.StrSequence = u.Field(
            default_factory=tuple,
            description="Singer metadata breadcrumb path segments",
        )
        metadata: t.JsonMapping = u.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Singer metadata payload associated with the breadcrumb",
        )

    class SingerCatalogEntry(m.ArbitraryTypesModel):
        """Singer catalog stream entry model."""

        tap_stream_id: Annotated[str, u.Field(description="Tap stream identifier")]
        stream: Annotated[str, u.Field(description="Singer stream name")]
        schema_definition: Annotated[
            t.JsonMapping,
            u.Field(
                alias=c.Meltano.SchemaKey.SCHEMA,
                serialization_alias=c.Meltano.SchemaKey.SCHEMA,
                validation_alias=c.Meltano.SchemaKey.SCHEMA,
                description="Singer stream schema payload",
            ),
        ]
        metadata: t.SequenceOf[
            FlextMeltanoModelsSingerCatalog.SingerCatalogMetadata
        ] = u.Field(
            default_factory=list[FlextMeltanoModelsSingerCatalog.SingerCatalogMetadata],
            description="Singer stream metadata blocks",
        )
        key_properties: t.StrSequence = u.Field(
            default_factory=tuple,
            description="Singer key property names for the stream",
        )
        replication_key: Annotated[
            str | None,
            u.Field(
                default=None,
                description="Column used for incremental replication",
            ),
        ] = None
        replication_method: Annotated[
            c.Meltano.SingerReplicationMethod | None,
            u.Field(default=None, description="Replication method for this stream"),
        ] = None
        is_view: Annotated[
            bool | None,
            u.Field(default=None, description="Whether this stream is a database view"),
        ] = None
        table_name: Annotated[
            str | None,
            u.Field(default=None, description="Source table name"),
        ] = None
        database_name: Annotated[
            str | None,
            u.Field(default=None, description="Source database name"),
        ] = None
        row_count: Annotated[
            int | None,
            u.Field(default=None, description="Estimated row count from source"),
        ] = None

    class SingerCatalog(m.ArbitraryTypesModel):
        """Singer catalog response model."""

        type: Annotated[
            c.Meltano.SingerMessageType,
            u.Field(
                default=c.Meltano.SingerMessageType.CATALOG,
                description="Singer catalog message discriminator",
            ),
        ] = c.Meltano.SingerMessageType.CATALOG
        streams: t.SequenceOf[FlextMeltanoModelsSingerCatalog.SingerCatalogEntry] = (
            u.Field(
                default_factory=list[
                    FlextMeltanoModelsSingerCatalog.SingerCatalogEntry
                ],
                description="Singer catalog stream entries",
            )
        )
