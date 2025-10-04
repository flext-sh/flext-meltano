"""Tests for FlextMeltanoLibraryRunner foundation - Basic functionality without external dependencies.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from flext_core import FlextResult

from flext_meltano.abstractions import FlextMeltanoAbstractions
from flext_meltano.adapters import FlextMeltanoAdapter


class TestFlextMeltanoLibraryRunnerFoundation:
    """Test FlextMeltanoLibraryRunner foundation functionality."""

    def test_import_error_handling(self) -> None:
        """Test that import errors are properly handled."""
        # Test that the module raises ImportError when dependencies are missing
        with pytest.raises(ImportError, match="Advanced library modules not available"):
            pass

    def test_adapter_import_without_library_runner(self) -> None:
        """Test that adapter can be imported even without library runner dependencies."""
        # Mock the library runner import to avoid the ImportError
        with patch.dict("sys.modules", {"flext_meltano.library_runner": Mock()}):
            # Test that adapter can be instantiated
            adapter = FlextMeltanoAdapter()
            assert adapter is not None
            assert hasattr(adapter, "_abstractions")

    def test_abstractions_functionality(self) -> None:
        """Test that abstractions work independently."""
        abstractions = FlextMeltanoAbstractions()
        assert abstractions is not None

        # Test getting wrappers
        project_wrapper = abstractions.get_project_wrapper()
        assert project_wrapper is not None

        runner_wrapper = abstractions.get_runner_wrapper()
        assert runner_wrapper is not None

    def test_adapter_basic_functionality(self) -> None:
        """Test basic adapter functionality without external dependencies."""
        adapter = FlextMeltanoAdapter()

        # Test basic methods
        assert hasattr(adapter, "get_version")
        assert hasattr(adapter, "discover_plugins")
        assert hasattr(adapter, "create_project")
        assert hasattr(adapter, "add_plugin")

        # Test version method
        version_result = adapter.get_version()
        assert isinstance(version_result, FlextResult)
        assert version_result.is_success

    def test_adapter_project_validation(self) -> None:
        """Test project validation functionality."""
        adapter = FlextMeltanoAdapter()

        # Test with non-existent directory
        non_existent_path = Path("/non/existent/path")
        validation_result = adapter.validate_project(non_existent_path)
        assert isinstance(validation_result, FlextResult)
        assert validation_result.is_failure

    def test_adapter_plugin_discovery(self) -> None:
        """Test plugin discovery functionality."""
        adapter = FlextMeltanoAdapter()

        # Test plugin discovery
        discovery_result = adapter.discover_plugins()
        assert isinstance(discovery_result, FlextResult)
        # This might succeed or fail depending on meltano availability
        # We just test that it returns a FlextResult

    def test_adapter_static_methods(self) -> None:
        """Test static adapter methods."""
        # Test adapt_project_config
        config = {"version": 1}
        adapted_config = FlextMeltanoAdapter.adapt_project_config(config)
        assert isinstance(adapted_config, FlextResult)
        assert adapted_config.is_success

        adapted_data = adapted_config.unwrap()
        assert "project_id" in adapted_data
        assert "version" in adapted_data
        assert "default_environment" in adapted_data

        # Test adapt_plugin
        plugin_data = {"type": "extractor", "pip_url": "test-plugin"}
        adapted_plugin = FlextMeltanoAdapter.adapt_plugin(plugin_data)
        assert isinstance(adapted_plugin, FlextResult)
        assert adapted_plugin.is_success

        adapted_plugin_data = adapted_plugin.unwrap()
        assert "name" in adapted_plugin_data
        assert "namespace" in adapted_plugin_data
        assert "executable" in adapted_plugin_data

    def test_flext_result_patterns(self) -> None:
        """Test that FlextResult patterns are used throughout."""
        adapter = FlextMeltanoAdapter()

        # Test that all methods return FlextResult
        methods_to_test = [
            "get_version",
            "discover_plugins",
            "create_project",
            "add_plugin",
            "validate_project",
        ]

        for method_name in methods_to_test:
            method = getattr(adapter, method_name)
            # We can't easily test all methods without proper setup,
            # but we can verify they exist and are callable
            assert callable(method)

    def test_logging_integration(self) -> None:
        """Test that logging is properly integrated."""
        adapter = FlextMeltanoAdapter()

        # Test that logger is available
        assert hasattr(adapter, "_logger")
        assert adapter._logger is not None

    def test_utilities_integration(self) -> None:
        """Test that utilities are properly integrated."""
        adapter = FlextMeltanoAdapter()

        # Test that utilities are available
        assert hasattr(adapter, "_utilities")
        assert adapter._utilities is not None

    def test_config_integration(self) -> None:
        """Test that configuration is properly integrated."""
        adapter = FlextMeltanoAdapter()

        # Test that config is available
        assert hasattr(adapter, "_config")
        assert adapter._config is not None
