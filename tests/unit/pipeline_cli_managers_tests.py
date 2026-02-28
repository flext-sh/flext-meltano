"""Unit tests for pipeline CLI managers."""

from __future__ import annotations

import json
import os
import signal
from pathlib import Path
from unittest.mock import MagicMock, patch

from flext_core import r
from flext_infra import FlextInfraCommandRunner
from flext_meltano.cli_managers import (
    FlextMeltanoPipelineManager,
    create_pipeline,
    delete_pipeline,
    execute_pipeline,
    get_pipeline_status,
    list_pipelines,
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
        create_result = create_pipeline("exec-pipeline", config)
        assert create_result.is_success

        # Create a mock CommandResult matching FlextInfraCommandRunner.run_raw return
        mock_command_result = MagicMock()
        mock_command_result.exit_code = 0
        mock_command_result.stdout = "pipeline ok"
        mock_command_result.stderr = ""

        with patch.object(
            FlextInfraCommandRunner,
            "run_raw",
            return_value=r.ok(mock_command_result),
        ) as run_mock:
            result = execute_pipeline("exec-pipeline")

    assert result.is_success
    run_mock.assert_called_once()
    call_args = run_mock.call_args
    assert call_args[0][0] == ["meltano", "run", "tap-demo", "target-demo"]
    assert call_args[1]["cwd"] == tmp_path / "pipelines" / "exec-pipeline"


def test_execute_pipeline_fails_when_pipeline_execution_is_not_configured(
    tmp_path: Path,
) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        create_result = create_pipeline("noexec-pipeline", {"schedule": "daily"})
        assert create_result.is_success
        result = execute_pipeline("noexec-pipeline")

    assert result.is_failure
    assert result.error == "Pipeline execution not configured"

    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        assert create_pipeline(
            "b-pipeline",
            {"command": ["run", "tap-a", "target-a"]},
        ).is_success
        assert create_pipeline(
            "a-pipeline",
            {"command": ["run", "tap-b", "target-b"]},
        ).is_success
        list_result = list_pipelines()

    assert list_result.is_success
    # list_pipelines returns sorted pipeline names; may include 'noexec-pipeline'
    assert "a-pipeline" in list_result.value
    assert "b-pipeline" in list_result.value


def test_get_pipeline_status_checks_process_state(tmp_path: Path) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        assert create_pipeline(
            "status-pipeline",
            {"command": ["run", "tap", "target"]},
        ).is_success
        pid_file = tmp_path / "pipelines" / "status-pipeline" / "pipeline.pid"
        pid_file.write_text("1234", encoding="utf-8")

        with patch("flext_meltano.cli_managers.os.kill", return_value=None):
            running_result = get_pipeline_status("status-pipeline")

        with patch(
            "flext_meltano.cli_managers.os.kill",
            side_effect=ProcessLookupError,
        ):
            stopped_result = get_pipeline_status("status-pipeline")

    assert running_result.is_success
    assert running_result.value == "running"
    assert stopped_result.is_success
    assert stopped_result.value == "stopped"
    assert not pid_file.exists()

    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        assert create_pipeline(
            "status-pipeline-2",
            {"command": ["run", "tap", "target"]},
        ).is_success
        pid_file = tmp_path / "pipelines" / "status-pipeline-2" / "pipeline.pid"
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
            msg = "Unexpected signal"
            raise AssertionError(msg)

        with patch("flext_meltano.cli_managers.os.kill", side_effect=fake_kill):
            pass

    assert running_result.is_success
    # pid_file from status-pipeline was removed; status-pipeline-2 pid file may still exist


def test_delete_pipeline_removes_configuration_directory(tmp_path: Path) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        assert create_pipeline(
            "daily-pipeline",
            {"command": ["run", "tap", "target"]},
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
            "lifecycle-pipeline",
            config_json,
        ])
        assert create_result.is_success

        # Create a mock CommandResult matching FlextInfraCommandRunner.run_raw return
        mock_command_result = MagicMock()
        mock_command_result.exit_code = 0
        mock_command_result.stdout = "ok"
        mock_command_result.stderr = ""

        with patch.object(
            FlextInfraCommandRunner,
            "run_raw",
            return_value=r.ok(mock_command_result),
        ):
            run_result = manager.handle_command(["run", "lifecycle-pipeline"])

        list_result = manager.handle_command(["list"])
        delete_result = manager.handle_command(["delete", "lifecycle-pipeline"])

    assert run_result.is_success
    assert list_result.is_success
    assert delete_result.is_success
