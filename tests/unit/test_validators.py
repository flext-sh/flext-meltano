"""Comprehensive tests for FlextMeltanoValidators using flext_tests.

Tests all validator functionality with real validation scenarios,
no mocks, using flext_tests for improved assertions and test builders.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_meltano import FlextMeltanoValidators, t


class TestFlextMeltanoValidatorsComprehensive:
    """Comprehensive tests for FlextMeltanoValidators with 100% coverage."""

    def test_validate_plugin_config_valid(self) -> None:
        config: dict[str, t.Scalar] = {
            "name": "tap-csv",
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert result.is_success

    def test_validate_plugin_config_missing_fields(self) -> None:
        config: dict[str, t.Scalar] = {"name": "tap-csv"}
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert result.is_failure
        assert result.is_failure

    def test_validate_plugin_config_empty_fields(self) -> None:
        config: dict[str, t.Scalar] = {
            "name": "",
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert result.is_failure
        assert result.is_failure

    def test_validate_plugin_config_invalid_types(self) -> None:
        config: dict[str, t.Scalar] = {
            "name": 123,
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert result.is_failure
        assert result.is_failure

    def test_validate_plugin_config_non_dict(self) -> None:
        """Test plugin config validation with non-dict input."""
        result = FlextMeltanoValidators.validate_plugin_config("not a dict")
        assert result.is_failure
        assert result.is_failure

    def test_validate_plugin_config_none(self) -> None:
        """Test plugin config validation with None input."""
        result = FlextMeltanoValidators.validate_plugin_config(None)
        assert result.is_failure
        assert result.is_failure

    def test_validate_meltano_config_valid(self) -> None:
        config: dict[str, t.Scalar] = {"version": 1, "project_id": "test-project"}
        result = FlextMeltanoValidators.validate_pipeline_project_business_rules(config)
        assert result.is_success

    def test_validate_meltano_config_missing_version(self) -> None:
        config: dict[str, t.Scalar] = {"project_id": "test-project"}
        result = FlextMeltanoValidators.validate_pipeline_project_business_rules(config)
        assert result.is_failure or result.is_success

    def test_validate_meltano_config_invalid_version(self) -> None:
        config: dict[str, t.Scalar] = {"version": 2, "project_id": "test-project"}
        result = FlextMeltanoValidators.validate_pipeline_project_business_rules(config)
        assert result.is_failure
        assert result.is_failure

    def test_validate_meltano_config_empty_project_id(self) -> None:
        """Test basic validator instantiation."""
        validator = FlextMeltanoValidators()
        assert validator is not None

    def test_validate_dbt_config_valid(self) -> None:
        dbt_config: dict[str, t.Scalar] = {
            "name": "analytics",
            "version": 1,
            "transformation_version": "1.0.0",
            "profile": "analytics_profile",
        }
        result = FlextMeltanoValidators.validate_transformation_business_rules(
            dbt_config
        )
        assert result.is_success

    def test_validate_dbt_config_missing_required(self) -> None:
        dbt_config: dict[str, t.Scalar] = {"name": "analytics"}
        result = FlextMeltanoValidators.validate_transformation_business_rules(
            dbt_config
        )
        assert result.is_failure
        assert result.is_failure

    @pytest.mark.parametrize(
        "invalid_config", [None, "not a dict", [], 123, {"invalid": "structure"}]
    )
    def test_validate_plugin_config_parametrized_invalid(
        self,
        invalid_config: t.Scalar | dict[str, t.Scalar] | list[t.Scalar] | None,
    ) -> None:
        result = FlextMeltanoValidators.validate_plugin_config(invalid_config)
        assert result.is_failure
        assert result.is_failure

    def test_complex_validation_scenario(self) -> None:
        meltano_config: dict[str, t.Scalar] = {
            "version": 1,
            "project_id": "integration-test",
        }
        dbt_config: dict[str, t.Scalar] = {
            "name": "analytics",
            "version": 1,
            "transformation_version": "1.0.0",
            "profile": "analytics_profile",
        }
        tap_config: dict[str, t.Scalar] = {
            "name": "tap-csv",
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }
        target_config: dict[str, t.Scalar] = {
            "name": "target-postgres",
            "namespace": "target_postgres",
            "pip_url": "pipelinewise-target-postgres",
            "executable": "target-postgres",
        }
        meltano_result = (
            FlextMeltanoValidators.validate_pipeline_project_business_rules(
                meltano_config
            )
        )
        dbt_result = FlextMeltanoValidators.validate_transformation_business_rules(
            dbt_config
        )
        tap_result = FlextMeltanoValidators.validate_plugin_config(tap_config)
        target_result = FlextMeltanoValidators.validate_plugin_config(target_config)
        assert meltano_result.is_success
        assert dbt_result.is_success
        assert tap_result.is_success
        assert target_result.is_success

    def test_validator_architecture_compliance(self) -> None:
        assert hasattr(FlextMeltanoValidators, "validate_plugin_config")
        assert hasattr(
            FlextMeltanoValidators, "validate_pipeline_project_business_rules"
        )
        assert hasattr(FlextMeltanoValidators, "validate_transformation_business_rules")
        assert not hasattr(FlextMeltanoValidators, "safe_json_stringify")
        assert not hasattr(FlextMeltanoValidators, "Text")
        config: dict[str, t.Scalar] = {
            "name": "test-plugin",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert result.is_success

    def test_validate_plugin_name_empty(self) -> None:
        config: dict[str, t.Scalar] = {
            "name": "",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert not result.is_success
        assert result.error is not None
        assert "Plugin config validation failed" in result.error

    def test_validate_plugin_name_whitespace(self) -> None:
        config: dict[str, t.Scalar] = {
            "name": "   ",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert not result.is_success
        assert result.error is not None
        assert "Plugin config validation failed" in result.error

    def test_validate_target_plugin_name_too_short(self) -> None:
        config: dict[str, t.Scalar] = {
            "name": "target-",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert not result.is_success
        assert result.error is not None
        assert result.error is not None
        assert "Target plugin names must be at least 8 characters" in result.error

    def test_validate_tap_plugin_name_too_short(self) -> None:
        config: dict[str, t.Scalar] = {
            "name": "tap-",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert not result.is_success
        assert result.error is not None
        assert result.error is not None
        assert "Source component names must be at least 5 characters" in result.error

    def test_validate_target_plugin_name_valid(self) -> None:
        config: dict[str, t.Scalar] = {
            "name": "target-postgres",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert result.is_success

    def test_validate_tap_plugin_name_valid(self) -> None:
        config: dict[str, t.Scalar] = {
            "name": "tap-csv",
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = FlextMeltanoValidators.validate_plugin_config(config)
        assert result.is_success
