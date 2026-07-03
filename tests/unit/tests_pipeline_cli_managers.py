"""Real-execution tests for the flat Meltano pipeline CLI handler."""

from __future__ import annotations

import multiprocessing
import os
import time
from multiprocessing.process import BaseProcess
from pathlib import Path

from flext_tests import tm

from flext_cli import cli as flext_cli
from flext_meltano import cli
from tests.constants import c
from tests.models import m
from tests.utilities import u


class TestFlextMeltanoPipelineCliManagers:
    """Exercise pipeline lifecycle commands through the flat public CLI."""

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

    def test_pipeline_help_request_returns_help_sentinel(self) -> None:
        """Pipeline help stays on the flat public CLI contract."""
        result = cli.handle_pipeline_command([c.Meltano.CMD_HELP_OPTION])

        tm.ok(result)
        tm.that(result.value, eq=c.Meltano.ExecutorCommand.HELP)

    def test_pipeline_create_list_run_and_delete_use_real_storage(
        self,
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
            create_result = cli.handle_pipeline_command([
                c.Meltano.PipelineCommand.CREATE,
                pipeline_name,
                config_json_result.value,
            ])
            list_result = cli.handle_pipeline_command([c.Meltano.PipelineCommand.LIST])
            status_result = cli.handle_pipeline_command([
                c.Meltano.PipelineCommand.STATUS,
                pipeline_name,
            ])
            run_result = cli.handle_pipeline_command([
                c.Meltano.PipelineCommand.RUN,
                pipeline_name,
            ])
            stored_result = flext_cli.read_json_file(config_path)
            delete_result = cli.handle_pipeline_command([
                c.Meltano.PipelineCommand.DELETE,
                pipeline_name,
            ])
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

        tm.that(list_result.value, has=pipeline_name)
        tm.that(status_result.value, eq="stopped")
        tm.that(run_result.value.lower(), has="usage:")
        tm.that(stored_payload.values, eq={"command": ["help"]})
        tm.that((tmp_path / "pipelines" / pipeline_name).exists(), eq=False)

    def test_pipeline_create_requires_runtime_configuration(
        self,
        tmp_path: Path,
    ) -> None:
        """Pipeline creation without JSON config fails on the real handler path."""
        previous_root = self._activate_pipelines_root(tmp_path)

        try:
            result = cli.handle_pipeline_command([
                c.Meltano.PipelineCommand.CREATE,
                "missing-config",
            ])
        finally:
            self._restore_pipelines_root(previous_root)

        tm.fail(result)
        tm.that(str(result.error), has="not configured")

    def test_pipeline_status_and_stop_use_real_pid_files(
        self,
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
            create_result = cli.handle_pipeline_command([
                c.Meltano.PipelineCommand.CREATE,
                pipeline_name,
                config_json_result.value,
            ])
            tm.ok(create_result)

            ensure_pid_dir_result = flext_cli.ensure_dir(pid_path.parent)
            tm.ok(ensure_pid_dir_result)
            write_pid_result = u.Cli.files_write_text(pid_path, str(process.pid))
            tm.ok(write_pid_result)

            running_result = cli.handle_pipeline_command([
                c.Meltano.PipelineCommand.STATUS,
                pipeline_name,
            ])
            stop_result = cli.handle_pipeline_command([
                c.Meltano.PipelineCommand.STOP,
                pipeline_name,
            ])
        finally:
            self._stop_process(process)
            self._restore_pipelines_root(previous_root)

        tm.ok(running_result)
        tm.ok(stop_result)
        tm.that(running_result.value, eq="running")
        tm.that(stop_result.value, eq="stopped")
        tm.that(pid_path.exists(), eq=False)
