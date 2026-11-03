# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_meltano/_protocols/singer_catalog
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_meltano import t

if TYPE_CHECKING:
    from flext_meltano._constants import FlextMeltanoConstantsEnums


class FlextMeltanoProtocolsSingerCatalog:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class SingerCatalogMetadata(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        breadcrumb: t.StrTuple
        metadata: t.FlatContainerMapping

    @runtime_checkable
    class SingerCatalogEntry(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def tap_stream_id(self) -> str:
            """Tap stream identifier."""
            ...

        @property
        def stream(self) -> str:
            """Singer stream name."""
            ...

        @property
        def schema_definition(self) -> t.FlatContainerMapping:
            """Singer stream schema payload."""
            ...

        @property
        def metadata(
            self,
        ) -> tuple[FlextMeltanoProtocolsSingerCatalog.SingerCatalogMetadata, ...]:
            """Singer stream metadata blocks."""
            ...

        key_properties: t.StrTuple

        @property
        def replication_key(self) -> str | None:
            """Column used for incremental replication."""
            ...

        @property
        def replication_method(
            self,
        ) -> Literal["FULL_TABLE", "INCREMENTAL", "LOG_BASED"] | None:
            """Replication method for this stream."""
            ...

        @property
        def is_view(self) -> bool | None:
            """Whether this stream is a database view."""
            ...

        @property
        def table_name(self) -> str | None:
            """Source table name."""
            ...

        @property
        def database_name(self) -> str | None:
            """Source database name."""
            ...

        @property
        def row_count(self) -> int | None:
            """Estimated row count from source."""
            ...

    @runtime_checkable
    class SingerCatalog(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def type(self) -> FlextMeltanoConstantsEnums.SingerMessageType:
            """Singer catalog message discriminator."""
            ...

        @property
        def streams(
            self,
        ) -> tuple[FlextMeltanoProtocolsSingerCatalog.SingerCatalogEntry, ...]:
            """Singer catalog stream entries."""
            ...


__all__: list[str] = [
    "FlextMeltanoProtocolsSingerCatalog",
]
