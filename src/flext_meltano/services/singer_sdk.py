"""Singer SDK bridge for FLEXT tap service runtimes.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from singer_sdk.tap_base import Tap


class FlextMeltanoSingerTapAdapter:
    """Bridge a Singer SDK tap instance into the internal Meltano tap contract."""

    def __init__(self, tap: Tap) -> None:
        """Store the raw Singer tap instance used by the bridge."""
        self._tap = tap

    def run_cli(self, args: Sequence[str], prog_name: str) -> int:
        """Execute the Singer CLI and normalize ``SystemExit`` into an int.

        Returns:
            The resulting ``int``.

        """
        try:
            singer_command = self._tap.get_singer_command()
            _ = singer_command.main(args=list(args), prog_name=prog_name)
        except SystemExit as exc:
            return exc.code if isinstance(exc.code, int) else 1
        else:
            return 0


__all__: list[str] = ["FlextMeltanoSingerTapAdapter"]
