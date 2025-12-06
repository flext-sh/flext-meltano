"""Singer State Management - Bookmark and incremental sync state handling.

This module provides state management for Singer incremental syncs with
FLEXT ecosystem patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from flext_core import FlextResult, FlextService
from pydantic import Field, model_validator

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import FlextMeltanoTypes

# Import aliases for simplified usage
# u is already imported from flext_core
t = FlextMeltanoTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels
r = FlextResult
s = FlextService


class FlextMeltanoStateManager(FlextService[dict[str, object]]):
    """Manages Singer state (bookmarks, incremental sync state).

    Handles loading, updating, and persisting state for incremental
    syncs with proper error handling and FlextResult patterns.
    """

    class StateEntry(m):
        """Singer state entry for a stream."""

        stream_name: str = Field(description="Name of the stream")
        bookmark_key: str | None = Field(
            default=None,
            description="Bookmark field for incremental",
        )
        bookmark_value: str | None = Field(
            default=None,
            description="Current bookmark value",
        )
        updated_at: datetime = Field(
            default_factory=datetime.now,
            description="Last update time",
        )

        @model_validator(mode="after")
        def validate_bookmark(self) -> FlextMeltanoStateManager.StateEntry:
            """Ensure bookmark_key and bookmark_value are both set or both None."""
            if (self.bookmark_key is None) != (self.bookmark_value is None):
                msg = "bookmark_key and bookmark_value must both be set or both be None"
                raise ValueError(msg)
            return self

    def __init__(self) -> None:
        """Initialize state manager."""
        super().__init__()
        self._state: dict[str, object] = {}

    def load_state(self, state_file: Path | None = None) -> r[dict[str, object]]:
        """Load state from file or memory.

        Args:
        state_file: Path to state file (optional)

        Returns:
        FlextResult containing loaded state dictionary

        """
        try:
            if state_file and state_file.exists():
                with state_file.open() as f:
                    self._state = json.load(f)
                self.logger.info(
                    "State loaded from file",
                    file=str(state_file),
                    entries=len(self._state),
                )
            return r[dict[str, object]].ok(self._state)
        except Exception as e:
            self.logger.exception("Failed to load state", error=str(e))
            return r[dict[str, object]].fail(f"Failed to load state: {e}")

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
                json.dump(self._state, f, indent=2, default=str)
            self.logger.info(
                "State saved to file",
                file=str(state_file),
            )
            return r[None].ok(None)
        except Exception as e:
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
            if stream_name not in self._state:
                self._state[stream_name] = {}

            self._state[stream_name][bookmark_key] = bookmark_value
            self.logger.debug(
                "Bookmark updated",
                stream=stream_name,
                key=bookmark_key,
            )
            return r[None].ok(None)
        except Exception as e:
            self.logger.exception("Failed to update bookmark", error=str(e))
            return r[None].fail(f"Failed to update bookmark: {e}")

    def get_bookmark(self, stream_name: str, bookmark_key: str) -> r[str | None]:
        """Get current bookmark value.

        Args:
        stream_name: Name of the stream
        bookmark_key: Bookmark field name

        Returns:
        FlextResult containing bookmark value or None

        """
        try:
            if stream_name in self._state:
                value = self._state[stream_name].get(bookmark_key)
                return r[str | None].ok(value)
            return r[str | None].ok(None)
        except Exception as e:
            self.logger.exception("Failed to get bookmark", error=str(e))
            return r[str | None].fail(f"Failed to get bookmark: {e}")

    def execute(self, **_kwargs: object) -> r[dict[str, object]]:
        """Execute (implements Domain.Service pattern)."""
        return r[dict[str, object]].ok(self._state)


__all__ = [
    "FlextMeltanoStateManager",
]
