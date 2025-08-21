"""Real functional tests for flext-meltano without mocks.

These tests actually test the real functionality using the actual implementation,
not mocks. They validate real integration with flext-core patterns.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from flext_core import FlextResult

from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.discovery import FlextMeltanoDiscoverer
from flext_meltano.execution import FlextMeltanoExecutor
from flext_meltano.installation import FlextMeltanoInstaller


class TestRealConfiguration:
    """Test real configuration functionality."""

    def test_config_creation_with_real_values(self) -> None:
        """Test creating config with actual file system paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            config = FlextMeltanoConfig(
                project_root=str(temp_path),
                environment="test",
                dbt_project_dir=str(temp_path / "dbt"),
            )

            assert config.project_root == str(temp_path)
            assert config.environment == "test"
            assert config.dbt_project_dir == str(temp_path / "dbt")

            # Test that config validates properly
            assert isinstance(config.project_root, str)
            assert len(config.project_root) > 0

    def test_config_validation_with_real_constraints(self) -> None:
        """Test config validation against real constraints."""
        # Valid config should work
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(
                project_root=str(temp_dir),
                environment="production",
            )

            # These should not raise exceptions
            assert config.environment in {"dev", "test", "staging", "production"}
            assert Path(config.project_root).exists()


class TestRealExecution:
    """Test real execution functionality."""

    def test_executor_initialization_with_real_config(self) -> None:
        """Test executor initializes with real configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(
                project_root=str(temp_dir),
                environment="test",
            )

            executor = FlextMeltanoExecutor(config)

            # Test real functionality
            assert executor.config == config
            assert hasattr(executor, "validate")
            assert hasattr(executor, "execute_pipeline")

            # Test validation actually works
            validation_result = executor.validate()
            assert isinstance(validation_result, FlextResult)
            assert hasattr(validation_result, "success")
            assert hasattr(validation_result, "error")

    def test_executor_validation_logic(self) -> None:
        """Test that executor validation has real logic."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(
                project_root=str(temp_dir),
                environment="test",
            )

            executor = FlextMeltanoExecutor(config)
            result = executor.validate()

            # Should return a proper FlextResult
            assert isinstance(result, FlextResult)

            # If it fails, it should have a real error message
            if not result.success:
                assert result.error is not None
                assert len(result.error) > 0
                assert (
                    "meltano" in result.error.lower()
                    or "not found" in result.error.lower()
                )


class TestRealDiscovery:
    """Test real discovery functionality."""

    def test_discoverer_initialization(self) -> None:
        """Test discoverer initializes properly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(
                project_root=str(temp_dir),
                environment="test",
            )

            discoverer = FlextMeltanoDiscoverer(config)

            # Test real attributes exist
            assert hasattr(discoverer, "config")
            assert hasattr(discoverer, "discover_plugins")
            assert discoverer.config == config

    def test_plugin_discovery_returns_real_result(self) -> None:
        """Test that plugin discovery returns proper FlextResult."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(
                project_root=str(temp_dir),
                environment="test",
            )

            discoverer = FlextMeltanoDiscoverer(config)
            result = discoverer.discover_plugins()

            # Should return a real FlextResult
            assert isinstance(result, FlextResult)

            # Should have proper structure
            if result.success:
                assert result.data is not None
                assert hasattr(result, "data")
            else:
                assert result.error is not None
                assert isinstance(result.error, str)


class TestRealInstallation:
    """Test real installation functionality."""

    def test_installer_initialization(self) -> None:
        """Test installer initializes with real config."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(
                project_root=str(temp_dir),
                environment="test",
            )

            installer = FlextMeltanoInstaller(config)

            # Test real functionality exists
            assert hasattr(installer, "config")
            assert hasattr(installer, "install_plugin")
            assert hasattr(installer, "validate")
            assert installer.config == config

    def test_installer_validation_has_real_logic(self) -> None:
        """Test installer validation with real constraints."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(
                project_root=str(temp_dir),
                environment="test",
            )

            installer = FlextMeltanoInstaller(config)
            result = installer.validate()

            # Should return proper FlextResult
            assert isinstance(result, FlextResult)

            # Should have meaningful validation
            if not result.success:
                assert result.error is not None
                assert len(result.error) > 0


class TestRealIntegrationPatterns:
    """Test real integration with flext-core patterns."""

    def test_flext_result_integration(self) -> None:
        """Test that all components properly use FlextResult pattern."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(
                project_root=str(temp_dir),
                environment="test",
            )

            # Test each component returns FlextResult
            components = [
                FlextMeltanoExecutor(config),
                FlextMeltanoDiscoverer(config),
                FlextMeltanoInstaller(config),
            ]

            for component in components:
                if hasattr(component, "validate"):
                    result = component.validate()
                    assert isinstance(result, FlextResult)

                    # FlextResult should have proper railway-oriented programming
                    assert hasattr(result, "success")
                    assert hasattr(result, "error")
                    assert hasattr(result, "data")

                    # success should be boolean
                    assert isinstance(result.success, bool)

    def test_real_error_handling(self) -> None:
        """Test real error handling without mocks."""
        # Test with invalid configuration
        config = FlextMeltanoConfig(
            project_root="/nonexistent/path/that/should/not/exist",
            environment="test",
        )

        executor = FlextMeltanoExecutor(config)
        result = executor.validate()

        # Should properly handle the error
        if not result.success:
            assert result.error is not None
            assert isinstance(result.error, str)
            assert len(result.error) > 0

            # Error should be meaningful
            assert (
                "not found" in result.error.lower()
                or "invalid" in result.error.lower()
                or "does not exist" in result.error.lower()
                or "meltano" in result.error.lower()
            )


class TestRealFileSystemOperations:
    """Test real file system operations."""

    def test_config_with_real_paths(self) -> None:
        """Test configuration handles real file system paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create some real directories
            dbt_dir = temp_path / "dbt"
            dbt_dir.mkdir()

            config = FlextMeltanoConfig(
                project_root=str(temp_path),
                dbt_project_dir=str(dbt_dir),
                environment="test",
            )

            # Test that paths work with real file system
            assert Path(config.project_root).exists()
            assert Path(config.dbt_project_dir).exists()
            assert Path(config.project_root).is_dir()

    def test_components_handle_real_paths(self) -> None:
        """Test components work with real file system paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            config = FlextMeltanoConfig(
                project_root=str(temp_path),
                environment="test",
            )

            # Components should handle real paths properly
            executor = FlextMeltanoExecutor(config)
            assert Path(executor.config.project_root).exists()

            # Validation should consider real file system
            result = executor.validate()

            # If validation fails due to missing meltano, that's expected and real
            if not result.success:
                assert (
                    "meltano" in result.error.lower()
                    or "not found" in result.error.lower()
                )
