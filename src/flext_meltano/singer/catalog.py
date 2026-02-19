"""Singer Catalog Management - Schema discovery and catalog handling.

This module provides catalog management for Singer with FLEXT ecosystem
patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from pathlib import Path

from flext_core import FlextResult, FlextService, u

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.singer.protocols import FlextMeltanoSingerProtocols
from flext_meltano.typings import FlextMeltanoTypes

# Import aliases for simplified usage
r = FlextResult
t = FlextMeltanoTypes
c = FlextMeltanoConstants
singer_p = FlextMeltanoSingerProtocols


class FlextMeltanoCatalogManager(FlextService[t.Singer.StreamCatalog]):
    """Manages Singer catalogs (schemas and stream definitions).

    Handles catalog discovery, loading, validation, and manipulation
    with proper error handling and FlextResult patterns.
    """

    def __init__(self) -> None:
        """Initialize catalog manager."""
        super().__init__()
        self._catalog: t.Singer.StreamCatalog = {"streams": []}

    def discover_streams(self, tap: singer_p.SingerTap) -> r[t.Singer.StreamCatalog]:
        """Discover streams from a tap.

        Args:
        tap: Singer tap instance with discover() method

        Returns:
        FlextResult containing discovered catalog

        """
        try:
            catalog = tap.discover()
            catalog_guard = u.guard(catalog, dict, return_value=True)
            if catalog_guard is not None and isinstance(catalog_guard, dict):
                self._catalog = catalog_guard
            else:
                self._catalog = {"streams": []}

            streams_raw = u.get(self._catalog, "streams", default=[])
            streams: list[t.Singer.CatalogEntry] = (
                streams_raw if isinstance(streams_raw, list) else []
            )
            stream_count = u.count(streams)
            self.logger.info(
                "Streams discovered",
                stream_count=stream_count,
            )
            return r[t.Singer.StreamCatalog].ok(self._catalog)
        except Exception as e:
            self.logger.exception("Failed to discover streams", error=str(e))
            return r[t.Singer.StreamCatalog].fail(f"Failed to discover: {e}")

    def load_catalog(self, catalog_file: Path) -> r[t.Singer.StreamCatalog]:
        """Load catalog from file.

        Args:
        catalog_file: Path to catalog file

        Returns:
        FlextResult containing loaded catalog

        """
        try:
            if not catalog_file.exists():
                return r[t.Singer.StreamCatalog].fail(
                    f"Catalog file not found: {catalog_file}",
                )

            with catalog_file.open(encoding="utf-8") as f:
                self._catalog = json.load(f)

            streams_raw = u.get(self._catalog, "streams", default=[])
            streams: list[t.Singer.CatalogEntry] = (
                streams_raw if isinstance(streams_raw, list) else []
            )
            stream_count = u.count(streams)
            self.logger.info(
                "Catalog loaded from file",
                file=str(catalog_file),
                stream_count=stream_count,
            )
            return r[t.Singer.StreamCatalog].ok(self._catalog)
        except Exception as e:
            self.logger.exception("Failed to load catalog", error=str(e))
            return r[t.Singer.StreamCatalog].fail(f"Failed to load catalog: {e}")

    def set_catalog(self, catalog: t.Singer.StreamCatalog) -> None:
        """Set catalog data directly.

        Args:
        catalog: Catalog data to set

        """
        self._catalog = catalog

    def save_catalog(self, catalog_file: Path) -> r[None]:
        """Save catalog to file.

        Args:
        catalog_file: Path to save catalog

        Returns:
        FlextResult with success status

        """
        try:
            catalog_file.parent.mkdir(parents=True, exist_ok=True)
            with catalog_file.open("w", encoding="utf-8") as f:
                json.dump(self._catalog, f, indent=2, default=str)

            self.logger.info(
                "Catalog saved to file",
                file=str(catalog_file),
            )
            return r[None].ok(None)
        except Exception as e:
            self.logger.exception("Failed to save catalog", error=str(e))
            return r[None].fail(f"Failed to save catalog: {e}")

    def select_streams(self, stream_names: list[str]) -> r[t.Singer.StreamCatalog]:
        """Select specific streams from catalog.

        Args:
        stream_names: List of stream names to select

        Returns:
        FlextResult containing filtered catalog

        """
        try:
            streams_raw = u.get(self._catalog, "streams", default=[])
            streams: list[t.Singer.CatalogEntry] = (
                streams_raw if isinstance(streams_raw, list) else []
            )
            selected = u.filter(streams, lambda s: u.get(s, "name") in stream_names)

            filtered_catalog: t.Singer.StreamCatalog = {"streams": selected}
            self.logger.info(
                "Streams selected",
                total=u.count(streams),
                selected=u.count(selected),
            )
            return r[t.Singer.StreamCatalog].ok(filtered_catalog)
        except Exception as e:
            self.logger.exception("Failed to select streams", error=str(e))
            return r[t.Singer.StreamCatalog].fail(f"Failed to select: {e}")

    def get_stream_schema(self, stream_name: str) -> r[t.Singer.StreamSchema | None]:
        """Get schema for a specific stream.

        Args:
        stream_name: Name of the stream

        Returns:
        FlextResult containing stream schema or None

        """
        try:
            streams_raw = u.get(self._catalog, "streams", default=[])
            streams: list[t.Singer.CatalogEntry] = (
                streams_raw if isinstance(streams_raw, list) else []
            )
            found_stream = u.find(
                streams, lambda value: u.get(value, "name") == stream_name
            )
            if found_stream is not None:
                schema_raw = u.get(found_stream, "schema", default={})
                schema: t.Singer.StreamSchema = (
                    schema_raw if isinstance(schema_raw, dict) else {}
                )
                self.logger.debug(
                    "Stream schema retrieved",
                    stream=stream_name,
                )
                return r[t.Singer.StreamSchema | None].ok(schema)

            return r[t.Singer.StreamSchema | None].ok(None)
        except Exception as e:
            self.logger.exception("Failed to get stream schema", error=str(e))
            return r[t.Singer.StreamSchema | None].fail(f"Failed to get schema: {e}")

    def execute(self) -> r[t.Singer.StreamCatalog]:
        """Execute (implements Service pattern)."""
        return r[t.Singer.StreamCatalog].ok(self._catalog)


__all__ = [
    "FlextMeltanoCatalogManager",
]
