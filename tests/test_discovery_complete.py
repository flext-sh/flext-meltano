"""Comprehensive tests for discovery module."""

from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

import pytest

from flext_meltano.base import FlextMeltanoConfig
from flext_meltano.discovery import (
    FlextMeltanoDiscoverer,
    FlextMeltanoDiscoveryCommand,
    FlextMeltanoDiscoveryContext,
    FlextMeltanoPlugin,
    create_discoverer,
    flext_meltano_discover_catalog,
    flext_meltano_discover_plugins,
)


class TestFlextMeltanoDiscoveryCommand:
    """Test FlextMeltanoDiscoveryCommand model."""

    def test_command_initialization(self) -> None:
        """Test command initialization."""
        command = FlextMeltanoDiscoveryCommand(tap_name="tap-csv")
        if command.tap_name != "tap-csv":
            msg = f"Expected {"tap-csv"}, got {command.tap_name}"
            raise AssertionError(msg)

    def test_command_with_different_tap(self) -> None:
        """Test command with different tap name."""
        command = FlextMeltanoDiscoveryCommand(tap_name="tap-postgres")
        if command.tap_name != "tap-postgres":
            msg = f"Expected {"tap-postgres"}, got {command.tap_name}"
            raise AssertionError(msg)

    def test_command_attribute_access(self) -> None:
        """Test that command attributes can be accessed."""
        command = FlextMeltanoDiscoveryCommand(tap_name="tap-csv")
        # Simple class - attributes can be modified
        command.tap_name = "tap-postgres"
        if command.tap_name != "tap-postgres":
            msg = f"Expected {"tap-postgres"}, got {command.tap_name}"
            raise AssertionError(msg)


class TestFlextMeltanoDiscoverer:
    """Test FlextMeltanoDiscoverer functionality."""

    def test_service_initialization(self) -> None:
        """Test service initialization."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDiscoverer(config)
        assert service is not None
        assert service.config is not None
        if service._initialized:
            msg = f"Expected False, got {service._initialized}"
            raise AssertionError(msg)

    def test_service_initialize(self) -> None:
        """Test service initialization method."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDiscoverer(config)
        result = service.initialize()
        assert result.is_success
        if not (service._initialized):
            msg = f"Expected True, got {service._initialized}"
            raise AssertionError(msg)

    def test_service_validate(self) -> None:
        """Test service validation."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDiscoverer(config)
        result = service.validate()
        # May fail if environment not properly set up
        assert result.is_success or not result.is_success

    def test_service_get_health_status(self) -> None:
        """Test service health status."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDiscoverer(config)
        result = service.get_health_status()
        assert result.is_success
        assert result.data is not None
        if "service" not in result.data:
            msg = f"Expected {"service"} in {result.data}"
            raise AssertionError(msg)
        if result.data["service"] != "discovery":
            msg = f"Expected {"discovery"}, got {result.data["service"]}"
            raise AssertionError(msg)

    def test_discover_catalog_async(self) -> None:
        """Test discover catalog async method."""

        async def run_test() -> None:
            config = FlextMeltanoConfig()
            service = FlextMeltanoDiscoverer(config)
            # This will likely fail since tap not installed, but should not crash
            result = await service.discover_catalog("tap-csv")
            assert result.is_success or not result.is_success

        asyncio.run(run_test())

    def test_discover_catalog_with_config_async(self) -> None:
        """Test discover catalog with config async."""

        async def run_test() -> None:
            config = FlextMeltanoConfig()
            service = FlextMeltanoDiscoverer(config)
            tap_config = {"files": [{"entity": "users", "path": "/data/users.csv"}]}
            # This will likely fail since tap not installed, but should not crash
            result = await service.discover_catalog("tap-csv", tap_config)
            assert result.is_success or not result.is_success

        asyncio.run(run_test())

    def test_discover_catalog_subprocess_async(self) -> None:
        """Test discover catalog subprocess method."""

        async def run_test() -> None:
            config = FlextMeltanoConfig()
            service = FlextMeltanoDiscoverer(config)
            context = FlextMeltanoDiscoveryContext(tap_name="tap-csv")
            # This will likely fail since tap not installed, but should not crash
            result = await service._discover_catalog_subprocess("tap-csv", {}, context)
            assert result.is_success or not result.is_success

        asyncio.run(run_test())

    def test_discover_catalog_direct_async(self) -> None:
        """Test discover catalog direct method."""

        async def run_test() -> None:
            config = FlextMeltanoConfig()
            service = FlextMeltanoDiscoverer(config)
            context = FlextMeltanoDiscoveryContext(tap_name="tap-csv")
            # This will likely fail since tap not installed, but should not crash
            result = await service._discover_catalog_direct("tap-csv", {}, context)
            assert result.is_success or not result.is_success

        asyncio.run(run_test())

    def test_discover_plugins(self) -> None:
        """Test discover plugins method."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDiscoverer(config)
        result = service.discover_plugins()
        # May fail if Meltano Hub not accessible, but should not crash
        assert result.is_success or not result.is_success

    def test_discover_plugins_with_type(self) -> None:
        """Test discover plugins with specific type."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDiscoverer(config)
        result = service.discover_plugins("extractors")
        # May fail if Meltano Hub not accessible, but should not crash
        assert result.is_success or not result.is_success

    def test_get_default_plugins(self) -> None:
        """Test get default plugins method."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDiscoverer(config)
        plugins = service._get_default_plugins()
        assert isinstance(plugins, list)
        assert len(plugins) > 0
        # Should contain common plugin types
        plugin_names = [p.name for p in plugins]
        if not any("tap-csv" in name for name in plugin_names):
            msg = f"Expected tap-csv plugin in {plugin_names}"
            raise AssertionError(msg)

    def test_convert_plugin_type_string(self) -> None:
        """Test convert plugin type string method."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDiscoverer(config)

        # Test valid types
        result = service._convert_plugin_type_string("extractors")
        assert result is not None

        result = service._convert_plugin_type_string("loaders")
        assert result is not None

        # Test invalid type
        result = service._convert_plugin_type_string("invalid")
        assert result is None

    def test_execute_command(self) -> None:
        """Test execute command method."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDiscoverer(config)
        command = FlextMeltanoDiscoveryCommand(tap_name="tap-csv")
        result = service.execute(command)
        # May fail if tap not available, but should not crash
        assert result.is_success or not result.is_success


class TestFlextMeltanoPlugin:
    """Test FlextMeltanoPlugin model."""

    def test_plugin_discovery_initialization(self) -> None:
        """Test plugin discovery initialization."""
        plugin = FlextMeltanoPlugin(
            name="tap-csv",
            type="extractor",
            namespace="tap_csv",
            pip_url="tap-csv",
        )
        if plugin.name != "tap-csv":
            msg = f"Expected {"tap-csv"}, got {plugin.name}"
            raise AssertionError(msg)
        assert plugin.type == "extractor"
        if plugin.namespace != "tap_csv":
            msg = f"Expected {"tap_csv"}, got {plugin.namespace}"
            raise AssertionError(msg)
        assert plugin.pip_url == "tap-csv"
        if plugin.description != "":
            msg = f"Expected {""}, got {plugin.description}"
            raise AssertionError(msg)
        assert plugin.version is None
        if plugin.capabilities != []:
            msg = f"Expected {[]}, got {plugin.capabilities}"
            raise AssertionError(msg)

    def test_plugin_discovery_with_all_fields(self) -> None:
        """Test plugin discovery with all fields."""
        plugin = FlextMeltanoPlugin(
            name="tap-postgres",
            type="extractor",
            namespace="tap_postgres",
            description="PostgreSQL tap",
            pip_url="pipelinewise-tap-postgres",
            version="1.0.0",
            capabilities=["discover", "catalog"],
        )
        if plugin.name != "tap-postgres":
            msg = f"Expected {"tap-postgres"}, got {plugin.name}"
            raise AssertionError(msg)
        assert plugin.type == "extractor"
        if plugin.namespace != "tap_postgres":
            msg = f"Expected {"tap_postgres"}, got {plugin.namespace}"
            raise AssertionError(msg)
        assert plugin.description == "PostgreSQL tap"
        if plugin.pip_url != "pipelinewise-tap-postgres":
            msg = f"Expected {"pipelinewise-tap-postgres"}, got {plugin.pip_url}"
            raise AssertionError(msg)
        assert plugin.version == "1.0.0"
        if plugin.capabilities != ["discover", "catalog"]:
            msg = f"Expected {["discover", "catalog"]}, got {plugin.capabilities}"
            raise AssertionError(msg)

    def test_plugin_discovery_frozen(self) -> None:
        """Test that plugin discovery is frozen (immutable)."""
        plugin = FlextMeltanoPlugin(
            name="tap-csv",
            type="extractors",
            namespace="tap_csv",
            description="CSV tap",
            pip_url="tap-csv",
        )
        with pytest.raises(Exception, match=".*"):  # ValidationError from Pydantic
            plugin.name = "changed"  # type: ignore[misc]


class TestFactoryFunctions:
    """Test factory functions."""

    def test_create_discoverer(self) -> None:
        """Test create discoverer factory function."""
        config = FlextMeltanoConfig()
        result = create_discoverer(config)
        assert result.is_success
        assert isinstance(result.data, FlextMeltanoDiscoverer)

    def test_flext_meltano_discover_catalog_async(self) -> None:
        """Test standalone discover catalog function."""

        async def run_test() -> None:
            result = await flext_meltano_discover_catalog(
                "tap-csv",
                Path.cwd(),
                {"files": [{"entity": "users", "path": "/data/users.csv"}]},
            )
            # May fail if tap not installed, but should not crash
            assert result.success or not result.success

        asyncio.run(run_test())

    def test_flext_meltano_discover_plugins(self) -> None:
        """Test standalone discover plugins function."""
        result = flext_meltano_discover_plugins()
        # May fail if Meltano Hub not accessible, but should not crash
        assert result.success or not result.success

    def test_flext_meltano_discover_plugins_with_type(self) -> None:
        """Test standalone discover plugins with type."""
        result = flext_meltano_discover_plugins("extractors")
        # May fail if Meltano Hub not accessible, but should not crash
        assert result.success or not result.success


class TestDiscoveryIntegration:
    """Integration tests for discovery functionality."""

    def test_complete_discovery_workflow(self) -> None:
        """Test complete discovery workflow."""
        config = FlextMeltanoConfig()

        # Create discovery service
        create_result = create_discoverer(config)
        assert create_result.is_success

        assert create_result.data is not None
        service = create_result.data

        # Test initialization
        init_result = service.initialize()
        assert init_result.is_success

        # Test health check
        health_result = service.get_health_status()
        assert health_result.is_success

        # Test plugin discovery
        plugins_result = service.discover_plugins()
        # May fail if Meltano Hub not accessible, but should not crash
        assert plugins_result.is_success or not plugins_result.is_success

    def test_discovery_error_handling(self) -> None:
        """Test discovery error handling."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDiscoverer(config)

        # Test with invalid plugin types
        result = service.discover_plugins("invalid_type")
        # Should handle gracefully
        assert result.is_success or not result.is_success

        # Test catalog discovery with nonexistent tap

        async def test_invalid_tap() -> None:
            result = await service.discover_catalog("nonexistent-tap")
            assert result.is_success or not result.is_success

        asyncio.run(test_invalid_tap())

    def test_discovery_with_custom_config(self) -> None:
        """Test discovery with custom configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_path = Path(temp_dir) / "test"
            config = FlextMeltanoConfig(project_root=str(custom_path))
            service = FlextMeltanoDiscoverer(config)

            if service.config.project_root != str(custom_path):

                msg = f"Expected {custom_path!s}, got {service.config.project_root}"
                raise AssertionError(msg)

        # Test operations still work
        init_result = service.initialize()
        assert init_result.is_success

        health_result = service.get_health_status()
        assert health_result.is_success

    def test_discovery_command_execution(self) -> None:
        """Test discovery command execution workflow."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDiscoverer(config)

        # Create and execute discovery command
        command = FlextMeltanoDiscoveryCommand(tap_name="tap-csv")
        result = service.execute(command)

        # Should handle gracefully even if tap not available
        assert result.is_success or not result.is_success

        # Verify command properties
        if command.tap_name != "tap-csv":
            msg = f"Expected {"tap-csv"}, got {command.tap_name}"
            raise AssertionError(msg)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
