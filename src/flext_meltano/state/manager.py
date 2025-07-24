"""FlextMeltano State Manager.

State persistence and management following Clean Architecture patterns.
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from flext_core import FlextResult

from flext_meltano.state.models import FlextMeltanoState

if TYPE_CHECKING:
    from pathlib import Path


class FlextMeltanoStateManager:
    """State manager for Meltano operations.

    Handles state persistence, retrieval, and management for data pipelines.
    """

    def __init__(self, state_file_path: Path | None = None) -> None:
        """Initialize state manager.

        Args:
            state_file_path: Optional path to state file

        """
        self._state_file_path = state_file_path
        self._current_state: FlextMeltanoState | None = None

    @property
    def state_file_path(self) -> Path | None:
        """Get current state file path."""
        return self._state_file_path

    def set_state_file_path(self, path: Path) -> FlextResult[None]:
        """Set state file path.

        Args:
            path: Path to state file

        Returns:
            FlextResult indicating success or failure

        """
        try:
            self._state_file_path = path
            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to set state file path: {e}")

    def load_state(
        self, state_path: Path | None = None,
    ) -> FlextResult[FlextMeltanoState]:
        """Load state from file.

        Args:
            state_path: Optional path to state file (overrides instance path)

        Returns:
            FlextResult containing loaded state

        """
        try:
            file_path = state_path or self._state_file_path

            if not file_path:
                # Return empty state if no path specified
                state = FlextMeltanoState()
                self._current_state = state
                return FlextResult.ok(state)

            if not file_path.exists():
                # Return empty state if file doesn't exist
                state = FlextMeltanoState()
                self._current_state = state
                return FlextResult.ok(state)

            # Load state from JSON file
            import json

            with file_path.open() as f:
                state_data = json.load(f)

            state = FlextMeltanoState(**state_data)
            self._current_state = state

            return FlextResult.ok(state)

        except Exception as e:
            return FlextResult.fail(f"Failed to load state: {e}")

    def save_state(
        self,
        state: FlextMeltanoState | None = None,
        state_path: Path | None = None,
    ) -> FlextResult[None]:
        """Save state to file.

        Args:
            state: Optional state to save (uses current state if None)
            state_path: Optional path to save to (overrides instance path)

        Returns:
            FlextResult indicating success or failure

        """
        try:
            file_path = state_path or self._state_file_path
            state_to_save = state or self._current_state

            if not file_path:
                return FlextResult.fail("No state file path specified")

            if not state_to_save:
                return FlextResult.fail("No state to save")

            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Save state as JSON
            import json

            with file_path.open("w") as f:
                json.dump(
                    state_to_save.model_dump(),
                    f,
                    indent=2,
                    default=str,  # Handle datetime serialization
                )

            # Update current state if we saved a different one
            if state:
                self._current_state = state

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to save state: {e}")

    def get_current_state(self) -> FlextResult[FlextMeltanoState]:
        """Get current state.

        Returns:
            FlextResult containing current state

        """
        try:
            if self._current_state is None:
                # Try to load from file first
                load_result = self.load_state()
                if not load_result.is_success:
                    return load_result

                loaded_state = load_result.data
                if loaded_state is None:
                    return FlextResult.fail("Failed to load state data")
                return FlextResult.ok(loaded_state)

            return FlextResult.ok(self._current_state)

        except Exception as e:
            return FlextResult.fail(f"Failed to get current state: {e}")

    def update_state(self, state: FlextMeltanoState) -> FlextResult[None]:
        """Update current state and optionally persist.

        Args:
            state: New state to set

        Returns:
            FlextResult indicating success or failure

        """
        try:
            self._current_state = state

            # Auto-save if we have a file path
            if self._state_file_path:
                save_result = self.save_state()
                if not save_result.is_success:
                    return save_result

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to update state: {e}")

    def reset_state(self) -> FlextResult[None]:
        """Reset state to empty state.

        Returns:
            FlextResult indicating success or failure

        """
        try:
            new_state = FlextMeltanoState()
            return self.update_state(new_state)

        except Exception as e:
            return FlextResult.fail(f"Failed to reset state: {e}")

    def backup_state(self, backup_path: Path) -> FlextResult[None]:
        """Create backup of current state.

        Args:
            backup_path: Path to save backup

        Returns:
            FlextResult indicating success or failure

        """
        try:
            current_state_result = self.get_current_state()
            if not current_state_result.is_success:
                return FlextResult.fail(
                    f"Failed to get current state for backup: "
                    f"{current_state_result.error}",
                )

            return self.save_state(current_state_result.data, backup_path)

        except Exception as e:
            return FlextResult.fail(f"Failed to backup state: {e}")

    def restore_state(self, backup_path: Path) -> FlextResult[None]:
        """Restore state from backup.

        Args:
            backup_path: Path to backup file

        Returns:
            FlextResult indicating success or failure

        """
        try:
            load_result = self.load_state(backup_path)
            if not load_result.is_success:
                return FlextResult.fail(
                    f"Failed to load backup state: {load_result.error}",
                )

            restored_state = load_result.data
            if restored_state is None:
                return FlextResult.fail("Failed to restore state: no data loaded")
            return self.update_state(restored_state)

        except Exception as e:
            return FlextResult.fail(f"Failed to restore state: {e}")

    def merge_state_from_file(self, other_state_path: Path) -> FlextResult[None]:
        """Merge state from another state file.

        Args:
            other_state_path: Path to other state file

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Load other state
            other_state_result = self.load_state(other_state_path)
            if not other_state_result.is_success:
                return FlextResult.fail(
                    f"Failed to load other state: {other_state_result.error}",
                )

            # Get current state
            current_state_result = self.get_current_state()
            if not current_state_result.is_success:
                return FlextResult.fail(
                    f"Failed to get current state: {current_state_result.error}",
                )

            # Merge states
            current_state = current_state_result.data
            other_state = other_state_result.data

            if current_state is None:
                return FlextResult.fail("Failed to get current state for merge")
            if other_state is None:
                return FlextResult.fail("Failed to get other state for merge")

            merge_result = current_state.merge_state(other_state)
            if not merge_result.is_success:
                return merge_result

            # Update with merged state
            return self.update_state(current_state)

        except Exception as e:
            return FlextResult.fail(f"Failed to merge state: {e}")

    # Async compatibility methods for backward compatibility with orchestrator
    async def get_state_async(self, job_name: str) -> FlextResult[FlextMeltanoState]:
        """Async wrapper for loading state by job name.

        Args:
            job_name: Name of the job to get state for

        Returns:
            FlextResult containing the state

        """
        # Run the sync version in thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.load_state())

    async def set_state_async(
        self, job_name: str, state: FlextMeltanoState,
    ) -> FlextResult[None]:
        """Async wrapper for saving state by job name.

        Args:
            job_name: Name of the job to save state for
            state: State object to save

        Returns:
            FlextResult indicating success/failure

        """
        # Run the sync version in thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.save_state(state))
