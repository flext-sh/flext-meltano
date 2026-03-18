"""Comprehensive tests for CLI to Model integration.

Tests the CliModelConverter integration with Meltano models:
- Dict to Pydantic model conversion
- Validation error propagation
- Round-trip conversion
- r railway pattern throughout

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import typing

from flext_cli import FlextCliModels
from flext_tests import tm

from flext_meltano import m, t


class TestCliModelConverterWithTapRunParams:
    """Test CliModelConverter integration with TapRunParams."""

    def test_converter_tap_run_params_minimal(self) -> None:
        """Test converting minimal dict[str, objectTapRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "tap_name": "tap-postgres",
            "discover": False,
            "config_file": None,
            "catalog_file": None,
            "state_file": None,
            "properties_file": None,
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TapRunParams", result.value)
        tm.that(model.tap_name, eq="tap-postgres")
        tm.that(model.config_file is None, eq=True)
        tm.that(model.discover is False, eq=True)

    def test_converter_tap_run_params_with_config(self) -> None:
        """Test converting dict[str, objecth config to TapRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "tap_name": "tap-postgres",
            "config_file": "/path/to/config.json",
            "discover": False,
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TapRunParams", result.value)
        tm.that(model.tap_name, eq="tap-postgres")
        tm.that(model.config_file, eq="/path/to/config.json")

    def test_converter_tap_run_params_discover_mode(self) -> None:
        """Test converting dict[str, objecth discover flag to TapRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "tap_name": "tap-postgres",
            "discover": True,
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TapRunParams", result.value)
        tm.that(model.tap_name, eq="tap-postgres")
        tm.that(model.config_file is None, eq=True)
        tm.that(model.discover is True, eq=True)

    def test_converter_tap_run_params_all_fields(self) -> None:
        """Test converting dict[str, objecth all fields to TapRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "tap_name": "tap-postgres",
            "config_file": "/config.json",
            "catalog_file": "/catalog.json",
            "state_file": "/state.json",
            "properties_file": "/properties.json",
            "discover": False,
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TapRunParams", result.value)
        tm.that(model.tap_name, eq="tap-postgres")
        tm.that(model.config_file, eq="/config.json")
        tm.that(model.catalog_file, eq="/catalog.json")
        tm.that(model.state_file, eq="/state.json")
        tm.that(model.properties_file, eq="/properties.json")
        tm.that(model.discover is False, eq=True)

    def test_converter_tap_run_params_missing_required(self) -> None:
        """Test validation error when tap_name is missing."""
        cli_args: dict[str, t.Scalar] = {"discover": False}
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams, cli_args
        )
        tm.fail(result)
        tm.that("validation" in str(result.error).lower(), eq=True)
        tm.that("tap_name" in str(result.error).lower(), eq=True)

    def test_converter_tap_run_params_invalid_type(self) -> None:
        """Test validation error when field has wrong type."""
        cli_args: dict[str, t.Scalar] = {
            "tap_name": "tap-postgres",
            "discover": "not-a-boolean",
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams, cli_args
        )
        tm.fail(result)
        tm.that("validation" in str(result.error).lower(), eq=True)


class TestCliModelConverterWithTargetRunParams:
    """Test CliModelConverter integration with TargetRunParams."""

    def test_converter_target_run_params_minimal(self) -> None:
        """Test converting minimal dict[str, objectTargetRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "target_name": "target-postgres",
            "config_file": None,
            "input_file": None,
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        tm.that(model.target_name, eq="target-postgres")
        tm.that(model.config_file is None, eq=True)
        tm.that(model.input_file is None, eq=True)

    def test_converter_target_run_params_with_config(self) -> None:
        """Test converting dict[str, objecth config to TargetRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "target_name": "target-postgres",
            "config_file": "/path/to/config.json",
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        tm.that(model.target_name, eq="target-postgres")
        tm.that(model.config_file, eq="/path/to/config.json")

    def test_converter_target_run_params_with_input(self) -> None:
        """Test converting dict[str, objecth input file to TargetRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "target_name": "target-postgres",
            "input_file": "/path/to/input.jsonl",
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        tm.that(model.target_name, eq="target-postgres")
        tm.that(model.input_file, eq="/path/to/input.jsonl")

    def test_converter_target_run_params_all_fields(self) -> None:
        """Test converting dict[str, objecth all fields to TargetRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "target_name": "target-postgres",
            "config_file": "/config.json",
            "input_file": "/input.jsonl",
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        tm.that(model.target_name, eq="target-postgres")
        tm.that(model.config_file, eq="/config.json")
        tm.that(model.input_file, eq="/input.jsonl")

    def test_converter_target_run_params_missing_required(self) -> None:
        """Test validation error when target_name is missing."""
        cli_args: dict[str, t.Scalar] = {"config_file": "/config.json"}
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams, cli_args
        )
        tm.fail(result)
        tm.that("validation" in str(result.error).lower(), eq=True)
        tm.that("target_name" in str(result.error).lower(), eq=True)


class TestCliModelConverterWithPipelineRunParams:
    """Test CliModelConverter integration with PipelineRunParams."""

    def test_converter_tap_run_params_minimal(self) -> None:
        """Test converting minimal dict[str, objectTapRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "tap_name": "tap-postgres",
            "config_file": "/path/to/config.json",
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TapRunParams", result.value)
        tm.that(model.tap_name, eq="tap-postgres")
        tm.that(model.config_file, eq="/path/to/config.json")

    def test_converter_target_run_params_with_config(self) -> None:
        """Test converting dict[str, objecth config_file to TargetRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "target_name": "target-postgres",
            "config_file": "/path/to/config.json",
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        tm.that(model.target_name, eq="target-postgres")
        tm.that(model.config_file, eq="/path/to/config.json")

    def test_converter_pipeline_run_params_with_catalog_state(self) -> None:
        """Test converting dict[str, objecth catalog/state to PipelineRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "tap_name": "tap-postgres",
            "target_name": "target-postgres",
            "catalog_file": "/catalog.json",
            "state_file": "/state.json",
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.PipelineRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.PipelineRunParams", result.value)
        tm.that(model.catalog_file, eq="/catalog.json")
        tm.that(model.state_file, eq="/state.json")

    def test_converter_pipeline_run_params_all_fields(self) -> None:
        """Test converting dict[str, objecth all fields to PipelineRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "tap_name": "tap-postgres",
            "target_name": "target-postgres",
            "tap_config": "/tap-config.json",
            "target_config": "/target-config.json",
            "catalog_file": "/catalog.json",
            "state_file": "/state.json",
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.PipelineRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.PipelineRunParams", result.value)
        tm.that(model.tap_name, eq="tap-postgres")
        tm.that(model.target_name, eq="target-postgres")
        tm.that(model.tap_config, eq="/tap-config.json")
        tm.that(model.target_config, eq="/target-config.json")
        tm.that(model.catalog_file, eq="/catalog.json")
        tm.that(model.state_file, eq="/state.json")

    def test_converter_pipeline_run_params_missing_tap_name(self) -> None:
        """Test validation error when tap_name is missing."""
        cli_args: dict[str, t.Scalar] = {"target_name": "target-postgres"}
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.PipelineRunParams, cli_args
        )
        tm.fail(result)
        tm.that("validation" in str(result.error).lower(), eq=True)

    def test_converter_pipeline_run_params_missing_target_name(self) -> None:
        """Test validation error when target_name is missing."""
        cli_args: dict[str, t.Scalar] = {"tap_name": "tap-postgres"}
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.PipelineRunParams, cli_args
        )
        tm.fail(result)
        tm.that("validation" in str(result.error).lower(), eq=True)


class TestCliModelConverterWithDbtRunParams:
    """Test CliModelConverter integration with DbtRunParams."""

    def test_converter_dbt_run_params_minimal(self) -> None:
        """Test converting minimal dict[str, objectDbtRunParams model."""
        cli_args: dict[str, t.Scalar] = {"project_dir": "/dbt/project"}
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.DbtRunParams", result.value)
        tm.that(model.project_dir, eq="/dbt/project")
        tm.that(model.models is None, eq=True)
        tm.that(model.full_refresh is False, eq=True)

    def test_converter_dbt_run_params_with_models(self) -> None:
        """Test converting dict[str, objecth models to DbtRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "project_dir": "/dbt/project",
            "models": "users orders",
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.DbtRunParams", result.value)
        tm.that(model.models, eq="users orders")

    def test_converter_dbt_run_params_with_select_exclude(self) -> None:
        """Test converting dict[str, objecth select/exclude to DbtRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "project_dir": "/dbt/project",
            "select": "tag:daily",
            "exclude": "tag:deprecated",
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.DbtRunParams", result.value)
        tm.that(model.select, eq="tag:daily")
        tm.that(model.exclude, eq="tag:deprecated")

    def test_converter_dbt_run_params_with_full_refresh(self) -> None:
        """Test converting dict[str, objecth full_refresh to DbtRunParams model."""
        cli_args: dict[str, t.Scalar] = {
            "project_dir": "/dbt/project",
            "full_refresh": True,
        }
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams, cli_args
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.DbtRunParams", result.value)
        tm.that(model.full_refresh is True, eq=True)

    def test_converter_dbt_run_params_missing_required(self) -> None:
        """Test validation error when project_dir is missing."""
        cli_args: dict[str, t.Scalar] = {"models": "users"}
        result = FlextCliModels.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams, cli_args
        )
        tm.fail(result)
        tm.that("validation" in str(result.error).lower(), eq=True)
