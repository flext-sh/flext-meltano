from __future__ import annotations

import json
import os
import signal
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

from flext_meltano.cli_managers import (
    FlextMeltanoPipelineManager,
    create_pipeline,
    delete_pipeline,
    execute_pipeline,
    get_pipeline_status,
    list_pipelines,
    stop_pipeline,
)


def _set_pipelines_root(tmp_path: Path) -> dict[str, str]:
    return {"FLEXT_MELTANO_PIPELINES_DIR": str(tmp_path / "pipelines")}


def test_create_pipeline_creates_directory_and_configuration(tmp_path: Path) -> None:
    config = {"command": ["run", "tap-demo", "target-demo"], "schedule": "daily"}
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        result = create_pipeline("daily-pipeline", config)

    assert result.is_success
    pipeline_dir = tmp_path / "pipelines" / "daily-pipeline"
    assert pipeline_dir.is_dir()
    assert (
        json.loads((pipeline_dir / "pipeline.json").read_text(encoding="utf-8"))
        == config
    )


def test_create_pipeline_fails_without_configuration(tmp_path: Path) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        result = create_pipeline("daily-pipeline", None)

    assert result.is_failure
    assert result.error == "Pipeline creation not configured"


def test_execute_pipeline_runs_real_subprocess_contract(tmp_path: Path) -> None:
    config = {"command": ["run", "tap-demo", "target-demo"]}
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        create_result = create_pipeline("daily-pipeline", config)
        assert create_result.is_success

        process_mock = MagicMock(spec=subprocess.Popen)
        process_mock.pid = 4242
        process_mock.communicate.return_value = ("pipeline ok", "")
        process_mock.returncode = 0
        process_mock.poll.return_value = 0

        with patch(
            "flext_meltano.cli_managers.subprocess.Popen",
            return_value=process_mock,
        ) as popen_mock:
            result = execute_pipeline("daily-pipeline")

    assert result.is_success
    popen_mock.assert_called_once_with(
        ["meltano", "run", "tap-demo", "target-demo"],
        cwd=str(tmp_path / "pipelines" / "daily-pipeline"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_execute_pipeline_fails_when_pipeline_execution_is_not_configured(
    tmp_path: Path,
) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        create_result = create_pipeline("daily-pipeline", {"schedule": "daily"})
        assert create_result.is_success
        result = execute_pipeline("daily-pipeline")

    assert result.is_failure
    assert result.error == "Pipeline execution not configured"


def test_list_pipelines_returns_real_directories(tmp_path: Path) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        assert create_pipeline(
            "b-pipeline", {"command": ["run", "tap-a", "target-a"]}
        ).is_success
        assert create_pipeline(
            "a-pipeline", {"command": ["run", "tap-b", "target-b"]}
        ).is_success
        result = list_pipelines()

    assert result.is_success
    assert result.value == ["a-pipeline", "b-pipeline"]


def test_get_pipeline_status_checks_process_state(tmp_path: Path) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        assert create_pipeline(
            "daily-pipeline", {"command": ["run", "tap", "target"]}
        ).is_success
        pid_file = tmp_path / "pipelines" / "daily-pipeline" / "pipeline.pid"
        pid_file.write_text("1234", encoding="utf-8")

        with patch("flext_meltano.cli_managers.os.kill", return_value=None):
            running_result = get_pipeline_status("daily-pipeline")

        with patch(
            "flext_meltano.cli_managers.os.kill",
            side_effect=ProcessLookupError,
        ):
            stopped_result = get_pipeline_status("daily-pipeline")

    assert running_result.is_success
    assert running_result.value == "running"
    assert stopped_result.is_success
    assert stopped_result.value == "stopped"
    assert not pid_file.exists()


def test_stop_pipeline_sends_sigterm_and_confirms_stop(tmp_path: Path) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        assert create_pipeline(
            "daily-pipeline", {"command": ["run", "tap", "target"]}
        ).is_success
        pid_file = tmp_path / "pipelines" / "daily-pipeline" / "pipeline.pid"
        pid_file.write_text("5678", encoding="utf-8")

        terminated = {"value": False}

        def fake_kill(pid: int, sig: int) -> None:
            assert pid == 5678
            if sig == 0:
                if terminated["value"]:
                    raise ProcessLookupError
                return
            if sig == signal.SIGTERM:
                terminated["value"] = True
                return
            raise AssertionError("Unexpected signal")

        with patch("flext_meltano.cli_managers.os.kill", side_effect=fake_kill):
            result = stop_pipeline("daily-pipeline")

    assert result.is_success
    assert not pid_file.exists()


def test_delete_pipeline_removes_configuration_directory(tmp_path: Path) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        assert create_pipeline(
            "daily-pipeline", {"command": ["run", "tap", "target"]}
        ).is_success
        result = delete_pipeline("daily-pipeline")

    assert result.is_success
    assert not (tmp_path / "pipelines" / "daily-pipeline").exists()


def test_pipeline_manager_lifecycle_commands_delegate_to_real_operations(
    tmp_path: Path,
) -> None:
    manager = FlextMeltanoPipelineManager(MagicMock())
    config_json = json.dumps({"command": ["run", "tap-demo", "target-demo"]})

    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        create_result = manager.handle_command([
            "create",
            "daily-pipeline",
            config_json,
        ])
        assert create_result.is_success

        process_mock = MagicMock(spec=subprocess.Popen)
        process_mock.pid = 9999
        process_mock.communicate.return_value = ("ok", "")
        process_mock.returncode = 0
        process_mock.poll.return_value = 0

        with patch(
            "flext_meltano.cli_managers.subprocess.Popen",
            return_value=process_mock,
        ):
            run_result = manager.handle_command(["run", "daily-pipeline"])

        list_result = manager.handle_command(["list"])
        delete_result = manager.handle_command(["delete", "daily-pipeline"])

    assert run_result.is_success
    assert list_result.is_success
    assert delete_result.is_success
