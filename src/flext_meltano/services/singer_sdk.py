"""Singer SDK bridge — canonical re-exports for consumer projects.

Direct re-exports from singer_sdk (allowed in flext-meltano/src/)
so that mypy recognizes them as valid types for subclassing.
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)

from singer_sdk import Sink
from singer_sdk.helpers.types import Context, Record
from singer_sdk.streams import Stream
from singer_sdk.tap_base import Tap
from singer_sdk.target_base import Target

from flext_meltano import m, p, t


class FlextMeltanoSingerTapAdapter:
    """Bridge a Singer SDK tap instance into FLEXT's internal runtime contract."""

    def __init__(
        self,
        tap: p.Meltano.SingerTapSdkBackend | p.Meltano.SingerTapSettingsBackend,
    ) -> None:
        """Store the raw Singer tap instance used by the bridge."""
        self._tap = tap

    @property
    def settings(self) -> t.JsonMapping:
        """Expose the tap configuration through the internal contract."""
        config_source = getattr(self._tap, "config", None)
        empty_source: Mapping[str, t.JsonPayload] = {}
        if isinstance(config_source, Mapping):
            source = config_source
        else:
            settings_source = getattr(self._tap, "settings", {})
            source = (
                settings_source
                if isinstance(settings_source, Mapping)
                else empty_source
            )
        normalized: dict[str, t.JsonValue] = {}
        for key, value in source.items():
            normalized[str(key)] = self._normalize_recursive(value)
        return normalized

    @staticmethod
    def _normalize_recursive(
        value: t.JsonPayload | t.JsonValue,
    ) -> t.JsonValue:
        """Normalize Singer config values into canonical CLI JSON values."""
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
        return t.Cli.JSON_VALUE_ADAPTER.validate_python(value)

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
