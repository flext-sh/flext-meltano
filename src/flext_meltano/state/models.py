"""FlextMeltano State Management Models.

State management data models following Clean Architecture patterns.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from flext_core import FlextResult
from pydantic import BaseModel, Field


class FlextMeltanoState(BaseModel):
    """Meltano state model with comprehensive validation.

    Represents the state of data extraction and processing.
    """

    bookmarks: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Stream bookmarks for incremental extraction",
    )

    currently_syncing: str | None = Field(
        default=None, description="Stream currently being synced",
    )

    schema_hash: str | None = Field(
        default=None, description="Hash of the schema for validation",
    )

    last_updated: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp of last state update",
    )

    version: str = Field(
        default="1.0",
        description="State format version",
        pattern=r"^\d+\.\d+$",
    )

    def get_stream_bookmark(self, stream_name: str) -> dict[str, Any] | None:
        """Get bookmark for specific stream.

        Args:
            stream_name: Name of the stream

        Returns:
            Stream bookmark or None if not found

        """
        return self.bookmarks.get(stream_name)

    def set_stream_bookmark(
        self, stream_name: str, bookmark: dict[str, Any],
    ) -> FlextResult[None]:
        """Set bookmark for specific stream.

        Args:
            stream_name: Name of the stream
            bookmark: Bookmark data to set

        Returns:
            FlextResult indicating success or failure

        """
        try:
            self.bookmarks[stream_name] = bookmark
            self.last_updated = datetime.now()
            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to set bookmark: {e}")

    def remove_stream_bookmark(self, stream_name: str) -> FlextResult[None]:
        """Remove bookmark for specific stream.

        Args:
            stream_name: Name of the stream

        Returns:
            FlextResult indicating success or failure

        """
        try:
            if stream_name in self.bookmarks:
                del self.bookmarks[stream_name]
                self.last_updated = datetime.now()

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to remove bookmark: {e}")

    def get_replication_key_value(self, stream_name: str, replication_key: str) -> Any:
        """Get replication key value for stream.

        Args:
            stream_name: Name of the stream
            replication_key: Name of the replication key field

        Returns:
            Replication key value or None if not found

        """
        bookmark = self.get_stream_bookmark(stream_name)
        if not bookmark:
            return None

        return bookmark.get("replication_key_value")

    def set_replication_key_value(
        self,
        stream_name: str,
        replication_key: str,
        value: Any,
    ) -> FlextResult[None]:
        """Set replication key value for stream.

        Args:
            stream_name: Name of the stream
            replication_key: Name of the replication key field
            value: Value to set

        Returns:
            FlextResult indicating success or failure

        """
        try:
            if stream_name not in self.bookmarks:
                self.bookmarks[stream_name] = {}

            self.bookmarks[stream_name].update(
                {
                    "replication_key": replication_key,
                    "replication_key_value": value,
                },
            )

            self.last_updated = datetime.now()
            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to set replication key value: {e}")

    def clear_bookmarks(self) -> FlextResult[None]:
        """Clear all stream bookmarks.

        Returns:
            FlextResult indicating success or failure

        """
        try:
            self.bookmarks.clear()
            self.currently_syncing = None
            self.last_updated = datetime.now()
            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to clear bookmarks: {e}")

    def get_streams_with_bookmarks(self) -> list[str]:
        """Get list of streams that have bookmarks.

        Returns:
            List of stream names with bookmarks

        """
        return list(self.bookmarks.keys())

    def is_stream_complete(self, stream_name: str) -> bool:
        """Check if a stream has completed sync.

        Args:
            stream_name: Name of the stream

        Returns:
            True if stream is complete, False otherwise

        """
        bookmark = self.get_stream_bookmark(stream_name)
        if not bookmark:
            return False

        complete_value = bookmark.get("complete", False)
        return bool(complete_value)

    def mark_stream_complete(self, stream_name: str) -> FlextResult[None]:
        """Mark a stream as complete.

        Args:
            stream_name: Name of the stream

        Returns:
            FlextResult indicating success or failure

        """
        try:
            if stream_name not in self.bookmarks:
                self.bookmarks[stream_name] = {}

            self.bookmarks[stream_name]["complete"] = True
            self.last_updated = datetime.now()

            # Clear currently_syncing if this was the active stream
            if self.currently_syncing == stream_name:
                self.currently_syncing = None

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to mark stream complete: {e}")

    def merge_state(self, other_state: FlextMeltanoState) -> FlextResult[None]:
        """Merge another state into this one.

        Args:
            other_state: State to merge

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Merge bookmarks, keeping the most recent values
            for stream_name, bookmark in other_state.bookmarks.items():
                if stream_name not in self.bookmarks:
                    self.bookmarks[stream_name] = bookmark
                else:
                    # Compare timestamps or replication key values to determine
                    # which bookmark is more recent
                    current_bookmark = self.bookmarks[stream_name]

                    # Simple merge strategy: use other state's bookmark if it has
                    # a replication key value and current doesn't, or if the
                    # replication key value is greater
                    other_rep_key = bookmark.get("replication_key_value")
                    current_rep_key = current_bookmark.get("replication_key_value")

                    if other_rep_key and (
                        not current_rep_key or other_rep_key > current_rep_key
                    ):
                        self.bookmarks[stream_name] = bookmark

            # Update last_updated to the most recent
            self.last_updated = max(self.last_updated, other_state.last_updated)

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to merge state: {e}")
