# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_meltano/_protocols/singer_catalog
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_meltano import c, t


class FlextMeltanoProtocolsSingerCatalog:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class SingerCatalogMetadata(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        breadcrumb: t.StrTuple
        metadata: t.FlatContainerMapping

    @runtime_checkable
    class SingerCatalogEntry(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        tap_stream_id: str
        stream: str
        schema_definition: t.FlatContainerMapping

        @property
        def metadata(
            self,
        ) -> tuple[FlextMeltanoProtocolsSingerCatalog.SingerCatalogMetadata, ...]:
            """Singer stream metadata blocks."""
            ...

        key_properties: t.StrTuple
        replication_key: str | None
        replication_method: Literal["FULL_TABLE", "INCREMENTAL", "LOG_BASED"] | None
        is_view: bool | None
        table_name: str | None
        database_name: str | None
        row_count: int | None

    @runtime_checkable
    class SingerCatalog(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        type: c.Meltano.SingerMessageType

        @property
        def streams(
            self,
        ) -> tuple[FlextMeltanoProtocolsSingerCatalog.SingerCatalogEntry, ...]:
            """Singer catalog stream entries."""
            ...


__all__: list[str] = [
    "FlextMeltanoProtocolsSingerCatalog",
]
