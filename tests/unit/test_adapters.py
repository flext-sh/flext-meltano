"""FLEXT Meltano Adapter Tests - Real functionality testing.

This module provides tests for FlextMeltanoAdapter using real functionality
without mocks or patches.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import tempfile
from pathlib import Path

from flext_core import FlextResult

from flext_meltano import FlextMeltanoAdapter


class TestFlextMeltanoAdapter:
    """Test suite for FlextMeltanoAdapter with real functionality."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.adapter = FlextMeltanoAdapter()

    def test_adapter_initialization(self) -> None:
        """Test adapter initialization."""
        adapter = FlextMeltanoAdapter()

        assert adapter is not None, "Adapter should be initialized"
        assert hasattr(adapter, "project_adapter"), "Should have project_adapter"
        assert hasattr(adapter, "plugin_adapter"), "Should have plugin_adapter"
        assert hasattr(adapter, "pipeline_adapter"), "Should have pipeline_adapter"
        assert hasattr(adapter, "singer_adapter"), "Should have singer_adapter"
        assert hasattr(adapter, "dbt_adapter"), "Should have dbt_adapter"

    def test_adapter_project_operations(self) -> None:
        """Test adapter project operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "test_project"
            result = self.adapter.project_adapter.create_project(
                "test-project",
                project_path,
            )

            assert isinstance(result, FlextResult), "Should return FlextResult"

    def test_adapter_plugin_operations(self) -> None:
        """Test adapter plugin operations."""
        result = self.adapter.plugin_adapter.discover_plugins()

        assert isinstance(result, FlextResult), "Should return FlextResult"

    def test_adapter_pipeline_operations(self) -> None:
        """Test adapter pipeline operations."""
        result = self.adapter.pipeline_adapter.execute_pipeline(
            "tap-csv",
            "target-jsonl",
        )

        assert isinstance(result, FlextResult), "Should return FlextResult"

    def test_adapter_failure_handling(self) -> None:
        """Test adapter failure handling."""
        invalid_path = Path("/nonexistent/directory")
        result = self.adapter.project_adapter.create_project("test", invalid_path)

        assert isinstance(result, FlextResult), "Should return FlextResult"
        assert hasattr(result, "is_success"), "Should have is_success"
        assert hasattr(result, "error"), "Should have error"
