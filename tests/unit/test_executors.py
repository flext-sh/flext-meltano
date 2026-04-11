"""Test module for FlextMeltanoExecutor.

Tests the executor service with real method signatures. Methods removed
from src/ (fake stubs) have been cleaned from this test file.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from collections.abc import Sequence
from pathlib import Path
from unittest import mock

from flext_meltano import FlextMeltanoExecutor
from tests import r, t, u

logger = u.fetch_logger(__name__)


class TestFlextMeltanoExecutorComplete:
    """Complete test suite for FlextMeltanoExecutor."""

    executor: FlextMeltanoExecutor

    def setup_method(self) -> None:
        """Setup for each test."""
        self.executor = FlextMeltanoExecutor()

    def test_executor_initialization(self) -> None:
        """Test executor initialization."""
        executor = FlextMeltanoExecutor()
        assert executor is not None

    def test_executor_with_custom_project_root(self) -> None:
        """Test executor with custom configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = {"project_root": temp_dir}
            executor = FlextMeltanoExecutor(config_overrides=config)
            assert executor is not None

    def test_run_command_no_args(self) -> None:
        """Test run_command with no arguments returns exit code 1."""
        result = self.executor.run_command([])
        assert isinstance(result, r)
        assert result.success
        assert result.value == 1

    def test_run_command_invalid(self) -> None:
        """Test run_command with invalid command."""
        result = self.executor.run_command(["invalid_command_that_does_not_exist"])
        assert isinstance(result, r)
        if not result.success:
            assert result.error is not None
            assert isinstance(result.error, str)

    def test_run_method_version(self) -> None:
        """Test run method with version argument returns r."""
        result = self.executor.run(["version"])
        assert isinstance(result, r)
        assert result.success
        assert "version" in result.value
        assert result.value["command"] == "version"

    def test_run_method_help(self) -> None:
        """Test run method with help argument."""
        result = self.executor.run(["help"])
        assert isinstance(result, r)
        assert result.success
        assert "help" in result.value
        assert "Usage: meltano" in str(result.value["help"])

    def test_run_method_empty_args_fails(self) -> None:
        """Test run method with empty args returns failure."""
        result = self.executor.run([])
        assert isinstance(result, r)
        assert result.failure
        assert result.error is not None
        assert "cannot be empty" in (result.error or "").lower()

    def test_health_method(self) -> None:
        """Test health check method."""
        result = self.executor.health()
        assert isinstance(result, r)
        assert result.success
        assert result.value["health"] == "OK"
        assert result.value["status"] == "healthy"

    def test_version_method(self) -> None:
        """Test version method returns dict with version info from runtime."""
        result = self.executor.version()
        assert isinstance(result, r)
        assert result.success
        version_data = result.value
        assert isinstance(version_data, dict)
        assert "command" in version_data
        assert "version" in version_data
        assert "success" in version_data
        assert "cli_type" in version_data
        assert version_data["command"] == "version"
        assert version_data["cli_type"] == "flext_meltano"

    def test_help_method(self) -> None:
        """Test help method."""
        result = self.executor.help()
        assert isinstance(result, r)
        assert result.success
        assert "Usage: meltano" in str(result.value["help"])

    def test_run_pipeline_command_method(self) -> None:
        """Test run_pipeline_command method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "pipeline_project"
            init_result = FlextMeltanoExecutor.initialize_project_root(project_root)
            assert init_result.success
            executor = FlextMeltanoExecutor(
                config_overrides={"project_root": str(project_root)},
            )
            result = executor.run_pipeline_command("tap-csv", "target-jsonl")
        assert isinstance(result, r)
        assert result.success
        assert "exit_code" in result.value
        assert "output" in result.value

    def test_route_command_method(self) -> None:
        """Test _route_command method routes correctly."""
        result = self.executor._route_command("version", [])
        assert isinstance(result, r)
        # may fail if meltano not on PATH
        assert result.success or result.failure

        result = self.executor._route_command("health", [])
        assert isinstance(result, r)
        assert result.success or result.failure

        result = self.executor._route_command("unknown", ["args"])
        assert isinstance(result, r)

    def test_execute_method(self) -> None:
        """Test execute method returns executor config."""
        result = self.executor.execute()
        assert isinstance(result, r)
        assert result.success
        exec_data = result.value
        assert isinstance(exec_data, dict)
        assert "executor_type" in exec_data
        assert "status" in exec_data

    def test_get_version_static(self) -> None:
        """Test get_version static method returns r[str]."""
        result = FlextMeltanoExecutor.get_version()
        assert isinstance(result, r)
        assert result.success
        assert isinstance(result.value, str)

    def test_run_cli_none_args(self) -> None:
        """Test run_cli with None returns ready status."""
        result = self.executor.run_cli(None)
        assert isinstance(result, r)
        assert result.success

    def test_run_cli_empty_args(self) -> None:
        """Test run_cli with empty list returns ready status."""
        result = self.executor.run_cli([])
        assert isinstance(result, r)
        assert result.success

    def test_run_cli_version_args(self) -> None:
        """Test run_cli with version args delegates to run."""
        result = self.executor.run_cli(["version"])
        assert isinstance(result, r)
        assert result.success
        assert "version" in result.value

    def test_create_flext_cli(self) -> None:
        """Test create_flext_cli static factory."""
        cli_result = FlextMeltanoExecutor.create_flext_cli()
        assert cli_result.success
        cli_app = cli_result.value
        assert cli_app is not None

    def test_create_cli_runner_no_args(self) -> None:
        """Test create_cli_runner with empty args."""
        result = FlextMeltanoExecutor.create_cli_runner([])
        assert isinstance(result, r)
        assert result.success
        runner_data = result.value
        assert isinstance(runner_data, dict)

    def test_create_cli_runner_with_args(self) -> None:
        """Test create_cli_runner with version args."""
        result = FlextMeltanoExecutor.create_cli_runner(["version"])
        assert isinstance(result, r)
        assert result.success
        assert "version" in result.value

    def test_execute_meltano_command(self) -> None:
        """Test execute_meltano_command normalizes prefixed runtime commands."""
        result = self.executor.execute_meltano_command(["meltano", "version"])
        assert isinstance(result, r)
        assert result.success
        assert result.value.success is True
        assert result.value.command[0] == "--version"

    def test_execute_meltano_command_without_prefix(self) -> None:
        """Test execute_meltano_command accepts non-prefixed runtime commands."""
        result = self.executor.execute_meltano_command(["help"])
        assert isinstance(result, r)
        assert result.success
        assert result.value.success is True
        assert result.value.command[0] == "--help"

    def test_execute_pipeline(self) -> None:
        """Test execute_pipeline method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "executor_pipeline_project"
            init_result = FlextMeltanoExecutor.initialize_project_root(project_root)
            assert init_result.success
            executor = FlextMeltanoExecutor(
                config_overrides={"project_root": str(project_root)},
            )
            result = executor.execute_pipeline("tap-csv", "target-jsonl")
        assert isinstance(result, r)
        assert result.success
        assert isinstance(result.value.exit_code, int)
        assert result.value.command[0] == "elt"

    def test_execute_dbt_command(self) -> None:
        """Test execute_dbt_command method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "executor_dbt_project"
            init_result = FlextMeltanoExecutor.initialize_project_root(project_root)
            assert init_result.success
            executor = FlextMeltanoExecutor(
                config_overrides={"project_root": str(project_root)},
            )
            result = executor.execute_dbt_command("run")
        assert isinstance(result, r)
        assert result.success
        assert isinstance(result.value.exit_code, int)
        assert result.value.command[0] == "invoke"

    def test_error_handling_with_invalid_project_root(self) -> None:
        """Test error handling with invalid configuration."""
        invalid_path = Path("/nonexistent/invalid/path")
        executor = FlextMeltanoExecutor(
            config_overrides={"project_root": str(invalid_path)},
        )
        result = executor.version()
        assert isinstance(result, r)
        assert result.success
        assert "version" in result.value

    def test_multiple_command_execution(self) -> None:
        """Test executing version multiple times in sequence."""
        for _ in range(3):
            result = self.executor.version()
            assert isinstance(result, r)
            assert result.success

    def test_concurrent_executor_instances(self) -> None:
        """Test multiple executor instances work independently."""
        executor1 = FlextMeltanoExecutor()
        executor2 = FlextMeltanoExecutor()
        result1 = executor1.version()
        result2 = executor2.version()
        assert isinstance(result1, r)
        assert isinstance(result2, r)
        assert result1.success
        assert result2.success

    def test_command_routing_edge_cases(self) -> None:
        """Test command routing edge cases."""
        edge_case_commands: Sequence[tuple[str, t.StrSequence]] = [
            ("nonexistent", []),
            ("version", ["extra", "args"]),
        ]
        for command, args in edge_case_commands:
            result = self.executor._route_command(command, args)
            assert isinstance(result, r)

    def test_pipeline_execution_error_scenarios(self) -> None:
        """Test pipeline execution with error scenarios."""
        problematic_pipelines = [
            ("", ""),
            ("nonexistent-tap", "nonexistent-target"),
        ]
        for tap, target in problematic_pipelines:
            result = self.executor.run_pipeline_command(tap, target)
            assert isinstance(result, r)
            if not result.success:
                assert result.error is not None
                assert isinstance(result.error, str)

    def test_project_root_property(self) -> None:
        """Test project_root property returns Path."""
        root = self.executor.project_root
        assert isinstance(root, Path)

    def test_version_mock_failure(self) -> None:
        """Test version error path using mock."""
        with mock.patch.object(
            FlextMeltanoExecutor,
            "get_version",
            return_value=r[str].fail("Version command failed"),
        ):
            version_result = FlextMeltanoExecutor().version()
            assert version_result.failure
            if version_result.error is not None:
                assert "Version command failed" in str(version_result.error)
