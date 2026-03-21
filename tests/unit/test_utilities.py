"""Enhanced comprehensive tests for u module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

from flext_tests import t, u

from flext_meltano import t, u


class TestFlextMeltanoUtilitiesEnhanced:
    """Enhanced tests for u class."""

    def test_inheritance_from_flext_utilities(self) -> None:
        """Test that u inherits from u.Meltano."""
        utilities = u()
        u.Tests.Matchers.that(isinstance(utilities, u), eq=True)

    def test_create_meltano_config_dict_success(self) -> None:
        """Test successful Meltano config dictionary creation."""
        result = u.Meltano.create_meltano_config_dict(
            project_id="test-project", version="1.0.0", default_environment="dev"
        )
        u.Tests.Matchers.ok(result)
        config_dict = result.value
        u.Tests.Matchers.that(config_dict["project_id"], eq="test-project")
        u.Tests.Matchers.that(config_dict["version"], eq="1.0.0")
        u.Tests.Matchers.that(config_dict["default_environment"], eq="dev")
        u.Tests.Matchers.that("plugins" in config_dict, eq=True)
        u.Tests.Matchers.that("environments" in config_dict, eq=True)

    def test_create_meltano_config_dict_with_plugins(self) -> None:
        """Test Meltano config dictionary creation with plugins."""
        plugins: t.Meltano.MeltanoConfigDict = {
            "extractors": [{"name": "tap-postgres"}],
            "loaders": [{"name": "target-csv"}],
        }
        result = u.Meltano.create_meltano_config_dict(
            project_id="etl-project", plugins=plugins
        )
        u.Tests.Matchers.ok(result)
        config_dict = result.value
        u.Tests.Matchers.that(isinstance(config_dict, dict), eq=True)
        u.Tests.Matchers.that(config_dict["project_id"], eq="etl-project")
        plugins_val = config_dict["plugins"]
        u.Tests.Matchers.that(isinstance(plugins_val, dict), eq=True)
        if isinstance(plugins_val, dict):
            extractors = plugins_val.get("extractors")
            loaders = plugins_val.get("loaders")
            u.Tests.Matchers.that(isinstance(extractors, list), eq=True)
            u.Tests.Matchers.that(isinstance(loaders, list), eq=True)
            if isinstance(extractors, list) and isinstance(loaders, list):
                u.Tests.Matchers.that(len(extractors) > 0, eq=True)
                u.Tests.Matchers.that(len(loaders) > 0, eq=True)
                first_extractor = extractors[0]
                first_loader = loaders[0]
                u.Tests.Matchers.that(isinstance(first_extractor, dict), eq=True)
                u.Tests.Matchers.that(isinstance(first_loader, dict), eq=True)
                if isinstance(first_extractor, dict) and isinstance(first_loader, dict):
                    u.Tests.Matchers.that(first_extractor["name"], eq="tap-postgres")
                    u.Tests.Matchers.that(first_loader["name"], eq="target-csv")

    def test_create_meltano_config_dict_with_environments(self) -> None:
        """Test Meltano config dictionary creation with environments."""
        environments: t.Meltano.MeltanoConfigDict = {
            "dev": {"plugins": {"extractors": []}},
            "prod": {"plugins": {"extractors": [{"name": "tap-postgres"}]}},
        }
        config_result = u.Meltano.create_meltano_config_dict(
            project_id="multi-env-project", environments=environments
        )
        u.Tests.Matchers.ok(config_result)
        config_dict = config_result.value
        u.Tests.Matchers.that(isinstance(config_dict, dict), eq=True)
        u.Tests.Matchers.that(config_dict["project_id"], eq="multi-env-project")
        env_dict = config_dict["environments"]
        u.Tests.Matchers.that(isinstance(env_dict, dict), eq=True)
        if isinstance(env_dict, dict):
            u.Tests.Matchers.that("dev" in env_dict, eq=True)
            u.Tests.Matchers.that("prod" in env_dict, eq=True)
            prod_env = env_dict["prod"]
            u.Tests.Matchers.that(isinstance(prod_env, dict), eq=True)
            if isinstance(prod_env, dict):
                prod_plugins = prod_env.get("plugins")
                u.Tests.Matchers.that(isinstance(prod_plugins, dict), eq=True)
                if isinstance(prod_plugins, dict):
                    prod_extractors = prod_plugins.get("extractors")
                    u.Tests.Matchers.that(isinstance(prod_extractors, list), eq=True)
                    if isinstance(prod_extractors, list):
                        u.Tests.Matchers.that(len(prod_extractors) > 0, eq=True)
                        first_prod_extractor = prod_extractors[0]
                        u.Tests.Matchers.that(
                            isinstance(first_prod_extractor, dict), eq=True
                        )
                        if isinstance(first_prod_extractor, dict):
                            u.Tests.Matchers.that(
                                first_prod_extractor["name"], eq="tap-postgres"
                            )

    def test_create_meltano_config_dict_numeric_project_id_converts_to_string(
        self,
    ) -> None:
        """Test Meltano config dictionary creation converts numeric project_id to string."""
        result = u.Meltano.create_meltano_config_dict(
            project_id="123", project_name="test-project", version="1.0.0"
        )
        u.Tests.Matchers.ok(result)
        config_dict = result.value
        u.Tests.Matchers.that(isinstance(config_dict, dict), eq=True)
        u.Tests.Matchers.that(config_dict["project_id"], eq="123")

    def test_validate_project_structure_success(self) -> None:
        """Test successful project structure validation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            (project_path / "pipeline.yml").write_text("project_id: test")
            (project_path / ".meltano").mkdir()
            (project_path / ".meltano" / "config").mkdir()
            (project_path / ".meltano" / "logs").mkdir()
            result = u.Meltano.validate_project_structure(project_path)
            u.Tests.Matchers.ok(result)
            u.Tests.Matchers.that(result.value is not None, eq=True)

    def test_validate_project_structure_missing_pipeline_yml(self) -> None:
        """Test project structure validation with missing pipeline.yml."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            (project_path / ".meltano").mkdir()
            result = u.Meltano.validate_project_structure(project_path)
            u.Tests.Matchers.fail(result)
            error = result.error
            u.Tests.Matchers.that(error is not None, eq=True)
            if error is not None:
                u.Tests.Matchers.that("Meltano config file not found" in error, eq=True)

    def test_validate_project_structure_missing_meltano_dir(self) -> None:
        """Test project structure validation with missing .meltano directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            (project_path / "pipeline.yml").write_text("project_id: test")
            result = u.Meltano.validate_project_structure(project_path)
            u.Tests.Matchers.ok(result)
            u.Tests.Matchers.that(result.value is True, eq=True)

    def test_validate_project_structure_nonexistent_path(self) -> None:
        """Test project structure validation with nonexistent path."""
        result = u.Meltano.validate_project_structure(Path("/nonexistent/path"))
        u.Tests.Matchers.fail(result)
        error = result.error
        u.Tests.Matchers.that(error is not None, eq=True)
        if error is not None:
            u.Tests.Matchers.that("Project path does not exist" in error, eq=True)

    def test_create_project_file_success(self) -> None:
        """Test successful project file creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            content: t.Meltano.MeltanoConfigDict = {
                "project_id": "test-project",
                "version": "1.0.0",
            }
            result = u.Meltano.create_project_file(
                project_path / "pipeline.yml", content
            )
            u.Tests.Matchers.ok(result)
            u.Tests.Matchers.that((project_path / "pipeline.yml").exists(), eq=True)
            written_content = (project_path / "pipeline.yml").read_text()
            u.Tests.Matchers.that(
                "project_id: test-project" in written_content, eq=True
            )

    def test_create_project_file_directory_not_exists(self) -> None:
        """Test project file creation in non-existent directory."""
        file_path = Path("/nonexistent/directory/pipeline.yml")
        content: t.Meltano.MeltanoConfigDict = {"project_id": "test"}
        result = u.Meltano.create_project_file(file_path, content)
        u.Tests.Matchers.fail(result)
        error = result.error
        u.Tests.Matchers.that(error is not None, eq=True)
        if error is not None:
            u.Tests.Matchers.that("Failed to create project file" in error, eq=True)

    def test_create_project_file_invalid_content_type(self) -> None:
        """Test project file creation with invalid content type."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            invalid_content = {"invalid": {"nested": ["data"]}}
            result = u.Meltano.create_project_file(
                project_path / "test.yml", invalid_content
            )
            u.Tests.Matchers.fail(result)
            u.Tests.Matchers.that(result.error is not None, eq=True)

    def test_load_yaml_file_success(self) -> None:
        """Test successful YAML file loading."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = Path(temp_dir) / "config.yml"
            with yaml_file.open("w", encoding="utf-8") as f:
                f.write("project_id: test-project\nversion: 1.0.0\n")
            result = u.Meltano.load_yaml_config(yaml_file)
            u.Tests.Matchers.ok(result)
            u.Tests.Matchers.that(result.value["project_id"], eq="test-project")
            u.Tests.Matchers.that(result.value["version"], eq="1.0.0")

    def test_load_yaml_file_invalid_format(self) -> None:
        """Test YAML file loading with invalid format."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = Path(temp_dir) / "invalid.yml"
            with yaml_file.open("w", encoding="utf-8") as f:
                f.write("invalid: yaml: content: [")
            result = u.Meltano.load_yaml_config(yaml_file)
            u.Tests.Matchers.fail(result)
            error = result.error
            u.Tests.Matchers.that(error is not None, eq=True)
            if error is not None:
                u.Tests.Matchers.that("Failed to load YAML" in error, eq=True)

    def test_load_yaml_file_nonexistent(self) -> None:
        """Test YAML file loading with nonexistent file."""
        result = u.Meltano.load_yaml_config(Path("/nonexistent/file.yml"))
        u.Tests.Matchers.fail(result)
        error = result.error
        u.Tests.Matchers.that(error is not None, eq=True)
        if error is not None:
            u.Tests.Matchers.that("File does not exist" in error, eq=True)

    def test_save_yaml_file_success(self) -> None:
        """Test successful YAML file saving."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = Path(temp_dir) / "output.yml"
            content: t.Meltano.MeltanoConfigDict = {
                "project_id": "save-test",
                "version": "2.0.0",
            }
            result = u.Meltano.write_meltano_yml(content, yaml_file)
            u.Tests.Matchers.ok(result)
            u.Tests.Matchers.that(yaml_file.exists(), eq=True)
            saved_content = yaml_file.read_text()
            u.Tests.Matchers.that("project_id: save-test" in saved_content, eq=True)
            u.Tests.Matchers.that("version: 2.0.0" in saved_content, eq=True)

    def test_save_yaml_file_invalid_content(self) -> None:
        """Test YAML file saving with invalid content."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = Path(temp_dir) / "output.yml"
            content_with_set: t.Meltano.MeltanoConfigDict = {"data": {"bad"}}
            result = u.Meltano.write_meltano_yml(content_with_set, yaml_file)
            u.Tests.Matchers.ok(result)
            u.Tests.Matchers.that(yaml_file.exists(), eq=True)
            load_result = u.Meltano.load_yaml_config(yaml_file)
            u.Tests.Matchers.fail(load_result)
            u.Tests.Matchers.that(load_result.error is not None, eq=True)
            u.Tests.Matchers.that(
                "YAML" in str(load_result.error) or "yaml" in str(load_result.error),
                eq=True,
            )

    def test_directory_exists_success(self) -> None:
        """Test successful directory existence check."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = u.Meltano.directory_exists(Path(temp_dir))
            u.Tests.Matchers.ok(result)
            u.Tests.Matchers.that(result.value is True, eq=True)

    def test_directory_exists_failure(self) -> None:
        """Test directory existence check with nonexistent directory."""
        result = u.Meltano.directory_exists(Path("/nonexistent/directory"))
        u.Tests.Matchers.ok(result)
        u.Tests.Matchers.that(result.value is False, eq=True)

    def test_directory_exists_file_instead_of_directory(self) -> None:
        """Test directory existence check with file instead of directory."""
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"test content")
            temp_file_path = Path(temp_file.name)
            result = u.Meltano.directory_exists(temp_file_path)
            u.Tests.Matchers.ok(result)
            u.Tests.Matchers.that(result.value is False, eq=True)
            temp_file_path.unlink()

    def test_utilities_handle_file_operation_errors_gracefully(self) -> None:
        """Test that utilities handle file operation errors gracefully."""
        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.side_effect = OSError("Permission denied")
            result = u.Meltano.directory_exists(Path("/restricted/path"))
            u.Tests.Matchers.fail(result)
            u.Tests.Matchers.that(result.error is not None, eq=True)
            error_msg = result.error or ""
            u.Tests.Matchers.that("Permission denied" in error_msg, eq=True)

    def test_create_meltano_config_dict_with_none_values(self) -> None:
        """Test Meltano config dictionary creation with None values."""
        result = u.Meltano.create_meltano_config_dict(
            project_id="test-project", project_name="Test Project"
        )
        u.Tests.Matchers.ok(result)
        config_dict = result.value
        u.Tests.Matchers.that(config_dict["project_id"], eq="test-project")
        u.Tests.Matchers.that(config_dict["version"], eq=1)
        u.Tests.Matchers.that("default_environment" not in config_dict, eq=True)
        u.Tests.Matchers.that(config_dict["plugins"], eq={})
        u.Tests.Matchers.that("environments" in config_dict, eq=True)

    def test_create_meltano_config_dict_with_empty_strings(self) -> None:
        """Test Meltano config dictionary creation with empty strings."""
        result = u.Meltano.create_meltano_config_dict(
            project_id="test-project", project_name=""
        )
        u.Tests.Matchers.ok(result)
        config_dict = result.value
        u.Tests.Matchers.that(config_dict["project_id"], eq="test-project")
        u.Tests.Matchers.that(config_dict["version"], eq=1)
        u.Tests.Matchers.that(config_dict["default_environment"], eq="dev")

    def test_validate_project_structure_with_subdirectories(self) -> None:
        """Test project structure validation with additional subdirectories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            (project_path / "pipeline.yml").write_text("project_id: test")
            (project_path / ".meltano").mkdir()
            (project_path / ".meltano" / "config").mkdir()
            (project_path / ".meltano" / "logs").mkdir()
            (project_path / ".meltano" / "run").mkdir()
            (project_path / "transform").mkdir()
            (project_path / "extract").mkdir()
            result = u.Meltano.validate_project_structure(project_path)
            u.Tests.Matchers.ok(result)
            u.Tests.Matchers.that(result.value is not None, eq=True)

    def test_create_project_file_with_string_content(self) -> None:
        """Test project file creation with string content."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            content = "project_id: test-project\nversion: 1.0.0"
            result = u.Meltano.create_project_file(project_path / "config.yml", content)
            u.Tests.Matchers.ok(result)
            u.Tests.Matchers.that((project_path / "config.yml").exists(), eq=True)
            written_content = (project_path / "config.yml").read_text()
            u.Tests.Matchers.that(written_content, eq=content)
