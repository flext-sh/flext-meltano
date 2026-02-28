"""Comprehensive tests for CLI to Model integration.

Tests the CliModelConverter integration with Meltano models:
- Dict to Pydantic model conversion
- Validation error propagation
- Round-trip conversion
- FlextResult railway pattern throughout

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import typing

from flext_cli import FlextCliModels
from flext_meltano import m, t


class TestCliModelConverterWithTapRunParams:
    """Test CliModelConverter integration with TapRunParams."""

    def test_converter_tap_run_params_minimal(self) -> None:
        """Test converting minimal dict[str, t.JsonValue] to TapRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "tap_name": "tap-postgres",
            "discover": False,
            "config_file": None,
            "catalog_file": None,
            "state_file": None,
            "properties_file": None,
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.TapRunParams", result.value)
        assert model.tap_name == "tap-postgres"
        assert model.config_file is None
        assert model.discover is False

    def test_converter_tap_run_params_with_config(self) -> None:
        """Test converting dict[str, t.JsonValue] with config to TapRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "tap_name": "tap-postgres",
            "config_file": "/path/to/config.json",
            "discover": False,
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.TapRunParams", result.value)
        assert model.tap_name == "tap-postgres"
        assert model.config_file == "/path/to/config.json"

    def test_converter_tap_run_params_discover_mode(self) -> None:
        """Test converting dict[str, t.JsonValue] with discover flag to TapRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "tap_name": "tap-postgres",
            "discover": True,
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.TapRunParams", result.value)
        assert model.tap_name == "tap-postgres"
        assert model.config_file is None
        assert model.discover is True

    def test_converter_tap_run_params_all_fields(self) -> None:
        """Test converting dict[str, t.JsonValue] with all fields to TapRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "tap_name": "tap-postgres",
            "config_file": "/config.json",
            "catalog_file": "/catalog.json",
            "state_file": "/state.json",
            "properties_file": "/properties.json",
            "discover": False,
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.TapRunParams", result.value)
        assert model.tap_name == "tap-postgres"
        assert model.config_file == "/config.json"
        assert model.catalog_file == "/catalog.json"
        assert model.state_file == "/state.json"
        assert model.properties_file == "/properties.json"
        assert model.discover is False

    def test_converter_tap_run_params_missing_required(self) -> None:
        """Test validation error when tap_name is missing."""
        cli_args: dict[str, t.JsonValue] = {
            "discover": False,
            # Missing required tap_name
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams,
            cli_args,
        )

        assert result.is_failure
        assert "validation" in str(result.error).lower()
        assert "tap_name" in str(result.error).lower()

    def test_converter_tap_run_params_invalid_type(self) -> None:
        """Test validation error when field has wrong type."""
        cli_args: dict[str, t.JsonValue] = {
            "tap_name": "tap-postgres",
            "discover": "not-a-boolean",  # Should be bool
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams,
            cli_args,
        )

        assert result.is_failure
        assert "validation" in str(result.error).lower()


class TestCliModelConverterWithTargetRunParams:
    """Test CliModelConverter integration with TargetRunParams."""

    def test_converter_target_run_params_minimal(self) -> None:
        """Test converting minimal dict[str, t.JsonValue] to TargetRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "target_name": "target-postgres",
            "config_file": None,
            "input_file": None,
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        assert model.target_name == "target-postgres"
        assert model.config_file is None
        assert model.input_file is None

    def test_converter_target_run_params_with_config(self) -> None:
        """Test converting dict[str, t.JsonValue] with config to TargetRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "target_name": "target-postgres",
            "config_file": "/path/to/config.json",
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        assert model.target_name == "target-postgres"
        assert model.config_file == "/path/to/config.json"

    def test_converter_target_run_params_with_input(self) -> None:
        """Test converting dict[str, t.JsonValue] with input file to TargetRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "target_name": "target-postgres",
            "input_file": "/path/to/input.jsonl",
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        assert model.target_name == "target-postgres"
        assert model.input_file == "/path/to/input.jsonl"

    def test_converter_target_run_params_all_fields(self) -> None:
        """Test converting dict[str, t.JsonValue] with all fields to TargetRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "target_name": "target-postgres",
            "config_file": "/config.json",
            "input_file": "/input.jsonl",
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        assert model.target_name == "target-postgres"
        assert model.config_file == "/config.json"
        assert model.input_file == "/input.jsonl"

    def test_converter_target_run_params_missing_required(self) -> None:
        """Test validation error when target_name is missing."""
        cli_args: dict[str, t.JsonValue] = {
            "config_file": "/config.json",
            # Missing required target_name
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams,
            cli_args,
        )

        assert result.is_failure
        assert "validation" in str(result.error).lower()
        assert "target_name" in str(result.error).lower()


class TestCliModelConverterWithPipelineRunParams:
    """Test CliModelConverter integration with PipelineRunParams."""

    def test_converter_tap_run_params_minimal(self) -> None:
        """Test converting minimal dict[str, t.JsonValue] to TapRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "tap_name": "tap-postgres",
            "config_file": "/path/to/config.json",
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.TapRunParams", result.value)
        assert model.tap_name == "tap-postgres"
        assert model.config_file == "/path/to/config.json"

    def test_converter_target_run_params_with_config(self) -> None:
        """Test converting dict[str, t.JsonValue] with config_file to TargetRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "target_name": "target-postgres",
            "config_file": "/path/to/config.json",
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        assert model.target_name == "target-postgres"
        assert model.config_file == "/path/to/config.json"

    def test_converter_pipeline_run_params_with_catalog_state(self) -> None:
        """Test converting dict[str, t.JsonValue] with catalog/state to PipelineRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "tap_name": "tap-postgres",
            "target_name": "target-postgres",
            "catalog_file": "/catalog.json",
            "state_file": "/state.json",
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.PipelineRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.PipelineRunParams", result.value)
        assert model.catalog_file == "/catalog.json"
        assert model.state_file == "/state.json"

    def test_converter_pipeline_run_params_all_fields(self) -> None:
        """Test converting dict[str, t.JsonValue] with all fields to PipelineRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "tap_name": "tap-postgres",
            "target_name": "target-postgres",
            "tap_config": "/tap-config.json",
            "target_config": "/target-config.json",
            "catalog_file": "/catalog.json",
            "state_file": "/state.json",
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.PipelineRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.PipelineRunParams", result.value)
        assert model.tap_name == "tap-postgres"
        assert model.target_name == "target-postgres"
        assert model.tap_config == "/tap-config.json"
        assert model.target_config == "/target-config.json"
        assert model.catalog_file == "/catalog.json"
        assert model.state_file == "/state.json"

    def test_converter_pipeline_run_params_missing_tap_name(self) -> None:
        """Test validation error when tap_name is missing."""
        cli_args: dict[str, t.JsonValue] = {
            "target_name": "target-postgres",
            # Missing required tap_name
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.PipelineRunParams,
            cli_args,
        )

        assert result.is_failure
        assert "validation" in str(result.error).lower()

    def test_converter_pipeline_run_params_missing_target_name(self) -> None:
        """Test validation error when target_name is missing."""
        cli_args: dict[str, t.JsonValue] = {
            "tap_name": "tap-postgres",
            # Missing required target_name
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.PipelineRunParams,
            cli_args,
        )

        assert result.is_failure
        assert "validation" in str(result.error).lower()


class TestCliModelConverterWithDbtRunParams:
    """Test CliModelConverter integration with DbtRunParams."""

    def test_converter_dbt_run_params_minimal(self) -> None:
        """Test converting minimal dict[str, t.JsonValue] to DbtRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "project_dir": "/dbt/project",
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.DbtRunParams", result.value)
        assert model.project_dir == "/dbt/project"
        assert model.models is None
        assert model.full_refresh is False

    def test_converter_dbt_run_params_with_models(self) -> None:
        """Test converting dict[str, t.JsonValue] with models to DbtRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "project_dir": "/dbt/project",
            "models": "users orders",
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.DbtRunParams", result.value)
        assert model.models == "users orders"

    def test_converter_dbt_run_params_with_select_exclude(self) -> None:
        """Test converting dict[str, t.JsonValue] with select/exclude to DbtRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "project_dir": "/dbt/project",
            "select": "tag:daily",
            "exclude": "tag:deprecated",
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.DbtRunParams", result.value)
        assert model.select == "tag:daily"
        assert model.exclude == "tag:deprecated"

    def test_converter_dbt_run_params_with_full_refresh(self) -> None:
        """Test converting dict[str, t.JsonValue] with full_refresh to DbtRunParams model."""
        cli_args: dict[str, t.JsonValue] = {
            "project_dir": "/dbt/project",
            "full_refresh": True,
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams,
            cli_args,
        )

        assert result.is_success
        model = typing.cast("m.Meltano.DbtRunParams", result.value)
        assert model.full_refresh is True

    def test_converter_dbt_run_params_missing_required(self) -> None:
        """Test validation error when project_dir is missing."""
        cli_args: dict[str, t.JsonValue] = {
            "models": "users",
            # Missing required project_dir
        }

        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams,
            cli_args,
        )

        assert result.is_failure
        assert "validation" in str(result.error).lower()
