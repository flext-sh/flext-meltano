"""Singer SDK bridge — canonical re-exports for consumer projects.

Direct re-exports from singer_sdk (allowed in flext-meltano/src/)
so that mypy recognizes them as valid types for subclassing.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol

import click
from singer_sdk import Sink
from singer_sdk.helpers.types import Context, Record
from singer_sdk.streams import Stream
from singer_sdk.tap_base import Tap
from singer_sdk.target_base import Target

from flext_meltano import m, p, t


class _SingerTapSdkBackend(Protocol):
    """Raw Singer SDK tap surface consumed by the FLEXT bridge."""

    @classmethod
    def get_singer_command(cls) -> click.Command:
        """Return the Singer SDK command bound to the tap type."""
        ...

    @property
    def config(self) -> Mapping[str, t.ValueOrModel]:
        """Expose the raw tap configuration."""
        ...

    def discover_streams(self) -> Sequence[p.Meltano.SingerStreamInfo]:
        """Return the tap streams."""
        ...

    def sync_all(self) -> None:
        """Run a full Singer sync."""
        ...


class _SingerTapSettingsBackend(Protocol):
    """Legacy tap backend contract exposing ``settings`` only."""

    @classmethod
    def get_singer_command(cls) -> click.Command:
        """Return the Singer SDK command bound to the tap type."""
        ...

    @property
    def settings(self) -> Mapping[str, t.ValueOrModel]:
        """Expose tap settings mapping."""
        ...

    def discover_streams(self) -> Sequence[p.Meltano.SingerStreamInfo]:
        """Return the tap streams."""
        ...

    def sync_all(self) -> None:
        """Run a full Singer sync."""
        ...


class FlextMeltanoSingerTapAdapter:
    """Bridge a Singer SDK tap instance into FLEXT's internal runtime contract."""

    def __init__(
        self,
        tap: _SingerTapSdkBackend | _SingerTapSettingsBackend,
    ) -> None:
        """Store the raw Singer tap instance used by the bridge."""
        self._tap = tap

    @property
    def settings(self) -> t.RecursiveContainerMapping:
        """Expose the tap configuration through the internal contract."""
        config_source = getattr(self._tap, "config", None)
        empty_source: Mapping[str, t.ValueOrModel] = {}
        if isinstance(config_source, Mapping):
            source = config_source
        else:
            settings_source = getattr(self._tap, "settings", {})
            source = (
                settings_source
                if isinstance(settings_source, Mapping)
                else empty_source
            )
        normalized: dict[str, t.RecursiveContainer] = {}
        for key, value in source.items():
            normalized[str(key)] = self._normalize_recursive(value)
        return normalized

    @staticmethod
    def _normalize_recursive(value: t.ValueOrModel) -> t.RecursiveContainer:
        """Normalize Singer config values into recursive container contracts."""
        if isinstance(value, t.CONTAINER_TYPES):
            return value
        if value is None:
            return None
        if isinstance(value, m.BaseModel):
            normalized_model = value.model_dump(mode="json")
            return {
                str(key): FlextMeltanoSingerTapAdapter._normalize_recursive(model_value)
                for key, model_value in normalized_model.items()
            }
        if isinstance(value, Mapping):
            return {
                str(key): FlextMeltanoSingerTapAdapter._normalize_recursive(
                    mapping_value
                )
                for key, mapping_value in value.items()
            }
        if isinstance(value, Sequence) and not isinstance(value, str):
            return [
                FlextMeltanoSingerTapAdapter._normalize_recursive(sequence_value)
                for sequence_value in value
            ]
        return str(value)

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
