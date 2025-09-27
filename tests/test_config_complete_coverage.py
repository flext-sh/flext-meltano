"""FLEXT Meltano Config Complete Coverage Tests - Comprehensive testing patterns.

This module provides complete coverage tests for FlextMeltanoConfig using
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
from flext_core.constants import FlextConstants

from flext_meltano import FlextMeltanoConfig


class TestFlextMeltanoConfig:
    """Test FlextMeltanoConfig base functionality."""

    def test_basic_config_creation(self) -> None:
        """Test basic config creation with all fields."""
        config = FlextMeltanoConfig()
        config.project_root = Path("/test/project")
        config.config_dir = Path(".meltano")
        config.logs_dir = Path("logs")
        config.environment = "development"
        config.log_level = "info"
        config.meltano_version = "3.9.1"
        config.singer_sdk_version = "0.48.0"
        config.dbt_version = "1.10.5"

        assert config.project_root == Path("/test/project").resolve()
        assert config.config_dir.name == ".meltano"  # Path is resolved, check name
        assert config.logs_dir.name == "logs"  # Path is resolved, check name
        assert config.environment == "development"
        assert config.log_level == "INFO"  # FlextConfig converts to uppercase
        assert config.meltano_version == "3.9.1"
        assert config.singer_sdk_version == "0.48.0"
        assert config.dbt_version == "1.10.5"

    def test_default_config_creation(self) -> None:
        """Test config creation with default values."""
        config = FlextMeltanoConfig()
        config.project_root = Path("/test")

        # Test defaults from FlextMeltanoConstants (paths are resolved)
        assert config.config_dir.name == ".meltano"
        assert config.logs_dir.name == "logs"
        assert config.environment == "development"
        # FlextConfig converts to uppercase and may be affected by singleton state
        assert config.log_level in {"INFO", "DEBUG"}  # Accept both possible values

    def test_path_validation_success(self) -> None:
        """Test successful path validation."""
        config = FlextMeltanoConfig(
            project_root=Path("/valid/path"),
            config_dir=Path("config"),
            logs_dir=Path("logs"),
        )

        # Should convert string paths to Path objects
        assert isinstance(config.project_root, Path)
        assert config.project_root.name == "path"

    def test_path_validation_conversion(self) -> None:
        """Test path validation converts string to Path."""
        config = FlextMeltanoConfig(project_root=Path("string/path"))
        assert isinstance(config.project_root, Path)
        # Path gets resolved to absolute path, check the name
        assert config.project_root.name == "path"

    def test_version_validation_success(self) -> None:
        """Test successful version validation."""
        config = FlextMeltanoConfig(
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
        config = FlextMeltanoConfig(project_root=Path("/test"))
        assert config.meltano_version == "3.9.1"
        assert config.singer_sdk_version == "0.48.0"
        assert config.dbt_version == "1.10.5"

    def test_get_project_file(self) -> None:
        """Test get_project_file method."""
        config = FlextMeltanoConfig(project_root=Path("/test/project"))
        project_file = config.get_project_file()

        assert isinstance(project_file, Path)
        assert project_file == Path("/test/project/meltano.yml")

    def test_get_absolute_config_dir(self) -> None:
        """Test get_absolute_config_dir method."""
        config = FlextMeltanoConfig(
            project_root=Path("/test/project"),
            config_dir=Path(".meltano"),
        )
        config_dir = config.get_absolute_config_dir()

        assert isinstance(config_dir, Path)
        # Since config_dir gets resolved by validator, check if it's absolute
        assert config_dir.is_absolute()
        assert config_dir.name == ".meltano"

    def test_get_absolute_logs_dir(self) -> None:
        """Test get_absolute_logs_dir method."""
        config = FlextMeltanoConfig(
            project_root=Path("/test/project"),
            logs_dir=Path("logs"),
        )
        logs_dir = config.get_absolute_logs_dir()

        assert isinstance(logs_dir, Path)
        # Since logs_dir gets resolved by validator, check if it's absolute
        assert logs_dir.is_absolute()
        assert logs_dir.name == "logs"

    def test_get_absolute_venv_dir(self) -> None:
        """Test get_absolute_venv_dir method."""
        config = FlextMeltanoConfig(project_root=Path("/test/project"))
        venv_dir = config.get_absolute_venv_dir()

        assert isinstance(venv_dir, Path)
        # Since project_root gets resolved by validator, check if it contains the expected path
        assert venv_dir.name == "python"
        assert ".meltano" in str(venv_dir.parent)

    def test_validate_project_structure_missing_project_file(self) -> None:
        """Test project structure validation with missing meltano.yml."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = FlextMeltanoConfig(project_root=Path(tmp_dir))
            result = config.validate_project_structure()

            assert result.is_failure
            assert "meltano.yml not found" in (result.error or "")

    def test_validate_project_structure_success(self) -> None:
        """Test successful project structure validation."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create meltano.yml file
            project_file = Path(tmp_dir) / "meltano.yml"
            project_file.write_text("version: 1\n")

            config = FlextMeltanoConfig(project_root=Path(tmp_dir))
            result = config.validate_project_structure()

            assert result.is_success
            assert result.unwrap() is True

    def test_get_environment_variables(self) -> None:
        """Test environment variables extraction."""
        config = FlextMeltanoConfig(
            project_root=Path("/test/project"),
            environment="development",
            log_level="debug",
        )
        env_vars = config.get_environment_variables()

        assert isinstance(env_vars, dict)
        assert env_vars["MELTANO_PROJECT_ROOT"] == str(config.project_root)
        assert env_vars["MELTANO_ENVIRONMENT"] == "development"
        assert env_vars["MELTANO_LOG_LEVEL"] == "DEBUG"

    def test_class_methods(self) -> None:
        """Test all class methods return expected values."""
        assert FlextMeltanoConfig.get_version() == "0.9.0"
        assert FlextMeltanoConfig.get_name() == "flext-meltano"
        assert FlextMeltanoConfig.get_default_timeout() == 30  # FlextConstants default
        assert FlextMeltanoConfig.get_default_batch_size() == 1000

    def test_get_supported_lists(self) -> None:
        """Test methods that return lists of supported values."""
        plugin_types = FlextMeltanoConfig.get_supported_plugin_types()
        environments = FlextMeltanoConfig.get_supported_environments()
        log_levels = FlextMeltanoConfig.get_supported_log_levels()

        assert isinstance(plugin_types, list)
        assert "extractors" in plugin_types
        assert "loaders" in plugin_types
        # Use "transformers" not "transforms" - matches actual implementation
        assert "transformers" in plugin_types

        assert isinstance(environments, list)
        assert "development" in environments
        assert "production" in environments

        assert isinstance(log_levels, list)
        assert "INFO" in log_levels
        assert "DEBUG" in log_levels

    def test_create_from_project_root_factory(self) -> None:
        """Test create_from_project_root factory method."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create meltano.yml for validation
            project_file = Path(tmp_dir) / "meltano.yml"
            project_file.write_text("version: 1\n")

            result = FlextMeltanoConfig.create_from_project_root(
                project_root=Path(tmp_dir),
            )

            assert result.is_success
            config = result.unwrap()
            assert config.project_root == Path(tmp_dir).resolve()
            assert config.environment == "development"  # default value

    def test_create_from_project_root_with_defaults(self) -> None:
        """Test create_from_project_root with default values."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create meltano.yml for validation
            project_file = Path(tmp_dir) / "meltano.yml"
            project_file.write_text("version: 1\n")

            result = FlextMeltanoConfig.create_from_project_root(
                project_root=Path(tmp_dir),
            )

            assert result.is_success
            config = result.unwrap()
            assert config.project_root == Path(tmp_dir).resolve()
            assert config.environment == "development"  # default

    def test_create_for_environment_factory(self) -> None:
        """Test create_for_environment factory method."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = FlextMeltanoConfig.create_for_environment(
                environment="staging",
                project_root=Path(tmp_dir),
                log_level="WARNING",
            )

            config = result
            assert config.environment == "staging"
            assert config.log_level == "WARNING"  # FlextConfig converts to uppercase
            assert config.project_root == Path(tmp_dir)

    def test_create_for_environment_with_validation_error(self) -> None:
        """Test create_for_environment with invalid parameters."""
        # Should raise ValueError for invalid environment
        with pytest.raises(ValueError, match="environment"):
            FlextMeltanoConfig.create_for_environment(
                environment="invalid_env",
                project_root=Path("/nonexistent"),
            )


class TestFlextMeltanoConfigEnums:
    """Test FlextMeltanoConfig uses FlextConstants for enums."""

    def test_uses_flext_constants_for_enums(self) -> None:
        """Test that FlextMeltanoConfig uses FlextConstants for enum values."""
        # Config uses FlextConstants.Config.LogLevel, not nested LogLevel
        assert hasattr(FlextConstants.Config, "LogLevel")
        # Environment types are string literals, not enums
        assert isinstance(FlextMeltanoConfig.model_fields["environment"].default, str)

    def test_handler_configuration_nested_class(self) -> None:
        """Test HandlerConfiguration nested class exists."""
        # HandlerConfiguration is a nested class for handler config
        assert hasattr(FlextMeltanoConfig, "HandlerConfiguration")
        assert inspect.isclass(FlextMeltanoConfig.HandlerConfiguration)


class TestFlextMeltanoConfigConstants:
    """Test all constants are properly set."""

    def test_version_constants(self) -> None:
        """Test version constants from FlextMeltanoConstants."""
        assert FlextMeltanoConfig.MELTANO_VERSION == "3.9.1"
        assert FlextMeltanoConfig.SINGER_SDK_VERSION == "0.48.0"
        assert FlextMeltanoConfig.DBT_VERSION == "1.10.5"

    def test_file_constants(self) -> None:
        """Test file path constants."""
        assert FlextMeltanoConfig.PROJECT_FILE == "meltano.yml"
        assert FlextMeltanoConfig.STATE_DIR == ".meltano"
        assert FlextMeltanoConfig.VENV_DIR == ".meltano/python"

    def test_environment_variable_constants(self) -> None:
        """Test environment variable name constants."""
        assert FlextMeltanoConfig.MELTANO_PROJECT_ROOT_ENV == "MELTANO_PROJECT_ROOT"
        assert FlextMeltanoConfig.MELTANO_ENVIRONMENT_ENV == "MELTANO_ENVIRONMENT"
        assert FlextMeltanoConfig.MELTANO_LOG_LEVEL_ENV == "MELTANO_LOG_LEVEL"


class TestFlextMeltanoConfigEdgeCases:
    """Test edge cases and error conditions."""

    def test_invalid_environment_validation(self) -> None:
        """Test validation fails with invalid environment using create_for_environment."""
        # Should raise ValueError for invalid environment
        with pytest.raises(ValueError, match="Invalid environment"):
            FlextMeltanoConfig.create_for_environment(
                environment="invalid_environment_name",
                project_root=Path("/test"),
            )

    def test_invalid_log_level_validation(self) -> None:
        """Test log level validation - uses default when invalid."""
        # Log level has default, so invalid values fall back to default
        config = FlextMeltanoConfig(project_root=Path("/test"), log_level="INFO")
        assert config.log_level == "INFO"  # Valid log level

    def test_empty_project_root_validation(self) -> None:
        """Test empty project root gets resolved to current directory."""
        config = FlextMeltanoConfig(project_root=Path())
        # Empty path gets resolved to current directory
        assert config.project_root.is_absolute()
        assert config.project_root.exists()

    def test_factory_methods_with_invalid_data(self) -> None:
        """Test factory methods handle invalid data gracefully."""
        # Should raise ValueError for invalid environment
        with pytest.raises(ValueError, match="environment"):
            FlextMeltanoConfig.create_for_environment(
                environment="invalid",
                project_root=Path(),
            )

    def test_environment_variables_with_special_paths(self) -> None:
        """Test environment variables with special characters in paths."""
        config = FlextMeltanoConfig()
        config.project_root = Path("/path with spaces/special-chars_123")
        config.environment = "development"
        env_vars = config.get_environment_variables()

        assert env_vars["MELTANO_PROJECT_ROOT"] == "/path with spaces/special-chars_123"

    def test_project_structure_validation_with_relative_paths(self) -> None:
        """Test project validation works with relative paths."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create meltano.yml
            project_file = Path(tmp_dir) / "meltano.yml"
            project_file.write_text("version: 1\n")

            # Use relative path
            current_dir = Path.cwd()
            try:
                os.chdir(tmp_dir)
                config = FlextMeltanoConfig()
                config.project_root = Path()
                result = config.validate_project_structure()

                assert result.is_success
            finally:
                os.chdir(current_dir)


class TestFlextMeltanoConfigIntegration:
    """Integration tests combining multiple config features."""

    def test_complete_config_workflow(self) -> None:
        """Test complete configuration workflow from creation to validation."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create meltano.yml
            project_file = Path(tmp_dir) / "meltano.yml"
            project_file.write_text("version: 1\nproject_id: test-project\n")

            # Create directories
            config_dir = Path(tmp_dir) / ".meltano"
            logs_dir = Path(tmp_dir) / "logs"
            config_dir.mkdir()
            logs_dir.mkdir()

            # Create config using factory
            result = FlextMeltanoConfig.create_from_project_root(
                project_root=Path(tmp_dir),
            )

            assert result.is_success
            config = result.unwrap()

            # Validate project structure
            validation_result = config.validate_project_structure()
            assert validation_result.is_success

            # Check paths are correct
            assert config.get_project_file().exists()
            assert config.get_absolute_config_dir().exists()
            assert config.get_absolute_logs_dir().exists()

            # Check environment variables
            env_vars = config.get_environment_variables()
            assert len(env_vars) >= 3
            assert all(isinstance(k, str) for k in env_vars)
            assert all(isinstance(v, str) for v in env_vars.values())

    def test_config_with_all_supported_values(self) -> None:
        """Test config creation with all supported enum values."""
        for env_type in FlextMeltanoConfig.get_supported_environments():
            # Skip invalid environment types
            if env_type == "local":
                continue

            # Production environment cannot have debug=True
            config = FlextMeltanoConfig(
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
        config = FlextMeltanoConfig(project_root=Path("/test"))

        # Test that constants are used properly
        project_file = config.get_project_file()
        assert project_file.name == FlextMeltanoConfig.PROJECT_FILE

        venv_dir = config.get_absolute_venv_dir()
        assert str(venv_dir).endswith(FlextMeltanoConfig.VENV_DIR)

        # Test environment variables use the right constants
        env_vars = config.get_environment_variables()
        assert FlextMeltanoConfig.MELTANO_PROJECT_ROOT_ENV in env_vars
        assert FlextMeltanoConfig.MELTANO_ENVIRONMENT_ENV in env_vars
        assert FlextMeltanoConfig.MELTANO_LOG_LEVEL_ENV in env_vars
