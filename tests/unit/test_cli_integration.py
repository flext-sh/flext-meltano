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
from collections.abc import Mapping

from flext_tests import tm

from tests import m, t


class TestCliModelConverterWithTapRunParams:
    """Test CliModelConverter integration with TapRunParams."""

    def test_converter_tap_run_params_minimal(self) -> None:
        """Test converting minimal Mapping[str, objectTapRunParams model."""
        cli_args: Mapping[str, str | bool | None] = {
            "tap_name": "tap-postgres",
            "discover": False,
            "config_file": None,
            "catalog_file": None,
            "state_file": None,
            "properties_file": None,
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams,
            cli_args,
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TapRunParams", result.value)
        tm.that(model.tap_name, eq="tap-postgres")
        tm.that(model.config_file, none=True)
        tm.that(model.discover is False, eq=True)

    def test_converter_tap_run_params_with_config(self) -> None:
        """Test converting Mapping[str, objecth config to TapRunParams model."""
        cli_args = {
            "tap_name": "tap-postgres",
            "config_file": "/path/to/config.json",
            "discover": False,
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams,
            cli_args,
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TapRunParams", result.value)
        tm.that(model.tap_name, eq="tap-postgres")
        tm.that(model.config_file, eq="/path/to/config.json")

    def test_converter_tap_run_params_discover_mode(self) -> None:
        """Test converting Mapping[str, objecth discover flag to TapRunParams model."""
        cli_args = {
            "tap_name": "tap-postgres",
            "discover": True,
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams,
            cli_args,
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TapRunParams", result.value)
        tm.that(model.tap_name, eq="tap-postgres")
        tm.that(model.config_file, none=True)
        tm.that(model.discover is True, eq=True)

    def test_converter_tap_run_params_all_fields(self) -> None:
        """Test converting Mapping[str, objecth all fields to TapRunParams model."""
        cli_args = {
            "tap_name": "tap-postgres",
            "config_file": "/config.json",
            "catalog_file": "/catalog.json",
            "state_file": "/state.json",
            "properties_file": "/properties.json",
            "discover": False,
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams,
            cli_args,
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
        cli_args: t.ContainerMapping = {"discover": False}
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams,
            cli_args,
        )
        tm.fail(result)
        tm.that(str(result.error).lower(), has="validation")
        tm.that(str(result.error).lower(), has="tap_name")

    def test_converter_tap_run_params_invalid_type(self) -> None:
        """Test validation error when field has wrong type."""
        cli_args: t.ContainerMapping = {
            "tap_name": "tap-postgres",
            "discover": "not-a-boolean",
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams,
            cli_args,
        )
        tm.fail(result)
        tm.that(str(result.error).lower(), has="validation")


class TestCliModelConverterWithTargetRunParams:
    """Test CliModelConverter integration with TargetRunParams."""

    def test_converter_target_run_params_minimal(self) -> None:
        """Test converting minimal Mapping[str, objectTargetRunParams model."""
        cli_args: Mapping[str, str | None] = {
            "target_name": "target-postgres",
            "config_file": None,
            "input_file": None,
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams,
            cli_args,
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        tm.that(model.target_name, eq="target-postgres")
        tm.that(model.config_file, none=True)
        tm.that(model.input_file, none=True)

    def test_converter_target_run_params_with_config(self) -> None:
        """Test converting Mapping[str, objecth config to TargetRunParams model."""
        cli_args: t.ContainerMapping = {
            "target_name": "target-postgres",
            "config_file": "/path/to/config.json",
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams,
            cli_args,
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        tm.that(model.target_name, eq="target-postgres")
        tm.that(model.config_file, eq="/path/to/config.json")

    def test_converter_target_run_params_with_input(self) -> None:
        """Test converting Mapping[str, objecth input file to TargetRunParams model."""
        cli_args: t.ContainerMapping = {
            "target_name": "target-postgres",
            "input_file": "/path/to/input.jsonl",
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams,
            cli_args,
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        tm.that(model.target_name, eq="target-postgres")
        tm.that(model.input_file, eq="/path/to/input.jsonl")

    def test_converter_target_run_params_all_fields(self) -> None:
        """Test converting Mapping[str, objecth all fields to TargetRunParams model."""
        cli_args: t.ContainerMapping = {
            "target_name": "target-postgres",
            "config_file": "/config.json",
            "input_file": "/input.jsonl",
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams,
            cli_args,
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        tm.that(model.target_name, eq="target-postgres")
        tm.that(model.config_file, eq="/config.json")
        tm.that(model.input_file, eq="/input.jsonl")

    def test_converter_target_run_params_missing_required(self) -> None:
        """Test validation error when target_name is missing."""
        cli_args: t.ContainerMapping = {"config_file": "/config.json"}
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams,
            cli_args,
        )
        tm.fail(result)
        tm.that(str(result.error).lower(), has="validation")
        tm.that(str(result.error).lower(), has="target_name")


class TestCliModelConverterWithPipelineRunParams:
    """Test CliModelConverter integration with PipelineRunParams."""

    def test_converter_tap_run_params_minimal(self) -> None:
        """Test converting minimal Mapping[str, objectTapRunParams model."""
        cli_args: t.ContainerMapping = {
            "tap_name": "tap-postgres",
            "config_file": "/path/to/config.json",
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TapRunParams,
            cli_args,
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TapRunParams", result.value)
        tm.that(model.tap_name, eq="tap-postgres")
        tm.that(model.config_file, eq="/path/to/config.json")

    def test_converter_target_run_params_with_config(self) -> None:
        """Test converting Mapping[str, objecth config_file to TargetRunParams model."""
        cli_args: t.ContainerMapping = {
            "target_name": "target-postgres",
            "config_file": "/path/to/config.json",
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.TargetRunParams,
            cli_args,
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.TargetRunParams", result.value)
        tm.that(model.target_name, eq="target-postgres")
        tm.that(model.config_file, eq="/path/to/config.json")

    def test_converter_pipeline_run_params_with_catalog_state(self) -> None:
        """Test converting Mapping[str, objecth catalog/state to PipelineRunParams model."""
        cli_args: t.ContainerMapping = {
            "tap_name": "tap-postgres",
            "target_name": "target-postgres",
            "catalog_file": "/catalog.json",
            "state_file": "/state.json",
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.PipelineRunParams,
            cli_args,
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.PipelineRunParams", result.value)
        tm.that(model.catalog_file, eq="/catalog.json")
        tm.that(model.state_file, eq="/state.json")

    def test_converter_pipeline_run_params_all_fields(self) -> None:
        """Test converting Mapping[str, objecth all fields to PipelineRunParams model."""
        cli_args: t.ContainerMapping = {
            "tap_name": "tap-postgres",
            "target_name": "target-postgres",
            "tap_config": "/tap-config.json",
            "target_config": "/target-config.json",
            "catalog_file": "/catalog.json",
            "state_file": "/state.json",
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.PipelineRunParams,
            cli_args,
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
        cli_args: t.ContainerMapping = {"target_name": "target-postgres"}
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.PipelineRunParams,
            cli_args,
        )
        tm.fail(result)
        tm.that(str(result.error).lower(), has="validation")

    def test_converter_pipeline_run_params_missing_target_name(self) -> None:
        """Test validation error when target_name is missing."""
        cli_args: t.ContainerMapping = {"tap_name": "tap-postgres"}
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.PipelineRunParams,
            cli_args,
        )
        tm.fail(result)
        tm.that(str(result.error).lower(), has="validation")


class TestCliModelConverterWithDbtRunParams:
    """Test CliModelConverter integration with DbtRunParams."""

    def test_converter_dbt_run_params_minimal(self) -> None:
        """Test converting minimal Mapping[str, objectDbtRunParams model."""
        cli_args: t.ContainerMapping = {"project_dir": "/dbt/project"}
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams,
            cli_args,
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.DbtRunParams", result.value)
        tm.that(model.project_dir, eq="/dbt/project")
        tm.that(model.models, none=True)
        tm.that(model.full_refresh is False, eq=True)

    def test_converter_dbt_run_params_with_models(self) -> None:
        """Test converting Mapping[str, objecth models to DbtRunParams model."""
        cli_args: t.ContainerMapping = {
            "project_dir": "/dbt/project",
            "models": "users orders",
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams,
            cli_args,
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.DbtRunParams", result.value)
        tm.that(model.models, eq="users orders")

    def test_converter_dbt_run_params_with_select_exclude(self) -> None:
        """Test converting Mapping[str, objecth select/exclude to DbtRunParams model."""
        cli_args: t.ContainerMapping = {
            "project_dir": "/dbt/project",
            "select": "tag:daily",
            "exclude": "tag:deprecated",
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams,
            cli_args,
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.DbtRunParams", result.value)
        tm.that(model.select, eq="tag:daily")
        tm.that(model.exclude, eq="tag:deprecated")

    def test_converter_dbt_run_params_with_full_refresh(self) -> None:
        """Test converting Mapping[str, objecth full_refresh to DbtRunParams model."""
        cli_args: t.ContainerMapping = {
            "project_dir": "/dbt/project",
            "full_refresh": True,
        }
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams,
            cli_args,
        )
        tm.ok(result)
        model = typing.cast("m.Meltano.DbtRunParams", result.value)
        tm.that(model.full_refresh is True, eq=True)

    def test_converter_dbt_run_params_missing_required(self) -> None:
        """Test validation error when project_dir is missing."""
        cli_args: t.ContainerMapping = {"models": "users"}
        result = m.Cli.CliModelConverter.cli_args_to_model(
            m.Meltano.DbtRunParams,
            cli_args,
        )
        tm.fail(result)
        tm.that(str(result.error).lower(), has="validation")
