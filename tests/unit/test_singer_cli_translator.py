"""Comprehensive tests for meltano module.

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

from flext_tests import r, tm

from flext_meltano import meltano
from tests.models import m


class TestsFlextMeltanoSingerCliTranslator:
    """Behavioral tests for the Singer CLI translator."""

    _MOCK_TARGET = "flext_meltano.services.singer_translator.u.Cli.run_raw"

    def test_translate_tap_run_minimal(self) -> None:
        result = meltano.translate_tap_run(
            m.Meltano.CliDataSourceParams(
                source_name="tap-postgres",
                discover=False,
            ),
        )
        tm.ok(result)
        tm.that(result.value, eq=["tap-postgres"])

    def test_translate_tap_run_discover_mode(self) -> None:
        result = meltano.translate_tap_run(
            m.Meltano.CliDataSourceParams(
                source_name="tap-postgres",
                discover=True,
            ),
        )
        tm.ok(result)
        tm.that(result.value, eq=["tap-postgres", "--discover"])

    def test_translate_tap_run_with_config(self) -> None:
        result = meltano.translate_tap_run(
            m.Meltano.CliDataSourceParams(
                source_name="tap-postgres",
                config_file="/path/to/settings.json",
                discover=False,
            ),
        )
        tm.ok(result)
        tm.that(result.value, eq=["tap-postgres", "--config", "/path/to/settings.json"])

    def test_translate_tap_run_with_catalog(self) -> None:
        result = meltano.translate_tap_run(
            m.Meltano.CliDataSourceParams(
                source_name="tap-postgres",
                catalog_file="/path/to/catalog.json",
                discover=False,
            ),
        )
        tm.ok(result)
        tm.that(result.value, has="--catalog")

    def test_translate_tap_run_with_state(self) -> None:
        result = meltano.translate_tap_run(
            m.Meltano.CliDataSourceParams(
                source_name="tap-postgres",
                state_file="/path/to/state.json",
                discover=False,
            ),
        )
        tm.ok(result)
        tm.that(result.value, eq=["tap-postgres", "--state", "/path/to/state.json"])

    def test_translate_tap_run_with_all_parameters(self) -> None:
        result = meltano.translate_tap_run(
            m.Meltano.CliDataSourceParams(
                source_name="tap-postgres",
                config_file="/path/to/settings.json",
                catalog_file="/path/to/catalog.json",
                state_file="/path/to/state.json",
                discover=False,
            ),
        )
        tm.ok(result)
        tm.that(result.value, has="tap-postgres")
        tm.that(result.value, has="--config")
        tm.that(result.value, has="--catalog")
        tm.that(result.value, has="--state")

    def test_translate_tap_run_discover_ignores_other_params(self) -> None:
        result = meltano.translate_tap_run(
            m.Meltano.CliDataSourceParams(
                source_name="tap-postgres",
                config_file="/path/to/settings.json",
                catalog_file="/path/to/catalog.json",
                discover=True,
            ),
        )
        tm.ok(result)
        tm.that(result.value, eq=["tap-postgres", "--discover"])

    def test_translate_target_run_minimal(self) -> None:
        result = meltano.translate_target_run(
            m.Meltano.CliDataSinkParams(sink_name="target-postgres"),
        )
        tm.ok(result)
        tm.that(result.value, eq=["target-postgres"])

    def test_translate_target_run_with_config(self) -> None:
        result = meltano.translate_target_run(
            m.Meltano.CliDataSinkParams(
                sink_name="target-postgres",
                config_file="/path/to/settings.json",
            ),
        )
        tm.ok(result)
        tm.that(
            result.value,
            eq=["target-postgres", "--config", "/path/to/settings.json"],
        )

    def test_translate_target_run_with_input(self) -> None:
        result = meltano.translate_target_run(
            m.Meltano.CliDataSinkParams(
                sink_name="target-postgres",
                input_file="/path/to/input.jsonl",
            ),
        )
        tm.ok(result)
        tm.that(result.value, eq=["target-postgres", "--input", "/path/to/input.jsonl"])

    def test_translate_target_run_with_all_parameters(self) -> None:
        result = meltano.translate_target_run(
            m.Meltano.CliDataSinkParams(
                sink_name="target-postgres",
                config_file="/path/to/settings.json",
                input_file="/path/to/input.jsonl",
            ),
        )
        tm.ok(result)
        tm.that(
            result.value,
            eq=[
                "target-postgres",
                "--config",
                "/path/to/settings.json",
                "--input",
                "/path/to/input.jsonl",
            ],
        )

    def test_translate_pipeline_run_minimal(self) -> None:
        result = meltano.translate_pipeline_run(
            m.Meltano.CliPipelineParams(
                source_name="tap-postgres",
                sink_name="target-postgres",
            ),
        )
        tm.ok(result)
        source_command, sink_command = result.value
        tm.that(source_command, eq=["tap-postgres"])
        tm.that(sink_command, eq=["target-postgres"])

    def test_translate_pipeline_run_with_source_config(self) -> None:
        result = meltano.translate_pipeline_run(
            m.Meltano.CliPipelineParams(
                source_name="tap-postgres",
                sink_name="target-postgres",
                source_config="/path/to/tap-settings.json",
            ),
        )
        tm.ok(result)
        source_command, sink_command = result.value
        tm.that(
            source_command,
            eq=["tap-postgres", "--config", "/path/to/tap-settings.json"],
        )
        tm.that(sink_command, eq=["target-postgres"])

    def test_translate_pipeline_run_with_sink_config(self) -> None:
        result = meltano.translate_pipeline_run(
            m.Meltano.CliPipelineParams(
                source_name="tap-postgres",
                sink_name="target-postgres",
                sink_config="/path/to/target-settings.json",
            ),
        )
        tm.ok(result)
        source_command, sink_command = result.value
        tm.that(source_command, eq=["tap-postgres"])
        tm.that(
            sink_command,
            eq=["target-postgres", "--config", "/path/to/target-settings.json"],
        )

    def test_translate_pipeline_run_with_catalog(self) -> None:
        result = meltano.translate_pipeline_run(
            m.Meltano.CliPipelineParams(
                source_name="tap-postgres",
                sink_name="target-postgres",
                catalog_file="/path/to/catalog.json",
            ),
        )
        tm.ok(result)
        source_command, sink_command = result.value
        tm.that(
            source_command,
            eq=["tap-postgres", "--catalog", "/path/to/catalog.json"],
        )
        tm.that(sink_command, eq=["target-postgres"])

    def test_translate_pipeline_run_with_state(self) -> None:
        result = meltano.translate_pipeline_run(
            m.Meltano.CliPipelineParams(
                source_name="tap-postgres",
                sink_name="target-postgres",
                state_file="/path/to/state.json",
            ),
        )
        tm.ok(result)
        source_command, sink_command = result.value
        tm.that(source_command, eq=["tap-postgres", "--state", "/path/to/state.json"])
        tm.that(sink_command, eq=["target-postgres"])

    def test_translate_pipeline_run_with_all_parameters(self) -> None:
        result = meltano.translate_pipeline_run(
            m.Meltano.CliPipelineParams(
                source_name="tap-postgres",
                sink_name="target-postgres",
                source_config="/path/to/tap-settings.json",
                sink_config="/path/to/target-settings.json",
                catalog_file="/path/to/catalog.json",
                state_file="/path/to/state.json",
            ),
        )
        tm.ok(result)
        source_command, sink_command = result.value
        tm.that(
            source_command,
            eq=[
                "tap-postgres",
                "--config",
                "/path/to/tap-settings.json",
                "--catalog",
                "/path/to/catalog.json",
                "--state",
                "/path/to/state.json",
            ],
        )
        tm.that(
            sink_command,
            eq=["target-postgres", "--config", "/path/to/target-settings.json"],
        )

    def test_translate_dbt_run_minimal(self) -> None:
        result = meltano.translate_dbt_run(
            m.Meltano.CliTransformationParams(project_dir="/dbt/project"),
        )
        tm.ok(result)
        tm.that(result.value, eq=["dbt", "run", "--projects-dir", "/dbt/project"])

    def test_translate_dbt_run_with_models(self) -> None:
        result = meltano.translate_dbt_run(
            m.Meltano.CliTransformationParams(
                project_dir="/dbt/project",
                models="users orders",
            ),
        )
        tm.ok(result)
        tm.that(
            result.value,
            eq=[
                "dbt",
                "run",
                "--projects-dir",
                "/dbt/project",
                "--models",
                "users orders",
            ],
        )

    def test_translate_dbt_run_with_select(self) -> None:
        result = meltano.translate_dbt_run(
            m.Meltano.CliTransformationParams(
                project_dir="/dbt/project",
                select="tag:daily",
            ),
        )
        tm.ok(result)
        tm.that(
            result.value,
            eq=[
                "dbt",
                "run",
                "--projects-dir",
                "/dbt/project",
                "--select",
                "tag:daily",
            ],
        )

    def test_translate_dbt_run_with_exclude(self) -> None:
        result = meltano.translate_dbt_run(
            m.Meltano.CliTransformationParams(
                project_dir="/dbt/project",
                exclude="tag:deprecated",
            ),
        )
        tm.ok(result)
        tm.that(
            result.value,
            eq=[
                "dbt",
                "run",
                "--projects-dir",
                "/dbt/project",
                "--exclude",
                "tag:deprecated",
            ],
        )

    def test_translate_dbt_run_with_full_refresh(self) -> None:
        result = meltano.translate_dbt_run(
            m.Meltano.CliTransformationParams(
                project_dir="/dbt/project",
                full_refresh=True,
            ),
        )
        tm.ok(result)
        tm.that(
            result.value,
            eq=[
                "dbt",
                "run",
                "--projects-dir",
                "/dbt/project",
                "--full-refresh",
            ],
        )

    def test_translate_dbt_run_with_all_parameters(self) -> None:
        result = meltano.translate_dbt_run(
            m.Meltano.CliTransformationParams(
                project_dir="/dbt/project",
                models="users orders",
                select="tag:daily",
                exclude="tag:deprecated",
                full_refresh=True,
            ),
        )
        tm.ok(result)
        tm.that(
            result.value,
            eq=[
                "dbt",
                "run",
                "--projects-dir",
                "/dbt/project",
                "--models",
                "users orders",
                "--select",
                "tag:daily",
                "--exclude",
                "tag:deprecated",
                "--full-refresh",
            ],
        )

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_success(self, mock_run_raw: MagicMock) -> None:
        mock_run_raw.return_value = r[m.Cli.CommandOutput].ok(
            m.Cli.CommandOutput(
                stdout="Success output",
                stderr="",
                exit_code=0,
            ),
        )
        result = meltano.execute_singer_command(
            ["tap-postgres", "--config", "settings.json"],
        )
        tm.ok(result)
        output = result.value
        tm.that(output["stdout"], eq="Success output")
        tm.that(output["stderr"], eq="")
        tm.that(output["returncode"], eq=0)
        mock_run_raw.assert_called_once()

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_with_input(self, mock_run_raw: MagicMock) -> None:
        mock_run_raw.return_value = r[m.Cli.CommandOutput].ok(
            m.Cli.CommandOutput(stdout="Success", stderr="", exit_code=0),
        )
        input_data = '{"type": "RECORD", "stream": "users"}'
        result = meltano.execute_singer_command(
            ["target-postgres"],
            input_data=input_data,
        )
        tm.ok(result)
        tm.that(mock_run_raw.call_args.kwargs["input_data"], eq=input_data.encode())

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_failure(self, mock_run_raw: MagicMock) -> None:
        mock_run_raw.return_value = r[m.Cli.CommandOutput].ok(
            m.Cli.CommandOutput(
                stdout="",
                stderr="Error: Connection failed",
                exit_code=1,
            ),
        )
        result = meltano.execute_singer_command([
            "tap-postgres",
        ])
        tm.fail(result)
        tm.that(str(result.error), has="Connection failed")

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_timeout(self, mock_run_raw: MagicMock) -> None:
        mock_run_raw.return_value = r[m.Cli.CommandOutput].fail(
            "timeout 10s: tap-postgres",
        )
        result = meltano.execute_singer_command(
            ["tap-postgres"],
            timeout=10,
        )
        tm.fail(result)
        tm.that(str(result.error), has="timeout")

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_not_found(self, mock_run_raw: MagicMock) -> None:
        mock_run_raw.return_value = r[m.Cli.CommandOutput].fail(
            "execution error: tap-nonexistent not found",
        )
        result = meltano.execute_singer_command(
            ["tap-nonexistent"],
        )
        tm.fail(result)
        tm.that(str(result.error), has="tap-nonexistent")
        tm.that(str(result.error), has="not found")

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_generic_exception(
        self,
        mock_run_raw: MagicMock,
    ) -> None:
        mock_run_raw.return_value = r[m.Cli.CommandOutput].fail(
            "execution error: Unexpected error",
        )
        result = meltano.execute_singer_command([
            "tap-postgres",
        ])
        tm.fail(result)
        tm.that(str(result.error), has="Unexpected error")
