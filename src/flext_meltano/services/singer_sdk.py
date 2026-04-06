"""Singer SDK bridge — canonical re-exports for consumer projects.

Direct re-exports from singer_sdk (allowed in flext-meltano/src/)
so that mypy recognizes them as valid types for subclassing.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

import click
from singer_sdk import Sink
from singer_sdk.helpers.types import Context, Record
from singer_sdk.streams import Stream
from singer_sdk.tap_base import Tap
from singer_sdk.target_base import Target

from flext_meltano import p, t


class _SingerTapSdkBackend(Protocol):
    """Raw Singer SDK tap surface consumed by the FLEXT bridge."""

    @classmethod
    def get_singer_command(cls) -> click.Command:
        """Return the Singer SDK command bound to the tap type."""
        ...

    @property
    def config(self) -> t.ContainerMapping:
        """Expose the normalized tap configuration."""
        ...

    def discover_streams(self) -> Sequence[p.Meltano.SingerStreamInfo]:
        """Return the tap streams."""
        ...

    def sync_all(self) -> None:
        """Run a full Singer sync."""
        ...


class FlextMeltanoSingerTapAdapter:
    """Bridge a Singer SDK tap instance into FLEXT's internal runtime contract."""

    def __init__(self, tap: _SingerTapSdkBackend) -> None:
        """Store the raw Singer tap instance used by the bridge."""
        self._tap = tap

    @property
    def config(self) -> t.ContainerMapping:
        """Expose the tap configuration through the internal contract."""
        return self._tap.config

    def run_cli(
        self,
        args: t.StrSequence,
        prog_name: str,
    ) -> int:
        """Execute the Singer CLI and normalize ``SystemExit`` into an int."""
        try:
            singer_command = self._tap.get_singer_command()
            _ = singer_command.main(args=list(args), prog_name=prog_name)
            return 0
        except SystemExit as exc:
            return exc.code if isinstance(exc.code, int) else 1

    def discover_streams(self) -> Sequence[p.Meltano.SingerStreamInfo]:
        """Delegate stream discovery to the raw Singer tap."""
        return self._tap.discover_streams()

    def sync_all(self) -> None:
        """Delegate sync execution to the raw Singer tap."""
        self._tap.sync_all()


__all__: t.StrSequence = [
    "Context",
    "FlextMeltanoSingerTapAdapter",
    "Record",
    "Sink",
    "Stream",
    "Tap",
    "Target",
]
