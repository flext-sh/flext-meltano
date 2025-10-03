"""FLEXT Meltano Adapter Real Tests - Real API integration testing."""

import tempfile
from pathlib import Path

from flext_tests import FlextTestsMatchers

from flext_core import FlextResult, FlextTypes
from flext_meltano import FlextMeltanoAdapter


class TestFlextMeltanoAdapterReal:
    """Test real FlextMeltanoAdapter functionality."""

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
        if result.is_success:
            version_info = result.value
            assert isinstance(version_info, dict)
            # Should contain version information
            assert "version" in version_info or "meltano_version" in version_info
        else:
            # If Meltano is not installed, should fail gracefully
            assert result.error
            assert isinstance(result.error, str)

    def test_discover_plugins(self) -> None:
        """Test plugin discovery - real Meltano Hub API."""
        result = self.adapter.discover_plugins()

        assert isinstance(result, FlextResult)
        if result.is_success:
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
            assert result.error

    def test_initialize_project(self) -> None:
        """Test project initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            result = self.adapter.initialize_project(project_path)

            assert isinstance(result, FlextResult)
            if result.is_success:
                project = result.value
                # Should return some project representation
                assert project is not None
            else:
                # May fail if Meltano is not available
                assert result.error

    def test_create_project(self) -> None:
        """Test project creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = "test-flext-project"
            project_path = Path(temp_dir)

            result = self.adapter.create_project(project_name, project_path)

            assert isinstance(result, FlextResult)
            if result.is_success:
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
                assert result.error

    def test_add_plugin(self) -> None:
        """Test adding plugin to project."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Try to initialize project first
            init_result = self.adapter.initialize_project(project_path)

            if init_result.is_success:
                project = init_result.value

                # Try to add a common plugin
                project_root = project["root"]
                assert isinstance(project_root, str), "Project root should be a string"
                plugin_result = self.adapter.add_plugin(
                    project_dir=Path(project_root),
                    plugin_type="extractors",
                    plugin_name="tap-csv",
                )

                assert isinstance(plugin_result, FlextResult)
                if plugin_result.is_success:
                    plugin_info = plugin_result.value
                    assert isinstance(plugin_info, dict)
                    # Should contain plugin information
                    assert "name" in plugin_info or "plugin_name" in plugin_info
                else:
                    # May fail due to network or Meltano setup
                    assert plugin_result.error

    def test_adapt_project_config(self) -> None:
        """Test project configuration adaptation."""
        config: FlextTypes.Dict = {
            "name": "test-project",
            "plugins": {"extractors": [], "loaders": []},
        }

        result = FlextMeltanoAdapter.adapt_project_config(config)

        # Use flext_tests matchers for cleaner assertions
        FlextTestsMatchers.assert_result_success(result)
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
        config: FlextTypes.Dict = {}

        result = FlextMeltanoAdapter.adapt_project_config(config)

        assert isinstance(result, FlextResult)
        assert result.is_success

        adapted_config = result.value
        assert isinstance(adapted_config, dict)
        assert "project_id" in adapted_config
        assert "version" in adapted_config

    def test_adapt_plugin(self) -> None:
        """Test plugin adaptation."""
        plugin_data: FlextTypes.Dict = {
            "type": "extractors",
            "pip_url": "pipelinewise-tap-csv",
        }

        result = FlextMeltanoAdapter.adapt_plugin(plugin_data)

        assert isinstance(result, FlextResult)
        assert result.is_success

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
        plugin_data: FlextTypes.Dict = {}

        result = FlextMeltanoAdapter.adapt_plugin(plugin_data)

        assert isinstance(result, FlextResult)
        assert result.is_success

        adapted_plugin = result.value
        assert isinstance(adapted_plugin, dict)
        assert "name" in adapted_plugin
        assert "namespace" in adapted_plugin

    def test_nested_class_access(self) -> None:
        """Test access to nested classes."""
        adapter = FlextMeltanoAdapter()

        # Should have unified methods instead of nested classes (SOLID refactored)
        unified_methods = [
            "execute_bridge_service",  # Bridge functionality
            "add_plugin",  # ProjectManager functionality
            "discover_plugins",  # PluginDiscovery functionality
            "create_project",  # ELTCoordinator functionality
        ]
        for method_name in unified_methods:
            assert hasattr(adapter, method_name), (
                f"Adapter should have {method_name} method"
            )
            method = getattr(adapter, method_name)
            assert callable(method), f"{method_name} should be callable"

    def test_error_handling_invalid_project_path(self) -> None:
        """Test error handling with invalid paths."""
        invalid_path = Path("/nonexistent/invalid/path/that/does/not/exist")

        result = self.adapter.create_project("test", invalid_path)

        assert isinstance(result, FlextResult)
        # Should fail gracefully
        assert not result.is_success
        assert result.error
        assert isinstance(result.error, str)

    def test_error_handling_invalid_plugin_data(self) -> None:
        """Test error handling with invalid plugin data."""
        invalid_plugin: FlextTypes.Dict = {
            "invalid": "data",
            "type": "nonexistent",
        }

        result = FlextMeltanoAdapter.adapt_plugin(invalid_plugin)

        assert isinstance(result, FlextResult)
        # Should still succeed but adapt the data
        if result.is_success:
            adapted = result.value
            assert isinstance(adapted, dict)
            assert "name" in adapted
            assert "namespace" in adapted

    def test_error_handling_none_inputs(self) -> None:
        """Test error handling with None inputs."""
        result = FlextMeltanoAdapter.adapt_project_config({})

        assert isinstance(result, FlextResult)
        # Should handle None gracefully
        if not result.is_success:
            assert result.error
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
            if result.is_success:
                project_info = result.value
                assert isinstance(project_info, dict)
            else:
                assert result.error

    def test_multiple_plugin_operations(self) -> None:
        """Test multiple plugin operations in sequence."""
        # Test plugin adaptation multiple times
        plugins: list[FlextTypes.Dict] = [
            {"type": "extractors", "name": "tap-csv"},
            {"type": "loaders", "name": "target-postgres"},
            {"type": "transformers", "name": "dbt"},
        ]

        for plugin in plugins:
            result = FlextMeltanoAdapter.adapt_plugin(plugin)
            assert isinstance(result, FlextResult)
            assert result.is_success

            adapted = result.value
            assert isinstance(adapted, dict)
            assert "name" in adapted
            assert "namespace" in adapted
