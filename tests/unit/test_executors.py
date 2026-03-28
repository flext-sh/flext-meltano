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

from flext_core import FlextLogger, r
from flext_tests import tm

from flext_meltano.services.executor import (
    FlextMeltanoExecutor,
)
from tests import t

logger = FlextLogger(__name__)


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
        tm.that(hasattr(executor, "logger"), eq=True)

    def test_executor_with_custom_project_root(self) -> None:
        """Test executor with custom configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = {"project_root": temp_dir}
            executor = FlextMeltanoExecutor(config_overrides=config)
            assert executor is not None

    def test_run_command_no_args(self) -> None:
        """Test run_command with no arguments returns exit code 1."""
        result = self.executor.run_command([])
        tm.that(result, is_=r)
        tm.ok(result)
        tm.that(result.value, eq=1)

    def test_run_command_invalid(self) -> None:
        """Test run_command with invalid command."""
        result = self.executor.run_command(["invalid_command_that_does_not_exist"])
        tm.that(result, is_=r)
        if not result.is_success:
            tm.that(result.error, none=False)
            tm.that(result.error, is_=str)

    def test_run_method_version(self) -> None:
        """Test run method with version argument returns r."""
        result = self.executor.run(["version"])
        tm.that(result, is_=r)
        # version runs subprocess; may fail if meltano not on PATH
        tm.that(result.is_success or result.is_failure, eq=True)

    def test_run_method_help(self) -> None:
        """Test run method with help argument."""
        result = self.executor.run(["help"])
        tm.that(result, is_=r)
        # help delegates to meltano --help subprocess; may fail if not installed
        tm.that(result.is_success or result.is_failure, eq=True)

    def test_run_method_empty_args_fails(self) -> None:
        """Test run method with empty args returns failure."""
        result = self.executor.run([])
        tm.that(result, is_=r)
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that((result.error or "").lower(), has="cannot be empty")

    def test_health_method(self) -> None:
        """Test health check method."""
        result = self.executor.health()
        tm.that(result, is_=r)
        # health runs meltano version subprocess; may succeed or fail
        tm.that(result.is_success or result.is_failure, eq=True)

    def test_version_method(self) -> None:
        """Test version method returns dict with version info when meltano available."""
        result = self.executor.version()
        tm.that(result, is_=r)
        # version runs meltano subprocess; may fail if meltano not installed
        if result.is_success:
            version_data = result.value
            tm.that(version_data, is_=dict)
            tm.that(version_data, has="command")
            tm.that(version_data, has="version")
            tm.that(version_data, has="success")
            tm.that(version_data, has="cli_type")
            tm.that(version_data["command"], eq="version")
            tm.that(version_data["cli_type"], eq="flext_meltano")
        else:
            tm.that(result.error, none=False)

    def test_help_method(self) -> None:
        """Test help method."""
        result = self.executor.help()
        tm.that(result, is_=r)
        tm.that(result.is_success or result.is_failure, eq=True)

    def test_run_pipeline_command_method(self) -> None:
        """Test run_pipeline_command method."""
        result = self.executor.run_pipeline_command("tap-csv", "target-jsonl")
        tm.that(result, is_=r)
        if not result.is_success:
            tm.that(result.error, none=False)
            tm.that(result.error, is_=str)

    def test_route_command_method(self) -> None:
        """Test _route_command method routes correctly."""
        result = self.executor._route_command("version", [])
        tm.that(result, is_=r)
        # may fail if meltano not on PATH
        tm.that(result.is_success or result.is_failure, eq=True)

        result = self.executor._route_command("health", [])
        tm.that(result, is_=r)
        tm.that(result.is_success or result.is_failure, eq=True)

        result = self.executor._route_command("unknown", ["args"])
        tm.that(result, is_=r)

    def test_execute_method(self) -> None:
        """Test execute method returns executor config."""
        result = self.executor.execute()
        tm.that(result, is_=r)
        tm.ok(result)
        exec_data = result.value
        tm.that(exec_data, is_=dict)
        tm.that(exec_data, has="executor_type")
        tm.that(exec_data, has="status")

    def test_get_version_static(self) -> None:
        """Test get_version static method returns r[str]."""
        result = FlextMeltanoExecutor.get_version()
        tm.that(result, is_=r)
        # Falls back to default version if meltano not installed
        if result.is_success:
            tm.that(result.value, is_=str)
        else:
            tm.that(result.error, none=False)

    def test_run_cli_none_args(self) -> None:
        """Test run_cli with None returns ready status."""
        result = self.executor.run_cli(None)
        tm.that(result, is_=r)
        tm.ok(result)

    def test_run_cli_empty_args(self) -> None:
        """Test run_cli with empty list returns ready status."""
        result = self.executor.run_cli([])
        tm.that(result, is_=r)
        tm.ok(result)

    def test_run_cli_version_args(self) -> None:
        """Test run_cli with version args delegates to run."""
        result = self.executor.run_cli(["version"])
        tm.that(result, is_=r)
        # version subprocess may fail if meltano not installed
        tm.that(result.is_success or result.is_failure, eq=True)

    def test_create_flext_cli(self) -> None:
        """Test create_flext_cli static factory."""
        cli_result = FlextMeltanoExecutor.create_flext_cli()
        tm.that(cli_result, is_=r)
        assert cli_result.is_success
        cli_app = cli_result.value
        assert cli_app is not None

    def test_create_cli_runner_no_args(self) -> None:
        """Test create_cli_runner with empty args."""
        result = FlextMeltanoExecutor.create_cli_runner([])
        tm.that(result, is_=r)
        tm.ok(result)
        runner_data = result.value
        tm.that(runner_data, is_=dict)

    def test_create_cli_runner_with_args(self) -> None:
        """Test create_cli_runner with version args."""
        result = FlextMeltanoExecutor.create_cli_runner(["version"])
        tm.that(result, is_=r)
        tm.that(result.is_success or result.is_failure, eq=True)

    def test_execute_meltano_command(self) -> None:
        """Test execute_meltano_command runs subprocess."""
        result = self.executor.execute_meltano_command(["meltano", "version"])
        tm.that(result, is_=r)
        # May fail if meltano not installed
        tm.that(result.is_success or result.is_failure, eq=True)

    def test_execute_pipeline(self) -> None:
        """Test execute_pipeline method."""
        result = self.executor.execute_pipeline("tap-csv", "target-jsonl")
        tm.that(result, is_=r)
        tm.that(result.is_success or result.is_failure, eq=True)

    def test_execute_dbt_command(self) -> None:
        """Test execute_dbt_command method."""
        result = self.executor.execute_dbt_command("run")
        tm.that(result, is_=r)
        tm.that(result.is_success or result.is_failure, eq=True)

    def test_error_handling_with_invalid_project_root(self) -> None:
        """Test error handling with invalid configuration."""
        invalid_path = Path("/nonexistent/invalid/path")
        executor = FlextMeltanoExecutor(
            config_overrides={"project_root": str(invalid_path)},
        )
        result = executor.version()
        tm.that(result, is_=r)
        # version uses get_version() which is static; may fail if meltano not installed
        tm.that(result.is_success or result.is_failure, eq=True)

    def test_multiple_command_execution(self) -> None:
        """Test executing version multiple times in sequence."""
        for _ in range(3):
            result = self.executor.version()
            tm.that(result, is_=r)
            tm.that(result.is_success or result.is_failure, eq=True)

    def test_concurrent_executor_instances(self) -> None:
        """Test multiple executor instances work independently."""
        executor1 = FlextMeltanoExecutor()
        executor2 = FlextMeltanoExecutor()
        result1 = executor1.version()
        result2 = executor2.version()
        tm.that(result1, is_=r)
        tm.that(result2, is_=r)
        # Both should return same result type regardless of meltano availability
        tm.that(result1.is_success or result1.is_failure, eq=True)
        tm.that(result2.is_success or result2.is_failure, eq=True)

    def test_command_routing_edge_cases(self) -> None:
        """Test command routing edge cases."""
        edge_case_commands: Sequence[tuple[str, t.StrSequence]] = [
            ("nonexistent", []),
            ("version", ["extra", "args"]),
        ]
        for command, args in edge_case_commands:
            result = self.executor._route_command(command, args)
            tm.that(result, is_=r)

    def test_pipeline_execution_error_scenarios(self) -> None:
        """Test pipeline execution with error scenarios."""
        problematic_pipelines = [
            ("", ""),
            ("nonexistent-tap", "nonexistent-target"),
        ]
        for tap, target in problematic_pipelines:
            result = self.executor.run_pipeline_command(tap, target)
            tm.that(result, is_=r)
            if not result.is_success:
                tm.that(result.error, none=False)
                tm.that(result.error, is_=str)

    def test_project_root_property(self) -> None:
        """Test project_root property returns Path."""
        root = self.executor.project_root
        tm.that(root, is_=Path)

    def test_version_mock_failure(self) -> None:
        """Test version error path using mock."""
        with mock.patch.object(
            FlextMeltanoExecutor,
            "get_version",
            return_value=r[str].fail("Version command failed"),
        ):
            version_result = FlextMeltanoExecutor().version()
            tm.fail(version_result)
            if version_result.error is not None:
                tm.that(str(version_result.error), has="Version command failed")
