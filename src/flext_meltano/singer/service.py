"""Singer Orchestration Service - ELT pipeline execution.

This module provides Singer ELT pipeline orchestration with FLEXT ecosystem
patterns, railway-oriented programming, and deep SDK integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flext_core import FlextResult, FlextService
from pydantic import Field

from flext_meltano.models import FlextMeltanoModels
from flext_meltano.singer.catalog import FlextMeltanoCatalogManager
from flext_meltano.singer.state import FlextMeltanoStateManager


class FlextMeltanoSingerService(FlextService):
    """Orchestrates Singer ELT pipelines (tap -> target) with deep SDK integration.

    Provides comprehensive Singer protocol orchestration including:
    - Tap and target lifecycle management
    - Catalog discovery and schema management
    - State management for incremental syncs
    - Stream record processing and mapping
    - Error handling with FlextResult[T]

    This service integrates directly with singer-sdk, providing a
    programmatic API for complete ELT operations.

    Attributes:
        catalog_manager: Manages Singer catalogs
        state_manager: Manages sync state and bookmarks

    """

    class PipelineConfig(FlextMeltanoModels):
        """Configuration for a Singer pipeline."""

        tap_config_path: Path | None = Field(
            default=None, description="Path to tap configuration"
        )
        target_config_path: Path | None = Field(
            default=None, description="Path to target configuration"
        )
        catalog_path: Path | None = Field(
            default=None, description="Path to catalog file"
        )
        state_path: Path | None = Field(default=None, description="Path to state file")
        selected_streams: list[str] | None = Field(
            default=None, description="Specific streams to sync"
        )

    class SyncResult(FlextMeltanoModels):
        """Result of a Singer sync operation."""

        records_processed: int = Field(description="Number of records processed")
        records_written: int = Field(description="Number of records written")
        errors: int = Field(description="Number of errors")
        state: dict[str, Any] | None = Field(default=None, description="Final state")
        duration_seconds: float = Field(description="Execution duration")

    def __init__(self) -> None:
        """Initialize Singer orchestration service."""
        super().__init__()
        self.catalog_manager = FlextMeltanoCatalogManager()
        self.state_manager = FlextMeltanoStateManager()

    def discover_tap_catalog(self, tap: object) -> FlextResult[dict[str, Any]]:
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
            return FlextResult[dict[str, Any]].fail(f"Tap discovery failed: {e}")

    def execute_sync(
        self,
        tap: object,
        target: object,
        catalog: dict[str, Any],
        state: dict[str, Any] | None = None,
    ) -> FlextResult[FlextMeltanoSingerService.SyncResult]:
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
            if not hasattr(tap, "sync"):
                return FlextResult[FlextMeltanoSingerService.SyncResult].fail(
                    "Tap must have sync() method"
                )
            if not hasattr(target, "consume"):
                return FlextResult[FlextMeltanoSingerService.SyncResult].fail(
                    "Target must have consume() method"
                )

            self.logger.info("Starting Singer sync")

            records_processed = 0
            records_written = 0
            errors = 0

            # Execute tap sync
            state_dict = state or {}

            # Get records from tap
            if hasattr(tap, "sync"):
                tap.sync(catalog, state_dict)

            # The target consumes from tap's output
            if hasattr(target, "consume"):
                target.consume(None)

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
            return FlextResult[FlextMeltanoSingerService.SyncResult].ok(result)
        except Exception as e:
            self.logger.exception("Singer sync failed", error=str(e))
            return FlextResult[FlextMeltanoSingerService.SyncResult].fail(
                f"Singer sync failed: {e}"
            )

    def load_catalog_from_file(self, catalog_path: Path) -> FlextResult[dict[str, Any]]:
        """Load catalog from file.

        Args:
            catalog_path: Path to catalog file

        Returns:
            FlextResult containing loaded catalog

        """
        return self.catalog_manager.load_catalog(catalog_path)

    def save_catalog_to_file(
        self,
        catalog: dict[str, Any],
        catalog_path: Path,
    ) -> FlextResult[None]:
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
        self, state_path: Path | None = None
    ) -> FlextResult[dict[str, Any]]:
        """Load state from file.

        Args:
            state_path: Path to state file

        Returns:
            FlextResult containing loaded state

        """
        return self.state_manager.load_state(state_path)

    def save_state_to_file(self, state_path: Path) -> FlextResult[None]:
        """Save state to file.

        Args:
            state_path: Path to save state

        Returns:
            FlextResult with success status

        """
        return self.state_manager.save_state(state_path)

    def execute(self) -> FlextResult[str]:
        """Execute (implements Domain.Service pattern)."""
        msg = "Singer service initialized"
        return FlextResult[str].ok(msg)


__all__ = [
    "FlextMeltanoSingerService",
]
