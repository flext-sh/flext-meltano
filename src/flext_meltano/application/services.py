"""Application services for FLEXT-MELTANO v0.7.0.

REFACTORED:
    Using flext-core service patterns - NO duplication.
    Clean architecture with dependency injection and ServiceResult pattern.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextResult

# Import from local DI container
from flext_meltano.infrastructure.di_container import injectable

# Initialize types via DI container
if TYPE_CHECKING:
    from uuid import UUID

    from flext_meltano.domain.entities import (
        FlextMeltanoJob,
        FlextMeltanoPlugin,
        FlextMeltanoProject,
        FlextMeltanoState,
    )


@injectable()
class FlextMeltanoProjectService:
    """Service for managing Meltano projects."""

    def __init__(self) -> None:
        """Initialize Meltano project service."""
        self._projects: dict[UUID, FlextMeltanoProject] = {}

    async def create_project(
        self,
        name: str,
        project_root: str,
        meltano_file_path: str,
        meltano_version: str,
        python_version: str = "3.13",
        default_environment: str = "dev",
        created_by: UUID | None = None,
    ) -> FlextResult[Any]:
        """Create a new Meltano project."""
        try:
            # Importing inside TYPE_CHECKING avoids circular imports
            from flext_meltano.domain.entities import (
                EnvironmentType,
                FlextMeltanoProject,
            )

            # Convert string to enum
            if default_environment in {"staging", "prod", "test"}:
                pass

            from pathlib import Path

            project = FlextMeltanoProject(
                name=name,
                project_id=name,  # Use name as project_id
                directory=Path(project_root),  # Required directory field
                config_path=Path(meltano_file_path),  # Required config_path field
                project_root=project_root,
                meltano_yml_path=meltano_file_path,
                meltano_version=meltano_version,
                environment=default_environment,  # Use string default_environment
            )

            self._projects[project.id] = project
            return FlextResult.ok(project)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to create project: {e}")

    async def get_project(
        self,
        project_id: UUID,
    ) -> FlextResult[Any]:
        """Get a project by ID."""
        try:
            project = self._projects.get(project_id)
            return FlextResult.ok(project)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to get project: {e}")

    async def list_projects(self) -> FlextResult[Any]:
        """List all projects."""
        try:
            projects = list(self._projects.values())
            return FlextResult.ok(projects)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to list projects: {e}")

    async def update_project(
        self,
        project_id: UUID,
        updates: dict[str, Any],
    ) -> FlextResult[Any]:
        """Update a project."""
        try:
            project = self._projects.get(project_id)
            if not project:
                return FlextResult.fail("Project not found")

            for key, value in updates.items():
                if hasattr(project, key):
                    setattr(project, key, value)

            # DomainEntity has updated_at automatically managed
            # No need to manually set updated_at
            return FlextResult.ok(project)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to update project: {e}")

    async def delete_project(self, project_id: UUID) -> FlextResult[Any]:
        """Delete a project."""
        try:
            if project_id in self._projects:
                del self._projects[project_id]
                return FlextResult.ok(True)
            return FlextResult.fail("Project not found")
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to delete project: {e}")


@injectable()
class FlextMeltanoPluginService:
    """Service for managing Meltano plugins."""

    def __init__(self) -> None:
        """Initialize Meltano plugin service."""
        self._plugins: dict[UUID, FlextMeltanoPlugin] = {}

    async def install_plugin(
        self,
        project_id: UUID,
        name: str,
        namespace: str,
        plugin_type: str,
        pip_url: str | None = None,
        executable: str | None = None,
        version: str | None = None,
    ) -> FlextResult[Any]:
        """Install a plugin."""
        try:
            # Using local import to avoid circular dependencies
            from flext_meltano.domain.entities import (
                FlextMeltanoPlugin,
                PluginType,
            )

            # Convert string to enum
            plugin_type_enum = PluginType.EXTRACTOR  # default
            if plugin_type == "loaders":
                plugin_type_enum = PluginType.LOADER
            elif plugin_type == "transformers":
                plugin_type_enum = PluginType.TRANSFORMER
            elif plugin_type == "orchestrators":
                plugin_type_enum = PluginType.ORCHESTRATOR
            elif plugin_type == "utilities":
                plugin_type_enum = PluginType.UTILITY
            elif plugin_type == "files":
                plugin_type_enum = PluginType.FILE

            plugin = FlextMeltanoPlugin(
                project_id=project_id,
                name=name,
                namespace=namespace,
                plugin_type=plugin_type_enum,  # Use the enum we converted
                pip_url=pip_url,
                executable=executable or name,
                # Remove description and version - not in entity definition
            )

            plugin.install()
            self._plugins[plugin.id] = plugin
            return FlextResult.ok(plugin)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to install plugin: {e}")

    async def get_plugin(self, plugin_id: UUID) -> FlextResult[Any]:
        """Get a plugin by ID."""
        try:
            plugin = self._plugins.get(plugin_id)
            return FlextResult.ok(plugin)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to get plugin: {e}")

    async def list_plugins(
        self,
        project_id: UUID,
    ) -> FlextResult[Any]:
        """List plugins for a project."""
        try:
            plugins = [
                plugin
                for plugin in self._plugins.values()
                if plugin.project_id == project_id
            ]
            return FlextResult.ok(plugins)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to list plugins: {e}")

    async def configure_plugin(
        self,
        plugin_id: UUID,
        config: dict[str, Any],
    ) -> FlextResult[Any]:
        """Configure a plugin."""
        try:
            plugin = self._plugins.get(plugin_id)
            if not plugin:
                return FlextResult.fail("Plugin not found")

            plugin.update_config(config)  # Correct method name
            # DomainEntity has updated_at automatically managed
            return FlextResult.ok(plugin)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to configure plugin: {e}")

    async def uninstall_plugin(self, plugin_id: UUID) -> FlextResult[Any]:
        """Uninstall a plugin."""
        try:
            plugin = self._plugins.get(plugin_id)
            if not plugin:
                return FlextResult.fail("Plugin not found")

            plugin.uninstall()
            del self._plugins[plugin_id]
            return FlextResult.ok(True)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to uninstall plugin: {e}")


@injectable()
class FlextMeltanoJobService:
    """Service for managing Meltano jobs."""

    def __init__(self) -> None:
        """Initialize Meltano job service."""
        self._jobs: dict[UUID, FlextMeltanoJob] = {}

    async def create_job(
        self,
        project_id: UUID,
        job_id: str,
        job_type: str,
        command: list[str],
        environment: str = "dev",
        config: dict[str, Any] | None = None,
        triggered_by: UUID | None = None,
    ) -> FlextResult[Any]:
        """Create a new job."""
        try:
            from flext_meltano.domain.entities import (
                EnvironmentType,
                FlextMeltanoJob,
            )

            # Convert string to enum
            env_type = EnvironmentType.DEVELOPMENT
            if environment == "staging":
                env_type = EnvironmentType.STAGING
            elif environment == "prod":
                env_type = EnvironmentType.PRODUCTION
            elif environment == "test":
                env_type = EnvironmentType.TEST

            job = FlextMeltanoJob(
                project_id=project_id,
                job_id=job_id,  # Required job_id field
                name=job_id,  # Use job_id for name as well
                tasks=command,  # Use tasks field, not command
                environment=env_type,  # Use enum type
                triggered_by=triggered_by,
            )

            # Use provided config or empty dict - config is for external use,
            # not stored in job entity
            job_config = config or {}

            # Apply configuration to job
            if hasattr(job, "configuration"):
                job.configuration = job_config
            elif hasattr(job, "config"):
                job.config = job_config

            self._jobs[job.id] = job
            return FlextResult.ok(job)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to create job: {e}")

    async def start_job(self, job_id: UUID) -> FlextResult[Any]:
        """Start a job."""
        try:
            job = self._jobs.get(job_id)
            if not job:
                return FlextResult.fail("Job not found")

            job.start_execution()
            return FlextResult.ok(job)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to start job: {e}")

    async def complete_job(
        self,
        job_id: UUID,
        exit_code: int,
        stdout: str | None = None,
        stderr: str | None = None,
    ) -> FlextResult[Any]:
        """Complete a job."""
        try:
            job = self._jobs.get(job_id)
            if not job:
                return FlextResult.fail("Job not found")

            job.complete_execution(exit_code, stdout, stderr)
            return FlextResult.ok(job)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to complete job: {e}")

    async def cancel_job(self, job_id: UUID) -> FlextResult[Any]:
        """Cancel a job."""
        try:
            job = self._jobs.get(job_id)
            if not job:
                return FlextResult.fail("Job not found")

            job.cancel_execution()
            return FlextResult.ok(job)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to cancel job: {e}")

    async def get_job(self, job_id: UUID) -> FlextResult[Any]:
        """Get a job by ID."""
        try:
            job = self._jobs.get(job_id)
            return FlextResult.ok(job)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to get job: {e}")

    async def list_jobs(self, project_id: UUID) -> FlextResult[Any]:
        """List jobs for a project."""
        try:
            jobs = [job for job in self._jobs.values() if job.project_id == project_id]
            return FlextResult.ok(jobs)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to list jobs: {e}")


@injectable()
class FlextMeltanoStateService:
    """Service for managing Meltano state."""

    def __init__(self) -> None:
        """Initialize Meltano state service."""
        self._states: dict[UUID, FlextMeltanoState] = {}

    async def create_state(
        self,
        project_id: UUID,
        job_id: UUID,
        state_id: str,
        state_data: dict[str, Any],
        environment: str = "dev",
        plugin_name: str | None = None,
    ) -> FlextResult[Any]:
        """Create a new state."""
        try:
            from flext_meltano.domain.entities import (
                EnvironmentType,
                FlextMeltanoState,
            )

            # Convert string to enum
            env_type = EnvironmentType.DEVELOPMENT
            if environment == "staging":
                env_type = EnvironmentType.STAGING
            elif environment == "prod":
                env_type = EnvironmentType.PRODUCTION
            elif environment == "test":
                env_type = EnvironmentType.TEST

            state = FlextMeltanoState(
                project_id=project_id,
                job_id=str(job_id),  # Convert UUID to string
                state_id=state_id,
                plugin_name=plugin_name
                or f"plugin-{state_id}",  # Use provided or default
                state_data=state_data,
                environment=env_type,  # Use enum type
            )

            self._states[state.id] = state
            return FlextResult.ok(state)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to create state: {e}")

    async def update_state(
        self,
        state_id: UUID,
        state_data: dict[str, Any],
    ) -> FlextResult[Any]:
        """Update state."""
        try:
            state = self._states.get(state_id)
            if not state:
                return FlextResult.fail("State not found")

            state.update_state(state_data)
            return FlextResult.ok(state)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to update state: {e}")

    async def merge_state(
        self,
        state_id: UUID,
        partial_state: dict[str, Any],
    ) -> FlextResult[Any]:
        """Merge partial state."""
        try:
            state = self._states.get(state_id)
            if not state:
                return FlextResult.fail("State not found")

            state.merge_state(partial_state)
            return FlextResult.ok(state)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to merge state: {e}")

    async def get_state(self, state_id: UUID) -> FlextResult[Any]:
        """Get state by ID."""
        try:
            state = self._states.get(state_id)
            return FlextResult.ok(state)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to get state: {e}")

    async def list_states(self, project_id: UUID) -> FlextResult[Any]:
        """List states for a project."""
        try:
            states = [
                state
                for state in self._states.values()
                if state.project_id == project_id
            ]
            return FlextResult.ok(states)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to list states: {e}")

    async def delete_state(self, state_id: UUID) -> FlextResult[Any]:
        """Delete state."""
        try:
            if state_id in self._states:
                del self._states[state_id]
                return FlextResult.ok(True)
            return FlextResult.fail("State not found")
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return FlextResult.fail(f"Failed to delete state: {e}")


# Export all service classes
__all__ = [
    "FlextMeltanoJobService",
    "FlextMeltanoPluginService",
    "FlextMeltanoProjectService",
    "FlextMeltanoStateService",
]

# Compatibility alias for existing imports
FlextMeltanoProjectApplicationService = FlextMeltanoProjectService


def get_service_instances() -> dict[str, Any]:
    """Get instances of all services for testing/validation purposes."""
    return {
        "project": FlextMeltanoProjectService(),
        "job": FlextMeltanoJobService(),
        "plugin": FlextMeltanoPluginService(),
        "state": FlextMeltanoStateService(),
    }


def validate_services() -> bool:
    """Validate that all services can be instantiated correctly."""
    try:
        services = get_service_instances()

        # Validate project service
        project_service = services["project"]
        if not hasattr(project_service, "_projects"):
            return False
        if not isinstance(getattr(project_service, "_projects", None), dict):
            return False

        # Validate job service
        job_service = services["job"]
        if not hasattr(job_service, "_jobs"):
            return False
        if not isinstance(getattr(job_service, "_jobs", None), dict):
            return False

        # Validate plugin service
        plugin_service = services["plugin"]
        if not hasattr(plugin_service, "_plugins"):
            return False
        if not isinstance(getattr(plugin_service, "_plugins", None), dict):
            return False

        # Validate state service
        state_service = services["state"]
        if not hasattr(state_service, "_states"):
            return False
        return isinstance(getattr(state_service, "_states", None), dict)
    except Exception:
        return False
