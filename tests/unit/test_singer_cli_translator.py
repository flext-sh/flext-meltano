"""Behavioral tests for the Singer SDK CLI translator.

Exercises the public contract of the ``FlextMeltanoSingerCliTranslator`` mixin
as exposed through the ``meltano`` facade:

- Pydantic parameter models translate to deterministic CLI argument sequences.
- ``execute_singer_command`` returns an ``r[T]`` describing success/failure and
  the observable output mapping (``stdout``/``stderr``/``returncode``).

Every subprocess test runs real operating-system processes (``printf``,
``cat``, ``sh``, ``sleep``) so the boundary behavior is genuine.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import time

import pytest

from flext_meltano import meltano
from flext_tests import tm
from tests import m


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
                    source_name="tap-postgres", discover=False
                ),
                ["tap-postgres"],
                id="minimal",
            ),
            pytest.param(
                m.Meltano.CliDataSourceParams(
                    source_name="tap-postgres", discover=True
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
        self, params: m.Meltano.CliDataSourceParams, expected: list[str]
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
                    sink_name="target-postgres", config_file="/path/to/settings.json"
                ),
                ["target-postgres", "--config", "/path/to/settings.json"],
                id="config",
            ),
            pytest.param(
                m.Meltano.CliDataSinkParams(
                    sink_name="target-postgres", input_file="/path/to/input.jsonl"
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
        self, params: m.Meltano.CliDataSinkParams, expected: list[str]
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
                    source_name="tap-postgres", sink_name="target-postgres"
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
        params: m.Meltano.CliPipelineParams,
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
                    project_dir="/dbt/project", models="users orders"
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
                    project_dir="/dbt/project", select="tag:daily"
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
                    project_dir="/dbt/project", exclude="tag:deprecated"
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
                    project_dir="/dbt/project", full_refresh=True
                ),
                ["dbt", "run", "--projects-dir", "/dbt/project", "--full-refresh"],
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
        self, params: m.Meltano.CliTransformationParams, expected: list[str]
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

    def test_execute_singer_command_success_returns_output_mapping(self) -> None:
        result = meltano.execute_singer_command(["printf", "Success output"])
        tm.ok(result)
        output = result.value
        tm.that(output["stdout"], eq="Success output")
        tm.that(output["stderr"], eq="")
        tm.that(output["returncode"], eq=0)

    def test_execute_singer_command_encodes_input_for_subprocess(self) -> None:
        input_data = '{"type": "RECORD", "stream": "users"}'
        result = meltano.execute_singer_command(["cat"], input_data=input_data)
        tm.ok(result)
        # Contract at the process boundary: text input is handed to the real
        # subprocess as encoded bytes and echoed back on stdout by ``cat``.
        tm.that(result.value["stdout"], eq=input_data)

    def test_execute_singer_command_nonzero_exit_is_failure(self) -> None:
        result = meltano.execute_singer_command([
            "sh",
            "-c",
            "echo Connection failed >&2; exit 1",
        ])
        tm.fail(result)
        tm.that(str(result.error), has="Connection failed")

    def test_execute_singer_command_missing_binary_fails_loud(self) -> None:
        """A missing binary escapes as FileNotFoundError — no silent fallback."""
        with pytest.raises(FileNotFoundError, match="definitely-not-a-real-tap"):
            meltano.execute_singer_command(["definitely-not-a-real-tap"])

    def test_execute_singer_command_timeout_interrupts_subprocess(self) -> None:
        started = time.monotonic()
        result = meltano.execute_singer_command(["sleep", "5"], timeout=1)
        elapsed = time.monotonic() - started
        tm.fail(result)
        tm.that(result.error, none=False)
        # The boundary timeout genuinely interrupts the subprocess: the call
        # returns promptly instead of waiting out the command's full runtime.
        tm.that(elapsed < 4, eq=True)


__all__: list[str] = ["TestsFlextMeltanoSingerCliTranslator"]
