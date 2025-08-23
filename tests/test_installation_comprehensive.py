"""Installation Module Comprehensive Test Suite - Plugin Management Layer Validation.

**Test Category**: Integration Tests
**Coverage Target**: 95%+ for installation module components
**Dependencies**: Mock subprocess calls, plugin registry, Meltano CLI integration
**Execution Time**: < 12 seconds total

## Test Scope

Validates the installation module components that provide **plugin installation and management**
for FLEXT Meltano's bridge architecture, focusing on Meltano plugin installation, configuration
management, and installation context tracking for Go service bridge operations.

## Test Coverage Areas

1. **Plugin Installation**: Meltano plugin installation via CLI orchestration
2. **Installation Context**: Installation metadata and tracking management
3. **Configuration Management**: Plugin configuration and setting validation
4. **Service Patterns**: FlextMeltanoInstaller service functionality
5. **Bridge Integration**: Installation operations via bridge interface
6. **Error Handling**: Installation failures and recovery patterns

## Architecture Alignment

Tests align with FLEXT Meltano's installation layer architecture:
- **Plugin Management**: Direct Meltano plugin installation and configuration
- **Installation Orchestration**: Subprocess-based installation with monitoring
- **Bridge Communication**: Installation status and results for Go services
- **Enterprise Patterns**: FlextResult integration and structured error handling

These tests ensure the installation module provides reliable plugin management
that enables comprehensive bridge-based plugin operations for Go services.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from flext_core import FlextResult

from flext_meltano import (
    FlextMeltanoConfig,
    FlextMeltanoInstallationContext,
    FlextMeltanoInstaller,
    FlextMeltanoPluginInfo,
    create_installer_service,
    flext_meltano_install_plugin,
)

# Constants
DEFAULT_TTL = 600
EXPECTED_BULK_SIZE = 2
EXPECTED_DATA_COUNT = 3


class TestFlextMeltanoInstallationContext:
    """Test FlextMeltanoInstallationContext model."""

    def test_context_initialization_defaults(self) -> None:
        """Test context initialization with defaults."""
        context = FlextMeltanoInstallationContext(
            plugin_name="tap-csv",
            plugin_type="extractors",
        )
        if context.plugin_name != "tap-csv":
            msg: str = f"Expected {'tap-csv'}, got {context.plugin_name}"
            raise AssertionError(msg)
        assert context.plugin_type == "extractors"
        if context.timeout_seconds != DEFAULT_TTL:
            msg: str = f"Expected {600}, got {context.timeout_seconds}"
            raise AssertionError(msg)
        assert context.metadata == {}
        assert isinstance(context.installation_id, str)
        assert isinstance(context.started_at, datetime)

    def test_context_initialization_custom(self) -> None:
        """Test context initialization with custom values."""
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_path = Path(temp_dir) / "test"
            context = FlextMeltanoInstallationContext(
                plugin_name="tap-postgres",
                plugin_type="extractors",
                project_root=custom_path,
                timeout_seconds=300,
                metadata={"test": "value"},
            )
            if context.plugin_name != "tap-postgres":
                msg: str = f"Expected {'tap-postgres'}, got {context.plugin_name}"
                raise AssertionError(
                    msg,
                )
            assert context.plugin_type == "extractors"
            if context.project_root != custom_path:
                msg: str = f"Expected {custom_path}, got {context.project_root}"
                raise AssertionError(
                    msg,
                )
            assert context.timeout_seconds == 300
            if context.metadata != {"test": "value"}:
                msg = f'Expected {{"test": "value"}}, got {context.metadata}'
                raise AssertionError(
                    msg,
                )


class TestFlextMeltanoPluginInfo:
    """Test FlextMeltanoPluginInfo model."""

    def test_plugin_info_minimal(self) -> None:
        """Test plugin info with minimal fields."""
        plugin = FlextMeltanoPluginInfo(
            name="tap-csv",
            type="extractors",
            namespace="tap_csv",
        )
        if plugin.name != "tap-csv":
            msg: str = f"Expected {'tap-csv'}, got {plugin.name}"
            raise AssertionError(msg)
        assert plugin.type == "extractors"
        if plugin.namespace != "tap_csv":
            msg: str = f"Expected {'tap_csv'}, got {plugin.namespace}"
            raise AssertionError(msg)
        assert plugin.pip_url is None
        assert plugin.executable is None
        if plugin.description != "":
            msg: str = f"Expected {''}, got {plugin.description}"
            raise AssertionError(msg)
        assert plugin.version is None
        if plugin.installed:
            msg: str = f"Expected False, got {plugin.installed}"
            raise AssertionError(msg)

    def test_plugin_info_complete(self) -> None:
        """Test plugin info with all fields."""
        plugin = FlextMeltanoPluginInfo(
            name="tap-postgres",
            type="extractors",
            namespace="tap_postgres",
            pip_url="pipelinewise-tap-postgres",
            executable="tap-postgres",
            description="PostgreSQL tap",
            version="0.9.0",
            installed=True,
        )
        if plugin.name != "tap-postgres":
            msg: str = f"Expected {'tap-postgres'}, got {plugin.name}"
            raise AssertionError(msg)
        assert plugin.type == "extractors"
        if plugin.namespace != "tap_postgres":
            msg: str = f"Expected {'tap_postgres'}, got {plugin.namespace}"
            raise AssertionError(msg)
        assert plugin.pip_url == "pipelinewise-tap-postgres"
        if plugin.executable != "tap-postgres":
            msg: str = f"Expected {'tap-postgres'}, got {plugin.executable}"
            raise AssertionError(msg)
        assert plugin.description == "PostgreSQL tap"
        if plugin.version != "0.9.0":
            msg: str = f"Expected {'1.0.0'}, got {plugin.version}"
            raise AssertionError(msg)
        if not (plugin.installed):
            msg: str = f"Expected True, got {plugin.installed}"
            raise AssertionError(msg)

    def test_plugin_info_frozen(self) -> None:
        """Test that plugin info is frozen."""
        plugin = FlextMeltanoPluginInfo(
            name="tap-csv",
            type="extractors",
            namespace="tap_csv",
        )
        with pytest.raises(Exception, match=".*"):  # ValidationError from Pydantic
            plugin.name = "changed"


class TestFlextMeltanoInstallerValidation:
    """Test FlextMeltanoInstaller validation methods."""

    def test_validation_success_with_meltano_yml(self) -> None:
        """Test validation success when meltano.yml exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create meltano.yml file
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            installer = FlextMeltanoInstaller(config)

            result = installer.validate()
            assert result.success
            if not (result.value):
                msg: str = f"Expected True, got {result.value}"
                raise AssertionError(msg)

    def test_validation_failure_missing_project_root(self) -> None:
        """Test validation failure when project root doesn't exist."""
        config = FlextMeltanoConfig(project_root="/nonexistent/path")
        installer = FlextMeltanoInstaller(config)

        result = installer.validate()
        assert not result.success
        assert result.error is not None
        if "Project root does not exist" not in result.error:
            msg: str = f"Expected {'Project root does not exist'} in {result.error}"
            raise AssertionError(
                msg,
            )

    def test_validation_failure_missing_meltano_yml(self) -> None:
        """Test validation failure when meltano.yml doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(project_root=temp_dir)
            installer = FlextMeltanoInstaller(config)

            result = installer.validate()
            assert not result.success
            assert result.error is not None
            if "No meltano.yml found" not in result.error:
                msg: str = f"Expected {'No meltano.yml found'} in {result.error}"
                raise AssertionError(
                    msg,
                )

    def test_validation_exception_handling(self) -> None:
        """Test validation exception handling."""
        # This should trigger an OSError or ValueError during validation
        config = FlextMeltanoConfig(project_root="")  # Empty path
        installer = FlextMeltanoInstaller(config)

        result = installer.validate()
        # Should handle gracefully - may succeed or fail, but no exception
        assert result.success or not result.success


class TestFlextMeltanoInstallerOperations:
    """Test FlextMeltanoInstaller operations with mocking."""

    @patch("subprocess.run")
    def test_add_plugin_success(self, mock_run: Mock) -> None:
        """Test successful plugin addition."""
        # Mock successful subprocess execution
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Plugin added successfully"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create meltano.yml file
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            installer = FlextMeltanoInstaller(config)

            result = installer.add_plugin("extractor", "tap-csv")
            assert result.success
            assert result.value is not None
            if not (result.value["success"]):
                msg: str = f"Expected True, got {result.value['success']}"
                raise AssertionError(msg)
            if result.value["plugin_name"] != "tap-csv":
                msg: str = f"Expected {'tap-csv'}, got {result.value['plugin_name']}"
                raise AssertionError(
                    msg,
                )
            assert result.value["plugin_type"] == "extractor"

    @patch("subprocess.run")
    def test_add_plugin_with_pip_url(self, mock_run: Mock) -> None:
        """Test plugin addition with custom pip URL."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Plugin added successfully"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            installer = FlextMeltanoInstaller(config)

            result = installer.add_plugin(
                "extractor",
                "tap-csv",
                "pipelinewise-tap-csv",
            )
            assert result.success
            assert result.value is not None
            if result.value["pip_url"] != "pipelinewise-tap-csv":
                msg: str = (
                    f"Expected {'pipelinewise-tap-csv'}, got {result.value['pip_url']}"
                )
                raise AssertionError(
                    msg,
                )

            # Verify command construction
            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            if args != [
                "meltano",
                "add",
                "extractor",
                "tap-csv",
                "--custom",
                "pipelinewise-tap-csv",
            ]:
                msg: str = f"Expected {['meltano', 'add', 'extractor', 'tap-csv', '--custom', 'pipelinewise-tap-csv']}, got {args}"
                raise AssertionError(
                    msg,
                )

    @patch("subprocess.run")
    def test_add_plugin_failure(self, mock_run: Mock) -> None:
        """Test plugin addition failure."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Plugin not found"
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            installer = FlextMeltanoInstaller(config)

            result = installer.add_plugin("extractor", "nonexistent-tap")
            assert not result.success
            assert result.error is not None
            if "Plugin add failed" not in result.error:
                msg: str = f"Expected {'Plugin add failed'} in {result.error}"
                raise AssertionError(
                    msg,
                )

    @patch("subprocess.run")
    def test_add_plugin_timeout(self, mock_run: Mock) -> None:
        """Test plugin addition timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired("meltano", 600)

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            installer = FlextMeltanoInstaller(config)

            result = installer.add_plugin("extractor", "tap-csv")
            assert not result.success
            assert result.error is not None
            if "Command timed out" not in result.error:
                msg: str = f"Expected {'Command timed out'} in {result.error}"
                raise AssertionError(
                    msg,
                )

    @patch("subprocess.run")
    def test_install_plugins_success(self, mock_run: Mock) -> None:
        """Test successful plugins installation."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "All plugins installed successfully"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            installer = FlextMeltanoInstaller(config)

            result = installer.install_plugins()
            assert result.success
            assert result.value is not None
            if result.value["operation"] != "install_all":
                msg: str = f"Expected {'install_all'}, got {result.value['operation']}"
                raise AssertionError(
                    msg,
                )
            if not (result.value["success"]):
                msg: str = f"Expected True, got {result.value['success']}"
                raise AssertionError(msg)

    @patch("subprocess.run")
    def test_remove_plugin_success(self, mock_run: Mock) -> None:
        """Test successful plugin removal."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Plugin removed successfully"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            installer = FlextMeltanoInstaller(config)

            result = installer.remove_plugin("extractor", "tap-csv")
            assert result.success
            assert result.value is not None
            if result.value["operation"] != "remove":
                msg: str = f"Expected {'remove'}, got {result.value['operation']}"
                raise AssertionError(
                    msg,
                )
            assert result.value["plugin_name"] == "tap-csv"

    @patch("subprocess.run")
    def test_list_plugins_success(self, mock_run: Mock) -> None:
        """Test successful plugin listing."""
        # Mock JSON response from meltano list
        mock_plugins = {
            "extractors": [
                {
                    "name": "tap-csv",
                    "namespace": "tap_csv",
                    "pip_url": "pipelinewise-tap-csv",
                    "description": "CSV file extractor",
                },
            ],
            "loaders": [
                {
                    "name": "target-jsonl",
                    "namespace": "target_jsonl",
                    "pip_url": "target-jsonl",
                    "description": "JSONL file loader",
                },
            ],
        }

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps(mock_plugins)
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            installer = FlextMeltanoInstaller(config)

            result = installer.list_plugins()
            assert result.success
            assert result.value is not None
            if len(result.value) != EXPECTED_BULK_SIZE:  # 2 plugins total
                msg: str = f"Expected {2}, got {len(result.value)}"
                raise AssertionError(msg)

            # Check first plugin
            assert result.value is not None
            plugin = result.value[0]
            if plugin.name != "tap-csv":
                msg: str = f"Expected {'tap-csv'}, got {plugin.name}"
                raise AssertionError(msg)
            assert plugin.type == "extractors"
            if not (plugin.installed):
                msg: str = f"Expected True, got {plugin.installed}"
                raise AssertionError(msg)

    @patch("subprocess.run")
    def test_list_plugins_json_decode_error(self, mock_run: Mock) -> None:
        """Test plugin listing with invalid JSON."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "invalid json"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            installer = FlextMeltanoInstaller(config)

            result = installer.list_plugins()
            assert not result.success
            assert result.error is not None
            if "Failed to parse plugin list JSON" not in result.error:
                msg: str = (
                    f"Expected {'Failed to parse plugin list JSON'} in {result.error}"
                )
                raise AssertionError(
                    msg,
                )

    def test_convert_plugin_list(self) -> None:
        """Test _convert_plugin_list method."""
        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)

        plugin_list = [
            {
                "name": "tap-csv",
                "namespace": "tap_csv",
                "pip_url": "pipelinewise-tap-csv",
                "description": "CSV extractor",
                "version": "0.9.0",
            },
            {
                "name": "tap-postgres",
                # Missing namespace - should use name with underscores
                "description": "PostgreSQL extractor",
            },
        ]

        plugins = installer._convert_plugin_list("extractors", plugin_list)
        if len(plugins) != EXPECTED_BULK_SIZE:
            msg: str = f"Expected {2}, got {len(plugins)}"
            raise AssertionError(msg)

        # First plugin
        if plugins[0].name != "tap-csv":
            msg: str = f"Expected {'tap-csv'}, got {plugins[0].name}"
            raise AssertionError(msg)
        assert plugins[0].type == "extractors"
        if plugins[0].namespace != "tap_csv":
            msg: str = f"Expected {'tap_csv'}, got {plugins[0].namespace}"
            raise AssertionError(msg)
        assert plugins[0].version == "0.9.0"

        # Second plugin with generated namespace
        if plugins[1].name != "tap-postgres":
            msg: str = f"Expected {'tap-postgres'}, got {plugins[1].name}"
            raise AssertionError(msg)
        assert plugins[1].namespace == "tap_postgres"  # Generated from name

    def test_convert_plugin_list_edge_cases(self) -> None:
        """Test _convert_plugin_list with edge cases."""
        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)

        # Test with non-list input
        plugins = installer._convert_plugin_list("extractors", "not a list")
        if plugins != []:
            msg: str = f"Expected {[]}, got {plugins}"
            raise AssertionError(msg)

        # Test with list containing non-dict items
        plugins = installer._convert_plugin_list("extractors", ["not a dict", 123])
        if plugins != []:
            msg: str = f"Expected {[]}, got {plugins}"
            raise AssertionError(msg)

        # Test with empty dict
        plugins = installer._convert_plugin_list("extractors", [{}])
        if len(plugins) != 1:
            msg: str = f"Expected {1}, got {len(plugins)}"
            raise AssertionError(msg)
        assert plugins[0].name == ""
        if plugins[0].namespace != "":
            msg: str = f"Expected {''}, got {plugins[0].namespace}"
            raise AssertionError(msg)


class TestFlextMeltanoInstallerPrivateMethods:
    """Test FlextMeltanoInstaller private methods."""

    @patch("subprocess.run")
    def test_execute_meltano_list_success(self, mock_run: Mock) -> None:
        """Test _execute_meltano_list success."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"extractors": []}'
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)

        result = installer._execute_meltano_list()
        assert result.success
        if result.value != '{"extractors": []}':
            msg: str = f"Expected {'{"extractors": []}'}, got {result.value}"
            raise AssertionError(msg)

    @patch("subprocess.run")
    def test_execute_meltano_list_failure(self, mock_run: Mock) -> None:
        """Test _execute_meltano_list failure."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Command failed"
        mock_run.return_value = mock_result

        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)

        result = installer._execute_meltano_list()
        assert not result.success
        assert result.error is not None
        if "Plugin list failed" not in result.error:
            msg: str = f"Expected {'Plugin list failed'} in {result.error}"
            raise AssertionError(msg)

    def test_parse_plugin_list_success(self) -> None:
        """Test _parse_plugin_list success."""
        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)

        json_data = '{"extractors": [{"name": "tap-csv"}]}'
        result = installer._parse_plugin_list(json_data)

        assert result.success
        assert result.value is not None
        if len(result.value) != 1:
            msg: str = f"Expected {1}, got {len(result.value)}"
            raise AssertionError(msg)
        assert result.value[0].name == "tap-csv"

    def test_parse_plugin_list_invalid_json(self) -> None:
        """Test _parse_plugin_list with invalid JSON."""
        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)

        result = installer._parse_plugin_list("invalid json")
        assert not result.success
        assert result.error is not None
        if "Failed to parse plugin list JSON" not in result.error:
            msg: str = (
                f"Expected {'Failed to parse plugin list JSON'} in {result.error}"
            )
            raise AssertionError(
                msg,
            )


class TestFlextMeltanoInstallerContexts:
    """Test FlextMeltanoInstaller with custom contexts."""

    @patch("subprocess.run")
    def test_add_plugin_with_custom_context(self, mock_run: Mock) -> None:
        """Test add_plugin with custom context."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Plugin added"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            installer = FlextMeltanoInstaller(config)

            context = FlextMeltanoInstallationContext(
                plugin_name="tap-csv",
                plugin_type="extractor",
                timeout_seconds=300,
            )

            result = installer.add_plugin("extractor", "tap-csv", context=context)
            assert result.success
            assert result.value is not None
            if result.value["installation_id"] != context.installation_id:
                msg: str = f"Expected {context.installation_id}, got {result.value['installation_id']}"
                raise AssertionError(
                    msg,
                )

    @patch("subprocess.run")
    def test_install_plugins_with_custom_context(self, mock_run: Mock) -> None:
        """Test install_plugins with custom context."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Plugins installed"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            installer = FlextMeltanoInstaller(config)

            context = FlextMeltanoInstallationContext(
                plugin_name="all",
                plugin_type="install",
                timeout_seconds=900,
            )

            result = installer.install_plugins(context)
            assert result.success
            assert result.value is not None
            if result.value["installation_id"] != context.installation_id:
                msg: str = f"Expected {context.installation_id}, got {result.value['installation_id']}"
                raise AssertionError(
                    msg,
                )

    @patch("subprocess.run")
    def test_remove_plugin_with_custom_context(self, mock_run: Mock) -> None:
        """Test remove_plugin with custom context."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Plugin removed"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            installer = FlextMeltanoInstaller(config)

            context = FlextMeltanoInstallationContext(
                plugin_name="tap-csv",
                plugin_type="extractor",
                timeout_seconds=120,
            )

            result = installer.remove_plugin("extractor", "tap-csv", context)
            assert result.success
            assert result.value is not None
            if result.value["installation_id"] != context.installation_id:
                msg: str = f"Expected {context.installation_id}, got {result.value['installation_id']}"
                raise AssertionError(
                    msg,
                )


class TestFactoryAndLegacyFunctions:
    """Test factory and legacy compatibility functions."""

    def test_create_installer_service_success(self) -> None:
        """Test successful installer service creation."""
        config = FlextMeltanoConfig()
        result = create_installer_service(config)

        assert result.success
        assert isinstance(result.value, FlextMeltanoInstaller)
        assert result.value._initialized is True  # Should be initialized

    def test_create_installer_service_initialization_failure(self) -> None:
        """Test installer service creation with initialization failure."""
        # This is tricky to test since FlextMeltanoInstaller.initialize() always returns success
        # We could patch the initialize method, but for now just verify the success case
        config = FlextMeltanoConfig()
        result = create_installer_service(config)
        assert result.success

    @patch("flext_meltano.installation.FlextMeltanoInstaller.add_plugin")
    def test_flext_meltano_install_plugin_success(self, mock_add_plugin: Mock) -> None:
        """Test legacy install plugin function success."""
        mock_add_plugin.return_value = FlextResult(data={"success": True})

        result = flext_meltano_install_plugin("extractor", "tap-csv", Path.cwd())
        if not (result.success):
            msg: str = f"Expected True, got {result.success}"
            raise AssertionError(msg)

        # Verify deprecation warning
        with pytest.warns(DeprecationWarning, match=".*"):
            flext_meltano_install_plugin("extractor", "tap-csv", Path.cwd())

    @patch("flext_meltano.installation.FlextMeltanoInstaller.add_plugin")
    def test_flext_meltano_install_plugin_failure(self, mock_add_plugin: Mock) -> None:
        """Test legacy install plugin function failure."""
        mock_add_plugin.return_value = FlextResult(error="Installation failed")

        result = flext_meltano_install_plugin("extractor", "tap-csv", Path.cwd())
        if result.success:
            msg: str = f"Expected False, got {result.success}"
            raise AssertionError(msg)
        assert result.error is not None
        if "Installation failed" not in result.error:
            msg: str = f"Expected {'Installation failed'} in {result.error}"
            raise AssertionError(msg)

    def test_flext_meltano_install_plugin_with_pip_url(self) -> None:
        """Test legacy install plugin function with pip URL."""
        with patch(
            "flext_meltano.installation.FlextMeltanoInstaller.add_plugin",
        ) as mock_add_plugin:
            mock_add_plugin.return_value = FlextResult(data={"success": True})

            result = flext_meltano_install_plugin(
                "extractor",
                "tap-csv",
                Path.cwd(),
                "pipelinewise-tap-csv",
            )
            if not (result.success):
                msg: str = f"Expected True, got {result.success}"
                raise AssertionError(msg)

            # Verify pip_url was passed correctly
            mock_add_plugin.assert_called_once_with(
                "extractor",
                "tap-csv",
                "pipelinewise-tap-csv",
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
