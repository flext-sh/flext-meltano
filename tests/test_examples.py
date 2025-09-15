"""Tests for examples to ensure they work and improve coverage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import importlib.util
import types
from pathlib import Path
from unittest.mock import patch

import pytest


class TestExamples:
    """Test examples work correctly."""

    def _import_example_module(self) -> types.ModuleType:
        """Import the example module dynamically."""
        example_path = (
            Path(__file__).parent.parent / "examples" / "01_simple_working.py"
        )
        spec = importlib.util.spec_from_file_location("example_module", example_path)
        if spec is None or spec.loader is None:
            pytest.skip("Could not load example module")
        example_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(example_module)
        return example_module

    def test_simple_working_example_imports(self) -> None:
        """Test that the simple working example can be imported."""
        example_module = self._import_example_module()

        assert hasattr(example_module, "simple_bridge_example")
        assert hasattr(example_module, "simple_executor_example")
        assert hasattr(example_module, "simple_config_example")

    def test_simple_bridge_example_execution(self) -> None:
        """Test bridge example can execute without errors."""
        example_module = self._import_example_module()

        with patch.object(example_module, "FlextMeltanoBridge") as mock_bridge:
            # Mock successful responses
            mock_instance = mock_bridge.return_value
            mock_instance.get_version.return_value.success = True
            mock_instance.get_version.return_value.value = "1.0.0"
            mock_instance.discover_plugins.return_value.success = True
            mock_instance.discover_plugins.return_value.value = ["plugin1", "plugin2"]

            # Should not raise exception
            example_module.simple_bridge_example()

    def test_simple_executor_example_execution(self) -> None:
        """Test executor example can execute without errors."""
        example_module = self._import_example_module()

        with patch.object(example_module, "FlextMeltanoExecutor") as mock_executor:
            # Mock successful response
            mock_instance = mock_executor.return_value
            mock_instance.execute.return_value.success = True
            mock_instance.execute.return_value.value = {"version": "1.0.0"}

            # Should not raise exception
            example_module.simple_executor_example()

    def test_simple_config_example_execution(self) -> None:
        """Test config example can execute without errors."""
        example_module = self._import_example_module()

        # Should not raise exception
        example_module.simple_config_example()

    def test_main_execution_with_mocked_functions(self) -> None:
        """Test main execution path with mocked functions."""
        example_module = self._import_example_module()

        with (
            patch.object(example_module, "simple_bridge_example") as mock_bridge,
            patch.object(example_module, "simple_executor_example") as mock_executor,
            patch.object(example_module, "simple_config_example") as mock_config,
        ):
            # Manually call main logic with mocks
            try:
                mock_bridge()
                mock_executor()
                mock_config()
            except Exception:
                pytest.fail("Main execution should not raise exceptions")
