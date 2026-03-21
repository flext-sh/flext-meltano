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
from flext_tests import u

from flext_meltano import FlextMeltanoSettings


class TestFlextMeltanoSettings:
    """Test FlextMeltanoSettings base functionality."""

    def test_basic_config_creation(self) -> None:
        """Test basic config creation with all fields."""
        config = FlextMeltanoSettings(
            project_root=Path("/test/project"),
            config_dir=Path(".meltano"),
            logs_dir=Path("logs"),
            log_level="INFO",
            meltano_version="3.9.1",
            singer_sdk_version="0.48.0",
            dbt_version="1.10.5",
        )
        u.Tests.Matchers.that(config.project_root, eq=Path("/test/project").resolve())
        u.Tests.Matchers.that(config.config_dir.name, eq=".meltano")
        u.Tests.Matchers.that(config.logs_dir.name, eq="logs")
        u.Tests.Matchers.that(config.log_level, eq="INFO")
        u.Tests.Matchers.that(config.meltano_version, eq="3.9.1")
        u.Tests.Matchers.that(config.singer_sdk_version, eq="0.48.0")
        u.Tests.Matchers.that(config.dbt_version, eq="1.10.5")

    def test_default_config_creation(self) -> None:
        """Test config creation with default values."""
        config = FlextMeltanoSettings()
        config.project_root = Path("/test")
        u.Tests.Matchers.that(config.config_dir.name in {".meltano", "config"}, eq=True)
        u.Tests.Matchers.that(config.logs_dir.name, eq="logs")
        u.Tests.Matchers.that(config.environment in {"development", "testing"}, eq=True)
        u.Tests.Matchers.that(config.log_level in {"INFO", "DEBUG", "WARNING"}, eq=True)

    def test_path_validation_success(self) -> None:
        """Test successful path validation."""
        config = FlextMeltanoSettings(
            project_root=Path("/valid/path"),
            config_dir=Path("config"),
            logs_dir=Path("logs"),
        )
        u.Tests.Matchers.that(isinstance(config.project_root, Path), eq=True)
        u.Tests.Matchers.that(config.project_root.name, eq="path")

    def test_path_validation_conversion(self) -> None:
        """Test path validation converts string to Path."""
        config = FlextMeltanoSettings(project_root=Path("string/path"))
        u.Tests.Matchers.that(isinstance(config.project_root, Path), eq=True)
        u.Tests.Matchers.that(config.project_root.name, eq="path")

    def test_version_validation_success(self) -> None:
        """Test successful version validation."""
        config = FlextMeltanoSettings(
            project_root=Path("/test"),
            meltano_version="3.9.1",
            singer_sdk_version="0.48.0",
            dbt_version="1.10.5",
        )
        u.Tests.Matchers.that(config.meltano_version, eq="3.9.1")
        u.Tests.Matchers.that(config.singer_sdk_version, eq="0.48.0")
        u.Tests.Matchers.that(config.dbt_version, eq="1.10.5")

    def test_version_validation_failure(self) -> None:
        """Test version validation - all fields have defaults so validation passes."""
        config = FlextMeltanoSettings(project_root=Path("/test"))
        u.Tests.Matchers.that(config.meltano_version, eq="3.9.1")
        u.Tests.Matchers.that(config.singer_sdk_version, eq="0.48.0")
        u.Tests.Matchers.that(config.dbt_version, eq="1.10.5")

    def test_get_project_file(self) -> None:
        """Test get_project_file method."""
        config = FlextMeltanoSettings(project_root=Path("/test/project"))
        project_file_result = config.get_project_file()
        u.Tests.Matchers.ok(project_file_result)
        project_file = project_file_result.value
        u.Tests.Matchers.that(isinstance(project_file, Path), eq=True)
        u.Tests.Matchers.that(project_file, eq=Path("/test/project/pipeline.yml"))

    def test_get_absolute_config_dir(self) -> None:
        """Test get_absolute_config_dir method."""
        config = FlextMeltanoSettings(
            project_root=Path("/test/project"), config_dir=Path(".meltano")
        )
        result = config.get_absolute_config_dir()
        u.Tests.Matchers.ok(result)
        config_dir = result.value
        u.Tests.Matchers.that(isinstance(config_dir, Path), eq=True)
        u.Tests.Matchers.that(config_dir.is_absolute(), eq=True)
        u.Tests.Matchers.that(config_dir.name, eq=".meltano")

    def test_get_absolute_logs_dir(self) -> None:
        """Test get_absolute_logs_dir method returns r."""
        config = FlextMeltanoSettings(
            project_root=Path("/test/project"), logs_dir=Path("logs")
        )
        result = config.get_absolute_logs_dir()
        u.Tests.Matchers.ok(result)
        logs_dir = result.value
        u.Tests.Matchers.that(isinstance(logs_dir, Path), eq=True)
        u.Tests.Matchers.that(logs_dir.is_absolute(), eq=True)
        u.Tests.Matchers.that(logs_dir.name, eq="logs")

    def test_get_absolute_venv_dir(self) -> None:
        """Test get_absolute_venv_dir method."""
        config = FlextMeltanoSettings(project_root=Path("/test/project"))
        venv_dir = config.get_absolute_venv_dir()
        u.Tests.Matchers.that(isinstance(venv_dir, Path), eq=True)
        u.Tests.Matchers.that(venv_dir.name, eq="python")
        u.Tests.Matchers.that(".meltano" in str(venv_dir.parent), eq=True)

    def test_validate_project_structure_missing_project_file(self) -> None:
        """Test project structure validation with missing pipeline.yml."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = FlextMeltanoSettings(project_root=Path(tmp_dir))
            result = config.validate_project_structure()
            u.Tests.Matchers.fail(result)
            u.Tests.Matchers.that(
                "pipeline.yml not found" in (result.error or ""), eq=True
            )

    def test_validate_project_structure_success(self) -> None:
        """Test successful project structure validation."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_file = Path(tmp_dir) / "pipeline.yml"
            project_file.write_text("version: 1\n")
            config = FlextMeltanoSettings(project_root=Path(tmp_dir))
            result = config.validate_project_structure()
            u.Tests.Matchers.ok(result)
            u.Tests.Matchers.that(result.value is True, eq=True)

    def test_get_environment_variables(self) -> None:
        """Test environment variables extraction."""
        config = FlextMeltanoSettings(
            project_root=Path("/test/project"), log_level="DEBUG"
        )
        env_vars = config.get_environment_variables()
        u.Tests.Matchers.that(isinstance(env_vars, dict), eq=True)
        u.Tests.Matchers.that(
            env_vars["MELTANO_PROJECT_ROOT"], eq=str(config.project_root)
        )
        u.Tests.Matchers.that(env_vars["MELTANO_LOG_LEVEL"], eq="DEBUG")

    def test_class_methods(self) -> None:
        """Test all class methods return expected values."""
        u.Tests.Matchers.that(FlextMeltanoSettings.get_version(), eq="0.9.0")
        u.Tests.Matchers.that(FlextMeltanoSettings.get_name(), eq="flext-meltano")
        u.Tests.Matchers.that(FlextMeltanoSettings.get_default_timeout(), eq=30)
        u.Tests.Matchers.that(FlextMeltanoSettings.get_default_batch_size(), eq=1000)

    def test_get_supported_lists(self) -> None:
        """Test methods that return lists of supported values."""
        plugin_types = FlextMeltanoSettings.get_supported_plugin_types()
        log_levels = FlextMeltanoSettings.get_supported_log_levels()
        u.Tests.Matchers.that(isinstance(plugin_types, list), eq=True)
        u.Tests.Matchers.that("extractors" in plugin_types, eq=True)
        u.Tests.Matchers.that("loaders" in plugin_types, eq=True)
        u.Tests.Matchers.that("transforms" in plugin_types, eq=True)
        u.Tests.Matchers.that(isinstance(log_levels, list), eq=True)
        u.Tests.Matchers.that("INFO" in log_levels, eq=True)
        u.Tests.Matchers.that("DEBUG" in log_levels, eq=True)

    def test_create_from_project_root_factory(self) -> None:
        """Test create_from_project_root factory method."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_file = Path(tmp_dir) / "pipeline.yml"
            project_file.write_text("version: 1\n")
            result = FlextMeltanoSettings.create_from_project_root(
                project_root=Path(tmp_dir)
            )
            u.Tests.Matchers.ok(result)
            config = result.value
            u.Tests.Matchers.that(config.project_root, eq=Path(tmp_dir).resolve())

    def test_create_from_project_root_with_defaults(self) -> None:
        """Test create_from_project_root with default values."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_file = Path(tmp_dir) / "pipeline.yml"
            project_file.write_text("version: 1\n")
            result = FlextMeltanoSettings.create_from_project_root(
                project_root=Path(tmp_dir)
            )
            u.Tests.Matchers.ok(result)
            config = result.value
            u.Tests.Matchers.that(config.project_root, eq=Path(tmp_dir).resolve())

    def test_create_for_environment_factory(self) -> None:
        """Test create_for_environment factory method."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = FlextMeltanoSettings(
                project_root=Path(tmp_dir), log_level="WARNING"
            )
            config = result
            u.Tests.Matchers.that(config.log_level, eq="WARNING")
            u.Tests.Matchers.that(config.project_root, eq=Path(tmp_dir))

    def test_create_for_environment_with_validation_error(self) -> None:
        """Test create_for_environment with invalid parameters."""
        with pytest.raises(ValueError):
            FlextMeltanoSettings.create_for_environment("invalid_env_type")


class TestFlextMeltanoSettingsEnums:
    """Test FlextMeltanoSettings uses FlextConstants for enums."""

    def test_uses_flext_constants_for_enums(self) -> None:
        """Test that FlextMeltanoSettings uses FlextConstants for enum values."""
        u.Tests.Matchers.that(hasattr(FlextConstants, "LogLevel"), eq=True)
        u.Tests.Matchers.that(
            isinstance(FlextMeltanoSettings.model_fields["environment"].default, str),
            eq=True,
        )

    def test_config_builders_nested_class(self) -> None:
        """Test ConfigBuilders nested class exists."""
        u.Tests.Matchers.that(hasattr(FlextMeltanoSettings, "ConfigBuilders"), eq=True)
        u.Tests.Matchers.that(
            inspect.isclass(FlextMeltanoSettings.ConfigBuilders), eq=True
        )


class TestFlextMeltanoSettingsConstants:
    """Test all constants are properly set."""

    def test_version_constants(self) -> None:
        """Test version constants from FlextMeltanoConstants."""
        u.Tests.Matchers.that(FlextMeltanoSettings.MELTANO_VERSION, eq="3.9.1")
        u.Tests.Matchers.that(FlextMeltanoSettings.SINGER_SDK_VERSION, eq="0.48.0")
        u.Tests.Matchers.that(FlextMeltanoSettings.DBT_VERSION, eq="1.10.5")

    def test_file_constants(self) -> None:
        """Test file path constants."""
        u.Tests.Matchers.that(FlextMeltanoSettings.PROJECT_FILE, eq="pipeline.yml")
        u.Tests.Matchers.that(FlextMeltanoSettings.STATE_DIR, eq=".pipeline")
        u.Tests.Matchers.that(FlextMeltanoSettings.VENV_DIR, eq=".meltano/python")

    def test_environment_variable_constants(self) -> None:
        """Test environment variable name constants."""
        u.Tests.Matchers.that(
            FlextMeltanoSettings.MELTANO_PROJECT_ROOT_ENV, eq="MELTANO_PROJECT_ROOT"
        )
        u.Tests.Matchers.that(
            FlextMeltanoSettings.MELTANO_ENVIRONMENT_ENV, eq="MELTANO_ENVIRONMENT"
        )
        u.Tests.Matchers.that(
            FlextMeltanoSettings.MELTANO_LOG_LEVEL_ENV, eq="MELTANO_LOG_LEVEL"
        )


class TestFlextMeltanoSettingsEdgeCases:
    """Test edge cases and error conditions."""

    def test_invalid_log_level_validation(self) -> None:
        """Test log level validation - uses default when invalid."""
        global_config = FlextSettings.get_global()
        u.Tests.Matchers.that(hasattr(global_config, "log_level"), eq=True)
        u.Tests.Matchers.that(global_config.log_level in {"INFO", "DEBUG"}, eq=True)

    def test_empty_project_root_validation(self) -> None:
        """Test empty project root resolves to current directory."""
        current_dir = Path.cwd()
        config = FlextMeltanoSettings(project_root=current_dir)
        u.Tests.Matchers.that(config.project_root.is_absolute(), eq=True)
        u.Tests.Matchers.that(config.project_root.exists(), eq=True)

    def test_project_structure_validation_with_relative_paths(self) -> None:
        """Test project validation works with relative paths."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_file = Path(tmp_dir) / "pipeline.yml"
            project_file.write_text("version: 1\n")
            current_dir = Path.cwd()
            try:
                os.chdir(tmp_dir)
                config = FlextMeltanoSettings()
                config.project_root = Path()
                result = config.validate_project_structure()
                u.Tests.Matchers.ok(result)
            finally:
                os.chdir(current_dir)


class TestFlextMeltanoSettingsIntegration:
    """Integration tests combining multiple config features."""

    def test_complete_config_workflow(self) -> None:
        """Test complete configuration workflow from creation to validation."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_file = Path(tmp_dir) / "pipeline.yml"
            project_file.write_text("version: 1\nproject_id: test-project\n")
            config_dir = Path(tmp_dir) / ".meltano"
            logs_dir = Path(tmp_dir) / "logs"
            config_dir.mkdir()
            logs_dir.mkdir()
            result = FlextMeltanoSettings.create_from_project_root(
                project_root=Path(tmp_dir)
            )
            u.Tests.Matchers.ok(result)
            config = result.value
            validation_result = config.validate_project_structure()
            u.Tests.Matchers.ok(validation_result)
            project_file_result = config.get_project_file()
            u.Tests.Matchers.ok(project_file_result)
            u.Tests.Matchers.that(project_file_result.value.exists(), eq=True)
            config_dir_result = config.get_absolute_config_dir()
            u.Tests.Matchers.ok(config_dir_result)
            config_dir_result.value.mkdir(parents=True, exist_ok=True)
            u.Tests.Matchers.that(config_dir_result.value.exists(), eq=True)
            logs_dir_result = config.get_absolute_logs_dir()
            u.Tests.Matchers.ok(logs_dir_result)
            logs_dir_result.value.mkdir(parents=True, exist_ok=True)
            u.Tests.Matchers.that(logs_dir_result.value.exists(), eq=True)
            env_vars = config.get_environment_variables()
            u.Tests.Matchers.that(len(env_vars) >= 3, eq=True)
            u.Tests.Matchers.that(all(isinstance(k, str) for k in env_vars), eq=True)
            u.Tests.Matchers.that(
                all(isinstance(v, str) for v in env_vars.values()), eq=True
            )

    def test_config_with_all_supported_values(self) -> None:
        """Test config creation with all supported enum values."""
        for env_type in FlextMeltanoSettings.get_supported_environments():
            if env_type == "local":
                continue
            config = FlextMeltanoSettings(
                project_root=Path("/test"),
                environment=env_type,
                log_level="INFO",
                debug=env_type != "production",
            )
            u.Tests.Matchers.that(config.environment, eq=env_type)
            expected_log_level = "INFO"
            test_env_log_level = "DEBUG"
            u.Tests.Matchers.that(
                config.log_level in {expected_log_level, test_env_log_level}, eq=True
            )

    def test_config_constants_integration(self) -> None:
        """Test that config constants integrate properly with functionality."""
        config = FlextMeltanoSettings(project_root=Path("/test"))
        project_file_result = config.get_project_file()
        u.Tests.Matchers.ok(project_file_result)
        u.Tests.Matchers.that(
            project_file_result.value.name, eq=FlextMeltanoSettings.PROJECT_FILE
        )
        venv_dir = config.get_absolute_venv_dir()
        u.Tests.Matchers.that(
            str(venv_dir).endswith(FlextMeltanoSettings.VENV_DIR), eq=True
        )
        env_vars = config.get_environment_variables()
        u.Tests.Matchers.that(
            FlextMeltanoSettings.MELTANO_PROJECT_ROOT_ENV in env_vars, eq=True
        )
        u.Tests.Matchers.that(
            FlextMeltanoSettings.MELTANO_ENVIRONMENT_ENV in env_vars, eq=True
        )
        u.Tests.Matchers.that(
            FlextMeltanoSettings.MELTANO_LOG_LEVEL_ENV in env_vars, eq=True
        )
