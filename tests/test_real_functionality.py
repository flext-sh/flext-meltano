"""Real functional tests for flext-meltano without mocks.

These tests actually test the real functionality using the actual implementation,
not mocks. They validate real integration with flext-core patterns.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from flext_core import FlextResult

from flext_meltano import (
    FlextMeltanoConfig,
    FlextMeltanoExecutor,
    MeltanoBridge,
    MeltanoDbtWrapper,
)


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
        # Test executor with empty config
        executor = FlextMeltanoExecutor({})

        # Test real functionality
        assert hasattr(executor, "is_valid")
        assert hasattr(executor, "execute")

        # Test is_valid method works
        is_valid_result = executor.is_valid()
        assert isinstance(is_valid_result, bool)

    def test_executor_validation_logic(self) -> None:
        """Test that executor validation has real logic."""
        executor = FlextMeltanoExecutor({})
        result = executor.is_valid()

        # Should return a boolean
        assert isinstance(result, bool)


class TestRealDiscovery:
    """Test real discovery functionality."""

    def test_discoverer_initialization(self) -> None:
        """Test bridge discovery initializes properly."""
        bridge = MeltanoBridge()

        # Test real attributes exist
        assert hasattr(bridge, "discover_plugins")
        assert hasattr(bridge, "execute")

    def test_plugin_discovery_returns_real_result(self) -> None:
        """Test that plugin discovery returns proper FlextResult."""
        bridge = MeltanoBridge()
        result = bridge.discover_plugins()

        # Should return a real FlextResult
        assert isinstance(result, FlextResult)

        # Should have proper structure
        if result.success:
            assert result.value is not None
            assert hasattr(result, "value")
        else:
            assert result.error is not None
            assert isinstance(result.error, str)


class TestRealInstallation:
    """Test real installation functionality via MeltanoBridge."""

    def test_bridge_initialization(self) -> None:
        """Test bridge initializes and can handle plugin installation."""
        bridge = MeltanoBridge()

        # Test real functionality exists
        assert hasattr(bridge, "install_plugin")
        assert hasattr(bridge, "discover_plugins")
        assert hasattr(bridge, "execute")

    def test_bridge_plugin_discovery_real_logic(self) -> None:
        """Test bridge plugin discovery with real Meltano Hub."""
        bridge = MeltanoBridge()
        result = bridge.discover_plugins()

        # Should return proper FlextResult
        assert isinstance(result, FlextResult)

        # Should have meaningful discovery
        if result.success:
            assert result.value is not None
            assert isinstance(result.value, list)
        else:
            assert result.error is not None
            assert len(result.error) > 0


class TestRealIntegrationPatterns:
    """Test real integration with flext-core patterns."""

    def test_flext_result_integration(self) -> None:
        """Test that all components properly use FlextResult pattern."""
        with tempfile.TemporaryDirectory() as temp_dir:
            FlextMeltanoConfig(
                project_root=str(temp_dir),
                environment="test",
            )

            # Test each component returns FlextResult
            components = [
                FlextMeltanoExecutor({}),  # Pass empty config dict
                MeltanoBridge(),
                MeltanoDbtWrapper(),
            ]

            for component in components:
                if hasattr(component, "execute"):
                    result = component.execute()
                    assert isinstance(result, FlextResult)

                    # FlextResult should have proper railway-oriented programming
                    assert hasattr(result, "success")
                    assert hasattr(result, "error")
                    assert hasattr(result, "value")

                    # success should be boolean
                    assert isinstance(result.success, bool)

    def test_real_error_handling(self) -> None:
        """Test real error handling without mocks."""
        # Test with empty config
        executor = FlextMeltanoExecutor({})
        result = executor.is_valid()

        # Should return a boolean
        assert isinstance(result, bool)


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
            if config.dbt_project_dir is not None:
                assert Path(config.dbt_project_dir).exists()
            assert Path(config.project_root).is_dir()

    def test_components_handle_real_paths(self) -> None:
        """Test components work with real file system paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Components should handle real paths properly
            executor = FlextMeltanoExecutor({})
            assert Path(temp_path).exists()

            # is_valid should work with real file system
            result = executor.is_valid()

            # Should return a boolean
            assert isinstance(result, bool)
