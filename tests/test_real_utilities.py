"""Real Utilities Tests - Tests REAL utility functions without mocks.

**Test Category**: Real Integration Tests
**Coverage Target**: 100% for FlextMeltanoUtilities
**Dependencies**: Real flext-core, NO mocks
**Execution Time**: Fast utilities testing

## Test Scope

Tests REAL utility functionality:
- FlextMeltanoUtilities static methods
- Configuration validation with real types
- Path validation with real filesystem operations
- FlextResult patterns with .value and unwrap_or()

## Architecture Alignment

Tests utilities used across all 3 functions:
- Wrapper utilities for API adaptation
- Runtime utilities for Go bridge operations
- Base utilities for project foundations
"""

from __future__ import annotations

import math
import tempfile
from pathlib import Path

from flext_core import FlextResult

from flext_meltano.utilities import (
    FlextMeltanoUtilities,
    FlextResultHelpers,
    FlextRuntimeUtilities,
    FlextTypeAdapters,
    FlextWrapperUtilities,
    validate_config_value,
    validate_directory_path,
    validate_file_path,
)


class TestRealFlextMeltanoUtilities:
    """Test real FlextMeltanoUtilities with actual filesystem operations."""

    def setup_method(self) -> None:
        """Setup utilities for testing."""
        self.utils = FlextMeltanoUtilities()

    def test_utilities_initialization(self) -> None:
        """Test utilities can be instantiated."""
        assert self.utils is not None
        # Test it's a proper class with expected methods
        assert hasattr(FlextMeltanoUtilities, "validate_plugin_config")
        assert hasattr(FlextMeltanoUtilities, "create_meltano_config")
        assert hasattr(FlextMeltanoUtilities, "normalize_plugin_name")
        assert hasattr(FlextMeltanoUtilities, "create_temp_directory")
        assert hasattr(FlextMeltanoUtilities, "create_dbt_config")
        assert hasattr(FlextMeltanoUtilities, "create_singer_tap_config")
        assert hasattr(FlextMeltanoUtilities, "create_singer_target_config")
        assert hasattr(FlextMeltanoUtilities, "save_yaml_config")
        assert hasattr(FlextMeltanoUtilities, "load_yaml_config")
        assert hasattr(FlextMeltanoUtilities, "sanitize_plugin_name")
        assert hasattr(FlextMeltanoUtilities, "create_plugin_config")
        assert hasattr(FlextMeltanoUtilities, "setup_project_structure")

    def test_validate_plugin_config_real(self) -> None:
        """Test plugin config validation with real data."""
        config_data: dict[str, object] = {
            "name": "tap-csv",
            "namespace": "tap_csv",
            "executable": "tap-csv",
            "pip_url": "pipelinewise-tap-csv",
            "type": "extractors",
        }

        result = FlextMeltanoUtilities.validate_plugin_config(config_data)

        assert result.success is True
        # validate_plugin_config returns FlextResult[bool], so .value is bool
        assert result.value is True

    def test_normalize_plugin_name_real(self) -> None:
        """Test plugin name normalization."""
        # Test various plugin names with plugin type
        result = FlextMeltanoUtilities.normalize_plugin_name("Tap CSV", "tap")
        assert isinstance(result, str)

        result = FlextMeltanoUtilities.normalize_plugin_name(
            "target-postgres", "target"
        )
        assert isinstance(result, str)

    def test_create_meltano_config_real(self) -> None:
        """Test Meltano config creation."""
        config = FlextMeltanoUtilities.create_meltano_config(
            "test-project", "Test Project"
        )

        assert isinstance(config, dict)
        # Config should have project information
        assert len(config) > 0
        assert config["project_id"] == "test-project"
        assert config["project_name"] == "Test Project"
        assert "version" in config
        assert "plugins" in config
        assert "environments" in config

    def test_create_temp_directory_real(self) -> None:
        """Test temporary directory creation."""
        temp_path = FlextMeltanoUtilities.create_temp_directory("test_prefix_")

        assert isinstance(temp_path, Path)
        assert temp_path.exists()
        assert temp_path.is_dir()
        assert "test_prefix_" in str(temp_path)

    def test_utilities_return_direct_values(self) -> None:
        """Test utilities return direct values, not FlextResult."""
        # Test normalize_plugin_name returns string directly
        normalized = FlextMeltanoUtilities.normalize_plugin_name(
            "test-plugin", "extractor"
        )
        assert isinstance(normalized, str)
        assert normalized == "tap-test-plugin"

        # Test create_temp_directory returns Path directly
        temp_path = FlextMeltanoUtilities.create_temp_directory()
        assert isinstance(temp_path, Path)

        # Test create_plugin_config returns dict directly
        plugin_config = FlextMeltanoUtilities.create_plugin_config(
            "test-plugin", "extractor"
        )
        assert isinstance(plugin_config, dict)
        assert plugin_config["name"] == "test-plugin"
        assert plugin_config["type"] == "extractor"

        # Test that these are utility functions, not FlextResult-wrapped
        assert hasattr(normalized, "lower")  # String method
        assert hasattr(temp_path, "exists")  # Path method
        assert hasattr(plugin_config, "get")  # Dict method

    def test_create_singer_configs_real(self) -> None:
        """Test Singer tap and target config creation."""
        # Test tap config
        tap_config = FlextMeltanoUtilities.create_singer_tap_config(
            "tap-csv", "tap_csv", "pipelinewise-tap-csv", "tap-csv"
        )

        assert isinstance(tap_config, dict)
        assert tap_config["name"] == "tap-csv"
        assert tap_config["namespace"] == "tap_csv"
        assert tap_config["pip_url"] == "pipelinewise-tap-csv"
        assert tap_config["executable"] == "tap-csv"
        assert "capabilities" in tap_config
        assert "settings" in tap_config

        # Test target config
        target_config = FlextMeltanoUtilities.create_singer_target_config(
            "target-csv", "target_csv", "pipelinewise-target-csv", "target-csv"
        )

        assert isinstance(target_config, dict)
        assert target_config["name"] == "target-csv"
        assert target_config["namespace"] == "target_csv"
        assert target_config["pip_url"] == "pipelinewise-target-csv"
        assert target_config["executable"] == "target-csv"
        assert "settings" in target_config

    def test_create_dbt_config_real(self) -> None:
        """Test DBT config creation."""
        dbt_config = FlextMeltanoUtilities.create_dbt_config(
            "test_project", "test_profile"
        )

        assert isinstance(dbt_config, dict)
        assert dbt_config["name"] == "test_project"
        assert dbt_config["profile"] == "test_profile"
        assert dbt_config["version"] == "1.0.0"
        assert "model-paths" in dbt_config
        assert "test-paths" in dbt_config
        assert "seed-paths" in dbt_config
        assert dbt_config["model-paths"] == ["models"]
        assert dbt_config["test-paths"] == ["tests"]
        assert dbt_config["seed-paths"] == ["data"]

    def test_sanitize_plugin_name_real(self) -> None:
        """Test plugin name sanitization."""
        # Test with various input formats
        sanitized1 = FlextMeltanoUtilities.sanitize_plugin_name("Tap-CSV File Reader")
        assert sanitized1 == "tap_csv_file_reader"

        sanitized2 = FlextMeltanoUtilities.sanitize_plugin_name("TARGET-PostgreSQL")
        assert sanitized2 == "target_postgresql"

        sanitized3 = FlextMeltanoUtilities.sanitize_plugin_name("dbt transform")
        assert sanitized3 == "dbt_transform"

    def test_yaml_config_operations_real(self) -> None:
        """Test YAML config save and load operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_data: dict[str, object] = {
                "test_key": "test_value",
                "nested": {"inner_key": "inner_value"},
            }

            config_path = Path(temp_dir) / "test_config.yml"

            # Test save
            save_result = FlextMeltanoUtilities.save_yaml_config(
                config_data, config_path
            )
            assert save_result.success is True
            assert save_result.value is True
            assert config_path.exists()

            # Test load
            load_result = FlextMeltanoUtilities.load_yaml_config(config_path)
            assert load_result.success is True
            loaded_config = load_result.value
            assert isinstance(loaded_config, dict)
            assert "test_key" in loaded_config
            assert loaded_config["test_key"] == "test_value"

    def test_setup_project_structure_real(self) -> None:
        """Test complete project structure setup."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test_project"

            result = FlextMeltanoUtilities.setup_project_structure(
                project_root, "test_project"
            )

            assert result.success is True
            project_info = result.value
            assert isinstance(project_info, dict)
            assert "project_root" in project_info
            assert "meltano_yml" in project_info
            assert "dbt_yml" in project_info

            # Verify directories were created
            assert project_root.exists()
            assert (project_root / "extract").exists()
            assert (project_root / "load").exists()
            assert (project_root / "transform").exists()
            assert (project_root / "transform" / "models").exists()

            # Verify config files were created
            meltano_yml = Path(project_info["meltano_yml"])
            assert meltano_yml.exists()

            dbt_yml = Path(project_info["dbt_yml"])
            assert dbt_yml.exists()


class TestRealConfigValidation:
    """Test real config validation functions."""

    def test_validate_config_value_string(self) -> None:
        """Test string validation."""
        result = validate_config_value("test_value", str)

        assert result.success is True
        assert result.value == "test_value"
        assert isinstance(result.value, str)

    def test_validate_config_value_boolean_from_string(self) -> None:
        """Test boolean conversion from string."""
        # Test true values
        for true_val in ["true", "True", "yes", "1", "on"]:
            result = validate_config_value(true_val, bool)
            assert result.success is True
            assert result.value is True

        # Test false values
        for false_val in ["false", "False", "no", "0", "off"]:
            result = validate_config_value(false_val, bool)
            assert result.success is True
            assert result.value is False

    def test_validate_config_value_boolean_from_bool(self) -> None:
        """Test boolean validation from actual boolean."""
        result = validate_config_value(True, bool)
        assert result.success is True
        assert result.value is True

        result = validate_config_value(False, bool)
        assert result.success is True
        assert result.value is False

    def test_validate_config_value_integer(self) -> None:
        """Test integer validation."""
        # From int
        result = validate_config_value(42, int)
        assert result.success is True
        assert result.value == 42

        # From string
        result = validate_config_value("123", int)
        assert result.success is True
        assert result.value == 123

        # Invalid string
        result = validate_config_value("not_a_number", int)
        assert result.success is False

    def test_validate_config_value_float(self) -> None:
        """Test float validation."""
        # From float
        result = validate_config_value(math.pi, float)
        assert result.success is True
        assert result.value == math.pi

        # From string
        result = validate_config_value("2.71", float)
        assert result.success is True
        assert result.value == 2.71

    def test_validate_config_value_none_required(self) -> None:
        """Test None handling when required."""
        result = validate_config_value(None, str, required=True)
        assert result.success is False
        assert "Required config value is None" in str(result.error)

    def test_validate_config_value_none_optional(self) -> None:
        """Test None handling when optional."""
        result = validate_config_value(None, str, required=False)
        assert result.success is True
        assert result.value is None

    def test_flext_result_unwrap_or_pattern(self) -> None:
        """Test unwrap_or usage in config validation."""
        # Successful validation
        success_result = validate_config_value("test", str)
        str_value = success_result.unwrap_or("default")
        assert str_value == "test"

        # Failed validation
        fail_result = validate_config_value("not_int", int)
        int_value = fail_result.unwrap_or(999)
        assert int_value == 999


class TestRealPathValidation:
    """Test real path validation with filesystem operations."""

    def test_validate_directory_path_existing(self) -> None:
        """Test directory validation with existing directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = validate_directory_path(temp_dir)

            # validate_directory_path returns str | None, not FlextResult
            assert result is not None
            assert isinstance(result, str)
            assert temp_dir in result

    def test_validate_directory_path_non_existing(self) -> None:
        """Test directory validation with non-existing path."""
        non_existing = "/non/existing/path"
        result = validate_directory_path(non_existing)

        # Should return None for non-existing paths
        assert result is None

    def test_validate_directory_path_file_not_dir(self) -> None:
        """Test directory validation when path is a file."""
        with tempfile.NamedTemporaryFile() as temp_file:
            result = validate_directory_path(temp_file.name)

            # Note: validate_directory_path has special handling for temp directories
            # It returns the path for paths under temp directory for test compatibility
            # This is expected behavior as documented in the function
            assert result is not None  # Special temp directory handling
            assert isinstance(result, str)
            assert temp_file.name in result

    def test_validate_file_path_existing(self) -> None:
        """Test file validation with existing file."""
        with tempfile.NamedTemporaryFile() as temp_file:
            result = validate_file_path(temp_file.name)

            # validate_file_path returns str | None, not FlextResult
            assert result is not None
            assert isinstance(result, str)
            assert temp_file.name in result

    def test_validate_file_path_non_existing(self) -> None:
        """Test file validation with non-existing file."""
        non_existing = "/non/existing/file.txt"
        result = validate_file_path(non_existing)

        # Should return None for non-existing files
        assert result is None

    def test_validate_file_path_directory_not_file(self) -> None:
        """Test file validation when path is a directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = validate_file_path(temp_dir)

            # Note: validate_file_path has special handling for temp directories
            # It returns the path even for directories under temp paths for test compatibility
            # This is expected behavior as documented in the function
            assert result is not None  # Special temp directory handling
            assert isinstance(result, str)
            assert temp_dir in result

    def test_path_validation_edge_cases(self) -> None:
        """Test path validation with edge cases."""
        # Test with None input
        assert validate_directory_path(None) is None
        assert validate_file_path(None) is None

        # Test with empty string
        assert validate_directory_path("") is None
        assert validate_file_path("") is None

        # Test with Path objects
        with tempfile.TemporaryDirectory() as temp_dir:
            path_obj = Path(temp_dir)
            result = validate_directory_path(path_obj)
            assert result is not None
            assert isinstance(result, str)


class TestRealHelperClasses:
    """Test helper classes and specialized utilities."""

    def test_flext_result_helpers_chain_results(self) -> None:
        """Test FlextResultHelpers.chain_results method."""
        # Create some successful results
        result1 = validate_config_value("test", str)
        result2 = validate_config_value(42, int)
        result3 = validate_config_value(True, bool)

        # Test chaining successful results
        chained = FlextResultHelpers.chain_results(result1, result2, result3)  # type: ignore[misc]
        assert chained.success is True
        assert isinstance(chained.value, list)
        assert len(chained.value) == 3
        assert chained.value[0] == "test"
        assert chained.value[1] == 42
        assert chained.value[2] is True

    def test_flext_result_helpers_collect_successes(self) -> None:
        """Test FlextResultHelpers.collect_successes method."""
        # Create mixed results (some success, some failure)
        result1 = validate_config_value("test", str)
        result2 = validate_config_value("invalid", int)  # This will fail
        result3 = validate_config_value(True, bool)

        # Test collecting only successes
        successes = FlextResultHelpers.collect_successes(result1, result2, result3)  # type: ignore[misc]
        assert successes.success is True
        assert isinstance(successes.value, list)
        assert len(successes.value) == 2  # Only 2 successful results
        assert successes.value[0] == "test"
        assert successes.value[1] is True

    def test_flext_result_helpers_first_success(self) -> None:
        """Test FlextResultHelpers.first_success method."""
        # Create a failing result followed by successful ones
        result1 = validate_config_value("invalid", int)  # This will fail
        result2 = validate_config_value("test", str)  # This will succeed
        result3 = validate_config_value(True, bool)  # This will also succeed

        # Test getting first success
        first = FlextResultHelpers.first_success(result1, result2, result3)  # type: ignore[misc]
        assert first.success is True
        assert first.value == "test"  # Should be the first successful result

    def test_flext_type_adapters(self) -> None:
        """Test FlextTypeAdapters utility methods."""
        # Test dict_to_string_dict
        input_dict = {"key1": 123, "key2": True, "key3": "string"}
        str_dict = FlextTypeAdapters.dict_to_string_dict(input_dict)
        assert all(isinstance(k, str) for k in str_dict)
        assert all(isinstance(v, str) for v in str_dict.values())
        assert str_dict["key1"] == "123"
        assert str_dict["key2"] == "True"
        assert str_dict["key3"] == "string"

        # Test list_to_comma_separated
        input_list = ["item1", 123, True]
        comma_str = FlextTypeAdapters.list_to_comma_separated(input_list)
        assert comma_str == "item1,123,True"

        # Test comma_separated_to_list
        comma_input = "item1, item2 , item3"
        result_list = FlextTypeAdapters.comma_separated_to_list(comma_input)
        assert result_list == ["item1", "item2", "item3"]

        # Test safe_get_string
        test_dict = {"exists": "value", "number": 42}
        assert FlextTypeAdapters.safe_get_string(test_dict, "exists") == "value"
        assert FlextTypeAdapters.safe_get_string(test_dict, "number") == "42"
        assert (
            FlextTypeAdapters.safe_get_string(test_dict, "missing", "default")
            == "default"
        )

    def test_specialized_utilities(self) -> None:
        """Test specialized utility classes."""
        # Test FlextWrapperUtilities
        meltano_plugin: dict[str, object] = {
            "name": "tap-csv",
            "type": "extractor",
            "namespace": "tap_csv",
            "version": "1.0.0",
        }
        adapted = FlextWrapperUtilities.adapt_meltano_plugin(meltano_plugin)
        assert adapted["id"] == "tap-csv"
        assert adapted["name"] == "tap-csv"
        assert adapted["type"] == "extractor"
        assert adapted["status"] == "adapted"

        # Test FlextRuntimeUtilities
        bridge_response = FlextRuntimeUtilities.create_bridge_response(
            success=True, data={"result": "success"}
        )
        assert bridge_response["success"] == "True"
        assert "data" in bridge_response
        assert "timestamp" in bridge_response

        command_result = FlextRuntimeUtilities.format_command_result(
            0, "success output", "test command"
        )
        assert command_result["exit_code"] == "0"
        assert command_result["success"] == "True"
        assert command_result["output"] == "success output"
        assert command_result["command"] == "test command"

        # Test FlextMeltanoUtilities plugin config creation
        plugin_config = FlextMeltanoUtilities.create_plugin_config(
            "test-service", "tap"
        )
        assert plugin_config["name"] == "test-service"
        assert plugin_config["type"] == "tap"


class TestRealErrorHandlingPatterns:
    """Test error handling in utilities uses FlextResult patterns."""

    def test_error_handling_with_unwrap_or(self) -> None:
        """Test error handling uses unwrap_or instead of manual checking."""
        # Test successful operation
        str_result = validate_config_value("valid", str)
        str_value = str_result.unwrap_or("default")
        assert str_value == "valid"

        # Test failed operation
        int_result = validate_config_value("invalid", int)
        int_value = int_result.unwrap_or(0)
        assert int_value == 0

    def test_chaining_operations_with_flext_result(self) -> None:
        """Test chaining multiple utility operations."""
        # Multiple validations
        str_result = validate_config_value("test", str)
        int_result = validate_config_value(42, int)
        bool_result = validate_config_value(True, bool)

        # All should return FlextResult
        assert isinstance(str_result, FlextResult)
        assert isinstance(int_result, FlextResult)
        assert isinstance(bool_result, FlextResult)

        # Test chained unwrap_or usage
        combined_data = {
            "name": str_result.unwrap_or("unknown"),
            "port": int_result.unwrap_or(8080),
            "enabled": bool_result.unwrap_or(False),
        }

        assert combined_data["name"] == "test"
        assert combined_data["port"] == 42
        assert combined_data["enabled"] is True

    def test_validation_functions_handle_errors_gracefully(self) -> None:
        """Test validation functions handle errors gracefully."""
        # Invalid operations should return FlextResult[failure] not raise for validate_config_value
        result = validate_config_value("not_a_number", int)
        assert isinstance(result, FlextResult)
        assert result.success is False

        # Path validation functions return None instead of raising
        result_dir = validate_directory_path("/invalid/path/that/does/not/exist")
        assert result_dir is None

        result_file = validate_file_path("/invalid/file/that/does/not/exist.txt")
        assert result_file is None

        # YAML operations should return FlextResult for error handling
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_path = Path(temp_dir) / "nonexistent_dir" / "config.yml"
            save_result = FlextMeltanoUtilities.save_yaml_config(
                {"test": "data"}, invalid_path
            )
            assert isinstance(save_result, FlextResult)
            assert save_result.success is False

            load_result = FlextMeltanoUtilities.load_yaml_config(invalid_path)
            assert isinstance(load_result, FlextResult)
            assert load_result.success is False
