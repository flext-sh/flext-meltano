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
from tests import c, m, u


class TestFlextMeltanoPipelineCliManagers:
    """Exercise pipeline lifecycle commands through the model-driven CLI."""

    @pytest.fixture
    def meltano_cli(self) -> FlextMeltanoCli:
        """Provide the public CLI facade used by every command scenario."""
        # mro-wkii.17 (codex): tests exercise the public Result boundary, never
        # the private framework runner or application object.
        return FlextMeltanoCli()

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
        meltano_cli: FlextMeltanoCli,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Pipeline help exposes the model-driven subcommands."""
        result = meltano_cli.run([
            c.Meltano.CliCommand.PIPELINE,
            c.Meltano.CMD_HELP_OPTION,
        ])
        output = capsys.readouterr().out

        tm.ok(result)
        tm.that(output, has=c.Meltano.PipelineCommand.CREATE)
        tm.that(output, has=c.Meltano.PipelineCommand.RUN)
        tm.that(output, has=c.Meltano.PipelineCommand.LIST)
        tm.that(output, has=c.Meltano.PipelineCommand.STATUS)
        tm.that(output, has=c.Meltano.PipelineCommand.STOP)
        tm.that(output, has=c.Meltano.PipelineCommand.DELETE)

    def test_pipeline_create_list_run_and_delete_use_real_storage(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
    ) -> None:
        """Pipeline lifecycle commands persist and execute through real helpers."""
        previous_root = self._activate_pipelines_root(tmp_path)
        meltano_cli = FlextMeltanoCli()
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
            create_result = meltano_cli.run([
                c.Meltano.CliCommand.PIPELINE,
                c.Meltano.PipelineCommand.CREATE,
                "--pipeline-name",
                pipeline_name,
                "--config-json",
                config_json_result.value,
            ])
            capsys.readouterr()
            list_result = meltano_cli.run([
                c.Meltano.CliCommand.PIPELINE,
                c.Meltano.PipelineCommand.LIST,
            ])
            list_output = capsys.readouterr().out
            status_result = meltano_cli.run([
                c.Meltano.CliCommand.PIPELINE,
                c.Meltano.PipelineCommand.STATUS,
                "--pipeline-name",
                pipeline_name,
            ])
            status_output = capsys.readouterr().out
            run_result = meltano_cli.run([
                c.Meltano.CliCommand.PIPELINE,
                c.Meltano.PipelineCommand.RUN,
                "--pipeline-name",
                pipeline_name,
            ])
            run_output = capsys.readouterr().out
            stored_result = flext_cli.json_read_file(config_path)
            delete_result = meltano_cli.run([
                c.Meltano.CliCommand.PIPELINE,
                c.Meltano.PipelineCommand.DELETE,
                "--pipeline-name",
                pipeline_name,
            ])
            capsys.readouterr()
        finally:
            self._restore_pipelines_root(previous_root)

        tm.ok(create_result)
        tm.ok(list_result)
        tm.ok(status_result)
        tm.ok(run_result)
        tm.ok(stored_result)
        tm.ok(delete_result)

        stored_payload = m.Meltano.ConfigMappingPayload.model_validate({
            "values": stored_result.value
        })

        tm.that(list_output, has=pipeline_name)
        tm.that(status_output, has="stopped")
        tm.that(run_output.lower(), has="usage:")
        tm.that(stored_payload.values, eq={"command": ["help"]})
        tm.that((tmp_path / "pipelines" / pipeline_name).exists(), eq=False)

    def test_pipeline_create_requires_runtime_configuration(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
    ) -> None:
        """Pipeline creation without JSON config fails on the real handler path."""
        previous_root = self._activate_pipelines_root(tmp_path)
        meltano_cli = FlextMeltanoCli()

        try:
            result = meltano_cli.run([
                c.Meltano.CliCommand.PIPELINE,
                c.Meltano.PipelineCommand.CREATE,
                "--pipeline-name",
                "missing-config",
            ])
            output = capsys.readouterr().out
        finally:
            self._restore_pipelines_root(previous_root)

        tm.fail(result, has="not configured")
        tm.that(output, has="not configured")

    def test_pipeline_status_and_stop_use_real_pid_files(
        self,
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
    ) -> None:
        """Status and stop commands inspect a real background process pid file."""
        previous_root = self._activate_pipelines_root(tmp_path)
        meltano_cli = FlextMeltanoCli()
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
            create_result = meltano_cli.run([
                c.Meltano.CliCommand.PIPELINE,
                c.Meltano.PipelineCommand.CREATE,
                "--pipeline-name",
                pipeline_name,
                "--config-json",
                config_json_result.value,
            ])
            capsys.readouterr()
            tm.ok(create_result)

            ensure_pid_dir_result = flext_cli.ensure_dir(pid_path.parent)
            tm.ok(ensure_pid_dir_result)
            write_pid_result = u.Cli.files_write_text(pid_path, str(process.pid))
            tm.ok(write_pid_result)

            running_result = meltano_cli.run([
                c.Meltano.CliCommand.PIPELINE,
                c.Meltano.PipelineCommand.STATUS,
                "--pipeline-name",
                pipeline_name,
            ])
            running_output = capsys.readouterr().out
            stop_result = meltano_cli.run([
                c.Meltano.CliCommand.PIPELINE,
                c.Meltano.PipelineCommand.STOP,
                "--pipeline-name",
                pipeline_name,
            ])
            stop_output = capsys.readouterr().out
        finally:
            self._stop_process(process)
            self._restore_pipelines_root(previous_root)

        tm.ok(running_result)
        tm.ok(stop_result)
        tm.that(running_output, has="running")
        tm.that(stop_output, has="stopped")
        tm.that(pid_path.exists(), eq=False)
