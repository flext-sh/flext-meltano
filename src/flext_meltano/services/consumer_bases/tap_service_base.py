"""Base service for FLEXT tap consumer projects.

Provides Singer tap lifecycle via MRO: CLI dispatch, stream discovery,
sync execution, and connection management. Consumer taps subclass
``singer_sdk.Tap`` (required by Singer SDK) — this base wraps the tap
instance with FLEXT service patterns (``r[T]``, typed config, lifecycle).

Consumer projects inherit this and override ``create_tap_instance()`` only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from abc import abstractmethod
from typing import Annotated, ClassVar, Self, override

from pydantic import Field, PrivateAttr

from flext_core import r
from flext_meltano import FlextMeltanoServiceBase, FlextMeltanoSingerTapBase, c, t


class FlextMeltanoTapServiceBase(FlextMeltanoServiceBase):
    """Base for all FLEXT tap service projects.

    Subclasses MUST define:
    - ``tap_name``: canonical tap identifier (e.g. ``"tap-oracle"``)
    - ``create_tap_instance()``: factory returning the singer_sdk Tap subclass

    This base provides via MRO:
    - CLI dispatch (``cli_main``)
    - Singer catalog discovery (``run_discover``)
    - Singer sync execution (``run_sync``)
    - Connection lifecycle (``connect`` / ``disconnect``)
    - Singleton accessor (``get_instance``)
    """

    tap_name: Annotated[
        t.NonEmptyStr,
        Field(description="Canonical tap name (e.g. tap-oracle)"),
    ] = "tap"

    _tap_instance: FlextMeltanoSingerTapBase | None = PrivateAttr(default=None)
    _instance: ClassVar[Self | None] = None

    @classmethod
    def get_instance(cls) -> Self:
        """Return the shared facade instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @abstractmethod
    def create_tap_instance(
        self,
        config: t.ContainerMapping | None = None,
    ) -> FlextMeltanoSingerTapBase:
        """Create the singer_sdk Tap subclass instance.

        Consumer implements this with its domain-specific Tap class.
        """

    # ------------------------------------------------------------------
    # CLI dispatch
    # ------------------------------------------------------------------

    def cli_main(self, args: t.StrSequence | None = None) -> int:
        """Main CLI entry point — routes to Singer SDK tap.cli()."""
        try:
            tap = self._get_or_create_tap()
            command_args = list(args) if args else sys.argv[1:]
            tap.cli(args=command_args)
            return 0
        except SystemExit as exc:
            return exc.code if isinstance(exc.code, int) else 1
        except (ValueError, TypeError, OSError, RuntimeError) as exc:
            self.logger.exception("Tap CLI failed", error=str(exc))
            return 1

    # ------------------------------------------------------------------
    # Singer operations
    # ------------------------------------------------------------------

    def run_discover(self) -> r[t.StrSequence]:
        """Discover stream names from the tap."""
        try:
            tap = self._get_or_create_tap()
            streams = tap.discover_streams()
            stream_names: t.StrSequence = [str(s.name) for s in streams]
            self.logger.info(
                "Streams discovered",
                tap=self.tap_name,
                count=len(stream_names),
            )
            return r[t.StrSequence].ok(stream_names)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
        ) as exc:
            self.logger.exception("Discovery failed", error=str(exc))
            return r[t.StrSequence].fail(str(exc))

    def run_sync(self) -> r[str]:
        """Execute Singer sync via tap."""
        try:
            tap = self._get_or_create_tap()
            tap.sync_all()
            return r[str].ok(self.tap_name)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
        ) as exc:
            self.logger.exception("Sync failed", error=str(exc))
            return r[str].fail(str(exc))

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------

    def connect(self) -> r[bool]:
        """Connect to the data source. Override in consumer."""
        return r[bool].ok(value=True)

    def disconnect(self) -> r[None]:
        """Disconnect from the data source. Override in consumer."""
        return r[None].ok(None)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _get_or_create_tap(self) -> FlextMeltanoSingerTapBase:
        """Lazy-create and cache the tap instance."""
        if self._tap_instance is None:
            self._tap_instance = self.create_tap_instance()
        return self._tap_instance

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute tap service — returns status."""
        return r[t.Meltano.MeltanoConfigDict].ok({
            "service": self.tap_name,
            "status": c.CommonStatus.ACTIVE.value,
            "type": "tap",
        })


__all__ = ["FlextMeltanoTapServiceBase"]
