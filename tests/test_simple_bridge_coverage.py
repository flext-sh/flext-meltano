"""Test Coverage for Simple Bridge Module - Functional Tests.

**Purpose**: Comprehensive functional testing of simple_bridge.py module
**Scope**: Real functionality testing (not just imports) to achieve 95%+ coverage
**Focus**: FlextMeltanoBridge, create_flext_meltano_bridge, Go integration interface
**Target**: Increase coverage from 21% to 95%+

This module provides REAL functional tests that exercise the actual bridge
functionality and Go integration patterns.
"""

from __future__ import annotations

import json
import sys
import tempfile
from unittest.mock import Mock, patch

from flext_core import FlextResult

from flext_meltano import (
    FlextMeltanoBridge,
    FlextMeltanoConfig,
    create_flext_meltano_bridge,
)


class TestFlextMeltanoBridge:
    """Test FlextMeltanoBridge with real functionality."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.config = FlextMeltanoConfig(
            project_root=tempfile.mkdtemp(prefix="test_project_"),
            environment="test",
        )
        self.bridge = FlextMeltanoBridge(self.config)

    def test_bridge_initialization_with_config(self) -> None:
        """Test bridge initialization with custom config."""
        config = FlextMeltanoConfig(project_root=tempfile.mkdtemp(prefix="custom_"))
        bridge = FlextMeltanoBridge(config)

        assert bridge._config is not None
        assert "/custom_" in bridge._config.project_root
        assert bridge._executor is not None

    def test_bridge_initialization_without_config(self) -> None:
        """Test bridge initialization with default config."""
        bridge = FlextMeltanoBridge()

        assert bridge._config is not None
        assert bridge._executor is not None

    def test_bridge_initialization_with_none_config(self) -> None:
        """Test bridge initialization with None config."""
        bridge = FlextMeltanoBridge(None)

        assert bridge._config is not None
        assert bridge._executor is not None

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_get_version_success(self, mock_executor_class: type) -> None:
        """Test successful version retrieval."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor

        # Mock successful command execution
        mock_result = FlextResult.ok(
            {
                "stdout": "meltano 3.0.0",
                "stderr": "",
                "returncode": 0,
            },
        )
        mock_executor.run_command.return_value = mock_result

        # Create bridge and test
        bridge = FlextMeltanoBridge()
        result = bridge.get_version()

        assert result.success
        assert isinstance(result.data, dict)
        assert "meltano" in result.data
        assert "python" in result.data
        assert "flext_meltano" in result.data
        assert (
            result.data["python"]
            == f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )
        assert result.data["flext_meltano"] == "2.0.0-enterprise"

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_get_version_failure(self, mock_executor_class: type) -> None:
        """Test version retrieval failure."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor

        # Mock failed command execution
        mock_result = FlextResult.fail("Meltano not found")
        mock_executor.run_command.return_value = mock_result

        # Create bridge and test
        bridge = FlextMeltanoBridge()
        result = bridge.get_version()

        assert result.success  # Should still succeed with "unknown" version
        assert result.data["meltano"] == "unknown"

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_get_version_exception_handling(self, mock_executor_class: type) -> None:
        """Test version retrieval with exception."""
        # Mock the executor to raise an exception
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor
        mock_executor.run_command.side_effect = OSError("Command not found")

        # Create bridge and test
        bridge = FlextMeltanoBridge()
        result = bridge.get_version()

        assert not result.success
        assert "Failed to get version information" in result.error

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_list_plugins_success_with_json(self, mock_executor_class: type) -> None:
        """Test successful plugin listing with JSON response."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor

        # Mock successful command execution with JSON
        plugins_json = [
            {"name": "tap-csv", "type": "extractors"},
            {"name": "target-csv", "type": "loaders"},
        ]
        mock_result = FlextResult.ok(
            {
                "stdout": json.dumps(plugins_json),
                "stderr": "",
                "returncode": 0,
            },
        )
        mock_executor.run_command.return_value = mock_result

        # Create bridge and test
        bridge = FlextMeltanoBridge()
        result = bridge.list_plugins()

        assert result.success
        assert isinstance(result.data, list)
        assert len(result.data) == 2
        assert result.data[0]["name"] == "tap-csv"
        assert result.data[1]["name"] == "target-csv"

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_list_plugins_success_without_json(self, mock_executor_class: type) -> None:
        """Test successful plugin listing with non-JSON response."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor

        # Mock successful command execution with plain text
        mock_result = FlextResult.ok(
            {
                "stdout": "tap-csv\ntarget-csv\n",
                "stderr": "",
                "returncode": 0,
            },
        )
        mock_executor.run_command.return_value = mock_result

        # Create bridge and test
        bridge = FlextMeltanoBridge()
        result = bridge.list_plugins()

        assert result.success
        assert isinstance(result.data, list)
        assert len(result.data) == 2
        assert result.data[0]["name"] == "tap-csv"
        assert result.data[0]["type"] == "unknown"
        assert result.data[1]["name"] == "target-csv"

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_list_plugins_empty_response(self, mock_executor_class: type) -> None:
        """Test plugin listing with empty response."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor

        # Mock successful command execution with empty stdout
        mock_result = FlextResult.ok(
            {
                "stdout": "",
                "stderr": "",
                "returncode": 0,
            },
        )
        mock_executor.run_command.return_value = mock_result

        # Create bridge and test
        bridge = FlextMeltanoBridge()
        result = bridge.list_plugins()

        assert result.success
        assert isinstance(result.data, list)
        assert len(result.data) == 0

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_list_plugins_failure(self, mock_executor_class: type) -> None:
        """Test plugin listing failure."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor

        # Mock failed command execution
        mock_result = FlextResult.fail("Command failed")
        mock_executor.run_command.return_value = mock_result

        # Create bridge and test
        bridge = FlextMeltanoBridge()
        result = bridge.list_plugins()

        assert result.success  # Should return empty list on failure
        assert result.data == []

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_list_plugins_exception_handling(self, mock_executor_class: type) -> None:
        """Test plugin listing with exception."""
        # Mock the executor to raise an exception
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor
        mock_executor.run_command.side_effect = OSError("Command failed")

        # Create bridge and test
        bridge = FlextMeltanoBridge()
        result = bridge.list_plugins()

        assert not result.success
        assert "Failed to list plugins" in result.error

    def test_add_plugin_always_fails(self) -> None:
        """Test that add_plugin always fails (not implemented)."""
        result = self.bridge.add_plugin("extractor", "tap-csv")

        assert not result.success
        assert (
            "Plugin installation requires initialized Meltano project" in result.error
        )

    def test_add_plugin_with_variant(self) -> None:
        """Test add_plugin with variant parameter."""
        result = self.bridge.add_plugin(
            "extractor",
            "tap-postgres",
            variant="meltano",
        )

        assert not result.success
        assert (
            "installation service not initialized" in result.error
            or "Plugin installation requires initialized Meltano project"
            in result.error
        )

    def test_add_plugin_with_pip_url(self) -> None:
        """Test add_plugin with pip_url parameter."""
        result = self.bridge.add_plugin(
            "extractor",
            "tap-custom",
            pip_url="git+https://github.com/user/tap-custom.git",
        )

        assert not result.success
        assert (
            "Plugin installation requires initialized Meltano project" in result.error
        )

    def test_discover_catalog_always_fails(self) -> None:
        """Test that discover_catalog always fails (not implemented)."""
        result = self.bridge.discover_catalog("tap-csv")

        assert not result.success
        assert "Catalog discovery requires configured Meltano project" in result.error

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_run_pipeline_success(self, mock_executor_class: type) -> None:
        """Test successful pipeline execution."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor

        # Mock successful pipeline execution
        mock_result = FlextResult.ok(
            {
                "stdout": "Pipeline completed successfully",
                "stderr": "",
                "returncode": 0,
            },
        )
        mock_executor.run_command.return_value = mock_result

        # Create bridge and test
        bridge = FlextMeltanoBridge()
        result = bridge.run_pipeline("tap-csv", "target-csv")

        assert result.success
        assert isinstance(result.data, dict)
        assert result.data["status"] == "success"
        assert result.data["tap"] == "tap-csv"
        assert result.data["target"] == "target-csv"
        assert result.data["environment"] == "dev"
        assert result.data["job_id"] is None

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_run_pipeline_with_environment(self, mock_executor_class: type) -> None:
        """Test pipeline execution with environment parameter."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor

        # Mock successful pipeline execution
        mock_result = FlextResult.ok({"stdout": "Success", "returncode": 0})
        mock_executor.run_command.return_value = mock_result

        # Create bridge and test
        bridge = FlextMeltanoBridge()
        result = bridge.run_pipeline(
            "tap-postgres",
            "target-warehouse",
            environment="prod",
        )

        assert result.success
        assert result.data["environment"] == "prod"

        # Verify correct command was called
        expected_cmd = [
            "run",
            "--environment",
            "prod",
            "tap-postgres",
            "target-warehouse",
        ]
        mock_executor.run_command.assert_called_with(expected_cmd)

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_run_pipeline_with_job_id(self, mock_executor_class: type) -> None:
        """Test pipeline execution with job_id parameter."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor

        # Mock successful pipeline execution
        mock_result = FlextResult.ok({"stdout": "Success", "returncode": 0})
        mock_executor.run_command.return_value = mock_result

        # Create bridge and test
        bridge = FlextMeltanoBridge()
        result = bridge.run_pipeline(
            "tap-csv",
            "target-csv",
            job_id="job-12345",
        )

        assert result.success
        assert result.data["job_id"] == "job-12345"

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_run_pipeline_failure(self, mock_executor_class: type) -> None:
        """Test pipeline execution failure."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor

        # Mock failed pipeline execution
        mock_result = FlextResult.fail("Pipeline execution failed")
        mock_executor.run_command.return_value = mock_result

        # Create bridge and test
        bridge = FlextMeltanoBridge()
        result = bridge.run_pipeline("tap-csv", "target-csv")

        assert not result.success
        assert "Pipeline execution failed" in result.error

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_run_pipeline_exception_handling(self, mock_executor_class: type) -> None:
        """Test pipeline execution with exception."""
        # Mock the executor to raise an exception
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor
        mock_executor.run_command.side_effect = OSError("Command failed")

        # Create bridge and test
        bridge = FlextMeltanoBridge()
        result = bridge.run_pipeline("tap-csv", "target-csv")

        assert not result.success
        assert "Failed to run pipeline" in result.error

    def test_invoke_dbt_always_fails(self) -> None:
        """Test that invoke_dbt always fails (not implemented)."""
        result = self.bridge.invoke_dbt("run")

        assert not result.success
        assert (
            "DBT service not initialized" in result.error
            or "DBT operations require configured DBT project" in result.error
        )

    def test_invoke_dbt_with_args(self) -> None:
        """Test invoke_dbt with additional arguments."""
        result = self.bridge.invoke_dbt("run", "--models", "my_model")

        assert not result.success
        assert "DBT operations require configured DBT project" in result.error

    def test_invoke_dbt_with_kwargs(self) -> None:
        """Test invoke_dbt with keyword arguments."""
        result = self.bridge.invoke_dbt("test", environment="prod", full_refresh=True)

        assert not result.success
        assert "DBT operations require configured DBT project" in result.error


class TestCreateFlextMeltanoBridge:
    """Test create_flext_meltano_bridge factory function."""

    def test_create_bridge_without_config(self) -> None:
        """Test creating bridge without config."""
        bridge = create_flext_meltano_bridge()

        assert isinstance(bridge, FlextMeltanoBridge)
        assert bridge._config is not None
        assert bridge._executor is not None

    def test_create_bridge_with_config(self) -> None:
        """Test creating bridge with custom config."""
        config = FlextMeltanoConfig(
            project_root=tempfile.mkdtemp(prefix="custom_project_"),
            environment="production",
        )
        bridge = create_flext_meltano_bridge(config)

        assert isinstance(bridge, FlextMeltanoBridge)
        assert bridge._config is config
        assert "/custom_project_" in bridge._config.project_root
        assert bridge._config.environment == "production"

    def test_create_bridge_with_none_config(self) -> None:
        """Test creating bridge with None config."""
        bridge = create_flext_meltano_bridge(None)

        assert isinstance(bridge, FlextMeltanoBridge)
        assert bridge._config is not None
        assert bridge._executor is not None


class TestBridgeIntegration:
    """Integration tests for bridge functionality."""

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_complete_bridge_workflow(self, mock_executor_class: type) -> None:
        """Test complete bridge workflow simulation."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor

        # Create bridge
        bridge = FlextMeltanoBridge()

        # Test version retrieval
        version_result = FlextResult.ok(
            {
                "stdout": "meltano 3.0.0",
                "returncode": 0,
            },
        )
        mock_executor.run_command.return_value = version_result

        version = bridge.get_version()
        assert version.success
        assert "meltano" in version.data

        # Test plugin listing
        plugins_result = FlextResult.ok(
            {
                "stdout": json.dumps([{"name": "tap-csv", "type": "extractors"}]),
                "returncode": 0,
            },
        )
        mock_executor.run_command.return_value = plugins_result

        plugins = bridge.list_plugins()
        assert plugins.success
        assert len(plugins.data) == 1

        # Test pipeline execution
        pipeline_result = FlextResult.ok(
            {
                "stdout": "Pipeline completed",
                "returncode": 0,
            },
        )
        mock_executor.run_command.return_value = pipeline_result

        pipeline = bridge.run_pipeline("tap-csv", "target-csv")
        assert pipeline.success

    def test_bridge_json_serialization(self) -> None:
        """Test that bridge results are JSON serializable."""
        bridge = FlextMeltanoBridge()

        # Test operations that should always work (mocked or stubbed)
        with patch(
            "flext_meltano.simple_bridge.FlextMeltanoExecutor",
        ) as mock_executor_class:
            mock_executor = Mock()
            mock_executor_class.return_value = mock_executor

            # Mock version result
            mock_executor.run_command.return_value = FlextResult.ok(
                {
                    "stdout": "meltano 3.0.0",
                    "returncode": 0,
                },
            )

            version_result = bridge.get_version()

            # Test JSON serialization
            if version_result.success:
                json_data = json.dumps(version_result.data)
                assert isinstance(json_data, str)

                # Verify we can parse it back
                parsed = json.loads(json_data)
                assert isinstance(parsed, dict)

    def test_bridge_error_handling_patterns(self) -> None:
        """Test consistent error handling across bridge methods."""
        bridge = FlextMeltanoBridge()

        # Test operations that always fail
        add_result = bridge.add_plugin("extractor", "tap-test")
        catalog_result = bridge.discover_catalog("tap-test")
        dbt_result = bridge.invoke_dbt("run")

        # All should fail consistently
        assert not add_result.success
        assert not catalog_result.success
        assert not dbt_result.success

        # All should have error messages
        assert add_result.error is not None
        assert catalog_result.error is not None
        assert dbt_result.error is not None

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_bridge_command_building(self, mock_executor_class: type) -> None:
        """Test bridge command building for different operations."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor
        mock_executor.run_command.return_value = FlextResult.ok({"stdout": "Success"})

        bridge = FlextMeltanoBridge()

        # Test version command
        bridge.get_version()
        mock_executor.run_command.assert_called_with(["--version"])

        # Test list plugins command
        bridge.list_plugins()
        mock_executor.run_command.assert_called_with(["list", "--format=json"])

        # Test pipeline command without environment
        bridge.run_pipeline("tap-csv", "target-csv")
        mock_executor.run_command.assert_called_with(["run", "tap-csv", "target-csv"])

        # Test pipeline command with environment
        bridge.run_pipeline("tap-postgres", "target-postgres", environment="prod")
        mock_executor.run_command.assert_called_with(
            [
                "run",
                "--environment",
                "prod",
                "tap-postgres",
                "target-postgres",
            ],
        )


class TestBridgeEdgeCases:
    """Test edge cases and error scenarios for bridge."""

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_version_with_invalid_stdout_type(self, mock_executor_class: type) -> None:
        """Test version handling with invalid stdout type."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor

        # Mock result with non-string stdout
        mock_result = FlextResult.ok(
            {
                "stdout": 123,  # Invalid type
                "returncode": 0,
            },
        )
        mock_executor.run_command.return_value = mock_result

        bridge = FlextMeltanoBridge()
        result = bridge.get_version()

        # Should still succeed with "unknown" version
        assert result.success
        assert result.data["meltano"] == "unknown"

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_plugins_with_invalid_json(self, mock_executor_class: type) -> None:
        """Test plugin listing with invalid JSON."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor

        # Mock result with invalid JSON
        mock_result = FlextResult.ok(
            {
                "stdout": "{invalid json}",
                "returncode": 0,
            },
        )
        mock_executor.run_command.return_value = mock_result

        bridge = FlextMeltanoBridge()
        result = bridge.list_plugins()

        # Should fallback to simple parsing
        assert result.success
        assert len(result.data) == 1
        assert result.data[0]["name"] == "{invalid json}"
        assert result.data[0]["type"] == "unknown"

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_plugins_with_missing_stdout(self, mock_executor_class: type) -> None:
        """Test plugin listing with missing stdout."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor

        # Mock result without stdout key
        mock_result = FlextResult.ok(
            {
                "returncode": 0,
            },
        )
        mock_executor.run_command.return_value = mock_result

        bridge = FlextMeltanoBridge()
        result = bridge.list_plugins()

        # Should return empty list
        assert result.success
        assert result.data == []

    def test_bridge_with_minimal_config(self) -> None:
        """Test bridge with minimal configuration."""
        config = FlextMeltanoConfig()  # Minimal config
        bridge = FlextMeltanoBridge(config)

        assert bridge._config is not None
        assert bridge._executor is not None

    @patch("flext_meltano.simple_bridge.FlextMeltanoExecutor")
    def test_pipeline_with_all_parameters(self, mock_executor_class: type) -> None:
        """Test pipeline execution with all parameters."""
        # Mock the executor
        mock_executor = Mock()
        mock_executor_class.return_value = mock_executor
        mock_executor.run_command.return_value = FlextResult.ok(
            {
                "stdout": "Success",
                "returncode": 0,
            },
        )

        bridge = FlextMeltanoBridge()
        result = bridge.run_pipeline(
            "tap-postgres",
            "target-warehouse",
            environment="production",
            job_id="job-abc123",
        )

        assert result.success
        assert result.data["tap"] == "tap-postgres"
        assert result.data["target"] == "target-warehouse"
        assert result.data["environment"] == "production"
        assert result.data["job_id"] == "job-abc123"
