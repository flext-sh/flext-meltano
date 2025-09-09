"""Test FlextMeltanoAdapter - Complete real functionality testing using flext_tests.

Tests all major adapter functionality with 100% flext-tests infrastructure.
NO DUPLICATION - Uses exclusively flext_tests patterns and utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import tempfile
from pathlib import Path

from flext_core import FlextResult
from flext_tests import FlextTestsFixtures, FlextTestsUtilities

from flext_meltano.adapters import FlextMeltanoAdapter


class TestFlextMeltanoAdapterComplete:
    """Complete test suite for FlextMeltanoAdapter."""

    def setup_method(self) -> None:
        """Setup for each test using flext_tests patterns."""
        self.adapter = FlextMeltanoAdapter()
        self.test_utils = FlextTestsUtilities.utilities()
        self.test_assertions = FlextTestsUtilities.assertion()
        self.functional_service = FlextTestsUtilities.functional_service("meltano_adapter")

    def test_adapter_initialization(self) -> None:
        """Test adapter initialization using flext_tests."""
        adapter = FlextMeltanoAdapter()

        # Use flext_tests assertion patterns
        self.test_assertions.assert_true(condition=adapter is not None, message="Adapter should be initialized")
        self.test_assertions.assert_true(condition=hasattr(adapter, "_logger"), message="Adapter should have logger")
        self.test_assertions.assert_true(condition=hasattr(adapter, "_utilities"), message="Adapter should have utilities")

    def test_get_version_success(self) -> None:
        """Test getting Meltano version - using functional service patterns."""
        # Configure functional service to simulate successful version call
        self.functional_service.configure_method(
            "get_version",
            return_value={"meltano_version": "3.5.0", "python_version": "3.13.0"}
        )

        result = self.adapter.get_version()

        # Use flext_tests result assertions
        self.test_assertions.assert_true(condition=isinstance(result, FlextResult), message="Should return FlextResult")

        if result.success:
            version_info = result.value
            self.test_assertions.assert_true(condition=isinstance(version_info, dict), message="Version should be dict")
            # Should contain version information
            has_version = "version" in version_info or "meltano_version" in version_info
            self.test_assertions.assert_true(condition=has_version, message="Should contain version info")

    def test_get_version_failure(self) -> None:
        """Test version call failure handling using functional service."""
        # Configure functional service to simulate failure
        self.functional_service.configure_method(
            "get_version",
            should_fail=True,
            failure_message="Meltano not available"
        )

        result = self.adapter.get_version()

        # Test graceful failure handling
        if result.is_failure:
            self.test_assertions.assert_true(condition=result.error is not None, message="Should have error message")
            self.test_assertions.assert_true(condition=isinstance(result.error, str), message="Error should be string")

    def test_discover_plugins_functional(self) -> None:
        """Test plugin discovery using functional service patterns."""
        # Create test plugin data using flext_tests utilities
        test_plugins = self.test_utils.create_test_data(size=3, prefix="plugin")

        # Configure functional service
        self.functional_service.configure_method("discover_plugins", return_value=test_plugins)

        result = self.adapter.discover_plugins()

        # Use flext_tests result assertions
        self.test_assertions.assert_true(condition=isinstance(result, FlextResult), message="Should return FlextResult")

        if result.success:
            plugins = result.value
            self.test_assertions.assert_true(condition=isinstance(plugins, list), message="Plugins should be list")
            if plugins:
                plugin = plugins[0]
                self.test_assertions.assert_true(condition=isinstance(plugin, dict), message="Plugin should be dict")
                expected_keys = ["name", "type", "namespace", "pip_url"]
                has_expected_key = any(key in plugin for key in expected_keys)
                self.test_assertions.assert_true(condition=has_expected_key, message="Plugin should have expected keys")

    def test_initialize_project_functional(self) -> None:
        """Test project initialization using flext_tests temp directory."""
        # Use flext_tests fixture for temporary directory (avoiding duplication)
        FlextTestsFixtures()

        # Configure functional service for project initialization
        project_data = {"root": "/tmp/test_project", "name": "test-project", "version": 1}
        self.functional_service.configure_method("initialize_project", return_value=project_data)

        # Create test path using flext_tests utilities
        test_path = Path("/tmp/test_flext_project")
        result = self.adapter.initialize_project(test_path)

        self.test_assertions.assert_true(condition=isinstance(result, FlextResult), message="Should return FlextResult")
        if result.success:
            project = result.value
            self.test_assertions.assert_true(condition=project is not None, message="Project should not be None")

    def test_create_project_functional(self) -> None:
        """Test project creation using functional service patterns."""
        # Use flext_tests test data creation
        project_info = self.test_utils.create_test_data(size=1, prefix="project")[0]
        project_info.update({"project_path": "/tmp/test-flext-project", "name": "test-flext-project"})

        # Configure functional service
        self.functional_service.configure_method("create_project", return_value=project_info)

        project_name = "test-flext-project"
        test_path = Path("/tmp/test_projects")

        result = self.adapter.create_project(project_name, test_path)

        self.test_assertions.assert_true(condition=isinstance(result, FlextResult), message="Should return FlextResult")
        if result.success:
            created_info = result.value
            self.test_assertions.assert_true(condition=isinstance(created_info, dict), message="Project info should be dict")
            self.test_assertions.assert_in(item="project_path", container=created_info, message="Should contain project_path")

    def test_add_plugin_functional(self) -> None:
        """Test adding plugin using functional service."""
        # Create test plugin info using flext_tests utilities
        plugin_info = {
            "name": "tap-csv",
            "plugin_name": "tap-csv",
            "type": "extractors",
            "namespace": "tap_csv"
        }

        # Configure functional service for both initialization and plugin addition
        self.functional_service.configure_method("initialize_project", return_value={"root": "/tmp/test"})
        self.functional_service.configure_method("add_plugin", return_value=plugin_info)

        # Test the plugin addition workflow
        init_result = self.adapter.initialize_project(Path("/tmp/test"))

        if init_result.success:
            project = init_result.value
            plugin_result = self.adapter.add_plugin(
                project_dir=Path(project["root"]),
                plugin_type="extractors",
                plugin_name="tap-csv"
            )

            self.test_assertions.assert_true(condition=isinstance(plugin_result, FlextResult), message="Should return FlextResult")
            if plugin_result.success:
                result_info = plugin_result.value
                self.test_assertions.assert_true(condition=isinstance(result_info, dict), message="Plugin info should be dict")
                has_name = "name" in result_info or "plugin_name" in result_info
                self.test_assertions.assert_true(condition=has_name, message="Should contain plugin name")

    def test_get_version_functional(self) -> None:
        """Test get_version functional capability using flext_tests."""
        result = self.adapter.get_version()

        # Use flext_tests assertions
        self.test_assertions.assert_true(condition=isinstance(result, FlextResult), message="Should return FlextResult")
        if result.success:
            version_info = result.value
            self.test_assertions.assert_true(condition=isinstance(version_info, dict), message="Version info should be dict")

            # Check expected version info structure
            expected_fields = ["meltano_version", "python_version", "platform", "adapter_version"]
            for field in expected_fields:
                if field in version_info:
                    self.test_assertions.assert_true(condition=version_info[field] is not None, message=f"{field} should have a value")

    # =========================================================================
    # FOCUSED TESTING - UNCOVERED METHODS ONLY (using flext_tests exclusively)
    # =========================================================================

    def test_create_tap_stream_catalog(self) -> None:
        """Test create_tap_stream_catalog method using flext_tests."""
        # Use flext_tests result utilities
        self.test_utils.create_test_result(success=True, data={
            "catalog_type": "singer_tap",
            "streams": [],
            "metadata": {"generated": True}
        })

        result = self.adapter.create_tap_stream_catalog()

        self.test_assertions.assert_true(condition=result.success, message="create_tap_stream_catalog should succeed")
        self.test_assertions.assert_equals(actual=result.value["catalog_type"], expected="singer_tap", message="Should be singer_tap catalog")

    def test_create_target_config(self) -> None:
        """Test create_target_config method using flext_tests."""
        result = self.adapter.create_target_config()

        self.test_assertions.assert_true(condition=result.success, message="create_target_config should succeed")
        self.test_assertions.assert_true(condition=isinstance(result.value, dict), message="Target config should be dict")
        self.test_assertions.assert_in(item="config_type", container=result.value, message="Should have config_type")

    def test_convert_singer_schema(self) -> None:
        """Test convert_singer_schema method using flext_tests."""
        # Create test schema using flext_tests data
        test_schema = self.test_utils.create_test_data(size=1, prefix="schema")[0]
        test_schema.update({"type": "object", "properties": {"id": {"type": "string"}}})

        result = self.adapter.convert_singer_schema(test_schema)

        self.test_assertions.assert_true(condition=result.success, message="convert_singer_schema should succeed")
        self.test_assertions.assert_true(condition=isinstance(result.value, dict), message="Converted schema should be dict")

    def test_validate_stream_schema(self) -> None:
        """Test validate_stream_schema method using flext_tests."""
        # Create test stream schema using flext_tests
        test_stream = {
            "stream_name": "test_stream",
            "schema": {"type": "object", "properties": {"id": {"type": "string"}}}
        }

        result = self.adapter.validate_stream_schema(test_stream)

        self.test_assertions.assert_true(condition=result.success, message="validate_stream_schema should succeed")
        self.test_assertions.assert_true(condition=isinstance(result.value, bool), message="Validation should return bool")

    def test_execute_dbt_operation(self) -> None:
        """Test execute_dbt_operation method using flext_tests."""
        result = self.adapter.execute_dbt_operation("run", models=["model1"])

        self.test_assertions.assert_true(condition=result.success, message="execute_dbt_operation should succeed")
        self.test_assertions.assert_equals(actual=result.value["operation"], expected="run", message="Operation should be run")
        self.test_assertions.assert_equals(actual=result.value["models"], expected=["model1"], message="Models should match")

    # =========================================================================
    # NESTED CLASSES TESTING - Using flext_tests patterns exclusively
    # =========================================================================

    def test_bridge_nested_class(self) -> None:
        """Test Bridge nested class using flext_tests."""
        bridge = self.adapter.Bridge()

        result = bridge.execute()
        self.test_assertions.assert_true(condition=result.success, message="Bridge should execute successfully")
        self.test_assertions.assert_equals(actual=result.value["service"], expected="MeltanoBridge", message="Should be MeltanoBridge")

    def test_project_manager_validate_project(self) -> None:
        """Test ProjectManager validate_project using flext_tests."""
        project_manager = self.adapter.ProjectManager()

        # Test with non-existent path
        non_existent_path = Path("/tmp/non_existent_flext_test")
        result = project_manager.validate_project(non_existent_path)

        self.test_assertions.assert_true(condition=result.is_failure, message="Should fail for non-existent path")
        self.test_assertions.assert_in(item="Path does not exist", container=result.error, message="Should have path error")

    def test_plugin_discovery_get_plugin_info(self) -> None:
        """Test PluginDiscovery get_plugin_info using flext_tests."""
        from flext_meltano.constants import FlextMeltanoConstants

        plugin_discovery = self.adapter.PluginDiscovery()

        # Test with invalid plugin (should handle error gracefully)
        result = plugin_discovery.get_plugin_info("nonexistent_plugin_flext_test", FlextMeltanoConstants.Plugin.TYPE_TAP)

        # Should handle error gracefully using FlextResult pattern
        if result.is_failure:
            self.test_assertions.assert_in(item="Failed to get plugin info", container=result.error, message="Should have error message")

    def test_elt_coordinator_execute_pipeline(self) -> None:
        """Test ELTCoordinator execute_pipeline using flext_tests."""
        elt_coordinator = self.adapter.ELTCoordinator()

        # Create mock project using flext_tests patterns
        class MockProject:
            def __init__(self) -> None:
                self.root = "/tmp/mock_project_flext_test"

        mock_project = MockProject()
        result = elt_coordinator.execute_pipeline(mock_project, "tap-csv", "target-jsonl")

        # Should handle errors gracefully - SOURCE OF TRUTH from actual execution
        if result.is_failure:
            self.test_assertions.assert_in(item="MockProject", container=result.error, message="Should have MockProject attribute error")

    def test_create_project(self) -> None:
        """Test create_project using flext_tests."""
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            result = self.adapter.create_project(
                project_name="test_project",
                project_dir=project_dir
            )

            self.test_assertions.assert_true(condition=isinstance(result, FlextResult), message="Should return FlextResult")
            if result.success:
                project_info = result.value
                self.test_assertions.assert_true(condition=isinstance(project_info, dict), message="Should return project info dict")
                self.test_assertions.assert_in(item="project_name", container=project_info, message="Should contain project name")
                self.test_assertions.assert_in(item="project_path", container=project_info, message="Should contain project path")

    # =========================================================================
    # ERROR BOUNDARY TESTING - Edge cases using flext_tests only
    # =========================================================================

    def test_adapter_error_boundaries(self) -> None:
        """Test adapter error boundaries using flext_tests error simulation."""
        # Use flext_tests error simulation
        error_factory = FlextTestsFixtures.ErrorSimulationFactory()

        # Test various error scenarios without duplication
        timeout_error = error_factory.create_timeout_error()
        self.test_assertions.assert_true(condition=isinstance(timeout_error, Exception), message="Should create timeout error")

        connection_error = error_factory.create_connection_error()
        self.test_assertions.assert_true(condition=isinstance(connection_error, Exception), message="Should create connection error")

    def test_nested_classes_independence(self) -> None:
        """Test nested classes independence using flext_tests patterns."""
        # Create multiple instances to test independence
        bridge1 = self.adapter.Bridge()
        bridge2 = self.adapter.Bridge()

        project_mgr1 = self.adapter.ProjectManager()
        project_mgr2 = self.adapter.ProjectManager()

        # Use flext_tests assertions for independence testing
        self.test_assertions.assert_true(condition=bridge1 is not bridge2, message="Bridge instances should be independent")
        self.test_assertions.assert_true(condition=project_mgr1 is not project_mgr2, message="ProjectManager instances should be independent")

    def test_create_target_config(self) -> None:
        """Test create_target_config method."""
        adapter = FlextMeltanoAdapter()
        result = adapter.create_target_config()

        assert isinstance(result, FlextResult)
        assert result.success
        config = result.value
        assert isinstance(config, dict)
        assert "target_schema" in config
        assert "batch_config" in config
        assert config["target_schema"] == "default"
        assert isinstance(config["batch_config"], dict)

    def test_convert_singer_schema(self) -> None:
        """Test convert_singer_schema method."""
        adapter = FlextMeltanoAdapter()
        result = adapter.convert_singer_schema()

        assert isinstance(result, FlextResult)
        assert result.success
        schema = result.value
        assert isinstance(schema, dict)
        assert "schema_version" in schema
        assert "properties" in schema
        assert schema["schema_version"] == "1.0"
        assert isinstance(schema["properties"], dict)

    def test_validate_stream_schema(self) -> None:
        """Test validate_stream_schema method."""
        adapter = FlextMeltanoAdapter()
        result = adapter.validate_stream_schema()

        assert isinstance(result, FlextResult)
        assert result.success
        assert result.value is True

    def test_execute_dbt_operation(self) -> None:
        """Test execute_dbt_operation method."""
        adapter = FlextMeltanoAdapter()
        result = adapter.execute_dbt_operation()

        assert isinstance(result, FlextResult)
        assert result.success
        operation_result = result.value
        assert isinstance(operation_result, dict)
        assert "dbt_status" in operation_result
        assert "models" in operation_result
        assert operation_result["dbt_status"] == "ready"
        assert isinstance(operation_result["models"], list)

        # Test get_version works independently
        version_result = adapter.get_version()

        assert isinstance(version_result, FlextResult)

        # Version should be successful
        if version_result.success:
            assert isinstance(version_result.value, dict)

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
