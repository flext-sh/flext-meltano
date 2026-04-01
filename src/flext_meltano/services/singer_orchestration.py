"""Singer Orchestration — MRO mixin for FlextMeltano facade.

High-level ELT pipeline coordination using catalog and state mixins
available via MRO on the facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import r

from flext_meltano import FlextMeltanoServiceBase, m, p


class FlextMeltanoSingerOrchestrationMixin(FlextMeltanoServiceBase):
    """Singer ELT orchestration mixin for MRO composition on FlextMeltano.

    Coordinates Singer tap→target pipelines using catalog and state
    management methods provided by sibling mixins via MRO:
    - ``discover_catalog_streams`` from ``FlextMeltanoSingerCatalogMixin``
    - ``load_state`` from ``FlextMeltanoSingerStateMixin``
    - ``save_state`` from ``FlextMeltanoSingerStateMixin``
    """

    def discover_tap_catalog(
        self,
        tap: p.Meltano.SingerTap,
    ) -> r[m.Meltano.SingerCatalog]:
        """Discover catalog from a tap instance.

        Delegates to ``self.discover_catalog_streams()`` (from CatalogMixin).
        """
        try:
            self.logger.info("Starting tap catalog discovery")
            result = self.discover_catalog_streams(tap)  # type: ignore[attr-defined]
            if result.is_success:
                self.logger.info("Tap catalog discovery completed")
            return result
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Tap discovery failed", error=str(e))
            return r[m.Meltano.SingerCatalog].fail(f"Tap discovery failed: {e}")

    def execute_sync(
        self,
        tap: p.Meltano.SingerTap,
        target: p.Meltano.SingerTarget,
        catalog: m.Meltano.SingerCatalog,
        state: m.Meltano.SingerStateMessage,
    ) -> r[m.Meltano.SingerSyncResult]:
        """Execute a complete Singer sync pipeline."""
        _ = tap, target, catalog, state
        return r[m.Meltano.SingerSyncResult].fail(
            "Singer protocol: requires singer-sdk tap/target integration "
            "to pipe tap stdout into target stdin and collect metrics"
        )

    def load_catalog_from_file(self, catalog_path: Path) -> r[m.Meltano.SingerCatalog]:
        """Load catalog from file via CatalogMixin."""
        return self.load_catalog(catalog_path)  # type: ignore[attr-defined]

    def load_state_from_file(
        self,
        state_path: Path | None = None,
    ) -> r[m.Meltano.SingerStateMessage]:
        """Load state from file via StateMixin."""
        return self.load_state(state_path)  # type: ignore[attr-defined]

    def save_catalog_to_file(
        self,
        catalog: m.Meltano.SingerCatalog,
        catalog_path: Path,
    ) -> r[None]:
        """Save catalog to file via CatalogMixin."""
        self.set_singer_catalog(catalog)  # type: ignore[attr-defined]
        return self.save_catalog(catalog_path)  # type: ignore[attr-defined]

    def save_state_to_file(self, state_path: Path) -> r[None]:
        """Save state to file via StateMixin."""
        return self.save_state(state_path)  # type: ignore[attr-defined]


__all__ = ["FlextMeltanoSingerOrchestrationMixin"]
