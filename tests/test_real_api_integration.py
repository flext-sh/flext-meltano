"""Real API Integration Tests - Testing actual Meltano/Singer/DBT functionality.

**Purpose**: Test real API integration without mocks or subprocess calls
**Target**: 100% real functionality with installed Meltano 3.9.1, Singer SDK 0.48.0, DBT Core 1.10.5
**Scope**: End-to-end testing of native API integration

This module tests the actual functionality that flext-meltano provides:
1. Meltano Hub discovery via native APIs
2. Singer SDK integration patterns
3. DBT functionality integration
4. Bridge operations for Go service integration
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextResult

from flext_meltano.base_dbt import MeltanoDbtWrapper
from flext_meltano.base_meltano import MeltanoBridge
from flext_meltano.base_singer import MeltanoSingerWrapper
from flext_meltano.executors_bridge import FlextMeltanoBridge
from flext_meltano.executors_meltano import FlextMeltanoExecutor


class TestRealMeltanoIntegration:
    """Test real Meltano integration using native APIs."""

    def test_meltano_hub_discovery_real(self) -> None:
        """Test real Meltano Hub plugin discovery via native API."""
        bridge = MeltanoBridge()

        # This calls real Meltano Hub APIs
        result = bridge.discover_plugins()

        assert result.success
        assert isinstance(result.value, list)
        assert len(result.value) > 0

        # Check that we get real plugin data
        first_plugin = result.value[0]
        assert "name" in first_plugin
        assert "type" in first_plugin
        assert first_plugin["type"] in {"extractor", "loader", "transformer"}

    def test_meltano_version_check_real(self) -> None:
        """Test real Meltano version checking via native API."""
        bridge = MeltanoBridge()

        result = bridge.get_version()

        assert result.success
        assert isinstance(result.value, dict)
        assert "version" in result.value

        # Should be using real Meltano 3.9.1
        version = result.value["version"]
        assert version.startswith("3.")


class TestRealSingerSDKIntegration:
    """Test real Singer SDK integration using native APIs."""

    def test_singer_sdk_wrapper_creation(self) -> None:
        """Test Singer SDK wrapper functionality."""
        wrapper = MeltanoSingerWrapper()

        # Test service execution (FlextDomainService pattern)
        result = wrapper.execute()

        assert result.success
        assert isinstance(result.value, dict)
        assert result.value["service"] == "MeltanoSingerWrapper"
        assert result.value["status"] == "ready"

    def test_singer_sdk_imports_available(self) -> None:
        """Test that Singer SDK components are properly available."""
        # These imports should work with real Singer SDK 0.48.0
        from singer_sdk import Stream, Tap, Target
        from singer_sdk.typing import PropertiesList

        # Test that classes are actually the real SDK classes
        assert hasattr(Tap, "discover_streams")
        assert hasattr(Stream, "schema")
        assert hasattr(PropertiesList, "to_dict")

        # Test basic target functionality
        assert Target is not None


class TestRealDBTIntegration:
    """Test real DBT integration using native APIs."""

    def test_dbt_wrapper_creation(self) -> None:
        """Test DBT wrapper functionality."""
        wrapper = MeltanoDbtWrapper()

        assert wrapper is not None
        # Test that DBT core is available
        assert hasattr(wrapper, "create_runner")

    def test_dbt_core_availability(self) -> None:
        """Test that DBT Core 1.10.5 is properly available."""
        from dbt.cli.main import dbtRunner

        # Should be real DBT Core
        runner = dbtRunner()
        assert runner is not None


class TestRealBridgeIntegration:
    """Test real Go bridge integration using native APIs."""

    def test_bridge_json_api_version(self) -> None:
        """Test Go bridge JSON API for version information."""
        bridge = FlextMeltanoBridge()

        result = bridge.get_version()

        # Should return Go-compatible JSON
        assert isinstance(result, dict)
        assert result["success"] is True
        assert "data" in result

        data = result["data"]
        assert "flext_meltano" in data
        assert "meltano" in data
        assert "dbt_core" in data
        assert "singer_sdk" in data
        assert data["integration_method"] == "native_apis"

    def test_bridge_json_api_plugins(self) -> None:
        """Test Go bridge JSON API for plugin listing."""
        bridge = FlextMeltanoBridge()

        result = bridge.list_plugins()

        # Should return Go-compatible JSON
        assert isinstance(result, dict)
        assert result["success"] is True
        assert "data" in result

        plugins = result["data"]
        assert isinstance(plugins, list)
        assert len(plugins) > 0

        # Check plugin structure for Go consumption
        first_plugin = plugins[0]
        assert "name" in first_plugin
        assert "type" in first_plugin


class TestRealExecutorIntegration:
    """Test real executor integration patterns."""

    def test_executor_creation_and_basic_functionality(self) -> None:
        """Test executor creation and basic operations."""
        executor = FlextMeltanoExecutor()

        assert executor is not None
        assert hasattr(executor, "execute")

        # Test FlextDomainService pattern
        result = executor.execute()
        assert isinstance(result, FlextResult)

    def test_executor_bridge_integration(self) -> None:
        """Test executor integration with bridge functionality."""
        FlextMeltanoExecutor()
        bridge = FlextMeltanoBridge()

        # Bridge should use executor internally
        assert bridge.executor is not None
        assert isinstance(bridge.executor, FlextMeltanoExecutor)

        # Test integrated operations
        version_result = bridge.get_version()
        assert version_result["success"] is True


class TestRealEndToEndWorkflow:
    """Test real end-to-end workflow patterns."""

    def test_complete_discovery_workflow(self) -> None:
        """Test complete plugin discovery workflow using real APIs."""
        # Step 1: Create bridge
        bridge = FlextMeltanoBridge()

        # Step 2: Get system info
        version_result = bridge.get_version()
        assert version_result["success"] is True

        # Step 3: Discover plugins
        plugins_result = bridge.list_plugins()
        assert plugins_result["success"] is True

        plugins = plugins_result["data"]
        assert len(plugins) > 0

        # Step 4: Verify real data
        extractors = [p for p in plugins if p["type"] == "extractor"]
        loaders = [p for p in plugins if p["type"] == "loader"]
        transformers = [p for p in plugins if p["type"] == "transformer"]

        assert len(extractors) > 0
        assert len(loaders) > 0
        assert len(transformers) > 0

    def test_script_bridge_integration(self) -> None:
        """Test that the bridge script logic works with real APIs."""
        # Instead of subprocess, test the bridge functionality directly
        # This simulates what the Go service would call via the bridge script
        bridge = FlextMeltanoBridge()

        # Test version endpoint (what Go service calls)
        version_result = bridge.get_version()
        assert version_result["success"] is True
        assert "data" in version_result
        assert "meltano" in version_result["data"]

        # Test plugins endpoint (what Go service calls)
        plugins_result = bridge.list_plugins()
        assert plugins_result["success"] is True
        assert "data" in plugins_result
        assert isinstance(plugins_result["data"], list)
        assert len(plugins_result["data"]) > 0


class TestRealConfigurationIntegration:
    """Test real configuration patterns."""

    def test_configuration_with_real_paths(self) -> None:
        """Test configuration handling with real file paths."""
        from flext_meltano.base_projects import FlextMeltanoConfig

        config = FlextMeltanoConfig()

        assert config.environment == "development"
        assert isinstance(config.project_root, str)
        assert Path(config.project_root).exists()

    def test_utilities_integration(self) -> None:
        """Test utilities with real functionality."""
        from flext_meltano.utilities import (
            FlextMeltanoUtilities,
            validate_directory_path,
        )

        # Test directory validation with real path
        current_dir = str(Path.cwd())
        result = validate_directory_path(current_dir)

        assert result is not None
        assert Path(result).exists()

        # Test utilities class
        utils = FlextMeltanoUtilities()
        assert utils is not None
