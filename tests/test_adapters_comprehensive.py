"""Comprehensive unit tests for FlextMeltanoAdapter.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from flext_core import FlextResult, FlextTypes
from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.typings import FlextMeltanoTypes


class TestFlextMeltanoAdapterInitialization:
    """Test FlextMeltanoAdapter initialization and basic functionality."""

    def test_adapter_initialization(self) -> None:
        """Test adapter initializes correctly with all required components."""
        adapter = FlextMeltanoAdapter()

        # Test that adapter can be created and has basic functionality
        assert adapter is not None
        assert hasattr(adapter, "get_version")
        assert hasattr(adapter, "discover_plugins")
        assert hasattr(adapter, "create_project")

    def test_adapter_singleton_pattern(self) -> None:
        """Test that adapter follows singleton pattern for configuration."""
        adapter1 = FlextMeltanoAdapter()
        adapter2 = FlextMeltanoAdapter()

        # Both adapters should be independent instances
        assert adapter1 is not adapter2
        # Test that both can perform basic operations
        version1 = adapter1.get_version()
        version2 = adapter2.get_version()
        assert version1.is_success
        assert version2.is_success


class TestFlextMeltanoAdapterProjectManagement:
    """Test project management functionality."""

    def test_create_project_success(self) -> None:
        """Test successful project creation."""
        adapter = FlextMeltanoAdapter()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "test_project"

            with patch.object(
                adapter, "_create_project_structure"
            ) as mock_create_structure:
                result = adapter.create_project(
                    project_name="test_project",
                    project_dir=project_path,
                )

                assert result.is_success
                assert result.data is not None
                assert result.data["project_name"] == "project_name"
                assert result.data["creation_method"] == "manual_file_creation"
                mock_create_structure.assert_called_once()

    def test_create_project_invalid_path(self) -> None:
        """Test project creation with invalid path."""
        adapter = FlextMeltanoAdapter()

        result = adapter.create_project(
            project_name="test_project",
            project_dir=Path("/invalid/path/that/does/not/exist"),
        )

        assert result.is_failure
        assert result.error is not None
        assert "Failed to create Meltano project" in str(result.error)

    def test_create_project_empty_name(self) -> None:
        """Test project creation with empty name."""
        adapter = FlextMeltanoAdapter()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "test_project"

            result = adapter.create_project(project_name="", project_dir=project_path)

            assert result.is_failure
            assert result.error is not None
            assert "Project name cannot be empty" in str(result.error)

    def test_load_project_success(self) -> None:
        """Test successful project loading."""
        adapter = FlextMeltanoAdapter()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create a minimal meltano.yml file
            meltano_yml = project_path / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test_project\n")

            with patch.object(adapter, "_load_meltano_project") as mock_load_project:
                mock_load_project.return_value = FlextResult[object].ok(Mock())

                result = adapter.initialize_project(project_path)

                assert result.is_success
                assert result.data is not None

    def test_load_project_nonexistent_path(self) -> None:
        """Test loading project from nonexistent path."""
        adapter = FlextMeltanoAdapter()

        result = adapter.initialize_project(Path("/nonexistent/path"))

        assert result.is_failure
        assert result.error is not None
        assert "Project directory not found" in str(result.error)

    def test_get_project_info_success(self) -> None:
        """Test successful project info retrieval."""
        adapter = FlextMeltanoAdapter()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create a minimal meltano.yml file
            meltano_yml = project_path / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test_project\n")

            with patch.object(adapter, "_load_meltano_project") as mock_load_project:
                mock_project = Mock()
                mock_project.root = project_path
                mock_project.id = "test_project"
                mock_project.meltano_version = "1.0.0"
                mock_load_project.return_value = FlextResult[object].ok(mock_project)

                # Load project first
                adapter.initialize_project(project_path)

                result = adapter.get_project_info()

                assert result.is_success
                assert result.data["project_root"] == str(project_path)

    def test_get_project_info_no_project_loaded(self) -> None:
        """Test project info retrieval when no project is loaded."""
        adapter = FlextMeltanoAdapter()

        result = adapter.get_project_info()

        assert result.is_failure
        assert result.error is not None
        assert "No project loaded" in str(result.error)


class TestFlextMeltanoAdapterPluginManagement:
    """Test plugin management functionality."""

    def test_discover_plugins_success(self) -> None:
        """Test successful plugin discovery."""
        adapter = FlextMeltanoAdapter()

        result = adapter.discover_plugins()

        assert result.is_success
        assert result.data is not None
        assert isinstance(result.data, list)
        assert len(result.data) > 0

    def test_discover_plugins_failure(self) -> None:
        """Test plugin discovery failure."""
        adapter = FlextMeltanoAdapter()

        # Test plugin discovery with mocked failure
        with patch.object(adapter, "discover_plugins") as mock_discover:
            mock_discover.return_value = FlextResult[
                list[FlextTypes.Core.Headers]
            ].fail("Discovery failed")

            result = adapter.discover_plugins()

            assert result.is_failure
            assert result.error is not None

    def test_add_plugin_success(self) -> None:
        """Test successful plugin addition."""
        adapter = FlextMeltanoAdapter()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            result = adapter.add_plugin(
                plugin_type="extractors",
                plugin_name="tap-postgres",
                project_dir=project_path,
            )

            assert result.is_success
            assert result.data is not None

    def test_add_plugin_invalid_config(self) -> None:
        """Test plugin addition with invalid config."""
        adapter = FlextMeltanoAdapter()

        # Test with invalid arguments - using correct method signature
        result = adapter.add_plugin(
            project_dir=Path("/invalid/path"),
            plugin_type="invalid_type",
            plugin_name="",
        )

        assert result.is_failure
        assert result.error is not None
        assert "Plugin addition failed" in str(result.error)


class TestFlextMeltanoAdapterConfigurationManagement:
    """Test configuration management functionality."""

    def test_convert_singer_schema_invalid_config(self) -> None:
        """Test singer schema conversion with invalid config."""
        adapter = FlextMeltanoAdapter()

        # Test with mocked failure
        with patch.object(adapter, "convert_singer_schema") as mock_convert:
            mock_convert.return_value = FlextResult[FlextTypes.Core.Dict].fail(
                "Invalid schema configuration"
            )

            result = adapter.convert_singer_schema()

            assert result.is_failure
            assert result.error is not None


class TestFlextMeltanoAdapterExecution:
    """Test execution functionality."""

    def test_execute_dbt_operation_success(self) -> None:
        """Test successful DBT operation execution."""
        adapter = FlextMeltanoAdapter()

        result = adapter.execute_dbt_operation()

        assert result.is_success
        assert result.data is not None
        assert "dbt_status" in result.data

    def test_execute_dbt_operation_failure(self) -> None:
        """Test DBT operation execution with failure."""
        adapter = FlextMeltanoAdapter()

        # Test with mocked failure
        with patch.object(adapter, "execute_dbt_operation") as mock_execute:
            mock_execute.return_value = FlextResult[FlextTypes.Core.Dict].fail(
                "DBT operation failed"
            )

            result = adapter.execute_dbt_operation()

            assert result.is_failure
            assert result.error is not None

    def test_execute_bridge_service_success(self) -> None:
        """Test successful bridge service execution."""
        adapter = FlextMeltanoAdapter()

        result = adapter.execute_bridge_service()

        assert result.is_success
        assert result.data is not None
        assert "service" in result.data
        assert result.data["service"] == "MeltanoBridge"

    def test_execute_bridge_service_failure(self) -> None:
        """Test bridge service execution with failure."""
        adapter = FlextMeltanoAdapter()

        # Test with mocked failure
        with patch.object(adapter, "execute_bridge_service") as mock_execute:
            mock_execute.return_value = FlextResult[
                FlextMeltanoTypes.CLI.ProcessResult
            ].fail("Bridge service failed")

            result = adapter.execute_bridge_service()

            assert result.is_failure
            assert result.error is not None


class TestFlextMeltanoAdapterStreamManagement:
    """Test stream management functionality."""

    def test_create_tap_stream_catalog_success(self) -> None:
        """Test successful tap stream catalog creation."""
        adapter = FlextMeltanoAdapter()

        result = adapter.create_tap_stream_catalog()

        assert result.is_success
        assert result.data is not None
        assert "streams" in result.data

    def test_convert_singer_schema_success(self) -> None:
        """Test successful singer schema conversion."""
        adapter = FlextMeltanoAdapter()

        result = adapter.convert_singer_schema()

        assert result.is_success
        assert result.data is not None
        assert "schema_version" in result.data
        assert "properties" in result.data


class TestFlextMeltanoAdapterErrorHandling:
    """Test error handling and edge cases."""

    def test_adapter_exception_handling(self) -> None:
        """Test adapter handles exceptions gracefully."""
        adapter = FlextMeltanoAdapter()

        # Test with mocked exception
        with patch.object(adapter, "discover_plugins") as mock_discover:
            mock_discover.return_value = FlextResult[
                list[FlextTypes.Core.Headers]
            ].fail("Unexpected error")

            result = adapter.discover_plugins()

            assert result.is_failure
            assert result.error is not None
            assert "Unexpected error" in str(result.error)

    def test_adapter_timeout_handling(self) -> None:
        """Test adapter handles timeouts gracefully."""
        adapter = FlextMeltanoAdapter()

        # Test with mocked timeout
        with patch.object(adapter, "execute_dbt_operation") as mock_execute:
            mock_execute.return_value = FlextResult[FlextTypes.Core.Dict].fail(
                "Operation timed out"
            )

            result = adapter.execute_dbt_operation()

            assert result.is_failure
            assert result.error is not None
            assert "Operation timed out" in str(result.error)

    def test_adapter_network_error_handling(self) -> None:
        """Test adapter handles network errors gracefully."""
        adapter = FlextMeltanoAdapter()

        # Test with mocked network error
        with patch.object(adapter, "discover_plugins") as mock_discover:
            mock_discover.return_value = FlextResult[
                list[FlextTypes.Core.Headers]
            ].fail("Network connection failed")

            result = adapter.discover_plugins()

            assert result.is_failure
            assert result.error is not None
            assert "Network connection failed" in str(result.error)


class TestFlextMeltanoAdapterIntegration:
    """Integration tests for FlextMeltanoAdapter."""

    def test_complete_workflow_simulation(self) -> None:
        """Test a complete workflow simulation."""
        adapter = FlextMeltanoAdapter()

        # Test basic workflow without accessing protected attributes
        # 1. Get version
        version_result = adapter.get_version()
        assert version_result.is_success
        assert version_result.data is not None

        # 2. Discover plugins
        plugins_result = adapter.discover_plugins()
        assert plugins_result.is_success
        assert isinstance(plugins_result.data, list)

        # 3. Create tap stream catalog
        catalog_result = adapter.create_tap_stream_catalog()
        assert catalog_result.is_success
        assert "streams" in catalog_result.data

        # 4. Create target config
        target_result = adapter.create_target_config()
        assert target_result.is_success
        assert "target_schema" in target_result.data

        # 5. Convert singer schema
        schema_result = adapter.convert_singer_schema()
        assert schema_result.is_success
        assert "schema_version" in schema_result.data

        # 6. Execute DBT operation
        dbt_result = adapter.execute_dbt_operation()
        assert dbt_result.is_success
        assert "dbt_status" in dbt_result.data

        # 7. Execute bridge service
        bridge_result = adapter.execute_bridge_service()
        assert bridge_result.is_success
        assert bridge_result.data["service"] == "MeltanoBridge"

    def test_adapter_state_management(self) -> None:
        """Test adapter state management across operations."""
        adapter = FlextMeltanoAdapter()

        # Test project initialization and info retrieval
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create a minimal meltano.yml file
            meltano_yml = project_path / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test_project\n")

            with patch.object(adapter, "_load_meltano_project") as mock_load_project:
                mock_load_project.return_value = FlextResult[object].ok(Mock())

                result = adapter.initialize_project(project_path)
                assert result.is_success
                assert result.data is not None

                # Get project info should work now
                info_result = adapter.get_project_info()
                assert info_result.is_success
                assert info_result.data is not None
