"""Unit tests for pipeline CLI managers."""

from __future__ import annotations

import os
import signal
from collections.abc import Mapping
from pathlib import Path
from unittest.mock import MagicMock, patch

from flext_core import r
from flext_infra import FlextInfraUtilitiesSubprocess
from flext_tests import tm

from flext_meltano import (
    FlextMeltanoPipelineManager,
    create_pipeline,
    delete_pipeline,
    execute_pipeline,
    get_pipeline_status,
    list_pipelines,
)
from tests import m, t


def _set_pipelines_root(tmp_path: Path) -> dict[str, str]:
    return {"FLEXT_MELTANO_PIPELINES_DIR": str(tmp_path / "pipelines")}


def test_create_pipeline_creates_directory_and_configuration(tmp_path: Path) -> None:
    command: list[t.Scalar | None] = ["run", "tap-demo", "target-demo"]
    config: dict[
        str,
        t.Scalar | list[t.Scalar | None] | Mapping[str, t.Scalar | None] | None,
    ] = {
        "command": command,
        "schedule": "daily",
    }
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        result = create_pipeline("daily-pipeline", config)
    tm.ok(result)
    pipeline_dir = tmp_path / "pipelines" / "daily-pipeline"
    tm.that(pipeline_dir.is_dir(), eq=True)
    stored = m.Meltano.ConfigMappingPayload.model_validate_json(
        (pipeline_dir / "pipeline.json").read_text(encoding="utf-8")
    )
    tm.that(stored.values, eq=config)


def test_create_pipeline_fails_without_configuration(tmp_path: Path) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        result = create_pipeline("daily-pipeline", None)
    tm.fail(result)
    tm.that(result.error, eq="Pipeline creation not configured")


def test_execute_pipeline_runs_real_subprocess_contract(tmp_path: Path) -> None:

    command: list[t.Scalar | None] = ["run", "tap-demo", "target-demo"]
    config: dict[
        str,
        t.Scalar | list[t.Scalar | None] | Mapping[str, t.Scalar | None] | None,
    ] = {"command": command}
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        create_result = create_pipeline("exec-pipeline", config)
        tm.ok(create_result)
        mock_command_result = MagicMock()
        mock_command_result.exit_code = 0
        mock_command_result.stdout = "pipeline ok"
        mock_command_result.stderr = ""
        with patch.t.NormalizedValue(
            FlextInfraUtilitiesSubprocess,
            "run_raw",
            return_value=r.ok(mock_command_result),
        ) as run_mock:
            result = execute_pipeline("exec-pipeline")
    tm.ok(result)
    run_mock.assert_called_once()
    call_args = run_mock.call_args
    tm.that(call_args[0][0], eq=["meltano", "run", "tap-demo", "target-demo"])
    tm.that(call_args[1]["cwd"], eq=tmp_path / "pipelines" / "exec-pipeline")


def test_execute_pipeline_fails_when_pipeline_execution_is_not_configured(
    tmp_path: Path,
) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        create_result = create_pipeline("noexec-pipeline", {"schedule": "daily"})
        tm.ok(create_result)
        result = execute_pipeline("noexec-pipeline")
    tm.fail(result)
    tm.that(result.error, eq="Pipeline execution not configured")
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        tm.ok(create_pipeline("b-pipeline", {"command": ["run", "tap-a", "target-a"]}))
        tm.ok(create_pipeline("a-pipeline", {"command": ["run", "tap-b", "target-b"]}))
        list_result = list_pipelines()
    tm.ok(list_result)
    tm.that("a-pipeline" in list_result.value, eq=True)
    tm.that("b-pipeline" in list_result.value, eq=True)


def test_get_pipeline_status_checks_process_state(tmp_path: Path) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        tm.ok(create_pipeline("status-pipeline", {"command": ["run", "tap", "target"]}))
        pid_file = tmp_path / "pipelines" / "status-pipeline" / "pipeline.pid"
        pid_file.write_text("1234", encoding="utf-8")
        with patch("flext_meltano.cli_managers.os.kill", return_value=None):
            running_result = get_pipeline_status("status-pipeline")
        with patch(
            "flext_meltano.cli_managers.os.kill", side_effect=ProcessLookupError
        ):
            stopped_result = get_pipeline_status("status-pipeline")
    tm.ok(running_result)
    tm.that(running_result.value, eq="running")
    tm.ok(stopped_result)
    tm.that(stopped_result.value, eq="stopped")
    tm.that(pid_file.exists(), eq=False)
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        tm.ok(
            create_pipeline("status-pipeline-2", {"command": ["run", "tap", "target"]})
        )
        pid_file = tmp_path / "pipelines" / "status-pipeline-2" / "pipeline.pid"
        pid_file.write_text("5678", encoding="utf-8")
        terminated = {"value": False}

        def fake_kill(pid: int, sig: int) -> None:
            tm.that(pid, eq=5678)
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
    tm.ok(running_result)


def test_delete_pipeline_removes_configuration_directory(tmp_path: Path) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        tm.ok(create_pipeline("daily-pipeline", {"command": ["run", "tap", "target"]}))
        result = delete_pipeline("daily-pipeline")
    tm.ok(result)
    tm.that((tmp_path / "pipelines" / "daily-pipeline").exists(), eq=False)


def test_pipeline_manager_lifecycle_commands_delegate_to_real_operations(
    tmp_path: Path,
) -> None:
    manager = FlextMeltanoPipelineManager(MagicMock())
    config_json = m.Meltano.ConfigMappingPayload(
        values={"command": ["run", "tap-demo", "target-demo"]}
    ).model_dump_json()
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        create_result = manager.handle_command([
            "create",
            "lifecycle-pipeline",
            config_json,
        ])
        tm.ok(create_result)
        mock_command_result = MagicMock()
        mock_command_result.exit_code = 0
        mock_command_result.stdout = "ok"
        mock_command_result.stderr = ""
        with patch.t.NormalizedValue(
            FlextInfraUtilitiesSubprocess,
            "run_raw",
            return_value=r.ok(mock_command_result),
        ):
            run_result = manager.handle_command(["run", "lifecycle-pipeline"])
        list_result = manager.handle_command(["list"])
        delete_result = manager.handle_command(["delete", "lifecycle-pipeline"])
    tm.ok(run_result)
    tm.ok(list_result)
    tm.ok(delete_result)
