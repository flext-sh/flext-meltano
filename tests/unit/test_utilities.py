"""Enhanced comprehensive tests for FlextMeltanoUtilities module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

from flext_core import FlextCore

from flext_meltano.utilities import FlextMeltanoUtilities


class TestFlextMeltanoUtilitiesEnhanced:
    """Enhanced tests for FlextMeltanoUtilities class."""

    def test_inheritance_from_flext_utilities(self) -> None:
        """Test that FlextMeltanoUtilities inherits from FlextCore.Utilities."""
        utilities = FlextMeltanoUtilities()
        assert isinstance(utilities, FlextCore.Utilities)

    def test_create_meltano_config_dict_success(self) -> None:
        """Test successful Meltano config dictionary creation."""
        utilities = FlextMeltanoUtilities()

        result = utilities.create_meltano_config_dict(
            project_id="test-project", version="1.0.0", default_environment="dev"
        )

        assert result.is_success
        config_dict = result.unwrap()

        assert config_dict["project_id"] == "test-project"
        assert config_dict["version"] == "1.0.0"
        assert config_dict["default_environment"] == "dev"
        assert "plugins" in config_dict
        assert "environments" in config_dict

    def test_create_meltano_config_dict_with_plugins(self) -> None:
        """Test Meltano config dictionary creation with plugins."""
        utilities = FlextMeltanoUtilities()

        plugins = {
            "extractors": [{"name": "tap-postgres"}],
            "loaders": [{"name": "target-csv"}],
        }

        result = utilities.create_meltano_config_dict(
            project_id="etl-project", plugins=plugins
        )

        assert result.is_success
        config_dict = result.unwrap()

        assert config_dict["project_id"] == "etl-project"
        assert config_dict["plugins"]["extractors"][0]["name"] == "tap-postgres"
        assert config_dict["plugins"]["loaders"][0]["name"] == "target-csv"

    def test_create_meltano_config_dict_with_environments(self) -> None:
        """Test Meltano config dictionary creation with environments."""
        utilities = FlextMeltanoUtilities()

        environments = {
            "dev": {"plugins": {"extractors": []}},
            "prod": {"plugins": {"extractors": [{"name": "tap-postgres"}]}},
        }

        config_result = utilities.create_meltano_config_dict(
            project_id="multi-env-project", environments=environments
        )

        assert config_result.is_success
        config_dict = config_result.unwrap()

        assert config_dict["project_id"] == "multi-env-project"
        assert "dev" in config_dict["environments"]
        assert "prod" in config_dict["environments"]
        assert (
            config_dict["environments"]["prod"]["plugins"]["extractors"][0]["name"]
            == "tap-postgres"
        )

    def test_create_meltano_config_dict_invalid_project_id_type(self) -> None:
        """Test Meltano config dictionary creation with invalid project_id type."""
        utilities = FlextMeltanoUtilities()

        # This should return a failure result due to invalid project_id type
        result = utilities.create_meltano_config_dict(
            project_id=123,  # Invalid type - should be string
            version="1.0.0",
        )

        assert result.is_failure
        assert "Failed to create Meltano config dict" in result.error

    def test_validate_project_structure_success(self) -> None:
        """Test successful project structure validation."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create required project structure
            (project_path / "meltano.yml").write_text("project_id: test")
            (project_path / ".meltano").mkdir()
            (project_path / ".meltano" / "config").mkdir()
            (project_path / ".meltano" / "logs").mkdir()

            result = utilities.validate_project_structure(project_path)

            assert result.is_success
            assert result.data is not None

    def test_validate_project_structure_missing_meltano_yml(self) -> None:
        """Test project structure validation with missing meltano.yml."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create .meltano directory but not meltano.yml
            (project_path / ".meltano").mkdir()

            result = utilities.validate_project_structure(project_path)

            assert result.is_failure
            assert result.error is not None and "meltano.yml not found" in result.error

    def test_validate_project_structure_missing_meltano_dir(self) -> None:
        """Test project structure validation with missing .meltano directory."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create meltano.yml but not .meltano directory
            (project_path / "meltano.yml").write_text("project_id: test")

            result = utilities.validate_project_structure(project_path)

            assert result.is_failure
            assert (
                result.error is not None
                and ".meltano directory not found" in result.error
            )

    def test_validate_project_structure_nonexistent_path(self) -> None:
        """Test project structure validation with nonexistent path."""
        utilities = FlextMeltanoUtilities()

        result = utilities.validate_project_structure(Path("/nonexistent/path"))

        assert result.is_failure
        assert (
            result.error is not None and "Project path does not exist" in result.error
        )

    def test_create_project_file_success(self) -> None:
        """Test successful project file creation."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            content = {"project_id": "test-project", "version": "1.0.0"}

            result = utilities.create_project_file(
                project_path / "meltano.yml", content
            )

            assert result.is_success
            assert (project_path / "meltano.yml").exists()

            # Verify content was written correctly
            written_content = (project_path / "meltano.yml").read_text()
            assert "project_id: test-project" in written_content

    def test_create_project_file_directory_not_exists(self) -> None:
        """Test project file creation in non-existent directory."""
        utilities = FlextMeltanoUtilities()

        # Try to create file in non-existent directory
        file_path = Path("/nonexistent/directory/meltano.yml")
        content = {"project_id": "test"}

        result = utilities.create_project_file(file_path, content)

        assert result.is_failure
        assert (
            result.error is not None and "Failed to create project file" in result.error
        )

    def test_create_project_file_invalid_content_type(self) -> None:
        """Test project file creation with invalid content type."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Pass invalid content (not dict[str, object] or string)
            result = utilities.create_project_file(
                project_path / "test.yml",
                123,  # Invalid content type
            )

            assert result.is_failure
            assert result.error is not None and "Invalid content type" in result.error

    def test_load_yaml_file_success(self) -> None:
        """Test successful YAML file loading."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = Path(temp_dir) / "config.yml"

            # Write valid YAML content
            with yaml_file.open("w", encoding="utf-8") as f:
                f.write("project_id: test-project\nversion: 1.0.0\n")

            result = utilities.load_yaml_file(yaml_file)

            assert result.is_success
            assert result.data["project_id"] == "test-project"
            assert result.data["version"] == "1.0.0"

    def test_load_yaml_file_invalid_format(self) -> None:
        """Test YAML file loading with invalid format."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = Path(temp_dir) / "invalid.yml"

            # Write invalid YAML content
            with yaml_file.open("w", encoding="utf-8") as f:
                f.write("invalid: yaml: content: [")

            result = utilities.load_yaml_file(yaml_file)

            assert result.is_failure
            assert (
                result.error is not None and "Failed to load YAML file" in result.error
            )

    def test_load_yaml_file_nonexistent(self) -> None:
        """Test YAML file loading with nonexistent file."""
        utilities = FlextMeltanoUtilities()

        result = utilities.load_yaml_file(Path("/nonexistent/file.yml"))

        assert result.is_failure
        assert result.error is not None and "File does not exist" in result.error

    def test_save_yaml_file_success(self) -> None:
        """Test successful YAML file saving."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = Path(temp_dir) / "output.yml"
            content = {"project_id": "save-test", "version": "2.0.0"}

            result = utilities.save_yaml_file(yaml_file, content)

            assert result.is_success
            assert yaml_file.exists()

            # Verify content was saved correctly
            saved_content = yaml_file.read_text()
            assert "project_id: save-test" in saved_content
            assert "version: 2.0.0" in saved_content

    def test_save_yaml_file_invalid_content(self) -> None:
        """Test YAML file saving with invalid content."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = Path(temp_dir) / "output.yml"

            # Try to save invalid content (contains non-serializable object)
            invalid_content = {"data": object()}  # object() is not YAML serializable

            result = utilities.save_yaml_file(yaml_file, invalid_content)

            assert result.is_failure
            assert (
                result.error is not None and "Failed to save YAML file" in result.error
            )

    def test_directory_exists_success(self) -> None:
        """Test successful directory existence check."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            result = utilities.directory_exists(Path(temp_dir))

            assert result.is_success
            assert result.data is True

    def test_directory_exists_failure(self) -> None:
        """Test directory existence check with nonexistent directory."""
        utilities = FlextMeltanoUtilities()

        result = utilities.directory_exists(Path("/nonexistent/directory"))

        assert result.is_success
        assert result.data is False

    def test_directory_exists_file_instead_of_directory(self) -> None:
        """Test directory existence check with file instead of directory."""
        utilities = FlextMeltanoUtilities()

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"test content")
            temp_file_path = Path(temp_file.name)

            result = utilities.directory_exists(temp_file_path)

            assert result.is_success
            assert result.data is False

            # Clean up
            temp_file_path.unlink()

    def test_utilities_handle_file_operation_errors_gracefully(self) -> None:
        """Test that utilities handle file operation errors gracefully."""
        utilities = FlextMeltanoUtilities()

        # Test with a path that causes permission errors
        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.side_effect = OSError("Permission denied")

            result = utilities.directory_exists(Path("/restricted/path"))

            assert result.is_failure
            assert result.error is not None and "Permission denied" in result.error

    def test_create_meltano_config_dict_with_none_values(self) -> None:
        """Test Meltano config dictionary creation with None values."""
        utilities = FlextMeltanoUtilities()

        result = utilities.create_meltano_config_dict(
            project_id="test-project", project_name="Test Project"
        )

        assert result.is_success
        config_dict = result.unwrap()

        assert config_dict["project_id"] == "test-project"
        assert config_dict["version"] == 1  # Default value
        assert config_dict["default_environment"] == "dev"  # Default value
        assert config_dict["plugins"] == {}  # Default empty dict
        assert config_dict["environments"] == {}  # Default empty dict

    def test_create_meltano_config_dict_with_empty_strings(self) -> None:
        """Test Meltano config dictionary creation with empty strings."""
        utilities = FlextMeltanoUtilities()

        result = utilities.create_meltano_config_dict(
            project_id="test-project", project_name=""
        )

        assert result.is_success
        config_dict = result.unwrap()

        assert config_dict["project_id"] == "test-project"
        assert config_dict["version"] == 1  # Default value
        assert config_dict["default_environment"] == "dev"  # Default value

    def test_validate_project_structure_with_subdirectories(self) -> None:
        """Test project structure validation with additional subdirectories."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create full project structure
            (project_path / "meltano.yml").write_text("project_id: test")
            (project_path / ".meltano").mkdir()
            (project_path / ".meltano" / "config").mkdir()
            (project_path / ".meltano" / "logs").mkdir()
            (project_path / ".meltano" / "run").mkdir()
            (project_path / "transform").mkdir()
            (project_path / "extract").mkdir()

            result = utilities.validate_project_structure(project_path)

            assert result.is_success
            assert result.data is not None

    def test_create_project_file_with_string_content(self) -> None:
        """Test project file creation with string content."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            content = "project_id: test-project\nversion: 1.0.0"

            result = utilities.create_project_file(project_path / "config.yml", content)

            assert result.is_success
            assert (project_path / "config.yml").exists()

            # Verify content was written correctly
            written_content = (project_path / "config.yml").read_text()
            assert written_content == content
