"""Enhanced comprehensive tests for FlextMeltanoUtilities module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

from flext_core import u

from flext_meltano.utilities import FlextMeltanoUtilities


class TestFlextMeltanoUtilitiesEnhanced:
    """Enhanced tests for FlextMeltanoUtilities class."""

    def test_inheritance_from_flext_utilities(self) -> None:
        """Test that FlextMeltanoUtilities inherits from u."""
        utilities = FlextMeltanoUtilities()
        assert isinstance(utilities, u)

    def test_create_meltano_config_dict_success(self) -> None:
        """Test successful Meltano config dictionary creation."""
        utilities = FlextMeltanoUtilities()

        result = utilities.create_meltano_config_dict(
            project_id="test-project",
            version="1.0.0",
            default_environment="dev",
        )

        assert result.is_success
        config_dict = result.value

        assert config_dict["project_id"] == "test-project"
        assert config_dict["version"] == "1.0.0"
        assert config_dict["default_environment"] == "dev"
        assert "plugins" in config_dict
        assert "environments" in config_dict

    def test_create_meltano_config_dict_with_plugins(self) -> None:
        """Test Meltano config dictionary creation with plugins."""
        utilities = FlextMeltanoUtilities()

        plugins: dict[str, object] = {
            "extractors": [{"name": "tap-postgres"}],
            "loaders": [{"name": "target-csv"}],
        }

        result = utilities.create_meltano_config_dict(
            project_id="etl-project",
            plugins=plugins,
        )

        assert result.is_success
        config_dict = result.value
        assert isinstance(config_dict, dict)

        assert config_dict["project_id"] == "etl-project"
        plugins_val = config_dict["plugins"]
        assert isinstance(plugins_val, dict)
        extractors = plugins_val.get("extractors")
        loaders = plugins_val.get("loaders")
        assert isinstance(extractors, list)
        assert isinstance(loaders, list)
        assert len(extractors) > 0
        assert len(loaders) > 0
        first_extractor = extractors[0]
        first_loader = loaders[0]
        assert isinstance(first_extractor, dict)
        assert isinstance(first_loader, dict)
        assert first_extractor["name"] == "tap-postgres"
        assert first_loader["name"] == "target-csv"

    def test_create_meltano_config_dict_with_environments(self) -> None:
        """Test Meltano config dictionary creation with environments."""
        utilities = FlextMeltanoUtilities()

        environments: dict[str, object] = {
            "dev": {"plugins": {"extractors": []}},
            "prod": {"plugins": {"extractors": [{"name": "tap-postgres"}]}},
        }

        config_result = utilities.create_meltano_config_dict(
            project_id="multi-env-project",
            environments=environments,
        )

        assert config_result.is_success
        config_dict = config_result.value
        assert isinstance(config_dict, dict)

        assert config_dict["project_id"] == "multi-env-project"
        env_dict = config_dict["environments"]
        assert isinstance(env_dict, dict)
        assert "dev" in env_dict
        assert "prod" in env_dict
        prod_env = env_dict["prod"]
        assert isinstance(prod_env, dict)
        prod_plugins = prod_env.get("plugins")
        assert isinstance(prod_plugins, dict)
        prod_extractors = prod_plugins.get("extractors")
        assert isinstance(prod_extractors, list)
        assert len(prod_extractors) > 0
        first_prod_extractor = prod_extractors[0]
        assert isinstance(first_prod_extractor, dict)
        assert first_prod_extractor["name"] == "tap-postgres"

    def test_create_meltano_config_dict_numeric_project_id_converts_to_string(
        self,
    ) -> None:
        """Test Meltano config dictionary creation converts numeric project_id to string."""
        utilities = FlextMeltanoUtilities()

        # Numeric project_id is converted to string by str() in implementation
        # Type hint says str but we pass int to test coercion behavior
        result = utilities.create_meltano_config_dict(
            project_id=123,  # type: ignore[arg-type] - testing coercion
            project_name="test-project",
            version="1.0.0",
        )

        # Implementation uses str() to convert, so this succeeds
        assert result.is_success
        config_dict = result.value
        assert isinstance(config_dict, dict)
        # Numeric 123 becomes string "123"
        assert config_dict["project_id"] == "123"

    def test_validate_project_structure_success(self) -> None:
        """Test successful project structure validation."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create required project structure
            (project_path / "pipeline.yml").write_text("project_id: test")
            (project_path / ".meltano").mkdir()
            (project_path / ".meltano" / "config").mkdir()
            (project_path / ".meltano" / "logs").mkdir()

            result = utilities.validate_project_structure(project_path)

            assert result.is_success
            assert result.value is not None

    def test_validate_project_structure_missing_pipeline_yml(self) -> None:
        """Test project structure validation with missing pipeline.yml."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create .meltano directory but not meltano.yml
            (project_path / ".meltano").mkdir()

            result = utilities.validate_project_structure(project_path)

            assert result.is_failure
            assert result.error is not None
            assert "Meltano config file not found" in result.error

    def test_validate_project_structure_missing_meltano_dir(self) -> None:
        """Test project structure validation with missing .meltano directory."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create pipeline.yml but not .meltano directory
            (project_path / "pipeline.yml").write_text("project_id: test")

            result = utilities.validate_project_structure(project_path)

            # Current implementation only checks for pipeline.yml existence
            assert result.is_success
            assert result.value is True

    def test_validate_project_structure_nonexistent_path(self) -> None:
        """Test project structure validation with nonexistent path."""
        utilities = FlextMeltanoUtilities()

        result = utilities.validate_project_structure(Path("/nonexistent/path"))

        assert result.is_failure
        assert result.error is not None
        assert "Project path does not exist" in result.error

    def test_create_project_file_success(self) -> None:
        """Test successful project file creation."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            content: dict[str, object] = {
                "project_id": "test-project",
                "version": "1.0.0",
            }

            result = utilities.create_project_file(
                project_path / "pipeline.yml",
                content,
            )

            assert result.is_success
            assert (project_path / "pipeline.yml").exists()

            # Verify content was written correctly
            written_content = (project_path / "pipeline.yml").read_text()
            assert "project_id: test-project" in written_content

    def test_create_project_file_directory_not_exists(self) -> None:
        """Test project file creation in non-existent directory."""
        utilities = FlextMeltanoUtilities()

        # Try to create file in non-existent directory
        file_path = Path("/nonexistent/directory/pipeline.yml")
        content: dict[str, object] = {"project_id": "test"}

        result = utilities.create_project_file(
            file_path,
            content,
        )

        assert result.is_failure
        assert result.error is not None
        assert "Failed to create project file" in result.error

    def test_create_project_file_invalid_content_type(self) -> None:
        """Test project file creation with invalid content type."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Pass invalid content (not dict[str, object] or string)
            # Using integer directly - runtime will handle the type mismatch
            invalid_content: object = 123
            result = utilities.create_project_file(
                project_path / "test.yml",
                invalid_content,  # type: ignore[arg-type]
            )

            assert result.is_failure
            assert result.error is not None
            assert "Invalid content type" in result.error

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
            assert result.value["project_id"] == "test-project"
            assert result.value["version"] == "1.0.0"

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
            assert result.error is not None
            assert "Failed to load YAML" in result.error

    def test_load_yaml_file_nonexistent(self) -> None:
        """Test YAML file loading with nonexistent file."""
        utilities = FlextMeltanoUtilities()

        result = utilities.load_yaml_file(Path("/nonexistent/file.yml"))

        assert result.is_failure
        assert result.error is not None
        assert "File does not exist" in result.error

    def test_save_yaml_file_success(self) -> None:
        """Test successful YAML file saving."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = Path(temp_dir) / "output.yml"
            content: dict[str, object] = {
                "project_id": "save-test",
                "version": "2.0.0",
            }

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

            # Try to save content with object (YAML can serialize but not deserialize)
            content_with_object = {"data": object()}

            result = utilities.save_yaml_file(yaml_file, content_with_object)

            # Save should succeed
            assert result.is_success
            assert yaml_file.exists()

            # But loading should fail
            load_result = utilities.load_yaml_file(yaml_file)
            assert load_result.is_failure
            assert load_result.error is not None
            assert "YAML" in str(load_result.error) or "yaml" in str(load_result.error)

    def test_directory_exists_success(self) -> None:
        """Test successful directory existence check."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            result = utilities.directory_exists(Path(temp_dir))

            assert result.is_success
            assert result.value is True

    def test_directory_exists_failure(self) -> None:
        """Test directory existence check with nonexistent directory."""
        utilities = FlextMeltanoUtilities()

        result = utilities.directory_exists(Path("/nonexistent/directory"))

        assert result.is_success
        assert result.value is False

    def test_directory_exists_file_instead_of_directory(self) -> None:
        """Test directory existence check with file instead of directory."""
        utilities = FlextMeltanoUtilities()

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"test content")
            temp_file_path = Path(temp_file.name)

            result = utilities.directory_exists(temp_file_path)

            assert result.is_success
            assert result.value is False

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
            assert result.error is not None
            assert "Permission denied" in result.error

    def test_create_meltano_config_dict_with_none_values(self) -> None:
        """Test Meltano config dictionary creation with None values."""
        utilities = FlextMeltanoUtilities()

        result = utilities.create_meltano_config_dict(
            project_id="test-project",
            project_name="Test Project",
        )

        assert result.is_success
        config_dict = result.value

        assert config_dict["project_id"] == "test-project"
        assert config_dict["version"] == 1  # Default value
        assert "default_environment" not in config_dict  # Not set when None
        assert config_dict["plugins"] == {}  # Default empty dict
        assert "environments" in config_dict  # Environments are set by default

    def test_create_meltano_config_dict_with_empty_strings(self) -> None:
        """Test Meltano config dictionary creation with empty strings."""
        utilities = FlextMeltanoUtilities()

        result = utilities.create_meltano_config_dict(
            project_id="test-project",
            project_name="",
        )

        assert result.is_success
        config_dict = result.value

        assert config_dict["project_id"] == "test-project"
        assert config_dict["version"] == 1  # Default value
        assert config_dict["default_environment"] == "dev"  # Default value

    def test_validate_project_structure_with_subdirectories(self) -> None:
        """Test project structure validation with additional subdirectories."""
        utilities = FlextMeltanoUtilities()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Create full project structure
            (project_path / "pipeline.yml").write_text("project_id: test")
            (project_path / ".meltano").mkdir()
            (project_path / ".meltano" / "config").mkdir()
            (project_path / ".meltano" / "logs").mkdir()
            (project_path / ".meltano" / "run").mkdir()
            (project_path / "transform").mkdir()
            (project_path / "extract").mkdir()

            result = utilities.validate_project_structure(project_path)

            assert result.is_success
            assert result.value is not None

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
