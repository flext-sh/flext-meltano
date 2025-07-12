"""FLEXT Meltano State Manager.

This module provides deep integration with Meltano's state management system,
enabling enterprise-grade state persistence, backup, and recovery capabilities.
"""

from __future__ import annotations

import asyncio
from datetime import UTC
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from typing import Any

# ZERO TOLERANCE - Meltano is REQUIRED and guaranteed in pyproject.toml
from meltano.core.state_service import StateService
from meltano.core.state_store import MeltanoState
from structlog import get_logger

if TYPE_CHECKING:
    from meltano.core.project import Project

    from flext_core.events.event_bus import EventBusProtocol

logger = get_logger(__name__)


class CachePolicy(Enum):
    """Cache usage policy enumeration for state operations."""

    USE_CACHE = "use_cache"
    FORCE_REFRESH = "force_refresh"
    CACHE_FIRST = "cache_first"


class FlextMeltanoStateManager:
    """Enterprise Meltano state manager with advanced features."""

    def __init__(self, event_bus: EventBusProtocol) -> None:
        self.event_bus = event_bus
        self.logger = logger.bind(component="flext_meltano_state_manager")
        self._lock = asyncio.Lock()

        self.logger.info("Initialized FLEXT Meltano State Manager")

    async def get_state(
        self,
        project: Project,
        job_id: str,
        cache_policy: CachePolicy = CachePolicy.USE_CACHE,
    ) -> dict[str, Any] | None:
        """Get state for a specific job."""
        try:
            state_service = StateService(project)
            state = state_service.get_state(job_id)

            if state:
                return {
                    "job_id": job_id,
                    "state_data": state.json(),
                    "retrieved_at": datetime.now(UTC).isoformat(),
                }
            return None

        except Exception as e:
            self.logger.exception("Failed to get state", job_id=job_id, error=str(e))
            return None

    async def set_state(
        self,
        project: Project,
        job_id: str,
        state_data: dict[str, Any],
    ) -> bool:
        """Set state for a specific job."""
        try:
            async with self._lock:
                state_service = StateService(project)
                state = MeltanoState(state_data)
                state_service.set_state(job_id, state)

                self.logger.info(
                    "State updated successfully",
                    job_id=job_id,
                    state_size=len(str(state_data)),
                )
                return True

        except Exception as e:
            self.logger.exception("Failed to set state", job_id=job_id, error=str(e))
            return False

    async def clear_state(self, project: Project, job_id: str) -> bool:
        """Clear state for a specific job."""
        try:
            async with self._lock:
                state_service = StateService(project)
                state_service.clear_state(job_id)

                self.logger.info("State cleared successfully", job_id=job_id)
                return True

        except Exception as e:
            self.logger.exception("Failed to clear state", job_id=job_id, error=str(e))
            return False
