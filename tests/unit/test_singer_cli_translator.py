"""Comprehensive tests for FlextMeltanoSingerCliTranslator module.

Tests the complete Singer SDK CLI command translation layer including:
- Pydantic model to CLI command conversion
- Command validation and error handling
- File path validation
- Command execution (mocked)

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from flext_infra import FlextInfraModels as m_infra
from flext_tests import tm

from flext_core import r
from flext_meltano import FlextMeltanoSingerCliTranslator
from tests import m


class TestFlextMeltanoSingerCliTranslatorTapRun:
    """Test translate_tap_run method."""

    def test_translate_tap_run_minimal(self) -> None:
        """Test tap run translation with minimal parameters."""
        params = m.Meltano.CliParameters.DataSourceParams(
            source_name="tap-postgres",
            discover=False,
        )
        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)
        tm.ok(result)
        command = result.value
        tm.that(command, eq=["tap-postgres"])

    def test_translate_tap_run_discover_mode(self) -> None:
        """Test tap run translation in discover mode."""
        params = m.Meltano.CliParameters.DataSourceParams(
            source_name="tap-postgres",
            discover=True,
        )
        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)
        tm.ok(result)
        command = result.value
        tm.that(command, eq=["tap-postgres", "--discover"])

    def test_translate_tap_run_with_config(self) -> None:
        """Test tap run translation with config file."""
        params = m.Meltano.CliParameters.DataSourceParams(
            source_name="tap-postgres",
            config_file="/path/to/config.json",
            discover=False,
        )
        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)
        tm.ok(result)
        command = result.value
        tm.that(command, eq=["tap-postgres", "--config", "/path/to/config.json"])

    def test_translate_tap_run_with_catalog(self) -> None:
        """Test tap run translation with catalog file."""
        params = m.Meltano.CliParameters.DataSourceParams(
            source_name="tap-postgres",
            catalog_file="/path/to/catalog.json",
            discover=False,
        )
        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)
        tm.ok(result)
        command = result.value
        tm.that(command, has="--catalog")

    def test_translate_tap_run_with_state(self) -> None:
        """Test tap run translation with state file."""
        params = m.Meltano.CliParameters.DataSourceParams(
            source_name="tap-postgres",
            state_file="/path/to/state.json",
            discover=False,
        )
        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)
        tm.ok(result)
        command = result.value
        tm.that(command, eq=["tap-postgres", "--state", "/path/to/state.json"])

    def test_translate_tap_run_with_all_parameters(self) -> None:
        """Test tap run translation with all parameters."""
        params = m.Meltano.CliParameters.DataSourceParams(
            source_name="tap-postgres",
            config_file="/path/to/config.json",
            catalog_file="/path/to/catalog.json",
            state_file="/path/to/state.json",
            discover=False,
        )
        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)
        tm.ok(result)
        command = result.value
        tm.that(command, has="tap-postgres")
        tm.that(command, has="--config")
        tm.that(command, has="--catalog")
        tm.that(command, has="--state")

    def test_translate_tap_run_discover_ignores_other_params(self) -> None:
        """Test that discover mode returns early, ignoring other parameters."""
        params = m.Meltano.CliParameters.DataSourceParams(
            source_name="tap-postgres",
            config_file="/path/to/config.json",
            catalog_file="/path/to/catalog.json",
            discover=True,
        )
        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)
        tm.ok(result)
        command = result.value
        tm.that(command, eq=["tap-postgres", "--discover"])


class TestFlextMeltanoSingerCliTranslatorTargetRun:
    """Test translate_target_run method."""

    def test_translate_target_run_minimal(self) -> None:
        """Test target run translation with minimal parameters."""
        params = m.Meltano.CliParameters.DataSinkParams(sink_name="target-postgres")
        result = FlextMeltanoSingerCliTranslator.translate_target_run(params)
        tm.ok(result)
        command = result.value
        tm.that(command, eq=["target-postgres"])

    def test_translate_target_run_with_config(self) -> None:
        """Test target run translation with config file."""
        params = m.Meltano.CliParameters.DataSinkParams(
            sink_name="target-postgres",
            config_file="/path/to/config.json",
        )
        result = FlextMeltanoSingerCliTranslator.translate_target_run(params)
        tm.ok(result)
        command = result.value
        tm.that(command, eq=["target-postgres", "--config", "/path/to/config.json"])

    def test_translate_target_run_with_input(self) -> None:
        """Test target run translation with input file."""
        params = m.Meltano.CliParameters.DataSinkParams(
            sink_name="target-postgres",
            input_file="/path/to/input.jsonl",
        )
        result = FlextMeltanoSingerCliTranslator.translate_target_run(params)
        tm.ok(result)
        command = result.value
        tm.that(command, eq=["target-postgres", "--input", "/path/to/input.jsonl"])

    def test_translate_target_run_with_all_parameters(self) -> None:
        """Test target run translation with all parameters."""
        params = m.Meltano.CliParameters.DataSinkParams(
            sink_name="target-postgres",
            config_file="/path/to/config.json",
            input_file="/path/to/input.jsonl",
        )
        result = FlextMeltanoSingerCliTranslator.translate_target_run(params)
        tm.ok(result)
        command = result.value
        tm.that(
            command,
            eq=[
                "target-postgres",
                "--config",
                "/path/to/config.json",
                "--input",
                "/path/to/input.jsonl",
            ],
        )


class TestFlextMeltanoSingerCliTranslatorPipelineRun:
    """Test translate_pipeline_run method."""

    def test_translate_pipeline_run_minimal(self) -> None:
        """Test pipeline run translation with minimal parameters."""
        params = m.Meltano.CliParameters.PipelineParams(
            source_name="tap-postgres",
            sink_name="target-postgres",
        )
        result = FlextMeltanoSingerCliTranslator.translate_pipeline_run(params)
        tm.ok(result)
        source_command, sink_command = result.value
        tm.that(source_command, eq=["tap-postgres"])
        tm.that(sink_command, eq=["target-postgres"])

    def test_translate_pipeline_run_with_source_config(self) -> None:
        """Test pipeline run translation with source config."""
        params = m.Meltano.CliParameters.PipelineParams(
            source_name="tap-postgres",
            sink_name="target-postgres",
            source_config="/path/to/tap-config.json",
        )
        result = FlextMeltanoSingerCliTranslator.translate_pipeline_run(params)
        tm.ok(result)
        source_command, sink_command = result.value
        tm.that(
            source_command,
            eq=[
                "tap-postgres",
                "--config",
                "/path/to/tap-config.json",
            ],
        )
        tm.that(sink_command, eq=["target-postgres"])

    def test_translate_pipeline_run_with_sink_config(self) -> None:
        """Test pipeline run translation with sink config."""
        params = m.Meltano.CliParameters.PipelineParams(
            source_name="tap-postgres",
            sink_name="target-postgres",
            sink_config="/path/to/target-config.json",
        )
        result = FlextMeltanoSingerCliTranslator.translate_pipeline_run(params)
        tm.ok(result)
        source_command, sink_command = result.value
        tm.that(source_command, eq=["tap-postgres"])
        tm.that(
            sink_command,
            eq=[
                "target-postgres",
                "--config",
                "/path/to/target-config.json",
            ],
        )

    def test_translate_pipeline_run_with_catalog(self) -> None:
        """Test pipeline run translation with catalog file."""
        params = m.Meltano.CliParameters.PipelineParams(
            source_name="tap-postgres",
            sink_name="target-postgres",
            catalog_file="/path/to/catalog.json",
        )
        result = FlextMeltanoSingerCliTranslator.translate_pipeline_run(params)
        tm.ok(result)
        source_command, sink_command = result.value
        tm.that(
            source_command,
            eq=["tap-postgres", "--catalog", "/path/to/catalog.json"],
        )
        tm.that(sink_command, eq=["target-postgres"])

    def test_translate_pipeline_run_with_state(self) -> None:
        """Test pipeline run translation with state file."""
        params = m.Meltano.CliParameters.PipelineParams(
            source_name="tap-postgres",
            sink_name="target-postgres",
            state_file="/path/to/state.json",
        )
        result = FlextMeltanoSingerCliTranslator.translate_pipeline_run(params)
        tm.ok(result)
        source_command, sink_command = result.value
        tm.that(source_command, eq=["tap-postgres", "--state", "/path/to/state.json"])
        tm.that(sink_command, eq=["target-postgres"])

    def test_translate_pipeline_run_with_all_parameters(self) -> None:
        """Test pipeline run translation with all parameters."""
        params = m.Meltano.CliParameters.PipelineParams(
            source_name="tap-postgres",
            sink_name="target-postgres",
            source_config="/path/to/tap-config.json",
            sink_config="/path/to/target-config.json",
            catalog_file="/path/to/catalog.json",
            state_file="/path/to/state.json",
        )
        result = FlextMeltanoSingerCliTranslator.translate_pipeline_run(params)
        tm.ok(result)
        source_command, sink_command = result.value
        tm.that(
            source_command,
            eq=[
                "tap-postgres",
                "--config",
                "/path/to/tap-config.json",
                "--catalog",
                "/path/to/catalog.json",
                "--state",
                "/path/to/state.json",
            ],
        )
        tm.that(
            sink_command,
            eq=[
                "target-postgres",
                "--config",
                "/path/to/target-config.json",
            ],
        )


class TestFlextMeltanoSingerCliTranslatorDbtRun:
    """Test translate_dbt_run method."""

    def test_translate_dbt_run_minimal(self) -> None:
        """Test DBT run translation with minimal parameters."""
        params = m.Meltano.CliParameters.TransformationParams(
            project_dir="/path/to/dbt/project",
        )
        result = FlextMeltanoSingerCliTranslator.translate_dbt_run(params)
        tm.ok(result)
        command = result.value
        tm.that(command, eq=["dbt", "run", "--projects-dir", "/path/to/dbt/project"])

    def test_translate_dbt_run_with_models(self) -> None:
        """Test DBT run translation with models parameter."""
        params = m.Meltano.CliParameters.TransformationParams(
            project_dir="/path/to/dbt/project",
            models="users orders",
        )
        result = FlextMeltanoSingerCliTranslator.translate_dbt_run(params)
        tm.ok(result)
        command = result.value
        tm.that(
            command,
            eq=[
                "dbt",
                "run",
                "--projects-dir",
                "/path/to/dbt/project",
                "--models",
                "users orders",
            ],
        )

    def test_translate_dbt_run_with_select(self) -> None:
        """Test DBT run translation with select parameter."""
        params = m.Meltano.CliParameters.TransformationParams(
            project_dir="/path/to/dbt/project",
            select="tag:daily",
        )
        result = FlextMeltanoSingerCliTranslator.translate_dbt_run(params)
        tm.ok(result)
        command = result.value
        tm.that(
            command,
            eq=[
                "dbt",
                "run",
                "--projects-dir",
                "/path/to/dbt/project",
                "--select",
                "tag:daily",
            ],
        )

    def test_translate_dbt_run_with_exclude(self) -> None:
        """Test DBT run translation with exclude parameter."""
        params = m.Meltano.CliParameters.TransformationParams(
            project_dir="/path/to/dbt/project",
            exclude="tag:deprecated",
        )
        result = FlextMeltanoSingerCliTranslator.translate_dbt_run(params)
        tm.ok(result)
        command = result.value
        tm.that(
            command,
            eq=[
                "dbt",
                "run",
                "--projects-dir",
                "/path/to/dbt/project",
                "--exclude",
                "tag:deprecated",
            ],
        )

    def test_translate_dbt_run_with_full_refresh(self) -> None:
        """Test DBT run translation with full refresh flag."""
        params = m.Meltano.CliParameters.TransformationParams(
            project_dir="/path/to/dbt/project",
            full_refresh=True,
        )
        result = FlextMeltanoSingerCliTranslator.translate_dbt_run(params)
        tm.ok(result)
        command = result.value
        tm.that(
            command,
            eq=[
                "dbt",
                "run",
                "--projects-dir",
                "/path/to/dbt/project",
                "--full-refresh",
            ],
        )

    def test_translate_dbt_run_with_all_parameters(self) -> None:
        """Test DBT run translation with all parameters."""
        params = m.Meltano.CliParameters.TransformationParams(
            project_dir="/path/to/dbt/project",
            models="users orders",
            select="tag:daily",
            exclude="tag:deprecated",
            full_refresh=True,
        )
        result = FlextMeltanoSingerCliTranslator.translate_dbt_run(params)
        tm.ok(result)
        command = result.value
        tm.that(
            command,
            eq=[
                "dbt",
                "run",
                "--projects-dir",
                "/path/to/dbt/project",
                "--models",
                "users orders",
                "--select",
                "tag:daily",
                "--exclude",
                "tag:deprecated",
                "--full-refresh",
            ],
        )


class TestFlextMeltanoSingerCliTranslatorExecuteCommand:
    """Test execute_singer_command method."""

    _MOCK_TARGET = (
        "flext_meltano.services.singer_translator.FlextInfraUtilitiesSubprocess.run_raw"
    )

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_success(self, mock_run_raw: MagicMock) -> None:
        """Test successful command execution."""
        mock_run_raw.return_value = r[m_infra.Infra.CommandOutput].ok(
            m_infra.Infra.CommandOutput(
                stdout="Success output",
                stderr="",
                exit_code=0,
            ),
        )
        result = FlextMeltanoSingerCliTranslator.execute_singer_command([
            "tap-postgres",
            "--config",
            "config.json",
        ])
        tm.ok(result)
        output = result.value
        tm.that(output["stdout"], eq="Success output")
        tm.that(output["stderr"], eq="")
        tm.that(output["returncode"], eq=0)
        mock_run_raw.assert_called_once()

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_with_input(self, mock_run_raw: MagicMock) -> None:
        """Test command execution with input data."""
        mock_run_raw.return_value = r[m_infra.Infra.CommandOutput].ok(
            m_infra.Infra.CommandOutput(stdout="Success", stderr="", exit_code=0),
        )
        input_data = '{"type": "RECORD", "stream": "users"}'
        result = FlextMeltanoSingerCliTranslator.execute_singer_command(
            ["target-postgres"],
            input_data=input_data,
        )
        tm.ok(result)
        call_args = mock_run_raw.call_args
        tm.that(call_args.kwargs["input_data"], eq=input_data.encode())

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_failure(self, mock_run_raw: MagicMock) -> None:
        """Test command execution failure (non-zero exit code)."""
        mock_run_raw.return_value = r[m_infra.Infra.CommandOutput].ok(
            m_infra.Infra.CommandOutput(
                stdout="",
                stderr="Error: Connection failed",
                exit_code=1,
            ),
        )
        result = FlextMeltanoSingerCliTranslator.execute_singer_command([
            "tap-postgres",
        ])
        tm.fail(result)
        tm.that(str(result.error), has="Connection failed")

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_timeout(self, mock_run_raw: MagicMock) -> None:
        """Test command execution timeout (run_raw returns failure)."""
        mock_run_raw.return_value = r[m_infra.Infra.CommandOutput].fail(
            "timeout 10s: tap-postgres",
        )
        result = FlextMeltanoSingerCliTranslator.execute_singer_command(
            ["tap-postgres"],
            timeout=10,
        )
        tm.fail(result)
        tm.that(str(result.error), has="timeout")

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_not_found(self, mock_run_raw: MagicMock) -> None:
        """Test command not found error (run_raw returns failure)."""
        mock_run_raw.return_value = r[m_infra.Infra.CommandOutput].fail(
            "execution error: tap-nonexistent not found",
        )
        result = FlextMeltanoSingerCliTranslator.execute_singer_command([
            "tap-nonexistent",
        ])
        tm.fail(result)
        tm.that(str(result.error), has="tap-nonexistent")
        tm.that(str(result.error), has="not found")

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_generic_exception(
        self,
        mock_run_raw: MagicMock,
    ) -> None:
        """Test generic exception handling (run_raw returns failure)."""
        mock_run_raw.return_value = r[m_infra.Infra.CommandOutput].fail(
            "execution error: Unexpected error",
        )
        result = FlextMeltanoSingerCliTranslator.execute_singer_command([
            "tap-postgres",
        ])
        tm.fail(result)
        tm.that(str(result.error), has="Unexpected error")
