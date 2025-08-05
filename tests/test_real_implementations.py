"""Tests for real implementations - Quick validation of refactored modules.

**Purpose**: Validate that the refactored modules work correctly
**Scope**: Basic functionality tests for dbt.py and flext_singer.py
**Target**: Ensure implementations are functional, not comprehensive coverage

This module provides quick smoke tests to ensure our refactoring efforts
resulted in working code.
"""

from __future__ import annotations

from flext_meltano.dbt import (
    FlextMeltanoDbtManager,
    FlextMeltanoDbtProject,
    FlextMeltanoDbtRunner,
)
from flext_meltano.flext_singer import FlextSingerBridge, FlextSingerCatalog


class TestDbtRealImplementations:
    """Test DBT real implementations."""

    def test_dbt_manager_creation(self):
        """Test DBT manager can be created."""
        manager = FlextMeltanoDbtManager()
        assert manager is not None
        assert hasattr(manager, "executor")
        assert hasattr(manager, "project_dir")

    def test_dbt_project_creation(self):
        """Test DBT project can be created."""
        project = FlextMeltanoDbtProject()
        assert project is not None
        assert hasattr(project, "executor")
        assert hasattr(project, "project_dir")

    def test_dbt_runner_creation(self):
        """Test DBT runner can be created."""
        runner = FlextMeltanoDbtRunner()
        assert runner is not None
        assert hasattr(runner, "executor")
        assert hasattr(runner, "project_dir")

    def test_dbt_manager_methods_exist(self):
        """Test DBT manager has expected methods."""
        manager = FlextMeltanoDbtManager()

        # Check all expected methods exist
        assert hasattr(manager, "run_models")
        assert hasattr(manager, "test_models")
        assert hasattr(manager, "compile_models")
        assert hasattr(manager, "generate_docs")
        assert hasattr(manager, "serve_docs")

        # Methods should be callable
        assert callable(manager.run_models)
        assert callable(manager.test_models)
        assert callable(manager.compile_models)

    def test_dbt_project_methods_exist(self):
        """Test DBT project has expected methods."""
        project = FlextMeltanoDbtProject()

        assert hasattr(project, "initialize")
        assert hasattr(project, "validate")
        assert callable(project.initialize)
        assert callable(project.validate)

    def test_dbt_runner_methods_exist(self):
        """Test DBT runner has expected methods."""
        runner = FlextMeltanoDbtRunner()

        assert hasattr(runner, "run")
        assert hasattr(runner, "run_models")
        assert hasattr(runner, "test_models")
        assert callable(runner.run)
        assert callable(runner.run_models)
        assert callable(runner.test_models)


class TestSingerRealImplementations:
    """Test Singer real implementations."""

    def test_singer_bridge_creation(self):
        """Test Singer bridge can be created."""
        bridge = FlextSingerBridge()
        assert bridge is not None
        assert hasattr(bridge, "_logger")
        assert hasattr(bridge, "_container")

    def test_singer_catalog_creation(self):
        """Test Singer catalog can be created."""
        catalog = FlextSingerCatalog()
        assert catalog is not None
        assert hasattr(catalog, "_logger")

    def test_singer_bridge_message_creation(self):
        """Test Singer bridge can create messages."""
        bridge = FlextSingerBridge()

        # Test record message creation
        result = bridge.flext_singer_create_record_message(
            stream="test_stream", record={"id": 1, "name": "test"}
        )

        assert result.success
        assert result.data is not None
        assert result.data["type"] == "RECORD"
        assert result.data["stream"] == "test_stream"
        assert result.data["record"] == {"id": 1, "name": "test"}

    def test_singer_bridge_schema_creation(self):
        """Test Singer bridge can create schema messages."""
        bridge = FlextSingerBridge()

        schema = {
            "type": "object",
            "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
        }

        result = bridge.flext_singer_create_schema_message(
            stream="test_stream", schema=schema, key_properties=["id"]
        )

        assert result.success
        assert result.data is not None
        assert result.data["type"] == "SCHEMA"
        assert result.data["stream"] == "test_stream"
        assert result.data["schema"] == schema
        assert result.data["key_properties"] == ["id"]

    def test_singer_bridge_universal_method(self):
        """Test Singer bridge universal message creation method."""
        bridge = FlextSingerBridge()

        # Test universal method for record creation
        result = bridge.flext_singer_create_message(
            "RECORD", stream="test_stream", record={"id": 1, "name": "test"}
        )

        assert result.success
        assert result.data is not None
        assert result.data["type"] == "RECORD"

    def test_singer_bridge_error_handling(self):
        """Test Singer bridge error handling."""
        bridge = FlextSingerBridge()

        # Test invalid message type
        result = bridge.flext_singer_create_message("INVALID_TYPE")
        assert not result.success
        assert "Unknown message type" in str(result.error)

    def test_singer_bridge_methods_exist(self):
        """Test Singer bridge has expected methods."""
        bridge = FlextSingerBridge()

        # Check all expected methods exist
        assert hasattr(bridge, "flext_singer_create_message")
        assert hasattr(bridge, "flext_singer_create_record_message")
        assert hasattr(bridge, "flext_singer_create_schema_message")
        assert hasattr(bridge, "flext_singer_create_state_message")

        # Methods should be callable
        assert callable(bridge.flext_singer_create_message)
        assert callable(bridge.flext_singer_create_record_message)
        assert callable(bridge.flext_singer_create_schema_message)


class TestIntegrationBasics:
    """Test basic integration between components."""

    def test_imports_work_correctly(self):
        """Test that all imports work without circular dependency issues."""
        # This test validates that our refactoring didn't break imports
        from flext_meltano.dbt import FlextMeltanoDbtManager
        from flext_meltano.flext_singer import FlextSingerBridge

        # Should be able to create instances without errors
        dbt_manager = FlextMeltanoDbtManager()
        singer_bridge = FlextSingerBridge()

        assert dbt_manager is not None
        assert singer_bridge is not None

    def test_flext_result_patterns_used(self):
        """Test that FlextResult patterns are properly used."""
        from flext_core import FlextResult

        from flext_meltano.dbt import FlextMeltanoDbtManager
        from flext_meltano.flext_singer import FlextSingerBridge

        dbt_manager = FlextMeltanoDbtManager()
        singer_bridge = FlextSingerBridge()

        # All methods should return FlextResult instances
        # (These will fail since we don't have Meltano installed, but we check return types)

        # Check that methods exist and are callable
        assert callable(dbt_manager.run_models)
        assert callable(singer_bridge.flext_singer_create_record_message)

        # Test actual message creation (this should work)
        result = singer_bridge.flext_singer_create_record_message("test", {"id": 1})
        assert isinstance(result, FlextResult)
        assert result.success
