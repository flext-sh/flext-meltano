"""Project Application Service - NEW SEMANTIC ARCHITECTURE.

🚨 DEPRECATION WARNING: Direct imports from this file are deprecated.

❌ OLD: from flext_meltano.application.services.project_service import ProjectApplicationService
✅ NEW: from flext_meltano import ProjectService

ProjectApplicationService coordinates project-related use cases
using flext-core foundation patterns.
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any

from flext_core import FlextResult
from flext_core.container import FlextContainer

from flext_meltano.domain.entities import MeltanoProject

# 🚨 ARCHITECTURAL COMPLIANCE: Using modern flext-core patterns
from flext_meltano.infrastructure.di_container import (
    AbstractService,
)

if TYPE_CHECKING:
    from pathlib import Path

    from flext_meltano.application.interfaces.external_services import (
        MeltanoCLIService,
    )
    from flext_meltano.application.interfaces.repositories import (
        ProjectRepository,
    )


class ProjectApplicationService(AbstractService):
    """Application service for Meltano project operations."""

    def __init__(
        self,
        project_repository: ProjectRepository,
        meltano_cli_service: MeltanoCLIService,
    ) -> None:
        """Initialize project application service."""
        self._project_repository = project_repository
        self._meltano_cli_service = meltano_cli_service

    async def create_project(
        self,
        name: str,
        directory: Path,
        description: str | None = None,
    ) -> FlextResult[Any]:
        """Create a new Meltano project."""
        # Check if project already exists
        existing = await self._project_repository.find_by_name(name)
        if existing:
            return FlextResult.fail(
                f"Project '{name}' already exists",
            )

        # Create project entity with business rules
        try:
            project = MeltanoProject(
                name=name,
                directory=directory,
                config_path=directory / "meltano.yml",
                description=description,
            )
        except ValueError as e:
            return FlextResult.fail(f"Invalid project data: {e}")

        # Initialize project via Meltano CLI
        init_result = await self._meltano_cli_service.init_project(name, str(directory))
        if not init_result.success:
            return FlextResult.fail(
                f"Failed to initialize Meltano project: {init_result.error}",
            )

        # Save project
        save_result = await self._project_repository.save(project)
        if not save_result.success:
            return FlextResult.fail(
                f"Failed to save project: {save_result.error}",
            )

        return FlextResult.ok({"project": project})

    async def get_project(self, name: str) -> ServiceResult[Any]:
        """Get project by name."""
        project = await self._project_repository.find_by_name(name)
        if not project:
            return FlextResult.fail(f"Project '{name}' not found")

        return FlextResult.ok({"project": project})

    async def activate_project(self, name: str) -> ServiceResult[Any]:
        """Activate a project."""
        project = await self._project_repository.find_by_name(name)
        if not project:
            return FlextResult.fail(f"Project '{name}' not found")

        # Use domain method with business rules
        activate_result = project.activate()
        if not activate_result.success:
            return FlextResult.fail(
                activate_result.error or "Activation failed",
            )

        # Save updated project
        save_result = await self._project_repository.save(project)
        if not save_result.success:
            return FlextResult.fail(
                f"Failed to save project: {save_result.error}",
            )

        return FlextResult.ok({"project": project})

    async def deactivate_project(self, name: str) -> ServiceResult[Any]:
        """Deactivate a project."""
        project = await self._project_repository.find_by_name(name)
        if not project:
            return FlextResult.fail(f"Project '{name}' not found")

        # Use domain method with business rules
        deactivate_result = project.deactivate()
        if not deactivate_result.success:
            return FlextResult.fail(
                deactivate_result.error or "Deactivation failed",
            )

        # Save updated project
        save_result = await self._project_repository.save(project)
        if not save_result.success:
            return FlextResult.fail(
                f"Failed to save project: {save_result.error}",
            )

        return FlextResult.ok({"project": project})

    async def change_environment(
        self,
        name: str,
        environment: str,
    ) -> FlextResult[Any]:
        """Change project environment."""
        project = await self._project_repository.find_by_name(name)
        if not project:
            return FlextResult.fail(f"Project '{name}' not found")

        # Use domain method with business rules
        change_result = project.change_environment(environment)
        if not change_result.success:
            return FlextResult.fail(
                change_result.error or "Environment change failed",
            )

        # Save updated project
        save_result = await self._project_repository.save(project)
        if not save_result.success:
            return FlextResult.fail(
                f"Failed to save project: {save_result.error}",
            )

        return FlextResult.ok({"project": project})

    async def update_project_status(
        self,
        name: str,
        status: str,
    ) -> FlextResult[Any]:
        """Update project status."""
        project = await self._project_repository.find_by_name(name)
        if not project:
            return FlextResult.fail(f"Project '{name}' not found")

        # Use domain method with business rules
        status_result = project.update_status(status)
        if not status_result.success:
            return FlextResult.fail(
                status_result.error or "Status update failed",
            )

        # Save updated project
        save_result = await self._project_repository.save(project)
        if not save_result.success:
            return FlextResult.fail(
                f"Failed to save project: {save_result.error}",
            )

        return FlextResult.ok({"project": project})

    async def list_projects(self) -> ServiceResult[Any]:
        """List all projects."""
        projects = await self._project_repository.find_all()
        return FlextResult.ok(projects)

    async def delete_project(self, name: str) -> ServiceResult[Any]:
        """Delete a project."""
        project = await self._project_repository.find_by_name(name)
        if not project:
            return FlextResult.fail(f"Project '{name}' not found")

        # Business rule: cannot delete active projects
        if project.is_active:
            return FlextResult.fail(
                "Cannot delete active project. Deactivate it first.",
            )

        # Delete from repository
        delete_result = await self._project_repository.delete(str(project.id))
        if not delete_result.success:
            return FlextResult.fail(
                f"Failed to delete project: {delete_result.error}",
            )

        return FlextResult.ok(None)

    def validate_invariants(self) -> bool:
        """Validate service invariants."""
        # Dependencies are guaranteed to be non-None by constructor
        # Service is always valid if properly constructed
        return True


# Deprecation warning for direct imports
def __getattr__(name: str) -> Any:
    """Handle direct imports with deprecation warning."""
    if name == "ProjectApplicationService":
        warnings.warn(
            "🚨 DEPRECATED: Importing ProjectApplicationService from 'flext_meltano.application.services.project_service' is deprecated.\n"
            "✅ Use: from flext_meltano import ProjectService\n"
            "📖 This import will be removed in version 0.8.0.\n"
            "📚 Migration guide: https://docs.flext.dev/migration/meltano",
            DeprecationWarning,
            stacklevel=2,
        )
        return ProjectApplicationService
    msg = f"module 'flext_meltano.application.services.project_service' has no attribute '{name}'"
    raise AttributeError(
        msg,
    )
