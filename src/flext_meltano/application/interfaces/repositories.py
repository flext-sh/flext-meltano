"""Repository Interfaces - NEW SEMANTIC ARCHITECTURE.

Repository interfaces define contracts for data access.
Built on flext-core AbstractRepository pattern.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

# 🚨 ARCHITECTURAL COMPLIANCE: Import via módulo raiz

if TYPE_CHECKING:
    # 🚨 ARCHITECTURAL COMPLIANCE: Using DI container
    from flext_core import ServiceResult

    from flext_meltano.domain.entities import (
        MeltanoJob,
        MeltanoPlugin,
        MeltanoProject,
        MeltanoState,
    )
    from flext_meltano.infrastructure.di_container import get_service_result

# Import outside TYPE_CHECKING for runtime access
from flext_meltano.infrastructure.di_container import get_service_result


class ProjectRepository(Protocol):
    """Repository interface for Meltano projects."""

    @abstractmethod
    async def find_by_name(self, name: str) -> MeltanoProject | None:
        """Find project by name."""
        ...

    @abstractmethod
    async def save(self, project: MeltanoProject) -> ServiceResult[MeltanoProject]:
        """Save a project."""
        ...

    @abstractmethod
    async def delete(self, project_id: str) -> ServiceResult[bool]:
        """Delete a project."""
        ...

    @abstractmethod
    async def list_projects(self) -> ServiceResult[list[MeltanoProject]]:
        """List all projects."""
        ...


class StateRepository(Protocol):
    """Repository interface for Meltano state."""

    @abstractmethod
    async def find_by_job_id(self, job_id: str) -> MeltanoState | None:
        """Find state by job ID."""
        ...

    @abstractmethod
    async def save(self, state: MeltanoState) -> ServiceResult[MeltanoState]:
        """Save a state."""
        ...

    @abstractmethod
    async def delete(self, state_id: str) -> ServiceResult[bool]:
        """Delete a state."""
        ...


class JobRepository(Protocol):
    """Repository interface for Meltano jobs."""

    @abstractmethod
    async def find_by_id(self, job_id: str) -> MeltanoJob | None:
        """Find job by ID."""
        ...

    @abstractmethod
    async def save(self, job: MeltanoJob) -> ServiceResult[MeltanoJob]:
        """Save a job."""
        ...

    @abstractmethod
    async def delete(self, job_id: str) -> ServiceResult[bool]:
        """Delete a job."""
        ...

    @abstractmethod
    async def list_jobs(self) -> ServiceResult[list[MeltanoJob]]:
        """List all jobs."""
        ...


class PluginRepository(Protocol):
    """Repository interface for Meltano plugins."""

    @abstractmethod
    async def find_by_name(self, plugin_name: str) -> MeltanoPlugin | None:
        """Find plugin by name."""
        ...

    @abstractmethod
    async def save(self, plugin: MeltanoPlugin) -> ServiceResult[MeltanoPlugin]:
        """Save a plugin."""
        ...

    @abstractmethod
    async def delete(self, plugin_id: str) -> ServiceResult[bool]:
        """Delete a plugin."""
        ...

    @abstractmethod
    async def list_plugins(self) -> ServiceResult[list[MeltanoPlugin]]:
        """List all plugins."""
        ...


__all__ = [
    "JobRepository",
    "PluginRepository",
    "ProjectRepository",
    "StateRepository",
]
