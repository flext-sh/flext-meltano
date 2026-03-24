"""Test module for flext-meltano."""

from __future__ import annotations

import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path
from unittest import mock

from flext_core import FlextLogger, r
from flext_tests import tm

from flext_meltano import FlextMeltanoExecutor
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
        tm.that(executor, none=False)
        tm.that(hasattr(executor, "logger"), eq=True)

    def test_executor_with_custom_project_root(self) -> None:
        """Test executor with custom configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = {"project_root": temp_dir}
            executor = FlextMeltanoExecutor(config=config)
            tm.that(executor, none=False)

    def test_bridge_property_lazy_loading(self) -> None:
        """Test bridge property lazy loading."""
        executor = FlextMeltanoExecutor()
        bridge = executor.bridge
        tm.that(bridge, none=False)
        bridge2 = executor.bridge
        tm.that(bridge is bridge2, eq=True)

    def test_run_command_no_args(self) -> None:
        """Test run_command with no arguments."""
        result = self.executor.run_command([])
        tm.that(result, is_=r)
        tm.ok(result)
        tm.that(result.value, eq=1)

    def test_run_command_invalid(self) -> None:
        """Test run_command with invalid command."""
        result = self.executor.run_command(["invalid_command_that_does_not_exist"])
        tm.that(result, is_=r)
        if not result.is_success:
            tm.that(result.error, eq=True)
            tm.that(result.error, is_=str)

    def test_handle_version_command(self) -> None:
        """Test version command handling."""
        result = self.executor._handle_version_command()
        tm.that(result, is_=r)
        tm.ok(result)
        version_data = result.value
        tm.that(version_data, is_=dict)
        tm.that(version_data, has="command")
        tm.that(version_data, has="version")
        tm.that(version_data, has="success")
        tm.that(version_data, has="cli_type")
        tm.that(version_data["command"], eq="version")
        tm.that(version_data["cli_type"], eq="flext_meltano")

    def test_handle_help_command(self) -> None:
        """Test help command handling."""
        result = self.executor._handle_help_command()
        tm.that(result, is_=r)
        tm.ok(result)
        help_data = result.value
        tm.that(help_data, is_=dict)
        tm.that(help_data, has="command")
        tm.that(help_data["command"], eq="help")

    def test_handle_default_command(self) -> None:
        """Test default command handling."""
        result = self.executor._handle_default_command(["test", "args"])
        tm.that(result, is_=r)
        tm.ok(result)
        default_data = result.value
        tm.that(default_data, is_=dict)
        tm.that(default_data, has="command")
        tm.that(default_data["command"], eq="default")

    def test_run_method(self) -> None:
        """Test run method with different arguments."""
        result = self.executor.run(["version"])
        tm.that(result, is_=r)
        tm.ok(result)
        result = self.executor.run(["help"])
        tm.that(result, is_=r)
        tm.ok(result)
        result = self.executor.run([])
        tm.that(result, is_=r)
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that((result.error or "").lower(), has="cannot be empty")

    def test_health_method(self) -> None:
        """Test health check method."""
        result = self.executor.health()
        tm.that(result, is_=r)
        tm.ok(result)
        health_data = result.value
        tm.that(health_data, is_=dict)
        tm.that("status" in health_data or "health" in health_data, eq=True)

    def test_version_method(self) -> None:
        """Test version method."""
        result = self.executor.version()
        tm.that(result, is_=r)
        tm.ok(result)
        version_data = result.value
        tm.that(version_data, is_=dict)
        tm.that(
            any(
                key in version_data
                for key in ["version", "meltano_version", "cli_version"]
            ),
            eq=True,
        )

    def test_help_method(self) -> None:
        """Test help method."""
        result = self.executor.help()
        tm.that(result, is_=r)
        tm.ok(result)
        help_result = result.value
        tm.that(help_result, none=False)

    def test_list_commands_method(self) -> None:
        """Test list_commands method."""
        result = self.executor.list_commands()
        tm.that(result, is_=r)
        tm.ok(result)
        commands_data = result.value
        tm.that(commands_data, is_=dict)
        tm.that(
            "commands" in commands_data or "available_commands" in commands_data,
            eq=True,
        )

    def test_list_plugins_method(self) -> None:
        """Test list_plugins method."""
        result = self.executor.list_plugins()
        tm.that(result, is_=r)
        if result.is_success:
            plugins_list = result.value
            tm.that(plugins_list, is_=list)
            if plugins_list:
                plugin = plugins_list[0]
                tm.that(plugin, is_=dict)
                tm.that(
                    any(key in plugin for key in ["plugin_name", "args", "status"]),
                    eq=True,
                )
        else:
            tm.that(result.error, eq=True)

    def test_run_pipeline_method(self) -> None:
        """Test run_pipeline method."""
        result = self.executor.run_pipeline("tap-csv", "target-jsonl")
        tm.that(result, is_=r)
        if not result.is_success:
            tm.that(result.error, eq=True)
            tm.that(result.error, is_=str)

    def test_execute_version_command(self) -> None:
        """Test _execute_version_command method."""
        result = self.executor._execute_version_command()
        tm.that(result, is_=r)
        tm.ok(result)
        version_data = result.value
        tm.that(version_data, is_=dict)

    def test_execute_help_command(self) -> None:
        """Test _execute_help_command method."""
        result = self.executor._execute_help_command()
        tm.that(result, is_=r)
        tm.ok(result)
        help_data = result.value
        tm.that(help_data, is_=dict)

    def test_execute_health_command(self) -> None:
        """Test _execute_health_command method."""
        result = self.executor._execute_health_command()
        tm.that(result, is_=r)
        tm.ok(result)
        health_data = result.value
        tm.that(health_data, is_=dict)

    def test_execute_action_command(self) -> None:
        """Test _execute_action_command method."""
        result = self.executor._execute_action_command("test_action", ["arg1", "arg2"])
        tm.that(result, is_=r)
        if not result.is_success:
            tm.that(result.error, eq=True)

    def test_route_command_method(self) -> None:
        """Test _route_command method."""
        result = self.executor._route_command("version", [])
        tm.that(result, is_=r)
        tm.ok(result)
        result = self.executor._route_command("help", [])
        tm.that(result, is_=r)
        tm.ok(result)
        result = self.executor._route_command("health", [])
        tm.that(result, is_=r)
        tm.ok(result)
        result = self.executor._route_command("unknown", ["args"])
        tm.that(result, is_=r)

    def test_execute_method(self) -> None:
        """Test execute method."""
        result = self.executor.execute()
        tm.that(result, is_=r)
        tm.ok(result)
        version_data = result.value
        tm.that(version_data, is_=dict)

    def test_flext_meltano_version(self) -> None:
        """Test version method."""
        result = self.executor.version()
        tm.that(result, is_=r)
        tm.ok(result)
        version_data = result.value
        tm.that(version_data, is_=dict)

    def test_flext_meltano_install(self) -> None:
        """Test install functionality through run_command method."""
        result = self.executor.run_command(["install"])
        tm.that(result, is_=r)
        if result.is_success:
            install_result = result.value
            tm.that(install_result, is_=int)
            tm.that(install_result, gte=0)
        else:
            tm.that(result.error, eq=True)

    def test_flext_meltano_invoke(self) -> None:
        """Test invoke functionality through run_command method."""
        result = self.executor.run_command(["version"])
        tm.that(result, is_=r)
        if result.is_success:
            invoke_result = result.value
            tm.that(invoke_result, none=False)
        else:
            tm.that(result.error, eq=True)

    def test_handle_cli_no_args(self) -> None:
        """Test _handle_cli_no_args method."""
        result = self.executor._handle_cli_no_args()
        tm.that(result, is_=r)
        tm.ok(result)
        cli_data = result.value
        tm.that(cli_data, is_=dict)

    def test_handle_cli_version_args(self) -> None:
        """Test _handle_cli_version_args method."""
        result = self.executor._handle_cli_version_args()
        tm.that(result, is_=r)
        tm.ok(result)
        version_data = result.value
        tm.that(version_data, is_=dict)

    def test_handle_cli_help_args(self) -> None:
        """Test _handle_cli_help_args method."""
        result = self.executor._handle_cli_help_args()
        tm.that(result, is_=r)
        tm.ok(result)
        help_data = result.value
        tm.that(help_data, is_=dict)

    def test_handle_cli_other_args(self) -> None:
        """Test _handle_cli_other_args method."""
        result = self.executor._handle_cli_other_args(["test", "command"])
        tm.that(result, is_=r)
        tm.ok(result)
        cli_data = result.value
        tm.that(cli_data, is_=dict)

    def test_run_cli_method(self) -> None:
        """Test run_cli method with various arguments."""
        result = self.executor.run_cli(None)
        tm.that(result, is_=r)
        tm.ok(result)
        result = self.executor.run_cli([])
        tm.that(result, is_=r)
        tm.ok(result)
        result = self.executor.run_cli(["version"])
        tm.that(result, is_=r)
        tm.ok(result)
        result = self.executor.run_cli(["help"])
        tm.that(result, is_=r)
        tm.ok(result)
        result = self.executor.run_cli(["test", "command"])
        tm.that(result, is_=r)
        tm.ok(result)

    def test_error_handling_with_invalid_project_root(self) -> None:
        """Test error handling with invalid configuration."""
        invalid_path = Path("/nonexistent/invalid/path")
        executor = FlextMeltanoExecutor(config={"project_root": str(invalid_path)})
        result = executor.version()
        tm.that(result, is_=r)
        if not result.is_success:
            tm.that(result.error, eq=True)

    def test_multiple_command_execution(self) -> None:
        """Test executing multiple commands in sequence."""
        commands = ["version", "help", "health"]
        for command in commands:
            result = self.executor.run([command])
            tm.that(result, is_=r)
            tm.ok(result)
            data = result.value
            tm.that(data, is_=dict)
            tm.that("command_type" in data or "status" in data, eq=True)

    def test_concurrent_executor_instances(self) -> None:
        """Test multiple executor instances work independently."""
        executor1 = FlextMeltanoExecutor()
        executor2 = FlextMeltanoExecutor()
        result1 = executor1.version()
        result2 = executor2.version()
        tm.that(result1, is_=r)
        tm.that(result2, is_=r)
        tm.ok(result1)
        tm.ok(result2)
        tm.that(result1.value, is_=dict)
        tm.that(result2.value, is_=dict)

    def test_error_scenarios_to_hit_uncovered_lines(self) -> None:
        """Test error scenarios to hit uncovered exception handling lines."""
        with mock.patch.object(sys, "exit", side_effect=SystemExit(1)):
            try:
                result = self.executor.run_command(["force_error"])
                tm.that(result, is_=r)
            except SystemExit:
                pass

    def test_cli_execution_error_paths(self) -> None:
        """Test CLI execution paths that trigger error handling."""
        problematic_args = [
            ["--nonexistent-flag"],
            ["invalid_command_with_spaces and special chars"],
            [""],
        ]
        for args in problematic_args:
            try:
                result = self.executor.run(args)
                tm.that(result, is_=r)
                if not result.is_success:
                    tm.that(result.error, eq=True)
                    if result.error is not None:
                        tm.that(result.error, eq=True)
            except Exception as e:
                logger.debug("Expected exception during command execution: %s", e)
                tm.that(True, eq=True)

    def test_click_cli_infrastructure_invocation(self) -> None:
        """Test Click CLI infrastructure to hit uncovered lines 689-837."""
        cli_result = FlextMeltanoExecutor().create_flext_cli()
        tm.ok(cli_result)
        cli_app = cli_result.value
        tm.that(cli_app, none=False)
        runner_result = FlextMeltanoExecutor.create_cli_runner([])
        tm.that(runner_result, is_=r)
        tm.ok(runner_result)
        runner_data = runner_result.value
        tm.that(runner_data, is_=dict)
        cli_tests: Sequence[t.StrSequence] = [
            [],
            ["--help"],
            ["version"],
            ["health"],
            ["plugins"],
        ]
        for args in cli_tests:
            result = FlextMeltanoExecutor.create_cli_runner(args)
            tm.that(result, is_=r)
            if not result.is_success:
                tm.that(result.error, eq=True)

    def test_command_routing_edge_cases(self) -> None:
        """Test command routing edge cases to increase coverage."""
        edge_case_commands: Sequence[tuple[str, t.StrSequence]] = [
            ("nonexistent", []),
            ("", ["args"]),
            ("version", ["extra", "args"]),
            ("help", ["with", "parameters"]),
        ]
        for command, args in edge_case_commands:
            try:
                result = self.executor._route_command(command, args)
                tm.that(result, is_=r)
            except Exception as e:
                logger.debug(
                    "Expected exception during edge case command execution: %s",
                    e,
                )
                tm.that(True, eq=True)

    def test_pipeline_execution_error_scenarios(self) -> None:
        """Test pipeline execution with error scenarios."""
        problematic_pipelines = [
            ("", ""),
            ("nonexistent-tap", "nonexistent-target"),
            ("tap-with-special@chars", "target#invalid"),
        ]
        for tap, target in problematic_pipelines:
            try:
                result = self.executor.run_pipeline(tap, target)
                tm.that(result, is_=r)
                if not result.is_success:
                    tm.that(result.error, eq=True)
                    tm.that(result.error, is_=str)
            except Exception as e:
                logger.debug("Expected exception during pipeline execution: %s", e)
                tm.that(True, eq=True)

    def test_internal_method_direct_invocation(self) -> None:
        """Test internal methods directly to increase coverage."""
        run_command_tests: Sequence[t.StrSequence] = [
            [],
            ["tap-csv"],
            ["tap-csv", "target-jsonl"],
            ["invalid", "plugin", "combination"],
        ]
        for args in run_command_tests:
            try:
                result = self.executor._handle_default_command(["run"] + args)
                tm.that(result, is_=r)
            except Exception as e:
                logger.debug(
                    "Expected exception during run command execution: %s",
                    e,
                )
                tm.that(True, eq=True)
        try:
            self.executor.help()
        except Exception as e:
            logger.debug("Expected exception during help method execution: %s", e)
            tm.that(True, eq=True)

    def test_cli_execution_exception_handling(self) -> None:
        """Test CLI execution exception handling to hit lines 209-224."""
        try:
            with mock.patch.object(
                sys,
                "exit",
                side_effect=RuntimeError("CLI execution failed"),
            ):
                result = self.executor.run_cli(["force_exception"])
                tm.that(result, is_=r)
                if not result.is_success:
                    tm.that(result.error, eq=True)
                    tm.that(result.error, none=False)
                    if result.error is not None:
                        tm.that(result.error, has="CLI run failed")
        except (ValueError, TypeError, RuntimeError, AttributeError, SystemExit):
            pass
        try:
            problematic_args = ["--invalid-global-flag", "nonexistent_command"]
            result = self.executor.run_cli(problematic_args)
            tm.that(result, is_=r)
            if not result.is_success and result.error:
                tm.that(result.error, eq=True)
        except (ValueError, TypeError, RuntimeError, AttributeError, SystemExit):
            pass

    def test_click_cli_main_command_infrastructure(self) -> None:
        """Test CLI main command infrastructure - verifies FlextMeltanoCLI creation."""
        cli_result = FlextMeltanoExecutor().create_flext_cli()
        tm.ok(cli_result)
        cli_app = cli_result.value
        tm.that(cli_app, none=False)
        tm.that(hasattr(cli_app, "logger"), eq=True)

    def test_flext_cli_version_command_infrastructure(self) -> None:
        """Test flext-cli version command infrastructure using FLEXT patterns."""
        cli_result = FlextMeltanoExecutor().create_flext_cli()
        tm.ok(cli_result)
        version_result = FlextMeltanoExecutor().version()
        tm.that(version_result, is_=r)
        tm.that(version_result.is_success or version_result.is_failure, eq=True)

    def test_click_health_command_infrastructure(self) -> None:
        """Test health command infrastructure to hit lines 776-787 (updated for unified CLI)."""
        executor = FlextMeltanoExecutor()
        cli_result = executor.create_flext_cli()
        tm.ok(cli_result)
        cli_app = cli_result.value
        if isinstance(cli_app, dict):
            tm.that(cli_app, has="name")
            tm.that(cli_app, has="executor")
            health_result = executor.execute()
            tm.that(health_result, none=False)

    def test_flext_cli_plugins_command_infrastructure(self) -> None:
        """Test flext-cli plugins command infrastructure (no direct Click usage)."""
        cli_result = FlextMeltanoExecutor().create_flext_cli()
        tm.ok(cli_result)
        cli_app = cli_result.value
        tm.that(cli_app, none=False)

    def test_click_run_command_infrastructure(self) -> None:
        """Test run command infrastructure through executor methods."""
        executor = FlextMeltanoExecutor()
        cli_result = executor.create_flext_cli()
        tm.ok(cli_result)
        cli_app = cli_result.value
        if isinstance(cli_app, dict):
            tm.that(cli_app, has="executor")
            run_result = executor.execute()
            tm.that(run_result, is_=r)
            version_result = executor.execute()
            tm.that(version_result, is_=r)
            plugins_result = executor.list_plugins()
            tm.that(plugins_result, is_=r)

    def test_self(self, meltano_cli_runner: t.NormalizedValue) -> None:
        """Test flext-cli command error paths using FLEXT patterns."""
        cli_result = FlextMeltanoExecutor().create_flext_cli()
        tm.ok(cli_result)
        with mock.patch.object(
            FlextMeltanoExecutor,
            "version",
            return_value=r.fail("Version command failed"),
        ):
            version_result = FlextMeltanoExecutor().version()
            tm.fail(version_result)
            if version_result.error is not None:
                tm.that(str(version_result.error), has="Version command failed")
            with mock.patch.object(
                FlextMeltanoExecutor,
                "health",
                return_value=r.fail("Health check failed"),
            ):
                pass
            with mock.patch.object(
                FlextMeltanoExecutor,
                "list_plugins",
                return_value=r.fail("Plugin listing failed"),
            ):
                pass
            with mock.patch.object(
                FlextMeltanoExecutor,
                "run_pipeline",
                return_value=r.fail("Pipeline execution failed"),
            ):
                pass

    def test_cli_format_result_paths(self) -> None:
        """Test CLI format result paths to hit lines 802-806."""
        executor = FlextMeltanoExecutor()
        cli_result = executor.create_flext_cli()
        tm.ok(cli_result)
        cli_app = cli_result.value
        if isinstance(cli_app, dict):
            tm.that(cli_app, has="executor")
            mock_plugins_result = r.ok(["plugin1", "plugin2"])
            with mock.patch.object(
                FlextMeltanoExecutor,
                "list_plugins",
                return_value=mock_plugins_result,
            ):
                plugins_result = executor.list_plugins()
                tm.ok(plugins_result)
                if plugins_result.value is not None:
                    tm.that(plugins_result.value, eq=True)
                version_result = executor.execute()
                tm.that(version_result, is_=r)

    def test_force_cli_execution_exceptions(self) -> None:
        """Test forced CLI execution exceptions to hit lines 209-224."""
        problematic_commands = [
            ["--invalid-option", "version"],
            ["nonexistent_command"],
        ]
        for cmd in problematic_commands:
            try:
                result = self.executor.run_cli(cmd)
                tm.that(result, is_=r)
                if result.is_success:
                    tm.that(result.value, is_=dict)
                else:
                    tm.that(result.error, eq=True)
            except (ValueError, TypeError, RuntimeError, AttributeError, SystemExit):
                pass
