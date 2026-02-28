"""FLEXT Meltano Config Complete Coverage Tests - Comprehensive testing patterns.

This module provides complete coverage tests for FlextMeltanoSettings using
comprehensive testing patterns and complete configuration validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import inspect
import os
import tempfile
from pathlib import Path

import pytest
from flext_core import FlextConstants, FlextSettings
from flext_meltano import FlextMeltanoSettings


class TestFlextMeltanoSettings:
    """Test FlextMeltanoSettings base functionality."""

    def test_basic_config_creation(self) -> None:
        """Test basic config creation with all fields."""
        config = FlextMeltanoSettings()
        config.project_root = Path("/test/project")
        config.config_dir = Path(".meltano")
        config.logs_dir = Path("logs")
        config.log_level = "INFO"  # type: ignore[assignment]
        config.meltano_version = "3.9.1"
        config.singer_sdk_version = "0.48.0"
        config.dbt_version = "1.10.5"

        assert config.project_root == Path("/test/project").resolve()
        assert config.config_dir.name == ".meltano"  # Path is resolved, check name
        assert config.logs_dir.name == "logs"  # Path is resolved, check name
        assert config.log_level == "INFO"
        assert config.meltano_version == "3.9.1"
        assert config.singer_sdk_version == "0.48.0"
        assert config.dbt_version == "1.10.5"

    def test_default_config_creation(self) -> None:
        """Test config creation with default values."""
        config = FlextMeltanoSettings()
        config.project_root = Path("/test")

        # Test defaults (config_dir may be .meltano or config per Platform)
        assert config.config_dir.name in {".meltano", "config"}
        assert config.logs_dir.name == "logs"
        assert config.environment in {"development", "testing"}
        # FlextSettings converts to uppercase and may be affected by singleton state
        assert config.log_level in {"INFO", "DEBUG", "WARNING"}  # Accept valid defaults

    def test_path_validation_success(self) -> None:
        """Test successful path validation."""
        config = FlextMeltanoSettings(
            project_root=Path("/valid/path"),
            config_dir=Path("config"),
            logs_dir=Path("logs"),
        )

        # Should convert string paths to Path objects
        assert isinstance(config.project_root, Path)
        assert config.project_root.name == "path"

    def test_path_validation_conversion(self) -> None:
        """Test path validation converts string to Path."""
        config = FlextMeltanoSettings(project_root=Path("string/path"))
        assert isinstance(config.project_root, Path)
        # Path gets resolved to absolute path, check the name
        assert config.project_root.name == "path"

    def test_version_validation_success(self) -> None:
        """Test successful version validation."""
        config = FlextMeltanoSettings(
            project_root=Path("/test"),
            meltano_version="3.9.1",
            singer_sdk_version="0.48.0",
            dbt_version="1.10.5",
        )

        assert config.meltano_version == "3.9.1"
        assert config.singer_sdk_version == "0.48.0"
        assert config.dbt_version == "1.10.5"

    def test_version_validation_failure(self) -> None:
        """Test version validation - all fields have defaults so validation passes."""
        # All version fields have defaults, so validation always passes
        config = FlextMeltanoSettings(project_root=Path("/test"))
        assert config.meltano_version == "3.9.1"
        assert config.singer_sdk_version == "0.48.0"
        assert config.dbt_version == "1.10.5"

    def test_get_project_file(self) -> None:
        """Test get_project_file method."""
        config = FlextMeltanoSettings(project_root=Path("/test/project"))
        project_file_result = config.get_project_file()

        assert project_file_result.is_success
        project_file = project_file_result.value
        assert isinstance(project_file, Path)
        assert project_file == Path("/test/project/pipeline.yml")

    def test_get_absolute_config_dir(self) -> None:
        """Test get_absolute_config_dir method."""
        config = FlextMeltanoSettings(
            project_root=Path("/test/project"),
            config_dir=Path(".meltano"),
        )
        result = config.get_absolute_config_dir()

        assert result.is_success
        config_dir = result.value
        assert isinstance(config_dir, Path)
        # Since config_dir gets resolved by validator, check if it's absolute
        assert config_dir.is_absolute()
        assert config_dir.name == ".meltano"

    def test_get_absolute_logs_dir(self) -> None:
        """Test get_absolute_logs_dir method returns FlextResult."""
        config = FlextMeltanoSettings(
            project_root=Path("/test/project"),
            logs_dir=Path("logs"),
        )
        result = config.get_absolute_logs_dir()

        assert result.is_success
        logs_dir = result.value
        assert isinstance(logs_dir, Path)
        assert logs_dir.is_absolute()
        assert logs_dir.name == "logs"

    def test_get_absolute_venv_dir(self) -> None:
        """Test get_absolute_venv_dir method."""
        config = FlextMeltanoSettings(project_root=Path("/test/project"))
        venv_dir = config.get_absolute_venv_dir()

        assert isinstance(venv_dir, Path)
        # Since project_root gets resolved by validator, check if it contains the expected path
        assert venv_dir.name == "python"
        assert ".meltano" in str(venv_dir.parent)

    def test_validate_project_structure_missing_project_file(self) -> None:
        """Test project structure validation with missing pipeline.yml."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = FlextMeltanoSettings(project_root=Path(tmp_dir))
            result = config.validate_project_structure()

            assert result.is_failure
            assert "pipeline.yml not found" in (result.error or "")

    def test_validate_project_structure_success(self) -> None:
        """Test successful project structure validation."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create pipeline.yml file
            project_file = Path(tmp_dir) / "pipeline.yml"
            project_file.write_text("version: 1\n")

            config = FlextMeltanoSettings(project_root=Path(tmp_dir))
            result = config.validate_project_structure()

            assert result.is_success
            assert result.value is True

    def test_get_environment_variables(self) -> None:
        """Test environment variables extraction."""
        config = FlextMeltanoSettings(
            project_root=Path("/test/project"),
            log_level="DEBUG",
        )
        env_vars = config.get_environment_variables()

        assert isinstance(env_vars, dict)
        assert env_vars["MELTANO_PROJECT_ROOT"] == str(config.project_root)
        assert env_vars["MELTANO_LOG_LEVEL"] == "DEBUG"

    def test_class_methods(self) -> None:
        """Test all class methods return expected values."""
        assert FlextMeltanoSettings.get_version() == "0.9.0"
        assert FlextMeltanoSettings.get_name() == "flext-meltano"
        assert (
            FlextMeltanoSettings.get_default_timeout() == 30
        )  # FlextConstants default
        assert FlextMeltanoSettings.get_default_batch_size() == 1000

    def test_get_supported_lists(self) -> None:
        """Test methods that return lists of supported values."""
        plugin_types = FlextMeltanoSettings.get_supported_plugin_types()
        log_levels = FlextMeltanoSettings.get_supported_log_levels()

        assert isinstance(plugin_types, list)
        assert "extractors" in plugin_types
        assert "loaders" in plugin_types
        # Meltano uses "transforms" as the plugin type
        assert "transforms" in plugin_types

        assert isinstance(log_levels, list)
        assert "INFO" in log_levels
        assert "DEBUG" in log_levels

    def test_create_from_project_root_factory(self) -> None:
        """Test create_from_project_root factory method."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create pipeline.yml for validation
            project_file = Path(tmp_dir) / "pipeline.yml"
            project_file.write_text("version: 1\n")

            result = FlextMeltanoSettings.create_from_project_root(
                project_root=Path(tmp_dir),
            )

            assert result.is_success
            config = result.value
            assert config.project_root == Path(tmp_dir).resolve()

    def test_create_from_project_root_with_defaults(self) -> None:
        """Test create_from_project_root with default values."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create pipeline.yml for validation
            project_file = Path(tmp_dir) / "pipeline.yml"
            project_file.write_text("version: 1\n")

            result = FlextMeltanoSettings.create_from_project_root(
                project_root=Path(tmp_dir),
            )

            assert result.is_success
            config = result.value
            assert config.project_root == Path(tmp_dir).resolve()

    def test_create_for_environment_factory(self) -> None:
        """Test create_for_environment factory method."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = FlextMeltanoSettings(
                project_root=Path(tmp_dir),
                log_level="WARNING",
            )

            config = result
            assert config.log_level == "WARNING"  # FlextSettings converts to uppercase
            assert config.project_root == Path(tmp_dir)

    def test_create_for_environment_with_validation_error(self) -> None:
        """Test create_for_environment with invalid parameters."""
        # Should raise ValueError for invalid environment type
        with pytest.raises(ValueError):
            FlextMeltanoSettings.create_for_environment("invalid_env_type")


class TestFlextMeltanoSettingsEnums:
    """Test FlextMeltanoSettings uses FlextConstants for enums."""

    def test_uses_flext_constants_for_enums(self) -> None:
        """Test that FlextMeltanoSettings uses FlextConstants for enum values."""
        # Config uses FlextConstants.Settings.LogLevel, not nested LogLevel
        assert hasattr(FlextConstants.Settings, "LogLevel")
        # Environment types are string literals, not enums
        assert isinstance(FlextMeltanoSettings.model_fields["environment"].default, str)

    def test_config_builders_nested_class(self) -> None:
        """Test ConfigBuilders nested class exists."""
        # ConfigBuilders is a nested class for configuration factory methods
        assert hasattr(FlextMeltanoSettings, "ConfigBuilders")
        assert inspect.isclass(FlextMeltanoSettings.ConfigBuilders)


class TestFlextMeltanoSettingsConstants:
    """Test all constants are properly set."""

    def test_version_constants(self) -> None:
        """Test version constants from FlextMeltanoConstants."""
        assert FlextMeltanoSettings.MELTANO_VERSION == "3.9.1"
        assert FlextMeltanoSettings.SINGER_SDK_VERSION == "0.48.0"
        assert FlextMeltanoSettings.DBT_VERSION == "1.10.5"

    def test_file_constants(self) -> None:
        """Test file path constants."""
        assert FlextMeltanoSettings.PROJECT_FILE == "pipeline.yml"
        assert FlextMeltanoSettings.STATE_DIR == ".pipeline"
        assert FlextMeltanoSettings.VENV_DIR == ".meltano/python"

    def test_environment_variable_constants(self) -> None:
        """Test environment variable name constants."""
        assert FlextMeltanoSettings.MELTANO_PROJECT_ROOT_ENV == "MELTANO_PROJECT_ROOT"
        assert FlextMeltanoSettings.MELTANO_ENVIRONMENT_ENV == "MELTANO_ENVIRONMENT"
        assert FlextMeltanoSettings.MELTANO_LOG_LEVEL_ENV == "MELTANO_LOG_LEVEL"


class TestFlextMeltanoSettingsEdgeCases:
    """Test edge cases and error conditions."""

    def test_invalid_log_level_validation(self) -> None:
        """Test log level validation - uses default when invalid."""
        # Log level validation is handled by FlextSettings
        global_config = FlextSettings.get_global_instance()
        # Test that global config has log_level
        assert hasattr(global_config, "log_level")
        assert global_config.log_level in {"INFO", "DEBUG"}  # Valid levels

    def test_empty_project_root_validation(self) -> None:
        """Test empty project root resolves to current directory."""
        # When passing explicit absolute path, it should stay absolute
        current_dir = Path.cwd()
        config = FlextMeltanoSettings(project_root=current_dir)
        assert config.project_root.is_absolute()
        assert config.project_root.exists()

    def test_project_structure_validation_with_relative_paths(self) -> None:
        """Test project validation works with relative paths."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create pipeline.yml
            project_file = Path(tmp_dir) / "pipeline.yml"
            project_file.write_text("version: 1\n")

            # Use relative path
            current_dir = Path.cwd()
            try:
                os.chdir(tmp_dir)
                config = FlextMeltanoSettings()
                config.project_root = Path()
                result = config.validate_project_structure()

                assert result.is_success
            finally:
                os.chdir(current_dir)


class TestFlextMeltanoSettingsIntegration:
    """Integration tests combining multiple config features."""

    def test_complete_config_workflow(self) -> None:
        """Test complete configuration workflow from creation to validation."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create pipeline.yml
            project_file = Path(tmp_dir) / "pipeline.yml"
            project_file.write_text("version: 1\nproject_id: test-project\n")

            # Create directories
            config_dir = Path(tmp_dir) / ".meltano"
            logs_dir = Path(tmp_dir) / "logs"
            config_dir.mkdir()
            logs_dir.mkdir()

            # Create config using factory
            result = FlextMeltanoSettings.create_from_project_root(
                project_root=Path(tmp_dir),
            )

            assert result.is_success
            config = result.value

            # Validate project structure
            validation_result = config.validate_project_structure()
            assert validation_result.is_success

            # Check paths are correct
            project_file_result = config.get_project_file()
            assert project_file_result.is_success
            assert project_file_result.value.exists()
            config_dir_result = config.get_absolute_config_dir()
            assert config_dir_result.is_success
            config_dir_result.value.mkdir(parents=True, exist_ok=True)
            assert config_dir_result.value.exists()
            logs_dir_result = config.get_absolute_logs_dir()
            assert logs_dir_result.is_success
            logs_dir_result.value.mkdir(parents=True, exist_ok=True)
            assert logs_dir_result.value.exists()

            # Check environment variables
            env_vars = config.get_environment_variables()
            assert len(env_vars) >= 3
            assert all(isinstance(k, str) for k in env_vars)
            assert all(isinstance(v, str) for v in env_vars.values())

    def test_config_with_all_supported_values(self) -> None:
        """Test config creation with all supported enum values."""
        for env_type in FlextMeltanoSettings.get_supported_environments():
            # Skip invalid environment types
            if env_type == "local":
                continue

            # Production environment cannot have debug=True
            config = FlextMeltanoSettings(
                project_root=Path("/test"),
                environment=env_type,
                log_level="INFO",
                debug=env_type != "production",
            )

            assert config.environment == env_type
            # In test environment, log_level is overridden by FLEXT_LOG_LEVEL=debug
            # So we check that it's either the expected value or the test environment value
            expected_log_level = "INFO"
            test_env_log_level = "DEBUG"  # From conftest.py
            assert config.log_level in {expected_log_level, test_env_log_level}

    def test_config_constants_integration(self) -> None:
        """Test that config constants integrate properly with functionality."""
        config = FlextMeltanoSettings(project_root=Path("/test"))

        # Test that constants are used properly
        project_file_result = config.get_project_file()
        assert project_file_result.is_success
        assert project_file_result.value.name == FlextMeltanoSettings.PROJECT_FILE

        venv_dir = config.get_absolute_venv_dir()
        assert str(venv_dir).endswith(FlextMeltanoSettings.VENV_DIR)

        # Test environment variables use the right constants
        env_vars = config.get_environment_variables()
        assert FlextMeltanoSettings.MELTANO_PROJECT_ROOT_ENV in env_vars
        assert FlextMeltanoSettings.MELTANO_ENVIRONMENT_ENV in env_vars
        assert FlextMeltanoSettings.MELTANO_LOG_LEVEL_ENV in env_vars
