"""FLEXT Meltano job executor."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from flext_core import FlextResult

from flext_meltano.constants import FlextMeltanoJobStatus
from flext_meltano.jobs.models import FlextMeltanoJob


class FlextMeltanoJobExecutor:
    """Executor for FLEXT Meltano jobs."""

    def __init__(self) -> None:
        """Initialize job executor."""
        self._jobs: dict[str, FlextMeltanoJob] = {}

    def create_job(
        self,
        name: str,
        config: dict[str, Any] | None = None,
    ) -> FlextResult[FlextMeltanoJob]:
        """Create a new job.

        Args:
            name: Job name
            config: Job configuration

        Returns:
            FlextResult with created job

        """
        try:
            job_id = f"job_{len(self._jobs) + 1}"
            job = FlextMeltanoJob(
                id=job_id,
                name=name,
                config=config or {},
            )
            self._jobs[job_id] = job
            return FlextResult.ok(job)

        except Exception as e:
            return FlextResult.fail(f"Failed to create job: {e}")

    def execute_job(self, job_id: str) -> FlextResult[FlextMeltanoJob]:
        """Execute a job.

        Args:
            job_id: Job ID

        Returns:
            FlextResult with executed job

        """
        if job_id not in self._jobs:
            return FlextResult.fail(f"Job '{job_id}' not found")

        job = self._jobs[job_id]
        job.status = FlextMeltanoJobStatus.RUNNING
        job.started_at = datetime.now(UTC)

        try:
            # TODO: Implement actual job execution logic
            job.status = FlextMeltanoJobStatus.COMPLETED
            job.completed_at = datetime.now(UTC)
            return FlextResult.ok(job)

        except Exception as e:
            job.status = FlextMeltanoJobStatus.FAILED
            job.error = str(e)
            job.completed_at = datetime.now(UTC)
            return FlextResult.fail(f"Job execution failed: {e}")

    def get_job(self, job_id: str) -> FlextResult[FlextMeltanoJob]:
        """Get job by ID.

        Args:
            job_id: Job ID

        Returns:
            FlextResult with job

        """
        if job_id not in self._jobs:
            return FlextResult.fail(f"Job '{job_id}' not found")
        return FlextResult.ok(self._jobs[job_id])

    def list_jobs(self) -> FlextResult[list[FlextMeltanoJob]]:
        """List all jobs.

        Returns:
            FlextResult with list of jobs

        """
        return FlextResult.ok(list(self._jobs.values()))
