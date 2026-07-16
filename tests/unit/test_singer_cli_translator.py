"""Behavioral tests for the Singer SDK CLI translator.

Exercises the public contract of the ``FlextMeltanoSingerCliTranslator`` mixin
as exposed through the ``meltano`` facade:

- Pydantic parameter models translate to deterministic CLI argument sequences.
- ``execute_singer_command`` returns an ``r[T]`` describing success/failure and
  the observable output mapping (``stdout``/``stderr``/``returncode``).

Only the genuine subprocess boundary (``u.Cli.run_raw``) is mocked; the
translator itself is always driven through its public API.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from flext_tests import r, tm

from flext_meltano import meltano
from tests import m

_MOCK_TARGET = "flext_meltano.services.singer_translator.u.Cli.run_raw"


class TestsFlextMeltanoSingerCliTranslator:
    """Behavioral tests for the Singer CLI translator public contract."""

    # ------------------------------------------------------------------ #
    # tap (source) translation
    # ------------------------------------------------------------------ #
    @pytest.mark.parametrize(
        ("params", "expected"),
        [
            pytest.param(
                m.Meltano.CliDataSourceParams(
                    source_name="tap-postgres",
                    discover=False,
                ),
                ["tap-postgres"],
                id="minimal",
            ),
            pytest.param(
                m.Meltano.CliDataSourceParams(
                    source_name="tap-postgres",
                    discover=True,
                ),
                ["tap-postgres", "--discover"],
                id="discover",
            ),
            pytest.param(
                m.Meltano.CliDataSourceParams(
                    source_name="tap-postgres",
                    config_file="/path/to/settings.json",
                    discover=False,
                ),
                ["tap-postgres", "--config", "/path/to/settings.json"],
                id="config",
            ),
            pytest.param(
                m.Meltano.CliDataSourceParams(
                    source_name="tap-postgres",
                    state_file="/path/to/state.json",
                    discover=False,
                ),
                ["tap-postgres", "--state", "/path/to/state.json"],
                id="state",
            ),
            pytest.param(
                # catalog_file drives BOTH --catalog and --properties.
                m.Meltano.CliDataSourceParams(
                    source_name="tap-postgres",
                    catalog_file="/path/to/catalog.json",
                    discover=False,
                ),
                [
                    "tap-postgres",
                    "--catalog",
                    "/path/to/catalog.json",
                    "--properties",
                    "/path/to/catalog.json",
                ],
                id="catalog-emits-catalog-and-properties",
            ),
            pytest.param(
                # discover short-circuits every other file argument.
                m.Meltano.CliDataSourceParams(
                    source_name="tap-postgres",
                    config_file="/path/to/settings.json",
                    catalog_file="/path/to/catalog.json",
                    discover=True,
                ),
                ["tap-postgres", "--discover"],
                id="discover-ignores-other-params",
            ),
        ],
    )
    def test_translate_tap_run_builds_expected_command(
        self,
        params: p.Meltano.CliDataSourceParams,
        expected: list[str],
    ) -> None:
        result = meltano.translate_tap_run(params)
        tm.ok(result)
        tm.that(result.value, eq=expected)

    def test_translate_tap_run_is_idempotent(self) -> None:
        params = m.Meltano.CliDataSourceParams(
            source_name="tap-postgres",
            config_file="/path/to/settings.json",
            discover=False,
        )
        first = meltano.translate_tap_run(params)
        second = meltano.translate_tap_run(params)
        tm.ok(first)
        tm.ok(second)
        tm.that(list(first.value), eq=list(second.value))

    # ------------------------------------------------------------------ #
    # target (sink) translation
    # ------------------------------------------------------------------ #
    @pytest.mark.parametrize(
        ("params", "expected"),
        [
            pytest.param(
                m.Meltano.CliDataSinkParams(sink_name="target-postgres"),
                ["target-postgres"],
                id="minimal",
            ),
            pytest.param(
                m.Meltano.CliDataSinkParams(
                    sink_name="target-postgres",
                    config_file="/path/to/settings.json",
                ),
                ["target-postgres", "--config", "/path/to/settings.json"],
                id="config",
            ),
            pytest.param(
                m.Meltano.CliDataSinkParams(
                    sink_name="target-postgres",
                    input_file="/path/to/input.jsonl",
                ),
                ["target-postgres", "--input", "/path/to/input.jsonl"],
                id="input",
            ),
            pytest.param(
                m.Meltano.CliDataSinkParams(
                    sink_name="target-postgres",
                    config_file="/path/to/settings.json",
                    input_file="/path/to/input.jsonl",
                ),
                [
                    "target-postgres",
                    "--config",
                    "/path/to/settings.json",
                    "--input",
                    "/path/to/input.jsonl",
                ],
                id="all",
            ),
        ],
    )
    def test_translate_target_run_builds_expected_command(
        self,
        params: p.Meltano.CliDataSinkParams,
        expected: list[str],
    ) -> None:
        result = meltano.translate_target_run(params)
        tm.ok(result)
        tm.that(result.value, eq=expected)

    # ------------------------------------------------------------------ #
    # pipeline translation (source + sink pair)
    # ------------------------------------------------------------------ #
    @pytest.mark.parametrize(
        ("params", "expected_source", "expected_sink"),
        [
            pytest.param(
                m.Meltano.CliPipelineParams(
                    source_name="tap-postgres",
                    sink_name="target-postgres",
                ),
                ["tap-postgres"],
                ["target-postgres"],
                id="minimal",
            ),
            pytest.param(
                m.Meltano.CliPipelineParams(
                    source_name="tap-postgres",
                    sink_name="target-postgres",
                    source_config="/path/to/tap-settings.json",
                ),
                ["tap-postgres", "--config", "/path/to/tap-settings.json"],
                ["target-postgres"],
                id="source-config",
            ),
            pytest.param(
                m.Meltano.CliPipelineParams(
                    source_name="tap-postgres",
                    sink_name="target-postgres",
                    sink_config="/path/to/target-settings.json",
                ),
                ["tap-postgres"],
                ["target-postgres", "--config", "/path/to/target-settings.json"],
                id="sink-config",
            ),
            pytest.param(
                m.Meltano.CliPipelineParams(
                    source_name="tap-postgres",
                    sink_name="target-postgres",
                    catalog_file="/path/to/catalog.json",
                ),
                ["tap-postgres", "--catalog", "/path/to/catalog.json"],
                ["target-postgres"],
                id="catalog",
            ),
            pytest.param(
                m.Meltano.CliPipelineParams(
                    source_name="tap-postgres",
                    sink_name="target-postgres",
                    state_file="/path/to/state.json",
                ),
                ["tap-postgres", "--state", "/path/to/state.json"],
                ["target-postgres"],
                id="state",
            ),
            pytest.param(
                m.Meltano.CliPipelineParams(
                    source_name="tap-postgres",
                    sink_name="target-postgres",
                    source_config="/path/to/tap-settings.json",
                    sink_config="/path/to/target-settings.json",
                    catalog_file="/path/to/catalog.json",
                    state_file="/path/to/state.json",
                ),
                [
                    "tap-postgres",
                    "--config",
                    "/path/to/tap-settings.json",
                    "--catalog",
                    "/path/to/catalog.json",
                    "--state",
                    "/path/to/state.json",
                ],
                ["target-postgres", "--config", "/path/to/target-settings.json"],
                id="all",
            ),
        ],
    )
    def test_translate_pipeline_run_builds_source_and_sink_commands(
        self,
        params: p.Meltano.CliPipelineParams,
        expected_source: list[str],
        expected_sink: list[str],
    ) -> None:
        result = meltano.translate_pipeline_run(params)
        tm.ok(result)
        source_command, sink_command = result.value
        tm.that(source_command, eq=expected_source)
        tm.that(sink_command, eq=expected_sink)

    # ------------------------------------------------------------------ #
    # dbt translation
    # ------------------------------------------------------------------ #
    @pytest.mark.parametrize(
        ("params", "expected"),
        [
            pytest.param(
                m.Meltano.CliTransformationParams(project_dir="/dbt/project"),
                ["dbt", "run", "--projects-dir", "/dbt/project"],
                id="minimal",
            ),
            pytest.param(
                m.Meltano.CliTransformationParams(
                    project_dir="/dbt/project",
                    models="users orders",
                ),
                [
                    "dbt",
                    "run",
                    "--projects-dir",
                    "/dbt/project",
                    "--models",
                    "users orders",
                ],
                id="models",
            ),
            pytest.param(
                m.Meltano.CliTransformationParams(
                    project_dir="/dbt/project",
                    select="tag:daily",
                ),
                [
                    "dbt",
                    "run",
                    "--projects-dir",
                    "/dbt/project",
                    "--select",
                    "tag:daily",
                ],
                id="select",
            ),
            pytest.param(
                m.Meltano.CliTransformationParams(
                    project_dir="/dbt/project",
                    exclude="tag:deprecated",
                ),
                [
                    "dbt",
                    "run",
                    "--projects-dir",
                    "/dbt/project",
                    "--exclude",
                    "tag:deprecated",
                ],
                id="exclude",
            ),
            pytest.param(
                m.Meltano.CliTransformationParams(
                    project_dir="/dbt/project",
                    full_refresh=True,
                ),
                [
                    "dbt",
                    "run",
                    "--projects-dir",
                    "/dbt/project",
                    "--full-refresh",
                ],
                id="full-refresh",
            ),
            pytest.param(
                m.Meltano.CliTransformationParams(
                    project_dir="/dbt/project",
                    models="users orders",
                    select="tag:daily",
                    exclude="tag:deprecated",
                    full_refresh=True,
                ),
                [
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
                id="all",
            ),
        ],
    )
    def test_translate_dbt_run_builds_expected_command(
        self,
        params: p.Meltano.CliTransformationParams,
        expected: list[str],
    ) -> None:
        result = meltano.translate_dbt_run(params)
        tm.ok(result)
        tm.that(result.value, eq=expected)

    # ------------------------------------------------------------------ #
    # execute_singer_command — observable r[T] contract at the subprocess
    # boundary (u.Cli.run_raw is the genuine external collaborator).
    # ------------------------------------------------------------------ #
    def test_execute_singer_command_rejects_empty_command(self) -> None:
        result = meltano.execute_singer_command([])
        tm.fail(result)
        tm.that(str(result.error), has="non-empty")

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_success_returns_output_mapping(
        self,
        mock_run_raw: MagicMock,
    ) -> None:
        mock_run_raw.return_value = r[p.Cli.CommandOutput].ok(
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

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_encodes_input_for_subprocess(
        self,
        mock_run_raw: MagicMock,
    ) -> None:
        mock_run_raw.return_value = r[p.Cli.CommandOutput].ok(
            m.Cli.CommandOutput(stdout="Success", stderr="", exit_code=0),
        )
        input_data = '{"type": "RECORD", "stream": "users"}'
        result = meltano.execute_singer_command(
            ["target-postgres"],
            input_data=input_data,
        )
        tm.ok(result)
        # Contract at the process boundary: text input is handed to the
        # subprocess as encoded bytes, and the command is passed through.
        tm.that(mock_run_raw.call_args.kwargs["input_data"], eq=input_data.encode())
        tm.that(list(mock_run_raw.call_args.args[0]), eq=["target-postgres"])

    @patch(_MOCK_TARGET)
    def test_execute_singer_command_nonzero_exit_is_failure(
        self,
        mock_run_raw: MagicMock,
    ) -> None:
        mock_run_raw.return_value = r[p.Cli.CommandOutput].ok(
            m.Cli.CommandOutput(
                stdout="",
                stderr="Error: Connection failed",
                exit_code=1,
            ),
        )
        result = meltano.execute_singer_command(["tap-postgres"])
        tm.fail(result)
        tm.that(str(result.error), has="Connection failed")

    @pytest.mark.parametrize(
        ("run_raw_error", "expected_fragments"),
        [
            pytest.param(
                "timeout 10s: tap-postgres",
                ["timeout"],
                id="timeout",
            ),
            pytest.param(
                "execution error: tap-nonexistent not found",
                ["tap-nonexistent", "not found"],
                id="not-found",
            ),
            pytest.param(
                "execution error: Unexpected error",
                ["Unexpected error"],
                id="generic-error",
            ),
        ],
    )
    @patch(_MOCK_TARGET)
    def test_execute_singer_command_propagates_boundary_failure(
        self,
        mock_run_raw: MagicMock,
        run_raw_error: str,
        expected_fragments: list[str],
    ) -> None:
        mock_run_raw.return_value = r[p.Cli.CommandOutput].fail(run_raw_error)
        result = meltano.execute_singer_command(["tap-postgres"], timeout=10)
        tm.fail(result)
        for fragment in expected_fragments:
            tm.that(str(result.error), has=fragment)


__all__: list[str] = ["TestsFlextMeltanoSingerCliTranslator"]
