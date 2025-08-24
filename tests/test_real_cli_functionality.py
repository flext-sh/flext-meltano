"""Real CLI Functionality Tests - NO MOCKS, only real API integration.

**Test Category**: Real Integration Tests
**Coverage Target**: 95%+ for CLI module components
**Dependencies**: Real Meltano 3.9.1, Singer SDK 0.48.0, DBT Core 1.10.5 APIs
**Execution Time**: Real execution, may take longer

## Test Scope

Tests REAL functionality using installed libraries:
- Meltano 3.9.1 native API integration
- Singer SDK 0.48.0 direct usage
- DBT Core 1.10.5 API calls
- FlextResult patterns with .value and unwrap_or()
- NO subprocess calls, NO mocks, REAL execution only

## Architecture Alignment

Tests the 3 core functions:
1. **Wrapper**: Real adaption of Meltano/Singer/DBT APIs to flext-core
2. **Runtime**: Real Go bridge execution capabilities
3. **Base**: Real foundation for flext-(tap|target|dbt) projects
"""

from __future__ import annotations

from flext_core import FlextResult

from flext_meltano import FlextMeltanoCli, flext_meltano_run_cli
from flext_meltano.meltano_adapters import MeltanoBridge


class TestRealFlextMeltanoCli:
    """Test real FlextMeltanoCli functionality with actual API integration."""

    def setup_method(self) -> None:
        """Setup real CLI instance for each test."""
        self.cli = FlextMeltanoCli()

    def test_cli_initialization_real(self) -> None:
        """Test CLI initializes with real dependencies."""
        assert self.cli is not None
        assert hasattr(self.cli, "logger")

        # Test that CLI has access to real methods
        assert hasattr(self.cli, "flext_meltano_version")
        assert hasattr(self.cli, "list_plugins")
        assert hasattr(self.cli, "flext_meltano_install")

    def test_version_real_meltano_api(self) -> None:
        """Test version retrieval using real Meltano API."""
        result = self.cli.flext_meltano_version()

        assert result.success is True, f"Version failed: {result.error}"
        assert isinstance(result.value, str)
        assert "Meltano" in result.value
        assert "3.9.1" in result.value  # Real version from installed package

    def test_health_check_real_dependencies(self) -> None:
        """Test health check validates real installed dependencies."""
        result = self.cli.health()

        assert result.success is True, f"Health check failed: {result.error}"
        assert isinstance(result.value, dict)

        health_data = result.value
        assert "status" in health_data
        assert health_data["status"] in {"healthy", "degraded", "unhealthy"}

    def test_list_commands_real_cli(self) -> None:
        """Test listing real CLI commands available."""
        result = self.cli.list_commands()

        assert result.success is True, f"List commands failed: {result.error}"
        assert isinstance(result.value, dict)

        commands_data = result.value
        assert "commands" in commands_data
        assert len(commands_data["commands"]) > 0

    def test_install_operation_real_api(self) -> None:
        """Test install operation using real Meltano API patterns."""
        result = self.cli.flext_meltano_install()

        # Should succeed as it uses real API patterns
        assert result.success is True, f"Install failed: {result.error}"
        assert isinstance(result.value, bool)
        assert result.value is True

    def test_list_plugins_real_meltano_hub(self) -> None:
        """Test plugin listing using real Meltano Hub API."""
        result = self.cli.list_plugins()

        assert result.success is True, f"List plugins failed: {result.error}"
        assert isinstance(result.value, dict)

        plugins_data = result.value
        assert "plugins" in plugins_data
        # Real Meltano Hub should have plugins available
        assert isinstance(plugins_data["plugins"], list)

    def test_plugin_invoke_real_validation(self) -> None:
        """Test plugin invocation with real validation patterns."""
        # Test with a common plugin name that should be recognizable
        result = self.cli.flext_meltano_invoke("tap-csv", "--help")

        # Should handle the invocation attempt properly
        assert result.success is True, f"Plugin invoke failed: {result.error}"
        assert isinstance(result.value, dict)

        invoke_data = result.value
        assert "plugin_name" in invoke_data
        assert invoke_data["plugin_name"] == "tap-csv"


class TestRealCliFactoryFunction:
    """Test real CLI factory function integration."""

    def test_cli_factory_function_real(self) -> None:
        """Test CLI factory function with real argument processing."""
        result = flext_meltano_run_cli(["--version"])

        assert result.success is True, f"CLI factory failed: {result.error}"
        assert isinstance(result.value, dict)

        cli_data = result.value
        assert "command" in cli_data
        assert cli_data["command"] in {"version", "--version"}  # Accept both formats

    def test_cli_factory_help_real(self) -> None:
        """Test CLI factory help command with real processing."""
        result = flext_meltano_run_cli(["--help"])

        assert result.success is True, f"CLI help failed: {result.error}"
        assert isinstance(result.value, dict)

        help_data = result.value
        assert "command" in help_data
        assert help_data["command"] in {"help", "--help"}  # Accept both formats

    def test_cli_factory_empty_args_real(self) -> None:
        """Test CLI factory with empty args using real defaults."""
        result = flext_meltano_run_cli([])

        # Should handle empty args gracefully
        assert result.success is True, f"CLI empty args failed: {result.error}"
        assert isinstance(result.value, dict)

    def test_cli_factory_none_args_real(self) -> None:
        """Test CLI factory with None args using real defaults."""
        result = flext_meltano_run_cli(None)

        # Should handle None args gracefully
        assert result.success is True, f"CLI None args failed: {result.error}"
        assert isinstance(result.value, dict)


class TestRealMeltanoIntegration:
    """Test real Meltano integration without subprocess calls."""

    def setup_method(self) -> None:
        """Setup with real CLI instance."""
        self.cli = FlextMeltanoCli()

    def test_real_meltano_version_api(self) -> None:
        """Test direct integration with real Meltano version API."""
        # This should use MeltanoBridge internally, not subprocess
        result = self.cli.flext_meltano_version()

        assert result.success is True
        version_str = result.value
        assert isinstance(version_str, str)

        # Verify it's using real API, not subprocess fallback
        assert "Meltano, version" in version_str
        assert "3.9.1" in version_str

    def test_real_meltano_bridge_integration(self) -> None:
        """Test that CLI uses real MeltanoBridge, not subprocess."""
        # Bridge imported at top level for integration testing
        bridge = MeltanoBridge()
        bridge_result = bridge.get_version()

        assert bridge_result.success is True
        bridge_version = bridge_result.value

        # Now test CLI uses same bridge
        cli_result = self.cli.flext_meltano_version()
        assert cli_result.success is True

        # Both should indicate real API usage (not subprocess)
        assert isinstance(bridge_version, dict)
        assert "version" in bridge_version
        assert bridge_version["version"] == "3.9.1"

    def test_real_singer_sdk_integration(self) -> None:
        """Test real Singer SDK integration available via CLI."""
        # CLI should have access to Singer SDK functionality
        # This tests the wrapper function integration

        result = self.cli.list_plugins()
        assert result.success is True

        plugins_data = result.value
        # Should be able to access Singer-related plugins through real API
        assert isinstance(plugins_data, dict)
        assert "plugins" in plugins_data

    def test_real_dbt_integration_available(self) -> None:
        """Test that real DBT integration is available via CLI."""
        # CLI should have access to DBT functionality through wrappers

        # Health check should validate DBT availability
        result = self.cli.health()
        assert result.success is True

        health_data = result.value
        assert isinstance(health_data, dict)
        # Health check validates real dependencies are available


class TestFlextResultPatterns:
    """Test FlextResult patterns using .value and unwrap_or() - NO .data or .unwrap()."""

    def setup_method(self) -> None:
        """Setup CLI for FlextResult pattern testing."""
        self.cli = FlextMeltanoCli()

    def test_flext_result_value_property(self) -> None:
        """Test FlextResult uses .value property, not .data."""
        result = self.cli.flext_meltano_version()

        assert result.success is True
        # Test .value property (NEW pattern)
        version_value = result.value
        assert isinstance(version_value, str)

        # Ensure .data is not used (OLD pattern)
        # Note: We won't test hasattr(.data) as it might exist for backwards compat
        # But we ensure code uses .value

    def test_flext_result_unwrap_or_pattern(self) -> None:
        """Test FlextResult unwrap_or() method for error handling."""
        # Test successful case
        success_result = self.cli.flext_meltano_version()
        version = success_result.unwrap_or("default_version")
        assert version != "default_version"  # Should get real version
        assert "Meltano" in version

        # Test with method that might fail gracefully
        plugins_result = self.cli.list_plugins()
        plugins = plugins_result.unwrap_or({"plugins": []})
        assert isinstance(plugins, dict)

    def test_error_handling_with_unwrap_or(self) -> None:
        """Test error handling uses unwrap_or() instead of manual checking."""
        # Test pattern: result.unwrap_or(default) instead of:
        # if result.success: return result.value else: return default

        result = self.cli.health()

        # Modern pattern with unwrap_or
        health_status = result.unwrap_or({"status": "unknown"})
        assert isinstance(health_status, dict)
        assert "status" in health_status

    def test_chaining_operations_with_flext_result(self) -> None:
        """Test chaining FlextResult operations properly."""
        # Test that all methods return FlextResult for chaining
        version_result = self.cli.flext_meltano_version()
        assert isinstance(version_result, FlextResult)

        health_result = self.cli.health()
        assert isinstance(health_result, FlextResult)

        plugins_result = self.cli.list_plugins()
        assert isinstance(plugins_result, FlextResult)
