"""Comprehensive unit tests for FlextMeltanoUtilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import mock_open, patch

import yaml

from flext_core import (
    FlextResult,
    FlextUtilities,
)
from flext_meltano.utilities import FlextMeltanoUtilities


class TestFlextMeltanoUtilitiesInitialization:
    """Test FlextMeltanoUtilities initialization and inheritance."""

    def test_utilities_inheritance(self) -> None:
        """Test utilities properly inherits from FlextUtilities."""
        utilities = FlextMeltanoUtilities()

        assert isinstance(utilities, FlextUtilities)
        assert hasattr(utilities, "create_meltano_config_dict")
        assert hasattr(utilities, "validate_meltano_project_structure")
        assert hasattr(utilities, "create_meltano_project_file")

    def test_utilities_class_methods(self) -> None:
        """Test utilities class methods are accessible."""
        # Test that class methods can be called without instantiation
        result = FlextMeltanoUtilities.create_meltano_config_dict("test_project")
        assert isinstance(result, FlextResult)


class TestFlextMeltanoUtilitiesConfigCreation:
    """Test configuration dictionary creation functionality."""

    def test_create_meltano_config_dict_success(self) -> None:
        """Test successful Meltano configuration dictionary creation."""
        result = FlextMeltanoUtilities.create_meltano_config_dict(
            project_id="test_project", project_name="Test Project"
        )

        assert result.is_success
        assert result.data is not None
        assert result.data["version"] == 1
        assert result.data["project_id"] == "safe_project_id"
        assert result.data["project_name"] == "safe_project_name"
        assert "environments" in result.data
        assert "plugins" in result.data

    def test_create_meltano_config_dict_default_project_name(self) -> None:
        """Test configuration creation with default project name."""
        result = FlextMeltanoUtilities.create_meltano_config_dict(
            project_id="test_project"
        )

        assert result.is_success
        assert result.data["project_name"] == "safe_project_id"

    def test_create_meltano_config_dict_empty_project_id(self) -> None:
        """Test configuration creation with empty project ID."""
        result = FlextMeltanoUtilities.create_meltano_config_dict(
            project_id="", project_name="Test Project"
        )

        assert result.is_failure
        assert result.error is not None and "Project ID cannot be empty" in result.error

    def test_create_meltano_config_dict_whitespace_project_id(self) -> None:
        """Test configuration creation with whitespace-only project ID."""
        result = FlextMeltanoUtilities.create_meltano_config_dict(
            project_id="   ", project_name="Test Project"
        )

        assert result.is_failure
        assert result.error is not None and "Project ID cannot be empty" in result.error

    def test_create_meltano_config_dict_invalid_project_id_type(self) -> None:
        """Test configuration creation with invalid project ID type."""
        result = FlextMeltanoUtilities.create_meltano_config_dict(
            project_id=123,
            project_name="Test Project",
        )

        assert result.is_failure
        assert (
            result.error is not None
            and "'int' object has no attribute 'strip'" in result.error
        )


class TestFlextMeltanoUtilitiesProjectValidation:
    """Test project structure validation functionality."""

    def test_validate_meltano_project_structure_success(self) -> None:
        """Test successful project structure validation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create required directories
            (project_path / "meltano.yml").touch()
            (project_path / "plugins").mkdir()
            (project_path / "transform").mkdir()
            (project_path / "schemas").mkdir()

            result = FlextMeltanoUtilities.validate_meltano_project_structure(
                project_path
            )

            assert result.is_success
            assert result.data["valid"] is True
            assert "meltano.yml" in result.data["required_files"]
            assert "plugins" in result.data["required_directories"]

    def test_validate_meltano_project_structure_missing_files(self) -> None:
        """Test project structure validation with missing files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create only some directories
            (project_path / "plugins").mkdir()

            result = FlextMeltanoUtilities.validate_meltano_project_structure(
                project_path
            )

            assert result.is_failure
            assert result.error is not None and "Missing required files" in result.error

    def test_validate_meltano_project_structure_missing_directories(self) -> None:
        """Test project structure validation with missing directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create only meltano.yml file
            (project_path / "meltano.yml").touch()

            result = FlextMeltanoUtilities.validate_meltano_project_structure(
                project_path
            )

            assert result.is_failure
            assert (
                result.error is not None
                and "Missing required directories" in result.error
            )

    def test_validate_meltano_project_structure_nonexistent_path(self) -> None:
        """Test project structure validation with nonexistent path."""
        result = FlextMeltanoUtilities.validate_meltano_project_structure(
            Path("/nonexistent/path")
        )

        assert result.is_failure
        assert (
            result.error is not None and "Project path does not exist" in result.error
        )

    def test_validate_meltano_project_structure_invalid_path_type(self) -> None:
        """Test project structure validation with invalid path type."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = FlextMeltanoUtilities.validate_meltano_project_structure(temp_dir)

        assert result.is_failure
        assert (
            result.error is not None
            and "Project path must be a Path object" in result.error
        )


class TestFlextMeltanoUtilitiesFileCreation:
    """Test file creation functionality."""

    def test_create_meltano_project_file_success(self) -> None:
        """Test successful Meltano project file creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            config_data = {
                "version": 1,
                "project_id": "test_project",
                "project_name": "Test Project",
            }

            result = FlextMeltanoUtilities.create_meltano_project_file(
                project_path=project_path, config_data=config_data
            )

            assert result.is_success
            assert result.data["file_created"] is True
            assert (project_path / "meltano.yml").exists()

    def test_create_meltano_project_file_invalid_path(self) -> None:
        """Test project file creation with invalid path."""
        config_data = {"version": 1, "project_id": "test_project"}

        result = FlextMeltanoUtilities.create_meltano_project_file(
            project_path=Path("/invalid/path"), config_data=config_data
        )

        assert result.is_failure
        assert result.error is not None and "Cannot create file" in result.error

    def test_create_meltano_project_file_invalid_config(self) -> None:
        """Test project file creation with invalid config data."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Invalid config data (not a dict)
            config_data = "invalid_config"

            result = FlextMeltanoUtilities.create_meltano_project_file(
                project_path=project_path, config_data=config_data
            )

            assert result.is_failure
            assert (
                result.error is not None
                and "Config data must be a dictionary" in result.error
            )

    def test_create_meltano_project_file_empty_config(self) -> None:
        """Test project file creation with empty config data."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            result = FlextMeltanoUtilities.create_meltano_project_file(
                project_path=project_path, config_data={}
            )

            assert result.is_failure
            assert (
                result.error is not None
                and "Config data cannot be empty" in result.error
            )


class TestFlextMeltanoUtilitiesYamlOperations:
    """Test YAML operations functionality."""

    def test_load_yaml_file_success(self) -> None:
        """Test successful YAML file loading."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = Path(temp_dir) / "test.yml"

            test_data = {
                "version": 1,
                "project_id": "test_project",
                "plugins": ["tap-postgres", "target-postgres"],
            }

            with Path(yaml_file).open("w", encoding="utf-8") as f:
                yaml.dump(test_data, f)

            result = FlextMeltanoUtilities.load_yaml_file(yaml_file)

            assert result.is_success
            assert result.data["version"] == 1
            assert result.data["project_id"] == "test_project"
            assert len(result.data["plugins"]) == 2

    def test_load_yaml_file_nonexistent(self) -> None:
        """Test YAML file loading with nonexistent file."""
        result = FlextMeltanoUtilities.load_yaml_file(Path("/nonexistent/file.yml"))

        assert result.is_failure
        assert result.error is not None and "File does not exist" in result.error

    def test_load_yaml_file_invalid_yaml(self) -> None:
        """Test YAML file loading with invalid YAML content."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = Path(temp_dir) / "invalid.yml"

            # Write invalid YAML content
            with Path(yaml_file).open("w", encoding="utf-8") as f:
                f.write("invalid: yaml: content: [")

            result = FlextMeltanoUtilities.load_yaml_file(yaml_file)

            assert result.is_failure
            assert result.error is not None and "Invalid YAML format" in result.error

    def test_save_yaml_file_success(self) -> None:
        """Test successful YAML file saving."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = Path(temp_dir) / "test.yml"

            test_data = {
                "version": 1,
                "project_id": "test_project",
                "plugins": ["tap-postgres", "target-postgres"],
            }

            result = FlextMeltanoUtilities.save_yaml_file(yaml_file, test_data)

            assert result.is_success
            assert result.data["file_saved"] is True
            assert yaml_file.exists()

    def test_save_yaml_file_invalid_data(self) -> None:
        """Test YAML file saving with invalid data."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = Path(temp_dir) / "test.yml"

            # Invalid data (not serializable)
            invalid_data = {"func": lambda x: x}  # Functions are not serializable

            result = FlextMeltanoUtilities.save_yaml_file(yaml_file, invalid_data)

            assert result.is_failure
            assert result.error is not None and "Cannot serialize data" in result.error

    def test_save_yaml_file_invalid_path(self) -> None:
        """Test YAML file saving with invalid path."""
        test_data = {"version": 1, "project_id": "test_project"}

        result = FlextMeltanoUtilities.save_yaml_file(
            Path("/invalid/path/test.yml"), test_data
        )

        assert result.is_failure
        assert result.error is not None and "Cannot create file" in result.error


class TestFlextMeltanoUtilitiesPathOperations:
    """Test path operations functionality."""

    def test_get_project_root_success(self) -> None:
        """Test successful project root detection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create meltano.yml file
            (project_path / "meltano.yml").touch()

            result = FlextMeltanoUtilities.get_project_root(project_path)

            assert result.is_success
            assert result.data["project_root"] == str(project_path)

    def test_get_project_root_no_meltano_file(self) -> None:
        """Test project root detection without meltano.yml file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            result = FlextMeltanoUtilities.get_project_root(project_path)

            assert result.is_failure
            assert (
                result.error is not None and "No meltano.yml file found" in result.error
            )

    def test_get_project_root_nonexistent_path(self) -> None:
        """Test project root detection with nonexistent path."""
        result = FlextMeltanoUtilities.get_project_root(Path("/nonexistent/path"))

        assert result.is_failure
        assert result.error is not None and "Path does not exist" in result.error

    def test_ensure_directory_exists_success(self) -> None:
        """Test successful directory creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            new_dir = base_path / "new_directory"

            result = FlextMeltanoUtilities.ensure_directory_exists(new_dir)

            assert result.is_success
            assert result.data["directory_created"] is True
            assert new_dir.exists()
            assert new_dir.is_dir()

    def test_ensure_directory_exists_already_exists(self) -> None:
        """Test directory creation when directory already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            existing_dir = Path(temp_dir)

            result = FlextMeltanoUtilities.ensure_directory_exists(existing_dir)

            assert result.is_success
            assert result.data["directory_exists"] is True

    def test_ensure_directory_exists_permission_error(self) -> None:
        """Test directory creation with permission error."""
        # Try to create directory in root (should fail due to permissions)
        result = FlextMeltanoUtilities.ensure_directory_exists(
            Path("/root/test_directory")
        )

        assert result.is_failure
        assert result.error is not None and "Permission denied" in result.error


class TestFlextMeltanoUtilitiesErrorHandling:
    """Test error handling and edge cases."""

    def test_utilities_exception_handling(self) -> None:
        """Test utilities handle exceptions gracefully."""
        with patch(
            "flext_meltano.utilities.FlextUtilities.TextProcessor.safe_string"
        ) as mock_safe_string:
            mock_safe_string.side_effect = Exception("Unexpected error")

            result = FlextMeltanoUtilities.create_meltano_config_dict("test_project")

            assert result.is_failure
            assert result.error is not None and "Unexpected error" in result.error

    def test_utilities_file_operation_error(self) -> None:
        """Test utilities handle file operation errors gracefully."""
        with patch("builtins.open", mock_open()) as mock_file:
            mock_file.side_effect = OSError("File operation failed")

            with tempfile.NamedTemporaryFile(suffix=".yml", delete=False) as temp_file:
                result = FlextMeltanoUtilities.save_yaml_file(
                    Path(temp_file.name), {"test": "data"}
                )

            assert result.is_failure
            assert result.error is not None and "File operation failed" in result.error

    def test_utilities_yaml_error_handling(self) -> None:
        """Test utilities handle YAML errors gracefully."""
        with patch("yaml.dump") as mock_yaml_dump:
            mock_yaml_dump.side_effect = yaml.YAMLError("YAML error")

            with tempfile.NamedTemporaryFile(suffix=".yml", delete=False) as temp_file:
                result = FlextMeltanoUtilities.save_yaml_file(
                    Path(temp_file.name), {"test": "data"}
                )

            assert result.is_failure
            assert result.error is not None and "YAML error" in result.error


class TestFlextMeltanoUtilitiesIntegration:
    """Integration tests for FlextMeltanoUtilities."""

    def test_complete_project_setup_workflow(self) -> None:
        """Test complete project setup workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # 1. Create configuration dictionary
            config_result = FlextMeltanoUtilities.create_meltano_config_dict(
                project_id="test_project", project_name="Test Project"
            )
            assert config_result.is_success

            # 2. Create project file
            file_result = FlextMeltanoUtilities.create_meltano_project_file(
                project_path=project_path, config_data=config_result.data
            )
            assert file_result.is_success

            # 3. Validate project structure
            validation_result = (
                FlextMeltanoUtilities.validate_meltano_project_structure(project_path)
            )
            assert validation_result.is_success

            # 4. Get project root
            root_result = FlextMeltanoUtilities.get_project_root(project_path)
            assert root_result.is_success
            assert root_result.data["project_root"] == str(project_path)

    def test_yaml_file_roundtrip(self) -> None:
        """Test YAML file save and load roundtrip."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = Path(temp_dir) / "test.yml"

            original_data = {
                "version": 1,
                "project_id": "test_project",
                "project_name": "Test Project",
                "plugins": ["tap-postgres", "target-postgres"],
                "environments": ["development", "production"],
            }

            # Save YAML file
            save_result = FlextMeltanoUtilities.save_yaml_file(yaml_file, original_data)
            assert save_result.is_success

            # Load YAML file
            load_result = FlextMeltanoUtilities.load_yaml_file(yaml_file)
            assert load_result.is_success

            # Verify data integrity
            assert load_result.data == original_data

    def test_utilities_with_flext_core_integration(self) -> None:
        """Test utilities integration with flext-core components."""
        utilities = FlextMeltanoUtilities()

        # Test that utilities properly use flext-core components
        assert isinstance(utilities, FlextUtilities)

        # Test configuration creation uses flext-core patterns
        result = utilities.create_meltano_config_dict("test_project")
        assert result.is_success
        assert isinstance(result, FlextResult)

        # Test that utilities follow flext-core error handling patterns
        error_result = utilities.create_meltano_config_dict("")
        assert error_result.is_failure
        assert isinstance(error_result, FlextResult)
