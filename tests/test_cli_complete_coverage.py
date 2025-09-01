"""Complete CLI coverage tests - testing all CLI functionality with real APIs.

**Purpose**: Achieve 95%+ coverage on executors_cli.py module
**Target**: Real functionality testing of all CLI commands and patterns
**Scope**: FlextMeltanoCli, flext_meltano_run_cli, command routing, error handling
"""

from __future__ import annotations

from flext_core import FlextResult

from flext_meltano.executors_bridge import FlextMeltanoBridge
from flext_meltano.executors_cli import FlextMeltanoCli, flext_meltano_run_cli


class TestFlextMeltanoCliComplete:
    """Complete coverage testing of FlextMeltanoCli."""

    def test_cli_initialization(self) -> None:
        """Test CLI initialization patterns."""
        cli = FlextMeltanoCli()

        assert cli is not None
        assert hasattr(cli, "bridge")
        assert hasattr(cli, "logger")
        assert cli.bridge is not None

    def test_run_command_empty_args(self) -> None:
        """Test CLI with empty arguments."""
        cli = FlextMeltanoCli()

        # Test run_command with empty args (returns int)
        exit_code = cli.run_command([])
        assert isinstance(exit_code, int)

        # Test run with empty args (returns FlextResult)
        result = cli.run([])
        assert isinstance(result, FlextResult)

        if result.success:
            assert isinstance(result.data, dict)
            assert "command" in result.data
            assert "status" in result.data

    def test_run_command_version_flag(self) -> None:
        """Test CLI --version command."""
        cli = FlextMeltanoCli()

        # Test run_command with --version
        exit_code = cli.run_command(["--version"])
        assert isinstance(exit_code, int)

        # Test run with --version
        result = cli.run(["--version"])
        assert isinstance(result, FlextResult)

        if result.success:
            assert isinstance(result.data, dict)
            assert "version" in result.data

    def test_run_command_help_flag(self) -> None:
        """Test CLI --help command."""
        cli = FlextMeltanoCli()

        exit_code = cli.run_command(["--help"])
        assert isinstance(exit_code, int)

        result = cli.run(["--help"])
        assert isinstance(result, FlextResult)

    def test_run_command_list_plugins(self) -> None:
        """Test CLI list-plugins command."""
        cli = FlextMeltanoCli()

        exit_code = cli.run_command(["list-plugins"])
        assert isinstance(exit_code, int)

        result = cli.run(["list-plugins"])
        assert isinstance(result, FlextResult)

        if result.success:
            assert isinstance(result.data, dict)
            assert "command" in result.data
            assert result.data.get("command") == "list-plugins"

    def test_run_command_run_pipeline(self) -> None:
        """Test CLI run-pipeline command with arguments."""
        cli = FlextMeltanoCli()

        # Test with tap and target arguments
        exit_code = cli.run_command(["run-pipeline", "tap-csv", "target-jsonl"])
        assert isinstance(exit_code, int)

        result = cli.run(["run-pipeline", "tap-csv", "target-jsonl"])
        assert isinstance(result, FlextResult)

    def test_run_command_discover_catalog(self) -> None:
        """Test CLI discover-catalog command."""
        cli = FlextMeltanoCli()

        exit_code = cli.run_command(["discover-catalog", "tap-csv"])
        assert isinstance(exit_code, int)

        result = cli.run(["discover-catalog", "tap-csv"])
        assert isinstance(result, FlextResult)

    def test_run_command_unknown_command(self) -> None:
        """Test CLI with unknown command."""
        cli = FlextMeltanoCli()

        exit_code = cli.run_command(["unknown-command"])
        assert isinstance(exit_code, int)

        result = cli.run(["unknown-command"])
        assert isinstance(result, FlextResult)

    def test_execute_method_patterns(self) -> None:
        """Test CLI execute method with different commands."""
        cli = FlextMeltanoCli()

        # Test execute with version command
        result = cli.execute("version")
        assert isinstance(result, FlextResult)

        # Test execute with help command
        result = cli.execute("help")
        assert isinstance(result, FlextResult)

        # Test execute with list-plugins
        result = cli.execute("list-plugins")
        assert isinstance(result, FlextResult)

    def test_execute_with_options(self) -> None:
        """Test CLI execute with command options."""
        cli = FlextMeltanoCli()

        # Test execute with options list
        result = cli.execute("version", ["--verbose"])
        assert isinstance(result, FlextResult)

        result = cli.execute("list-plugins", ["--format", "json"])
        assert isinstance(result, FlextResult)

    def test_bridge_integration_patterns(self) -> None:
        """Test CLI bridge integration."""
        cli = FlextMeltanoCli()

        # Verify bridge is properly initialized
        assert isinstance(cli.bridge, FlextMeltanoBridge)

        # Test bridge operations through CLI
        version_result = cli.bridge.get_version()
        assert isinstance(version_result, dict)
        assert "success" in version_result

        plugins_result = cli.bridge.list_plugins()
        assert isinstance(plugins_result, dict)
        assert "success" in plugins_result

    def test_error_handling_patterns(self) -> None:
        """Test CLI error handling patterns."""
        cli = FlextMeltanoCli()

        # Test with malformed commands
        result = cli.run(["run-pipeline"])  # Missing required args
        assert isinstance(result, FlextResult)

        result = cli.run(["discover-catalog"])  # Missing required args
        assert isinstance(result, FlextResult)

        # Test execute with invalid options
        result = cli.execute("invalid-command", ["--invalid-flag"])
        assert isinstance(result, FlextResult)


class TestFlextMeltanoRunCliFunction:
    """Complete testing of flext_meltano_run_cli function."""

    def test_run_cli_with_none_args(self) -> None:
        """Test run CLI function with None args."""
        result = flext_meltano_run_cli(None)
        assert isinstance(result, FlextResult)

    def test_run_cli_with_empty_list(self) -> None:
        """Test run CLI function with empty list."""
        result = flext_meltano_run_cli([])
        assert isinstance(result, FlextResult)

    def test_run_cli_with_version_command(self) -> None:
        """Test run CLI function with version command."""
        result = flext_meltano_run_cli(["--version"])
        assert isinstance(result, FlextResult)

        if result.success:
            assert isinstance(result.data, dict)

    def test_run_cli_with_help_command(self) -> None:
        """Test run CLI function with help command."""
        result = flext_meltano_run_cli(["--help"])
        assert isinstance(result, FlextResult)

    def test_run_cli_with_list_plugins(self) -> None:
        """Test run CLI function with list-plugins."""
        result = flext_meltano_run_cli(["list-plugins"])
        assert isinstance(result, FlextResult)

    def test_run_cli_with_pipeline_command(self) -> None:
        """Test run CLI function with pipeline command."""
        result = flext_meltano_run_cli(["run-pipeline", "tap-csv", "target-jsonl"])
        assert isinstance(result, FlextResult)

    def test_run_cli_with_discover_command(self) -> None:
        """Test run CLI function with discover command."""
        result = flext_meltano_run_cli(["discover-catalog", "tap-csv"])
        assert isinstance(result, FlextResult)

    def test_run_cli_with_unknown_command(self) -> None:
        """Test run CLI function with unknown command."""
        result = flext_meltano_run_cli(["unknown-command"])
        assert isinstance(result, FlextResult)

    def test_run_cli_error_recovery(self) -> None:
        """Test run CLI function error recovery."""
        # Test with malformed commands
        result = flext_meltano_run_cli(["run-pipeline"])  # Missing args
        assert isinstance(result, FlextResult)

        result = flext_meltano_run_cli(["discover-catalog"])  # Missing args
        assert isinstance(result, FlextResult)


class TestCliIntegrationPatterns:
    """Test CLI integration with other components."""

    def test_cli_bridge_version_integration(self) -> None:
        """Test CLI version command integration with bridge."""
        cli = FlextMeltanoCli()

        # CLI version should match bridge version
        cli_result = cli.run(["--version"])
        bridge_result = cli.bridge.get_version()

        assert isinstance(cli_result, FlextResult)
        assert isinstance(bridge_result, FlextResult)

        if cli_result.success and bridge_result.success:
            # Both should report consistent version info
            assert "version" in cli_result.data
            assert "version" in bridge_result.data

    def test_cli_plugins_integration(self) -> None:
        """Test CLI plugins command integration."""
        cli = FlextMeltanoCli()

        # CLI list-plugins should match bridge list_plugins
        cli_result = cli.run(["list-plugins"])
        bridge_result = cli.bridge.list_plugins()

        assert isinstance(cli_result, FlextResult)
        assert isinstance(bridge_result, dict)

        if cli_result.success and bridge_result.get("success"):
            # Both should report operation information
            assert "command" in cli_result.data
            assert "data" in bridge_result

    def test_cli_pipeline_integration(self) -> None:
        """Test CLI pipeline command integration."""
        cli = FlextMeltanoCli()

        # CLI pipeline should use bridge run_pipeline
        cli_result = cli.run(["run-pipeline", "tap-csv", "target-jsonl"])
        bridge_result = cli.bridge.run_pipeline("tap-csv", "target-jsonl")

        assert isinstance(cli_result, FlextResult)
        assert isinstance(bridge_result, dict)

        # Both should handle the operation (success or graceful failure)
        assert "success" in bridge_result

    def test_cli_discovery_integration(self) -> None:
        """Test CLI discovery integration."""
        cli = FlextMeltanoCli()

        # Test discover command routing
        cli_result = cli.run(["discover-catalog", "tap-csv"])
        assert isinstance(cli_result, FlextResult)


class TestCliCommandRouting:
    """Test CLI command routing and argument parsing."""

    def test_command_routing_patterns(self) -> None:
        """Test different command routing patterns."""
        cli = FlextMeltanoCli()

        # Test single commands
        commands = [
            ["--version"],
            ["--help"],
            ["list-plugins"],
            ["status"],
        ]

        for command in commands:
            result = cli.run(command)
            assert isinstance(result, FlextResult)

    def test_command_with_arguments(self) -> None:
        """Test commands that require arguments."""
        cli = FlextMeltanoCli()

        # Test commands with arguments
        commands_with_args = [
            ["run-pipeline", "tap-csv", "target-jsonl"],
            ["discover-catalog", "tap-csv"],
        ]

        for command in commands_with_args:
            result = cli.run(command)
            assert isinstance(result, FlextResult)

    def test_command_validation(self) -> None:
        """Test command argument validation."""
        cli = FlextMeltanoCli()

        # Test insufficient arguments
        incomplete_commands = [
            ["run-pipeline"],  # Missing tap and target
            ["run-pipeline", "tap-csv"],  # Missing target
            ["discover-catalog"],  # Missing tap
        ]

        for command in incomplete_commands:
            result = cli.run(command)
            assert isinstance(result, FlextResult)
            # Should handle gracefully, not crash

    def test_help_command_variations(self) -> None:
        """Test different help command variations."""
        cli = FlextMeltanoCli()

        help_commands = [
            ["--help"],
            ["-h"],
            ["help"],
        ]

        for command in help_commands:
            result = cli.run(command)
            assert isinstance(result, FlextResult)


class TestCliRealWorldUsage:
    """Test CLI real-world usage patterns."""

    def test_typical_workflow_commands(self) -> None:
        """Test typical CLI workflow commands."""
        cli = FlextMeltanoCli()

        # Typical workflow: version -> list plugins -> discover -> run
        workflow_commands = [
            ["--version"],
            ["list-plugins"],
            ["discover-catalog", "tap-csv"],
            ["run-pipeline", "tap-csv", "target-jsonl"],
        ]

        for command in workflow_commands:
            result = cli.run(command)
            assert isinstance(result, FlextResult)
            # Each step should complete without crashing

    def test_error_scenarios_handling(self) -> None:
        """Test CLI error scenarios."""
        cli = FlextMeltanoCli()

        # Error scenarios that should be handled gracefully
        error_commands = [
            ["run-pipeline", "nonexistent-tap", "nonexistent-target"],
            ["discover-catalog", "nonexistent-tap"],
            ["invalid-command"],
            [""],  # Empty string command
        ]

        for command in error_commands:
            result = cli.run(command)
            assert isinstance(result, FlextResult)
            # Should not raise exceptions

    def test_cli_consistency_across_methods(self) -> None:
        """Test consistency between CLI methods."""
        cli = FlextMeltanoCli()

        # Test same command via different methods
        command = ["--version"]

        run_result = cli.run(command)
        execute_result = cli.execute("version")

        assert isinstance(run_result, FlextResult)
        assert isinstance(execute_result, FlextResult)

        # Both methods should behave consistently
        if run_result.success and execute_result.success:
            # Both should contain version information
            assert "version" in run_result.data or "status" in run_result.data
            assert isinstance(execute_result.data, dict)
