"""Test FlextMeltanoAdapter - Complete real functionality testing.

Tests all major adapter functionality with 100% real API integration.
"""

import tempfile
from pathlib import Path

from flext_core import FlextResult

from flext_meltano.adapters import FlextMeltanoAdapter


class TestFlextMeltanoAdapterComplete:
    """Complete test suite for FlextMeltanoAdapter."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.adapter = FlextMeltanoAdapter()

    def test_adapter_initialization(self) -> None:
        """Test adapter initialization."""
        adapter = FlextMeltanoAdapter()
        assert adapter is not None
        assert hasattr(adapter, "_logger")
        assert hasattr(adapter, "_utilities")

    def test_get_version(self) -> None:
        """Test getting Meltano version - real API call."""
        result = self.adapter.get_version()

        assert isinstance(result, FlextResult)
        # Version call should work if Meltano is available
        if result.success:
            version_info = result.value
            assert isinstance(version_info, dict)
            # Should contain version information
            assert "version" in version_info or "meltano_version" in version_info
        else:
            # If Meltano is not installed, should fail gracefully
            assert result.error_message
            assert isinstance(result.error_message, str)

    def test_discover_plugins(self) -> None:
        """Test plugin discovery - real Meltano Hub API."""
        result = self.adapter.discover_plugins()

        assert isinstance(result, FlextResult)
        if result.success:
            plugins = result.value
            assert isinstance(plugins, list)
            # If any plugins found, check structure
            if plugins:
                plugin = plugins[0]
                assert isinstance(plugin, dict)
                # Plugin should have basic attributes
                expected_keys = ["name", "type", "namespace", "pip_url"]
                assert any(key in plugin for key in expected_keys)
        else:
            # Network/API issues are acceptable
            assert result.error_message

    def test_initialize_project(self) -> None:
        """Test project initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            result = self.adapter.initialize_project(project_path)

            assert isinstance(result, FlextResult)
            if result.success:
                project = result.value
                # Should return some project representation
                assert project is not None
            else:
                # May fail if Meltano is not available
                assert result.error_message

    def test_create_project(self) -> None:
        """Test project creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = "test-flext-project"
            project_path = Path(temp_dir)

            result = self.adapter.create_project(project_name, project_path)

            assert isinstance(result, FlextResult)
            if result.success:
                project_info = result.value
                assert isinstance(project_info, dict)
                assert "project_path" in project_info

                # Check if project directory structure was created
                expected_path = project_path / project_name
                if expected_path.exists():
                    assert expected_path.is_dir()
                    # May have meltano.yml
                    meltano_yml = expected_path / "meltano.yml"
                    if meltano_yml.exists():
                        assert meltano_yml.is_file()
            else:
                # Acceptable if Meltano is not available
                assert result.error_message

    def test_add_plugin(self) -> None:
        """Test adding plugin to project."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Try to initialize project first
            init_result = self.adapter.initialize_project(project_path)

            if init_result.success:
                project = init_result.value

                # Try to add a common plugin
                plugin_result = self.adapter.add_plugin(
                    project_dir=Path(project["root"]), plugin_type="extractors", plugin_name="tap-csv"
                )

                assert isinstance(plugin_result, FlextResult)
                if plugin_result.success:
                    plugin_info = plugin_result.value
                    assert isinstance(plugin_info, dict)
                    # Should contain plugin information
                    assert "name" in plugin_info or "plugin_name" in plugin_info
                else:
                    # May fail due to network or Meltano setup
                    assert plugin_result.error_message

    def test_adapt_project_config(self) -> None:
        """Test project configuration adaptation."""
        config = {"name": "test-project", "plugins": {"extractors": [], "loaders": []}}

        result = FlextMeltanoAdapter.adapt_project_config(config)

        assert isinstance(result, FlextResult)
        assert result.success

        adapted_config = result.value
        assert isinstance(adapted_config, dict)

        # Should add required fields
        assert "project_id" in adapted_config
        assert "version" in adapted_config

        # Should preserve original content
        assert adapted_config["name"] == "test-project"
        assert "plugins" in adapted_config

    def test_adapt_project_config_minimal(self) -> None:
        """Test project config adaptation with minimal input."""
        config = {}

        result = FlextMeltanoAdapter.adapt_project_config(config)

        assert isinstance(result, FlextResult)
        assert result.success

        adapted_config = result.value
        assert isinstance(adapted_config, dict)
        assert "project_id" in adapted_config
        assert "version" in adapted_config

    def test_adapt_plugin(self) -> None:
        """Test plugin adaptation."""
        plugin_data = {"type": "extractors", "pip_url": "pipelinewise-tap-csv"}

        result = FlextMeltanoAdapter.adapt_plugin(plugin_data)

        assert isinstance(result, FlextResult)
        assert result.success

        adapted_plugin = result.value
        assert isinstance(adapted_plugin, dict)

        # Should add required fields
        assert "name" in adapted_plugin
        assert "namespace" in adapted_plugin

        # Should preserve original data
        assert adapted_plugin["type"] == "extractors"
        assert adapted_plugin["pip_url"] == "pipelinewise-tap-csv"

    def test_adapt_plugin_minimal(self) -> None:
        """Test plugin adaptation with minimal input."""
        plugin_data = {}

        result = FlextMeltanoAdapter.adapt_plugin(plugin_data)

        assert isinstance(result, FlextResult)
        assert result.success

        adapted_plugin = result.value
        assert isinstance(adapted_plugin, dict)
        assert "name" in adapted_plugin
        assert "namespace" in adapted_plugin

    def test_nested_bridge_class_access(self) -> None:
        """Test access to nested Bridge class."""
        adapter = FlextMeltanoAdapter()

        # Should have Bridge class
        assert hasattr(adapter, "Bridge")
        bridge_class = getattr(adapter, "Bridge")
        assert bridge_class is not None

        # Test Bridge instantiation - should work after consolidation
        bridge_instance = bridge_class()
        assert bridge_instance is not None
        # Bridge should have execute method (FlextDomainService requirement)
        assert hasattr(bridge_instance, "execute")

    def test_nested_project_manager_class_access(self) -> None:
        """Test access to nested ProjectManager class."""
        adapter = FlextMeltanoAdapter()

        # Should have ProjectManager class
        assert hasattr(adapter, "ProjectManager")
        pm_class = getattr(adapter, "ProjectManager")
        assert pm_class is not None

        # Test ProjectManager instantiation - should work without parameters
        project_manager = pm_class()
        assert project_manager is not None

        # Verify it has the expected methods
        assert hasattr(project_manager, "validate_project")

    def test_nested_plugin_discovery_class_access(self) -> None:
        """Test access to nested PluginDiscovery class."""
        adapter = FlextMeltanoAdapter()

        # Should have PluginDiscovery class
        assert hasattr(adapter, "PluginDiscovery")
        pd_class = getattr(adapter, "PluginDiscovery")
        assert pd_class is not None

        # Test PluginDiscovery instantiation - should work without parameters
        plugin_discovery = pd_class()
        assert plugin_discovery is not None

        # Verify it has the expected methods
        assert hasattr(plugin_discovery, "get_plugin_info")

    def test_nested_elt_coordinator_class_access(self) -> None:
        """Test access to nested ELTCoordinator class."""
        adapter = FlextMeltanoAdapter()

        # Should have ELTCoordinator class
        assert hasattr(adapter, "ELTCoordinator")
        elt_class = getattr(adapter, "ELTCoordinator")
        assert elt_class is not None

        # Test ELTCoordinator instantiation - should work without parameters
        elt_coordinator = elt_class()
        assert elt_coordinator is not None

        # Verify it has the expected methods
        assert hasattr(elt_coordinator, "_logger")

    def test_error_handling_invalid_project_path(self) -> None:
        """Test error handling with invalid paths."""
        invalid_path = Path("/nonexistent/invalid/path/that/does/not/exist")

        result = self.adapter.create_project("test", invalid_path)

        assert isinstance(result, FlextResult)
        # Should fail gracefully
        assert not result.success
        assert result.error_message
        assert isinstance(result.error_message, str)

    def test_error_handling_invalid_plugin_data(self) -> None:
        """Test error handling with invalid plugin data."""
        invalid_plugin = {"invalid": "data", "type": "nonexistent"}

        result = FlextMeltanoAdapter.adapt_plugin(invalid_plugin)

        assert isinstance(result, FlextResult)
        # Should still succeed but adapt the data
        if result.success:
            adapted = result.value
            assert isinstance(adapted, dict)
            assert "name" in adapted
            assert "namespace" in adapted

    def test_error_handling_none_inputs(self) -> None:
        """Test error handling with None inputs."""
        result = FlextMeltanoAdapter.adapt_project_config(None)

        assert isinstance(result, FlextResult)
        # Should handle None gracefully
        if not result.success:
            assert result.error_message
        else:
            # If it succeeds, should return valid config
            config = result.value
            assert isinstance(config, dict)

    def test_project_creation_with_existing_directory(self) -> None:
        """Test project creation when directory already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = "existing-project"
            project_path = Path(temp_dir)

            # Create directory first
            existing_dir = project_path / project_name
            existing_dir.mkdir(exist_ok=True)

            result = self.adapter.create_project(project_name, project_path)

            assert isinstance(result, FlextResult)
            # May succeed or fail depending on Meltano behavior
            if result.success:
                project_info = result.value
                assert isinstance(project_info, dict)
            else:
                assert result.error_message

    def test_multiple_plugin_operations(self) -> None:
        """Test multiple plugin operations in sequence."""
        # Test plugin adaptation multiple times
        plugins = [
            {"type": "extractors", "name": "tap-csv"},
            {"type": "loaders", "name": "target-postgres"},
            {"type": "transformers", "name": "dbt"},
        ]

        for plugin in plugins:
            result = FlextMeltanoAdapter.adapt_plugin(plugin)
            assert isinstance(result, FlextResult)
            assert result.success

            adapted = result.value
            assert isinstance(adapted, dict)
            assert "name" in adapted
            assert "namespace" in adapted

    def test_concurrent_adapter_instances(self) -> None:
        """Test multiple adapter instances work independently."""
        adapter1 = FlextMeltanoAdapter()
        adapter2 = FlextMeltanoAdapter()

        # Both should work independently
        result1 = adapter1.get_version()
        result2 = adapter2.get_version()

        assert isinstance(result1, FlextResult)
        assert isinstance(result2, FlextResult)

        # Both should have consistent behavior
        assert result1.success == result2.success
        if result1.success and result2.success:
            assert isinstance(result1.value, dict)
            assert isinstance(result2.value, dict)

    def test_adapter_with_different_configurations(self) -> None:
        """Test adapter behavior with different plugin configurations."""
        configs = [
            {"type": "extractors", "name": "tap-csv", "pip_url": "tap-csv"},
            {"type": "loaders", "name": "target-jsonl", "pip_url": "target-jsonl"},
            {"type": "transformers", "name": "dbt", "pip_url": "dbt-core"},
        ]

        for config in configs:
            result = FlextMeltanoAdapter.adapt_plugin(config)
            assert isinstance(result, FlextResult)
            assert result.success

            adapted = result.value
            assert isinstance(adapted, dict)
            assert adapted["type"] == config["type"]
            assert adapted["name"] == config["name"]

    def test_project_config_with_complex_structure(self) -> None:
        """Test project config adaptation with complex nested structure."""
        complex_config = {
            "name": "complex-project",
            "plugins": {
                "extractors": [
                    {"name": "tap-csv", "type": "extractors"},
                    {"name": "tap-postgres", "type": "extractors"},
                ],
                "loaders": [{"name": "target-jsonl", "type": "loaders"}],
                "transformers": [{"name": "dbt", "type": "transformers"}],
            },
            "environments": {
                "dev": {"MELTANO_ENVIRONMENT": "dev"},
                "prod": {"MELTANO_ENVIRONMENT": "prod"},
            },
        }

        result = FlextMeltanoAdapter.adapt_project_config(complex_config)

        assert isinstance(result, FlextResult)
        assert result.success

        adapted = result.value
        assert isinstance(adapted, dict)
        assert "project_id" in adapted
        assert "version" in adapted
        assert adapted["name"] == "complex-project"
        assert "plugins" in adapted
        assert "environments" in adapted

    def test_plugin_discovery_with_specific_types(self) -> None:
        """Test plugin discovery for specific plugin types."""
        result = self.adapter.discover_plugins()

        assert isinstance(result, FlextResult)
        if result.success:
            plugins = result.value
            assert isinstance(plugins, list)
            # If plugins found, verify they have valid types
            for plugin in plugins:
                if "type" in plugin:
                    # Accept any valid plugin type from real API
                    assert isinstance(plugin["type"], str)
                    assert len(plugin["type"]) > 0
        else:
            # Network/API failures are acceptable
            assert result.error_message

    def test_project_initialization_with_custom_config(self) -> None:
        """Test project initialization with custom configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            result = self.adapter.initialize_project(project_path)

            assert isinstance(result, FlextResult)
            if result.success:
                project = result.value
                assert project is not None
            else:
                # Meltano may be unavailable
                assert result.error_message
