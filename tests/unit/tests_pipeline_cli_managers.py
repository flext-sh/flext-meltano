"""Unit tests for pipeline CLI managers."""

from __future__ import annotations

import os
import signal
from collections.abc import (
    Mapping,
    Sequence,
)
from pathlib import Path
from unittest.mock import MagicMock, patch

from flext_tests import tm

from flext_meltano import FlextMeltanoExecutor, FlextMeltanoPipelineManager
from tests import m, r, t


class TestFlextMeltanoPipelineCliManagers:
    """Unit tests for pipeline CLI managers."""

    @staticmethod
    def _set_pipelines_root(tmp_path: Path) -> t.StrMapping:
        return {"FLEXT_MELTANO_PIPELINES_DIR": str(tmp_path / "pipelines")}

    def test_create_pipeline_creates_directory_and_configuration(
        self,
        tmp_path: Path,
    ) -> None:
        command: Sequence[t.Scalar | None] = ["run", "tap-demo", "target-demo"]
        settings: Mapping[
            str,
            t.Scalar | Sequence[t.Scalar | None] | Mapping[str, t.Scalar | None] | None,
        ] = {
            "command": command,
            "schedule": "daily",
        }

        with patch.dict(os.environ, self._set_pipelines_root(tmp_path), clear=False):
            result = FlextMeltanoPipelineManager.create_pipeline(
                "daily-pipeline", settings
            )

        tm.ok(result)
        pipeline_dir = tmp_path / "pipelines" / "daily-pipeline"
        tm.that(pipeline_dir.is_dir(), eq=True)
        stored = m.Meltano.ConfigMappingPayload.model_validate_json(
            (pipeline_dir / "pipeline.json").read_text(encoding="utf-8"),
        )
        tm.that(stored.values, eq=settings)

    def test_create_pipeline_fails_without_configuration(
        self,
        tmp_path: Path,
    ) -> None:
        with patch.dict(os.environ, self._set_pipelines_root(tmp_path), clear=False):
            result = FlextMeltanoPipelineManager.create_pipeline("daily-pipeline", None)

        tm.fail(result)
        tm.that(result.error, eq="Pipeline creation not configured")

    def test_execute_pipeline_runs_real_subprocess_contract(
        self,
        tmp_path: Path,
    ) -> None:
        command: Sequence[t.Scalar | None] = ["run", "tap-demo", "target-demo"]
        settings: Mapping[
            str,
            t.Scalar | Sequence[t.Scalar | None] | Mapping[str, t.Scalar | None] | None,
        ] = {"command": command}
        mock_cmd_result = m.Meltano.CommandExecutionResult(
            command=["run", "tap-demo", "target-demo"],
            success=True,
            exit_code=0,
            output="pipeline ok",
            error="",
            execution_time=0.1,
        )

        with patch.dict(os.environ, self._set_pipelines_root(tmp_path), clear=False):
            create_result = FlextMeltanoPipelineManager.create_pipeline(
                "exec-pipeline", settings
            )
            tm.ok(create_result)
            with patch.object(
                FlextMeltanoExecutor,
                "execute_meltano_command",
                return_value=r[m.Meltano.CommandExecutionResult].ok(mock_cmd_result),
            ) as run_mock:
                result = FlextMeltanoPipelineManager.execute_pipeline("exec-pipeline")

        tm.ok(result)
        run_mock.assert_called_once()
        call_args = run_mock.call_args
        tm.that(call_args[0][0], eq=["run", "tap-demo", "target-demo"])
        tm.that(call_args[1]["_cwd"], eq=tmp_path / "pipelines" / "exec-pipeline")

    def test_execute_pipeline_fails_when_pipeline_execution_is_not_configured(
        self,
        tmp_path: Path,
    ) -> None:
        with patch.dict(os.environ, self._set_pipelines_root(tmp_path), clear=False):
            create_result = FlextMeltanoPipelineManager.create_pipeline(
                "noexec-pipeline",
                {"schedule": "daily"},
            )
            tm.ok(create_result)
            result = FlextMeltanoPipelineManager.execute_pipeline("noexec-pipeline")

        tm.fail(result)
        tm.that(result.error, eq="Pipeline execution not configured")

        with patch.dict(os.environ, self._set_pipelines_root(tmp_path), clear=False):
            tm.ok(
                FlextMeltanoPipelineManager.create_pipeline(
                    "b-pipeline",
                    {"command": ["run", "tap-a", "target-a"]},
                ),
            )
            tm.ok(
                FlextMeltanoPipelineManager.create_pipeline(
                    "a-pipeline",
                    {"command": ["run", "tap-b", "target-b"]},
                ),
            )
            list_result = FlextMeltanoPipelineManager.list_pipelines()

        tm.ok(list_result)
        tm.that(list_result.value, has="a-pipeline")
        tm.that(list_result.value, has="b-pipeline")

    def test_get_pipeline_status_checks_process_state(
        self,
        tmp_path: Path,
    ) -> None:
        with patch.dict(os.environ, self._set_pipelines_root(tmp_path), clear=False):
            tm.ok(
                FlextMeltanoPipelineManager.create_pipeline(
                    "status-pipeline",
                    {"command": ["run", "tap", "target"]},
                ),
            )
            pid_file = tmp_path / "pipelines" / "status-pipeline" / "pipeline.pid"
            pid_file.write_text("1234", encoding="utf-8")
            with patch(
                "flext_meltano.services._pipeline_lifecycle.os.kill",
                return_value=None,
            ):
                running_result = FlextMeltanoPipelineManager.get_pipeline_status(
                    "status-pipeline",
                )
            with patch(
                "flext_meltano.services._pipeline_lifecycle.os.kill",
                side_effect=ProcessLookupError,
            ):
                stopped_result = FlextMeltanoPipelineManager.get_pipeline_status(
                    "status-pipeline",
                )

        tm.ok(running_result)
        tm.that(running_result.value, eq="running")
        tm.ok(stopped_result)
        tm.that(stopped_result.value, eq="stopped")
        tm.that(not pid_file.exists(), eq=True)

        with patch.dict(os.environ, self._set_pipelines_root(tmp_path), clear=False):
            tm.ok(
                FlextMeltanoPipelineManager.create_pipeline(
                    "status-pipeline-2",
                    {"command": ["run", "tap", "target"]},
                ),
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
                error_message = "Unexpected signal"
                raise AssertionError(error_message)

            with patch(
                "flext_meltano.services._pipeline_lifecycle.os.kill",
                side_effect=fake_kill,
            ):
                stop_result = FlextMeltanoPipelineManager.stop_pipeline(
                    "status-pipeline-2",
                )

        tm.ok(running_result)
        tm.ok(stop_result)
        tm.that(stop_result.value, eq="stopped")
        tm.that(not pid_file.exists(), eq=True)

    def test_delete_pipeline_removes_configuration_directory(
        self,
        tmp_path: Path,
    ) -> None:
        with patch.dict(os.environ, self._set_pipelines_root(tmp_path), clear=False):
            tm.ok(
                FlextMeltanoPipelineManager.create_pipeline(
                    "daily-pipeline",
                    {"command": ["run", "tap", "target"]},
                ),
            )
            result = FlextMeltanoPipelineManager.delete_pipeline("daily-pipeline")

        tm.ok(result)
        tm.that(not (tmp_path / "pipelines" / "daily-pipeline").exists(), eq=True)

    def test_pipeline_manager_lifecycle_commands_delegate_to_real_operations(
        self,
        tmp_path: Path,
    ) -> None:
        manager = FlextMeltanoPipelineManager(MagicMock())
        config_json = m.Meltano.ConfigMappingPayload(
            values={"command": ["run", "tap-demo", "target-demo"]},
        ).model_dump_json()
        mock_cmd_result = m.Meltano.CommandExecutionResult(
            command=["run", "tap-demo", "target-demo"],
            success=True,
            exit_code=0,
            output="ok",
            error="",
            execution_time=0.1,
        )

        with patch.dict(os.environ, self._set_pipelines_root(tmp_path), clear=False):
            create_result = manager.handle_command([
                "create",
                "lifecycle-pipeline",
                config_json,
            ])
            tm.ok(create_result)
            with patch.object(
                FlextMeltanoExecutor,
                "execute_meltano_command",
                return_value=r[m.Meltano.CommandExecutionResult].ok(mock_cmd_result),
            ):
                run_result = manager.handle_command(["run", "lifecycle-pipeline"])
            list_result = manager.handle_command(["list"])
            delete_result = manager.handle_command(["delete", "lifecycle-pipeline"])

        tm.ok(run_result)
        tm.ok(list_result)
        tm.ok(delete_result)
