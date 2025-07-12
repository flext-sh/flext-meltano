"""FLEXT Meltano Job Manager.

This module provides comprehensive job management capabilities integrated with
Meltano's job system, enabling enterprise-grade job tracking, scheduling,
and monitoring.
"""

from __future__ import annotations

import asyncio
from datetime import UTC
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

# ZERO TOLERANCE - Meltano is REQUIRED and guaranteed in pyproject.toml
from meltano.core.db import project_engine
from meltano.core.job.job import Job
from structlog import get_logger

# Meltano core availability is guaranteed by dependency constraints
MELTANO_CORE_AVAILABLE = True

if TYPE_CHECKING:
    from meltano.core.job import State
    from meltano.core.project import Project

    from flext_meltano.event_bus_protocol import EventBusProtocol

logger = get_logger(__name__)


class JobExecutionMode(Enum):
    """Execution mode enumeration for job management operations."""

    DRY_RUN = "dry_run"
    EXECUTE = "execute"


class FlextMeltanoJobManager:
    """Enterprise Meltano job manager with advanced tracking and scheduling."""

    def __init__(self, event_bus: EventBusProtocol) -> None:
        """Initialize job manager with event bus integration."""
        self.event_bus = event_bus
        self.logger = logger.bind(component="flext_meltano_job_manager")
        self._lock = asyncio.Lock()

        self.logger.info(
            "Initialized FLEXT Meltano Job Manager with full Meltano integration",
        )

    async def get_job(self, project: Project, job_id: str) -> Job | None:
        """Get job by ID from project database.

        Args:
            project: Meltano project instance.
            job_id: Unique job identifier.

        Returns:
            Job instance if found, None otherwise.

        """
        try:
            _engine, session_factory = project_engine(project)

            with session_factory() as session:
                job = session.query(Job).filter(Job.id == job_id).first()

                if job:
                    self.logger.debug(
                        "Retrieved job",
                        job_id=job_id,
                        state=job.state.value if job.state else None,
                    )
                else:
                    self.logger.debug("Job not found", job_id=job_id)

                return job  # type: ignore[no-any-return]

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            ConnectionError,
            ImportError,
            LookupError,
            KeyError,
        ) as e:
            self.logger.exception(
                "Failed to retrieve job",
                job_id=job_id,
                error=str(e),
            )
            raise

    async def list_jobs(
        self,
        project: Project,
        state: State | None = None,
        run_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Job]:
        """List jobs with optional filtering.

        Args:
            project: Meltano project instance.
            state: Optional state filter.
            run_id: Optional run ID filter.
            limit: Maximum number of jobs to return.
            offset: Number of jobs to skip.

        Returns:
            List of Job instances matching the criteria.

        """
        try:
            _engine, session_factory = project_engine(project)

            with session_factory() as session:
                query = session.query(Job)

                # Apply filters
                if state:
                    query = query.filter(Job.state == state)  # type: ignore[comparison-overlap]

                if run_id:
                    query = query.filter(Job.run_id == run_id)

                # Apply pagination and ordering
                jobs = (
                    query.order_by(Job.started_at.desc())
                    .offset(offset)
                    .limit(limit)
                    .all()
                )

                self.logger.debug(
                    "Listed jobs",
                    count=len(jobs),
                    state=state.value if state else None,
                    run_id=run_id,
                    limit=limit,
                    offset=offset,
                )

                return jobs  # type: ignore[no-any-return]

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            ConnectionError,
            ImportError,
            LookupError,
            AttributeError,
        ) as e:
            self.logger.exception(
                "Failed to list jobs",
                error=str(e),
                state=state.value if state else None,
                run_id=run_id,
            )
            raise

    async def update_job_state(
        self,
        project: Project,
        job_id: str,
        new_state: State,
        reason: str | None = None,
    ) -> bool:
        """Update job state in database.

        Args:
            project: Meltano project instance.
            job_id: Unique job identifier.
            new_state: New state to set.
            reason: Optional reason for state change.

        Returns:
            True if update was successful, False otherwise.

        """
        try:
            _engine, session_factory = project_engine(project)

            with session_factory() as session:
                job = session.query(Job).filter(Job.id == job_id).first()

                if not job:
                    self.logger.warning("Job not found for state update", job_id=job_id)
                    return False

                old_state = job.state
                job.state = new_state
                job.last_heartbeat_at = datetime.now(UTC)

                session.commit()

                self.logger.info(
                    "Updated job state",
                    job_id=job_id,
                    old_state=old_state.value if old_state else None,
                    new_state=new_state.value,
                    reason=reason,
                )

                # Publish state change event
                await self.event_bus.publish(
                    {
                        "type": "job.state_changed",
                        "data": {
                            "job_id": job_id,
                            "run_id": job.run_id,
                            "old_state": old_state.value if old_state else None,
                            "new_state": new_state.value,
                            "reason": reason,
                            "updated_at": datetime.now(UTC).isoformat(),
                        },
                    },
                )

                return True

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            ConnectionError,
            ImportError,
            LookupError,
            AttributeError,
        ) as e:
            self.logger.exception(
                "Failed to update job state",
                job_id=job_id,
                new_state=new_state.value,
                error=str(e),
            )
            raise
