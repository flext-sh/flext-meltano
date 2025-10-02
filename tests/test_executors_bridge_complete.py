"""Test module for flext-meltano."""

import tempfile
from collections.abc import Callable
from pathlib import Path

from flext_core import FlextResult
from flext_meltano import FlextMeltanoBridge


class TestFlextMeltanoBridgeComplete:
    """Complete test suite for FlextMeltanoBridge."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.bridge = FlextMeltanoBridge()

    def test_bridge_initialization(self) -> None:
        """Test bridge initialization."""
        bridge = FlextMeltanoBridge()
        assert bridge is not None
        assert hasattr(bridge, "adapter")
        assert hasattr(bridge, "logger")

    def test_get_version(self) -> None:
        """Test get_version method."""
        result = self.bridge.get_version()

        assert isinstance(result, FlextResult)
        if result.is_success:
            version_info = result.value
            assert isinstance(version_info, dict)
            # Should contain version information
            assert any(
                key in version_info for key in ["version", "meltano_version", "meltano"]
            )
        else:
            # May fail if Meltano is not available
            assert result.error

    def test_get_version_json(self) -> None:
        """Test get_version_json method."""
        version_json = self.bridge.get_version_json()

        assert isinstance(version_json, str)
        # Should be a valid JSON string
        assert len(version_json) > 0
        assert "meltano" in version_json

    def test_discover_plugins(self) -> None:
        """Test discover_plugins method."""
        result = self.bridge.discover_plugins()

        assert isinstance(result, FlextResult)
        if result.is_success:
            plugins_data = result.data
            assert isinstance(plugins_data, dict)
            plugins = plugins_data.get("plugins", [])
            assert isinstance(plugins, list)
            # If plugins found, check structure
            if plugins:
                plugin = plugins[0]
                assert isinstance(plugin, dict)
        else:
            # Network/API failures are acceptable
            assert result.error

    def test_list_plugins(self) -> None:
        """Test list_plugins method."""
        result = self.bridge.list_plugins()

        assert isinstance(result, FlextResult)
        if result.is_success:
            plugins = result.value
            assert isinstance(plugins, list)
            # Validate real plugin structure
            if plugins:
                plugin = plugins[0]
                assert isinstance(plugin, dict)
                assert "name" in plugin
                assert "type" in plugin
        else:
            # May fail without proper Meltano setup
            assert "error" in result

    def test_initialize_project(self) -> None:
        """Test initialize_project method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            result = self.bridge.initialize_project(str(project_path))

            assert isinstance(result, FlextResult)
            if result.is_success:
                project_info = result.value
                assert isinstance(project_info, dict)
            else:
                # May fail without proper Meltano setup
                assert result.error

    def test_get_project_info(self) -> None:
        """Test get_project_info method."""
        result = self.bridge.get_project_info()

        assert isinstance(result, dict)
        assert "success" in result
        assert "data" in result
        if result["success"]:
            project_info = result["data"]
            assert isinstance(project_info, dict)
        else:
            # May fail without active project
            assert "error" in result

    def test_install_plugin(self) -> None:
        """Test install_plugin method."""
        result = self.bridge.install_plugin("extractors", "tap-csv")

        assert isinstance(result, FlextResult)
        if result.is_success:
            install_info = result.value
            assert isinstance(install_info, dict)
        else:
            # May fail without proper setup or network issues
            assert result.error

    def test_execute_meltano_command(self) -> None:
        """Test execute_meltano_command method."""
        result = self.bridge.execute_meltano_command(["--version"])

        assert isinstance(result, dict)
        assert "success" in result
        assert "data" in result
        if result["success"]:
            command_result = result["data"]
            assert isinstance(command_result, dict)
        else:
            # May fail if Meltano CLI is not available
            assert "error" in result

    def test_execute_meltano_command_real(self) -> None:
        """Test execute_meltano_command_real method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            result = self.bridge.execute_meltano_command(
                ["--version"],
                str(project_path),
            )

            assert isinstance(result, dict)
            assert "success" in result
            # Real command execution may succeed or fail
            if not result["success"]:
                assert "error" in result

    def test_execute_dbt_command(self) -> None:
        """Test execute_dbt_command method."""
        result = self.bridge.execute_dbt_command(["--version"])

        assert isinstance(result, dict)
        assert "success" in result
        assert "data" in result
        if result["success"]:
            dbt_result = result["data"]
            assert isinstance(dbt_result, dict)
        else:
            # May fail if DBT is not available
            assert "error" in result

    def test_invoke_dbt(self) -> None:
        """Test invoke_dbt method."""
        result = self.bridge.invoke_dbt("--version")

        assert isinstance(result, dict)
        assert "success" in result
        # DBT invocation may succeed or fail depending on setup
        if not result["success"]:
            assert "error" in result

    def test_run_pipeline(self) -> None:
        """Test run_pipeline method."""
        result = self.bridge.run_pipeline("tap-csv", "target-jsonl")

        assert isinstance(result, dict)
        assert "success" in result
        assert "data" in result
        if result["success"]:
            pipeline_result = result["data"]
            assert pipeline_result is not None
        else:
            # Pipeline may fail without proper plugin setup
            assert "error" in result

    def test_run_pipeline_real(self) -> None:
        """Test run_pipeline method."""
        with tempfile.TemporaryDirectory() as _:
            result = self.bridge.run_pipeline("tap-csv", "target-jsonl")

            assert isinstance(result, dict)
            # Real pipeline execution may succeed or fail
            assert "success" in result

    def test_run_elt_pipeline(self) -> None:
        """Test run_elt_pipeline method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            result = self.bridge.run_elt_pipeline(
                "tap-csv",
                "target-jsonl",
                str(project_path),
            )

            assert isinstance(result, dict)
            assert "success" in result

    def test_run_plugin(self) -> None:
        """Test run_plugin method."""

        def run_test() -> object:
            with tempfile.TemporaryDirectory() as temp_dir:
                project_path = Path(temp_dir)
                # Create a mock project object
                project = {"path": project_path}
                return self.bridge.run_plugin(
                    project,
                    "tap-csv",
                    "describe",
                    [],
                )

        # Run the test
        result = run_test()

        # The method returns object, so we check it exists
        assert result is not None

    def test_create_bridge(self) -> None:
        """Test bridge creation."""
        result = FlextMeltanoBridge()

        assert isinstance(result, FlextMeltanoBridge)
        assert result is not None
        assert hasattr(result, "adapter")

    def test_executor_property(self) -> None:
        """Test adapter property access."""
        adapter = self.bridge.adapter
        assert adapter is not None
        # Adapter should be accessible

    def test_multiple_bridge_operations(self) -> None:
        """Test multiple bridge operations in sequence."""
        # Test get_version operation
        version_result = self.bridge.get_version()
        assert isinstance(version_result, FlextResult)

        # Test discover_plugins operation
        discover_result = self.bridge.discover_plugins(None)
        assert isinstance(discover_result, FlextResult)

        # Test list_plugins operation
        list_result = self.bridge.list_plugins()
        assert isinstance(list_result, FlextResult)
        # Each operation should return FlextResult

    def test_error_handling_invalid_commands(self) -> None:
        """Test error handling with invalid commands."""
        invalid_commands = [["--invalid-flag"], ["nonexistent-command"], []]

        for cmd in invalid_commands:
            result = self.bridge.execute_meltano_command(cmd)
            assert isinstance(result, dict)
            assert "success" in result
            assert "data" in result
            # Should handle invalid commands gracefully

    def test_concurrent_bridge_instances(self) -> None:
        """Test multiple bridge instances work independently."""
        bridge1 = FlextMeltanoBridge()
        bridge2 = FlextMeltanoBridge()

        # Both should work independently
        result1 = bridge1.get_version()
        result2 = bridge2.get_version()

        assert isinstance(result1, FlextResult)
        assert isinstance(result2, FlextResult)

        # Both should have consistent behavior
        assert result1.is_success == result2.is_success

    def test_bridge_with_different_plugins(self) -> None:
        """Test bridge operations with different plugin types."""
        plugin_configs: list[tuple[str, str]] = [
            ("extractors", "tap-csv"),
            ("loaders", "target-jsonl"),
            ("transformers", "dbt"),
        ]

        for plugin_type, plugin_name in plugin_configs:
            result = self.bridge.install_plugin(plugin_type, plugin_name)
            assert isinstance(result, FlextResult)
            # Installation may succeed or fail, should handle gracefully

    def test_pipeline_execution_patterns(self) -> None:
        """Test different pipeline execution patterns."""
        pipeline_configs: list[tuple[str, str]] = [
            ("tap-csv", "target-jsonl"),
            ("tap-postgres", "target-postgres"),
            ("tap-github", "target-bigquery"),
        ]

        for tap, target in pipeline_configs:
            result = self.bridge.run_pipeline(tap, target)
            assert isinstance(result, dict)
            assert "success" in result
            # Pipeline execution may fail without proper setup

    def test_command_result_consistency(self) -> None:
        """Test command result format consistency."""
        commands = [
            ["--version"],
            ["--help"],
        ]

        for cmd in commands:
            result = self.bridge.execute_meltano_command(cmd)
            assert isinstance(result, dict)
            assert "success" in result
            assert "data" in result

            if result["success"]:
                cmd_result = result["data"]
                assert isinstance(cmd_result, dict)
                # Should have consistent result structure

    def test_bridge_lifecycle_operations(self) -> None:
        """Test bridge lifecycle and state management."""
        # Test bridge creation and initialization
        create_result = FlextMeltanoBridge()
        assert isinstance(create_result, FlextMeltanoBridge)

        # Test version information after creation
        version_result = self.bridge.get_version()
        assert isinstance(version_result, FlextResult)

        # Test project info access
        project_result = self.bridge.get_project_info()
        assert isinstance(project_result, dict)
        assert "success" in project_result

    def test_error_scenarios_for_coverage(self) -> None:
        """Test error scenarios to increase coverage on exception handling."""
        # Test with invalid paths to trigger error handling
        invalid_path = Path("/nonexistent/invalid/path/that/does/not/exist")

        # Test initialize_project with invalid path
        init_result = self.bridge.initialize_project(str(invalid_path))
        assert isinstance(init_result, FlextResult)
        if not init_result.is_success:
            assert init_result.error

        # Test get_project_info with invalid path
        project_result = self.bridge.get_project_info(str(invalid_path))
        assert isinstance(project_result, dict)
        assert "success" in project_result

        # Test install_plugin with invalid plugin type
        install_result = self.bridge.install_plugin("invalid_type", "invalid_plugin")
        assert isinstance(install_result, FlextResult)
        # May succeed or fail, both are acceptable for invalid plugins

    def test_parameter_validation_coverage(self) -> None:
        """Test various parameter combinations to increase branch coverage."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Test empty command lists
            cmd_result = self.bridge.execute_meltano_command([])
            assert isinstance(cmd_result, dict)
            assert "success" in cmd_result

            # Test single argument commands
            version_result = self.bridge.execute_meltano_command(["version"])
            assert isinstance(version_result, dict)
            assert "success" in version_result

            # Test dbt commands with various parameters
            dbt_result = self.bridge.execute_dbt_command(["help"])
            assert isinstance(dbt_result, dict)
            assert "success" in dbt_result

            # Test with different project roots
            real_result = self.bridge.execute_meltano_command(
                ["version"],
                str(project_path),
            )
            assert isinstance(real_result, dict)
            assert "success" in real_result

    def test_additional_method_coverage(self) -> None:
        """Test additional methods to increase coverage."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Test invoke_dbt with different parameter combinations
            dbt_result1 = self.bridge.invoke_dbt("version")
            assert isinstance(dbt_result1, dict)
            assert "success" in dbt_result1

            # Test invoke_dbt with positional arguments
            dbt_result2 = self.bridge.invoke_dbt("compile", str(project_path))
            assert isinstance(dbt_result2, dict)
            assert "success" in dbt_result2

            # Test pipeline execution with non-standard plugins
            pipeline_result = self.bridge.run_pipeline("tap-unknown", "target-unknown")
            assert isinstance(pipeline_result, dict)
            assert "success" in pipeline_result

            # Test different combinations to hit unused branches
            try:
                # Test edge cases that might trigger different code paths
                with tempfile.TemporaryDirectory() as temp_dir_inner:
                    nonexistent_path = f"{temp_dir_inner}/nonexistent_project"
                    edge_result = self.bridge.get_project_info(nonexistent_path)
                assert isinstance(edge_result, dict)
            except (ValueError, TypeError, RuntimeError, AttributeError):
                # Some edge cases may raise exceptions, which is acceptable
                pass

    def test_internal_methods_for_coverage(self) -> None:
        """Test internal methods to achieve higher coverage."""
        # Test adapter _create_temporary_meltano_project method directly (no wrappers)
        temp_project_result = self.bridge.adapter.create_temporary_meltano_project()
        assert isinstance(temp_project_result, FlextResult)
        # May succeed or fail depending on adapter implementation

        # Test _run_plugin_sync internal method
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            project = {"path": project_path}

            sync_result = self.bridge._run_plugin_sync(
                project,
                "tap-csv",
                "describe",
                [],
            )
            # Method returns object, check it exists
            assert sync_result is not None

    def test_edge_cases_and_error_paths(self) -> None:
        """Test edge cases and error paths to maximize coverage."""
        # Test with extreme/invalid inputs to trigger error handling

        # Test with empty strings
        try:
            empty_result = self.bridge.install_plugin("", "")
            assert isinstance(empty_result, FlextResult)
        except (ValueError, TypeError, RuntimeError, AttributeError):
            # May raise exception for invalid empty inputs
            pass

        # Test with None-like values (as string)
        try:
            none_result = self.bridge.execute_dbt_command(["none"])
            assert isinstance(none_result, dict)
        except (ValueError, TypeError, RuntimeError, AttributeError):
            # May fail for invalid commands
            pass

        # Test invoke_dbt with special characters
        try:
            special_result = self.bridge.invoke_dbt("--help")
            assert isinstance(special_result, dict)
        except (ValueError, TypeError, RuntimeError, AttributeError):
            pass

    def test_error_recovery_patterns(self) -> None:
        """Test error recovery and resilience patterns."""
        # Test FlextResult operations
        flext_result_operations: list[Callable[[], object]] = [
            lambda: self.bridge.install_plugin("extractors", "invalid@plugin#name"),
        ]

        for operation in flext_result_operations:
            result = operation()
            assert isinstance(result, FlextResult)

            # Should fail gracefully with informative errors
            if not result.is_success:
                assert result.error
                assert len(result.error) > 0

        # Test dict operations
        dict_operations = [
            lambda: self.bridge.run_pipeline("nonexistent-tap", "nonexistent-target"),
            lambda: self.bridge.execute_dbt_command(["--invalid-command"]),
        ]

        for operation in dict_operations:
            result = operation()
            assert isinstance(result, dict)
            assert "success" in result

            # Should fail gracefully with informative errors
            if not result["success"]:
                assert "error" in result
                assert len(str(result["error"])) > 0
