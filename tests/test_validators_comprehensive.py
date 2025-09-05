"""Comprehensive tests for FlextMeltanoValidators using flext_tests.

Tests all validator functionality with real validation scenarios,
no mocks, using flext_tests for improved assertions and test builders.
"""

import pytest
from flext_tests import FlextMatchers

from flext_meltano.validators import FlextMeltanoValidators


class TestFlextMeltanoValidatorsComprehensive:
    """Comprehensive tests for FlextMeltanoValidators with 100% coverage."""

    def test_validate_plugin_config_valid(self) -> None:
        """Test plugin config validation with valid configuration."""
        config = {
            "name": "tap-csv",
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }

        result = FlextMeltanoValidators.validate_plugin_config(config)
        FlextMatchers.assert_result_success(result, True)

    def test_validate_plugin_config_missing_fields(self) -> None:
        """Test plugin config validation with missing required fields."""
        config = {"name": "tap-csv"}  # Missing required fields

        result = FlextMeltanoValidators.validate_plugin_config(config)
        FlextMatchers.assert_result_failure(result)

    def test_validate_plugin_config_empty_fields(self) -> None:
        """Test plugin config validation with empty fields."""
        config = {
            "name": "",  # Empty name should fail
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }

        result = FlextMeltanoValidators.validate_plugin_config(config)
        FlextMatchers.assert_result_failure(result)

    def test_validate_plugin_config_invalid_types(self) -> None:
        """Test plugin config validation with invalid types."""
        config = {
            "name": 123,  # Should be string
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }

        result = FlextMeltanoValidators.validate_plugin_config(config)
        FlextMatchers.assert_result_failure(result)

    def test_validate_plugin_config_non_dict(self) -> None:
        """Test plugin config validation with non-dict input."""
        result = FlextMeltanoValidators.validate_plugin_config("not a dict")
        FlextMatchers.assert_result_failure(result)

    def test_validate_plugin_config_none(self) -> None:
        """Test plugin config validation with None input."""
        result = FlextMeltanoValidators.validate_plugin_config(None)
        FlextMatchers.assert_result_failure(result)

    def test_validate_meltano_config_valid(self) -> None:
        """Test Meltano config validation with valid configuration."""
        config = {"version": 1, "project_id": "test-project"}

        result = FlextMeltanoValidators.validate_meltano_config(config)
        FlextMatchers.assert_result_success(result, True)

    def test_validate_meltano_config_missing_version(self) -> None:
        """Test Meltano config validation with missing version."""
        config = {"project_id": "test-project"}  # Missing version

        result = FlextMeltanoValidators.validate_meltano_config(config)
        FlextMatchers.assert_result_failure(result)

    def test_validate_meltano_config_invalid_version(self) -> None:
        """Test Meltano config validation with invalid version."""
        config = {
            "version": 2,  # Invalid version (must be 1)
            "project_id": "test-project",
        }

        result = FlextMeltanoValidators.validate_meltano_config(config)
        FlextMatchers.assert_result_failure(result)

    def test_validate_meltano_config_empty_project_id(self) -> None:
        """Test Meltano config validation with empty project_id."""
        config = {
            "version": 1,
            "project_id": "",  # Empty project_id should fail
        }

        result = FlextMeltanoValidators.validate_meltano_config(config)
        FlextMatchers.assert_result_failure(result)

    def test_validate_dbt_config_valid(self) -> None:
        """Test DBT config validation with valid configuration."""
        dbt_config = {"name": "analytics", "version": "1.0.0"}

        result = FlextMeltanoValidators.validate_dbt_config(dbt_config)
        FlextMatchers.assert_result_success(result, True)

    def test_validate_dbt_config_missing_required(self) -> None:
        """Test DBT config validation with missing required fields."""
        dbt_config = {"name": "analytics"}  # Missing version

        result = FlextMeltanoValidators.validate_dbt_config(dbt_config)
        FlextMatchers.assert_result_failure(result)

    @pytest.mark.parametrize(
        "invalid_config", [None, "not a dict", [], 123, {"invalid": "structure"}]
    )
    def test_validate_plugin_config_parametrized_invalid(
        self, invalid_config: object
    ) -> None:
        """Test plugin config validation with various invalid inputs."""
        result = FlextMeltanoValidators.validate_plugin_config(invalid_config)
        FlextMatchers.assert_result_failure(result)

    def test_complex_validation_scenario(self) -> None:
        """Test complex validation scenario combining multiple validators."""
        # Test combining multiple validations
        meltano_config = {"version": 1, "project_id": "integration-test"}

        dbt_config = {"name": "analytics", "version": "1.0.0"}

        tap_config = {
            "name": "tap-csv",
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }

        target_config = {
            "name": "target-postgres",
            "namespace": "target_postgres",
            "pip_url": "pipelinewise-target-postgres",
            "executable": "target-postgres",
        }

        # Validate all configs
        meltano_result = FlextMeltanoValidators.validate_meltano_config(meltano_config)
        dbt_result = FlextMeltanoValidators.validate_dbt_config(dbt_config)
        tap_result = FlextMeltanoValidators.validate_plugin_config(tap_config)
        target_result = FlextMeltanoValidators.validate_plugin_config(target_config)

        # All should pass
        FlextMatchers.assert_result_success(meltano_result, True)
        FlextMatchers.assert_result_success(dbt_result, True)
        FlextMatchers.assert_result_success(tap_result, True)
        FlextMatchers.assert_result_success(target_result, True)

    def test_validator_inheritance_from_flext_utilities(self) -> None:
        """Test that FlextMeltanoValidators properly inherits from FlextUtilities."""
        # Should have access to parent class methods
        assert hasattr(FlextMeltanoValidators, "safe_json_stringify")
        assert hasattr(FlextMeltanoValidators, "TextProcessor")

        # Test that we can use inherited functionality
        test_data = {"test": "data"}
        json_result = FlextMeltanoValidators.safe_json_stringify(test_data)
        assert '"test": "data"' in json_result
