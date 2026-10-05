"""Singer SDK bridge for FLEXT tap service runtimes.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import cast

from singer_sdk import Sink
from singer_sdk.streams import Stream
from singer_sdk.tap_base import Tap
from singer_sdk.target_base import Target

from flext_meltano import c, m, p, t


class FlextMeltanoSingerTapAdapter:
    """Bridge a Singer SDK tap instance into the internal Meltano tap contract."""

    def __init__(self, tap: Tap) -> None:
        """Store the raw Singer tap instance used by the bridge."""
        self._tap = tap

    @property
    def settings(self) -> t.JsonMapping:
        """Expose tap configuration through the internal runtime contract."""
        # Why: the Singer SDK Tap declares neither attribute in its typed
        # surface; the candidates are read as unknown objects and narrowed to
        # the declared mapping contract through isinstance.
        # Why: the Singer SDK Tap declares neither attribute in its typed
        # surface; the candidates are read as JSON values, guarded with
        # isinstance, and re-declared at the contract mapping type.
        config_candidate: t.JsonValue | None = getattr(self._tap, "config", None)
        settings_candidate: t.JsonValue | None = getattr(self._tap, "settings", {})
        empty_source: t.MappingKV[str, t.JsonPayload] = {}
        source: Mapping[str, t.JsonPayload]
        if isinstance(config_candidate, Mapping):
            source = cast("Mapping[str, t.JsonPayload]", config_candidate)
        elif isinstance(settings_candidate, Mapping):
            source = cast("Mapping[str, t.JsonPayload]", settings_candidate)
        else:
            source = empty_source
        normalized: t.JsonDict = {}
        for key, value in source.items():
            normalized[key] = self._normalize_recursive(value)
        return normalized

    @staticmethod
    def _normalize_recursive(value: t.JsonPayload | t.JsonValue) -> t.JsonValue:
        """Normalize Singer config values into canonical CLI JSON values.

        Returns:
            The resulting ``t.JsonValue``.
        """
        if value is None:
            return None
        if isinstance(value, m.BaseModel):
            normalized_model = value.model_dump(mode="json")
            return {
                key: FlextMeltanoSingerTapAdapter._normalize_recursive(model_value)
                for key, model_value in normalized_model.items()
            }
        if isinstance(value, Mapping):
            return {
                key: FlextMeltanoSingerTapAdapter._normalize_recursive(mapping_value)
                for key, mapping_value in value.items()
            }
        if isinstance(value, Sequence) and not isinstance(value, c.STR_BYTES_TYPES):
            return [
                FlextMeltanoSingerTapAdapter._normalize_recursive(sequence_value)
                for sequence_value in value
            ]
        return t.Cli.JSON_VALUE_ADAPTER.validate_python(value)

    def run_cli(self, args: t.StrSequence, prog_name: str) -> int:
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

    def discover_streams(self) -> t.SequenceOf[p.Meltano.SingerStreamInfo]:
        """Delegate stream discovery to the raw Singer tap.

        Returns:
            The resulting ``t.SequenceOf[p.Meltano.SingerStreamInfo]``.
        """
        streams: t.SequenceOf[p.Meltano.SingerStreamInfo] = self._tap.discover_streams()
        return streams

    def sync_all(self) -> None:
        """Delegate sync execution to the raw Singer tap."""
        self._tap.sync_all()


__all__: list[str] = ["FlextMeltanoSingerTapAdapter", "Sink", "Stream", "Tap", "Target"]
