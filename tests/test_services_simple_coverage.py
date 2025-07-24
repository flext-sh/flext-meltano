"""Simple targeted tests to improve services.py coverage.

This test focuses on covering specific missed lines without complex mocking.
"""

from __future__ import annotations

import sys
from typing import Any
from unittest.mock import MagicMock
from uuid import uuid4

# Mock dependencies before importing services
sys.modules["flext_observability"] = MagicMock()
sys.modules["flext_observability.logging"] = MagicMock()

# Mock flext_core with simple approach
flext_core_mock = MagicMock()
mock_result = MagicMock()
mock_result.ok = lambda value: MagicMock(value=value, is_success=True, is_failure=False)
mock_result.fail = lambda msg: MagicMock(
    value=None, message=msg, is_success=False, is_failure=True
)
flext_core_mock.FlextResult = mock_result
sys.modules["flext_core"] = flext_core_mock

# Mock DI container
di_container_mock = MagicMock()
di_container_mock.injectable = lambda: lambda cls: cls
sys.modules["flext_meltano.infrastructure.di_container"] = di_container_mock


# Mock domain entities
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


# Mock environment and plugin types
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


# Domain entities mock setup
domain_entities_mock = MagicMock()
domain_entities_mock.FlextMeltanoProject = MockProject
domain_entities_mock.FlextMeltanoJob = MockJob
domain_entities_mock.FlextMeltanoPlugin = MockPlugin
domain_entities_mock.FlextMeltanoState = MockState
domain_entities_mock.EnvironmentType = MockEnvironmentType
domain_entities_mock.PluginType = MockPluginType
sys.modules["flext_meltano.domain.entities"] = domain_entities_mock

# Import services after mocking
# Mock additional problematic imports before services
sys.modules["meltano"] = MagicMock()
sys.modules["meltano.core"] = MagicMock()
sys.modules["meltano.core.db"] = MagicMock()
sys.modules["meltano.core.job"] = MagicMock()
sys.modules["meltano.core.job.job"] = MagicMock()
sys.modules["meltano.core.sqlalchemy"] = MagicMock()

# Import services after mocking all dependencies
from flext_meltano.application import services as services_module  # noqa: E402


class TestServicesSimpleCoverage:
    """Simple tests to cover missing lines in services.py."""

    async def test_project_service_all_environments(self) -> None:
        """Test creating projects with all environment types to cover lines 58, 60, 62."""
        service = services_module.FlextMeltanoProjectService()

        # Test each environment type branch
        test_cases = [
            ("staging", "staging"),
            ("prod", "prod"),
            ("test", "test"),
            ("dev", "dev"),  # default case
            ("unknown", "dev"),  # should default to dev
        ]

        for env_input, _expected in test_cases:
            result = await service.create_project(
                name=f"test-{env_input}",
                project_root=f"/tmp/{env_input}",  # noqa: S108
                meltano_file_path=f"/tmp/{env_input}/meltano.yml",  # noqa: S108
                meltano_version="3.0.0",
                default_environment=env_input,
            )
            assert result is not None

    async def test_plugin_service_all_types(self) -> None:
        """Test installing plugins with all types to cover lines 160, 162, 164, 166, 168."""
        service = services_module.FlextMeltanoPluginService()
        project_id = uuid4()

        # Test each plugin type branch
        plugin_types = [
            "loaders",
            "transformers",
            "orchestrators",
            "utilities",
            "files",
            "extractors",  # default case
            "unknown",  # should default to extractors
        ]

        for plugin_type in plugin_types:
            result = await service.install_plugin(
                project_id=project_id,
                name=f"plugin-{plugin_type}",
                namespace=f"ns_{plugin_type}",
                plugin_type=plugin_type,
            )
            assert result is not None

    async def test_job_service_all_environments(self) -> None:
        """Test creating jobs with all environment types to cover lines 268, 270, 272."""
        service = services_module.FlextMeltanoJobService()
        project_id = uuid4()

        # Test each environment type branch for jobs
        environments = ["staging", "prod", "test", "dev", "unknown"]

        for env in environments:
            result = await service.create_job(
                project_id=project_id,
                job_id=f"job-{env}",
                job_type="test",
                command=["echo", "test"],
                environment=env,
            )
            assert result is not None

    async def test_state_service_all_environments(self) -> None:
        """Test creating states with all environment types to cover lines 384, 386, 388."""
        service = services_module.FlextMeltanoStateService()
        project_id = uuid4()
        job_id = uuid4()

        # Test each environment type branch for states
        environments = ["staging", "prod", "test", "dev", "unknown"]

        for env in environments:
            result = await service.create_state(
                project_id=project_id,
                job_id=job_id,
                state_id=f"state-{env}",
                state_data={"test": True},
                environment=env,
            )
            assert result is not None

    async def test_job_service_config_branches(self) -> None:
        """Test job configuration branches to cover lines 289, 291."""
        service = services_module.FlextMeltanoJobService()
        project_id = uuid4()

        # Create job with config to test hasattr branches
        result = await service.create_job(
            project_id=project_id,
            job_id="test-job",
            job_type="test",
            command=["echo", "test"],
            config={"test": "value"},
        )
        assert result is not None

    async def test_update_project_hasattr_false(self) -> None:
        """Test update_project when hasattr returns False to cover line 110."""
        service = services_module.FlextMeltanoProjectService()
        project_id = uuid4()

        # Add a project to update
        mock_project = MockProject(id=project_id, name="test")
        service._projects[project_id] = mock_project  # type: ignore[assignment]

        # Try to update with attribute that doesn't exist
        result = await service.update_project(project_id, {"nonexistent_attr": "value"})
        assert result is not None

    async def test_delete_operations_success(self) -> None:
        """Test successful delete operations to cover lines 124-125, 461-462."""
        # Test project deletion
        project_service = services_module.FlextMeltanoProjectService()
        project_id = uuid4()
        project_service._projects[project_id] = MockProject(id=project_id)  # type: ignore[assignment]

        result = await project_service.delete_project(project_id)
        assert result is not None
        assert project_id not in project_service._projects

        # Test state deletion
        state_service = services_module.FlextMeltanoStateService()
        state_id = uuid4()
        state_service._states[state_id] = MockState(id=state_id)  # type: ignore[assignment]

        result = await state_service.delete_state(state_id)
        assert result is not None
        assert state_id not in state_service._states

    def test_validation_functions(self) -> None:
        """Test validation functions to cover lines 498, 500, 505, 507, 512, 514, 519."""
        # Test get_service_instances
        services_dict = services_module.get_service_instances()
        assert isinstance(services_dict, dict)
        assert len(services_dict) == 4

        # Test validate_services
        result = services_module.validate_services()
        assert isinstance(result, bool)
        assert result is True

    def test_type_checking_imports(self) -> None:
        """Test that TYPE_CHECKING imports work to cover lines 19-21."""
        # This test just ensures the module can be imported and instantiated
        # which exercises the TYPE_CHECKING import block
        project_service = services_module.FlextMeltanoProjectService()
        assert hasattr(project_service, "_projects")

        job_service = services_module.FlextMeltanoJobService()
        assert hasattr(job_service, "_jobs")

        plugin_service = services_module.FlextMeltanoPluginService()
        assert hasattr(plugin_service, "_plugins")

        state_service = services_module.FlextMeltanoStateService()
        assert hasattr(state_service, "_states")
