"""Singer Catalog Management - Schema discovery and catalog handling.

This module provides catalog management for Singer with FLEXT ecosystem
patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import override

from flext_core import FlextService, r

from flext_meltano import FlextMeltanoConstants, FlextMeltanoModels, FlextMeltanoTypes
from flext_meltano.singer.protocols import FlextMeltanoSingerProtocols

t = FlextMeltanoTypes
m = FlextMeltanoModels
c = FlextMeltanoConstants
singer_p = FlextMeltanoSingerProtocols


class FlextMeltanoCatalogManager(FlextService[m.Meltano.SingerCatalog]):
    """Manages Singer catalogs (schemas and stream definitions).

    Handles catalog discovery, loading, validation, and manipulation
    with proper error handling and r patterns.
    """

    def __init__(self) -> None:
        """Initialize catalog manager."""
        super().__init__()
        self._catalog = m.Meltano.SingerCatalog()

    def discover_streams(self, tap: singer_p.SingerTap) -> r[m.Meltano.SingerCatalog]:
        """Discover streams from a tap.

        Args:
        tap: Singer tap instance with discover() method

        Returns:
        r containing discovered catalog

        """
        try:
            self._catalog = tap.discover()
            self.logger.info(
                "Streams discovered", stream_count=len(self._catalog.streams)
            )
            return r[m.Meltano.SingerCatalog].ok(self._catalog)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to discover streams", error=str(e))
            return r[m.Meltano.SingerCatalog].fail(f"Failed to discover: {e}")

    @override
    def execute(self) -> r[m.Meltano.SingerCatalog]:
        """Execute (implements Service pattern)."""
        return r[m.Meltano.SingerCatalog].ok(self._catalog)

    def get_stream_schema(self, stream_name: str) -> r[Mapping[str, object
        """Get schema for a specific stream.

        Args:
        stream_name: Name of the stream

        Returns:
        r containing stream schema or None

        """
        try:
            for entry in self._catalog.streams:
                if entry.stream == stream_name:
                    self.logger.debug("Stream schema retrieved", stream=stream_name)
                    return r[Mapping[str, object(entry.schema_definition)
            return r[Mapping[str, objectil(
                f"Stream not found in catalog: {stream_name}"
            )
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to get stream schema", error=str(e))
            return r[Mapping[str, objectil(f"Failed to get schema: {e}")

    def load_catalog(self, catalog_file: Path) -> r[m.Meltano.SingerCatalog]:
        """Load catalog from file.

        Args:
        catalog_file: Path to catalog file

        Returns:
        r containing loaded catalog

        """
        try:
            if not catalog_file.exists():
                return r[m.Meltano.SingerCatalog].fail(
                    f"Catalog file not found: {catalog_file}"
                )
            with catalog_file.open(encoding="utf-8") as f:
                raw_data = json.load(f)
            self._catalog = m.Meltano.SingerCatalog.model_validate(raw_data)
            self.logger.info(
                "Catalog loaded from file",
                file=str(catalog_file),
                stream_count=len(self._catalog.streams),
            )
            return r[m.Meltano.SingerCatalog].ok(self._catalog)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to load catalog", error=str(e))
            return r[m.Meltano.SingerCatalog].fail(f"Failed to load catalog: {e}")

    def save_catalog(self, catalog_file: Path) -> r[None]:
        """Save catalog to file.

        Args:
        catalog_file: Path to save catalog

        Returns:
        r with success status

        """
        try:
            catalog_file.parent.mkdir(parents=True, exist_ok=True)
            with catalog_file.open("w", encoding="utf-8") as f:
                f.write(self._catalog.model_dump_json(indent=2, by_alias=True))
            self.logger.info("Catalog saved to file", file=str(catalog_file))
            return r[None].ok(None)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to save catalog", error=str(e))
            return r[None].fail(f"Failed to save catalog: {e}")

    def select_streams(self, stream_names: list[str]) -> r[m.Meltano.SingerCatalog]:
        """Select specific streams from catalog.

        Args:
        stream_names: List of stream names to select

        Returns:
        r containing filtered catalog

        """
        try:
            selected = [
                entry for entry in self._catalog.streams if entry.stream in stream_names
            ]
            filtered_catalog = m.Meltano.SingerCatalog(streams=selected)
            self.logger.info(
                "Streams selected",
                total=len(self._catalog.streams),
                selected=len(selected),
            )
            return r[m.Meltano.SingerCatalog].ok(filtered_catalog)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to select streams", error=str(e))
            return r[m.Meltano.SingerCatalog].fail(f"Failed to select: {e}")

    def set_catalog(self, catalog: m.Meltano.SingerCatalog) -> None:
        """Set catalog data directly.

        Args:
        catalog: Catalog model to set

        """
        self._catalog = catalog


__all__ = ["FlextMeltanoCatalogManager"]
