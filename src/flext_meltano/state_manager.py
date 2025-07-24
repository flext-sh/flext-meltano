"""FLEXT Meltano State Manager.

⚠️  DEPRECATION NOTICE: This implementation is being consolidated.
    Main implementation: /state/manager.py (FlextMeltanoStateManager)

    The consolidated implementation provides:
    - File-based and Meltano StateService backend support
    - Async compatibility methods for orchestrator
    - FlextResult error handling patterns
    - Comprehensive state models

    TODO: Migrate remaining usage to main implementation and deprecate this file.

This module provides deep integration with Meltano's state management system,
enabling enterprise-grade state persistence, backup, and recovery capabilities.
"""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING, Any

# ZERO TOLERANCE - Meltano is REQUIRED and guaranteed in pyproject.toml
from meltano.core.state_service import StateService

if TYPE_CHECKING:
    from meltano.core.project import Project

    from flext_meltano.event_bus_protocol import FlextMeltanoEventBusProtocol

logger = logging.getLogger(__name__)


class FlextMeltanoCachePolicy(Enum):
    """Cache usage policy enumeration for state operations."""

    USE_CACHE = "use_cache"
    FORCE_REFRESH = "force_refresh"
    CACHE_FIRST = "cache_first"


class FlextMeltanoStateManager:
    """Enterprise Meltano state manager with advanced features."""

    def __init__(self, event_bus: FlextMeltanoEventBusProtocol) -> None:
        """Initialize FLEXT Meltano State Manager."""
        self.event_bus = event_bus
        self.logger = logger
        self._lock = asyncio.Lock()

        self.logger.info("Initialized FLEXT Meltano State Manager")

    async def get_state(
        self,
        project: Project,
        job_id: str,
        _cache_policy: FlextMeltanoCachePolicy = FlextMeltanoCachePolicy.USE_CACHE,
    ) -> dict[str, Any] | None:
        """Get job state by ID."""
        try:
            state_service = StateService(project)
            state = state_service.get_state(job_id)

            if state:
                return {
                    "job_id": job_id,
                    "state_data": state if isinstance(state, dict) else str(state),
                    "retrieved_at": datetime.now(UTC).isoformat(),
                }
            return None
        except Exception as e:
            self.logger.exception(f"Failed to get state: job_id={job_id}, error={e}")
            return None

    async def set_state(
        self,
        project: Project,
        job_id: str,
        state_data: dict[str, Any],
    ) -> bool:
        """Update job state with provided data."""
        try:
            async with self._lock:
                state_service = StateService(project)
                # Convert state_data to appropriate format for Meltano
                state_json = (
                    json.dumps(state_data)
                    if isinstance(state_data, dict)
                    else str(state_data)
                )
                state_service.set_state(job_id, state_json)

                self.logger.info(
                    f"State updated successfully: job_id={job_id}, state_size={len(str(state_data))}",
                )
                return True
        except Exception as e:
            self.logger.exception(f"Failed to set state: job_id={job_id}, error={e}")
            return False

    async def clear_state(self, project: Project, job_id: str) -> bool:
        try:
            async with self._lock:
                state_service = StateService(project)
                state_service.clear_state(job_id)

                self.logger.info(f"State cleared successfully: job_id={job_id}")
                return True
        except Exception as e:
            self.logger.exception(f"Failed to clear state: job_id={job_id}, error={e}")
            return False
