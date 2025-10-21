"""Singer Catalog Management - Schema discovery and catalog handling.

This module provides catalog management for Singer with FLEXT ecosystem
patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from flext_core import FlextResult, FlextService


class FlextMeltanoCatalogManager(FlextService):
    """Manages Singer catalogs (schemas and stream definitions).

    Handles catalog discovery, loading, validation, and manipulation
    with proper error handling and FlextResult patterns.
    """

    def __init__(self) -> None:
        """Initialize catalog manager."""
        super().__init__()
        self._catalog: dict[str, Any] = {"streams": []}

    def discover_streams(self, tap: object) -> FlextResult[dict[str, Any]]:
        """Discover streams from a tap.

        Args:
        tap: Singer tap instance with discover() method

        Returns:
        FlextResult containing discovered catalog

        """
        try:
            if not hasattr(tap, "discover"):
                return FlextResult[dict[str, Any]].fail(
                    "Tap must have discover() method"
                )

            catalog = tap.discover()
            self._catalog = catalog if isinstance(catalog, dict) else {"streams": []}

            stream_count = len(self._catalog.get("streams", []))
            self.logger.info(
                "Streams discovered",
                stream_count=stream_count,
            )
            return FlextResult[dict[str, Any]].ok(self._catalog)
        except Exception as e:
            self.logger.exception("Failed to discover streams", error=str(e))
            return FlextResult[dict[str, Any]].fail(f"Failed to discover: {e}")

    def load_catalog(self, catalog_file: Path) -> FlextResult[dict[str, Any]]:
        """Load catalog from file.

        Args:
        catalog_file: Path to catalog file

        Returns:
        FlextResult containing loaded catalog

        """
        try:
            if not catalog_file.exists():
                return FlextResult[dict[str, Any]].fail(
                    f"Catalog file not found: {catalog_file}"
                )

            with catalog_file.open(encoding="utf-8") as f:
                self._catalog = json.load(f)

            stream_count = len(self._catalog.get("streams", []))
            self.logger.info(
                "Catalog loaded from file",
                file=str(catalog_file),
                stream_count=stream_count,
            )
            return FlextResult[dict[str, Any]].ok(self._catalog)
        except Exception as e:
            self.logger.exception("Failed to load catalog", error=str(e))
            return FlextResult[dict[str, Any]].fail(f"Failed to load catalog: {e}")

    def set_catalog(self, catalog: dict[str, Any]) -> None:
        """Set catalog data directly.

        Args:
        catalog: Catalog data to set

        """
        self._catalog = catalog

    def save_catalog(self, catalog_file: Path) -> FlextResult[None]:
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
            return FlextResult[None].ok(None)
        except Exception as e:
            self.logger.exception("Failed to save catalog", error=str(e))
            return FlextResult[None].fail(f"Failed to save catalog: {e}")

    def select_streams(self, stream_names: list[str]) -> FlextResult[dict[str, Any]]:
        """Select specific streams from catalog.

        Args:
        stream_names: List of stream names to select

        Returns:
        FlextResult containing filtered catalog

        """
        try:
            streams = self._catalog.get("streams", [])
            selected = [s for s in streams if s.get("name") in stream_names]

            filtered_catalog = {"streams": selected}
            self.logger.info(
                "Streams selected",
                total=len(streams),
                selected=len(selected),
            )
            return FlextResult[dict[str, Any]].ok(filtered_catalog)
        except Exception as e:
            self.logger.exception("Failed to select streams", error=str(e))
            return FlextResult[dict[str, Any]].fail(f"Failed to select: {e}")

    def get_stream_schema(self, stream_name: str) -> FlextResult[dict[str, Any] | None]:
        """Get schema for a specific stream.

        Args:
        stream_name: Name of the stream

        Returns:
        FlextResult containing stream schema or None

        """
        try:
            streams = self._catalog.get("streams", [])
            for stream in streams:
                if stream.get("name") == stream_name:
                    schema = stream.get("schema", {})
                    self.logger.debug(
                        "Stream schema retrieved",
                        stream=stream_name,
                    )
                    return FlextResult[dict[str, Any] | None].ok(schema)

            return FlextResult[dict[str, Any] | None].ok(None)
        except Exception as e:
            self.logger.exception("Failed to get stream schema", error=str(e))
            return FlextResult[dict[str, Any] | None].fail(f"Failed to get schema: {e}")

    def execute(self) -> FlextResult[dict[str, Any]]:
        """Execute (implements Domain.Service pattern)."""
        return FlextResult[dict[str, Any]].ok(self._catalog)


__all__ = [
    "FlextMeltanoCatalogManager",
]
