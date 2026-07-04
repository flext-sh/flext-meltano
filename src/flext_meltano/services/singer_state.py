"""Singer State Management — MRO mixin for FlextMeltano facade.

Provides bookmark and incremental sync state handling.
Converted from standalone FlextMeltanoStateManager to facade mixin.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_cli import cli
from flext_meltano import FlextMeltanoServiceBase, c, e, m, p, r, u

if TYPE_CHECKING:
    from pathlib import Path


class FlextMeltanoSingerStateMixin(FlextMeltanoServiceBase):
    """Singer state management mixin for MRO composition on FlextMeltano.

    Handles loading, updating, and persisting state for incremental
    syncs with proper error handling and r patterns.
    """

    _singer_state: m.Meltano.SingerStateMessage = u.PrivateAttr(
        default_factory=m.Meltano.SingerStateMessage,
    )

    def fetch_bookmark(self, stream_name: str, bookmark_key: str) -> p.Result[str]:
        """Get current bookmark value for a stream."""
        try:
            stream_state = self._singer_state.value.get(stream_name)
            if stream_state is None:
                return e.fail_not_found("Stream state", stream_name, result_type=r[str])
            if not isinstance(stream_state, dict):
                return e.fail_validation(
                    f"Stream state for {stream_name} is not a dict",
                    result_type=r[str],
                )
            value = stream_state.get(bookmark_key)
            if value is None:
                return e.fail_not_found(
                    "Bookmark",
                    f"{stream_name}.{bookmark_key}",
                    result_type=r[str],
                )
            return r[str].ok(str(value))
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            self.logger.exception("Failed to get bookmark", error=str(exc))
            return e.fail_operation("get bookmark", exc, result_type=r[str])

    def load_state(
        self,
        state_file: Path | None = None,
    ) -> p.Result[m.Meltano.SingerStateMessage]:
        """Load state from file or return in-memory state."""
        try:
            if state_file and state_file.exists():
                load_result = u.Cli.files_read_json_model(
                    state_file,
                    m.Meltano.SingerStateMessage,
                )
                if load_result.failure:
                    return r[m.Meltano.SingerStateMessage].fail(
                        load_result.error or "state read failed",
                    )
                self._singer_state = load_result.value
                self.logger.info(
                    "State loaded from file",
                    file=str(state_file),
                    entries=len(self._singer_state.value),
                )
            return r[m.Meltano.SingerStateMessage].ok(self._singer_state)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            self.logger.exception("Failed to load state", error=str(exc))
            return e.fail_operation(
                "load state",
                exc,
                result_type=r[m.Meltano.SingerStateMessage],
            )

    def save_state(self, state_file: Path) -> p.Result[None]:
        """Save state to file."""
        try:
            state_file.parent.mkdir(parents=True, exist_ok=True)
            write_result = cli.atomic_write_text_file(
                state_file,
                self._singer_state.model_dump_json(indent=2),
            )
            if write_result.failure:
                return r[None].fail(write_result.error or "state write failed")
            self.logger.info("State saved to file", file=str(state_file))
            return r[None].ok(None)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            self.logger.exception("Failed to save state", error=str(exc))
            return e.fail_operation("save state", exc, result_type=r[None])

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

        def _run_update_bookmark() -> p.Result[None]:
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

        try:
            return _run_update_bookmark()
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            self.logger.exception("Failed to update bookmark", error=str(exc))
            return e.fail_operation("update bookmark", exc, result_type=r[None])


__all__: list[str] = ["FlextMeltanoSingerStateMixin"]
