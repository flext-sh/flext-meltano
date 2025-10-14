"""Comprehensive tests for FlextMeltanoValidators using flext_tests.

Tests all validator functionality with real validation scenarios,
no mocks, using flext_tests for improved assertions and test builders.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from typing import cast

import pytest
from flext_core import FlextCore
from flext_tests.matchers import FlextTestsMatchers

from flext_meltano import FlextMeltanoValidators


class TestFlextMeltanoValidatorsComprehensive:
    """Comprehensive tests for FlextMeltanoValidators with 100% coverage."""

    def test_validate_plugin_config_valid(self) -> None:
        config: FlextCore.Types.Dict = {
            "name": "tap-csv",
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }

        result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextCore.Types.JsonValue", config)
        )
        FlextTestsMatchers.assert_result_success(result, True)

    def test_validate_plugin_config_missing_fields(self) -> None:
        config: FlextCore.Types.Dict = {"name": "tap-csv"}

        result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextCore.Types.JsonValue", config)
        )
        FlextTestsMatchers.assert_result_failure(
            cast("FlextCore.Result[object]", result)
        )

    def test_validate_plugin_config_empty_fields(self) -> None:
        config: FlextCore.Types.Dict = {
            "name": "",
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }

        result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextCore.Types.JsonValue", config)
        )
        FlextTestsMatchers.assert_result_failure(
            cast("FlextCore.Result[object]", result)
        )

    def test_validate_plugin_config_invalid_types(self) -> None:
        config: FlextCore.Types.Dict = {
            "name": 123,
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }

        result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextCore.Types.JsonValue", config)
        )
        FlextTestsMatchers.assert_result_failure(
            cast("FlextCore.Result[object]", result)
        )

    def test_validate_plugin_config_non_dict(self) -> None:
        """Test plugin config validation with non-dict input."""
        result = FlextMeltanoValidators.validate_plugin_config("not a dict")
        FlextTestsMatchers.assert_result_failure(
            cast("FlextCore.Result[object]", result)
        )

    def test_validate_plugin_config_none(self) -> None:
        """Test plugin config validation with None input."""
        result = FlextMeltanoValidators.validate_plugin_config(None)
        FlextTestsMatchers.assert_result_failure(
            cast("FlextCore.Result[object]", result)
        )

    def test_validate_meltano_config_valid(self) -> None:
        config: FlextCore.Types.Dict = {"version": 1, "project_id": "test-project"}

        result = FlextMeltanoValidators.validate_meltano_project_business_rules(
            cast("FlextCore.Types.JsonValue", config)
        )
        FlextTestsMatchers.assert_result_success(result, True)

    def test_validate_meltano_config_missing_version(self) -> None:
        config: FlextCore.Types.Dict = {"project_id": "test-project"}

        result = FlextMeltanoValidators.validate_meltano_project_business_rules(
            cast("FlextCore.Types.JsonValue", config)
        )
        FlextTestsMatchers.assert_result_failure(
            cast("FlextCore.Result[object]", result)
        )

    def test_validate_meltano_config_invalid_version(self) -> None:
        config: FlextCore.Types.Dict = {
            "version": 2,
            "project_id": "test-project",
        }

        result = FlextMeltanoValidators.validate_meltano_project_business_rules(
            cast("FlextCore.Types.JsonValue", config)
        )
        FlextTestsMatchers.assert_result_failure(
            cast("FlextCore.Result[object]", result)
        )

    def test_validate_meltano_config_empty_project_id(self) -> None:
        config: FlextCore.Types.Dict = {
            "version": 1,
            "project_id": "",
        }

        result = FlextMeltanoValidators.validate_meltano_project_business_rules(
            cast("FlextCore.Types.JsonValue", config)
        )
        FlextTestsMatchers.assert_result_failure(
            cast("FlextCore.Result[object]", result)
        )

    def test_validate_dbt_config_valid(self) -> None:
        dbt_config: FlextCore.Types.Dict = {
            "name": "analytics",
            "version": "1.0.0",
            "profile": "analytics_profile",
        }

        result = FlextMeltanoValidators.validate_dbt_business_rules(
            cast("FlextCore.Types.JsonValue", dbt_config)
        )
        FlextTestsMatchers.assert_result_success(result, True)

    def test_validate_dbt_config_missing_required(self) -> None:
        dbt_config: FlextCore.Types.Dict = {"name": "analytics"}

        result = FlextMeltanoValidators.validate_dbt_business_rules(
            cast("FlextCore.Types.JsonValue", dbt_config)
        )
        FlextTestsMatchers.assert_result_failure(
            cast("FlextCore.Result[object]", result)
        )

    @pytest.mark.parametrize(
        "invalid_config",
        [None, "not a dict", [], 123, {"invalid": "structure"}],
    )
    def test_validate_plugin_config_parametrized_invalid(
        self,
        invalid_config: object,
    ) -> None:
        result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextCore.Types.JsonValue", invalid_config)
        )
        FlextTestsMatchers.assert_result_failure(
            cast("FlextCore.Result[object]", result)
        )

    def test_complex_validation_scenario(self) -> None:
        meltano_config: FlextCore.Types.Dict = {
            "version": 1,
            "project_id": "integration-test",
        }

        dbt_config: FlextCore.Types.Dict = {
            "name": "analytics",
            "version": "1.0.0",
            "profile": "analytics_profile",
        }

        tap_config: FlextCore.Types.Dict = {
            "name": "tap-csv",
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }

        target_config: FlextCore.Types.Dict = {
            "name": "target-postgres",
            "namespace": "target_postgres",
            "pip_url": "pipelinewise-target-postgres",
            "executable": "target-postgres",
        }

        meltano_result = FlextMeltanoValidators.validate_meltano_project_business_rules(
            cast("FlextCore.Types.JsonValue", meltano_config)
        )
        dbt_result = FlextMeltanoValidators.validate_dbt_business_rules(
            cast("FlextCore.Types.JsonValue", dbt_config)
        )
        tap_result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextCore.Types.JsonValue", tap_config)
        )
        target_result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextCore.Types.JsonValue", target_config)
        )

        FlextTestsMatchers.assert_result_success(meltano_result, True)
        FlextTestsMatchers.assert_result_success(dbt_result, True)
        FlextTestsMatchers.assert_result_success(tap_result, True)
        FlextTestsMatchers.assert_result_success(target_result, True)

    def test_validator_architecture_compliance(self) -> None:
        assert hasattr(FlextMeltanoValidators, "validate_plugin_config")
        assert hasattr(
            FlextMeltanoValidators, "validate_meltano_project_business_rules"
        )
        assert hasattr(FlextMeltanoValidators, "validate_dbt_business_rules")

        assert not hasattr(FlextMeltanoValidators, "safe_json_stringify")
        assert not hasattr(FlextMeltanoValidators, "TextProcessor")

        config: FlextCore.Types.Dict = {
            "name": "test-plugin",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextCore.Types.JsonValue", config)
        )
        assert result.is_success

    def test_validate_plugin_name_empty(self) -> None:
        config: FlextCore.Types.Dict = {
            "name": "",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextCore.Types.JsonValue", config)
        )
        assert not result.is_success
        assert result.error is not None
        assert (
            result.error is not None and "Plugin name cannot be empty" in result.error
        )

    def test_validate_plugin_name_whitespace(self) -> None:
        config: FlextCore.Types.Dict = {
            "name": "   ",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextCore.Types.JsonValue", config)
        )
        assert not result.is_success
        assert result.error is not None
        assert (
            result.error is not None and "Plugin name cannot be empty" in result.error
        )

    def test_validate_target_plugin_name_too_short(self) -> None:
        config: FlextCore.Types.Dict = {
            "name": "target-",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextCore.Types.JsonValue", config)
        )
        assert not result.is_success
        assert result.error is not None
        assert (
            result.error is not None
            and "Target plugin names must be at least 8 characters" in result.error
        )

    def test_validate_tap_plugin_name_too_short(self) -> None:
        config: FlextCore.Types.Dict = {
            "name": "tap-",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextCore.Types.JsonValue", config)
        )
        assert not result.is_success
        assert result.error is not None
        assert (
            result.error is not None
            and "Tap plugin names must be at least 5 characters" in result.error
        )

    def test_validate_target_plugin_name_valid(self) -> None:
        config: FlextCore.Types.Dict = {
            "name": "target-postgres",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextCore.Types.JsonValue", config)
        )
        assert result.is_success

    def test_validate_tap_plugin_name_valid(self) -> None:
        config: FlextCore.Types.Dict = {
            "name": "tap-csv",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextCore.Types.JsonValue", config)
        )
        assert result.is_success
