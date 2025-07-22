"""Application services for FLEXT-MELTANO v0.7.0.

REFACTORED:
    Using flext-core service patterns - NO duplication.
    Clean architecture with dependency injection and ServiceResult pattern.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core.config import injectable
from flext_core.domain.shared_types import ServiceResult

if TYPE_CHECKING:
    from uuid import UUID

    from flext_meltano.domain.entities import (
        MeltanoJob,
        MeltanoPlugin,
        MeltanoProject,
        MeltanoState,
    )


@injectable()
class MeltanoProjectService:
    """Service for managing Meltano projects."""

    def __init__(self) -> None:
        """Initialize Meltano project service."""
        self._projects: dict[UUID, MeltanoProject] = {}

    async def create_project(
        self,
        name: str,
        project_root: str,
        meltano_file_path: str,
        meltano_version: str,
        python_version: str = "3.13",
        default_environment: str = "dev",
        created_by: UUID | None = None,
    ) -> ServiceResult[Any]:
        """Create a new Meltano project."""
        try:
            # Importing inside TYPE_CHECKING avoids circular imports
            from flext_meltano.domain.entities import EnvironmentType, MeltanoProject

            # Convert string to enum
            env_type = EnvironmentType.DEVELOPMENT
            if default_environment == "staging":
                env_type = EnvironmentType.STAGING
            elif default_environment == "prod":
                env_type = EnvironmentType.PRODUCTION
            elif default_environment == "test":
                env_type = EnvironmentType.TEST

            project = MeltanoProject(
                name=name,
                description=f"Meltano project: {name}",
                project_root=project_root,
                meltano_yml_path=meltano_file_path,  # Correct field name
                meltano_version=meltano_version,
                project_id=f"flext-{name}",  # Required field
                default_environment=env_type,  # Use enum type
                created_by=created_by,
            )

            self._projects[project.id] = project
            return ServiceResult.ok(project)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to create project: {e}")

    async def get_project(
        self,
        project_id: UUID,
    ) -> ServiceResult[Any]:
        """Get a project by ID."""
        try:
            project = self._projects.get(project_id)
            return ServiceResult.ok(project)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to get project: {e}")

    async def list_projects(self) -> ServiceResult[Any]:
        """List all projects."""
        try:
            projects = list(self._projects.values())
            return ServiceResult.ok(projects)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to list projects: {e}")

    async def update_project(
        self,
        project_id: UUID,
        updates: dict[str, Any],
    ) -> ServiceResult[Any]:
        """Update a project."""
        try:
            project = self._projects.get(project_id)
            if not project:
                return ServiceResult.fail("Project not found")

            for key, value in updates.items():
                if hasattr(project, key):
                    setattr(project, key, value)

            # DomainEntity has updated_at automatically managed
            # No need to manually set updated_at
            return ServiceResult.ok(project)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to update project: {e}")

    async def delete_project(self, project_id: UUID) -> ServiceResult[Any]:
        """Delete a project."""
        try:
            if project_id in self._projects:
                del self._projects[project_id]
                return ServiceResult.ok(True)
            return ServiceResult.fail("Project not found")
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to delete project: {e}")


@injectable()
class MeltanoPluginService:
    """Service for managing Meltano plugins."""

    def __init__(self) -> None:
        """Initialize Meltano plugin service."""
        self._plugins: dict[UUID, MeltanoPlugin] = {}

    async def install_plugin(
        self,
        project_id: UUID,
        name: str,
        namespace: str,
        plugin_type: str,
        pip_url: str | None = None,
        executable: str | None = None,
        version: str | None = None,
    ) -> ServiceResult[Any]:
        """Install a plugin."""
        try:
            # Using local import to avoid circular dependencies
            from flext_meltano.domain.entities import MeltanoPlugin, PluginType

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

            plugin = MeltanoPlugin(
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
            return ServiceResult.ok(plugin)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to install plugin: {e}")

    async def get_plugin(self, plugin_id: UUID) -> ServiceResult[Any]:
        """Get a plugin by ID."""
        try:
            plugin = self._plugins.get(plugin_id)
            return ServiceResult.ok(plugin)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to get plugin: {e}")

    async def list_plugins(
        self,
        project_id: UUID,
    ) -> ServiceResult[Any]:
        """List plugins for a project."""
        try:
            plugins = [
                plugin
                for plugin in self._plugins.values()
                if plugin.project_id == project_id
            ]
            return ServiceResult.ok(plugins)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to list plugins: {e}")

    async def configure_plugin(
        self,
        plugin_id: UUID,
        config: dict[str, Any],
    ) -> ServiceResult[Any]:
        """Configure a plugin."""
        try:
            plugin = self._plugins.get(plugin_id)
            if not plugin:
                return ServiceResult.fail("Plugin not found")

            plugin.update_config(config)  # Correct method name
            # DomainEntity has updated_at automatically managed
            return ServiceResult.ok(plugin)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to configure plugin: {e}")

    async def uninstall_plugin(self, plugin_id: UUID) -> ServiceResult[Any]:
        """Uninstall a plugin."""
        try:
            plugin = self._plugins.get(plugin_id)
            if not plugin:
                return ServiceResult.fail("Plugin not found")

            plugin.uninstall()
            del self._plugins[plugin_id]
            return ServiceResult.ok(True)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to uninstall plugin: {e}")


@injectable()
class MeltanoJobService:
    """Service for managing Meltano jobs."""

    def __init__(self) -> None:
        """Initialize Meltano job service."""
        self._jobs: dict[UUID, MeltanoJob] = {}

    async def create_job(
        self,
        project_id: UUID,
        job_id: str,
        job_type: str,
        command: list[str],
        environment: str = "dev",
        config: dict[str, Any] | None = None,
        triggered_by: UUID | None = None,
    ) -> ServiceResult[Any]:
        """Create a new job."""
        try:
            from flext_meltano.domain.entities import EnvironmentType, MeltanoJob

            # Convert string to enum
            env_type = EnvironmentType.DEVELOPMENT
            if environment == "staging":
                env_type = EnvironmentType.STAGING
            elif environment == "prod":
                env_type = EnvironmentType.PRODUCTION
            elif environment == "test":
                env_type = EnvironmentType.TEST

            job = MeltanoJob(
                project_id=project_id,
                name=job_id,  # Use name field, not job_id
                description=f"Meltano job: {job_type}",
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
            return ServiceResult.ok(job)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to create job: {e}")

    async def start_job(self, job_id: UUID) -> ServiceResult[Any]:
        """Start a job."""
        try:
            job = self._jobs.get(job_id)
            if not job:
                return ServiceResult.fail("Job not found")

            job.start_execution()
            return ServiceResult.ok(job)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to start job: {e}")

    async def complete_job(
        self,
        job_id: UUID,
        exit_code: int,
        stdout: str | None = None,
        stderr: str | None = None,
    ) -> ServiceResult[Any]:
        """Complete a job."""
        try:
            job = self._jobs.get(job_id)
            if not job:
                return ServiceResult.fail("Job not found")

            job.complete_execution(exit_code, stdout, stderr)
            return ServiceResult.ok(job)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to complete job: {e}")

    async def cancel_job(self, job_id: UUID) -> ServiceResult[Any]:
        """Cancel a job."""
        try:
            job = self._jobs.get(job_id)
            if not job:
                return ServiceResult.fail("Job not found")

            job.cancel_execution()
            return ServiceResult.ok(job)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to cancel job: {e}")

    async def get_job(self, job_id: UUID) -> ServiceResult[Any]:
        """Get a job by ID."""
        try:
            job = self._jobs.get(job_id)
            return ServiceResult.ok(job)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to get job: {e}")

    async def list_jobs(self, project_id: UUID) -> ServiceResult[Any]:
        """List jobs for a project."""
        try:
            jobs = [job for job in self._jobs.values() if job.project_id == project_id]
            return ServiceResult.ok(jobs)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to list jobs: {e}")


@injectable()
class MeltanoStateService:
    """Service for managing Meltano state."""

    def __init__(self) -> None:
        """Initialize Meltano state service."""
        self._states: dict[UUID, MeltanoState] = {}

    async def create_state(
        self,
        project_id: UUID,
        job_id: UUID,
        state_id: str,
        state_data: dict[str, Any],
        environment: str = "dev",
        plugin_name: str | None = None,
    ) -> ServiceResult[Any]:
        """Create a new state."""
        try:
            from flext_meltano.domain.entities import EnvironmentType, MeltanoState

            # Convert string to enum
            env_type = EnvironmentType.DEVELOPMENT
            if environment == "staging":
                env_type = EnvironmentType.STAGING
            elif environment == "prod":
                env_type = EnvironmentType.PRODUCTION
            elif environment == "test":
                env_type = EnvironmentType.TEST

            state = MeltanoState(
                project_id=project_id,
                job_id=job_id,
                state_id=state_id,
                plugin_name=plugin_name
                or f"plugin-{state_id}",  # Use provided or default
                state_data=state_data,
                environment=env_type,  # Use enum type
            )

            self._states[state.id] = state
            return ServiceResult.ok(state)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to create state: {e}")

    async def update_state(
        self,
        state_id: UUID,
        state_data: dict[str, Any],
    ) -> ServiceResult[Any]:
        """Update state."""
        try:
            state = self._states.get(state_id)
            if not state:
                return ServiceResult.fail("State not found")

            state.update_state(state_data)
            return ServiceResult.ok(state)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to update state: {e}")

    async def merge_state(
        self,
        state_id: UUID,
        partial_state: dict[str, Any],
    ) -> ServiceResult[Any]:
        """Merge partial state."""
        try:
            state = self._states.get(state_id)
            if not state:
                return ServiceResult.fail("State not found")

            state.merge_state(partial_state)
            return ServiceResult.ok(state)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to merge state: {e}")

    async def get_state(self, state_id: UUID) -> ServiceResult[Any]:
        """Get state by ID."""
        try:
            state = self._states.get(state_id)
            return ServiceResult.ok(state)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to get state: {e}")

    async def list_states(self, project_id: UUID) -> ServiceResult[Any]:
        """List states for a project."""
        try:
            states = [
                state
                for state in self._states.values()
                if state.project_id == project_id
            ]
            return ServiceResult.ok(states)
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to list states: {e}")

    async def delete_state(self, state_id: UUID) -> ServiceResult[Any]:
        """Delete state."""
        try:
            if state_id in self._states:
                del self._states[state_id]
                return ServiceResult.ok(True)
            return ServiceResult.fail("State not found")
        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return ServiceResult.fail(f"Failed to delete state: {e}")
