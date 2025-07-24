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
    from flext_core import FlextResult

    from flext_meltano.domain.entities import (
        MeltanoJob,
        MeltanoPlugin,
        MeltanoProject,
        MeltanoState,
    )

# Import outside TYPE_CHECKING for runtime access


class FlextMeltanoProjectRepository(Protocol):
    """Repository interface for Meltano projects."""

    @abstractmethod
    async def find_by_name(self, name: str) -> MeltanoProject | None:
        """Find project by name."""
        ...

    @abstractmethod
    async def save(self, project: MeltanoProject) -> FlextResult[MeltanoProject]:
        """Save a project."""
        ...

    @abstractmethod
    async def delete(self, project_id: str) -> FlextResult[bool]:
        """Delete a project."""
        ...

    @abstractmethod
    async def list_projects(self) -> FlextResult[list[MeltanoProject]]:
        """List all projects."""
        ...


class FlextMeltanoStateRepository(Protocol):
    """Repository interface for Meltano state."""

    @abstractmethod
    async def find_by_job_id(self, job_id: str) -> MeltanoState | None:
        """Find state by job ID."""
        ...

    @abstractmethod
    async def save(self, state: MeltanoState) -> FlextResult[MeltanoState]:
        """Save a state."""
        ...

    @abstractmethod
    async def delete(self, state_id: str) -> FlextResult[bool]:
        """Delete a state."""
        ...


class FlextMeltanoJobRepository(Protocol):
    """Repository interface for Meltano jobs."""

    @abstractmethod
    async def find_by_id(self, job_id: str) -> MeltanoJob | None:
        """Find job by ID."""
        ...

    @abstractmethod
    async def save(self, job: MeltanoJob) -> FlextResult[MeltanoJob]:
        """Save a job."""
        ...

    @abstractmethod
    async def delete(self, job_id: str) -> FlextResult[bool]:
        """Delete a job."""
        ...

    @abstractmethod
    async def list_jobs(self) -> FlextResult[list[MeltanoJob]]:
        """List all jobs."""
        ...


class FlextMeltanoPluginRepository(Protocol):
    """Repository interface for Meltano plugins."""

    @abstractmethod
    async def find_by_name(self, plugin_name: str) -> MeltanoPlugin | None:
        """Find plugin by name."""
        ...

    @abstractmethod
    async def save(self, plugin: MeltanoPlugin) -> FlextResult[MeltanoPlugin]:
        """Save a plugin."""
        ...

    @abstractmethod
    async def delete(self, plugin_id: str) -> FlextResult[bool]:
        """Delete a plugin."""
        ...

    @abstractmethod
    async def list_plugins(self) -> FlextResult[list[MeltanoPlugin]]:
        """List all plugins."""
        ...


# Create aliases for the expected repository names
JobRepository = FlextMeltanoJobRepository
PluginRepository = FlextMeltanoPluginRepository
ProjectRepository = FlextMeltanoProjectRepository
StateRepository = FlextMeltanoStateRepository


__all__ = [
    "FlextMeltanoJobRepository",
    "FlextMeltanoPluginRepository",
    "FlextMeltanoProjectRepository",
    "FlextMeltanoStateRepository",
    "JobRepository",
    "PluginRepository",
    "ProjectRepository",
    "StateRepository",
]
