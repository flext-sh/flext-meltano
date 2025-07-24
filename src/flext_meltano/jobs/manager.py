"""FLEXT Meltano job manager."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_meltano.jobs.executor import FlextMeltanoJobExecutor

if TYPE_CHECKING:
    from flext_core import FlextResult

    from flext_meltano.jobs.models import FlextMeltanoJob


class FlextMeltanoJobManager:
    """Manager for FLEXT Meltano jobs."""

    def __init__(self) -> None:
        """Initialize job manager."""
        self._executor = FlextMeltanoJobExecutor()

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
        return self._executor.create_job(name, config)

    def execute_job(self, job_id: str) -> FlextResult[FlextMeltanoJob]:
        """Execute a job.

        Args:
            job_id: Job ID

        Returns:
            FlextResult with executed job

        """
        return self._executor.execute_job(job_id)

    def get_job(self, job_id: str) -> FlextResult[FlextMeltanoJob]:
        """Get job by ID.

        Args:
            job_id: Job ID

        Returns:
            FlextResult with job

        """
        return self._executor.get_job(job_id)

    def list_jobs(self) -> FlextResult[list[FlextMeltanoJob]]:
        """List all jobs.

        Returns:
            FlextResult with list of jobs

        """
        return self._executor.list_jobs()
