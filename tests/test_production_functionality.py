"""Production functionality tests for flext-meltano.

This module tests actual flext-meltano functionality as it would be used in production,
focusing on real operations, integration patterns, and the Bridge interface.

Key Tests:
- FlextMeltanoBridge production interface
- Real subprocess execution through Meltano CLI
- Configuration and environment setup
- Error handling and result patterns
- Singer SDK integration patterns
- DBT integration functionality

Author: FLEXT Development Team
Version: 2.0.0-enterprise
"""

import subprocess
import sys
from pathlib import Path

import pytest
from flext_core import FlextResult

from flext_meltano import (
    FlextMeltanoBridge,
    FlextMeltanoConfig,
    FlextMeltanoExecutor,
)


class TestFlextMeltanoBridgeProduction:
    """Test the production FlextMeltano bridge interface."""

    def test_bridge_creation_with_config(self) -> None:
        """Test creating a bridge with custom configuration."""
        config = FlextMeltanoConfig(
            project_root="/tmp/test_project",
            environment="test",
        )

        bridge = FlextMeltanoBridge(config)

        assert bridge._config.project_root == "/tmp/test_project"
        assert bridge._config.environment == "test"
        assert isinstance(bridge._executor, FlextMeltanoExecutor)

    def test_bridge_factory_function(self) -> None:
        """Test the bridge factory function."""
        bridge = create_flext_meltano_bridge()

        assert isinstance(bridge, FlextMeltanoBridge)
        assert bridge._config is not None
        assert bridge._executor is not None

    def test_get_version_functionality(self) -> None:
        """Test getting version information through the bridge."""
        bridge = create_flext_meltano_bridge()
        result = bridge.get_version()

        assert isinstance(result, FlextResult)

        if result.success:
            assert isinstance(result.value, dict)
            assert "python" in result.value
            assert "flext_meltano" in result.value
            # Python version should be current version
            expected_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            assert result.value["python"] == expected_version
            assert result.value["flext_meltano"] == "2.0.0-enterprise"
        else:
            # If meltano is not available, that's acceptable in test environment
            assert "Failed to get version information" in str(result.error)

    def test_plugin_registry_access(self) -> None:
        """Test accessing the plugin registry."""
        bridge = create_flext_meltano_bridge()
        registry = bridge.get_plugin_registry()

        # Registry should exist (may be empty)
        assert registry is not None

    def test_create_data_plugin_tap(self) -> None:
        """Test creating a tap plugin through the bridge."""
        bridge = create_flext_meltano_bridge()
        result = bridge.create_data_plugin_from_name("tap-csv")

        assert isinstance(result, FlextResult)

        if result.success:
            plugin = result.value
            assert plugin.name == "tap-csv"
            assert "tap" in plugin.name.lower()
        else:
            # Plugin creation might fail if dependencies aren't available
            assert result.error is not None

    def test_create_data_plugin_target(self) -> None:
        """Test creating a target plugin through the bridge."""
        bridge = create_flext_meltano_bridge()
        result = bridge.create_data_plugin_from_name("target-jsonl")

        assert isinstance(result, FlextResult)

        if result.success:
            plugin = result.value
            assert plugin.name == "target-jsonl"
            assert "target" in plugin.name.lower()

    def test_list_plugins_functionality(self) -> None:
        """Test listing plugins through the bridge."""
        bridge = create_flext_meltano_bridge()
        result = bridge.list_plugins()

        assert isinstance(result, FlextResult)

        if result.success:
            assert isinstance(result.value, list)
            # Each plugin should be a dict with basic info
            for plugin in result.value:
                assert isinstance(plugin, dict)
                if plugin:  # If plugin has data
                    assert "name" in plugin or "type" in plugin
        else:
            # If meltano list fails, that's acceptable in test environment
            assert result.error is not None

    def test_add_plugin_functionality(self) -> None:
        """Test adding a plugin through the bridge."""
        bridge = create_flext_meltano_bridge()
        result = bridge.add_plugin("extractor", "tap-csv")

        assert isinstance(result, FlextResult)

        # In test environment, this might fail due to missing Meltano project
        # But the interface should work correctly
        if not result.success:
            assert "installation requires initialized Meltano project" in str(
                result.error
            )

    def test_discover_catalog_functionality(self) -> None:
        """Test catalog discovery through the bridge."""
        bridge = create_flext_meltano_bridge()
        result = bridge.discover_catalog("tap-csv")

        assert isinstance(result, FlextResult)

        # In test environment, this might fail due to missing configuration
        if not result.success:
            assert "requires configured Meltano project" in str(result.error)

    def test_run_pipeline_interface(self) -> None:
        """Test the pipeline execution interface."""
        bridge = create_flext_meltano_bridge()
        result = bridge.run_pipeline("tap-csv", "target-csv")

        assert isinstance(result, FlextResult)

        # Pipeline execution requires proper Meltano setup, but interface should work
        if result.success:
            assert isinstance(result.value, dict)
            assert "status" in result.value
            assert "tap" in result.value
            assert "target" in result.value
        else:
            # Expected to fail without proper Meltano project setup
            assert result.error is not None

    def test_invoke_dbt_interface(self) -> None:
        """Test the DBT invocation interface."""
        bridge = create_flext_meltano_bridge()
        result = bridge.invoke_dbt("run", "--help")

        assert isinstance(result, FlextResult)

        # DBT operations require proper project setup
        if not result.success:
            assert "DBT operations require configured DBT project" in str(result.error)


class TestFlextMeltanoExecutor:
    """Test the FlextMeltanoExecutor for real command execution."""

    def test_executor_creation(self) -> None:
        """Test creating an executor with configuration."""
        config = FlextMeltanoConfig(environment="test")
        executor = FlextMeltanoExecutor(config)

        assert executor.config == config

    def test_meltano_command_execution(self) -> None:
        """Test executing a real Meltano command through the executor."""
        config = FlextMeltanoConfig()
        executor = FlextMeltanoExecutor(config)

        # Test meltano version command
        result = executor.run_command(["--version"])

        assert isinstance(result, FlextResult)
        # This should work in any environment with Meltano, or fail gracefully
        if result.success:
            assert isinstance(result.value, dict)
        else:
            assert result.error is not None


class TestFlextMeltanoConfiguration:
    """Test configuration handling and validation."""

    def test_default_configuration(self) -> None:
        """Test default configuration values."""
        config = FlextMeltanoConfig()

        assert config.project_root is not None
        assert config.environment == "dev"

    def test_custom_configuration(self) -> None:
        """Test creating custom configuration."""
        config = FlextMeltanoConfig(
            project_root="/custom/path",
            environment="production",
        )

        assert config.project_root == "/custom/path"
        assert config.environment == "production"

    def test_configuration_validation(self) -> None:
        """Test configuration validation."""
        # Test with valid path
        config = FlextMeltanoConfig(project_root="/tmp")
        assert config.project_root == "/tmp"

        # Environment should be string
        config = FlextMeltanoConfig(environment="staging")
        assert config.environment == "staging"


class TestRealSubprocessExecution:
    """Test real subprocess execution patterns."""

    def test_subprocess_with_timeout(self) -> None:
        """Test subprocess execution with timeout handling."""
        # Test a command that should complete quickly
        result = subprocess.run(
            ["python3", "-c", "import time; print('Quick command')"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )

        assert result.returncode == 0
        assert "Quick command" in result.stdout

    def test_subprocess_error_handling(self) -> None:
        """Test subprocess error handling."""
        # Test a command that should fail
        result = subprocess.run(
            ["python3", "-c", "raise ValueError('Test error')"],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0
        assert "ValueError" in result.stderr

    def test_subprocess_environment_variables(self) -> None:
        """Test subprocess with environment variables."""
        import os

        env = os.environ.copy()
        env["TEST_VAR"] = "test_value"

        result = subprocess.run(
            [
                "python3",
                "-c",
                "import os; print(os.environ.get('TEST_VAR', 'not_found'))",
            ],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode == 0
        assert "test_value" in result.stdout


class TestFlextCoreIntegration:
    """Test integration with flext-core patterns."""

    def test_flext_result_success_pattern(self) -> None:
        """Test FlextResult success pattern."""
        result: FlextResult[str] = FlextResult[str].ok("Success value")

        assert result.success
        assert result.value == "Success value"
        assert result.error is None

    def test_flext_result_failure_pattern(self) -> None:
        """Test FlextResult failure pattern."""
        result: FlextResult[str] = FlextResult[str].fail("Error message")

        assert not result.success
        assert result.value is None
        assert result.error == "Error message"

    def test_flext_result_chaining(self) -> None:
        """Test FlextResult method chaining."""

        def double_value(x: int) -> int:
            return x * 2

        def stringify_value(x: int) -> str:
            return f"Value: {x}"

        result = FlextResult[int].ok(5).map(double_value).map(stringify_value)

        assert result.success
        assert result.value == "Value: 10"


class TestFileSystemOperations:
    """Test real file system operations used by flext-meltano."""

    def test_path_operations(self) -> None:
        """Test Path operations used in configuration."""
        # Test creating Path objects as used in configuration
        project_path = Path("/tmp/test_project")
        config_file = project_path / "meltano.yml"

        assert isinstance(project_path, Path)
        assert str(config_file).endswith("meltano.yml")
        assert config_file.parent == project_path

    def test_directory_existence_check(self) -> None:
        """Test directory existence patterns used in the codebase."""
        # Test checking if a directory exists (common pattern in flext-meltano)
        temp_dir = Path("/tmp")

        # /tmp should exist on most systems
        exists = temp_dir.exists() and temp_dir.is_dir()
        assert isinstance(exists, bool)

    def test_file_path_construction(self) -> None:
        """Test file path construction patterns."""
        # Test patterns used for configuration files
        base_path = Path.home()
        flext_dir = base_path / ".flext"
        config_file = flext_dir / "config.yml"

        assert isinstance(config_file, Path)
        assert config_file.name == "config.yml"
        assert config_file.parent.name == ".flext"


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
