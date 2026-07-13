"""Real-execution tests for the Meltano pipeline CLI commands."""

from __future__ import annotations

import multiprocessing
import os
import time
from multiprocessing.process import BaseProcess
from pathlib import Path

import pytest
from flext_tests import tm

from flext_cli import cli as flext_cli
from flext_meltano.cli import FlextMeltanoCli
from tests import c, m, t, u


class TestFlextMeltanoPipelineCliManagers:
    """Exercise pipeline lifecycle commands through the model-driven CLI."""

    @pytest.fixture
    def runner(self) -> t.Cli.TyperRunner:
        """Provide a fresh CliRunner for each test."""
        runner_result = flext_cli.create_cli_runner()
        tm.ok(runner_result)
        return runner_result.value

    @pytest.fixture
    def app(self) -> t.Cli.CliApp:
        """Provide the compiled Typer application under test."""
        return FlextMeltanoCli()._app

    @staticmethod
    def _activate_pipelines_root(tmp_path: Path) -> str | None:
        previous_root = os.environ.get(c.Meltano.CLI_DEFAULT_PIPELINES_ROOT_ENV)
        os.environ[c.Meltano.CLI_DEFAULT_PIPELINES_ROOT_ENV] = str(
            tmp_path / "pipelines"
        )
        return previous_root

    @staticmethod
    def _restore_pipelines_root(previous_root: str | None) -> None:
        if previous_root is None:
            os.environ.pop(c.Meltano.CLI_DEFAULT_PIPELINES_ROOT_ENV, None)
            return
        os.environ[c.Meltano.CLI_DEFAULT_PIPELINES_ROOT_ENV] = previous_root

    @staticmethod
    def _spawn_sleep_process() -> BaseProcess:
        process = multiprocessing.get_context("spawn").Process(
            target=time.sleep,
            args=(30,),
        )
        process.start()
        deadline = time.monotonic() + 5
        while not process.is_alive() and time.monotonic() < deadline:
            time.sleep(0.01)
        return process

    @staticmethod
    def _stop_process(process: BaseProcess) -> None:
        if not process.is_alive():
            return
        process.terminate()
        process.join(timeout=5)
        if process.is_alive():
            process.kill()
            process.join(timeout=5)

    def test_pipeline_help_request_lists_subcommands(
        self,
        runner: t.Cli.TyperRunner,
        app: t.Cli.CliApp,
    ) -> None:
        """Pipeline help exposes the model-driven subcommands."""
        result = runner.invoke(
            app,
            [
                c.Meltano.CliCommand.PIPELINE,
                c.Meltano.CMD_HELP_OPTION,
            ],
        )

        tm.that(result.exit_code, eq=0)
        tm.that(result.output, has=c.Meltano.PipelineCommand.CREATE)
        tm.that(result.output, has=c.Meltano.PipelineCommand.RUN)
        tm.that(result.output, has=c.Meltano.PipelineCommand.LIST)
        tm.that(result.output, has=c.Meltano.PipelineCommand.STATUS)
        tm.that(result.output, has=c.Meltano.PipelineCommand.STOP)
        tm.that(result.output, has=c.Meltano.PipelineCommand.DELETE)

    def test_pipeline_create_list_run_and_delete_use_real_storage(
        self,
        runner: t.Cli.TyperRunner,
        app: t.Cli.CliApp,
        tmp_path: Path,
    ) -> None:
        """Pipeline lifecycle commands persist and execute through real helpers."""
        previous_root = self._activate_pipelines_root(tmp_path)
        pipeline_name = "daily-pipeline"
        config_json_result = u.Cli.json_dumps({"command": ["help"]})
        config_path = (
            tmp_path
            / "pipelines"
            / pipeline_name
            / c.Meltano.CLI_DEFAULT_PIPELINE_CONFIG_FILE
        )

        try:
            tm.ok(config_json_result)
            create_result = runner.invoke(
                app,
                [
                    c.Meltano.CliCommand.PIPELINE,
                    c.Meltano.PipelineCommand.CREATE,
                    "--pipeline-name",
                    pipeline_name,
                    "--config-json",
                    config_json_result.value,
                ],
            )
            list_result = runner.invoke(
                app,
                [
                    c.Meltano.CliCommand.PIPELINE,
                    c.Meltano.PipelineCommand.LIST,
                ],
            )
            status_result = runner.invoke(
                app,
                [
                    c.Meltano.CliCommand.PIPELINE,
                    c.Meltano.PipelineCommand.STATUS,
                    "--pipeline-name",
                    pipeline_name,
                ],
            )
            run_result = runner.invoke(
                app,
                [
                    c.Meltano.CliCommand.PIPELINE,
                    c.Meltano.PipelineCommand.RUN,
                    "--pipeline-name",
                    pipeline_name,
                ],
            )
            stored_result = flext_cli.read_json_file(config_path)
            delete_result = runner.invoke(
                app,
                [
                    c.Meltano.CliCommand.PIPELINE,
                    c.Meltano.PipelineCommand.DELETE,
                    "--pipeline-name",
                    pipeline_name,
                ],
            )
        finally:
            self._restore_pipelines_root(previous_root)

        tm.that(create_result.exit_code, eq=0)
        tm.that(list_result.exit_code, eq=0)
        tm.that(status_result.exit_code, eq=0)
        tm.that(run_result.exit_code, eq=0)
        tm.ok(stored_result)
        tm.that(delete_result.exit_code, eq=0)

        stored_payload = m.Meltano.ConfigMappingPayload.model_validate({
            "values": stored_result.value
        })

        tm.that(list_result.output, has=pipeline_name)
        tm.that(status_result.output, has="stopped")
        tm.that(run_result.output.lower(), has="usage:")
        tm.that(stored_payload.values, eq={"command": ["help"]})
        tm.that((tmp_path / "pipelines" / pipeline_name).exists(), eq=False)

    def test_pipeline_create_requires_runtime_configuration(
        self,
        runner: t.Cli.TyperRunner,
        app: t.Cli.CliApp,
        tmp_path: Path,
    ) -> None:
        """Pipeline creation without JSON config fails on the real handler path."""
        previous_root = self._activate_pipelines_root(tmp_path)

        try:
            result = runner.invoke(
                app,
                [
                    c.Meltano.CliCommand.PIPELINE,
                    c.Meltano.PipelineCommand.CREATE,
                    "--pipeline-name",
                    "missing-config",
                ],
            )
        finally:
            self._restore_pipelines_root(previous_root)

        tm.that(result.exit_code, eq=1)
        tm.that(result.output, has="not configured")

    def test_pipeline_status_and_stop_use_real_pid_files(
        self,
        runner: t.Cli.TyperRunner,
        app: t.Cli.CliApp,
        tmp_path: Path,
    ) -> None:
        """Status and stop commands inspect a real background process pid file."""
        previous_root = self._activate_pipelines_root(tmp_path)
        pipeline_name = "status-pipeline"
        config_json_result = u.Cli.json_dumps({"command": ["help"]})
        pid_path = (
            tmp_path
            / "pipelines"
            / pipeline_name
            / c.Meltano.CLI_DEFAULT_PIPELINE_PID_FILE
        )
        process = self._spawn_sleep_process()

        try:
            tm.ok(config_json_result)
            create_result = runner.invoke(
                app,
                [
                    c.Meltano.CliCommand.PIPELINE,
                    c.Meltano.PipelineCommand.CREATE,
                    "--pipeline-name",
                    pipeline_name,
                    "--config-json",
                    config_json_result.value,
                ],
            )
            tm.that(create_result.exit_code, eq=0)

            ensure_pid_dir_result = flext_cli.ensure_dir(pid_path.parent)
            tm.ok(ensure_pid_dir_result)
            write_pid_result = u.Cli.files_write_text(pid_path, str(process.pid))
            tm.ok(write_pid_result)

            running_result = runner.invoke(
                app,
                [
                    c.Meltano.CliCommand.PIPELINE,
                    c.Meltano.PipelineCommand.STATUS,
                    "--pipeline-name",
                    pipeline_name,
                ],
            )
            stop_result = runner.invoke(
                app,
                [
                    c.Meltano.CliCommand.PIPELINE,
                    c.Meltano.PipelineCommand.STOP,
                    "--pipeline-name",
                    pipeline_name,
                ],
            )
        finally:
            self._stop_process(process)
            self._restore_pipelines_root(previous_root)

        tm.that(running_result.exit_code, eq=0)
        tm.that(stop_result.exit_code, eq=0)
        tm.that(running_result.output, has="running")
        tm.that(stop_result.output, has="stopped")
        tm.that(pid_path.exists(), eq=False)
