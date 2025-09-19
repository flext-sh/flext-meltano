"""Comprehensive tests for FlextMeltanoValidators using flext_tests.

Tests all validator functionality with real validation scenarios,
no mocks, using flext_tests for improved assertions and test builders.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from typing import cast

import pytest
from flext_tests import FlextTestsMatchers

from flext_core import FlextResult
from flext_meltano.validators import FlextMeltanoValidators


class TestFlextMeltanoValidatorsComprehensive:
    """Comprehensive tests for FlextMeltanoValidators with 100% coverage."""

    def test_validate_plugin_config_valid(self) -> None:
        """Test plugin config validation with valid configuration."""
        config: dict[str, object] = {
            "name": "tap-csv",
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }

        result = FlextMeltanoValidators.validate_plugin_config(config)
        FlextTestsMatchers.assert_result_success(result, True)

    def test_validate_plugin_config_missing_fields(self) -> None:
        """Test plugin config validation with missing required fields."""
        config: dict[str, object] = {"name": "tap-csv"}  # Missing required fields

        result = FlextMeltanoValidators.validate_plugin_config(config)
        FlextTestsMatchers.assert_result_failure(cast("FlextResult[object]", result))

    def test_validate_plugin_config_empty_fields(self) -> None:
        """Test plugin config validation with empty fields."""
        config: dict[str, object] = {
            "name": "",  # Empty name should fail
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }

        result = FlextMeltanoValidators.validate_plugin_config(config)
        FlextTestsMatchers.assert_result_failure(cast("FlextResult[object]", result))

    def test_validate_plugin_config_invalid_types(self) -> None:
        """Test plugin config validation with invalid types."""
        config: dict[str, object] = {
            "name": 123,  # Should be string
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }

        result = FlextMeltanoValidators.validate_plugin_config(config)
        FlextTestsMatchers.assert_result_failure(cast("FlextResult[object]", result))

    def test_validate_plugin_config_non_dict(self) -> None:
        """Test plugin config validation with non-dict input."""
        result = FlextMeltanoValidators.validate_plugin_config("not a dict")
        FlextTestsMatchers.assert_result_failure(cast("FlextResult[object]", result))

    def test_validate_plugin_config_none(self) -> None:
        """Test plugin config validation with None input."""
        result = FlextMeltanoValidators.validate_plugin_config(None)
        FlextTestsMatchers.assert_result_failure(cast("FlextResult[object]", result))

    def test_validate_meltano_config_valid(self) -> None:
        """Test Meltano config validation with valid configuration."""
        config: dict[str, object] = {"version": 1, "project_id": "test-project"}

        result = FlextMeltanoValidators.validate_meltano_config(config)
        FlextTestsMatchers.assert_result_success(result, True)

    def test_validate_meltano_config_missing_version(self) -> None:
        """Test Meltano config validation with missing version."""
        config: dict[str, object] = {"project_id": "test-project"}  # Missing version

        result = FlextMeltanoValidators.validate_meltano_config(config)
        FlextTestsMatchers.assert_result_failure(cast("FlextResult[object]", result))

    def test_validate_meltano_config_invalid_version(self) -> None:
        """Test Meltano config validation with invalid version."""
        config: dict[str, object] = {
            "version": 2,  # Invalid version (must be 1)
            "project_id": "test-project",
        }

        result = FlextMeltanoValidators.validate_meltano_config(config)
        FlextTestsMatchers.assert_result_failure(cast("FlextResult[object]", result))

    def test_validate_meltano_config_empty_project_id(self) -> None:
        """Test Meltano config validation with empty project_id."""
        config: dict[str, object] = {
            "version": 1,
            "project_id": "",  # Empty project_id should fail
        }

        result = FlextMeltanoValidators.validate_meltano_config(config)
        FlextTestsMatchers.assert_result_failure(cast("FlextResult[object]", result))

    def test_validate_dbt_config_valid(self) -> None:
        """Test DBT config validation with valid configuration."""
        dbt_config = {"name": "analytics", "version": "1.0.0"}

        result = FlextMeltanoValidators.validate_dbt_config(dbt_config)
        FlextTestsMatchers.assert_result_success(result, True)

    def test_validate_dbt_config_missing_required(self) -> None:
        """Test DBT config validation with missing required fields."""
        dbt_config = {"name": "analytics"}  # Missing version

        result = FlextMeltanoValidators.validate_dbt_config(dbt_config)
        FlextTestsMatchers.assert_result_failure(cast("FlextResult[object]", result))

    @pytest.mark.parametrize(
        "invalid_config", [None, "not a dict", [], 123, {"invalid": "structure"}],
    )
    def test_validate_plugin_config_parametrized_invalid(
        self, invalid_config: object,
    ) -> None:
        """Test plugin config validation with various invalid inputs."""
        result = FlextMeltanoValidators.validate_plugin_config(invalid_config)
        FlextTestsMatchers.assert_result_failure(cast("FlextResult[object]", result))

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
        FlextTestsMatchers.assert_result_success(meltano_result, True)
        FlextTestsMatchers.assert_result_success(dbt_result, True)
        FlextTestsMatchers.assert_result_success(tap_result, True)
        FlextTestsMatchers.assert_result_success(target_result, True)

    def test_validator_architecture_compliance(self) -> None:
        """Test that FlextMeltanoValidators follows SOLID principles without inheritance violations."""
        # FlextMeltanoValidators should NOT inherit from FlextUtilities (SOLID violation)
        # Instead, it should have its own validation methods without inheritance

        # Verify it has the core Meltano-specific validation methods
        assert hasattr(FlextMeltanoValidators, "validate_plugin_config")
        assert hasattr(FlextMeltanoValidators, "validate_meltano_config")
        assert hasattr(FlextMeltanoValidators, "validate_dbt_config")

        # Verify it does NOT have utility methods (should be separate concerns)
        assert not hasattr(FlextMeltanoValidators, "safe_json_stringify")
        assert not hasattr(FlextMeltanoValidators, "TextProcessor")

        # Test core validation functionality works independently
        config: dict[str, object] = {
            "name": "test-plugin",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert result.success

    def test_validate_plugin_name_empty(self) -> None:
        """Test plugin name validation with empty name."""
        config: dict[str, object] = {
            "name": "",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert not result.success
        assert result.error is not None
        assert "String should have at least 1 character" in result.error

    def test_validate_plugin_name_whitespace(self) -> None:
        """Test plugin name validation with whitespace only."""
        config: dict[str, object] = {
            "name": "   ",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert not result.success
        assert result.error is not None
        assert "Plugin name cannot be empty" in result.error

    def test_validate_target_plugin_name_too_short(self) -> None:
        """Test target plugin name validation with too short name."""
        config: dict[str, object] = {
            "name": "target-",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert not result.success
        assert result.error is not None
        assert "Target plugin names must be at least 8 characters" in result.error

    def test_validate_tap_plugin_name_too_short(self) -> None:
        """Test tap plugin name validation with too short name."""
        config: dict[str, object] = {
            "name": "tap-",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert not result.success
        assert result.error is not None
        assert "Tap plugin names must be at least 5 characters" in result.error

    def test_validate_target_plugin_name_valid(self) -> None:
        """Test target plugin name validation with valid name."""
        config: dict[str, object] = {
            "name": "target-postgres",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert result.success

    def test_validate_tap_plugin_name_valid(self) -> None:
        """Test tap plugin name validation with valid name."""
        config: dict[str, object] = {
            "name": "tap-csv",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert result.success
