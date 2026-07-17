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
from abc import ABC, abstractmethod
from typing import Annotated, override

from flext_meltano import (
    FlextMeltanoServiceBase,
    FlextMeltanoSettings,
    c,
    p,
    r,
    t,
    u,
)
from flext_meltano.services.declarative_tap import FlextMeltanoDeclarativeTap


class FlextMeltanoTapServiceBase(FlextMeltanoServiceBase, ABC):
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

    _tap_instance: p.Meltano.SingerTapInstance | None = u.PrivateAttr(
        default_factory=lambda: None,
    )

    def __init__(
        self,
        settings: FlextMeltanoSettings | None = None,
    ) -> None:
        """Expose the canonical settings bootstrap for tap facades."""
        super().__init__(runtime_settings=settings)

    @abstractmethod
    def create_tap_instance(
        self,
        settings: p.Settings | None = None,
    ) -> p.Meltano.SingerTapInstance:
        """Create the singer_sdk Tap subclass instance.

        Consumer implements this with its domain-specific Tap class.
        """

    # ------------------------------------------------------------------
    # CLI dispatch
    # ------------------------------------------------------------------

    def cli_main(self, args: t.StrSequence | None = None) -> int:
        """Run the main CLI entry point through the internal Singer bridge."""
        try:
            tap = self._get_or_create_tap()
            command_args = list(args) if args else sys.argv[1:]
            exit_code: int = tap.run_cli(command_args, self.tap_name)
            return exit_code
        except c.EXC_OS_RUNTIME_TYPE as exc:
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
            stream_names: t.StrSequence = [s.name for s in streams]
            self.logger.info(
                "Streams discovered",
                tap=self.tap_name,
                count=len(stream_names),
            )
            return r[t.StrSequence].ok(stream_names)
        except c.EXC_BROAD_RUNTIME_OS as exc:
            self.logger.exception("Discovery failed", error=str(exc))
            return r[t.StrSequence].fail(str(exc))

    def run_sync(self) -> p.Result[str]:
        """Execute Singer sync via tap."""
        try:
            tap = self._get_or_create_tap()
            tap.sync_all()
            return r[str].ok(self.tap_name)
        except c.EXC_BROAD_RUNTIME_OS as exc:
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

    @staticmethod
    def build_declarative_tap(
        spec: p.Meltano.TapSpec,
        fetcher: p.Meltano.RecordFetcher,
    ) -> p.Meltano.SingerTapInstance:
        """Build a flat-CLI Singer tap from declarative specs (no singer_sdk here).

        Declarative consumer taps override ``create_tap_instance`` with a single
        call to this helper, passing their ``m.Meltano.TapSpec`` and a
        ``p.Meltano.RecordFetcher``. ``flext-meltano`` owns every ``singer_sdk``
        detail behind ``FlextMeltanoDeclarativeTap``.
        """
        return FlextMeltanoDeclarativeTap.build(spec, fetcher)

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute tap service — returns status."""
        return r[t.JsonMapping].ok({
            "service": self.tap_name,
            "status": "active",
            "type": "tap",
        })


__all__: list[str] = ["FlextMeltanoTapServiceBase"]
