"""Unit tests for pipeline CLI managers."""

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

        completed = subprocess.CompletedProcess(
            args=["meltano", "run", "tap-demo", "target-demo"],
            returncode=0,
            stdout="pipeline ok",
            stderr="",
        )

        with patch(
            "flext_meltano.cli_managers.subprocess.run",
            return_value=completed,
        ) as run_mock:
            result = execute_pipeline("daily-pipeline")

    assert result.is_success
    run_mock.assert_called_once_with(
        ["meltano", "run", "tap-demo", "target-demo"],
        cwd=str(tmp_path / "pipelines" / "daily-pipeline"),
        check=False,
        capture_output=True,
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
    assert list_result.value == ["a-pipeline", "b-pipeline"]


def test_get_pipeline_status_checks_process_state(tmp_path: Path) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        assert create_pipeline(
            "daily-pipeline",
            {"command": ["run", "tap", "target"]},
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

    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        assert create_pipeline(
            "daily-pipeline",
            {"command": ["run", "tap", "target"]},
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
            msg = "Unexpected signal"
            raise AssertionError(msg)

        with patch("flext_meltano.cli_managers.os.kill", side_effect=fake_kill):
            pass

    assert running_result.is_success
    assert not pid_file.exists()


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
            "daily-pipeline",
            config_json,
        ])
        assert create_result.is_success

        completed = subprocess.CompletedProcess(
            args=["meltano", "run", "tap-demo", "target-demo"],
            returncode=0,
            stdout="ok",
            stderr="",
        )

        with patch(
            "flext_meltano.cli_managers.subprocess.run",
            return_value=completed,
        ):
            run_result = manager.handle_command(["run", "daily-pipeline"])

        list_result = manager.handle_command(["list"])
        delete_result = manager.handle_command(["delete", "daily-pipeline"])

    assert run_result.is_success
    assert list_result.is_success
    assert delete_result.is_success
