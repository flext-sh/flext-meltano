"""Singer State Management — MRO mixin for FlextMeltano facade.

Provides bookmark and incremental sync state handling.
Converted from standalone FlextMeltanoStateManager to facade mixin.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_cli import cli

from flext_meltano import FlextMeltanoServiceBase, c, m, p, r, u


class FlextMeltanoSingerStateMixin(FlextMeltanoServiceBase):
    """Singer state management mixin for MRO composition on FlextMeltano.

    Handles loading, updating, and persisting state for incremental
    syncs with proper error handling and r patterns.
    """

    _singer_state: m.Meltano.SingerStateMessage = u.PrivateAttr(
        default_factory=m.Meltano.SingerStateMessage,
    )

    def get_bookmark(self, stream_name: str, bookmark_key: str) -> p.Result[str]:
        """Get current bookmark value for a stream."""
        try:
            stream_state = self._singer_state.value.get(stream_name)
            if stream_state is None:
                return r[str].fail(f"Stream state not found: {stream_name}")
            if not isinstance(stream_state, dict):
                return r[str].fail(f"Stream state for {stream_name} is not a dict")
            value = stream_state.get(bookmark_key)
            if value is None:
                return r[str].fail(f"Bookmark not found: {stream_name}.{bookmark_key}")
            return r[str].ok(str(value))
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Failed to get bookmark", error=str(e))
            return r[str].fail(f"Failed to get bookmark: {e}")

    def load_state(
        self,
        state_file: Path | None = None,
    ) -> p.Result[m.Meltano.SingerStateMessage]:
        """Load state from file or return in-memory state."""
        try:
            if state_file and state_file.exists():
                load_result = cli.read_json_model(
                    state_file, m.Meltano.SingerStateMessage
                )
                if load_result.failure:
                    return r[m.Meltano.SingerStateMessage].fail(str(load_result.error))
                self._singer_state = load_result.value
                self.logger.info(
                    "State loaded from file",
                    file=str(state_file),
                    entries=len(self._singer_state.value),
                )
            return r[m.Meltano.SingerStateMessage].ok(self._singer_state)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Failed to load state", error=str(e))
            return r[m.Meltano.SingerStateMessage].fail(f"Failed to load state: {e}")

    def save_state(self, state_file: Path) -> p.Result[None]:
        """Save state to file."""
        try:
            state_file.parent.mkdir(parents=True, exist_ok=True)
            write_result = cli.write_text_file(
                state_file, self._singer_state.model_dump_json(indent=2)
            )
            if write_result.failure:
                return r[None].fail(str(write_result.error))
            self.logger.info("State saved to file", file=str(state_file))
            return r[None].ok(None)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Failed to save state", error=str(e))
            return r[None].fail(f"Failed to save state: {e}")

    def to_state_message(self) -> m.Meltano.SingerStateMessage:
        """Return current state as SingerStateMessage."""
        return self._singer_state

    def update_bookmark(
        self,
        stream_name: str,
        bookmark_key: str,
        bookmark_value: str,
    ) -> p.Result[None]:
        """Update bookmark for a stream."""
        try:
            self._singer_state.value.setdefault(stream_name, {})
            stream_bookmarks = self._singer_state.value[stream_name]
            match stream_bookmarks:
                case dict():
                    stream_bookmarks[bookmark_key] = bookmark_value
                case _:
                    self.logger.warning(
                        "Stream state is not a dict, cannot update bookmark",
                        stream=stream_name,
                        state_type=type(stream_bookmarks).__name__,
                    )
            self.logger.debug("Bookmark updated", stream=stream_name, key=bookmark_key)
            return r[None].ok(None)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Failed to update bookmark", error=str(e))
            return r[None].fail(f"Failed to update bookmark: {e}")


__all__: list[str] = ["FlextMeltanoSingerStateMixin"]
