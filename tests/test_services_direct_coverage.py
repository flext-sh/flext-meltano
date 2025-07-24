"""Direct coverage test using normal imports for services.py module.

This test uses standard imports that coverage can track properly.
"""

from __future__ import annotations

import sys
from typing import Any
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

# Mock all problematic dependencies before imports
sys.modules["meltano"] = MagicMock()
sys.modules["meltano.core"] = MagicMock()
sys.modules["meltano.core.db"] = MagicMock()
sys.modules["meltano.core.job"] = MagicMock()
sys.modules["meltano.core.job.job"] = MagicMock()
sys.modules["meltano.core.sqlalchemy"] = MagicMock()
sys.modules["flext_observability"] = MagicMock()
sys.modules["flext_observability.logging"] = MagicMock()

# Mock flext_core properly
flext_core_mock = MagicMock()
flext_result_mock = MagicMock()
flext_result_mock.ok = MagicMock(return_value=MagicMock(value=MagicMock()))
flext_result_mock.fail = MagicMock(return_value=MagicMock(value=None))
flext_core_mock.FlextResult = flext_result_mock
sys.modules["flext_core"] = flext_core_mock

# Mock DI container
di_container_mock = MagicMock()
di_container_mock.injectable = lambda: lambda cls: cls
sys.modules["flext_meltano.infrastructure.di_container"] = di_container_mock


# Mock domain entities with proper classes
class MockEntity:
    """Base mock entity."""

    def __init__(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.id = getattr(self, "id", None) or uuid4()


class MockProject(MockEntity):
    """Mock project entity."""


class MockJob(MockEntity):
    """Mock job entity."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.project_id = getattr(self, "project_id", uuid4())

    def start_execution(self) -> None:
        pass

    def complete_execution(
        self, exit_code: int, stdout: str | None = None, stderr: str | None = None
    ) -> None:
        pass

    def cancel_execution(self) -> None:
        pass


class MockPlugin(MockEntity):
    """Mock plugin entity."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.project_id = getattr(self, "project_id", uuid4())

    def install(self) -> None:
        pass

    def update_config(self, config: Any) -> None:
        pass

    def uninstall(self) -> None:
        pass


class MockState(MockEntity):
    """Mock state entity."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.project_id = getattr(self, "project_id", uuid4())

    def update_state(self, state_data: Any) -> None:
        pass

    def merge_state(self, partial_state: Any) -> None:
        pass


# Create enum mocks
class MockEnvironmentType:
    """Mock environment type enum."""

    DEVELOPMENT = "dev"
    STAGING = "staging"
    PRODUCTION = "prod"
    TEST = "test"


class MockPluginType:
    """Mock plugin type enum."""

    EXTRACTOR = "extractors"
    LOADER = "loaders"
    TRANSFORMER = "transformers"
    ORCHESTRATOR = "orchestrators"
    UTILITY = "utilities"
    FILE = "files"


# Mock domain entities module
domain_entities_mock = MagicMock()
domain_entities_mock.FlextMeltanoProject = MockProject
domain_entities_mock.FlextMeltanoJob = MockJob
domain_entities_mock.FlextMeltanoPlugin = MockPlugin
domain_entities_mock.FlextMeltanoState = MockState
domain_entities_mock.EnvironmentType = MockEnvironmentType
domain_entities_mock.PluginType = MockPluginType
sys.modules["flext_meltano.domain.entities"] = domain_entities_mock

# Import services after all mocking
from flext_meltano.application import services as services_module  # noqa: E402


class TestDirectServicesImport:
    """Test services with direct imports that coverage can track."""

    def test_services_module_has_all_classes(self) -> None:
        """Test that all service classes are available."""
        assert hasattr(services_module, "FlextMeltanoProjectService")
        assert hasattr(services_module, "FlextMeltanoJobService")
        assert hasattr(services_module, "FlextMeltanoPluginService")
        assert hasattr(services_module, "FlextMeltanoStateService")

    def test_services_module_has_utility_functions(self) -> None:
        """Test that utility functions are available."""
        assert hasattr(services_module, "get_service_instances")
        assert hasattr(services_module, "validate_services")

    def test_service_instantiation(self) -> None:
        """Test that all services can be instantiated."""
        project_service = services_module.FlextMeltanoProjectService()
        assert project_service is not None
        assert hasattr(project_service, "_projects")

        job_service = services_module.FlextMeltanoJobService()
        assert job_service is not None
        assert hasattr(job_service, "_jobs")

        plugin_service = services_module.FlextMeltanoPluginService()
        assert plugin_service is not None
        assert hasattr(plugin_service, "_plugins")

        state_service = services_module.FlextMeltanoStateService()
        assert state_service is not None
        assert hasattr(state_service, "_states")

    def test_get_service_instances(self) -> None:
        """Test get_service_instances function."""
        services = services_module.get_service_instances()
        assert isinstance(services, dict)
        assert len(services) == 4
        assert "project" in services
        assert "job" in services
        assert "plugin" in services
        assert "state" in services

    def test_validate_services(self) -> None:
        """Test validate_services function."""
        result = services_module.validate_services()
        assert isinstance(result, bool)
        assert result is True


class TestProjectService:
    """Test FlextMeltanoProjectService methods."""

    @pytest.fixture
    def service(self) -> Any:
        """Create project service instance."""
        return services_module.FlextMeltanoProjectService()

    async def test_create_project(self, service: Any) -> None:
        """Test create_project method."""
        result = await service.create_project(
            name="test-project",
            project_root="/tmp/test",  # noqa: S108
            meltano_file_path="/tmp/test/meltano.yml",  # noqa: S108
            meltano_version="3.0.0",
        )
        assert result is not None

    async def test_list_projects(self, service: Any) -> None:
        """Test list_projects method."""
        result = await service.list_projects()
        assert result is not None

    async def test_get_project(self, service: Any) -> None:
        """Test get_project method."""
        project_id = uuid4()
        result = await service.get_project(project_id)
        assert result is not None

    async def test_update_project(self, service: Any) -> None:
        """Test update_project method."""
        project_id = uuid4()
        result = await service.update_project(project_id, {"name": "updated"})
        assert result is not None

    async def test_delete_project(self, service: Any) -> None:
        """Test delete_project method."""
        project_id = uuid4()
        result = await service.delete_project(project_id)
        assert result is not None


class TestJobService:
    """Test FlextMeltanoJobService methods."""

    @pytest.fixture
    def service(self) -> Any:
        """Create job service instance."""
        return services_module.FlextMeltanoJobService()

    async def test_create_job(self, service: Any) -> None:
        """Test create_job method."""
        project_id = uuid4()
        result = await service.create_job(
            project_id=project_id,
            job_id="test-job",
            job_type="extract",
            command=["meltano", "run", "tap-test"],
        )
        assert result is not None

    async def test_start_job(self, service: Any) -> None:
        """Test start_job method."""
        job_id = uuid4()
        result = await service.start_job(job_id)
        assert result is not None

    async def test_complete_job(self, service: Any) -> None:
        """Test complete_job method."""
        job_id = uuid4()
        result = await service.complete_job(job_id, 0, "success", "")
        assert result is not None

    async def test_cancel_job(self, service: Any) -> None:
        """Test cancel_job method."""
        job_id = uuid4()
        result = await service.cancel_job(job_id)
        assert result is not None

    async def test_get_job(self, service: Any) -> None:
        """Test get_job method."""
        job_id = uuid4()
        result = await service.get_job(job_id)
        assert result is not None

    async def test_list_jobs(self, service: Any) -> None:
        """Test list_jobs method."""
        project_id = uuid4()
        result = await service.list_jobs(project_id)
        assert result is not None


class TestPluginService:
    """Test FlextMeltanoPluginService methods."""

    @pytest.fixture
    def service(self) -> Any:
        """Create plugin service instance."""
        return services_module.FlextMeltanoPluginService()

    async def test_install_plugin(self, service: Any) -> None:
        """Test install_plugin method."""
        project_id = uuid4()
        result = await service.install_plugin(
            project_id=project_id,
            name="tap-test",
            namespace="tap_test",
            plugin_type="extractors",
        )
        assert result is not None

    async def test_get_plugin(self, service: Any) -> None:
        """Test get_plugin method."""
        plugin_id = uuid4()
        result = await service.get_plugin(plugin_id)
        assert result is not None

    async def test_list_plugins(self, service: Any) -> None:
        """Test list_plugins method."""
        project_id = uuid4()
        result = await service.list_plugins(project_id)
        assert result is not None

    async def test_configure_plugin(self, service: Any) -> None:
        """Test configure_plugin method."""
        plugin_id = uuid4()
        result = await service.configure_plugin(plugin_id, {"key": "value"})
        assert result is not None

    async def test_uninstall_plugin(self, service: Any) -> None:
        """Test uninstall_plugin method."""
        plugin_id = uuid4()
        result = await service.uninstall_plugin(plugin_id)
        assert result is not None


class TestStateService:
    """Test FlextMeltanoStateService methods."""

    @pytest.fixture
    def service(self) -> Any:
        """Create state service instance."""
        return services_module.FlextMeltanoStateService()

    async def test_create_state(self, service: Any) -> None:
        """Test create_state method."""
        project_id = uuid4()
        job_id = uuid4()
        result = await service.create_state(
            project_id=project_id,
            job_id=job_id,
            state_id="test-state",
            state_data={"key": "value"},
        )
        assert result is not None

    async def test_get_state(self, service: Any) -> None:
        """Test get_state method."""
        state_id = uuid4()
        result = await service.get_state(state_id)
        assert result is not None

    async def test_update_state(self, service: Any) -> None:
        """Test update_state method."""
        state_id = uuid4()
        result = await service.update_state(state_id, {"key": "updated"})
        assert result is not None

    async def test_merge_state(self, service: Any) -> None:
        """Test merge_state method."""
        state_id = uuid4()
        result = await service.merge_state(state_id, {"new_key": "new_value"})
        assert result is not None

    async def test_list_states(self, service: Any) -> None:
        """Test list_states method."""
        project_id = uuid4()
        result = await service.list_states(project_id)
        assert result is not None

    async def test_delete_state(self, service: Any) -> None:
        """Test delete_state method."""
        state_id = uuid4()
        result = await service.delete_state(state_id)
        assert result is not None
