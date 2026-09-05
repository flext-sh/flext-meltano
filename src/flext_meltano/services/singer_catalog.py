"""Singer Catalog Management — MRO mixin for FlextMeltano facade.

Provides catalog discovery, loading, saving, and stream selection.
Converted from standalone FlextMeltanoCatalogManager to facade mixin.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_cli import cli
from flext_meltano import FlextMeltanoServiceBase, c, m, p, r, t, u

if TYPE_CHECKING:
    from pathlib import Path


class FlextMeltanoSingerCatalogMixin(FlextMeltanoServiceBase):
    """Singer catalog management mixin for MRO composition on FlextMeltano.

    Manages Singer catalogs (schemas and stream definitions).
    Internal state ``_singer_catalog`` is initialized as empty catalog.
    """

    _singer_catalog: m.Meltano.SingerCatalog = u.PrivateAttr(
        default_factory=m.Meltano.SingerCatalog
    )

    def discover_catalog_streams(
        self, tap: p.Meltano.SingerTap
    ) -> p.Result[m.Meltano.SingerCatalog]:
        """Discover streams from a Singer tap instance.

        Named ``discover_catalog_streams`` to avoid conflict with
        ``FlextMeltanoAbstractions.discover_streams`` (Meltano CLI-based).
        """
        try:
            self._singer_catalog = tap.discover()
            self.logger.info(
                "Streams discovered", stream_count=len(self._singer_catalog.streams)
            )
            return r[m.Meltano.SingerCatalog].ok(self._singer_catalog)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Failed to discover streams", error=str(e))
            return r[m.Meltano.SingerCatalog].fail(f"Failed to discover: {e}", exception=e)

    def fetch_stream_schema(self, stream_name: str) -> p.Result[t.JsonMapping]:
        """Get schema for a specific stream from cached catalog."""
        try:
            for entry in self._singer_catalog.streams:
                if entry.stream == stream_name:
                    self.logger.debug("Stream schema retrieved", stream=stream_name)
                    return r[t.JsonMapping].ok(entry.schema_definition)
            return r[t.JsonMapping].fail(f"Stream not found in catalog: {stream_name}")
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Failed to get stream schema", error=str(e))
            return r[t.JsonMapping].fail(f"Failed to get schema: {e}", exception=e)

    def load_catalog(self, catalog_file: Path) -> p.Result[m.Meltano.SingerCatalog]:
        """Load catalog from JSON file."""
        try:
            if not catalog_file.exists():
                return r[m.Meltano.SingerCatalog].fail(
                    f"Catalog file not found: {catalog_file}"
                )

            def _store(catalog: m.Meltano.SingerCatalog) -> m.Meltano.SingerCatalog:
                self._singer_catalog = catalog
                self.logger.info(
                    "Catalog loaded from file",
                    file=str(catalog_file),
                    stream_count=len(catalog.streams),
                )
                return catalog

            return u.Cli.files_read_json_model(
                catalog_file, m.Meltano.SingerCatalog
            ).map(_store)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Failed to load catalog", error=str(e))
            return r[m.Meltano.SingerCatalog].fail(f"Failed to load catalog: {e}", exception=e)

    def save_catalog(self, catalog_file: Path) -> p.Result[bool]:
        """Save catalog to JSON file."""
        try:
            catalog_file.parent.mkdir(parents=True, exist_ok=True)
            write_result = cli.atomic_write_text_file(
                catalog_file,
                self._singer_catalog.model_dump_json(indent=2, by_alias=True),
            )
            if write_result.failure:
                return r[bool].from_failure(write_result)
            self.logger.info("Catalog saved to file", file=str(catalog_file))
            return r[bool].ok(True)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Failed to save catalog", error=str(e))
            return r[bool].fail(f"Failed to save catalog: {e}", exception=e)

    def select_streams(
        self, stream_names: t.StrSequence
    ) -> p.Result[m.Meltano.SingerCatalog]:
        """Select specific streams from cached catalog."""
        try:
            selected = [
                entry
                for entry in self._singer_catalog.streams
                if entry.stream in stream_names
            ]
            filtered_catalog = m.Meltano.SingerCatalog(streams=selected)
            self.logger.info(
                "Streams selected",
                total=len(self._singer_catalog.streams),
                selected=len(selected),
            )
            return r[m.Meltano.SingerCatalog].ok(filtered_catalog)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Failed to select streams", error=str(e))
            return r[m.Meltano.SingerCatalog].fail(f"Failed to select: {e}", exception=e)

    def configure_singer_catalog(self, catalog: m.Meltano.SingerCatalog) -> None:
        """Set catalog data directly."""
        self._singer_catalog = catalog


__all__: list[str] = ["FlextMeltanoSingerCatalogMixin"]
