"""FLX Meltano Job Manager.

This module provides comprehensive job management capabilities integrated with
Meltano's job system, enabling enterprise-grade job tracking, scheduling, and monitoring.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Any

import structlog

# ZERO TOLERANCE - Meltano is REQUIRED and guaranteed in pyproject.toml
from meltano.core.db import project_engine
from meltano.core.job import State
from meltano.core.job.job import Job

# Meltano core availability is guaranteed by dependency constraints
MELTANO_CORE_AVAILABLE = True


if TYPE_CHECKING:
    from flx_core.events.event_bus import EventBusProtocol
    from meltano.core.project import Project

logger = structlog.get_logger()


class JobExecutionMode(Enum):
    """Execution mode enumeration for job management operations.

    Defines whether operations should be executed in simulation mode or
    with actual changes, replacing boolean dry_run parameters.

    Attributes
    ----------
        DRY_RUN: Simulation mode - report what would be done without changes.
        EXECUTE: Production mode - perform actual operations with changes.

    """

    DRY_RUN = "dry_run"
    EXECUTE = "execute"


class FlxMeltanoJobManager:
    """Enterprise Meltano job manager with advanced tracking and scheduling.

    This manager provides comprehensive job management capabilities including:
    - Job lifecycle management
    - Advanced job querying and filtering
    - Job scheduling and retry logic
    - Real-time job monitoring
    - Job performance analytics
    - Enterprise-grade audit trails
    """

    def __init__(self, event_bus: EventBusProtocol) -> None:
        """Initialize the FLX Meltano Job Manager.

        Args:
        ----
        event_bus: FLX event bus for job events

        """
        self.event_bus = event_bus
        self.logger = logger.bind(component="flx_meltano_job_manager")
        self._lock = asyncio.Lock()

        self.logger.info(
            "Initialized FLX Meltano Job Manager with full Meltano integration",
        )

    async def get_job(self, project: Project, job_id: str) -> Job | None:
        """Get a job by ID.

        Args:
        ----
        project: Meltano project instance
        job_id: Job identifier

        Returns:
        -------
        Job instance or None if not found

        """
        try:
            engine = project_engine(project)
            session_factory = engine.session_factory

            with session_factory() as session:
                job = session.query(Job).filter(Job.job_id == job_id).first()

                if job:
                    self.logger.debug(
                        "Retrieved job",
                        job_id=job_id,
                        state=job.state.value if job.state else None,
                    )
                else:
                    self.logger.debug("Job not found", job_id=job_id)

                return job

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
            # ZERO TOLERANCE - Specific exception types for job retrieval failures
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
        ----
        project: Meltano project instance
        state: Optional state filter
        run_id: Optional run ID filter
        limit: Maximum number of jobs to return
        offset: Number of jobs to skip

        Returns:
        -------
        List of job instances

        """
        try:
            engine = project_engine(project)
            session_factory = engine.session_factory

            with session_factory() as session:
                query = session.query(Job)

                # Apply filters
                if state:
                    query = query.filter(Job.state == state)

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

                return jobs

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
            # ZERO TOLERANCE - Specific exception types for job listing failures
            self.logger.exception(
                "Failed to list jobs",
                error=str(e),
                state=state.value if state else None,
                run_id=run_id,
            )
            raise

    async def update_job_state(
        self, project: Project, job_id: str, new_state: State, reason: str | None = None
    ) -> bool:
        """Update job state.

        Args:
        ----
        project: Meltano project instance
        job_id: Job identifier
        new_state: New state for the job
        reason: Optional reason for state change

        Returns:
        -------
        True if update was successful

        """
        try:
            engine = project_engine(project)
            session_factory = engine.session_factory

            with session_factory() as session:
                job = session.query(Job).filter(Job.job_id == job_id).first()

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
            # ZERO TOLERANCE - Specific exception types for job state update failures
            self.logger.exception(
                "Failed to update job state",
                job_id=job_id,
                new_state=new_state.value,
                error=str(e),
            )
            raise

    async def get_job_statistics(
        self, project: Project, days: int = 7
    ) -> dict[str, Any]:
        """Get job statistics for the specified time period.

        Args:
        ----
        project: Meltano project instance
        days: Number of days to include in statistics

        Returns:
        -------
        Job statistics dictionary

        """
        try:
            engine = project_engine(project)
            session_factory = engine.session_factory

            cutoff_date = datetime.now(UTC).replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            ) - timezone.timedelta(days=days)

            with session_factory() as session:
                # Get total job count
                total_jobs = (
                    session.query(Job).filter(Job.started_at >= cutoff_date).count()
                )

                # Get job counts by state
                state_counts = {}
                for state in State:
                    count = (
                        session.query(Job)
                        .filter(Job.started_at >= cutoff_date)
                        .filter(Job.state == state)
                        .count()
                    )
                    state_counts[state.value] = count

                # Calculate success rate
                success_count = state_counts.get(State.SUCCESS.value, 0)
                success_rate = (
                    (success_count / total_jobs * 100) if total_jobs > 0 else 0
                )

                statistics = {
                    "period_days": days,
                    "cutoff_date": cutoff_date.isoformat(),
                    "total_jobs": total_jobs,
                    "state_counts": state_counts,
                    "success_rate": round(success_rate, 2),
                    "generated_at": datetime.now(UTC).isoformat(),
                }

                self.logger.debug(
                    "Generated job statistics",
                    days=days,
                    total_jobs=total_jobs,
                    success_rate=success_rate,
                )

                return statistics

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
            # ZERO TOLERANCE - Specific exception types for job statistics retrieval failures
            self.logger.exception(
                "Failed to get job statistics",
                days=days,
                error=str(e),
            )
            raise

    async def get_running_jobs(
        self, project: Project, heartbeat_timeout_minutes: int = 5
    ) -> list[Job]:
        """Get all currently running jobs.

        Args:
        ----
        project: Meltano project instance
        heartbeat_timeout_minutes: Minutes after which a job is considered stale

        Returns:
        -------
        List of running job instances

        """
        try:
            engine = project_engine(project)
            session_factory = engine.session_factory

            timeout_cutoff = datetime.now(UTC) - timezone.timedelta(
                minutes=heartbeat_timeout_minutes,
            )

            with session_factory() as session:
                running_jobs = (
                    session.query(Job)
                    .filter(Job.state == State.RUNNING)
                    .filter(Job.last_heartbeat_at >= timeout_cutoff)
                    .order_by(Job.started_at.desc())
                    .all()
                )

                self.logger.debug(
                    "Retrieved running jobs",
                    count=len(running_jobs),
                    heartbeat_timeout_minutes=heartbeat_timeout_minutes,
                )

                return running_jobs

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
            # ZERO TOLERANCE - Specific exception types for running jobs retrieval failures
            self.logger.exception(
                "Failed to get running jobs",
                error=str(e),
            )
            raise

    async def get_stale_jobs(
        self, project: Project, heartbeat_timeout_minutes: int = 5
    ) -> list[Job]:
        """Get jobs that appear to be stale (running but no recent heartbeat).

        Args:
        ----
        project: Meltano project instance
        heartbeat_timeout_minutes: Minutes after which a job is considered stale

        Returns:
        -------
        List of stale job instances

        """
        try:
            engine = project_engine(project)
            session_factory = engine.session_factory

            timeout_cutoff = datetime.now(UTC) - timezone.timedelta(
                minutes=heartbeat_timeout_minutes,
            )

            with session_factory() as session:
                stale_jobs = (
                    session.query(Job)
                    .filter(Job.state == State.RUNNING)
                    .filter(Job.last_heartbeat_at < timeout_cutoff)
                    .order_by(Job.last_heartbeat_at.asc())
                    .all()
                )

                self.logger.debug(
                    "Retrieved stale jobs",
                    count=len(stale_jobs),
                    heartbeat_timeout_minutes=heartbeat_timeout_minutes,
                )

                return stale_jobs

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            ConnectionError,
            ImportError,
            LookupError,
            AttributeError,
            TimeoutError,
        ) as e:
            # ZERO TOLERANCE - Specific exception types for stale jobs retrieval failures
            self.logger.exception(
                "Failed to get stale jobs",
                error=str(e),
            )
            raise

    async def cleanup_stale_jobs(
        self,
        project: Project,
        heartbeat_timeout_minutes: int = 5,
        execution_mode: JobExecutionMode = JobExecutionMode.DRY_RUN,
    ) -> dict[str, Any]:
        """Clean up stale jobs by marking them as failed.

        Args:
        ----
        project: Meltano project instance
        heartbeat_timeout_minutes: Minutes after which a job is considered stale
        execution_mode: Execution mode for cleanup operation

        Returns:
        -------
        Cleanup result information

        """
        try:
            stale_jobs = await self.get_stale_jobs(project, heartbeat_timeout_minutes)

            if not stale_jobs:
                return {
                    "execution_mode": execution_mode.value,
                    "stale_jobs_found": 0,
                    "jobs_cleaned": 0,
                    "message": "No stale jobs found",
                }

            cleaned_jobs = []

            if execution_mode == JobExecutionMode.EXECUTE:
                for job in stale_jobs:
                    success = await self.update_job_state(
                        project,
                        job.job_id,
                        State.FAIL,
                        reason=f"Marked as failed due to stale heartbeat (timeout: {heartbeat_timeout_minutes}m)",
                    )

                    if success:
                        cleaned_jobs.append(
                            {
                                "job_id": job.job_id,
                                "run_id": job.run_id,
                                "last_heartbeat": (
                                    job.last_heartbeat_at.isoformat()
                                    if job.last_heartbeat_at
                                    else None
                                ),
                            },
                        )

            result = {
                "execution_mode": execution_mode.value,
                "stale_jobs_found": len(stale_jobs),
                "jobs_cleaned": len(cleaned_jobs),
                "heartbeat_timeout_minutes": heartbeat_timeout_minutes,
                "cleaned_at": datetime.now(UTC).isoformat(),
            }

            if execution_mode == JobExecutionMode.DRY_RUN:
                result["would_clean"] = [
                    {
                        "job_id": job.job_id,
                        "run_id": job.run_id,
                        "last_heartbeat": (
                            job.last_heartbeat_at.isoformat()
                            if job.last_heartbeat_at
                            else None
                        ),
                    }
                    for job in stale_jobs
                ]
            else:
                result["cleaned_jobs"] = cleaned_jobs

            self.logger.info(
                "Stale job cleanup completed",
                execution_mode=execution_mode.value,
                stale_jobs_found=len(stale_jobs),
                jobs_cleaned=len(cleaned_jobs),
            )

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            ConnectionError,
            ImportError,
            LookupError,
            PermissionError,
            TimeoutError,
        ) as e:
            # ZERO TOLERANCE - Specific exception types for stale jobs cleanup failures
            self.logger.exception(
                "Failed to cleanup stale jobs",
                error=str(e),
            )
            raise
        else:
            return result

    async def get_job_performance_metrics(
        self, project: Project, days: int = 30
    ) -> dict[str, Any]:
        """Get job performance metrics.

        Args:
        ----
        project: Meltano project instance
        days: Number of days to analyze

        Returns:
        -------
        Performance metrics dictionary

        """
        try:
            engine = project_engine(project)
            session_factory = engine.session_factory

            cutoff_date = datetime.now(UTC) - timezone.timedelta(days=days)

            with session_factory() as session:
                # Get completed jobs for performance analysis
                completed_jobs = (
                    session.query(Job)
                    .filter(Job.started_at >= cutoff_date)
                    .filter(Job.state.in_([State.SUCCESS, State.FAIL]))
                    .all()
                )

                if not completed_jobs:
                    return {
                        "period_days": days,
                        "total_jobs": 0,
                        "message": "No completed jobs found in the specified period",
                    }

                # Calculate durations (mock calculation - would need actual duration tracking)
                durations = []
                for job in completed_jobs:
                    if job.started_at and job.last_heartbeat_at:
                        duration = (
                            job.last_heartbeat_at - job.started_at
                        ).total_seconds()
                        durations.append(duration)

                if durations:
                    avg_duration = sum(durations) / len(durations)
                    min_duration = min(durations)
                    max_duration = max(durations)

                    # Calculate percentiles (simplified)
                    sorted_durations = sorted(durations)
                    p50_duration = sorted_durations[len(sorted_durations) // 2]
                    p95_duration = sorted_durations[int(len(sorted_durations) * 0.95)]
                else:
                    avg_duration = min_duration = max_duration = p50_duration = (
                        p95_duration
                    ) = 0

                metrics = {
                    "period_days": days,
                    "total_jobs": len(completed_jobs),
                    "jobs_with_duration": len(durations),
                    "duration_metrics": {
                        "average_seconds": round(avg_duration, 2),
                        "min_seconds": round(min_duration, 2),
                        "max_seconds": round(max_duration, 2),
                        "p50_seconds": round(p50_duration, 2),
                        "p95_seconds": round(p95_duration, 2),
                    },
                    "success_rate": round(
                        len([j for j in completed_jobs if j.state == State.SUCCESS])
                        / len(completed_jobs)
                        * 100,
                        2,
                    ),
                    "generated_at": datetime.now(UTC).isoformat(),
                }

                self.logger.debug(
                    "Generated performance metrics",
                    days=days,
                    total_jobs=len(completed_jobs),
                    avg_duration=avg_duration,
                )

                return metrics

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
            # ZERO TOLERANCE - Specific exception types for performance metrics retrieval failures
            self.logger.exception(
                "Failed to get performance metrics",
                days=days,
                error=str(e),
            )
            raise

    async def delete_old_jobs(
        self,
        project: Project,
        days_to_keep: int = 30,
        execution_mode: JobExecutionMode = JobExecutionMode.DRY_RUN,
    ) -> dict[str, Any]:
        """Delete old jobs beyond the retention period.

        Args:
        ----
        project: Meltano project instance
        days_to_keep: Number of days of job history to keep
        execution_mode: Execution mode for deletion operation

        Returns:
        -------
        Deletion result information

        """
        try:
            engine = project_engine(project)
            session_factory = engine.session_factory

            cutoff_date = datetime.now(UTC) - timezone.timedelta(days=days_to_keep)

            with session_factory() as session:
                # Find old jobs
                old_jobs_query = session.query(Job).filter(Job.started_at < cutoff_date)
                old_jobs_count = old_jobs_query.count()

                if old_jobs_count == 0:
                    return {
                        "execution_mode": execution_mode.value,
                        "days_to_keep": days_to_keep,
                        "old_jobs_found": 0,
                        "jobs_deleted": 0,
                        "message": "No old jobs found for deletion",
                    }

                deleted_count = 0
                if execution_mode == JobExecutionMode.EXECUTE:
                    deleted_count = old_jobs_query.delete()
                    session.commit()

                result = {
                    "execution_mode": execution_mode.value,
                    "days_to_keep": days_to_keep,
                    "cutoff_date": cutoff_date.isoformat(),
                    "old_jobs_found": old_jobs_count,
                    "jobs_deleted": deleted_count,
                    "processed_at": datetime.now(UTC).isoformat(),
                }

                self.logger.info(
                    "Job deletion completed",
                    execution_mode=execution_mode.value,
                    days_to_keep=days_to_keep,
                    old_jobs_found=old_jobs_count,
                    jobs_deleted=deleted_count,
                )

                return result

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            ConnectionError,
            ImportError,
            LookupError,
            PermissionError,
            TimeoutError,
        ) as e:
            # ZERO TOLERANCE - Specific exception types for old jobs deletion failures
            self.logger.exception(
                "Failed to delete old jobs",
                days_to_keep=days_to_keep,
                error=str(e),
            )
            raise
