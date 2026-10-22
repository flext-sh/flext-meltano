"""Base service for FLEXT tap consumer projects.

Provides Singer tap lifecycle via MRO: CLI dispatch and declarative tap
construction. Consumer taps subclass
``singer_sdk.Tap`` (required by Singer SDK) — this base wraps the tap
instance with FLEXT service patterns (``r[T]``, typed settings, lifecycle).

Consumer projects inherit this and override ``create_tap_instance()`` only.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from typing import Annotated, override

from flext_meltano import FlextMeltanoServiceBase, c, m, p, r, t
from flext_meltano.services import FlextMeltanoDeclarativeTap


class FlextMeltanoTapServiceBase(FlextMeltanoServiceBase, ABC):
    """Base for all FLEXT tap service projects.

    Subclasses MUST define:
    - ``tap_name``: canonical tap identifier (e.g. ``"tap-oracle"``)
    - ``create_tap_instance()``: factory returning the singer_sdk Tap subclass

    This base provides via MRO:
    - CLI dispatch (``cli_main``)
    - Declarative tap construction (``build_declarative_tap``)
    """

    tap_name: Annotated[
        t.NonEmptyStr,
        m.Field(description="Canonical tap name (e.g. tap-oracle)"),
    ] = "tap"

    _tap_instance: p.Meltano.SingerTapInstance | None = m.PrivateAttr(
        default_factory=lambda: None,
    )

    def __init__(self, settings: p.Settings | None = None) -> None:
        """Expose the canonical settings bootstrap for tap facades."""
        super().__init__(runtime_settings=settings)

    @abstractmethod
    def create_tap_instance(
        self,
        _settings: p.Settings | None = None,
    ) -> p.Meltano.SingerTapInstance:
        """Create the singer_sdk Tap subclass instance.

        Consumer implements this with its domain-specific Tap class.
        """

    # ------------------------------------------------------------------
    # CLI dispatch
    # ------------------------------------------------------------------

    def cli_main(self, args: t.StrSequence | None = None) -> int:
        """Run the main CLI entry point through the internal Singer bridge.

        Returns:
            The resulting ``int``.

        Raises:
            SystemExit: If a ``c.EXC_OS_RUNTIME_TYPE`` is caught.

        """
        try:
            tap = self._get_or_create_tap()
            command_args = list(args) if args else sys.argv[1:]
            exit_code: int = tap.run_cli(command_args, self.tap_name)
        except c.EXC_OS_RUNTIME_TYPE as exc:
            self.logger.exception("Tap CLI failed", error=str(exc))
            raise SystemExit(1) from exc
        else:
            return exit_code

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _get_or_create_tap(self) -> p.Meltano.SingerTapInstance:
        """Lazy-create and cache the tap instance.

        Returns:
            The resulting ``p.Meltano.SingerTapInstance``.

        """
        if self._tap_instance is None:
            self._tap_instance = self.create_tap_instance()
        return self._tap_instance

    @staticmethod
    def build_declarative_tap(
        spec: m.Meltano.TapSpec,
        fetcher: p.Meltano.RecordFetcher,
    ) -> p.Meltano.SingerTapInstance:
        """Build a flat-CLI Singer tap from declarative specs (no singer_sdk here).

        Declarative consumer taps override ``create_tap_instance`` with a single
        call to this helper, passing their ``m.Meltano.TapSpec`` and a
        ``p.Meltano.RecordFetcher``. ``flext-meltano`` owns every ``singer_sdk``
        detail behind ``FlextMeltanoDeclarativeTap``.

        Returns:
            The resulting ``p.Meltano.SingerTapInstance``.

        """
        return FlextMeltanoDeclarativeTap.build(spec, fetcher)

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute tap service — returns status.

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """
        return r[t.JsonMapping].ok({
            "service": self.tap_name,
            "status": "active",
            "type": "tap",
        })


__all__: list[str] = ["FlextMeltanoTapServiceBase"]
