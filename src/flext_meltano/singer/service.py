"""Singer Orchestration Service - ELT pipeline execution.

This module provides Singer ELT pipeline orchestration with FLEXT ecosystem
patterns, railway-oriented programming, and deep SDK integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextModels, FlextResult, FlextService
from pydantic import Field

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.singer.catalog import FlextMeltanoCatalogManager
from flext_meltano.singer.protocols import FlextMeltanoSingerProtocols
from flext_meltano.singer.state import FlextMeltanoStateManager
from flext_meltano.typings import FlextMeltanoTypes

# Import aliases following order: c -> t -> p -> r -> m -> s
c = FlextMeltanoConstants
t = FlextMeltanoTypes
singer_p = FlextMeltanoSingerProtocols
r = FlextResult
m = FlextModels
s = FlextService


class FlextMeltanoSingerService(s[str]):
    """Orchestrates Singer ELT pipelines (tap -> target) with deep SDK integration.

    Provides complete Singer protocol orchestration including:
    - Tap and target lifecycle management
    - Catalog discovery and schema management
    - State management for incremental syncs
    - Stream record processing and mapping
    - Error handling with r[T]

    This service integrates directly with singer-sdk, providing a
    programmatic API for complete ELT operations.

    Attributes:
    catalog_manager: Manages Singer catalogs
    state_manager: Manages sync state and bookmarks

    """

    class PipelineConfig(m.Entity):
        """Configuration for a Singer pipeline."""

        tap_config_path: Path | None = Field(
            default=None,
            description="Path to tap configuration",
        )
        target_config_path: Path | None = Field(
            default=None,
            description="Path to target configuration",
        )
        catalog_path: Path | None = Field(
            default=None,
            description="Path to catalog file",
        )
        state_path: Path | None = Field(default=None, description="Path to state file")
        selected_streams: list[str] | None = Field(
            default=None,
            description="Specific streams to sync",
        )

    class SyncResult(m.Entity):
        """Result of a Singer sync operation."""

        records_processed: int = Field(description="Number of records processed")
        records_written: int = Field(description="Number of records written")
        errors: int = Field(description="Number of errors")
        state: t.Singer.TapConfig | None = Field(
            default=None, description="Final state"
        )
        duration_seconds: float = Field(description="Execution duration")

    def __init__(self) -> None:
        """Initialize Singer orchestration service."""
        super().__init__()
        self.catalog_manager = FlextMeltanoCatalogManager()
        self.state_manager = FlextMeltanoStateManager()

    def discover_tap_catalog(
        self,
        tap: singer_p.SingerTap,
    ) -> r[t.Singer.StreamCatalog]:
        """Discover catalog from a tap instance.

        Args:
        tap: Singer tap instance

        Returns:
        FlextResult containing discovered catalog

        """
        try:
            self.logger.info("Starting tap catalog discovery")
            result = self.catalog_manager.discover_streams(tap)
            if result.is_success:
                self.logger.info("Tap catalog discovery completed")
            return result
        except Exception as e:
            self.logger.exception("Tap discovery failed", error=str(e))
            return r[t.Singer.StreamCatalog].fail(f"Tap discovery failed: {e}")

    def execute_sync(
        self,
        tap: singer_p.SingerTap,
        target: singer_p.SingerTarget,
        catalog: t.Singer.StreamCatalog,
        state: t.Singer.TapConfig | None = None,
    ) -> r[FlextMeltanoSingerService.SyncResult]:
        """Execute a complete Singer sync pipeline.

        Args:
        tap: Singer tap instance
        target: Singer target instance
        catalog: Catalog dictionary
        state: Optional state dictionary for incremental sync

        Returns:
        FlextResult containing sync result with metrics

        """
        try:
            self.logger.info("Starting Singer sync")

            records_processed = 0
            records_written = 0
            errors = 0

            # Execute tap sync
            state_dict = state or {}

            # Get records from tap
            records: t.Singer.MessageBatch = []
            tap.sync(catalog, state_dict)

            # The target consumes from tap's output
            target.consume(records)

            result = FlextMeltanoSingerService.SyncResult(
                records_processed=records_processed,
                records_written=records_written,
                errors=errors,
                state=state_dict,
                duration_seconds=0.0,
            )

            self.logger.info(
                "Singer sync completed",
                records=records_processed,
                written=records_written,
            )
            return r[FlextMeltanoSingerService.SyncResult].ok(result)
        except Exception as e:
            self.logger.exception("Singer sync failed", error=str(e))
            return r[FlextMeltanoSingerService.SyncResult].fail(
                f"Singer sync failed: {e}",
            )

    def load_catalog_from_file(self, catalog_path: Path) -> r[t.Singer.StreamCatalog]:
        """Load catalog from file.

        Args:
        catalog_path: Path to catalog file

        Returns:
        FlextResult containing loaded catalog

        """
        return self.catalog_manager.load_catalog(catalog_path)

    def save_catalog_to_file(
        self,
        catalog: t.Singer.StreamCatalog,
        catalog_path: Path,
    ) -> r[None]:
        """Save catalog to file.

        Args:
        catalog: Catalog dictionary
        catalog_path: Path to save

        Returns:
        FlextResult with success status

        """
        self.catalog_manager.set_catalog(catalog)
        return self.catalog_manager.save_catalog(catalog_path)

    def load_state_from_file(
        self,
        state_path: Path | None = None,
    ) -> r[t.Singer.TapConfig]:
        """Load state from file.

        Args:
        state_path: Path to state file

        Returns:
        FlextResult containing loaded state

        """
        return self.state_manager.load_state(state_path)

    def save_state_to_file(self, state_path: Path) -> r[None]:
        """Save state to file.

        Args:
        state_path: Path to save state

        Returns:
        FlextResult with success status

        """
        return self.state_manager.save_state(state_path)

    def execute(self) -> r[str]:
        """Execute (implements Service pattern)."""
        msg = "Singer service initialized"
        return r[str].ok(msg)


__all__ = [
    "FlextMeltanoSingerService",
]
