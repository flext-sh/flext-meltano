"""Tests for FLEXT Meltano simple API.

Comprehensive tests for simple API functionality.
Zero tolerance for untested code.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from flext_meltano.config.settings import FlextMeltanoSettings
from flext_meltano.simple_api import (
    flext_create_basic_config,
    setup_meltano_simple,
)


class TestSetupMeltanoSimple:
    """Test setup_meltano_simple function."""

    def test_setup_with_string_path(self) -> None:
        """Test setup with string path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = setup_meltano_simple(temp_dir)

            assert result["success"] is True
            assert isinstance(result["settings"], FlextMeltanoSettings)
            assert result["project_root"] == str(Path(temp_dir))
            assert result["environment"] == "dev"  # default

    def test_setup_with_path_object(self) -> None:
        """Test setup with Path object."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path_obj = Path(temp_dir)
            result = setup_meltano_simple(path_obj)

            assert result["success"] is True
            assert isinstance(result["settings"], FlextMeltanoSettings)
            assert result["project_root"] == str(path_obj)
            assert result["environment"] == "dev"

    def test_setup_with_custom_environment(self) -> None:
        """Test setup with custom environment."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = setup_meltano_simple(temp_dir, environment="production")

            assert result["success"] is True
            assert result["environment"] == "production"
            settings = result["settings"]
            assert settings.environment == "production"

    def test_setup_with_dev_environment(self) -> None:
        """Test setup with dev environment explicitly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = setup_meltano_simple(temp_dir, environment="dev")

            assert result["success"] is True
            assert result["environment"] == "dev"

    def test_setup_with_staging_environment(self) -> None:
        """Test setup with staging environment."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = setup_meltano_simple(temp_dir, environment="staging")

            assert result["success"] is True
            assert result["environment"] == "staging"

    def test_setup_with_test_environment(self) -> None:
        """Test setup with test environment."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = setup_meltano_simple(temp_dir, environment="test")

            assert result["success"] is True
            assert result["environment"] == "test"

    def test_setup_result_structure(self) -> None:
        """Test that result structure is consistent."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = setup_meltano_simple(temp_dir)

            # Check all expected keys are present
            expected_keys = {"success", "settings", "project_root", "environment"}
            assert set(result.keys()) == expected_keys

            # Check data types
            assert isinstance(result["success"], bool)
            assert isinstance(result["settings"], FlextMeltanoSettings)
            assert isinstance(result["project_root"], str)
            assert isinstance(result["environment"], str)

    def test_setup_settings_configuration(self) -> None:
        """Test that settings are properly configured."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = setup_meltano_simple(temp_dir, environment="production")

            settings = result["settings"]
            assert settings.environment == "production"
            assert str(settings.project.project_root) == temp_dir
            assert settings.project.default_environment == "production"

    def test_setup_with_absolute_path(self) -> None:
        """Test setup with absolute path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            abs_path = Path(temp_dir).resolve()
            result = setup_meltano_simple(str(abs_path))

            assert result["success"] is True
            assert result["project_root"] == str(abs_path)

    def test_setup_with_relative_path(self) -> None:
        """Test setup with relative path."""
        result = setup_meltano_simple("./test_project")

        assert result["success"] is True
        assert "test_project" in result["project_root"]

    def test_setup_with_nonexistent_path(self) -> None:
        """Test setup with nonexistent path."""
        nonexistent_path = "/tmp/nonexistent/path/12345"  # noqa: S108
        result = setup_meltano_simple(nonexistent_path)

        # Should still work, as we're just configuring
        assert result["success"] is True
        assert result["project_root"] == nonexistent_path

    def test_setup_path_conversion_string_to_path(self) -> None:
        """Test that string paths are properly converted to Path objects."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = setup_meltano_simple(temp_dir)

            settings = result["settings"]
            assert isinstance(settings.project.project_root, Path)
            assert str(settings.project.project_root) == temp_dir

    def test_setup_path_conversion_path_object(self) -> None:
        """Test that Path objects are preserved."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path_obj = Path(temp_dir)
            result = setup_meltano_simple(path_obj)

            settings = result["settings"]
            assert isinstance(settings.project.project_root, Path)
            assert settings.project.project_root == path_obj

    def test_setup_multiple_calls_independence(self) -> None:
        """Test that multiple setup calls are independent."""
        with (
            tempfile.TemporaryDirectory() as temp_dir1,
            tempfile.TemporaryDirectory() as temp_dir2,
        ):
            result1 = setup_meltano_simple(temp_dir1, environment="dev")
            result2 = setup_meltano_simple(temp_dir2, environment="prod")

            assert result1["project_root"] != result2["project_root"]
            assert result1["environment"] != result2["environment"]
            assert result1["settings"] != result2["settings"]

    def test_setup_environment_variations(self) -> None:
        """Test various environment string formats."""
        environments = ["dev", "development", "prod", "production", "test", "staging"]

        with tempfile.TemporaryDirectory() as temp_dir:
            for env in environments:
                result = setup_meltano_simple(temp_dir, environment=env)
                assert result["success"] is True
                assert result["environment"] == env


class TestFlextCreateBasicConfig:
    """Test flext_create_basic_config function."""

    def test_create_basic_config_structure(self) -> None:
        """Test basic config structure."""
        config = flext_create_basic_config()

        # Check all expected keys are present
        expected_keys = {"version", "default_environment", "environments", "plugins"}
        assert set(config.keys()) == expected_keys

    def test_create_basic_config_values(self) -> None:
        """Test basic config values."""
        config = flext_create_basic_config()

        assert config["version"] == 1
        assert config["default_environment"] == "dev"

    def test_create_basic_config_environments(self) -> None:
        """Test environments configuration."""
        config = flext_create_basic_config()

        environments = config["environments"]
        assert isinstance(environments, list)
        assert len(environments) == 2
        assert {"name": "dev"} in environments
        assert {"name": "prod"} in environments

    def test_create_basic_config_plugins(self) -> None:
        """Test plugins configuration."""
        config = flext_create_basic_config()

        plugins = config["plugins"]
        assert isinstance(plugins, dict)

        expected_plugin_types = {"extractors", "loaders", "transformers"}
        assert set(plugins.keys()) == expected_plugin_types

        # All plugin types should be empty lists initially
        for plugin_type in expected_plugin_types:
            assert plugins[plugin_type] == []

    def test_create_basic_config_data_types(self) -> None:
        """Test data types in basic config."""
        config = flext_create_basic_config()

        assert isinstance(config["version"], int)
        assert isinstance(config["default_environment"], str)
        assert isinstance(config["environments"], list)
        assert isinstance(config["plugins"], dict)

    def test_create_basic_config_immutability(self) -> None:
        """Test that multiple calls return independent objects."""
        config1 = flext_create_basic_config()
        config2 = flext_create_basic_config()

        # Should be equal in content but different objects
        assert config1 == config2
        assert config1 is not config2
        assert config1["plugins"] is not config2["plugins"]
        assert config1["environments"] is not config2["environments"]

    def test_create_basic_config_modification_safety(self) -> None:
        """Test that modifying one config doesn't affect others."""
        config1 = flext_create_basic_config()
        config2 = flext_create_basic_config()

        # Modify config1
        config1["plugins"]["extractors"].append({"name": "tap-csv"})
        config1["environments"].append({"name": "staging"})

        # config2 should be unchanged
        assert config2["plugins"]["extractors"] == []
        assert len(config2["environments"]) == 2

    def test_create_basic_config_plugin_structure(self) -> None:
        """Test plugin structure details."""
        config = flext_create_basic_config()

        plugins = config["plugins"]

        # Each plugin type should be an empty list
        assert plugins["extractors"] == []
        assert plugins["loaders"] == []
        assert plugins["transformers"] == []

        # Lists should be mutable
        plugins["extractors"].append("test")
        assert "test" in plugins["extractors"]

    def test_create_basic_config_environment_structure(self) -> None:
        """Test environment structure details."""
        config = flext_create_basic_config()

        environments = config["environments"]

        # Should have exactly dev and prod environments
        env_names = {env["name"] for env in environments}
        assert env_names == {"dev", "prod"}

        # Each environment should be a dict with name key
        for env in environments:
            assert isinstance(env, dict)
            assert "name" in env
            assert isinstance(env["name"], str)

    def test_create_basic_config_consistency(self) -> None:
        """Test consistency across multiple calls."""
        configs = [flext_create_basic_config() for _ in range(5)]

        # All configs should be identical in structure and content
        first_config = configs[0]
        for config in configs[1:]:
            assert config == first_config

            # But should be different objects
            assert config is not first_config


class TestSimpleApiIntegration:
    """Test integration between simple API functions."""

    def test_setup_and_basic_config_compatibility(self) -> None:
        """Test that setup_meltano_simple is compatible with basic config format."""
        basic_config = flext_create_basic_config()

        with tempfile.TemporaryDirectory() as temp_dir:
            setup_result = setup_meltano_simple(
                temp_dir, environment=basic_config["default_environment"],
            )

            assert setup_result["environment"] == basic_config["default_environment"]
            assert setup_result["success"] is True

    def test_basic_config_environments_in_setup(self) -> None:
        """Test using basic config environments in setup."""
        basic_config = flext_create_basic_config()

        with tempfile.TemporaryDirectory() as temp_dir:
            for env_config in basic_config["environments"]:
                env_name = env_config["name"]
                result = setup_meltano_simple(temp_dir, environment=env_name)

                assert result["success"] is True
                assert result["environment"] == env_name
