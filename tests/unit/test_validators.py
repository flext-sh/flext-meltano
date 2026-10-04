"""Behavioral tests for the Meltano validators public contract.

Exercises the observable ``r[bool]`` outcomes of the validator facade
(``validate_plugin_config``, ``validate_pipeline_project_business_rules``,
``validate_transformation_business_rules``) through their public API only:
success/failure state, unwrapped values, error messages and combinators.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from flext_tests import tm

from flext_meltano import meltano

if TYPE_CHECKING:
    from tests import t


class TestsFlextMeltanoValidators:
    """Contract tests for the Meltano business-rule validators."""

    # ------------------------------------------------------------------
    # Plugin configuration
    # ------------------------------------------------------------------

    @staticmethod
    def test_valid_plugin_config_succeeds_with_true_value() -> None:
        """Test valid plugin config succeeds with true value."""
        settings: t.ScalarMapping = {
            "name": "tap-csv",
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }
        result = meltano.validate_plugin_config(settings)
        tm.ok(result)
        tm.that(result.value, eq=True)
        tm.that(result.unwrap(), eq=True)

    @staticmethod
    def test_plugin_config_missing_required_fields_fails() -> None:
        """Test plugin config missing required fields fails."""
        settings: t.ScalarMapping = {"name": "tap-csv"}
        result = meltano.validate_plugin_config(settings)
        tm.fail(result)
        tm.that(result.error, has="Plugin settings validation failed")

    @staticmethod
    @pytest.mark.parametrize(
        ("name", "expected_fragment"),
        [
            ("", "Plugin settings validation failed"),
            ("   ", "Plugin settings validation failed"),
            ("target-", "Target plugin names must be at least 8 characters"),
            ("tap-", "Source component names must be at least 5 characters"),
        ],
    )
    def test_plugin_name_business_rules_reject_invalid_names(
        name: str,
        expected_fragment: str,
    ) -> None:
        """Test plugin name business rules reject invalid names."""
        settings: t.ScalarMapping = {
            "name": name,
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = meltano.validate_plugin_config(settings)
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has=expected_fragment)

    @staticmethod
    @pytest.mark.parametrize("name", ["tap-csv", "target-postgres"])
    def test_plugin_name_business_rules_accept_valid_names(name: str) -> None:
        """Test plugin name business rules accept valid names."""
        settings: t.ScalarMapping = {
            "name": name,
            "namespace": "test_ns",
            "pip_url": "test",
            "executable": "test",
        }
        result = meltano.validate_plugin_config(settings)
        tm.ok(result)
        tm.that(result.value, eq=True)

    @staticmethod
    @pytest.mark.parametrize(
        "invalid_config",
        [
            {},
            {"invalid": "structure"},
            {"name": "tap-csv", "namespace": "tap_csv"},
            {"namespace": "tap_csv", "pip_url": "u", "executable": "e"},
        ],
    )
    def test_plugin_config_rejects_mappings_missing_required_fields(
        invalid_config: t.ScalarMapping,
    ) -> None:
        """Test plugin config rejects mappings missing required fields."""
        result = meltano.validate_plugin_config(invalid_config)
        tm.fail(result)
        tm.that(result.error, has="Plugin settings validation failed")

    @staticmethod
    def test_plugin_config_failure_preserves_error_through_map() -> None:
        """Test plugin config failure preserves error through map."""
        settings: t.ScalarMapping = {"name": "tap-csv"}
        result = meltano.validate_plugin_config(settings)
        mapped = result.map(lambda value: value)
        tm.fail(mapped)
        tm.that(mapped.error, eq=result.error)

    # ------------------------------------------------------------------
    # Pipeline project rules
    # ------------------------------------------------------------------

    @staticmethod
    def test_valid_pipeline_project_succeeds() -> None:
        """Test valid pipeline project succeeds."""
        settings: t.ScalarMapping = {"schema_version": 1, "project_id": "test-project"}
        result = meltano.validate_pipeline_project_business_rules(settings)
        tm.ok(result)
        tm.that(result.value, eq=True)

    @staticmethod
    def test_pipeline_project_defaults_schema_version_when_omitted() -> None:
        """Test pipeline project defaults schema version when omitted."""
        settings: t.ScalarMapping = {"project_id": "test-project"}
        result = meltano.validate_pipeline_project_business_rules(settings)
        tm.ok(result)
        tm.that(result.value, eq=True)

    @staticmethod
    def test_pipeline_project_missing_project_id_fails() -> None:
        """Test pipeline project missing project id fails."""
        settings: t.ScalarMapping = {"schema_version": 1}
        result = meltano.validate_pipeline_project_business_rules(settings)
        tm.fail(result)
        tm.that(result.error, has="Project validation failed")

    @staticmethod
    def test_pipeline_project_unsupported_schema_version_fails() -> None:
        """Test pipeline project unsupported schema version fails."""
        settings: t.ScalarMapping = {"schema_version": 2, "project_id": "test-project"}
        result = meltano.validate_pipeline_project_business_rules(settings)
        tm.fail(result)
        tm.that(result.error, has="Project validation failed")

    # ------------------------------------------------------------------
    # Transformation project rules
    # ------------------------------------------------------------------

    @staticmethod
    def test_valid_transformation_config_succeeds() -> None:
        """Test valid transformation config succeeds."""
        dbt_config: t.ScalarMapping = {
            "name": "analytics",
            "transformation_version": "1.0.0",
            "profile": "analytics_profile",
        }
        result = meltano.validate_transformation_business_rules(dbt_config)
        tm.ok(result)
        tm.that(result.value, eq=True)

    @staticmethod
    def test_transformation_config_missing_required_fails() -> None:
        """Test transformation config missing required fails."""
        dbt_config: t.ScalarMapping = {"name": "analytics"}
        result = meltano.validate_transformation_business_rules(dbt_config)
        tm.fail(result)
        tm.that(result.error, has="Transformation validation failed")

    # ------------------------------------------------------------------
    # Invariants
    # ------------------------------------------------------------------

    @staticmethod
    def test_validation_is_idempotent_for_same_input() -> None:
        """Test validation is idempotent for same input."""
        settings: t.ScalarMapping = {
            "name": "tap-csv",
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }
        first = meltano.validate_plugin_config(settings)
        second = meltano.validate_plugin_config(settings)
        tm.that(first.success, eq=second.success)
        tm.that(first.value, eq=second.value)

    @staticmethod
    def test_independent_validators_agree_on_full_pipeline() -> None:
        """Test independent validators agree on full pipeline."""
        meltano_config: t.ScalarMapping = {
            "schema_version": 1,
            "project_id": "integration-test",
        }
        dbt_config: t.ScalarMapping = {
            "name": "analytics",
            "transformation_version": "1.0.0",
            "profile": "analytics_profile",
        }
        tap_config: t.ScalarMapping = {
            "name": "tap-csv",
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }
        target_config: t.ScalarMapping = {
            "name": "target-postgres",
            "namespace": "target_postgres",
            "pip_url": "pipelinewise-target-postgres",
            "executable": "target-postgres",
        }
        tm.ok(meltano.validate_pipeline_project_business_rules(meltano_config))
        tm.ok(meltano.validate_transformation_business_rules(dbt_config))
        tm.ok(meltano.validate_plugin_config(tap_config))
        tm.ok(meltano.validate_plugin_config(target_config))
