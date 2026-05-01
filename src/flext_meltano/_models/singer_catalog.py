"""FLEXT Meltano models - Singer catalog and pipeline settings models."""

from __future__ import annotations

from pathlib import Path
from types import MappingProxyType
from typing import Annotated

from flext_cli import m, u

from flext_meltano import c, t


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
            default_factory=lambda: list[
                FlextMeltanoModelsSingerCatalog.SingerCatalogMetadata
            ](),
            description="Singer stream metadata blocks",
        )
        key_properties: t.StrSequence = u.Field(
            default_factory=tuple,
            description="Singer key property names for the stream",
        )
        replication_key: Annotated[
            str | None,
            u.Field(
                default=None, description="Column used for incremental replication"
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
            str | None, u.Field(default=None, description="Source table name")
        ] = None
        database_name: Annotated[
            str | None, u.Field(default=None, description="Source database name")
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
                default_factory=lambda: list[
                    FlextMeltanoModelsSingerCatalog.SingerCatalogEntry
                ](),
                description="Singer catalog stream entries",
            )
        )

    class SingerPipelineConfig(m.Entity):
        """Configuration for a Singer ELT pipeline."""

        tap_config_path: Annotated[
            Path | None, u.Field(default=None, description="Path to tap configuration")
        ] = None
        target_config_path: Annotated[
            Path | None,
            u.Field(default=None, description="Path to target configuration"),
        ] = None
        catalog_path: Annotated[
            Path | None, u.Field(default=None, description="Path to catalog file")
        ] = None
        state_path: Annotated[
            Path | None, u.Field(default=None, description="Path to state file")
        ] = None
        selected_streams: Annotated[
            t.StrSequence | None,
            u.Field(default=None, description="Specific streams to sync"),
        ] = None

    class SingerSyncResult(m.Entity):
        """Result of a Singer sync operation."""

        records_processed: Annotated[
            t.NonNegativeInt, u.Field(description="Number of records processed")
        ]
        records_written: Annotated[
            t.NonNegativeInt, u.Field(description="Number of records written")
        ]
        errors: Annotated[t.NonNegativeInt, u.Field(description="Number of errors")]
        state: t.JsonMapping = u.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Singer state payload captured after sync execution",
        )
        duration_seconds: Annotated[
            t.NonNegativeFloat, u.Field(description="Execution duration")
        ]
