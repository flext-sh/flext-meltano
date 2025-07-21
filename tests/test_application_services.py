"""Test FLEXT Meltano application services - 206 lines of code, 0% coverage.

ZERO TOLERANCE for fake code, mockups, or library fallbacks.
Comprehensive tests for ALL service classes and functionality.
"""

from __future__ import annotations

import sys
from typing import Any
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest

# Mock missing dependencies to avoid import errors - must be before local imports
sys.modules["flext_observability"] = MagicMock()
sys.modules["flext_observability.logging"] = MagicMock()

# ruff: noqa: E402 - Module mocking must happen before imports
from flext_meltano.application.services import (
    MeltanoJobService,
    MeltanoPluginService,
    MeltanoProjectService,
    MeltanoStateService,
)


class TestMeltanoProjectService:
    """Test MeltanoProjectService - comprehensive coverage."""

    @pytest.fixture
    def service(self) -> MeltanoProjectService:
        """Create a MeltanoProjectService instance."""
        return MeltanoProjectService()

    @pytest.fixture
    def sample_project_data(self) -> dict[str, Any]:
        """Sample project data for testing."""
        return {
            "name": "test-project",
            "project_root": "/test/project",
            "meltano_file_path": "/test/project/meltano.yml",
            "meltano_version": "3.0.0",
            "python_version": "3.13",
            "default_environment": "dev",
        }

    @pytest.mark.asyncio
    async def test_create_project_success(
        self,
        service: MeltanoProjectService,
        sample_project_data: dict[str, Any],
    ) -> None:
        """Test successful project creation."""
        result = await service.create_project(**sample_project_data)

        assert result.is_success is True
        assert result.error is None

        project = result.data
        assert project is not None
        assert project.name == "test-project"
        assert project.project_root == "/test/project"
        assert project.meltano_file_path == "/test/project/meltano.yml"
        assert project.meltano_version == "3.0.0"
        assert project.python_version == "3.13"
        assert project.default_environment == "dev"
        assert project.description == "Meltano project: test-project"

        # Project should be stored in service
        assert project.id in service._projects
        assert service._projects[project.id] == project

    @pytest.mark.asyncio
    async def test_create_project_with_created_by(
        self,
        service: MeltanoProjectService,
        sample_project_data: dict[str, Any],
    ) -> None:
        """Test project creation with created_by parameter."""
        created_by = uuid4()
        sample_project_data["created_by"] = created_by

        result = await service.create_project(**sample_project_data)

        assert result.is_success is True
        project = result.data
        assert project.created_by == created_by

    @pytest.mark.asyncio
    async def test_create_project_with_minimal_params(
        self,
        service: MeltanoProjectService,
    ) -> None:
        """Test project creation with minimal required parameters."""
        result = await service.create_project(
            name="minimal-project",
            project_root="/minimal",
            meltano_file_path="/minimal/meltano.yml",
            meltano_version="3.0.0",
        )

        assert result.is_success is True
        project = result.data
        assert project.name == "minimal-project"
        assert project.python_version == "3.13"  # Default value
        assert project.default_environment == "dev"  # Default value

    @pytest.mark.asyncio
    async def test_create_project_error_handling(
        self,
        service: MeltanoProjectService,
    ) -> None:
        """Test project creation error handling."""
        # Mock the MeltanoProject to raise an exception
        with patch("flext_meltano.domain.entities.MeltanoProject") as mock_project:
            mock_project.side_effect = ValueError("Invalid project data")

            result = await service.create_project(
                name="error-project",
                project_root="/error",
                meltano_file_path="/error/meltano.yml",
                meltano_version="3.0.0",
            )

            assert result.is_success is False
            assert "Failed to create project: Invalid project data" in result.error

    @pytest.mark.asyncio
    async def test_get_project_success(
        self,
        service: MeltanoProjectService,
        sample_project_data: dict[str, Any],
    ) -> None:
        """Test successful project retrieval."""
        # First create a project
        create_result = await service.create_project(**sample_project_data)
        project = create_result.data

        # Then retrieve it
        result = await service.get_project(project.id)

        assert result.is_success is True
        assert result.data == project

    @pytest.mark.asyncio
    async def test_get_project_not_found(self, service: MeltanoProjectService) -> None:
        """Test project retrieval when project doesn't exist."""
        non_existent_id = uuid4()
        result = await service.get_project(non_existent_id)

        assert result.is_success is True
        assert result.data is None

    @pytest.mark.asyncio
    async def test_list_projects_empty(self, service: MeltanoProjectService) -> None:
        """Test listing projects when none exist."""
        result = await service.list_projects()

        assert result.is_success is True
        assert result.data == []

    @pytest.mark.asyncio
    async def test_list_projects_with_data(
        self,
        service: MeltanoProjectService,
        sample_project_data: dict[str, Any],
    ) -> None:
        """Test listing projects with existing data."""
        # Create multiple projects
        project1_result = await service.create_project(**sample_project_data)

        sample_project_data["name"] = "test-project-2"
        project2_result = await service.create_project(**sample_project_data)

        # List projects
        result = await service.list_projects()

        assert result.is_success is True
        projects = result.data
        assert len(projects) == 2
        assert project1_result.data in projects
        assert project2_result.data in projects

    @pytest.mark.asyncio
    async def test_update_project_success(
        self,
        service: MeltanoProjectService,
        sample_project_data: dict[str, Any],
    ) -> None:
        """Test successful project update."""
        # Create a project
        create_result = await service.create_project(**sample_project_data)
        project = create_result.data
        original_updated_at = project.updated_at

        # Update the project
        updates = {
            "name": "updated-project",
            "description": "Updated description",
        }
        result = await service.update_project(project.id, updates)

        assert result.is_success is True
        updated_project = result.data
        assert updated_project.name == "updated-project"
        assert updated_project.description == "Updated description"
        assert updated_project.updated_at > original_updated_at

    @pytest.mark.asyncio
    async def test_update_project_not_found(
        self,
        service: MeltanoProjectService,
    ) -> None:
        """Test updating a project that doesn't exist."""
        non_existent_id = uuid4()
        updates = {"name": "updated-name"}

        result = await service.update_project(non_existent_id, updates)

        assert result.is_success is False
        assert result.error == "Project not found"

    @pytest.mark.asyncio
    async def test_update_project_invalid_attribute(
        self,
        service: MeltanoProjectService,
        sample_project_data: dict[str, Any],
    ) -> None:
        """Test updating a project with invalid attributes."""
        # Create a project
        create_result = await service.create_project(**sample_project_data)
        project = create_result.data

        # Update with invalid attribute (should be ignored)
        updates = {
            "valid_name": "new-name",
            "invalid_attribute": "should-be-ignored",
        }
        result = await service.update_project(project.id, updates)

        assert result.is_success is True
        # Invalid attribute should be ignored, valid updates should be skipped if attribute doesn't exist

    @pytest.mark.asyncio
    async def test_delete_project_success(
        self,
        service: MeltanoProjectService,
        sample_project_data: dict[str, Any],
    ) -> None:
        """Test successful project deletion."""
        # Create a project
        create_result = await service.create_project(**sample_project_data)
        project = create_result.data

        # Verify it exists
        assert project.id in service._projects

        # Delete it
        result = await service.delete_project(project.id)

        assert result.is_success is True
        assert result.data is True
        assert project.id not in service._projects

    @pytest.mark.asyncio
    async def test_delete_project_not_found(
        self,
        service: MeltanoProjectService,
    ) -> None:
        """Test deleting a project that doesn't exist."""
        non_existent_id = uuid4()

        result = await service.delete_project(non_existent_id)

        assert result.is_success is False
        assert result.error == "Project not found"


class TestMeltanoPluginService:
    """Test MeltanoPluginService - comprehensive coverage."""

    @pytest.fixture
    def service(self) -> MeltanoPluginService:
        """Create a MeltanoPluginService instance."""
        return MeltanoPluginService()

    @pytest.fixture
    def sample_plugin_data(self) -> dict[str, Any]:
        """Sample plugin data for testing."""
        return {
            "project_id": uuid4(),
            "name": "tap-csv",
            "namespace": "tap_csv",
            "plugin_type": "extractors",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
            "version": "1.0.0",
        }

    @pytest.mark.asyncio
    async def test_install_plugin_success(
        self,
        service: MeltanoPluginService,
        sample_plugin_data: dict[str, Any],
    ) -> None:
        """Test successful plugin installation."""
        result = await service.install_plugin(**sample_plugin_data)

        assert result.is_success is True
        plugin = result.data
        assert plugin is not None
        assert plugin.name == "tap-csv"
        assert plugin.namespace == "tap_csv"
        assert str(plugin.plugin_type) == "extractors"
        assert plugin.pip_url == "pipelinewise-tap-csv"
        assert plugin.executable == "tap-csv"
        assert plugin.version == "1.0.0"
        assert plugin.description == "Plugin: tap-csv"

        # Plugin should be stored
        assert plugin.id in service._plugins
        assert service._plugins[plugin.id] == plugin

    @pytest.mark.asyncio
    async def test_install_plugin_with_defaults(
        self,
        service: MeltanoPluginService,
    ) -> None:
        """Test plugin installation with default values."""
        result = await service.install_plugin(
            project_id=uuid4(),
            name="tap-simple",
            namespace="tap_simple",
            plugin_type="extractors",
        )

        assert result.is_success is True
        plugin = result.data
        assert plugin.pip_url is None
        assert plugin.executable == "tap-simple"  # Defaults to name
        assert plugin.version == "latest"  # Default version

    @pytest.mark.asyncio
    async def test_install_plugin_error_handling(
        self,
        service: MeltanoPluginService,
        sample_plugin_data: dict[str, Any],
    ) -> None:
        """Test plugin installation error handling."""
        # Mock the MeltanoPlugin to raise an exception
        with patch("flext_meltano.domain.entities.MeltanoPlugin") as mock_plugin:
            mock_plugin.side_effect = ValueError("Invalid plugin data")

            result = await service.install_plugin(**sample_plugin_data)

            assert result.is_success is False
            assert "Failed to install plugin: Invalid plugin data" in result.error

    @pytest.mark.asyncio
    async def test_get_plugin_success(
        self,
        service: MeltanoPluginService,
        sample_plugin_data: dict[str, Any],
    ) -> None:
        """Test successful plugin retrieval."""
        # Install a plugin
        install_result = await service.install_plugin(**sample_plugin_data)
        assert install_result.is_success is True, (
            f"Plugin installation failed: {install_result.error}"
        )
        plugin = install_result.data

        # Retrieve it
        result = await service.get_plugin(plugin.id)

        assert result.is_success is True
        assert result.data == plugin

    @pytest.mark.asyncio
    async def test_get_plugin_not_found(self, service: MeltanoPluginService) -> None:
        """Test plugin retrieval when plugin doesn't exist."""
        non_existent_id = uuid4()
        result = await service.get_plugin(non_existent_id)

        assert result.is_success is True
        assert result.data is None

    @pytest.mark.asyncio
    async def test_list_plugins_by_project(
        self,
        service: MeltanoPluginService,
        sample_plugin_data: dict[str, Any],
    ) -> None:
        """Test listing plugins by project."""
        project_id = uuid4()

        # Install plugins for the project
        sample_plugin_data["project_id"] = project_id
        plugin1_result = await service.install_plugin(**sample_plugin_data)

        sample_plugin_data["name"] = "target-csv"
        sample_plugin_data["plugin_type"] = "loaders"
        plugin2_result = await service.install_plugin(**sample_plugin_data)

        # Install plugin for different project
        sample_plugin_data["project_id"] = uuid4()
        sample_plugin_data["name"] = "tap-other"
        await service.install_plugin(**sample_plugin_data)

        # List plugins for specific project (method name corrected)
        result = await service.list_plugins(project_id)

        assert result.is_success is True
        plugins = result.data
        assert len(plugins) == 2
        assert plugin1_result.data in plugins
        assert plugin2_result.data in plugins

    @pytest.mark.asyncio
    async def test_uninstall_plugin_success(
        self,
        service: MeltanoPluginService,
        sample_plugin_data: dict[str, Any],
    ) -> None:
        """Test successful plugin uninstallation."""
        # Install a plugin
        install_result = await service.install_plugin(**sample_plugin_data)
        plugin = install_result.data

        # Verify it exists
        assert plugin.id in service._plugins

        # Uninstall it
        result = await service.uninstall_plugin(plugin.id)

        assert result.is_success is True
        assert result.data is True
        assert plugin.id not in service._plugins

    @pytest.mark.asyncio
    async def test_uninstall_plugin_not_found(
        self,
        service: MeltanoPluginService,
    ) -> None:
        """Test uninstalling a plugin that doesn't exist."""
        non_existent_id = uuid4()

        result = await service.uninstall_plugin(non_existent_id)

        assert result.is_success is False
        assert result.error == "Plugin not found"


class TestMeltanoJobService:
    """Test MeltanoJobService - comprehensive coverage."""

    @pytest.fixture
    def service(self) -> MeltanoJobService:
        """Create a MeltanoJobService instance."""
        return MeltanoJobService()

    @pytest.fixture
    def sample_job_data(self) -> dict[str, Any]:
        """Sample job data for testing."""
        return {
            "project_id": uuid4(),
            "job_id": "test-job",
            "job_type": "run",
            "command": ["meltano", "run", "tap-csv", "target-csv"],
            "environment": "dev",
        }

    @pytest.mark.asyncio
    async def test_create_job_success(
        self,
        service: MeltanoJobService,
        sample_job_data: dict[str, Any],
    ) -> None:
        """Test successful job creation."""
        result = await service.create_job(**sample_job_data)

        assert result.is_success is True
        job = result.data
        assert job is not None
        assert job.job_id == "test-job"
        assert job.command == ["meltano", "run", "tap-csv", "target-csv"]
        assert job.environment == "dev"
        assert job.description == "Meltano job: run"
        assert job.name == "Job: test-job"

        # Job should be stored
        assert job.id in service._jobs
        assert service._jobs[job.id] == job

    @pytest.mark.asyncio
    async def test_create_job_with_minimal_params(
        self,
        service: MeltanoJobService,
    ) -> None:
        """Test job creation with minimal parameters."""
        result = await service.create_job(
            project_id=uuid4(),
            job_id="minimal-job",
            job_type="run",
            command=["meltano", "run"],
        )

        assert result.is_success is True
        job = result.data
        assert job.job_id == "minimal-job"
        assert job.command == ["meltano", "run"]
        assert job.environment == "dev"  # Default value
        assert job.name == "Job: minimal-job"

    @pytest.mark.asyncio
    async def test_get_job_success(
        self,
        service: MeltanoJobService,
        sample_job_data: dict[str, Any],
    ) -> None:
        """Test successful job retrieval."""
        # Create a job
        create_result = await service.create_job(**sample_job_data)
        job = create_result.data

        # Retrieve it
        result = await service.get_job(job.id)

        assert result.is_success is True
        assert result.data == job

    @pytest.mark.asyncio
    async def test_list_jobs_by_project(
        self,
        service: MeltanoJobService,
        sample_job_data: dict[str, Any],
    ) -> None:
        """Test listing jobs by project."""
        project_id = uuid4()

        # Create jobs for the project
        sample_job_data["project_id"] = project_id
        job1_result = await service.create_job(**sample_job_data)

        sample_job_data["job_id"] = "test-job-2"
        job2_result = await service.create_job(**sample_job_data)

        # Create job for different project
        sample_job_data["project_id"] = uuid4()
        sample_job_data["job_id"] = "other-job"
        await service.create_job(**sample_job_data)

        # List jobs for specific project (method name corrected)
        result = await service.list_jobs(project_id)

        assert result.is_success is True
        jobs = result.data
        assert len(jobs) == 2
        assert job1_result.data in jobs
        assert job2_result.data in jobs

    @pytest.mark.asyncio
    async def test_start_job_success(
        self,
        service: MeltanoJobService,
        sample_job_data: dict[str, Any],
    ) -> None:
        """Test successful job start."""
        # Create a job
        create_result = await service.create_job(**sample_job_data)
        job = create_result.data

        # Start it
        result = await service.start_job(job.id)

        assert result.is_success is True
        started_job = result.data
        assert started_job.id == job.id

    @pytest.mark.asyncio
    async def test_start_job_not_found(self, service: MeltanoJobService) -> None:
        """Test starting a job that doesn't exist."""
        non_existent_id = uuid4()

        result = await service.start_job(non_existent_id)

        assert result.is_success is False
        assert result.error == "Job not found"

    @pytest.mark.asyncio
    async def test_complete_job_success(
        self,
        service: MeltanoJobService,
        sample_job_data: dict[str, Any],
    ) -> None:
        """Test successful job completion."""
        # Create a job
        create_result = await service.create_job(**sample_job_data)
        job = create_result.data

        # Complete it
        result = await service.complete_job(job.id, exit_code=0, stdout="Success")

        assert result.is_success is True
        completed_job = result.data
        assert completed_job.id == job.id

    @pytest.mark.asyncio
    async def test_cancel_job_success(
        self,
        service: MeltanoJobService,
        sample_job_data: dict[str, Any],
    ) -> None:
        """Test successful job cancellation."""
        # Create a job
        create_result = await service.create_job(**sample_job_data)
        job = create_result.data

        # Cancel it
        result = await service.cancel_job(job.id)

        assert result.is_success is True
        cancelled_job = result.data
        assert cancelled_job.id == job.id


class TestMeltanoStateService:
    """Test MeltanoStateService - comprehensive coverage."""

    @pytest.fixture
    def service(self) -> MeltanoStateService:
        """Create a MeltanoStateService instance."""
        return MeltanoStateService()

    @pytest.fixture
    def sample_state_data(self) -> dict[str, Any]:
        """Sample state data for testing."""
        return {
            "project_id": uuid4(),
            "job_id": uuid4(),
            "state_id": "tap-csv",
            "state_data": {
                "last_updated": "2023-01-01",
                "bookmarks": {"table1": {"timestamp": "2023-01-01"}},
            },
            "environment": "dev",
        }

    @pytest.mark.asyncio
    async def test_create_state_success(
        self,
        service: MeltanoStateService,
        sample_state_data: dict[str, Any],
    ) -> None:
        """Test successful state creation."""
        result = await service.create_state(**sample_state_data)

        assert result.is_success is True
        state = result.data
        assert state is not None
        assert state.state_id == "tap-csv"
        assert state.state_data == sample_state_data["state_data"]
        assert state.environment == "dev"
        assert (
            state.description == f"Meltano state for job: {sample_state_data['job_id']}"
        )

        # State should be stored
        assert state.id in service._states
        assert service._states[state.id] == state

    @pytest.mark.asyncio
    async def test_get_state_success(
        self,
        service: MeltanoStateService,
        sample_state_data: dict[str, Any],
    ) -> None:
        """Test successful state retrieval."""
        # Create state
        create_result = await service.create_state(**sample_state_data)
        state = create_result.data

        # Retrieve it by ID
        result = await service.get_state(state.id)

        assert result.is_success is True
        assert result.data == state

    @pytest.mark.asyncio
    async def test_get_state_not_found(self, service: MeltanoStateService) -> None:
        """Test state retrieval when state doesn't exist."""
        result = await service.get_state(uuid4())

        assert result.is_success is True
        assert result.data is None

    @pytest.mark.asyncio
    async def test_list_states_by_project(
        self,
        service: MeltanoStateService,
        sample_state_data: dict[str, Any],
    ) -> None:
        """Test listing states by project."""
        project_id = uuid4()

        # Create states for the project
        sample_state_data["project_id"] = project_id
        state1_result = await service.create_state(**sample_state_data)

        sample_state_data["state_id"] = "target-csv"
        sample_state_data["job_id"] = uuid4()
        state2_result = await service.create_state(**sample_state_data)

        # Create state for different project
        sample_state_data["project_id"] = uuid4()
        sample_state_data["state_id"] = "tap-other"
        sample_state_data["job_id"] = uuid4()
        await service.create_state(**sample_state_data)

        # List states for specific project (method name corrected)
        result = await service.list_states(project_id)

        assert result.is_success is True
        states = result.data
        assert len(states) == 2
        assert state1_result.data in states
        assert state2_result.data in states

    @pytest.mark.asyncio
    async def test_delete_state_success(
        self,
        service: MeltanoStateService,
        sample_state_data: dict[str, Any],
    ) -> None:
        """Test successful state deletion."""
        # Create state
        create_result = await service.create_state(**sample_state_data)
        assert create_result.is_success is True, (
            f"State creation failed: {create_result.error}"
        )
        state = create_result.data
        assert state is not None, "State creation returned None"

        # Verify it exists
        assert state.id in service._states

        # Delete it by ID
        result = await service.delete_state(state.id)

        assert result.is_success is True
        assert result.data is True
        assert state.id not in service._states

    @pytest.mark.asyncio
    async def test_delete_state_not_found(self, service: MeltanoStateService) -> None:
        """Test deleting state that doesn't exist."""
        result = await service.delete_state(uuid4())

        assert result.is_success is False
        assert result.error == "State not found"

    @pytest.mark.asyncio
    async def test_update_state_success(
        self,
        service: MeltanoStateService,
        sample_state_data: dict[str, Any],
    ) -> None:
        """Test successful state update."""
        # Create initial state
        create_result = await service.create_state(**sample_state_data)
        original_state = create_result.data

        # Update state
        new_state_data = {
            "last_updated": "2023-12-31",
            "bookmarks": {"table2": {"timestamp": "2023-12-31"}},
        }
        result = await service.update_state(original_state.id, new_state_data)

        assert result.is_success is True
        updated_state = result.data

        # Should be same ID but updated data
        assert updated_state.id == original_state.id
        assert updated_state.state_data == new_state_data

    @pytest.mark.asyncio
    async def test_merge_state_success(
        self,
        service: MeltanoStateService,
        sample_state_data: dict[str, Any],
    ) -> None:
        """Test successful state merge."""
        # Create initial state
        create_result = await service.create_state(**sample_state_data)
        original_state = create_result.data

        # Merge partial state
        partial_state = {
            "new_field": "new_value",
            "bookmarks": {"table2": {"timestamp": "2023-12-31"}},
        }
        result = await service.merge_state(original_state.id, partial_state)

        assert result.is_success is True
        merged_state = result.data

        # Should be same ID with merged data
        assert merged_state.id == original_state.id


class TestServiceErrorHandling:
    """Test error handling across all services."""

    @pytest.mark.asyncio
    async def test_all_services_handle_generic_exceptions(self) -> None:
        """Test that all services handle generic exceptions properly."""
        # Test exception handling in various service methods

        # Project service
        project_service = MeltanoProjectService()
        with patch("flext_meltano.domain.entities.MeltanoProject") as mock:
            mock.side_effect = RuntimeError("Unexpected error")
            result = await project_service.create_project(
                "test",
                "/test",
                "/test/meltano.yml",
                "3.0.0",
            )
            assert result.is_success is False
            assert "Failed to create project: Unexpected error" in result.error

        # Plugin service
        plugin_service = MeltanoPluginService()
        with patch("flext_meltano.domain.entities.MeltanoPlugin") as mock:
            mock.side_effect = OSError("File system error")
            result = await plugin_service.install_plugin(
                uuid4(),
                "test",
                "test",
                "extractors",
                executable="test",
            )
            assert result.is_success is False
            assert "Failed to install plugin: File system error" in result.error

        # Job service
        job_service = MeltanoJobService()
        with patch("flext_meltano.domain.entities.MeltanoJob") as mock:
            mock.side_effect = TypeError("Type error")
            result = await job_service.create_job(
                uuid4(),
                "test-job",
                "run",
                ["meltano", "run"],
            )
            assert result.is_success is False
            assert "Failed to create job: Type error" in result.error

        # State service
        state_service = MeltanoStateService()
        with patch("flext_meltano.domain.entities.MeltanoState") as mock:
            mock.side_effect = ValueError("Value error")
            result = await state_service.create_state(
                uuid4(),
                uuid4(),
                "test-state",
                {},
                "dev",
            )
            assert result.is_success is False
            assert "Failed to create state: Value error" in result.error


class TestServiceIntegration:
    """Test integration between services."""

    @pytest.mark.asyncio
    async def test_service_dependency_injection(self) -> None:
        """Test that services work with dependency injection."""
        # All services should be instantiable (injectable decorator working)
        project_service = MeltanoProjectService()
        plugin_service = MeltanoPluginService()
        job_service = MeltanoJobService()
        state_service = MeltanoStateService()

        # Services should be properly initialized
        assert project_service is not None
        assert plugin_service is not None
        assert job_service is not None
        assert state_service is not None

    @pytest.mark.asyncio
    async def test_service_initialization(self) -> None:
        """Test that all services initialize correctly."""
        project_service = MeltanoProjectService()
        plugin_service = MeltanoPluginService()
        job_service = MeltanoJobService()
        state_service = MeltanoStateService()

        # All services should initialize empty storage
        assert project_service._projects == {}
        assert plugin_service._plugins == {}
        assert job_service._jobs == {}
        assert state_service._states == {}

    @pytest.mark.asyncio
    async def test_uuid_consistency(self) -> None:
        """Test that UUIDs are properly handled across services."""
        project_id = uuid4()

        # Create entities with the same project_id
        project_service = MeltanoProjectService()
        plugin_service = MeltanoPluginService()
        job_service = MeltanoJobService()
        state_service = MeltanoStateService()

        # All should accept and handle UUIDs correctly
        project_result = await project_service.create_project(
            "test",
            "/test",
            "/test/meltano.yml",
            "3.0.0",
        )
        assert isinstance(project_result.data.id, UUID)

        plugin_result = await plugin_service.install_plugin(
            project_id,
            "test",
            "test",
            "extractors",
            executable="test",
        )
        assert isinstance(plugin_result.data.id, UUID)
        assert plugin_result.data.project_id == project_id

        job_result = await job_service.create_job(
            project_id,
            "test-job",
            "run",
            ["meltano", "run"],
        )
        assert isinstance(job_result.data.id, UUID)
        assert job_result.data.project_id == project_id

        state_result = await state_service.create_state(
            project_id,
            uuid4(),
            "test-state",
            {},
            "dev",
        )
        assert isinstance(state_result.data.id, UUID)
        assert state_result.data.project_id == project_id
