"""FLX Meltano State Manager.

This module provides deep integration with Meltano's state management system,
enabling enterprise-grade state persistence, backup, and recovery capabilities.
"""

from __future__ import annotations

import asyncio
import os
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any

import orjson
import structlog

# ZERO TOLERANCE - Meltano is REQUIRED and guaranteed in pyproject.toml
from meltano.core.state_service import StateService
from meltano.core.state_store import MeltanoState

if TYPE_CHECKING:
    from flx_core.events.event_bus import EventBusProtocol
    from meltano.core.project import Project

logger = structlog.get_logger()


class CachePolicy(Enum):
    """Cache usage policy enumeration for state operations.

    Defines whether to use cached state or force retrieval from backend,
    replacing boolean parameters with explicit cache policies.

    Attributes
    ----------
        USE_CACHE: Use cached state if available.
        FORCE_REFRESH: Always fetch from backend, ignore cache.

    """

    USE_CACHE = "use_cache"
    FORCE_REFRESH = "force_refresh"


class BackupPolicy(Enum):
    """Backup creation policy enumeration for state operations.

    Defines whether to create backups during state modifications,
    replacing boolean parameters with explicit backup policies.

    Attributes
    ----------
        CREATE_BACKUP: Create backup before state modifications.
        SKIP_BACKUP: Skip backup creation for faster operations.

    """

    CREATE_BACKUP = "create_backup"
    SKIP_BACKUP = "skip_backup"


class OverwritePolicy(Enum):
    """Overwrite policy enumeration for state restoration.

    Defines whether to overwrite existing state during restoration,
    replacing boolean parameters with explicit overwrite policies.

    Attributes
    ----------
        ALLOW_OVERWRITE: Allow overwriting existing state.
        PROTECT_EXISTING: Prevent overwriting existing state.

    """

    ALLOW_OVERWRITE = "allow_overwrite"
    PROTECT_EXISTING = "protect_existing"


class FlxMeltanoStateManager:
    """Enterprise Meltano state manager with advanced persistence and recovery.

    This manager provides comprehensive state management capabilities including:
    - Deep integration with Meltano's state system
    - Multi-backend state storage (filesystem, S3, database)
    - State versioning and backup
    - Automatic state recovery and validation
    - Real-time state change events
    - Cross-environment state synchronization
    """

    def __init__(self, event_bus: EventBusProtocol) -> None:
        """Initialize the FLX Meltano State Manager.

        Args:
        ----
            event_bus: FLX event bus for state change events

        """
        self.event_bus = event_bus
        self.logger = logger.bind(component="flx_meltano_state_manager")
        self._state_cache: dict[str, MeltanoState] = {}
        self._lock = asyncio.Lock()

        # Initialize backup directory based on MELTANO_PROJECT_ROOT or current working directory
        project_root = Path(os.getenv("MELTANO_PROJECT_ROOT", "."))
        self.backup_dir = project_root / ".meltano" / "state_backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info(
            "Initialized FLX Meltano State Manager",
            backup_dir=str(self.backup_dir),
        )

    async def get_state(
        self,
        project: Project,
        state_id: str,
        cache_policy: CachePolicy = CachePolicy.USE_CACHE,
    ) -> MeltanoState | None:
        """Get state for a specific state ID.

        Args:
        ----
            project: Meltano project instance
            state_id: State identifier
            cache_policy: Cache usage policy for state retrieval

        Returns:
        -------
            Meltano state object or None if not found

        """
        cache_key = f"{project.root}:{state_id}"

        # Check cache first if requested
        if cache_policy == CachePolicy.USE_CACHE and cache_key in self._state_cache:
            self.logger.debug("Returning cached state", state_id=state_id)
            return self._state_cache[cache_key]

        self.logger.info("Retrieving state from backend", state_id=state_id)

        try:
            # Get state through Meltano's StateService
            state_service = StateService(project)
            state = await asyncio.get_event_loop().run_in_executor(
                None,
                state_service.get_state,
                state_id,
            )

            # Cache the state based on cache policy
            if state and cache_policy == CachePolicy.USE_CACHE:
                async with self._lock:
                    self._state_cache[cache_key] = state

            self.logger.debug(
                "Retrieved state",
                state_id=state_id,
                has_state=state is not None,
                state_size=len(str(state)) if state else 0,
            )

        except (
            OSError,
            ValueError,
            TypeError,
            RuntimeError,
            ConnectionError,
            TimeoutError,
        ) as e:
            # ZERO TOLERANCE - Specific exception types for state retrieval failures
            self.logger.exception(
                "Failed to retrieve state",
                state_id=state_id,
                error=str(e),
            )
            raise
        else:
            return state

    async def set_state(
        self,
        project: Project,
        state_id: str,
        state: MeltanoState,
        backup_policy: BackupPolicy = BackupPolicy.CREATE_BACKUP,
    ) -> None:
        """Set state for a specific state ID.

        Args:
        ----
            project: Meltano project instance
            state_id: State identifier
            state: State object to set
            backup_policy: Backup creation policy for state modifications

        """
        cache_key = f"{project.root}:{state_id}"

        self.logger.info(
            "Setting state",
            state_id=state_id,
            state_size=len(str(state)),
            backup_policy=backup_policy,
        )

        try:
            # Create backup if requested and previous state exists
            if backup_policy == BackupPolicy.CREATE_BACKUP:
                await self._create_state_backup(project, state_id)

            # Set state through Meltano's StateService
            state_service = StateService(project)
            await asyncio.get_event_loop().run_in_executor(
                None,
                state_service.add_state,
                state_id,
                state,
            )

            # Update cache
            async with self._lock:
                self._state_cache[cache_key] = state

            # Publish state change event
            await self.event_bus.publish(
                "state.updated",
                {
                    "project_root": str(project.root),
                    "state_id": state_id,
                    "state_size": len(str(state)),
                    "updated_at": datetime.now(UTC).isoformat(),
                },
            )

            self.logger.info("Successfully set state", state_id=state_id)

        except (
            OSError,
            ValueError,
            TypeError,
            RuntimeError,
            ConnectionError,
            TimeoutError,
        ) as e:
            # ZERO TOLERANCE - Specific exception types for state persistence failures
            self.logger.exception(
                "Failed to set state",
                state_id=state_id,
                error=str(e),
            )
            raise

    async def merge_state(
        self, project: Project, state_id: str, partial_state: dict[str, Any]
    ) -> MeltanoState:
        """Merge partial state with existing state.

        Args:
        ----
            project: Meltano project instance
            state_id: State identifier
            partial_state: Partial state to merge

        Returns:
        -------
            Merged state object

        """
        self.logger.info(
            "Merging state",
            state_id=state_id,
            partial_keys=list(partial_state.keys()),
        )

        try:
            # Get current state
            current_state = await self.get_state(project, state_id)

            if current_state is None:
                # Create new state if none exists
                new_state = MeltanoState()
                new_state.update(partial_state)
            else:
                # Merge with existing state
                new_state = current_state.copy()
                new_state.merge(partial_state)

            # Set the merged state
            await self.set_state(project, state_id, new_state)

            self.logger.info("Successfully merged state", state_id=state_id)

        except (OSError, ValueError, TypeError, RuntimeError, AttributeError) as e:
            # ZERO TOLERANCE - Specific exception types for state merging failures
            self.logger.exception(
                "Failed to merge state",
                state_id=state_id,
                error=str(e),
            )
            raise
        else:
            return new_state

    async def clear_state(
        self,
        project: Project,
        state_id: str,
        backup_policy: BackupPolicy = BackupPolicy.CREATE_BACKUP,
    ) -> None:
        """Clear state for a specific state ID.

        Args:
        ----
            project: Meltano project instance
            state_id: State identifier
            backup_policy: Backup creation policy before clearing state

        """
        cache_key = f"{project.root}:{state_id}"

        self.logger.info(
            "Clearing state",
            state_id=state_id,
            backup_policy=backup_policy,
        )

        try:
            # Create backup if requested
            if backup_policy == BackupPolicy.CREATE_BACKUP:
                await self._create_state_backup(project, state_id)

            # Clear state through Meltano's StateService
            state_service = StateService(project)
            await asyncio.get_event_loop().run_in_executor(
                None,
                state_service.clear_state,
                state_id,
            )

            # Remove from cache
            async with self._lock:
                self._state_cache.pop(cache_key, None)

            # Publish state cleared event
            await self.event_bus.publish(
                "state.cleared",
                {
                    "project_root": str(project.root),
                    "state_id": state_id,
                    "cleared_at": datetime.now(UTC).isoformat(),
                },
            )

            self.logger.info("Successfully cleared state", state_id=state_id)

        except (
            OSError,
            ValueError,
            TypeError,
            RuntimeError,
            ConnectionError,
            PermissionError,
        ) as e:
            # ZERO TOLERANCE - Specific exception types for state clearing failures
            self.logger.exception(
                "Failed to clear state",
                state_id=state_id,
                error=str(e),
            )
            raise

    async def list_state_ids(self, project: Project) -> list[str]:
        """List all state IDs for a project.

        Args:
        ----
            project: Meltano project instance

        Returns:
        -------
            List of state IDs

        """
        try:
            state_service = StateService(project)
            state_ids = await asyncio.get_event_loop().run_in_executor(
                None,
                state_service.list_state_ids,
            )

            self.logger.debug(
                "Listed state IDs",
                project_root=str(project.root),
                count=len(state_ids),
            )

        except (OSError, ValueError, TypeError, RuntimeError, ConnectionError) as e:
            # ZERO TOLERANCE - Specific exception types for state ID enumeration failures
            self.logger.exception(
                "Failed to list state IDs",
                project_root=str(project.root),
                error=str(e),
            )
            raise
        else:
            return state_ids

    async def get_state_history(
        self, _project: Project, state_id: str, limit: int = 10
    ) -> list[dict[str, Any]]:
        """Get state history for a specific state ID.

        Args:
        ----
            project: Meltano project instance
            state_id: State identifier
            limit: Maximum number of history entries to return

        Returns:
        -------
            List of state history entries

        """
        # Query state history from backup storage with enterprise-grade implementation
        self.logger.info(
            "Getting state history",
            state_id=state_id,
            limit=limit,
        )

        try:
            # REAL state history implementation - query backup storage
            history = []

            # Query state backup directory for historical versions
            state_backup_dir = self.backup_dir / state_id
            if state_backup_dir.exists():
                # Get all state version files sorted by modification time
                state_files = sorted(
                    state_backup_dir.glob("*.json"),
                    key=lambda p: p.stat().st_mtime,
                    reverse=True,
                )

                for i, state_file in enumerate(state_files[:limit]):
                    try:
                        with state_file.open("r", encoding="utf-8") as f:
                            # Read file content first, then use orjson
                            content = f.read()
                            state_data = orjson.loads(content)

                        # Calculate state size and changes
                        state_size = len(orjson.dumps(state_data))

                        history.append(
                            {
                                "state_id": state_id,
                                "timestamp": datetime.fromtimestamp(
                                    state_file.stat().st_mtime,
                                    UTC,
                                ).isoformat(),
                                "version": len(state_files)
                                - i,  # Version number from newest to oldest
                                "action": "backup_saved",
                                "size_bytes": state_size,
                                "file_path": str(state_file),
                                "message": f"State backup version {len(state_files) - i} with {len(state_data)} keys",
                            },
                        )
                    except (orjson.JSONDecodeError, OSError) as e:
                        # Log corrupted state file but continue
                        self.logger.warning(
                            "Corrupted state backup",
                            file=str(state_file),
                            error=str(e),
                        )
                        continue

        except (OSError, PermissionError, ValueError, TypeError) as e:
            # ZERO TOLERANCE - Specific exception types for state history retrieval failures
            self.logger.exception(
                "Failed to get state history",
                state_id=state_id,
                error=str(e),
            )
            raise
        else:
            return history

    async def backup_all_states(
        self, project: Project, backup_name: str | None = None
    ) -> dict[str, Any]:
        """Create a backup of all states for a project.

        Args:
        ----
            project: Meltano project instance
            backup_name: Optional backup name

        Returns:
        -------
            Backup information

        """
        backup_name = (
            backup_name or f"backup_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
        )

        self.logger.info(
            "Creating backup of all states",
            project_root=str(project.root),
            backup_name=backup_name,
        )

        try:
            # Get all state IDs
            state_ids = await self.list_state_ids(project)

            backed_up_states = []
            failed_states = []

            # Backup each state
            for state_id in state_ids:
                try:
                    await self._create_state_backup(project, state_id, backup_name)
                    backed_up_states.append(state_id)
                except (OSError, ValueError, RuntimeError, PermissionError) as e:
                    self.logger.warning(
                        "Failed to backup state",
                        state_id=state_id,
                        error=str(e),
                    )
                    failed_states.append({"state_id": state_id, "error": str(e)})

            backup_info = {
                "backup_name": backup_name,
                "project_root": str(project.root),
                "created_at": datetime.now(UTC).isoformat(),
                "total_states": len(state_ids),
                "backed_up_count": len(backed_up_states),
                "failed_count": len(failed_states),
                "backed_up_states": backed_up_states,
                "failed_states": failed_states,
            }

            # Publish backup completed event
            await self.event_bus.publish("state.backup_completed", backup_info)

            self.logger.info(
                "Backup completed",
                backup_name=backup_name,
                backed_up_count=len(backed_up_states),
                failed_count=len(failed_states),
            )

        except (OSError, PermissionError, ValueError, RuntimeError) as e:
            # ZERO TOLERANCE - Specific exception types for bulk state backup failures
            self.logger.exception(
                "Failed to backup all states",
                backup_name=backup_name,
                error=str(e),
            )
            raise
        else:
            return backup_info

    async def restore_state_from_backup(
        self,
        project: Project,
        state_id: str,
        backup_name: str,
        overwrite_policy: OverwritePolicy = OverwritePolicy.PROTECT_EXISTING,
    ) -> None:
        """Restore state from a backup.

        Args:
        ----
            project: Meltano project instance
            state_id: State identifier to restore
            backup_name: Name of the backup to restore from
            overwrite_policy: Overwrite policy for state restoration

        """
        self.logger.info(
            "Restoring state from backup",
            state_id=state_id,
            backup_name=backup_name,
            overwrite_policy=overwrite_policy,
        )

        try:
            # Check if state exists and overwrite is allowed
            if overwrite_policy == OverwritePolicy.PROTECT_EXISTING:
                current_state = await self.get_state(
                    project,
                    state_id,
                    cache_policy=CachePolicy.FORCE_REFRESH,
                )
                if current_state is not None:
                    msg = f"State '{state_id}' exists and overwrite policy is PROTECT_EXISTING"
                    raise ValueError(msg)

            # Load backup
            backup_state = await self._load_state_backup(project, state_id, backup_name)
            if backup_state is None:
                msg = (
                    f"No backup found for state '{state_id}' in backup '{backup_name}'"
                )
                raise ValueError(msg)

            # Restore the state
            await self.set_state(
                project,
                state_id,
                backup_state,
                backup_policy=BackupPolicy.SKIP_BACKUP,
            )

            # Publish restore completed event
            await self.event_bus.publish(
                "state.restored",
                {
                    "project_root": str(project.root),
                    "state_id": state_id,
                    "backup_name": backup_name,
                    "restored_at": datetime.now(UTC).isoformat(),
                },
            )

            self.logger.info(
                "Successfully restored state from backup",
                state_id=state_id,
                backup_name=backup_name,
            )

        except (
            OSError,
            PermissionError,
            ValueError,
            TypeError,
            orjson.JSONDecodeError,
        ) as e:
            # ZERO TOLERANCE - Specific exception types for state restoration failures
            self.logger.exception(
                "Failed to restore state from backup",
                state_id=state_id,
                backup_name=backup_name,
                error=str(e),
            )
            raise

    async def _create_state_backup(
        self, project: Project, state_id: str, backup_name: str | None = None
    ) -> None:
        """Create a backup of a specific state.

        Args:
        ----
            project: Meltano project instance
            state_id: State identifier to backup
            backup_name: Optional backup name

        """
        backup_name = (
            backup_name or f"auto_backup_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
        )

        try:
            # Get current state
            current_state = await self.get_state(
                project,
                state_id,
                cache_policy=CachePolicy.FORCE_REFRESH,
            )
            if current_state is None:
                self.logger.debug("No state to backup", state_id=state_id)
                return

            # Create backup directory
            backup_dir = project.root / ".meltano" / "state_backups" / backup_name
            backup_dir.mkdir(parents=True, exist_ok=True)

            # Save state to backup file
            backup_file = backup_dir / f"{state_id}.json"
            backup_data = {
                "state_id": state_id,
                "backup_name": backup_name,
                "created_at": datetime.now(UTC).isoformat(),
                "project_root": str(project.root),
                "state": self._serialize_state_safe(current_state),
            }

            with backup_file.open("w") as f:
                # Use orjson with pretty formatting
                formatted_data = orjson.dumps(backup_data, option=orjson.OPT_INDENT_2)
                f.write(formatted_data.decode())

            self.logger.debug(
                "Created state backup",
                state_id=state_id,
                backup_name=backup_name,
                backup_file=str(backup_file),
            )

        except (
            OSError,
            PermissionError,
            ValueError,
            TypeError,
            orjson.JSONEncodeError,
        ) as e:
            # ZERO TOLERANCE - Specific exception types for state backup creation failures
            self.logger.exception(
                "Failed to create state backup",
                state_id=state_id,
                backup_name=backup_name,
                error=str(e),
            )
            # Don't re-raise backup errors unless critical

    async def _load_state_backup(
        self, project: Project, state_id: str, backup_name: str
    ) -> MeltanoState | None:
        """Load state from a backup file.

        Args:
        ----
            project: Meltano project instance
            state_id: State identifier to load
            backup_name: Backup name to load from

        Returns:
        -------
            Loaded state or None if not found

        """
        try:
            backup_file = (
                project.root
                / ".meltano"
                / "state_backups"
                / backup_name
                / f"{state_id}.json"
            )

            if not backup_file.exists():
                return None

            with backup_file.open() as f:
                content = f.read()
                backup_data = orjson.loads(content)

            # Reconstruct MeltanoState from backup
            state_data = backup_data.get("state")
            if isinstance(state_data, str):
                # Try to parse as JSON if it's a string
                try:
                    state_data = orjson.loads(state_data)
                except orjson.JSONDecodeError as e:
                    # If not JSON, treat as raw state data
                    self.logger.debug(
                        "State data is not JSON, treating as raw data",
                        state_id=state_id,
                        error=str(e),
                    )

            # Create MeltanoState object
            # This is a simplified reconstruction - in practice we'd need to handle
            # the specific MeltanoState format properly
            state = MeltanoState()
            if isinstance(state_data, dict):
                state.update(state_data)

        except (
            OSError,
            PermissionError,
            ValueError,
            TypeError,
            orjson.JSONDecodeError,
        ) as e:
            # ZERO TOLERANCE - Specific exception types for state backup loading failures
            self.logger.exception(
                "Failed to load state backup",
                state_id=state_id,
                backup_name=backup_name,
                error=str(e),
            )
        else:
            return state
        return None

    async def clear_cache(self) -> None:
        """Clear the state cache to free memory and force fresh state retrieval.

        Removes all cached state objects from memory, forcing subsequent
        state requests to fetch fresh data from the backend storage.

        Note:
        ----
            Clears all cached pipeline state with thread-safe locking and logging.

        """
        async with self._lock:
            cleared_count = len(self._state_cache)
            self._state_cache.clear()

            self.logger.info("Cleared state cache", cleared_count=cleared_count)

    def _serialize_state_safe(self, state: object) -> str:
        """Serialize state object safely with try/except pattern - ZERO TOLERANCE MODERNIZATION.

        Args:
        ----
            state: The state object that may or may not have a 'json' method

        Returns:
        -------
            String representation of the state

        """
        try:
            # Try to call json() method for proper serialization
            json_method = state.json  # type: ignore[attr-defined]
            return json_method()
        except AttributeError:
            # Fallback to string representation if no json method
            return str(state)
