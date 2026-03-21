"""Unit tests for pipeline CLI managers."""

from __future__ import annotations

import os
import signal
from collections.abc import Mapping
from pathlib import Path
from unittest.mock import MagicMock, patch

from flext_core import r, t
from flext_infra import FlextInfraUtilitiesSubprocess

from flext_meltano import m
from flext_meltano.cli_managers import (
    FlextMeltanoPipelineManager,
    create_pipeline,
    delete_pipeline,
    execute_pipeline,
    get_pipeline_status,
    list_pipelines,
)
from tests.utilities import u


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
    u.Tests.Matchers.ok(result)
    pipeline_dir = tmp_path / "pipelines" / "daily-pipeline"
    u.Tests.Matchers.that(pipeline_dir.is_dir(), eq=True)
    stored = m.Meltano.ConfigMappingPayload.model_validate_json(
        (pipeline_dir / "pipeline.json").read_text(encoding="utf-8")
    )
    u.Tests.Matchers.that(stored.values, eq=config)


def test_create_pipeline_fails_without_configuration(tmp_path: Path) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        result = create_pipeline("daily-pipeline", None)
    u.Tests.Matchers.fail(result)
    u.Tests.Matchers.that(result.error, eq="Pipeline creation not configured")


def test_execute_pipeline_runs_real_subprocess_contract(tmp_path: Path) -> None:

    command: list[t.Scalar | None] = ["run", "tap-demo", "target-demo"]
    config: dict[
        str,
        t.Scalar | list[t.Scalar | None] | Mapping[str, t.Scalar | None] | None,
    ] = {"command": command}
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        create_result = create_pipeline("exec-pipeline", config)
        u.Tests.Matchers.ok(create_result)
        mock_command_result = MagicMock()
        mock_command_result.exit_code = 0
        mock_command_result.stdout = "pipeline ok"
        mock_command_result.stderr = ""
        with patch.object(
            FlextInfraUtilitiesSubprocess,
            "run_raw",
            return_value=r.ok(mock_command_result),
        ) as run_mock:
            result = execute_pipeline("exec-pipeline")
    u.Tests.Matchers.ok(result)
    run_mock.assert_called_once()
    call_args = run_mock.call_args
    u.Tests.Matchers.that(
        call_args[0][0], eq=["meltano", "run", "tap-demo", "target-demo"]
    )
    u.Tests.Matchers.that(
        call_args[1]["cwd"], eq=tmp_path / "pipelines" / "exec-pipeline"
    )


def test_execute_pipeline_fails_when_pipeline_execution_is_not_configured(
    tmp_path: Path,
) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        create_result = create_pipeline("noexec-pipeline", {"schedule": "daily"})
        u.Tests.Matchers.ok(create_result)
        result = execute_pipeline("noexec-pipeline")
    u.Tests.Matchers.fail(result)
    u.Tests.Matchers.that(result.error, eq="Pipeline execution not configured")
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        u.Tests.Matchers.ok(
            create_pipeline("b-pipeline", {"command": ["run", "tap-a", "target-a"]})
        )
        u.Tests.Matchers.ok(
            create_pipeline("a-pipeline", {"command": ["run", "tap-b", "target-b"]})
        )
        list_result = list_pipelines()
    u.Tests.Matchers.ok(list_result)
    u.Tests.Matchers.that("a-pipeline" in list_result.value, eq=True)
    u.Tests.Matchers.that("b-pipeline" in list_result.value, eq=True)


def test_get_pipeline_status_checks_process_state(tmp_path: Path) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        u.Tests.Matchers.ok(
            create_pipeline("status-pipeline", {"command": ["run", "tap", "target"]})
        )
        pid_file = tmp_path / "pipelines" / "status-pipeline" / "pipeline.pid"
        pid_file.write_text("1234", encoding="utf-8")
        with patch("flext_meltano.cli_managers.os.kill", return_value=None):
            running_result = get_pipeline_status("status-pipeline")
        with patch(
            "flext_meltano.cli_managers.os.kill", side_effect=ProcessLookupError
        ):
            stopped_result = get_pipeline_status("status-pipeline")
    u.Tests.Matchers.ok(running_result)
    u.Tests.Matchers.that(running_result.value, eq="running")
    u.Tests.Matchers.ok(stopped_result)
    u.Tests.Matchers.that(stopped_result.value, eq="stopped")
    u.Tests.Matchers.that(pid_file.exists(), eq=False)
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        u.Tests.Matchers.ok(
            create_pipeline("status-pipeline-2", {"command": ["run", "tap", "target"]})
        )
        pid_file = tmp_path / "pipelines" / "status-pipeline-2" / "pipeline.pid"
        pid_file.write_text("5678", encoding="utf-8")
        terminated = {"value": False}

        def fake_kill(pid: int, sig: int) -> None:
            u.Tests.Matchers.that(pid, eq=5678)
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
    u.Tests.Matchers.ok(running_result)


def test_delete_pipeline_removes_configuration_directory(tmp_path: Path) -> None:
    with patch.dict(os.environ, _set_pipelines_root(tmp_path), clear=False):
        u.Tests.Matchers.ok(
            create_pipeline("daily-pipeline", {"command": ["run", "tap", "target"]})
        )
        result = delete_pipeline("daily-pipeline")
    u.Tests.Matchers.ok(result)
    u.Tests.Matchers.that(
        (tmp_path / "pipelines" / "daily-pipeline").exists(), eq=False
    )


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
        u.Tests.Matchers.ok(create_result)
        mock_command_result = MagicMock()
        mock_command_result.exit_code = 0
        mock_command_result.stdout = "ok"
        mock_command_result.stderr = ""
        with patch.object(
            FlextInfraUtilitiesSubprocess,
            "run_raw",
            return_value=r.ok(mock_command_result),
        ):
            run_result = manager.handle_command(["run", "lifecycle-pipeline"])
        list_result = manager.handle_command(["list"])
        delete_result = manager.handle_command(["delete", "lifecycle-pipeline"])
    u.Tests.Matchers.ok(run_result)
    u.Tests.Matchers.ok(list_result)
    u.Tests.Matchers.ok(delete_result)
