"""FLEXT Meltano models - Singer catalog and pipeline config models."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Annotated, Literal

from flext_cli import FlextCliModels
from pydantic import Field

from flext_meltano import t


class FlextMeltanoModelsSingerCatalog:
    """Singer catalog, pipeline config, and sync result models."""

    class SingerCatalogMetadata(FlextCliModels.ArbitraryTypesModel):
        """Singer catalog metadata block model."""

        breadcrumb: Annotated[
            t.StrSequence, Field(description="Singer metadata breadcrumb path")
        ] = Field(default_factory=list)
        metadata: Annotated[
            t.ContainerMapping, Field(description="Singer metadata properties")
        ] = Field(default_factory=dict)

    class SingerCatalogEntry(FlextCliModels.ArbitraryTypesModel):
        """Singer catalog stream entry model."""

        tap_stream_id: Annotated[str, Field(description="Tap stream identifier")]
        stream: Annotated[str, Field(description="Singer stream name")]
        schema_definition: Annotated[
            t.FlatContainerMapping,
            Field(
                alias="schema",
                serialization_alias="schema",
                validation_alias="schema",
                description="Singer stream schema payload",
            ),
        ]
        metadata: Annotated[
            Sequence[FlextMeltanoModelsSingerCatalog.SingerCatalogMetadata],
            Field(description="Singer stream metadata blocks"),
        ] = Field(
            default_factory=lambda: list[
                FlextMeltanoModelsSingerCatalog.SingerCatalogMetadata
            ]()
        )
        key_properties: Annotated[
            t.StrSequence, Field(description="Primary key columns for this stream")
        ] = Field(default_factory=list)
        replication_key: Annotated[
            str | None,
            Field(default=None, description="Column used for incremental replication"),
        ] = None
        replication_method: Annotated[
            Literal["FULL_TABLE", "INCREMENTAL", "LOG_BASED"] | None,
            Field(default=None, description="Replication method for this stream"),
        ] = None
        is_view: Annotated[
            bool | None,
            Field(default=None, description="Whether this stream is a database view"),
        ] = None
        table_name: Annotated[
            str | None, Field(default=None, description="Source table name")
        ] = None
        database_name: Annotated[
            str | None, Field(default=None, description="Source database name")
        ] = None
        row_count: Annotated[
            int | None,
            Field(default=None, description="Estimated row count from source"),
        ] = None

    class SingerCatalog(FlextCliModels.ArbitraryTypesModel):
        """Singer catalog response model."""

        type: Annotated[
            Literal["CATALOG"],
            Field(
                default="CATALOG", description="Singer catalog message discriminator"
            ),
        ] = "CATALOG"
        streams: Annotated[
            Sequence[FlextMeltanoModelsSingerCatalog.SingerCatalogEntry],
            Field(description="Singer catalog stream entries"),
        ] = Field(
            default_factory=lambda: list[
                FlextMeltanoModelsSingerCatalog.SingerCatalogEntry
            ]()
        )

    class SingerPipelineConfig(FlextCliModels.Entity):
        """Configuration for a Singer ELT pipeline."""

        tap_config_path: Annotated[
            Path | None, Field(default=None, description="Path to tap configuration")
        ] = None
        target_config_path: Annotated[
            Path | None, Field(default=None, description="Path to target configuration")
        ] = None
        catalog_path: Annotated[
            Path | None, Field(default=None, description="Path to catalog file")
        ] = None
        state_path: Annotated[
            Path | None, Field(default=None, description="Path to state file")
        ] = None
        selected_streams: Annotated[
            t.StrSequence | None,
            Field(default=None, description="Specific streams to sync"),
        ] = None

    class SingerSyncResult(FlextCliModels.Entity):
        """Result of a Singer sync operation."""

        records_processed: Annotated[
            t.NonNegativeInt, Field(description="Number of records processed")
        ]
        records_written: Annotated[
            t.NonNegativeInt, Field(description="Number of records written")
        ]
        errors: Annotated[t.NonNegativeInt, Field(description="Number of errors")]
        state: Annotated[
            t.ContainerMapping, Field(description="Final state payload")
        ] = Field(default_factory=dict)
        duration_seconds: Annotated[
            t.NonNegativeFloat, Field(description="Execution duration")
        ]
