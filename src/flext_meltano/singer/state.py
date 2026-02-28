"""Singer State Management - Bookmark and incremental sync state handling.

This module provides state management for Singer incremental syncs with
FLEXT ecosystem patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import ClassVar, override

from flext_core import FlextResult, FlextService

from flext_meltano import FlextMeltanoConstants, FlextMeltanoModels, FlextMeltanoTypes

# Import aliases for simplified usage
t = FlextMeltanoTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels
r = FlextResult


class FlextMeltanoStateManager(FlextService[m.Meltano.SingerStateMessage]):
    """Manages Singer state (bookmarks, incremental sync state).

    Handles loading, updating, and persisting state for incremental
    syncs with proper error handling and FlextResult patterns.
    """

    # StateEntry is now canonical in m.Meltano.SingerStateEntry
    StateEntry: ClassVar[type[m.Meltano.SingerStateEntry]] = m.Meltano.SingerStateEntry

    def __init__(self) -> None:
        """Initialize state manager."""
        super().__init__()
        self._state_msg: m.Meltano.SingerStateMessage = m.Meltano.SingerStateMessage()

    def load_state(
        self, state_file: Path | None = None
    ) -> r[m.Meltano.SingerStateMessage]:
        """Load state from file or memory.

        Args:
        state_file: Path to state file (optional)

        Returns:
        FlextResult containing loaded state as SingerStateMessage

        """
        try:
            if state_file and state_file.exists():
                with state_file.open() as f:
                    self._state_msg = m.Meltano.SingerStateMessage.model_validate(
                        json.load(f),
                    )
                self.logger.info(
                    "State loaded from file",
                    file=str(state_file),
                    entries=len(self._state_msg.value),
                )
            return r[m.Meltano.SingerStateMessage].ok(self._state_msg)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to load state", error=str(e))
            return r[m.Meltano.SingerStateMessage].fail(f"Failed to load state: {e}")

    def save_state(self, state_file: Path) -> r[None]:
        """Save state to file.

        Args:
        state_file: Path to save state file

        Returns:
        FlextResult with success status

        """
        try:
            state_file.parent.mkdir(parents=True, exist_ok=True)
            with state_file.open("w", encoding="utf-8") as f:
                f.write(self._state_msg.model_dump_json(indent=2))
            self.logger.info(
                "State saved to file",
                file=str(state_file),
            )
            return r[None].ok(None)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to save state", error=str(e))
            return r[None].fail(f"Failed to save state: {e}")

    def update_bookmark(
        self,
        stream_name: str,
        bookmark_key: str,
        bookmark_value: str,
    ) -> r[None]:
        """Update bookmark for a stream.

        Args:
        stream_name: Name of the stream
        bookmark_key: Bookmark field name
        bookmark_value: New bookmark value

        Returns:
        FlextResult with success status

        """
        try:
            if stream_name not in self._state_msg.value:
                self._state_msg.value[stream_name] = {}

            stream_bookmarks = self._state_msg.value[stream_name]
            match stream_bookmarks:
                case dict():
                    stream_bookmarks[bookmark_key] = bookmark_value
                case _:
                    pass
            self.logger.debug(
                "Bookmark updated",
                stream=stream_name,
                key=bookmark_key,
            )
            return r[None].ok(None)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to update bookmark", error=str(e))
            return r[None].fail(f"Failed to update bookmark: {e}")

    def get_bookmark(self, stream_name: str, bookmark_key: str) -> r[str]:
        """Get current bookmark value.

        Args:
        stream_name: Name of the stream
        bookmark_key: Bookmark field name

        Returns:
        FlextResult containing bookmark value or None

        """
        try:
            stream_state = self._state_msg.value.get(stream_name)
            if stream_state is None:
                return r[str].fail(f"Stream state not found: {stream_name}")

            match stream_state:
                case dict():
                    pass
                case _:
                    return r[str].fail(f"Stream state for {stream_name} is not a dict")

            value = stream_state.get(bookmark_key)
            if value is None:
                return r[str].fail(
                    f"Bookmark not found: {stream_name}.{bookmark_key}",
                )
            return r[str].ok(str(value))
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to get bookmark", error=str(e))
            return r[str].fail(f"Failed to get bookmark: {e}")

    def to_state_message(self) -> m.Meltano.SingerStateMessage:
        """Return current state as SingerStateMessage."""
        return self._state_msg

    @override
    def execute(self, **_kwargs: t.JsonValue) -> r[m.Meltano.SingerStateMessage]:
        """Execute (implements Service pattern)."""
        return r[m.Meltano.SingerStateMessage].ok(self.to_state_message())


__all__ = [
    "FlextMeltanoStateManager",
]
