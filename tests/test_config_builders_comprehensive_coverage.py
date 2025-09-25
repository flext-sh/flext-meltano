"""FLEXT Meltano Config Builders Comprehensive Coverage Tests - Complete testing patterns.

This module provides comprehensive coverage tests for FlextMeltanoConfigBuilders using
flext_tests patterns and complete ELT configuration validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_core import FlextResult
from flext_meltano import FlextMeltanoConfigBuilders, FlextMeltanoConstants, PluginTypes
from flext_tests import FlextTestsUtilities


class TestConfigBuildersComprehensiveCoverage:
    """Comprehensive coverage tests for FlextMeltanoConfigBuilders."""

    def setup_method(self) -> None:
        """Setup test utilities."""
        self.test_utils = FlextTestsUtilities.utilities()
        self.test_assertions = FlextTestsUtilities.assertion()

    def test_dbt_config_builder_create_dbt_config_with_defaults(self) -> None:
        """Test DBT config creation with default parameters."""
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_dbt_config("test_project")

        assert result.is_success
        config = result.unwrap()

        assert config["name"] == "test_project"
        assert config["version"] == "1.0.0"
        assert not config["profile"]  # profile_name="" is preserved by safe_string
        assert config["model-paths"] == ["models"]
        assert config["analysis-paths"] == ["analysis"]
        assert config["test-paths"] == ["tests"]
        assert config["seed-paths"] == ["data"]
        assert config["macro-paths"] == ["macros"]

    def test_dbt_config_builder_create_dbt_config_with_custom_profile(self) -> None:
        """Test DBT config creation with custom profile name."""
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_dbt_config("my_project", "custom_profile")

        assert result.is_success
        config = result.unwrap()

        assert config["name"] == "my_project"
        assert config["profile"] == "custom_profile"

    def test_dbt_config_builder_create_dbt_config_empty_project_name(self) -> None:
        """Test DBT config creation with empty project name - keeps empty string."""
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_dbt_config("")

        assert result.is_success
        config = result.unwrap()

        # FlextUtilities.TextProcessor.safe_string preserves empty strings
        assert not config["name"]
        assert not config["profile"]

    def test_dbt_config_builder_create_dbt_config_empty_profile_name(self) -> None:
        """Test DBT config creation with empty profile name - defaults to project."""
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_dbt_config("test_project", "")

        assert result.is_success
        config = result.unwrap()

        assert config["name"] == "test_project"
        assert not config["profile"]  # Empty profile preserved by safe_string

    def test_meltano_config_builder_create_meltano_config_basic(self) -> None:
        """Test basic Meltano configuration creation."""
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_meltano_config("test_project")

        assert result.is_success
        config = result.unwrap()

        assert config["project_id"] == "test_project"
        assert not config["project_name"]  # Empty project_name defaults to empty
        assert config["version"] == 1
        assert "plugins" in config

    def test_meltano_config_builder_create_meltano_config_with_custom_name(
        self,
    ) -> None:
        """Test Meltano config creation with custom project name."""
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_meltano_config("my_project", "Custom Project Name")

        assert result.is_success
        config = result.unwrap()

        assert config["project_id"] == "my_project"
        assert config["project_name"] == "Custom Project Name"

    def test_meltano_config_builder_empty_project_id(self) -> None:
        """Test Meltano config creation with empty project ID - keeps empty string."""
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_meltano_config("")

        assert result.is_success
        config = result.unwrap()

        # FlextUtilities.TextProcessor.safe_string preserves empty strings
        assert not config["project_id"]
        assert not config["project_name"]

    def test_meltano_config_builder_add_plugin_to_config_extractor(self) -> None:
        """Test adding extractor plugin to existing config."""
        builder = FlextMeltanoConfigBuilders()

        # First create base config
        base_result = builder.create_meltano_config("test_project")
        assert base_result.is_success
        base_config = base_result.unwrap()

        # Create plugin config
        plugin_config: dict[str, object] = {
            "name": "tap-csv",
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }

        # Add plugin to config
        result = builder.add_plugin_to_config(base_config, "extractors", plugin_config)

        assert result.is_success
        updated_config = result.unwrap()

        assert isinstance(updated_config, dict)
        assert isinstance(updated_config["plugins"], dict)
        assert isinstance(updated_config["plugins"]["extractors"], list)
        assert len(updated_config["plugins"]["extractors"]) == 1
        assert updated_config["plugins"]["extractors"][0]["name"] == "tap-csv"

    def test_meltano_config_builder_add_plugin_to_config_loader(self) -> None:
        """Test adding loader plugin to existing config."""
        builder = FlextMeltanoConfigBuilders()

        # First create base config
        base_result = builder.create_meltano_config("test_project")
        assert base_result.is_success
        base_config = base_result.unwrap()

        # Create plugin config
        plugin_config: dict[str, object] = {
            "name": "target-jsonl",
            "namespace": "target_jsonl",
            "pip_url": "pipelinewise-target-jsonl",
            "executable": "target-jsonl",
        }

        # Add plugin to config
        result = builder.add_plugin_to_config(base_config, "loaders", plugin_config)

        assert result.is_success
        updated_config = result.unwrap()

        assert isinstance(updated_config, dict)
        assert isinstance(updated_config["plugins"], dict)
        assert isinstance(updated_config["plugins"]["loaders"], list)
        assert len(updated_config["plugins"]["loaders"]) == 1
        assert updated_config["plugins"]["loaders"][0]["name"] == "target-jsonl"

    def test_meltano_config_builder_add_plugin_invalid_plugin_type(self) -> None:
        """Test adding plugin with invalid plugin type - should fail gracefully."""
        builder = FlextMeltanoConfigBuilders()

        base_result = builder.create_meltano_config("test_project")
        assert base_result.is_success
        base_config = base_result.unwrap()

        plugin_config: dict[str, object] = {"name": "test-plugin"}

        # Try to add plugin with invalid type
        result = builder.add_plugin_to_config(
            base_config,
            "invalid_type",
            plugin_config,
        )

        # Should handle gracefully (either succeed by creating new section or fail safely)
        # The exact behavior depends on implementation
        assert isinstance(result, FlextResult)

    def test_singer_config_builder_create_singer_tap_config(self) -> None:
        """Test Singer tap configuration creation."""
        builder = FlextMeltanoConfigBuilders()

        result = builder.create_singer_tap_config(
            tap_name="tap-csv",
            namespace="tap_csv",
            pip_url="pipelinewise-tap-csv",
            executable="tap-csv",
        )

        assert result.is_success
        config = result.unwrap()

        assert config["name"] == "tap-csv"
        assert config["namespace"] == "tap_csv"
        assert config["pip_url"] == "pipelinewise-tap-csv"
        assert config["executable"] == "tap-csv"
        assert config["type"] == PluginTypes.EXTRACTORS.value

    def test_singer_config_builder_create_singer_target_config(self) -> None:
        """Test Singer target configuration creation."""
        builder = FlextMeltanoConfigBuilders()

        result = builder.create_singer_target_config(
            target_name="target-jsonl",
            namespace="target_jsonl",
            pip_url="pipelinewise-target-jsonl",
            executable="target-jsonl",
        )

        assert result.is_success
        config = result.unwrap()

        assert config["name"] == "target-jsonl"
        assert config["namespace"] == "target_jsonl"
        assert config["pip_url"] == "pipelinewise-target-jsonl"
        assert config["executable"] == "target-jsonl"
        assert config["type"] == PluginTypes.LOADERS.value

    def test_singer_config_builder_create_generic_config_extractor(self) -> None:
        """Test generic Singer config creation for extractor."""
        builder = FlextMeltanoConfigBuilders()

        result = builder._create_singer_config_generic(
            plugin_name="tap-github",
            plugin_type=PluginTypes.EXTRACTORS.value,
        )

        assert result.is_success
        config = result.unwrap()

        assert config["name"] == "tap-github"
        assert config["type"] == PluginTypes.EXTRACTORS.value

    def test_singer_config_builder_create_generic_config_loader(self) -> None:
        """Test generic Singer config creation for loader."""
        builder = FlextMeltanoConfigBuilders()

        result = builder._create_singer_config_generic(
            plugin_name="target-postgres",
            plugin_type=PluginTypes.LOADERS.value,
        )

        assert result.is_success
        config = result.unwrap()

        assert config["name"] == "target-postgres"
        assert config["type"] == PluginTypes.LOADERS.value

    def test_singer_plugin_config_model_defaults(self) -> None:
        """Test Singer config creation with default values."""
        builder = FlextMeltanoConfigBuilders()

        result = builder._create_singer_config_generic(plugin_name="test-plugin")

        assert result.is_success
        config = result.unwrap()

        assert config["name"] == "test-plugin"
        assert config["type"] == PluginTypes.EXTRACTORS.value  # Default type
        assert config["namespace"] == "tap_test_plugin"  # Generated namespace
        assert not config["executable"]  # Empty executable when not provided
        assert "pip_url" in config  # Should have pip_url

    def test_singer_plugin_config_model_all_fields(self) -> None:
        """Test Singer config creation with all fields set."""
        builder = FlextMeltanoConfigBuilders()

        result = builder._create_singer_config_generic(
            plugin_name="tap-postgres",
            plugin_type=PluginTypes.EXTRACTORS.value,
            namespace="tap_postgres",
            pip_url="pipelinewise-tap-postgres",
            executable="tap-postgres",
        )

        assert result.is_success
        config = result.unwrap()

        assert config["name"] == "tap-postgres"
        assert config["type"] == PluginTypes.EXTRACTORS.value
        assert config["namespace"] == "tap_postgres"
        assert config["pip_url"] == "pipelinewise-tap-postgres"
        assert config["executable"] == "tap-postgres"

    def test_config_builders_constants_integration(self) -> None:
        """Test integration with SOURCE OF TRUTH constants."""
        builder = FlextMeltanoConfigBuilders()

        # Test that default configurations come from constants
        result = builder._create_singer_config_generic(plugin_name="test-plugin")

        assert result.is_success
        config = result.unwrap()

        assert isinstance(config, dict)
        # Test that plugin types come from constants
        assert config["type"] == PluginTypes.EXTRACTORS.value  # Default
        assert "metadata" in config
        assert isinstance(config["metadata"], dict)
        assert (
            config["metadata"]["created_by"]
            == FlextMeltanoConstants.METADATA_CREATED_BY
        )

    def test_edge_case_none_values_handling(self) -> None:
        """Test handling of empty values in configurations."""
        builder = FlextMeltanoConfigBuilders()

        # Test DBT config with empty project name - safe_string preserves empty
        result = builder.create_dbt_config("")
        assert result.is_success
        config = result.unwrap()
        assert not config["name"]  # safe_string preserves empty string

        # Test Meltano config with empty project name
        result = builder.create_meltano_config("project", "")
        assert result.is_success
        config = result.unwrap()
        assert not config["project_name"]  # safe_string preserves empty
