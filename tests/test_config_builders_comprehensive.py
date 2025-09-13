
import concurrent.futures
import shutil
import tempfile
from pathlib import Path

import pytest
from flext_tests import FlextTestsMatchers

from flext_meltano.config_builders import FlextMeltanoConfigBuilders
from flext_meltano.constants import PluginTypes

"""FLEXT Meltano Config Builders Comprehensive Tests - Advanced testing patterns.

This module provides comprehensive tests for FlextMeltanoConfigBuilders using
advanced testing patterns and comprehensive ELT configuration validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


class TestSingerConfigComprehensive:
    """Comprehensive tests for Singer configuration through unified methods."""

    def test_singer_tap_config_creation_with_params(self) -> None:
        """Test creating tap configuration with all parameters."""
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_singer_tap_config(
            tap_name="tap-csv",
            namespace="tap_csv",
            pip_url="pipelinewise-tap-csv",
            executable="tap-csv",
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value
        assert config["name"] == "tap-csv"
        assert config["type"] == PluginTypes.EXTRACTORS.value  # SOURCE OF TRUTH
        assert config["namespace"] == "tap_csv"
        assert config["pip_url"] == "pipelinewise-tap-csv"
        assert config["executable"] == "tap-csv"

    def test_singer_tap_config_defaults(self) -> None:
        """Test default values for tap configuration."""
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_singer_tap_config("tap-postgres")

        FlextTestsMatchers.assert_result_success(result)
        config = result.value
        assert config["name"] == "tap-postgres"
        assert config["type"] == PluginTypes.EXTRACTORS.value  # SOURCE OF TRUTH
        assert "namespace" in config
        assert "executable" in config

    def test_singer_target_config_creation(self) -> None:
        """Test creating target configuration."""
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_singer_target_config(
            target_name="target-postgres",
            namespace="target_postgres",
            pip_url="pipelinewise-target-postgres",
            executable="target-postgres",
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value
        assert config["type"] == PluginTypes.LOADERS.value  # SOURCE OF TRUTH
        assert config["name"] == "target-postgres"
        assert config["namespace"] == "target_postgres"
        assert config["pip_url"] == "pipelinewise-target-postgres"
        assert config["executable"] == "target-postgres"

    def test_singer_config_validation_edge_cases(self) -> None:
        """Test Singer configuration validation edge cases."""
        builder = FlextMeltanoConfigBuilders()

        # Test with empty names (should be handled gracefully)
        tap_result = builder.create_singer_tap_config("")
        FlextTestsMatchers.assert_result_success(tap_result)

        target_result = builder.create_singer_target_config("")
        FlextTestsMatchers.assert_result_success(target_result)


class TestFlextMeltanoConfigBuildersDbtComprehensive:
    """Comprehensive tests for DBT configuration builder."""

    def test_create_dbt_config_basic(self) -> None:
        """Test creating basic DBT configuration."""
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_dbt_config(project_name="test_project")

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        assert isinstance(config, dict)
        assert config["name"] == "test_project"
        assert config["version"] == "1.0.0"
        assert isinstance(config["profile"], str)  # Profile field exists
        assert "model-paths" in config
        assert "target-path" in config

    def test_create_dbt_config_with_profile(self) -> None:
        """Test creating DBT configuration with custom profile."""
        result = FlextMeltanoConfigBuilders().create_dbt_config(
            project_name="analytics_project", profile_name="prod_analytics"
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        assert config["name"] == "analytics_project"
        assert config["profile"] == "prod_analytics"

    def test_create_dbt_config_empty_project_name(self) -> None:
        """Test creating DBT configuration with empty project name."""
        result = FlextMeltanoConfigBuilders().create_dbt_config(project_name="")

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        # Should handle empty project name gracefully
        assert isinstance(config["name"], str)
        assert "version" in config
        assert "profile" in config

    def test_create_dbt_config_special_characters(self) -> None:
        """Test DBT configuration with special characters."""
        result = FlextMeltanoConfigBuilders().create_dbt_config(
            project_name="project@#$%^&*()", profile_name="profile!@#$%^&*()"
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        # Should handle special characters safely
        assert isinstance(config["name"], str)
        assert isinstance(config["profile"], str)
        assert len(config["name"]) > 0
        assert len(config["profile"]) > 0

    def test_dbt_config_structure_completeness(self) -> None:
        """Test that DBT configuration has all required structure."""
        result = FlextMeltanoConfigBuilders().create_dbt_config("complete_project")

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        # Verify all essential DBT configuration keys
        essential_keys = [
            "name",
            "version",
            "profile",
            "model-paths",
            "analysis-paths",
            "test-paths",
            "seed-paths",
            "macro-paths",
            "snapshot-paths",
            "target-path",
            "clean-targets",
        ]

        for key in essential_keys:
            assert key in config, f"Missing essential key: {key}"

    @pytest.mark.parametrize(
        ("project_name", "profile_name"),
        [
            ("simple_project", "simple_profile"),
            ("project-with-dashes", "profile-with-dashes"),
            ("project_with_underscores", "profile_with_underscores"),
            ("project123", "profile456"),
            ("UPPERCASE_PROJECT", "UPPERCASE_PROFILE"),
        ],
    )
    def test_dbt_config_parametrized_names(
        self, project_name: str, profile_name: str
    ) -> None:
        """Test DBT configuration with various naming patterns."""
        result = FlextMeltanoConfigBuilders().create_dbt_config(
            project_name=project_name, profile_name=profile_name
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        assert isinstance(config["name"], str)
        assert isinstance(config["profile"], str)
        assert len(config["name"]) > 0
        assert len(config["profile"]) > 0


class TestFlextMeltanoConfigBuildersSingerComprehensive:
    """Comprehensive tests for Singer configuration builders."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self) -> None:
        """Cleanup after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_create_tap_config_basic(self) -> None:
        """Test creating basic tap configuration."""
        result = FlextMeltanoConfigBuilders().create_singer_tap_config(
            tap_name="tap-csv"
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        assert isinstance(config, dict)
        assert config["name"] == "tap-csv"
        assert config["type"] == PluginTypes.EXTRACTORS.value  # SOURCE OF TRUTH
        assert "namespace" in config
        assert "executable" in config

    def test_create_tap_config_with_parameters(self) -> None:
        """Test creating tap configuration with custom parameters."""
        result = FlextMeltanoConfigBuilders().create_singer_tap_config(
            tap_name="tap-postgres",
            namespace="tap_postgres",
            pip_url="pipelinewise-tap-postgres",
            executable="tap-postgres",
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        assert config["name"] == "tap-postgres"
        assert config["namespace"] == "tap_postgres"
        assert config["pip_url"] == "pipelinewise-tap-postgres"
        assert config["executable"] == "tap-postgres"

    def test_create_tap_config_empty_name(self) -> None:
        """Test creating tap configuration with empty name."""
        result = FlextMeltanoConfigBuilders().create_singer_tap_config(tap_name="")

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        # Should handle empty name gracefully
        assert isinstance(config["name"], str)
        assert "type" in config
        assert config["type"] == PluginTypes.EXTRACTORS.value  # SOURCE OF TRUTH

    def test_create_target_config_basic(self) -> None:
        """Test creating basic target configuration."""
        result = FlextMeltanoConfigBuilders().create_singer_target_config(
            target_name="target-postgres"
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        assert config["name"] == "target-postgres"
        assert config["type"] == PluginTypes.LOADERS.value  # SOURCE OF TRUTH
        assert "namespace" in config
        assert "executable" in config

    def test_create_target_config_with_parameters(self) -> None:
        """Test creating target configuration with custom parameters."""
        result = FlextMeltanoConfigBuilders().create_singer_target_config(
            target_name="target-snowflake",
            namespace="target_snowflake",
            pip_url="pipelinewise-target-snowflake",
            executable="target-snowflake",
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        assert config["name"] == "target-snowflake"
        assert config["namespace"] == "target_snowflake"
        assert config["pip_url"] == "pipelinewise-target-snowflake"
        assert config["executable"] == "target-snowflake"

    def test_singer_config_error_handling(self) -> None:
        """Test error handling in Singer configuration builders."""
        # Test with empty tap name (should handle gracefully)
        result = FlextMeltanoConfigBuilders().create_singer_tap_config(tap_name="")

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        # Should handle empty name gracefully
        assert isinstance(config["name"], str)
        assert config["type"] == PluginTypes.EXTRACTORS.value  # SOURCE OF TRUTH

    @pytest.mark.parametrize(
        ("tap_name", "expected_normalized"),
        [
            ("tap-csv", "tap-csv"),
            ("tap_postgres", "tap_postgres"),
            ("TAP-MYSQL", "TAP-MYSQL"),
            ("tap.special.dots", "tap.special.dots"),
        ],
    )
    def test_tap_config_name_handling(
        self, tap_name: str, expected_normalized: str
    ) -> None:
        """Test tap configuration name handling."""
        result = FlextMeltanoConfigBuilders().create_singer_tap_config(
            tap_name=tap_name
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value
        # Verify the tap name is preserved in the configuration
        assert config["name"] == tap_name
        # Verify the normalized name matches expected
        assert config["name"] == expected_normalized

        # Name should be preserved as-is after safe_string processing
        assert isinstance(config["name"], str)
        assert len(config["name"]) > 0


class TestFlextMeltanoConfigBuildersMeltanoComprehensive:
    """Comprehensive tests for Meltano configuration builders."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self) -> None:
        """Cleanup after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_create_meltano_config_basic(self) -> None:
        """Test creating basic meltano configuration."""
        result = FlextMeltanoConfigBuilders().create_meltano_config(
            project_id="test_project"
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        assert isinstance(config, dict)
        assert config["project_id"] == "test_project"
        assert config["version"] == 1
        assert "plugins" in config
        assert "environments" in config

    def test_create_meltano_config_with_project_name(self) -> None:
        """Test creating meltano configuration with custom project name."""
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_meltano_config(
            project_id="analytics_project", project_name="Analytics Project"
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        assert config["project_id"] == "analytics_project"
        assert config["project_name"] == "Analytics Project"
        assert "extractors" in config["plugins"]
        assert "loaders" in config["plugins"]

    def test_create_meltano_config_environments_structure(self) -> None:
        """Test meltano configuration has proper environments structure."""
        result = FlextMeltanoConfigBuilders().create_meltano_config(
            project_id="env_project"
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        assert "environments" in config
        environments = config["environments"]
        assert isinstance(environments, list)
        assert len(environments) == 3  # dev, staging, prod

        # Check environment structure
        env_names = [env["name"] for env in environments]
        assert "dev" in env_names
        assert "staging" in env_names
        assert "prod" in env_names

    def test_meltano_config_structure_completeness(self) -> None:
        """Test that meltano config has complete structure."""
        result = FlextMeltanoConfigBuilders().create_meltano_config(
            project_id="complete_project"
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        # Essential meltano config keys
        essential_keys = ["project_id", "version", "plugins", "environments"]
        for key in essential_keys:
            assert key in config

        # Essential plugin types
        plugin_types = ["extractors", "loaders", "transformers", "orchestrators"]
        for plugin_type in plugin_types:
            assert plugin_type in config["plugins"]

    def test_meltano_config_metadata(self) -> None:
        """Test meltano configuration has proper metadata."""
        result = FlextMeltanoConfigBuilders().create_meltano_config(
            project_id="metadata_test"
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        assert "metadata" in config
        metadata = config["metadata"]
        assert metadata["created_by"] == "flext-meltano"
        assert "created_at" in metadata
        assert "flext_version" in metadata

    def test_meltano_config_error_handling(self) -> None:
        """Test error handling in Meltano configuration builders."""
        # Test with empty project ID (should handle gracefully)
        result = FlextMeltanoConfigBuilders().create_meltano_config(project_id="")

        FlextTestsMatchers.assert_result_success(result)
        config = result.value

        # Should handle empty string gracefully
        assert isinstance(config["project_id"], str)
        assert "version" in config
        assert "plugins" in config


class TestFlextMeltanoConfigBuildersIntegrationComprehensive:
    """Comprehensive integration tests for configuration builders."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self) -> None:
        """Cleanup after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_complete_project_configuration_workflow(self) -> None:
        """Test complete project configuration workflow."""
        # Create DBT configuration
        dbt_result = FlextMeltanoConfigBuilders().create_dbt_config(
            project_name="analytics_project", profile_name="prod_analytics"
        )
        FlextTestsMatchers.assert_result_success(dbt_result)

        # Create tap configuration
        tap_result = FlextMeltanoConfigBuilders().create_singer_tap_config(
            tap_name="tap-postgres", pip_url="pipelinewise-tap-postgres"
        )
        FlextTestsMatchers.assert_result_success(tap_result)

        # Create target configuration
        target_result = FlextMeltanoConfigBuilders().create_singer_target_config(
            target_name="target-postgres", pip_url="pipelinewise-target-postgres"
        )
        FlextTestsMatchers.assert_result_success(target_result)

        # Create Meltano project configuration
        meltano_result = FlextMeltanoConfigBuilders().create_meltano_config(
            project_id="analytics_project", project_name="Analytics Project"
        )
        FlextTestsMatchers.assert_result_success(meltano_result)

        # Verify all configurations are consistent
        dbt_config = dbt_result.value
        tap_config = tap_result.value
        target_config = target_result.value
        meltano_config = meltano_result.value

        # Project names should match
        assert dbt_config["name"] == meltano_config["project_id"] == "analytics_project"

        # Plugin configurations should be valid
        assert tap_config["name"] == "tap-postgres"
        assert target_config["name"] == "target-postgres"
        assert "extractors" in meltano_config["plugins"]
        assert "loaders" in meltano_config["plugins"]

    def test_configuration_builders_performance(self, benchmark: object) -> None:
        """Test configuration builders performance."""

        def create_all_configs() -> None:
            # Create multiple configurations
            FlextMeltanoConfigBuilders().create_dbt_config("perf_test")
            FlextMeltanoConfigBuilders().create_singer_tap_config("tap-csv")
            FlextMeltanoConfigBuilders().create_singer_target_config("target-csv")
            FlextMeltanoConfigBuilders().create_meltano_config("perf_project")

        # All configurations should complete quickly
        benchmark(create_all_configs)

    def test_concurrent_configuration_building(self) -> None:
        """Test concurrent configuration building doesn't interfere."""

        def create_config(config_num: int) -> object:
            return FlextMeltanoConfigBuilders().create_dbt_config(
                f"project_{config_num}"
            )

        # Create multiple configurations concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(create_config, i) for i in range(10)]
            results = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        # All should succeed
        for result in results:
            FlextTestsMatchers.assert_result_success(result)
            assert isinstance(result.value, dict)
            assert "name" in result.value

    def test_configuration_consistency_across_builders(self) -> None:
        """Test configuration consistency across different builders."""
        project_name = "consistency_test"

        # Create configurations with same project name
        dbt_result = FlextMeltanoConfigBuilders().create_dbt_config(project_name)
        meltano_result = FlextMeltanoConfigBuilders().create_meltano_config(
            project_name
        )

        FlextTestsMatchers.assert_result_success(dbt_result)
        FlextTestsMatchers.assert_result_success(meltano_result)

        # Names should be consistent
        assert (
            dbt_result.value["name"]
            == meltano_result.value["project_id"]
            == project_name
        )

        # Both should have valid structure
        assert isinstance(dbt_result.value, dict)
        assert isinstance(meltano_result.value, dict)

    def test_unified_builder_methods_accessibility(self) -> None:
        """Test that unified builder methods are properly accessible."""
        # Should be able to access all methods on unified class
        builder = FlextMeltanoConfigBuilders()

        assert hasattr(builder, "create_dbt_config")
        assert hasattr(builder, "create_singer_tap_config")
        assert hasattr(builder, "create_singer_target_config")
        assert hasattr(builder, "create_meltano_config")

        # Verify methods are callable
        assert callable(builder.create_dbt_config)
        assert callable(builder.create_singer_tap_config)
        assert callable(builder.create_singer_target_config)
        assert callable(builder.create_meltano_config)

    @pytest.mark.parametrize(
        ("method_name", "args"),
        [
            ("create_dbt_config", ("test_project",)),
            ("create_singer_tap_config", ("test_tap",)),
            ("create_singer_target_config", ("test_target",)),
            ("create_meltano_config", ("test_meltano",)),
        ],
    )
    def test_builder_methods_parametrized(self, method_name: str, args: tuple) -> None:
        """Test builder methods with parametrized inputs."""
        builder = FlextMeltanoConfigBuilders()
        method = getattr(builder, method_name)

        result = method(*args)
        FlextTestsMatchers.assert_result_success(result)
        assert isinstance(result.value, dict)
