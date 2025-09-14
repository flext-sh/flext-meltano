"""FLEXT Meltano Config Builders Complete Tests - Comprehensive testing patterns."""

from flext_core import FlextResult
from flext_tests import FlextTestsUtilities

from flext_meltano.config_builders import FlextMeltanoConfigBuilders
from flext_meltano.constants import PluginTypes


class TestFlextMeltanoConfigBuildersComplete:
    """Complete test suite for FlextMeltanoConfigBuilders using flext_tests exclusively."""

    def setup_method(self) -> None:
        """Setup for each test using flext_tests patterns."""
        self.test_utils = FlextTestsUtilities.utilities()
        self.test_assertions = FlextTestsUtilities.assertion()
        self.functional_service = FlextTestsUtilities.functional_service(
            "config_builders"
        )

    # =========================================================================
    # SINGER PLUGIN CONFIG MODEL TESTING - Using flext_tests patterns
    # =========================================================================

    def test_singer_tap_config_creation_with_parameters(self) -> None:
        """Test Singer tap config creation with parameters using flext_tests."""
        # Create tap config with all parameters
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_singer_tap_config(
            tap_name="tap-csv",
            namespace="tap_csv",
            pip_url="pipelinewise-tap-csv",
            executable="tap-csv",
        )

        # Use flext_tests assertions
        self.test_assertions.assert_true(
            condition=result.is_success,
            message="Tap config creation should succeed",
        )

        config = result.unwrap()
        self.test_assertions.assert_equals(
            actual=config["name"],
            expected="tap-csv",
            message="Plugin name should match",
        )
        self.test_assertions.assert_equals(
            actual=config["type"],
            expected=PluginTypes.EXTRACTORS.value,  # SOURCE OF TRUTH
            message="Plugin type should be extractor",
        )
        self.test_assertions.assert_equals(
            actual=config["namespace"],
            expected="tap_csv",
            message="Namespace should match",
        )
        self.test_assertions.assert_equals(
            actual=config["pip_url"],
            expected="pipelinewise-tap-csv",
            message="Pip URL should match",
        )
        self.test_assertions.assert_equals(
            actual=config["executable"],
            expected="tap-csv",
            message="Executable should match",
        )

    def test_singer_tap_config_defaults(self) -> None:
        """Test Singer tap config creation with default values using flext_tests."""
        # Create tap config with minimal parameters
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_singer_tap_config("tap-postgres")

        self.test_assertions.assert_true(
            condition=result.is_success,
            message="Tap config creation should succeed",
        )

        config = result.unwrap()
        self.test_assertions.assert_equals(
            actual=config["name"],
            expected="tap-postgres",
            message="Plugin name should be set",
        )
        self.test_assertions.assert_equals(
            actual=config["type"],
            expected=PluginTypes.EXTRACTORS.value,  # SOURCE OF TRUTH
            message="Should default to extractor",
        )
        self.test_assertions.assert_equals(
            actual=config["namespace"],
            expected="tap_tap_postgres",  # Generated namespace pattern when not provided
            message="Should generate default namespace pattern",
        )
        self.test_assertions.assert_equals(
            actual=config["pip_url"],
            expected="pipelinewise-tap-postgres",
            message="Should generate default pip_url",
        )
        self.test_assertions.assert_equals(
            actual=config["executable"],
            expected="",
            message="Should default to empty executable",
        )

    # =========================================================================
    # DBT CONFIG BUILDER TESTING - Lines 79-109 comprehensive coverage
    # =========================================================================

    def test_dbt_config_builder_basic_success(self) -> None:
        """Test successful DBT config creation using flext_tests."""
        # Test basic DBT config creation (lines 79-107)
        result = FlextMeltanoConfigBuilders().create_dbt_config("my_dbt_project")

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )
        self.test_assertions.assert_true(
            condition=result.is_success, message="DBT config creation should succeed"
        )

        config = result.unwrap()
        self.test_assertions.assert_equals(
            actual=config["name"],
            expected="my_dbt_project",
            message="Project name should match",
        )
        self.test_assertions.assert_equals(
            actual=config["version"],
            expected="1.0.0",
            message="Should set default version",
        )
        self.test_assertions.assert_equals(
            actual=config["profile"],
            expected="",
            message="Should default profile to empty when not provided",
        )

        # Test structure elements
        self.test_assertions.assert_in(
            item="model-paths", container=config, message="Should include model-paths"
        )
        self.test_assertions.assert_in(
            item="test-paths", container=config, message="Should include test-paths"
        )
        self.test_assertions.assert_in(
            item="metadata", container=config, message="Should include metadata"
        )

        # Test metadata structure
        metadata = config["metadata"]
        self.test_assertions.assert_equals(
            actual=metadata["created_by"],
            expected="flext-meltano",
            message="Should include created_by",
        )
        self.test_assertions.assert_in(
            item="created_at", container=metadata, message="Should include timestamp"
        )

    def test_dbt_config_builder_with_profile(self) -> None:
        """Test DBT config creation with custom profile using flext_tests."""
        # Test with custom profile name (lines 84-86)
        result = FlextMeltanoConfigBuilders().create_dbt_config(
            "analytics_project", "custom_profile"
        )

        self.test_assertions.assert_true(
            condition=result.is_success,
            message="DBT config with profile should succeed",
        )

        config = result.unwrap()
        self.test_assertions.assert_equals(
            actual=config["name"],
            expected="analytics_project",
            message="Project name should match",
        )
        self.test_assertions.assert_equals(
            actual=config["profile"],
            expected="custom_profile",
            message="Profile should use custom value",
        )

        # Test model configuration with project name
        models_config = config["models"]
        self.test_assertions.assert_in(
            item="analytics_project",
            container=models_config,
            message="Should include project-specific model config",
        )

    def test_dbt_config_builder_error_handling(self) -> None:
        """Test DBT config builder error handling using flext_tests."""
        # Test the error handling branch (lines 108-109)
        # This is difficult to trigger directly, but we can test the structure

        # Test with empty project name to exercise safe_string functionality
        result = FlextMeltanoConfigBuilders().create_dbt_config("")

        # Should still succeed due to safe_string providing default only for None
        self.test_assertions.assert_true(
            condition=result.is_success,
            message="Should handle empty project name gracefully",
        )
        config = result.unwrap()
        self.test_assertions.assert_equals(
            actual=config["name"],
            expected="",
            message="Should preserve empty project name",
        )

    # =========================================================================
    # SINGER CONFIG BUILDER TESTING - Lines 130-221 comprehensive coverage
    # =========================================================================

    def test_create_singer_config_generic_extractor(self) -> None:
        """Test generic Singer config creation for extractor using flext_tests."""
        # Test generic config creation for extractor using unified class pattern
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_singer_tap_config(
            tap_name="tap-postgres",
            namespace="postgres_tap",
            pip_url="pipelinewise-tap-postgres",
            executable="tap-postgres",
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )
        self.test_assertions.assert_true(
            condition=result.is_success, message="Generic Singer config should succeed"
        )

        config = result.unwrap()
        self.test_assertions.assert_equals(
            actual=config["name"], expected="tap-postgres", message="Name should match"
        )
        self.test_assertions.assert_equals(
            actual=config["namespace"],
            expected="postgres_tap",
            message="Namespace should match",
        )
        self.test_assertions.assert_equals(
            actual=config["executable"],
            expected="tap-postgres",
            message="Executable should match",
        )
        self.test_assertions.assert_equals(
            actual=config["type"],
            expected=PluginTypes.EXTRACTORS.value,  # SOURCE OF TRUTH
            message="Type should be extractor",
        )

        # Test pip_url handling (lines 155-158)
        self.test_assertions.assert_equals(
            actual=config["pip_url"],
            expected="pipelinewise-tap-postgres",
            message="Should use provided pip_url",
        )

        # Test metadata structure
        metadata = config["metadata"]
        self.test_assertions.assert_equals(
            actual=metadata["created_by"],
            expected="flext-meltano",
            message="Should include created_by",
        )

    def test_create_singer_config_generic_loader(self) -> None:
        """Test generic Singer config creation for loader using flext_tests."""
        # Test generic config creation for loader using unified class pattern
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_singer_target_config(
            target_name="target-jsonl",
            namespace="jsonl_target",
            executable="target-jsonl",
        )

        self.test_assertions.assert_true(
            condition=result.is_success, message="Generic loader config should succeed"
        )

        config = result.unwrap()
        self.test_assertions.assert_equals(
            actual=config["type"],
            expected=PluginTypes.LOADERS.value,
            message="Type should be loader (SOURCE OF TRUTH)",
        )

        # Test type-specific pip_url default (lines 159-166)
        self.test_assertions.assert_equals(
            actual=config["pip_url"],
            expected="target-target-jsonl",
            message="Should use loader-specific pip_url default",
        )

    def test_create_singer_config_generic_no_pip_url_extractor(self) -> None:
        """Test generic Singer config creation without pip_url for extractor using flext_tests."""
        # Test pip_url default generation for extractor using unified class pattern
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_singer_tap_config(
            tap_name="tap-csv"
            # No pip_url provided - should generate default
        )

        self.test_assertions.assert_true(
            condition=result.is_success, message="Should succeed without pip_url"
        )

        config = result.unwrap()
        # Test extractor-specific default (lines 160-165)
        self.test_assertions.assert_equals(
            actual=config["pip_url"],
            expected="pipelinewise-tap-csv",
            message="Should generate pipelinewise prefix for extractor",
        )

    def test_create_singer_tap_config_success(self) -> None:
        """Test Singer tap config creation using flext_tests."""
        # Test tap config creation (lines 183-192)
        result = FlextMeltanoConfigBuilders().create_singer_tap_config(
            "tap-github",
            namespace="github_tap",
            pip_url="pipelinewise-tap-github",
            executable="tap-github",
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )
        self.test_assertions.assert_true(
            condition=result.is_success, message="Tap config creation should succeed"
        )

        config = result.unwrap()
        self.test_assertions.assert_equals(
            actual=config["name"],
            expected="tap-github",
            message="Tap name should match",
        )
        self.test_assertions.assert_equals(
            actual=config["type"],
            expected=PluginTypes.EXTRACTORS.value,  # SOURCE OF TRUTH
            message="Should set type to extractor",
        )
        self.test_assertions.assert_equals(
            actual=config["namespace"],
            expected="github_tap",
            message="Namespace should match",
        )

    def test_create_singer_target_config_success(self) -> None:
        """Test Singer target config creation using flext_tests."""
        # Test target config creation (lines 195-221)
        result = FlextMeltanoConfigBuilders().create_singer_target_config(
            "target-postgres",
            namespace="postgres_target",
            pip_url="target-postgres",
            executable="target-postgres",
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )
        self.test_assertions.assert_true(
            condition=result.is_success, message="Target config creation should succeed"
        )

        config = result.unwrap()
        self.test_assertions.assert_equals(
            actual=config["name"],
            expected="target-postgres",
            message="Target name should match",
        )
        self.test_assertions.assert_equals(
            actual=config["type"],
            expected=PluginTypes.LOADERS.value,  # SOURCE OF TRUTH
            message="Should set type to loader",
        )
        self.test_assertions.assert_equals(
            actual=config["namespace"],
            expected="postgres_target",
            message="Namespace should match",
        )

    def test_singer_config_error_handling(self) -> None:
        """Test Singer config builder error handling using flext_tests."""
        # Test error handling with edge cases using unified class pattern
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_singer_tap_config(
            tap_name=""  # Empty name to test error handling
        )

        # Should still succeed due to safe_string preserving empty values
        self.test_assertions.assert_true(
            condition=result.is_success, message="Should handle empty name gracefully"
        )
        config = result.unwrap()
        self.test_assertions.assert_equals(
            actual=config["name"], expected="", message="Should preserve empty name"
        )

    # =========================================================================
    # COMPREHENSIVE WORKFLOW TESTING - Integration scenarios
    # =========================================================================

    def test_complete_meltano_project_config_workflow(self) -> None:
        """Test complete Meltano project configuration workflow using flext_tests."""
        # Create DBT configuration
        dbt_result = FlextMeltanoConfigBuilders().create_dbt_config(
            "analytics_project", "analytics_profile"
        )
        self.test_assertions.assert_true(
            condition=dbt_result.is_success, message="DBT config should be created"
        )

        # Create tap configuration
        tap_result = FlextMeltanoConfigBuilders().create_singer_tap_config(
            "tap-postgres",
            namespace="postgres_source",
            pip_url="pipelinewise-tap-postgres",
        )
        self.test_assertions.assert_true(
            condition=tap_result.is_success, message="Tap config should be created"
        )

        # Create target configuration
        target_result = FlextMeltanoConfigBuilders().create_singer_target_config(
            "target-snowflake",
            namespace="snowflake_destination",
            pip_url="target-snowflake",
        )
        self.test_assertions.assert_true(
            condition=target_result.is_success,
            message="Target config should be created",
        )

        # Verify all configurations are consistent
        dbt_config = dbt_result.unwrap()
        tap_config = tap_result.unwrap()
        target_config = target_result.unwrap()

        # Check metadata consistency
        for config in [dbt_config, tap_config, target_config]:
            metadata = config["metadata"]
            self.test_assertions.assert_equals(
                actual=metadata["created_by"],
                expected="flext-meltano",
                message="All configs should have consistent created_by",
            )
            self.test_assertions.assert_in(
                item="created_at",
                container=metadata,
                message="All configs should have timestamps",
            )

    def test_configuration_builder_edge_cases(self) -> None:
        """Test configuration builder edge cases using flext_tests."""
        # Test with special characters in names
        special_names = ["tap-test_123", "target.special-name", "dbt-project_v2"]

        for name in special_names:
            # Test DBT config with special name
            dbt_result = FlextMeltanoConfigBuilders().create_dbt_config(name)
            self.test_assertions.assert_true(
                condition=dbt_result.is_success,
                message=f"DBT config should handle special name: {name}",
            )

            # Test Singer tap config with special name
            tap_result = FlextMeltanoConfigBuilders().create_singer_tap_config(name)
            self.test_assertions.assert_true(
                condition=tap_result.is_success,
                message=f"Tap config should handle special name: {name}",
            )

    def test_safe_string_functionality_integration(self) -> None:
        """Test integration with FlextUtilities safe_string functionality using flext_tests."""
        # Test with None-like values that should trigger safe_string defaults
        edge_cases = ["", None, "   ", "\t\n"]

        for edge_case in edge_cases:
            if edge_case is None:
                continue  # Skip None as it would cause type errors

            # Test DBT config with edge case
            dbt_result = FlextMeltanoConfigBuilders().create_dbt_config(edge_case)
            self.test_assertions.assert_true(
                condition=dbt_result.is_success,
                message=f"DBT config should handle edge case: {edge_case!r}",
            )

            # Test Singer config with edge case
            tap_result = FlextMeltanoConfigBuilders().create_singer_tap_config(
                edge_case
            )
            self.test_assertions.assert_true(
                condition=tap_result.is_success,
                message=f"Tap config should handle edge case: {edge_case!r}",
            )

    def test_type_safety_and_constraints(self) -> None:
        """Test type safety and constraints using flext_tests."""
        # Test that all methods return proper FlextResult types
        methods_to_test = [
            lambda: FlextMeltanoConfigBuilders().create_dbt_config("test_project"),
            lambda: FlextMeltanoConfigBuilders().create_singer_tap_config("test_tap"),
            lambda: FlextMeltanoConfigBuilders().create_singer_target_config(
                "test_target"
            ),
        ]

        for method in methods_to_test:
            result = method()
            self.test_assertions.assert_true(
                condition=isinstance(result, FlextResult),
                message=f"Method {method} should return FlextResult",
            )

            if result.is_success:
                config = result.unwrap()
                self.test_assertions.assert_true(
                    condition=isinstance(config, dict),
                    message="Config should be a dictionary",
                )
                self.test_assertions.assert_in(
                    item="metadata",
                    container=config,
                    message="All configs should include metadata",
                )

    def test_advanced_plugin_config_scenarios(self) -> None:
        """Test advanced plugin configuration scenarios using flext_tests."""
        # Test loader type with complex configuration using direct method call
        builder = FlextMeltanoConfigBuilders()
        result = builder._create_singer_config_generic(
            plugin_name="target-bigquery",
            plugin_type=PluginTypes.LOADERS.value,  # SOURCE OF TRUTH
            namespace="bigquery_warehouse",
            executable="target-bigquery",
        )

        self.test_assertions.assert_true(
            condition=result.is_success, message="Complex loader config should succeed"
        )
        config = result.unwrap()

        # Test that loader type generates correct pip_url default (lines 163-166)
        expected_pip_url = "target-target-bigquery"
        self.test_assertions.assert_equals(
            actual=config["pip_url"],
            expected=expected_pip_url,
            message="Loader should use target prefix for pip_url default",
        )

        # Test safe namespace handling
        self.test_assertions.assert_equals(
            actual=config["namespace"],
            expected="bigquery_warehouse",
            message="Should preserve complex namespace",
        )
