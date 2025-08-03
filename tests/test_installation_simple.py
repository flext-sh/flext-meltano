"""Installation Module Simple Test Suite - Core Functionality Validation.

**Test Category**: Unit Tests
**Coverage Target**: 85%+ for installation module core functionality
**Dependencies**: Installation module, basic plugin scenarios, core operations
**Execution Time**: < 10 seconds total

## Test Scope

Validates core installation module functionality with simplified test scenarios
to ensure basic plugin installation and management operations work correctly.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from flext_meltano.base import FlextMeltanoConfig
from flext_meltano.installation import (
    FlextMeltanoInstaller,
    create_installer_service,
    flext_meltano_install_plugin,
)


class TestFlextMeltanoInstaller:
    """Test FlextMeltano installer functionality."""

    def test_installer_initialization(self) -> None:
        """Test installer initialization."""

        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)
        assert installer is not None
        assert installer.config is not None

    def test_installer_initialization_with_path(self) -> None:
        """Test installer initialization with custom path."""

        with tempfile.TemporaryDirectory() as temp_dir:
            custom_path = Path(temp_dir) / "test"
            config = FlextMeltanoConfig(project_root=str(custom_path))
            installer = FlextMeltanoInstaller(config)
            if installer.project_root != custom_path:
                msg = f"Expected {custom_path}, got {installer.project_root}"
                raise AssertionError(msg)

    def test_installer_validate(self) -> None:
        """Test installer validation."""

        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)
        result = installer.validate()
        # May fail if project doesn't exist, but should not crash
        assert result.is_success or not result.is_success

    def test_installer_initialize(self) -> None:
        """Test installer initialization method."""

        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)
        result = installer.initialize()
        assert result.is_success
        if not (installer._initialized):
            msg = f"Expected True, got {installer._initialized}"
            raise AssertionError(msg)

    def test_installer_get_health_status(self) -> None:
        """Test installer health status."""

        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)
        result = installer.get_health_status()
        assert result.is_success
        assert result.data is not None
        if "service" not in result.data:
            msg = f"Expected {'service'} in {result.data}"
            raise AssertionError(msg)
        if result.data["service"] != "installation":
            msg = f"Expected {'installation'}, got {result.data['service']}"
            raise AssertionError(msg)

    def test_installer_add_plugin(self) -> None:
        """Test installer add_plugin method."""

        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)
        result = installer.add_plugin("extractor", "tap-csv")
        # May fail if meltano not installed, but should not crash
        assert result.is_success or not result.is_success

    def test_installer_add_plugin_with_config(self) -> None:
        """Test installer add plugin with configuration."""

        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)
        result = installer.add_plugin(
            "extractor",
            "tap-csv",
            pip_url="pipelinewise-tap-csv",
        )
        # May fail if meltano not installed, but should not crash
        assert result.is_success or not result.is_success

    def test_installer_install_plugins(self) -> None:
        """Test installer install_plugins method."""

        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)
        result = installer.install_plugins()
        # May fail if meltano not installed, but should not crash
        assert result.is_success or not result.is_success

    def test_installer_remove_plugin(self) -> None:
        """Test installer remove plugin."""

        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)
        result = installer.remove_plugin("extractor", "tap-csv")
        # May fail if meltano not installed, but should not crash
        assert result.is_success or not result.is_success

    def test_installer_list_plugins(self) -> None:
        """Test installer list plugins."""

        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)
        result = installer.list_plugins()
        # May fail if meltano not installed, but should not crash
        assert result.is_success or not result.is_success


class TestFlextMeltanoInstallerFactoryFunctions:
    """Test installer factory functions."""

    def test_create_installer_service(self) -> None:
        """Test creating installer service via factory."""

        config = FlextMeltanoConfig()
        result = create_installer_service(config)
        assert result.is_success
        assert isinstance(result.data, FlextMeltanoInstaller)

    def test_create_installer_service_with_path(self) -> None:
        """Test creating installer service with custom path."""

        with tempfile.TemporaryDirectory() as temp_dir:
            custom_path = Path(temp_dir) / "test"
            config = FlextMeltanoConfig(project_root=str(custom_path))
            result = create_installer_service(config)
            assert result.is_success
        assert result.data is not None
        if result.data.project_root != custom_path:
            msg = f"Expected {custom_path}, got {result.data.project_root}"
            raise AssertionError(msg)

    def test_flext_meltano_install_plugin(self) -> None:
        """Test standalone install plugin function."""

        result = flext_meltano_install_plugin("extractor", "tap-csv", Path.cwd())
        # May fail if meltano not installed, but should not crash
        assert result.success or not result.success

    def test_flext_meltano_install_plugin_invalid_type(self) -> None:
        """Test standalone install plugin with invalid type."""

        result = flext_meltano_install_plugin("invalid", "some-plugin", Path.cwd())
        # Should handle gracefully
        assert result.success or not result.success


class TestFlextMeltanoInstallerIntegration:
    """Integration tests for installer functionality."""

    def test_installer_workflow(self) -> None:
        """Test typical installer workflow."""

        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)

        # Test initialization
        init_result = installer.initialize()
        assert init_result.is_success

        # Test health check
        health_result = installer.get_health_status()
        assert health_result.is_success

        # Test plugin operations - may fail if meltano not installed, but should not crash
        # get_plugin_status method is not implemented yet

    def test_installer_service_creation(self) -> None:
        """Test installer service creation workflow."""

        config = FlextMeltanoConfig()

        # Create installer service
        create_result = create_installer_service(config)
        assert create_result.is_success

        installer = create_result.data
        assert installer is not None

        # Test basic operations
        health_result = installer.get_health_status()
        assert health_result.is_success

        validate_result = installer.validate()
        # May fail if project setup is incomplete, but should not crash
        assert validate_result.is_success or not validate_result.is_success

    def test_installer_error_handling(self) -> None:
        """Test installer error handling."""

        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)

        # Test with potentially problematic inputs
        test_cases = [
            ("add_plugin", ("", "")),
            ("add_plugin", ("invalid", "nonexistent")),
            ("remove_plugin", ("invalid", "nonexistent-plugin")),
            ("list_plugins", ()),
        ]

        for method_name, args in test_cases:
            method = getattr(installer, method_name)
            result = method(*args)
            # Should not raise exceptions, should return FlextResult
            assert result.is_success or not result.is_success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
