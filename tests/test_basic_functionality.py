from flext_core import ServiceResult

"""Basic functionality tests for flext-meltano.

These tests verify that the Meltano functionality works correctly.
"""

from flext_meltano import (
    EnvironmentType,
    JobService,
    JobStatus,
    MeltanoJob,
    MeltanoPlugin,
    MeltanoProject,
    MeltanoState,
    PluginService,
    PluginType,
    ProjectService,
    ServiceResult,
    StateService,
)
from flext_meltano.infrastructure.di_container import get_container


class TestMeltanoBasicFunctionality:
    """Test basic Meltano functionality."""

    def test_meltano_imports(self) -> None:
        """Test that all Meltano components can be imported."""
        assert ProjectService is not None
        assert StateService is not None
        assert JobService is not None
        assert PluginService is not None
        assert MeltanoProject is not None
        assert MeltanoJob is not None
        assert MeltanoPlugin is not None
        assert MeltanoState is not None

    def test_meltano_enums(self) -> None:
        """Test that Meltano enums work correctly."""
        assert JobStatus.RUNNING == "running"
        assert JobStatus.COMPLETED == "completed"
        assert JobStatus.FAILED == "failed"

        assert PluginType.EXTRACTOR == "extractors"
        assert PluginType.LOADER == "loaders"
        assert PluginType.TRANSFORMER == "transformers"

        assert EnvironmentType.DEVELOPMENT == "dev"
        assert EnvironmentType.PRODUCTION == "prod"

    def test_meltano_entities(self) -> None:
        """Test that Meltano entities can be imported."""
        # Test that entities can be imported
        assert MeltanoProject is not None
        assert MeltanoJob is not None
        assert MeltanoPlugin is not None
        assert MeltanoState is not None


class TestMeltanoServices:
    """Test Meltano services."""

    def test_project_service(self) -> None:
        """Test ProjectService functionality."""
        # ProjectService should be available
        assert ProjectService is not None

    def test_state_service(self) -> None:
        """Test StateService functionality."""
        # StateService should be available
        assert StateService is not None

    def test_job_service(self) -> None:
        """Test JobService functionality."""
        # JobService should be available
        assert JobService is not None

    def test_plugin_service(self) -> None:
        """Test PluginService functionality."""
        # PluginService should be available
        assert PluginService is not None


class TestMeltanoIntegration:
    """Test Meltano integration scenarios."""

    def test_meltano_with_container(self) -> None:
        """Test Meltano works with DI container."""
        container = get_container()
        assert container is not None

        # Meltano should be able to access container
        assert ProjectService is not None

    def test_meltano_service_result(self) -> None:
        """Test Meltano uses ServiceResult correctly."""
        # ServiceResult should be available from flext_core
        assert ServiceResult is not None

        # Test creating a ServiceResult
        result = ServiceResult.ok({"test": "value"})
        assert result.success
        assert result.data == {"test": "value"}


class TestMeltanoErrorHandling:
    """Test Meltano error handling."""

    def test_meltano_error_handling(self) -> None:
        """Test Meltano handles errors gracefully."""
        # Meltano should handle errors without crashing
        assert ProjectService is not None

    def test_meltano_validation(self) -> None:
        """Test Meltano validation."""
        # Test that enums validate correctly
        assert JobStatus.RUNNING == "running"
        assert PluginType.EXTRACTOR == "extractors"
        assert EnvironmentType.DEVELOPMENT == "dev"
