"""Comprehensive tests for CLI to Model integration.

Tests direct CLI model conversion integration with Meltano models:
- Dict to Pydantic model conversion
- Validation error propagation
- Round-trip conversion
- r railway pattern throughout

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from tests import m, t, u


class TestFlextMeltanoCliModelConversion:
    """Behavioral tests for Meltano CLI model conversion."""

    def test_tap_run_params_minimal(self) -> None:
        cli_args: t.Cli.JsonMapping = {
            "tap_name": "tap-postgres",
            "discover": False,
        }
        result = u.Cli.cli_args_to_model(m.Meltano.TapRunParams, cli_args)
        tm.ok(result)
        model = result.value
        tm.that(model.tap_name, eq="tap-postgres")
        tm.that(model.config_file, none=True)
        tm.that(model.discover is False, eq=True)

    def test_tap_run_params_with_config(self) -> None:
        cli_args: t.Cli.JsonMapping = {
            "tap_name": "tap-postgres",
            "config_file": "/path/to/config.json",
            "discover": False,
        }
        result = u.Cli.cli_args_to_model(m.Meltano.TapRunParams, cli_args)
        tm.ok(result)
        model = result.value
        tm.that(model.config_file, eq="/path/to/config.json")

    def test_tap_run_params_discover_mode(self) -> None:
        cli_args: t.Cli.JsonMapping = {
            "tap_name": "tap-postgres",
            "discover": True,
        }
        result = u.Cli.cli_args_to_model(m.Meltano.TapRunParams, cli_args)
        tm.ok(result)
        model = result.value
        tm.that(model.discover is True, eq=True)

    def test_tap_run_params_all_fields(self) -> None:
        cli_args: t.Cli.JsonMapping = {
            "tap_name": "tap-postgres",
            "config_file": "/config.json",
            "catalog_file": "/catalog.json",
            "state_file": "/state.json",
            "properties_file": "/properties.json",
            "discover": False,
        }
        result = u.Cli.cli_args_to_model(m.Meltano.TapRunParams, cli_args)
        tm.ok(result)
        model = result.value
        tm.that(model.config_file, eq="/config.json")
        tm.that(model.catalog_file, eq="/catalog.json")
        tm.that(model.state_file, eq="/state.json")
        tm.that(model.properties_file, eq="/properties.json")

    def test_tap_run_params_missing_required(self) -> None:
        result = u.Cli.cli_args_to_model(m.Meltano.TapRunParams, {"discover": False})
        tm.fail(result)
        tm.that(str(result.error).lower(), has="validation")
        tm.that(str(result.error).lower(), has="tap_name")

    def test_tap_run_params_invalid_type(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.TapRunParams,
            {"tap_name": "tap-postgres", "discover": "not-a-boolean"},
        )
        tm.fail(result)
        tm.that(str(result.error).lower(), has="validation")

    def test_target_run_params_minimal(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.TargetRunParams,
            {"target_name": "target-postgres"},
        )
        tm.ok(result)
        model = result.value
        tm.that(model.target_name, eq="target-postgres")
        tm.that(model.config_file, none=True)
        tm.that(model.input_file, none=True)

    def test_target_run_params_with_config(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.TargetRunParams,
            {"target_name": "target-postgres", "config_file": "/path/to/config.json"},
        )
        tm.ok(result)
        tm.that(result.value.config_file, eq="/path/to/config.json")

    def test_target_run_params_with_input(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.TargetRunParams,
            {"target_name": "target-postgres", "input_file": "/path/to/input.jsonl"},
        )
        tm.ok(result)
        tm.that(result.value.input_file, eq="/path/to/input.jsonl")

    def test_target_run_params_all_fields(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.TargetRunParams,
            {
                "target_name": "target-postgres",
                "config_file": "/config.json",
                "input_file": "/input.jsonl",
            },
        )
        tm.ok(result)
        tm.that(result.value.config_file, eq="/config.json")
        tm.that(result.value.input_file, eq="/input.jsonl")

    def test_target_run_params_missing_required(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.TargetRunParams,
            {"config_file": "/config.json"},
        )
        tm.fail(result)
        tm.that(str(result.error).lower(), has="validation")
        tm.that(str(result.error).lower(), has="target_name")

    def test_pipeline_run_params_with_tap_args(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.TapRunParams,
            {"tap_name": "tap-postgres", "config_file": "/path/to/config.json"},
        )
        tm.ok(result)
        tm.that(result.value.tap_name, eq="tap-postgres")
        tm.that(result.value.config_file, eq="/path/to/config.json")

    def test_pipeline_run_params_with_target_args(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.TargetRunParams,
            {"target_name": "target-postgres", "config_file": "/path/to/config.json"},
        )
        tm.ok(result)
        tm.that(result.value.target_name, eq="target-postgres")
        tm.that(result.value.config_file, eq="/path/to/config.json")

    def test_pipeline_run_params_with_catalog_state(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.PipelineRunParams,
            {
                "tap_name": "tap-postgres",
                "target_name": "target-postgres",
                "catalog_file": "/catalog.json",
                "state_file": "/state.json",
            },
        )
        tm.ok(result)
        tm.that(result.value.catalog_file, eq="/catalog.json")
        tm.that(result.value.state_file, eq="/state.json")

    def test_pipeline_run_params_all_fields(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.PipelineRunParams,
            {
                "tap_name": "tap-postgres",
                "target_name": "target-postgres",
                "tap_config": "/tap-config.json",
                "target_config": "/target-config.json",
                "catalog_file": "/catalog.json",
                "state_file": "/state.json",
            },
        )
        tm.ok(result)
        tm.that(result.value.tap_config, eq="/tap-config.json")
        tm.that(result.value.target_config, eq="/target-config.json")
        tm.that(result.value.catalog_file, eq="/catalog.json")
        tm.that(result.value.state_file, eq="/state.json")

    def test_pipeline_run_params_missing_tap_name(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.PipelineRunParams,
            {"target_name": "target-postgres"},
        )
        tm.fail(result)
        tm.that(str(result.error).lower(), has="validation")

    def test_pipeline_run_params_missing_target_name(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.PipelineRunParams,
            {"tap_name": "tap-postgres"},
        )
        tm.fail(result)
        tm.that(str(result.error).lower(), has="validation")

    def test_dbt_run_params_minimal(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.DbtRunParams,
            {"project_dir": "/dbt/project"},
        )
        tm.ok(result)
        tm.that(result.value.project_dir, eq="/dbt/project")
        tm.that(result.value.models, none=True)
        tm.that(result.value.full_refresh is False, eq=True)

    def test_dbt_run_params_with_models(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.DbtRunParams,
            {"project_dir": "/dbt/project", "models": "users orders"},
        )
        tm.ok(result)
        tm.that(result.value.models, eq="users orders")

    def test_dbt_run_params_with_select_exclude(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.DbtRunParams,
            {
                "project_dir": "/dbt/project",
                "select": "tag:daily",
                "exclude": "tag:deprecated",
            },
        )
        tm.ok(result)
        tm.that(result.value.select, eq="tag:daily")
        tm.that(result.value.exclude, eq="tag:deprecated")

    def test_dbt_run_params_with_full_refresh(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.DbtRunParams,
            {"project_dir": "/dbt/project", "full_refresh": True},
        )
        tm.ok(result)
        tm.that(result.value.full_refresh is True, eq=True)

    def test_dbt_run_params_missing_required(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.DbtRunParams,
            {"models": "users"},
        )
        tm.fail(result)
        tm.that(str(result.error).lower(), has="validation")
