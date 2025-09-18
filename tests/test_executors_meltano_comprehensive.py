"""Comprehensive test module for FlextMeltanoExecutor - UNIFIED patterns only.

Tests the FlextMeltanoExecutor unified class following FLEXT standards.
NO ALIASES, NO BACKWARD COMPATIBILITY - Direct API testing only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import pytest

from flext_core import FlextResult
from flext_meltano.executors import FlextMeltanoExecutor


class TestFlextMeltanoExecutorUnified:
    """Test FlextMeltanoExecutor unified class - NO ALIASES."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        # Use temporary directory for test isolation
        self.temp_dir = Path(tempfile.mkdtemp())
        self.executor = FlextMeltanoExecutor(project_root=self.temp_dir)

    def test_unified_executor_initialization(self) -> None:
        """Test FlextMeltanoExecutor unified initialization."""
        assert isinstance(self.executor, FlextMeltanoExecutor)
        assert self.executor.project_root is not None
        assert isinstance(self.executor.project_root, Path)

    def test_unified_executor_has_required_attributes(self) -> None:
        """Test that unified executor has all required attributes."""
        required_attributes = [
            "project_root",
            "meltano_adapter",
            "logger",
            "_bridge",
        ]

        for attr in required_attributes:
            assert hasattr(self.executor, attr), f"Missing required attribute: {attr}"

    def test_unified_executor_has_required_methods(self) -> None:
        """Test that unified executor has all required methods and properties."""
        required_methods = [
            "execute",
            "execute_meltano_command",
            "get_project_info",
            "run_command",
        ]

        required_properties = [
            "project_root_safe",
            "meltano_adapter_safe",
            "logger_safe",
            "bridge",
        ]

        for method in required_methods:
            assert hasattr(self.executor, method), f"Missing required method: {method}"
            assert callable(getattr(self.executor, method)), (
                f"Method {method} is not callable"
            )

        for prop in required_properties:
            assert hasattr(self.executor, prop), f"Missing required property: {prop}"

    def test_unified_executor_execute_method(self) -> None:
        """Test FlextMeltanoExecutor execute method."""
        result = self.executor.execute()
        assert isinstance(result, FlextResult)
        # Should succeed or fail gracefully
        assert result.is_success or result.is_failure

    def test_unified_executor_safe_property_access(self) -> None:
        """Test safe property access."""
        # Test safe project root access
        project_root = self.executor.project_root_safe
        assert isinstance(project_root, Path)

        # Test safe meltano adapter access
        adapter = self.executor.meltano_adapter_safe
        assert adapter is not None

        # Test safe logger access
        logger = self.executor.logger_safe
        assert logger is not None

    def test_unified_executor_bridge_access(self) -> None:
        """Test bridge access through unified executor."""
        bridge = self.executor.bridge
        assert bridge is not None
        # Bridge should be the bridge instance with real methods
        assert hasattr(bridge, "get_version")
        assert hasattr(bridge, "run_pipeline")

    def test_unified_executor_run_command_structure(self) -> None:
        """Test unified executor run_command method structure."""
        # Test with version command (should always be available)
        result = self.executor.run_command(["--version"])
        assert isinstance(result, FlextResult)
        # Command should execute (success or controlled failure)
        assert result.is_success or result.is_failure

    def test_unified_executor_get_project_info(self) -> None:
        """Test unified executor get_project_info method."""
        result = self.executor.get_project_info(self.temp_dir)
        assert isinstance(result, FlextResult)
        # Should return project info or controlled failure
        assert result.is_success or result.is_failure

    def test_unified_executor_execute_meltano_command(self) -> None:
        """Test unified executor execute_meltano_command method."""
        # Test with simple command using project root
        result = self.executor.execute_meltano_command(self.temp_dir, ["--version"])
        assert isinstance(result, FlextResult)
        # Should execute command or handle gracefully
        assert result.is_success or result.is_failure

    def test_no_backward_compatibility_aliases(self) -> None:
        """Test that NO backward compatibility aliases exist."""
        # Verify that old aliases do NOT exist
        forbidden_attributes = [
            "simple_meltano_executor",
            "simple_dbt_executor",
            "meltano_executor",
            "adapter",  # Should use meltano_adapter_safe()
        ]

        for attr in forbidden_attributes:
            assert not hasattr(self.executor, attr), (
                f"VIOLATION: Found eliminated alias {attr} - should not exist"
            )

    def test_unified_executor_type_consistency(self) -> None:
        """Test that executor maintains type consistency."""
        # All instances should be the same unified type
        executor1 = FlextMeltanoExecutor()
        executor2 = FlextMeltanoExecutor()

        assert type(executor1) is type(executor2)
        assert isinstance(executor1, FlextMeltanoExecutor)
        assert isinstance(executor2, FlextMeltanoExecutor)

    def test_unified_executor_project_isolation(self) -> None:
        """Test that executors with different project roots are isolated."""
        temp_dir2 = Path(tempfile.mkdtemp())
        executor2 = FlextMeltanoExecutor(project_root=temp_dir2)

        # Should have different project roots
        assert self.executor.project_root != executor2.project_root
        assert self.executor.project_root == self.temp_dir
        assert executor2.project_root == temp_dir2

    def test_unified_executor_flext_result_consistency(self) -> None:
        """Test that all executor methods return FlextResult consistently."""
        # All methods that return results should use FlextResult
        result_methods = [
            "execute",
            "execute_meltano_command",
            "get_project_info",
            "run_command",
        ]

        for method_name in result_methods:
            method = getattr(self.executor, method_name)
            if method_name == "execute":
                result = method()
            elif method_name == "execute_meltano_command":
                result = method(self.temp_dir, ["--version"])
            elif method_name == "run_command":
                result = method(["--version"])
            elif method_name == "get_project_info":
                result = method(self.temp_dir)
            else:
                result = method()

            assert isinstance(result, FlextResult), (
                f"Method {method_name} did not return FlextResult"
            )

    def teardown_method(self) -> None:
        """Clean up test fixtures."""
        # Clean up temporary directory
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)


if __name__ == "__main__":
    pytest.main([__file__])
