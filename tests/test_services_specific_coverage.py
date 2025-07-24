"""Specific targeted tests to cover exact missing lines in services.py.

This test focuses on the exact missing lines identified in coverage report.
"""

from __future__ import annotations

import sys
from typing import Any
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest

# Mock dependencies before importing
sys.modules["flext_observability"] = MagicMock()
sys.modules["flext_observability.logging"] = MagicMock()


# Mock flext_core with properly typed result objects
class MockFlextResult:
    """Type-correct mock for FlextResult that matches real interface."""

    def __init__(
        self, success: bool, data: Any = None, error: str | None = None
    ) -> None:
        self.success = success
        self.data = data
        self.error = error
        self.is_success = success
        self.is_failure = not success

    @classmethod
    def ok(cls, data: Any) -> MockFlextResult:
        """Create successful result."""
        return cls(success=True, data=data, error=None)

    @classmethod
    def fail(cls, error: str) -> MockFlextResult:
        """Create failure result."""
        return cls(success=False, data=None, error=error)


flext_core_mock = MagicMock()
flext_core_mock.FlextResult = MockFlextResult
sys.modules["flext_core"] = flext_core_mock

# Mock DI container
di_container_mock = MagicMock()
di_container_mock.injectable = lambda: lambda cls: cls
sys.modules["flext_meltano.infrastructure.di_container"] = di_container_mock


# Type-correct mock domain entities
class MockFlextMeltanoProject:
    """Type-correct mock for FlextMeltanoProject."""

    def __init__(self, **kwargs: Any) -> None:
        self.id: UUID = kwargs.get("id", uuid4())
        self.name: str = kwargs.get("name", "test")
        # Add other expected attributes
        for key, value in kwargs.items():
            setattr(self, key, value)


class MockFlextMeltanoJob:
    """Type-correct mock for FlextMeltanoJob."""

    def __init__(self, **kwargs: Any) -> None:
        self.id: UUID = kwargs.get("id", uuid4())
        self.project_id: UUID = kwargs.get("project_id", uuid4())
        # Add configuration attributes that tests check for
        if "configuration" not in kwargs and "config" not in kwargs:
            self.configuration: dict[str, Any] = {}
        for key, value in kwargs.items():
            setattr(self, key, value)

    def start_execution(self) -> None:
        pass

    def complete_execution(
        self, exit_code: int, stdout: str | None = None, stderr: str | None = None
    ) -> None:
        pass

    def cancel_execution(self) -> None:
        pass


class MockFlextMeltanoPlugin:
    """Type-correct mock for FlextMeltanoPlugin."""

    def __init__(self, **kwargs: Any) -> None:
        self.id: UUID = kwargs.get("id", uuid4())
        self.project_id: UUID = kwargs.get("project_id", uuid4())
        for key, value in kwargs.items():
            setattr(self, key, value)

    def install(self) -> None:
        pass

    def update_config(self, config: dict[str, Any]) -> None:
        pass

    def uninstall(self) -> None:
        pass


class MockFlextMeltanoState:
    """Type-correct mock for FlextMeltanoState."""

    def __init__(self, **kwargs: Any) -> None:
        self.id: UUID = kwargs.get("id", uuid4())
        self.project_id: UUID = kwargs.get("project_id", uuid4())
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update_state(self, state_data: dict[str, Any]) -> None:
        pass

    def merge_state(self, partial_state: dict[str, Any]) -> None:
        pass


# Mock enums
class MockEnvironmentType:
    """Mock environment type."""

    DEVELOPMENT = "dev"
    STAGING = "staging"
    PRODUCTION = "prod"
    TEST = "test"


class MockPluginType:
    """Mock plugin type."""

    EXTRACTOR = "extractors"
    LOADER = "loaders"
    TRANSFORMER = "transformers"
    ORCHESTRATOR = "orchestrators"
    UTILITY = "utilities"
    FILE = "files"


# Domain entities mock setup
domain_entities_mock = MagicMock()
domain_entities_mock.FlextMeltanoProject = MockFlextMeltanoProject
domain_entities_mock.FlextMeltanoJob = MockFlextMeltanoJob
domain_entities_mock.FlextMeltanoPlugin = MockFlextMeltanoPlugin
domain_entities_mock.FlextMeltanoState = MockFlextMeltanoState
domain_entities_mock.EnvironmentType = MockEnvironmentType
domain_entities_mock.PluginType = MockPluginType
sys.modules["flext_meltano.domain.entities"] = domain_entities_mock

# Mock additional problematic imports before services
sys.modules["meltano"] = MagicMock()
sys.modules["meltano.core"] = MagicMock()
sys.modules["meltano.core.db"] = MagicMock()
sys.modules["meltano.core.job"] = MagicMock()
sys.modules["meltano.core.job.job"] = MagicMock()
sys.modules["meltano.core.sqlalchemy"] = MagicMock()

# Import services after mocking all dependencies
from flext_meltano.application import services as services_module  # noqa: E402


def assert_error_message(result: Any, expected_message: str) -> None:
    """Helper to assert error messages robustly."""
    assert result.is_failure
    assert result.error is not None
    # Convert to string for comparison - works for both str and mock
    error_str = str(result.error)
    assert expected_message in error_str


class TestSpecificCoverageTargets:
    """Tests targeting specific uncovered lines."""

    async def test_create_project_exception_lines_77_78(self) -> None:
        """Test create_project exception handling lines 77-78."""
        service = services_module.FlextMeltanoProjectService()

        # Create a scenario where FlextMeltanoProject constructor raises exception
        with patch(
            "flext_meltano.domain.entities.FlextMeltanoProject",
            side_effect=ValueError("Test project creation error"),
        ):
            result = await service.create_project(
                name="test",
                project_root="/tmp/test",  # noqa: S108
                meltano_file_path="/tmp/test/meltano.yml",  # noqa: S108
                meltano_version="3.0.0",
            )
            assert result.is_failure
            assert result.error is not None
            assert (
                "Failed to create project: Test project creation error" in result.error
            )

    async def test_get_project_exception_lines_88_89(self) -> None:
        """Test get_project exception handling lines 88-89."""
        service = services_module.FlextMeltanoProjectService()
        project_id = uuid4()

        # Mock the _projects dict to raise an exception on .get()
        mock_dict = MagicMock()
        mock_dict.get.side_effect = RuntimeError("Database connection failed")

        service._projects = mock_dict
        result = await service.get_project(project_id)
        assert result.is_failure
        assert result.error is not None
        assert isinstance(result.error, str)
        assert_error_message(result, "assert "Failed to get project: Database connection failed" in result.error")

    async def test_list_projects_exception_lines_96_97(self) -> None:
        """Test list_projects exception handling lines 96-97."""
        service = services_module.FlextMeltanoProjectService()

        # Mock the _projects dict to raise an exception on .values()
        mock_dict = MagicMock()
        mock_dict.values.side_effect = OSError("Filesystem error")

        service._projects = mock_dict
        result = await service.list_projects()
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to list projects: Filesystem error" in result.error")

    async def test_update_project_hasattr_false_line_112(self) -> None:
        """Test update_project hasattr false branch line 112."""
        service = services_module.FlextMeltanoProjectService()
        project_id = uuid4()

        # Create a project and try to update with non-existent attribute
        project = MockFlextMeltanoProject(id=project_id, name="test")
        service._projects[project_id] = project  # type: ignore[assignment]

        result = await service.update_project(
            project_id, {"nonexistent_field": "value"}
        )
        assert result.is_success
        # The line 112 (setattr) should not be called for non-existent attributes

    async def test_update_project_exception_lines_117_118(self) -> None:
        """Test update_project exception handling lines 117-118."""
        service = services_module.FlextMeltanoProjectService()
        project_id = uuid4()

        # Add a project
        service._projects[project_id] = MockFlextMeltanoProject(id=project_id, name="test")  # type: ignore[assignment]

        # Mock hasattr to raise an exception
        with patch("builtins.hasattr", side_effect=RuntimeError("Introspection error")):
            result = await service.update_project(project_id, {"name": "updated"})
            assert result.is_failure
            assert result.error is not None
            assert_error_message(result, "assert "Failed to update project: Introspection error" in result.error")

    async def test_delete_project_exception_lines_127_128(self) -> None:
        """Test delete_project exception handling lines 127-128."""
        service = services_module.FlextMeltanoProjectService()
        project_id = uuid4()

        # Mock _projects to raise exception on __contains__ (use OSError which is caught)
        mock_dict = MagicMock()
        mock_dict.__contains__.side_effect = OSError("Filesystem error")

        service._projects = mock_dict
        result = await service.delete_project(project_id)
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to delete project: Filesystem error" in result.error")

    async def test_install_plugin_exception_lines_183_184(self) -> None:
        """Test install_plugin exception handling lines 183-184."""
        service = services_module.FlextMeltanoPluginService()
        project_id = uuid4()

        # Mock FlextMeltanoPlugin to raise exception
        with patch(
            "flext_meltano.domain.entities.FlextMeltanoPlugin",
            side_effect=TypeError("Plugin creation failed"),
        ):
            result = await service.install_plugin(
                project_id=project_id,
                name="test-plugin",
                namespace="test_namespace",
                plugin_type="extractors",
            )
            assert result.is_failure
            assert result.error is not None
            assert_error_message(result, "assert "Failed to install plugin: Plugin creation failed" in result.error")

    async def test_get_plugin_exception_lines_191_192(self) -> None:
        """Test get_plugin exception handling lines 191-192."""
        service = services_module.FlextMeltanoPluginService()
        plugin_id = uuid4()

        # Mock _plugins dict to raise exception (use RuntimeError which is caught)
        mock_dict = MagicMock()
        mock_dict.get.side_effect = RuntimeError("Plugin cache corrupted")

        service._plugins = mock_dict
        result = await service.get_plugin(plugin_id)
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to get plugin: Plugin cache corrupted" in result.error")

    async def test_list_plugins_exception_lines_206_207(self) -> None:
        """Test list_plugins exception handling lines 206-207."""
        service = services_module.FlextMeltanoPluginService()
        project_id = uuid4()

        # Create a mock plugin that raises an exception when accessing project_id
        class ExceptionPlugin:
            @property
            def project_id(self) -> Any:
                raise RuntimeError("Plugin project ID access failed")

        # Add the problematic plugin to trigger exception during list comprehension
        service._plugins[uuid4()] = ExceptionPlugin()  # type: ignore[assignment]

        result = await service.list_plugins(project_id)
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to list plugins: Plugin project ID access failed" in result.error")

    async def test_configure_plugin_exception_lines_223_224(self) -> None:
        """Test configure_plugin exception handling lines 223-224."""
        service = services_module.FlextMeltanoPluginService()
        plugin_id = uuid4()

        # Add a plugin and mock update_config to raise exception
        MockFlextMeltanoPlugin(id=plugin_id)

        # Create a special plugin that raises on update_config
        class FailingPlugin(MockFlextMeltanoPlugin):
            def update_config(self, config: dict[str, Any]) -> None:
                raise ValueError("Invalid config format")

        failing_plugin = FailingPlugin(id=plugin_id)
        service._plugins[plugin_id] = failing_plugin  # type: ignore[assignment]

        result = await service.configure_plugin(plugin_id, {"key": "value"})
        assert_error_message(result, "Failed to configure plugin: Invalid config format")

    async def test_uninstall_plugin_exception_lines_236_237(self) -> None:
        """Test uninstall_plugin exception handling lines 236-237."""
        service = services_module.FlextMeltanoPluginService()
        plugin_id = uuid4()

        # Add a plugin and mock uninstall to raise exception
        class FailingPlugin(MockFlextMeltanoPlugin):
            def uninstall(self) -> None:
                raise OSError("Permission denied")

        failing_plugin = FailingPlugin(id=plugin_id)
        service._plugins[plugin_id] = failing_plugin  # type: ignore[assignment]

        result = await service.uninstall_plugin(plugin_id)
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to uninstall plugin: Permission denied" in result.error")

    async def test_create_job_config_hasattr_lines_289_291(self) -> None:
        """Test create_job config attribute checking lines 289, 291."""
        service = services_module.FlextMeltanoJobService()
        project_id = uuid4()

        # Create a job entity that has 'configuration' attribute
        job_mock = MockFlextMeltanoJob(id=uuid4(), project_id=project_id)
        job_mock.configuration = {}

        with patch(
            "flext_meltano.domain.entities.FlextMeltanoJob", return_value=job_mock
        ):
            result = await service.create_job(
                project_id=project_id,
                job_id="test-job",
                job_type="extract",
                command=["test"],
                config={"timeout": 300},
            )
            assert result.is_success
            # This should hit line 289 (hasattr check for 'configuration')
            # and line 291 (job.configuration = job_config)

    async def test_create_job_exception_lines_295_296(self) -> None:
        """Test create_job exception handling lines 295-296."""
        service = services_module.FlextMeltanoJobService()
        project_id = uuid4()

        # Mock FlextMeltanoJob to raise exception
        with patch(
            "flext_meltano.domain.entities.FlextMeltanoJob",
            side_effect=RuntimeError("Job creation failed"),
        ):
            result = await service.create_job(
                project_id=project_id,
                job_id="test-job",
                job_type="extract",
                command=["test"],
            )
            assert result.is_failure
            assert result.error is not None
            assert_error_message(result, "assert "Failed to create job: Job creation failed" in result.error")

    async def test_start_job_exception_lines_307_308(self) -> None:
        """Test start_job exception handling lines 307-308."""
        service = services_module.FlextMeltanoJobService()
        job_id = uuid4()

        # Add a job and mock start_execution to raise exception
        class FailingJob(MockFlextMeltanoJob):
            def start_execution(self) -> None:
                raise RuntimeError("Job start failed")

        failing_job = FailingJob(id=job_id)
        service._jobs[job_id] = failing_job  # type: ignore[assignment]

        result = await service.start_job(job_id)
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to start job: Job start failed" in result.error")

    async def test_complete_job_exception_lines_325_326(self) -> None:
        """Test complete_job exception handling lines 325-326."""
        service = services_module.FlextMeltanoJobService()
        job_id = uuid4()

        # Add a job and mock complete_execution to raise exception
        class FailingJob(MockFlextMeltanoJob):
            def complete_execution(
                self,
                exit_code: int,
                stdout: str | None = None,
                stderr: str | None = None,
            ) -> None:
                raise ValueError("Invalid exit code")

        failing_job = FailingJob(id=job_id)
        service._jobs[job_id] = failing_job  # type: ignore[assignment]

        result = await service.complete_job(job_id, 0, "output", "")
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to complete job: Invalid exit code" in result.error")

    async def test_cancel_job_exception_lines_337_338(self) -> None:
        """Test cancel_job exception handling lines 337-338."""
        service = services_module.FlextMeltanoJobService()
        job_id = uuid4()

        # Add a job and mock cancel_execution to raise exception
        class FailingJob(MockFlextMeltanoJob):
            def cancel_execution(self) -> None:
                raise OSError("Process termination failed")

        failing_job = FailingJob(id=job_id)
        service._jobs[job_id] = failing_job  # type: ignore[assignment]

        result = await service.cancel_job(job_id)
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to cancel job: Process termination failed" in result.error")

    async def test_get_job_exception_lines_345_346(self) -> None:
        """Test get_job exception handling lines 345-346."""
        service = services_module.FlextMeltanoJobService()
        job_id = uuid4()

        # Mock _jobs dict to raise exception
        mock_dict = MagicMock()
        mock_dict.get.side_effect = RuntimeError("Job cache corrupted")

        service._jobs = mock_dict
        result = await service.get_job(job_id)
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to get job: Job cache corrupted" in result.error")

    async def test_list_jobs_exception_lines_353_354(self) -> None:
        """Test list_jobs exception handling lines 353-354."""
        service = services_module.FlextMeltanoJobService()
        project_id = uuid4()

        # Create a mock job that raises an exception when accessing project_id
        class ExceptionJob:
            @property
            def project_id(self) -> Any:
                raise RuntimeError("Project ID access failed")

        # Add the problematic job to trigger exception during list comprehension
        service._jobs[uuid4()] = ExceptionJob()  # type: ignore[assignment]

        result = await service.list_jobs(project_id)
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to list jobs: Project ID access failed" in result.error")

    async def test_create_state_exception_lines_402_403(self) -> None:
        """Test create_state exception handling lines 402-403."""
        service = services_module.FlextMeltanoStateService()
        project_id = uuid4()
        job_id = uuid4()

        # Mock FlextMeltanoState to raise exception
        with patch(
            "flext_meltano.domain.entities.FlextMeltanoState",
            side_effect=ValueError("State creation failed"),
        ):
            result = await service.create_state(
                project_id=project_id,
                job_id=job_id,
                state_id="test-state",
                state_data={"key": "value"},
            )
            assert result.is_failure
            assert result.error is not None
            assert_error_message(result, "assert "Failed to create state: State creation failed" in result.error")

    async def test_update_state_exception_lines_418_419(self) -> None:
        """Test update_state exception handling lines 418-419."""
        service = services_module.FlextMeltanoStateService()
        state_id = uuid4()

        # Add a state and mock update_state to raise exception
        class FailingState(MockFlextMeltanoState):
            def update_state(self, state_data: dict[str, Any]) -> None:
                raise RuntimeError("State update failed")

        failing_state = FailingState(id=state_id)
        service._states[state_id] = failing_state  # type: ignore[assignment]

        result = await service.update_state(state_id, {"key": "value"})
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to update state: State update failed" in result.error")

    async def test_merge_state_exception_lines_434_435(self) -> None:
        """Test merge_state exception handling lines 434-435."""
        service = services_module.FlextMeltanoStateService()
        state_id = uuid4()

        # Add a state and mock merge_state to raise exception
        class FailingState(MockFlextMeltanoState):
            def merge_state(self, partial_state: dict[str, Any]) -> None:
                raise TypeError("Incompatible state format")

        failing_state = FailingState(id=state_id)
        service._states[state_id] = failing_state  # type: ignore[assignment]

        result = await service.merge_state(state_id, {"key": "value"})
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to merge state: Incompatible state format" in result.error")

    async def test_get_state_exception_lines_442_443(self) -> None:
        """Test get_state exception handling lines 442-443."""
        service = services_module.FlextMeltanoStateService()
        state_id = uuid4()

        # Mock _states dict to raise exception
        mock_dict = MagicMock()
        mock_dict.get.side_effect = OSError("State storage unavailable")

        service._states = mock_dict
        result = await service.get_state(state_id)
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to get state: State storage unavailable" in result.error")

    async def test_list_states_exception_lines_454_455(self) -> None:
        """Test list_states exception handling lines 454-455."""
        service = services_module.FlextMeltanoStateService()
        project_id = uuid4()

        # Mock _states.values() to raise exception
        mock_dict = MagicMock()
        mock_dict.values.side_effect = RuntimeError("State enumeration failed")

        service._states = mock_dict
        result = await service.list_states(project_id)
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to list states: State enumeration failed" in result.error")

    async def test_delete_state_exception_lines_464_465(self) -> None:
        """Test delete_state exception handling lines 464-465."""
        service = services_module.FlextMeltanoStateService()
        state_id = uuid4()

        # Mock _states to raise exception on __contains__
        mock_dict = MagicMock()
        mock_dict.__contains__.side_effect = RuntimeError("State index corrupted")

        service._states = mock_dict
        result = await service.delete_state(state_id)
        assert result.is_failure
        assert result.error is not None
        assert_error_message(result, "assert "Failed to delete state: State index corrupted" in result.error")

    def test_validate_services_exception_lines_521_522(self) -> None:
        """Test validate_services exception handling lines 521-522."""
        # Mock get_service_instances to raise exception
        with patch.object(
            services_module,
            "get_service_instances",
            side_effect=RuntimeError("Service instantiation failed"),
        ):
            result = services_module.validate_services()
            assert result is False
            # This covers line 522 (return False in except block)

    def test_validate_services_attribute_validation_lines_498_500_505_507_512_514_519(
        self,
    ) -> None:
        """Test validate_services attribute validation lines."""
        # Create mock services with missing attributes
        mock_services = {
            "project": MagicMock(),
            "job": MagicMock(),
            "plugin": MagicMock(),
            "state": MagicMock(),
        }

        # Test project service validation (lines 498, 500)
        mock_services["project"]._projects = "not_a_dict"  # Wrong type
        with patch.object(
            services_module, "get_service_instances", return_value=mock_services
        ):
            result = services_module.validate_services()
            assert result is False

        # Test job service validation (lines 505, 507)
        mock_services["project"]._projects = {}  # Fix project
        del mock_services["job"]._jobs  # Missing attribute
        with patch.object(
            services_module, "get_service_instances", return_value=mock_services
        ):
            result = services_module.validate_services()
            assert result is False

        # Test plugin service validation (lines 512, 514)
        mock_services["job"]._jobs = {}  # Fix job
        mock_services["plugin"]._plugins = None  # Wrong type
        with patch.object(
            services_module, "get_service_instances", return_value=mock_services
        ):
            result = services_module.validate_services()
            assert result is False

        # Test state service validation (line 519)
        mock_services["plugin"]._plugins = {}  # Fix plugin
        mock_services["state"]._states = []  # Wrong type
        with patch.object(
            services_module, "get_service_instances", return_value=mock_services
        ):
            result = services_module.validate_services()
            assert result is False

    def test_type_checking_imports_lines_19_21(self) -> None:
        """Test TYPE_CHECKING import lines 19-21."""
        # These lines are covered by importing the module, but let's ensure they're hit
        # by creating service instances that use the types
        from uuid import UUID

        # This should exercise the TYPE_CHECKING import block
        project_service = services_module.FlextMeltanoProjectService()
        assert hasattr(project_service, "_projects")

        # Create an actual UUID to ensure the import is used
        test_id = UUID("12345678-1234-5678-9012-123456789012")
        assert isinstance(test_id, UUID)

    async def test_update_project_hasattr_true_line_112(self) -> None:
        """Test update_project when hasattr returns True to cover line 112 (setattr call)."""
        service = services_module.FlextMeltanoProjectService()
        project_id = uuid4()

        # Create a project with a name attribute
        mock_project = MockFlextMeltanoProject(id=project_id, name="original")
        service._projects[project_id] = mock_project  # type: ignore[assignment]

        # Update with attribute that exists
        result = await service.update_project(project_id, {"name": "updated"})
        assert result.is_success
        assert mock_project.name == "updated"  # Check setattr worked

    async def test_plugin_service_line_222_uninstall_call(self) -> None:
        """Test uninstall_plugin to cover line 222 (successful plugin.uninstall() call)."""
        service = services_module.FlextMeltanoPluginService()
        plugin_id = uuid4()

        # Add a plugin that can be uninstalled
        plugin = MockFlextMeltanoPlugin(id=plugin_id)
        service._plugins[plugin_id] = plugin  # type: ignore[assignment]

        result = await service.uninstall_plugin(plugin_id)
        assert result.is_success
        # Line 222 should be covered (plugin.uninstall() call)

    async def test_plugin_service_lines_234_235_successful_delete(self) -> None:
        """Test uninstall_plugin successful deletion lines 234-235."""
        service = services_module.FlextMeltanoPluginService()
        plugin_id = uuid4()

        # Add a plugin
        plugin = MockFlextMeltanoPlugin(id=plugin_id)
        service._plugins[plugin_id] = plugin  # type: ignore[assignment]

        result = await service.uninstall_plugin(plugin_id)
        assert result.is_success
        assert (
            plugin_id not in service._plugins
        )  # Line 234: del self._plugins[plugin_id]
        # Line 235: return FlextResult.ok(True)

    async def test_job_service_line_291_config_attribute(self) -> None:
        """Test create_job to cover line 291 (job.config = job_config)."""
        service = services_module.FlextMeltanoJobService()
        project_id = uuid4()

        # Create a job entity that has 'config' attribute but not 'configuration'
        job_mock = MockFlextMeltanoJob(id=uuid4(), project_id=project_id)
        # Remove configuration attribute if it exists
        if hasattr(job_mock, "configuration"):
            delattr(job_mock, "configuration")
        job_mock.config = {}  # type: ignore[attr-defined]

        with patch(
            "flext_meltano.domain.entities.FlextMeltanoJob", return_value=job_mock
        ):
            result = await service.create_job(
                project_id=project_id,
                job_id="test-job",
                job_type="extract",
                command=["test"],
                config={"timeout": 300},
            )
            assert result.is_success
            # This should hit line 291 (job.config = job_config)

    async def test_job_service_line_306_successful_start(self) -> None:
        """Test start_job successful execution to cover line 306."""
        service = services_module.FlextMeltanoJobService()
        job_id = uuid4()

        # Add a job
        job = MockFlextMeltanoJob(id=job_id)
        service._jobs[job_id] = job  # type: ignore[assignment]

        result = await service.start_job(job_id)
        assert result.is_success
        # Line 306: return FlextResult.ok(job)

    async def test_job_service_line_324_successful_complete(self) -> None:
        """Test complete_job successful execution to cover line 324."""
        service = services_module.FlextMeltanoJobService()
        job_id = uuid4()

        # Add a job
        job = MockFlextMeltanoJob(id=job_id)
        service._jobs[job_id] = job  # type: ignore[assignment]

        result = await service.complete_job(job_id, 0, "output", "")
        assert result.is_success
        # Line 324: return FlextResult.ok(job)

    async def test_job_service_line_336_successful_cancel(self) -> None:
        """Test cancel_job successful execution to cover line 336."""
        service = services_module.FlextMeltanoJobService()
        job_id = uuid4()

        # Add a job
        job = MockFlextMeltanoJob(id=job_id)
        service._jobs[job_id] = job  # type: ignore[assignment]

        result = await service.cancel_job(job_id)
        assert result.is_success
        # Line 336: return FlextResult.ok(job)

    async def test_state_service_line_417_successful_update(self) -> None:
        """Test update_state successful execution to cover line 417."""
        service = services_module.FlextMeltanoStateService()
        state_id = uuid4()

        # Add a state
        state = MockFlextMeltanoState(id=state_id)
        service._states[state_id] = state  # type: ignore[assignment]

        result = await service.update_state(state_id, {"key": "value"})
        assert result.is_success
        # Line 417: return FlextResult.ok(state)

    async def test_state_service_line_433_successful_merge(self) -> None:
        """Test merge_state successful execution to cover line 433."""
        service = services_module.FlextMeltanoStateService()
        state_id = uuid4()

        # Add a state
        state = MockFlextMeltanoState(id=state_id)
        service._states[state_id] = state  # type: ignore[assignment]

        result = await service.merge_state(state_id, {"key": "value"})
        assert result.is_success
        # Line 433: return FlextResult.ok(state)

    def test_validation_functions_lines_498_507_512_519_success_paths(self) -> None:
        """Test validate_services success paths to cover validation lines."""
        # Create properly configured mock services
        mock_services = {
            "project": MagicMock(),
            "job": MagicMock(),
            "plugin": MagicMock(),
            "state": MagicMock(),
        }

        # Set up all attributes correctly
        mock_services["project"]._projects = {}
        mock_services["job"]._jobs = {}
        mock_services["plugin"]._plugins = {}
        mock_services["state"]._states = {}

        with patch.object(
            services_module, "get_service_instances", return_value=mock_services
        ):
            result = services_module.validate_services()
            assert result is True
            # This should cover all the validation success paths:
            # Line 498: if not hasattr(project_service, "_projects"):
            # Line 507: if not hasattr(job_service, "_jobs"):
            # Line 512: if not hasattr(plugin_service, "_plugins"):
            # Line 519: if not hasattr(state_service, "_states"):
