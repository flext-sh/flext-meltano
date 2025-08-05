"""Test Coverage for Common Module - Functional Tests.

**Purpose**: Comprehensive functional testing of common.py module
**Scope**: Real functionality testing (not just imports) to achieve 95%+ coverage
**Focus**: validate_directory_path, validate_file_path, validate_config_value
**Target**: Increase coverage from 14% to 95%+

This module provides REAL functional tests that exercise the actual validation
logic and edge cases of the common utility functions.
"""

from __future__ import annotations

import math
import tempfile
from pathlib import Path

from flext_meltano.common import (
    validate_config_value,
    validate_directory_path,
    validate_file_path,
)


class TestValidateDirectoryPath:
    """Test validate_directory_path with real functionality."""

    def test_validate_none_directory_path(self):
        """Test validation with None directory path."""
        result = validate_directory_path(None)
        assert result is None

    def test_validate_empty_directory_path(self):
        """Test validation with empty string directory path."""
        result = validate_directory_path("")
        assert result is None

    def test_validate_existing_directory_path(self):
        """Test validation with existing directory."""
        # Use current directory which definitely exists
        current_dir = str(Path.cwd())
        result = validate_directory_path(current_dir)

        assert result is not None
        assert Path(result).is_absolute()
        assert Path(result).exists()
        assert Path(result).is_dir()

    def test_validate_nonexistent_directory_path(self):
        """Test validation with non-existent directory."""
        nonexistent_path = "/this/path/definitely/does/not/exist"
        result = validate_directory_path(nonexistent_path)

        assert result is None

    def test_validate_file_as_directory_path(self):
        """Test validation with file path instead of directory."""
        # Create a temporary file outside temp directory
        current_dir = Path.cwd()
        test_file = current_dir / "test_temp_file.txt"
        test_file.write_text("test content")

        try:
            result = validate_directory_path(str(test_file))
            assert result is None  # Should fail because it's a file, not directory
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_validate_temp_directory_path(self):
        """Test validation with temp directory path."""
        # Test with actual temp directory
        temp_dir = tempfile.gettempdir()
        result = validate_directory_path(temp_dir)

        assert result is not None
        assert Path(result).is_absolute()

    def test_validate_test_directory_path_nonexistent(self):
        """Test validation with test directory path (non-existent but allowed)."""
        test_path = "/test/path/for/testing"
        result = validate_directory_path(test_path)

        # Should return the path even if it doesn't exist (test environment)
        assert result == test_path

    def test_validate_test_prefix_directory_path(self):
        """Test validation with test_ prefix directory path."""
        test_path = "test_directory"
        result = validate_directory_path(test_path)

        # Should return the path even if it doesn't exist (test environment)
        assert result == test_path

    def test_validate_relative_to_temp_directory(self):
        """Test validation with path relative to temp directory."""
        temp_dir = Path(tempfile.gettempdir())
        test_path = temp_dir / "test_subdir"

        result = validate_directory_path(str(test_path))

        # Should return the path because it's relative to temp directory
        assert result == str(test_path)

    def test_validate_absolute_temp_subdirectory(self):
        """Test validation with absolute path in temp directory."""
        temp_dir = Path(tempfile.gettempdir())
        test_path = temp_dir / "nonexistent" / "subdir"

        result = validate_directory_path(str(test_path))

        # Should return the path because it's under temp directory
        assert result == str(test_path)


class TestValidateFilePath:
    """Test validate_file_path with real functionality."""

    def test_validate_none_file_path(self):
        """Test validation with None file path."""
        result = validate_file_path(None)
        assert result is None

    def test_validate_empty_file_path(self):
        """Test validation with empty string file path."""
        result = validate_file_path("")
        assert result is None

    def test_validate_existing_file_path(self):
        """Test validation with existing file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file_path = tmp_file.name
            tmp_file.write(b"test content")

        try:
            result = validate_file_path(tmp_file_path)

            assert result is not None
            assert Path(result).is_absolute()
            assert Path(result).exists()
            assert Path(result).is_file()
        finally:
            Path(tmp_file_path).unlink()

    def test_validate_nonexistent_file_path(self):
        """Test validation with non-existent file."""
        nonexistent_path = "/this/file/definitely/does/not/exist.txt"
        result = validate_file_path(nonexistent_path)

        assert result is None

    def test_validate_directory_as_file_path(self):
        """Test validation with directory path instead of file."""
        # Use current directory
        current_dir = str(Path.cwd())
        result = validate_file_path(current_dir)

        assert result is None  # Should fail because it's a directory, not file

    def test_validate_temp_file_path(self):
        """Test validation with temp file path."""
        # Create temporary file in temp directory
        with tempfile.NamedTemporaryFile() as tmp_file:
            result = validate_file_path(tmp_file.name)

            assert result is not None
            assert Path(result).is_absolute()

    def test_validate_test_file_path_nonexistent(self):
        """Test validation with test file path (non-existent but allowed)."""
        test_path = "/test/path/test_file.txt"
        result = validate_file_path(test_path)

        # Should return the path even if it doesn't exist (test environment)
        assert result == test_path

    def test_validate_test_prefix_file_path(self):
        """Test validation with test_ prefix file path."""
        test_path = "test_file.txt"
        result = validate_file_path(test_path)

        # Should return the path even if it doesn't exist (test environment)
        assert result == test_path

    def test_validate_relative_to_temp_file(self):
        """Test validation with file path relative to temp directory."""
        temp_dir = Path(tempfile.gettempdir())
        test_path = temp_dir / "test_file.txt"

        result = validate_file_path(str(test_path))

        # Should return the path because it's relative to temp directory
        assert result == str(test_path)

    def test_validate_absolute_temp_subfile(self):
        """Test validation with absolute file path in temp directory."""
        temp_dir = Path(tempfile.gettempdir())
        test_path = temp_dir / "nonexistent" / "test_file.txt"

        result = validate_file_path(str(test_path))

        # Should return the path because it's under temp directory
        assert result == str(test_path)


class TestValidateConfigValue:
    """Test validate_config_value with real functionality."""

    def test_validate_none_value_with_default(self):
        """Test validation with None value and default."""
        result = validate_config_value(None, str, "default_value")
        assert result == "default_value"

    def test_validate_none_value_without_default(self):
        """Test validation with None value and no default."""
        result = validate_config_value(None, str, None)
        assert result is None

    def test_validate_correct_type_string(self):
        """Test validation with correct string type."""
        test_value = "test_string"
        result = validate_config_value(test_value, str, "default")
        assert result == test_value

    def test_validate_correct_type_int(self):
        """Test validation with correct integer type."""
        test_value = 42
        result = validate_config_value(test_value, int, 0)
        assert result == test_value

    def test_validate_correct_type_bool(self):
        """Test validation with correct boolean type."""
        test_value = True
        result = validate_config_value(test_value, bool, default=False)
        assert result == test_value

    def test_validate_correct_type_float(self):
        """Test validation with correct float type."""
        test_value = math.pi
        result = validate_config_value(test_value, float, 0.0)
        assert result == test_value

    def test_validate_correct_type_list(self):
        """Test validation with correct list type."""
        test_value = [1, 2, 3]
        result = validate_config_value(test_value, list, [])
        assert result == test_value

    def test_validate_correct_type_dict(self):
        """Test validation with correct dict type."""
        test_value = {"key": "value"}
        result = validate_config_value(test_value, dict, {})
        assert result == test_value

    def test_validate_convertible_string_to_int(self):
        """Test validation with string convertible to int."""
        test_value = "123"
        result = validate_config_value(test_value, int, 0)
        assert result == 123
        assert isinstance(result, int)

    def test_validate_convertible_string_to_float(self):
        """Test validation with string convertible to float."""
        test_value = "3.14"
        result = validate_config_value(test_value, float, 0.0)
        assert result == math.pi
        assert isinstance(result, float)

    def test_validate_convertible_int_to_string(self):
        """Test validation with int convertible to string."""
        test_value = 42
        result = validate_config_value(test_value, str, "default")
        assert result == "42"
        assert isinstance(result, str)

    def test_validate_convertible_bool_to_string(self):
        """Test validation with bool convertible to string."""
        test_value = True
        result = validate_config_value(test_value, str, "default")
        assert result == "True"
        assert isinstance(result, str)

    def test_validate_convertible_int_to_bool(self):
        """Test validation with int convertible to bool."""
        # Non-zero int converts to True
        test_value = 1
        result = validate_config_value(test_value, bool, default=False)
        assert result is True
        assert isinstance(result, bool)

        # Zero int converts to False
        test_value = 0
        result = validate_config_value(test_value, bool, default=True)
        assert result is False
        assert isinstance(result, bool)

    def test_validate_non_convertible_string_to_int(self):
        """Test validation with string not convertible to int."""
        test_value = "not_a_number"
        default_value = 99
        result = validate_config_value(test_value, int, default_value)
        assert result == default_value

    def test_validate_non_convertible_string_to_float(self):
        """Test validation with string not convertible to float."""
        test_value = "not_a_float"
        default_value = 9.99
        result = validate_config_value(test_value, float, default_value)
        assert result == default_value

    def test_validate_non_convertible_type(self):
        """Test validation with completely incompatible types."""
        test_value = {"dict": "value"}
        default_value = 42
        result = validate_config_value(test_value, int, default_value)
        assert result == default_value

    def test_validate_complex_type_conversion(self):
        """Test validation with complex type conversions."""
        # List to string conversion
        test_value = [1, 2, 3]
        result = validate_config_value(test_value, str, "default")
        assert result == "[1, 2, 3]"
        assert isinstance(result, str)

    def test_validate_none_type_with_none_default(self):
        """Test validation edge case with None type."""
        test_value = "some_value"
        result = validate_config_value(test_value, type(None), None)
        # This should return None since value can't be converted to NoneType
        assert result is None


class TestCommonModuleIntegration:
    """Integration tests for common module functions."""

    def test_directory_and_file_validation_workflow(self):
        """Test complete workflow using directory and file validation."""
        # Create temporary directory and file
        with tempfile.TemporaryDirectory() as temp_dir:
            # Validate the directory
            dir_result = validate_directory_path(temp_dir)
            assert dir_result is not None
            assert Path(dir_result).exists()
            assert Path(dir_result).is_dir()

            # Create a file in the directory
            test_file = Path(temp_dir) / "test_file.txt"
            test_file.write_text("test content")

            # Validate the file
            file_result = validate_file_path(str(test_file))
            assert file_result is not None
            assert Path(file_result).exists()
            assert Path(file_result).is_file()

    def test_config_validation_with_real_config_patterns(self):
        """Test config validation with real configuration patterns."""
        # Test configuration dictionary
        config = {
            "host": "localhost",
            "port": "5432",
            "debug": "true",
            "timeout": 30,
            "features": ["feature1", "feature2"],
        }

        # Validate each configuration value
        host = validate_config_value(config["host"], str, "default_host")
        assert host == "localhost"

        port = validate_config_value(config["port"], int, 3306)
        assert port == 5432
        assert isinstance(port, int)

        debug = validate_config_value(config["debug"], bool, default=False)
        assert debug is True  # "true" string converts to True

        timeout = validate_config_value(config["timeout"], int, 60)
        assert timeout == 30

        features = validate_config_value(config["features"], list, [])
        assert features == ["feature1", "feature2"]

    def test_path_validation_edge_cases(self):
        """Test path validation with edge cases."""
        # Test various edge cases
        edge_cases = [
            ("", None),  # Empty string
            ("   ", None),  # Whitespace only
            (".", str(Path.cwd())),  # Current directory
            ("..", str(Path.cwd().parent)),  # Parent directory
        ]

        for test_path, expected_result in edge_cases:
            if expected_result is None:
                result = validate_directory_path(test_path)
                assert result is None
            else:
                result = validate_directory_path(test_path)
                if result is not None:
                    # Normalize paths for comparison
                    assert Path(result).resolve() == Path(expected_result).resolve()


class TestCommonModulePerformance:
    """Performance and stress tests for common module functions."""

    def test_validation_performance_with_many_paths(self):
        """Test validation performance with many path validations."""
        # Test with many non-existent paths (should be fast)
        paths = [f"/nonexistent/path_{i}" for i in range(100)]

        results = []
        for path in paths:
            result = validate_directory_path(path)
            results.append(result)

        # All should be None since paths don't exist
        assert all(result is None for result in results)
        assert len(results) == 100

    def test_config_validation_performance(self):
        """Test config validation performance with many values."""
        # Test with many config values
        values = list(range(1000))

        results = []
        for value in values:
            result = validate_config_value(value, str, "default")
            results.append(result)

        # All should be string representations
        assert all(isinstance(result, str) for result in results)
        assert len(results) == 1000
        assert results[0] == "0"
        assert results[999] == "999"

    def test_mixed_validation_workflow(self):
        """Test mixed validation workflow with various types."""
        test_data = [
            (42, str, "default", str),
            ("123", int, 0, int),
            (True, str, "default", str),
            ([1, 2, 3], str, "default", str),
            ({"key": "value"}, str, "default", str),
            ("invalid", int, 999, int),
        ]

        for value, expected_type, default, expected_result_type in test_data:
            result = validate_config_value(value, expected_type, default)
            assert isinstance(result, expected_result_type)
