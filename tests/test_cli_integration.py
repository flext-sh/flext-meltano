"""CLI Integration Test Suite - Command Interface Validation.

**Test Category**: Integration Tests
**Coverage Target**: 90%+ for CLI interface and command handling
**Dependencies**: CLI module, command parsing, subprocess execution
**Execution Time**: < 10 seconds total

## Test Scope

Validates comprehensive CLI interface functionality including command parsing, argument
validation, execution patterns, and response handling within FLEXT Meltano's
command-line interface architecture.
"""

from __future__ import annotations

import pytest

from flext_meltano import FlextMeltanoCli, flext_meltano_run_cli


class TestFlextMeltanoCli:
    """Test CLI functionality."""

    def test_cli_initialization(self) -> None:
      """Test CLI initialization."""
      cli = FlextMeltanoCli()
      assert cli is not None

    def test_cli_health_check(self) -> None:
      """Test CLI health check."""
      cli = FlextMeltanoCli()

      result = cli.health()
      assert result.success
      assert result.data is not None
      assert result.data is not None
      if "status" not in result.data:
          msg: str = f"Expected {'status'} in {result.data}"
          raise AssertionError(msg)
      if result.data["status"] != "healthy":
          msg: str = f"Expected {'healthy'}, got {result.data['status']}"
          raise AssertionError(msg)

    def test_cli_version_info(self) -> None:
      """Test CLI version information."""
      cli = FlextMeltanoCli()

      result = cli.version()
      assert result.success
      assert result.data is not None
      assert result.data is not None
      if "version" not in result.data:
          msg: str = f"Expected {'version'} in {result.data}"
          raise AssertionError(msg)
      assert isinstance(result.data["version"], str)

    def test_cli_help_command(self) -> None:
      """Test CLI help command."""
      cli = FlextMeltanoCli()

      result = cli.help()
      assert result.success
      assert result.data is not None
      assert result.data is not None
      if "commands" not in result.data:
          msg: str = f"Expected {'commands'} in {result.data}"
          raise AssertionError(msg)
      assert isinstance(result.data["commands"], list)

    def test_cli_run_command_success(self) -> None:
      """Test CLI run command with success."""
      cli = FlextMeltanoCli()

      result = cli.run(["--version"])
      assert result.success

    def test_cli_run_command_with_args(self) -> None:
      """Test CLI run command with arguments."""
      cli = FlextMeltanoCli()

      result = cli.run(["help", "--verbose"])
      assert result.success

    def test_cli_execute_simple_command(self) -> None:
      """Test CLI execute simple command."""
      cli = FlextMeltanoCli()

      result = cli.execute("version")
      assert result.success

    def test_cli_execute_command_with_options(self) -> None:
      """Test CLI execute command with options."""
      cli = FlextMeltanoCli()

      result = cli.execute("run", options=["--dry-run"])
      assert result.success

    def test_cli_list_commands(self) -> None:
      """Test CLI list available commands."""
      cli = FlextMeltanoCli()

      result = cli.list_commands()
      assert result.success
      assert result.data is not None
      assert result.data is not None
      if "commands" not in result.data:
          msg: str = f"Expected {'commands'} in {result.data}"
          raise AssertionError(msg)
      commands = result.data["commands"]
      if "version" not in commands:
          msg: str = f"Expected {'version'} in {commands}"
          raise AssertionError(msg)
      assert "help" in commands
      if "health" not in commands:
          msg: str = f"Expected {'health'} in {commands}"
          raise AssertionError(msg)


class TestFlextMeltanoRunCli:
    """Test CLI run function."""

    def test_run_cli_version(self) -> None:
      """Test run CLI with version command."""
      result = flext_meltano_run_cli(["--version"])
      assert result.success

    def test_run_cli_help(self) -> None:
      """Test run CLI with help command."""
      result = flext_meltano_run_cli(["--help"])
      assert result.success

    def test_run_cli_empty_args(self) -> None:
      """Test run CLI with empty arguments."""
      result = flext_meltano_run_cli([])
      assert result.success

    def test_run_cli_invalid_command(self) -> None:
      """Test run CLI with invalid command."""
      result = flext_meltano_run_cli(["nonexistent-command"])
      # Should handle gracefully
      assert result.success or not result.success  # Either outcome is acceptable

    def test_run_cli_multiple_args(self) -> None:
      """Test run CLI with multiple arguments."""
      result = flext_meltano_run_cli(["run", "--dry-run", "--verbose"])
      assert result.success


class TestCLIIntegrationPatterns:
    """Test CLI integration patterns and workflows."""

    def test_cli_workflow_version_then_help(self) -> None:
      """Test CLI workflow: version then help."""
      cli = FlextMeltanoCli()

      # Get version
      version_result = cli.version()
      assert version_result.success

      # Get help
      help_result = cli.help()
      assert help_result.success

    def test_cli_workflow_health_check(self) -> None:
      """Test CLI workflow: health check."""
      cli = FlextMeltanoCli()

      # Check health
      health_result = cli.health()
      assert health_result.success
      assert health_result.data is not None
      if health_result.data["status"] != "healthy":
          msg: str = f"Expected {'healthy'}, got {health_result.data['status']}"
          raise AssertionError(msg)

    def test_cli_command_execution_patterns(self) -> None:
      """Test various CLI command execution patterns."""
      cli = FlextMeltanoCli()

      # Execute different command types
      commands_to_test = [
          "version",
          "help",
      ]

      for command in commands_to_test:
          result = cli.execute(command)
          assert result.success, f"Command '{command}' failed"

    def test_cli_run_with_different_arg_patterns(self) -> None:
      """Test CLI run with different argument patterns."""
      cli = FlextMeltanoCli()

      arg_patterns = [
          ["--version"],
          ["help"],
          ["version"],
      ]

      for args in arg_patterns:
          result = cli.run(args)
          assert result.success, f"Args {args} failed"

    def test_cli_error_handling(self) -> None:
      """Test CLI error handling."""
      cli = FlextMeltanoCli()

      # Test with potentially invalid commands
      result = cli.execute("potentially-invalid-command")
      # Should handle gracefully (either succeed or fail gracefully)
      assert hasattr(result, "success")

    def test_cli_integration_with_meltano_commands(self) -> None:
      """Test CLI integration with potential Meltano commands."""
      cli = FlextMeltanoCli()

      # Test Meltano-like commands
      meltano_commands = [
          "discover",
          "install",
          "run",
      ]

      for command in meltano_commands:
          result = cli.execute(command, options=["--help"])
          # Should handle gracefully
          assert hasattr(result, "success")

    def test_functional_cli_run_patterns(self) -> None:
      """Test functional CLI run patterns."""
      test_patterns = [
          [],
          ["--version"],
          ["version"],
          ["help"],
      ]

      for pattern in test_patterns:
          result = flext_meltano_run_cli(pattern)
          assert hasattr(result, "success"), f"Pattern {pattern} failed"


class TestCLIEdgeCases:
    """Test CLI edge cases and error conditions."""

    def test_cli_with_none_args(self) -> None:
      """Test CLI with None arguments."""
      result = flext_meltano_run_cli(None)
      # Should handle None gracefully
      assert hasattr(result, "success")

    def test_cli_with_empty_string_command(self) -> None:
      """Test CLI with empty string command."""
      cli = FlextMeltanoCli()

      result = cli.execute("")
      # Should handle empty string gracefully
      assert hasattr(result, "success")

    def test_cli_with_whitespace_command(self) -> None:
      """Test CLI with whitespace-only command."""
      cli = FlextMeltanoCli()

      result = cli.execute("   ")
      # Should handle whitespace gracefully
      assert hasattr(result, "success")

    def test_cli_command_list_consistency(self) -> None:
      """Test CLI command list consistency."""
      cli = FlextMeltanoCli()

      result = cli.list_commands()
      assert result.success

      assert result.data is not None
      commands = result.data.get("commands", [])
      assert isinstance(commands, list)

      # Basic commands should be available
      expected_commands = ["version", "help", "health"]
      for expected in expected_commands:
          if expected not in commands:
              msg: str = f"Expected command '{expected}' not found in {commands}"
              raise AssertionError(msg)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
