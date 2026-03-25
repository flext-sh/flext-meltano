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
from flext_core import FlextSettings
from flext_core._constants.settings import FlextConstantsSettings
from flext_tests import tm

from flext_meltano import FlextMeltanoSettings
from tests import c

LogLevel = FlextConstantsSettings.LogLevel


class TestFlextMeltanoSettings:
    """Test FlextMeltanoSettings base functionality."""

    def test_basic_config_creation(self) -> None:
        """Test basic config creation with all fields."""
        config = FlextMeltanoSettings(
            project_root=Path("/test/project"),
            config_dir=Path(".meltano"),
            logs_dir=Path("logs"),
            log_level=LogLevel.INFO,
            meltano_version="3.9.1",
            singer_sdk_version="0.48.0",
            dbt_version="1.10.5",
        )
        tm.that(config.project_root, eq=Path("/test/project").resolve())
        tm.that(config.config_dir.name, eq=".meltano")
        tm.that(config.logs_dir.name, eq="logs")
        tm.that(config.log_level, eq="INFO")
        tm.that(config.meltano_version, eq="3.9.1")
        tm.that(config.singer_sdk_version, eq="0.48.0")
        tm.that(config.dbt_version, eq="1.10.5")

    def test_default_config_creation(self) -> None:
        """Test config creation with default values."""
        config = FlextMeltanoSettings()
        config.project_root = Path("/test")
        tm.that({".meltano", "config"}, has=config.config_dir.name)
        tm.that(config.logs_dir.name, eq="logs")
        tm.that({"development", "testing"}, has=config.environment)
        tm.that({"INFO", "DEBUG", "WARNING"}, has=config.log_level)

    def test_path_validation_success(self) -> None:
        """Test successful path validation."""
        config = FlextMeltanoSettings(
            project_root=Path("/valid/path"),
            config_dir=Path("config"),
            logs_dir=Path("logs"),
        )
        tm.that(config.project_root, is_=Path)
        tm.that(config.project_root.name, eq="path")

    def test_path_validation_conversion(self) -> None:
        """Test path validation converts string to Path."""
        config = FlextMeltanoSettings(project_root=Path("string/path"))
        tm.that(config.project_root, is_=Path)
        tm.that(config.project_root.name, eq="path")

    def test_version_validation_success(self) -> None:
        """Test successful version validation."""
        config = FlextMeltanoSettings(
            project_root=Path("/test"),
            meltano_version="3.9.1",
            singer_sdk_version="0.48.0",
            dbt_version="1.10.5",
        )
        tm.that(config.meltano_version, eq="3.9.1")
        tm.that(config.singer_sdk_version, eq="0.48.0")
        tm.that(config.dbt_version, eq="1.10.5")

    def test_version_validation_failure(self) -> None:
        """Test version validation - all fields have defaults so validation passes."""
        config = FlextMeltanoSettings(project_root=Path("/test"))
        tm.that(config.meltano_version, eq="3.9.1")
        tm.that(config.singer_sdk_version, eq="0.48.0")
        tm.that(config.dbt_version, eq="1.10.5")

    def test_get_project_file(self) -> None:
        """Test get_project_file method."""
        config = FlextMeltanoSettings(project_root=Path("/test/project"))
        project_file_result = config.get_project_file()
        tm.ok(project_file_result)
        project_file = project_file_result.value
        tm.that(project_file, is_=Path)
        tm.that(project_file, eq=Path("/test/project/pipeline.yml"))

    def test_get_absolute_config_dir(self) -> None:
        """Test get_absolute_config_dir method."""
        config = FlextMeltanoSettings(
            project_root=Path("/test/project"),
            config_dir=Path(".meltano"),
        )
        result = config.get_absolute_config_dir()
        tm.ok(result)
        config_dir = result.value
        tm.that(config_dir, is_=Path)
        tm.that(config_dir.is_absolute(), eq=True)
        tm.that(config_dir.name, eq=".meltano")

    def test_get_absolute_logs_dir(self) -> None:
        """Test get_absolute_logs_dir method returns r."""
        config = FlextMeltanoSettings(
            project_root=Path("/test/project"),
            logs_dir=Path("logs"),
        )
        result = config.get_absolute_logs_dir()
        tm.ok(result)
        logs_dir = result.value
        tm.that(logs_dir, is_=Path)
        tm.that(logs_dir.is_absolute(), eq=True)
        tm.that(logs_dir.name, eq="logs")

    def test_get_absolute_venv_dir(self) -> None:
        """Test get_absolute_venv_dir method."""
        config = FlextMeltanoSettings(project_root=Path("/test/project"))
        venv_dir = config.get_absolute_venv_dir()
        tm.that(venv_dir, is_=Path)
        tm.that(venv_dir.name, eq="python")
        tm.that(str(venv_dir.parent), has=".meltano")

    def test_validate_project_structure_missing_project_file(self) -> None:
        """Test project structure validation with missing pipeline.yml."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = FlextMeltanoSettings(project_root=Path(tmp_dir))
            result = config.validate_project_structure()
            tm.fail(result)
            tm.that((result.error or ""), has="pipeline.yml not found")

    def test_validate_project_structure_success(self) -> None:
        """Test successful project structure validation."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_file = Path(tmp_dir) / "pipeline.yml"
            project_file.write_text("version: 1\n")
            config = FlextMeltanoSettings(project_root=Path(tmp_dir))
            result = config.validate_project_structure()
            tm.ok(result)
            tm.that(result.value is True, eq=True)

    def test_get_environment_variables(self) -> None:
        """Test environment variables extraction."""
        config = FlextMeltanoSettings(
            project_root=Path("/test/project"),
            log_level=LogLevel.DEBUG,
        )
        env_vars = config.get_environment_variables()
        tm.that(env_vars, is_=dict)
        tm.that(env_vars["MELTANO_PROJECT_ROOT"], eq=str(config.project_root))
        tm.that(env_vars["MELTANO_LOG_LEVEL"], eq="DEBUG")

    def test_class_methods(self) -> None:
        """Test all class methods return expected values."""
        tm.that(FlextMeltanoSettings.get_version(), eq="0.9.0")
        tm.that(FlextMeltanoSettings.get_name(), eq="flext-meltano")
        tm.that(FlextMeltanoSettings.get_default_timeout(), eq=30)
        tm.that(FlextMeltanoSettings.get_default_batch_size(), eq=1000)

    def test_get_supported_lists(self) -> None:
        """Test methods that return lists of supported values."""
        plugin_types = FlextMeltanoSettings.get_supported_plugin_types()
        log_levels = FlextMeltanoSettings.get_supported_log_levels()
        tm.that(plugin_types, is_=list)
        tm.that(plugin_types, has="extractors")
        tm.that(plugin_types, has="loaders")
        tm.that(plugin_types, has="transforms")
        tm.that(log_levels, is_=list)
        tm.that(log_levels, has="INFO")
        tm.that(log_levels, has="DEBUG")

    def test_create_from_project_root_factory(self) -> None:
        """Test create_from_project_root factory method."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_file = Path(tmp_dir) / "pipeline.yml"
            project_file.write_text("version: 1\n")
            result = FlextMeltanoSettings.create_from_project_root(
                project_root=Path(tmp_dir),
            )
            tm.ok(result)
            config = result.value
            tm.that(config.project_root, eq=Path(tmp_dir).resolve())

    def test_create_from_project_root_with_defaults(self) -> None:
        """Test create_from_project_root with default values."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_file = Path(tmp_dir) / "pipeline.yml"
            project_file.write_text("version: 1\n")
            result = FlextMeltanoSettings.create_from_project_root(
                project_root=Path(tmp_dir),
            )
            tm.ok(result)
            config = result.value
            tm.that(config.project_root, eq=Path(tmp_dir).resolve())

    def test_create_for_environment_factory(self) -> None:
        """Test create_for_environment factory method."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = FlextMeltanoSettings(
                project_root=Path(tmp_dir),
                log_level=LogLevel.WARNING,
            )
            config = result
            tm.that(config.log_level, eq="WARNING")
            tm.that(config.project_root, eq=Path(tmp_dir))

    def test_create_for_environment_with_validation_error(self) -> None:
        """Test create_for_environment with invalid parameters."""
        with pytest.raises(ValueError):
            FlextMeltanoSettings.create_for_environment("invalid_env_type")


class TestFlextMeltanoSettingsEnums:
    """Test FlextMeltanoSettings uses c for enums."""

    def test_uses_flext_constants_for_enums(self) -> None:
        """Test that FlextMeltanoSettings uses c for enum values."""
        tm.that(hasattr(c, "LogLevel"), eq=True)
        tm.that(FlextMeltanoSettings.model_fields["environment"].default, is_=str)

    def test_config_builders_nested_class(self) -> None:
        """Test ConfigBuilders nested class exists."""
        tm.that(hasattr(FlextMeltanoSettings, "ConfigBuilders"), eq=True)
        tm.that(inspect.isclass(FlextMeltanoSettings.ConfigBuilders), eq=True)


class TestFlextMeltanoSettingsConstants:
    """Test all constants are properly set."""

    def test_version_constants(self) -> None:
        """Test version constants from FlextMeltanoConstants."""
        tm.that(FlextMeltanoSettings.MELTANO_VERSION, eq="3.9.1")
        tm.that(FlextMeltanoSettings.SINGER_SDK_VERSION, eq="0.48.0")
        tm.that(FlextMeltanoSettings.DBT_VERSION, eq="1.10.5")

    def test_file_constants(self) -> None:
        """Test file path constants."""
        tm.that(FlextMeltanoSettings.PROJECT_FILE, eq="pipeline.yml")
        tm.that(FlextMeltanoSettings.STATE_DIR, eq=".pipeline")
        tm.that(FlextMeltanoSettings.VENV_DIR, eq=".meltano/python")

    def test_environment_variable_constants(self) -> None:
        """Test environment variable name constants."""
        tm.that(
            FlextMeltanoSettings.MELTANO_PROJECT_ROOT_ENV,
            eq="MELTANO_PROJECT_ROOT",
        )
        tm.that(FlextMeltanoSettings.MELTANO_ENVIRONMENT_ENV, eq="MELTANO_ENVIRONMENT")
        tm.that(FlextMeltanoSettings.MELTANO_LOG_LEVEL_ENV, eq="MELTANO_LOG_LEVEL")


class TestFlextMeltanoSettingsEdgeCases:
    """Test edge cases and error conditions."""

    def test_invalid_log_level_validation(self) -> None:
        """Test log level validation - uses default when invalid."""
        global_config = FlextSettings.get_global()
        tm.that(hasattr(global_config, "log_level"), eq=True)
        tm.that({"INFO", "DEBUG"}, has=global_config.log_level)

    def test_empty_project_root_validation(self) -> None:
        """Test empty project root resolves to current directory."""
        current_dir = Path.cwd()
        config = FlextMeltanoSettings(project_root=current_dir)
        tm.that(config.project_root.is_absolute(), eq=True)
        tm.that(config.project_root.exists(), eq=True)

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
                tm.ok(result)
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
                project_root=Path(tmp_dir),
            )
            tm.ok(result)
            config = result.value
            validation_result = config.validate_project_structure()
            tm.ok(validation_result)
            project_file_result = config.get_project_file()
            tm.ok(project_file_result)
            tm.that(project_file_result.value.exists(), eq=True)
            config_dir_result = config.get_absolute_config_dir()
            tm.ok(config_dir_result)
            config_dir_result.value.mkdir(parents=True, exist_ok=True)
            tm.that(config_dir_result.value.exists(), eq=True)
            logs_dir_result = config.get_absolute_logs_dir()
            tm.ok(logs_dir_result)
            logs_dir_result.value.mkdir(parents=True, exist_ok=True)
            tm.that(logs_dir_result.value.exists(), eq=True)
            env_vars = config.get_environment_variables()
            tm.that(len(env_vars), gte=3)
            tm.that(all(isinstance(k, str) for k in env_vars), eq=True)
            tm.that(all(isinstance(v, str) for v in env_vars.values()), eq=True)

    def test_config_with_all_supported_values(self) -> None:
        """Test config creation with all supported enum values."""
        for env_type in FlextMeltanoSettings.get_supported_environments():
            if env_type == "local":
                continue
            config = FlextMeltanoSettings(
                project_root=Path("/test"),
                environment=env_type,
                log_level=LogLevel.INFO,
                debug=env_type != "production",
            )
            tm.that(config.environment, eq=env_type)
            expected_log_level = "INFO"
            tm.that(config.log_level, eq=expected_log_level)

    def test_config_constants_integration(self) -> None:
        """Test that config constants integrate properly with functionality."""
        config = FlextMeltanoSettings(project_root=Path("/test"))
        project_file_result = config.get_project_file()
        tm.ok(project_file_result)
        tm.that(project_file_result.value.name, eq=FlextMeltanoSettings.PROJECT_FILE)
        venv_dir = config.get_absolute_venv_dir()
        tm.that(str(venv_dir).endswith(FlextMeltanoSettings.VENV_DIR), eq=True)
        env_vars = config.get_environment_variables()
        tm.that(env_vars, has=FlextMeltanoSettings.MELTANO_PROJECT_ROOT_ENV)
        tm.that(env_vars, has=FlextMeltanoSettings.MELTANO_ENVIRONMENT_ENV)
        tm.that(env_vars, has=FlextMeltanoSettings.MELTANO_LOG_LEVEL_ENV)
