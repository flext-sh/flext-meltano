"""Base service for FLEXT tap consumer projects.

Provides Singer tap lifecycle via MRO: CLI dispatch, stream discovery,
sync execution, and connection management. Consumer taps subclass
``singer_sdk.Tap`` (required by Singer SDK) — this base wraps the tap
instance with FLEXT service patterns (``r[T]``, typed settings, lifecycle).

Consumer projects inherit this and override ``create_tap_instance()`` only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from abc import abstractmethod
from typing import Annotated, ClassVar, Self, override

from flext_core import FlextSettings
from flext_meltano import FlextMeltanoServiceBase, c, p, r, t, u


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
        u.Field(description="Canonical tap name (e.g. tap-oracle)"),
    ] = "tap"

    _tap_instance: p.Meltano.SingerTapInstance | None = u.PrivateAttr(default=None)
    _instance: ClassVar[Self | None] = None

    def __init__(
        self,
        settings: FlextSettings | t.RecursiveContainerMapping | None = None,
    ) -> None:
        """Expose the canonical settings bootstrap for tap facades."""
        super().__init__(settings=settings)

    @classmethod
    def get_instance(cls) -> Self:
        """Return the shared facade instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @abstractmethod
    def create_tap_instance(
        self,
        settings: t.RecursiveContainerMapping | None = None,
    ) -> p.Meltano.SingerTapInstance:
        """Create the singer_sdk Tap subclass instance.

        Consumer implements this with its domain-specific Tap class.
        """

    # ------------------------------------------------------------------
    # CLI dispatch
    # ------------------------------------------------------------------

    def cli_main(self, args: t.StrSequence | None = None) -> int:
        """Main CLI entry point through the internal Singer bridge."""
        try:
            tap = self._get_or_create_tap()
            command_args = list(args) if args else sys.argv[1:]
            return tap.run_cli(command_args, self.tap_name)
        except (ValueError, TypeError, OSError, RuntimeError) as exc:
            self.logger.exception("Tap CLI failed", error=str(exc))
            return 1

    # ------------------------------------------------------------------
    # Singer operations
    # ------------------------------------------------------------------

    def run_discover(self) -> p.Result[t.StrSequence]:
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

    def run_sync(self) -> p.Result[str]:
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

    def connect(self) -> p.Result[bool]:
        """Connect to the data source. Override in consumer."""
        return r[bool].ok(value=True)

    def disconnect(self) -> p.Result[None]:
        """Disconnect from the data source. Override in consumer."""
        return r[None].ok(None)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _get_or_create_tap(self) -> p.Meltano.SingerTapInstance:
        """Lazy-create and cache the tap instance."""
        if self._tap_instance is None:
            self._tap_instance = self.create_tap_instance()
        return self._tap_instance

    @override
    def execute(self) -> p.Result[t.RecursiveContainerMapping]:
        """Execute tap service — returns status."""
        return r[t.RecursiveContainerMapping].ok({
            "service": self.tap_name,
            "status": c.CommonStatus.ACTIVE.value,
            "type": "tap",
        })


__all__: list[str] = ["FlextMeltanoTapServiceBase"]
