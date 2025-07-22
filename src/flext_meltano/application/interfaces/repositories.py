"""Repository Interfaces - NEW SEMANTIC ARCHITECTURE.

Repository interfaces define contracts for data access.
Built on flext-core AbstractRepository pattern.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from flext_core.domain.shared_types import Any, ServiceResult

    from flext_meltano.domain.entities import (
        MeltanoJob,
        MeltanoPlugin,
        MeltanoProject,
        MeltanoState,
    )


class ProjectRepository(Protocol):
    """Repository interface for Meltano projects."""

    @abstractmethod
    async def find_by_name(self, name: str) -> MeltanoProject | None:
        """Find project by name."""

    @abstractmethod
    async def find_by_directory(self, directory: str) -> MeltanoProject | None:
        """Find project by directory path."""

    @abstractmethod
    async def find_active_projects(self) -> list[MeltanoProject]:
        """Find all active projects."""

    @abstractmethod
    async def find_all(self) -> list[MeltanoProject]:
        """Find all projects."""

    @abstractmethod
    async def save(self, project: MeltanoProject) -> ServiceResult[Any]:
        """Save project."""

    @abstractmethod
    async def delete(self, project_id: str) -> ServiceResult[Any]:
        """Delete project."""


class PluginRepository(Protocol):
    """Repository interface for Meltano plugins."""

    @abstractmethod
    async def find_by_name_and_type(
        self,
        name: str,
        plugin_type: str,
    ) -> MeltanoPlugin | None:
        """Find plugin by name and type."""

    @abstractmethod
    async def find_by_project(self, project_id: str) -> list[MeltanoPlugin]:
        """Find plugins by project."""

    @abstractmethod
    async def find_by_type(self, plugin_type: str) -> list[MeltanoPlugin]:
        """Find plugins by type."""

    @abstractmethod
    async def find_installed_plugins(self) -> list[MeltanoPlugin]:
        """Find all installed plugins."""


class JobRepository(Protocol):
    """Repository interface for Meltano jobs."""

    @abstractmethod
    async def find_by_name(self, name: str) -> MeltanoJob | None:
        """Find job by name."""

    @abstractmethod
    async def find_by_project(self, project_id: str) -> list[MeltanoJob]:
        """Find jobs by project."""

    @abstractmethod
    async def find_by_status(self, status: str) -> list[MeltanoJob]:
        """Find jobs by status."""

    @abstractmethod
    async def find_running_jobs(self) -> list[MeltanoJob]:
        """Find all running jobs."""

    @abstractmethod
    async def find_recent_jobs(self, limit: int = 10) -> list[MeltanoJob]:
        """Find recent jobs."""


class StateRepository(Protocol):
    """Repository interface for Meltano state."""

    @abstractmethod
    async def find_by_job(self, job_id: str) -> MeltanoState | None:
        """Find state by job ID."""

    @abstractmethod
    async def find_latest_by_job_name(self, job_name: str) -> MeltanoState | None:
        """Find latest state for a job name."""

    @abstractmethod
    async def find_by_project(self, project_id: str) -> list[MeltanoState]:
        """Find states by project."""

    @abstractmethod
    async def find_stale_states(self, hours: float = 24.0) -> list[MeltanoState]:
        """Find stale states older than specified hours."""

    @abstractmethod
    async def cleanup_old_states(self, days: int = 30) -> ServiceResult[Any]:
        """Cleanup states older than specified days."""
