"""CLI Module Comprehensive Test Suite - Command Interface Layer Validation.

**Test Category**: Integration Tests
**Coverage Target**: 95%+ for CLI module components
**Dependencies**: Mock subprocess calls, temporary directories, FlextResult patterns
**Execution Time**: < 8 seconds total

## Test Scope

Validates the CLI module components that provide **command-line interface functionality**
for FLEXT Meltano's bridge architecture, focusing on direct CLI operations, version
management, and development command execution patterns.

## Test Coverage Areas

1. **CLI Initialization**: FlextMeltanoCli class initialization and configuration
2. **Version Operations**: Version information retrieval and formatting
3. **Command Execution**: CLI command orchestration with error handling
4. **Project Management**: Project root handling and path validation
5. **Bridge Integration**: CLI operations callable from bridge scripts
6. **Error Handling**: Command failures and subprocess error management

## Architecture Alignment

Tests align with FLEXT Meltano's CLI layer architecture:
- **Development Interface**: Direct CLI access for development workflows
- **Bridge Support**: CLI operations accessible via bridge scripts
- **Enterprise Error Handling**: FlextResult pattern validation throughout
- **Project Context**: Proper project root and environment management

These tests ensure the CLI module provides reliable command-line interface
functionality that supports both direct development usage and bridge integration.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from flext_core import FlextResult

from flext_meltano import FlextMeltanoCli, flext_meltano_run_cli


class TestFlextMeltanoCli:
    """Test FlextMeltanoCli class functionality."""

    def test_cli_initialization_default(self) -> None:
        """Test CLI initialization with default project root."""
        cli = FlextMeltanoCli()
        if cli.project_root != Path.cwd():
            msg: str = f"Expected {Path.cwd()}, got {cli.project_root}"
            raise AssertionError(msg)

    def test_cli_initialization_custom_path(self) -> None:
        """Test CLI initialization with custom project root."""
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_path = Path(temp_dir) / "test"
            cli = FlextMeltanoCli(project_root=custom_path)
            if cli.project_root != custom_path:
                msg: str = f"Expected {custom_path}, got {cli.project_root}"
                raise AssertionError(msg)

    def test_cli_initialization_none_path(self) -> None:
        """Test CLI initialization with None path."""
        cli = FlextMeltanoCli(project_root=None)
        if cli.project_root != Path.cwd():
            msg: str = f"Expected {Path.cwd()}, got {cli.project_root}"
            raise AssertionError(msg)

    def test_execute_empty_command(self) -> None:
        """Test execute with empty command."""
        cli = FlextMeltanoCli()
        result = cli.execute("")

        assert result.success
        assert result.value is not None
        if result.value["cli_type"] != "flext_meltano":
            msg: str = f"Expected {'flext_meltano'}, got {result.value['cli_type']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["project_root"] != str(cli.project_root):
            msg: str = (
                f"Expected {cli.project_root!s}, got {result.value['project_root']}"
            )
            raise AssertionError(msg)

    def test_execute_whitespace_command(self) -> None:
        """Test execute with whitespace-only command."""
        cli = FlextMeltanoCli()
        result = cli.execute("   ")

        assert result.success
        assert result.value is not None
        if result.value["cli_type"] != "flext_meltano":
            msg: str = f"Expected {'flext_meltano'}, got {result.value['cli_type']}"
            raise AssertionError(msg)

    def test_execute_version_command(self) -> None:
        """Test execute with version command."""
        cli = FlextMeltanoCli()
        result = cli.execute("version")

        assert result.success
        assert result.value is not None
        if result.value["version"] != "3.9.1":
            msg: str = f"Expected {'3.9.1'}, got {result.value['version']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["cli_type"] != "flext_meltano":
            msg: str = f"Expected {'flext_meltano'}, got {result.value['cli_type']}"
            raise AssertionError(msg)

    def test_execute_help_command(self) -> None:
        """Test execute with help command."""
        cli = FlextMeltanoCli()
        result = cli.execute("help")

        assert result.success
        assert result.value is not None
        assert result.value is not None
        if "commands" not in result.value:
            msg: str = f"Expected {'commands'} in {result.value}"
            raise AssertionError(msg)
        assert "version" in result.value["commands"]
        if result.value["cli_type"] != "flext_meltano":
            msg: str = f"Expected {'flext_meltano'}, got {result.value['cli_type']}"
            raise AssertionError(msg)

    def test_execute_health_command(self) -> None:
        """Test execute with health command."""
        cli = FlextMeltanoCli()
        result = cli.execute("health")

        assert result.success
        assert result.value is not None
        if result.value["status"] != "healthy":
            msg: str = f"Expected {'healthy'}, got {result.value['status']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["project_root"] != str(cli.project_root):
            msg: str = (
                f"Expected {cli.project_root!s}, got {result.value['project_root']}"
            )
            raise AssertionError(msg)

    def test_execute_discover_command(self) -> None:
        """Test execute with discover command."""
        cli = FlextMeltanoCli()
        result = cli.execute("discover", ["--all"])

        assert result.success
        assert result.value is not None
        if result.value["command"] != "discover":
            msg: str = f"Expected {'discover'}, got {result.value['command']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["options"] != ["--all"]:
            msg: str = f"Expected {['--all']}, got {result.value['options']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["status"] != "success":
            msg: str = f"Expected {'success'}, got {result.value['status']}"
            raise AssertionError(msg)

    def test_execute_install_command(self) -> None:
        """Test execute with install command."""
        cli = FlextMeltanoCli()
        result = cli.execute("install", ["tap-csv"])

        assert result.success
        assert result.value is not None
        if result.value["command"] != "install":
            msg: str = f"Expected {'install'}, got {result.value['command']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["options"] != ["tap-csv"]:
            msg: str = f"Expected {['tap-csv']}, got {result.value['options']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["status"] != "success":
            msg: str = f"Expected {'success'}, got {result.value['status']}"
            raise AssertionError(msg)

    def test_execute_run_command(self) -> None:
        """Test execute with run command."""
        cli = FlextMeltanoCli()
        result = cli.execute("run", ["tap-csv", "target-jsonl"])

        assert result.success
        assert result.value is not None
        if result.value["command"] != "run":
            msg: str = f"Expected {'run'}, got {result.value['command']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["options"] != ["tap-csv", "target-jsonl"]:
            msg = (
                f"Expected {['tap-csv', 'target-jsonl']}, got {result.value['options']}"
            )
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["status"] != "success":
            msg: str = f"Expected {'success'}, got {result.value['status']}"
            raise AssertionError(msg)

    def test_execute_unknown_command(self) -> None:
        """Test execute with unknown command."""
        cli = FlextMeltanoCli()
        result = cli.execute("unknown-command", ["arg1", "arg2"])

        assert result.success
        assert result.value is not None
        if result.value["command"] != "unknown-command":
            msg: str = f"Expected {'unknown-command'}, got {result.value['command']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["status"] != "unknown_command":
            msg: str = f"Expected {'unknown_command'}, got {result.value['status']}"
            raise AssertionError(msg)

    def test_execute_with_none_options(self) -> None:
        """Test execute with None options."""
        cli = FlextMeltanoCli()
        result = cli.execute("version", None)

        assert result.success
        assert result.value is not None
        if result.value["version"] != "3.9.1":
            msg: str = f"Expected {'3.9.1'}, got {result.value['version']}"
            raise AssertionError(msg)


class TestFlextMeltanoCliMethodsDirectly:
    """Test FlextMeltanoCli methods directly."""

    def test_health_method(self) -> None:
        """Test health method directly."""
        cli = FlextMeltanoCli()
        result = cli.health()

        assert result.success
        assert result.value is not None
        if result.value["status"] != "healthy":
            msg: str = f"Expected {'healthy'}, got {result.value['status']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["project_root"] != str(cli.project_root):
            msg: str = (
                f"Expected {cli.project_root!s}, got {result.value['project_root']}"
            )
            raise AssertionError(msg)

    def test_version_method(self) -> None:
        """Test version method directly."""
        cli = FlextMeltanoCli()
        result = cli.version()

        assert result.success
        assert result.value is not None
        if result.value["version"] != "3.9.1":
            msg: str = f"Expected {'3.9.1'}, got {result.value['version']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["cli_type"] != "flext_meltano":
            msg: str = f"Expected {'flext_meltano'}, got {result.value['cli_type']}"
            raise AssertionError(msg)

    def test_help_method(self) -> None:
        """Test help method directly."""
        cli = FlextMeltanoCli()
        result = cli.help()

        assert result.success
        assert result.value is not None
        if "commands" not in result.value:
            msg: str = f"Expected {'commands'} in {result.value}"
            raise AssertionError(msg)
        expected_commands = ["version", "help", "health", "run", "discover", "install"]
        assert result.value is not None
        if result.value["commands"] != expected_commands:
            msg: str = f"Expected {expected_commands}, got {result.value['commands']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["cli_type"] != "flext_meltano":
            msg: str = f"Expected {'flext_meltano'}, got {result.value['cli_type']}"
            raise AssertionError(msg)

    def test_run_empty_args(self) -> None:
        """Test run method with empty args."""
        cli = FlextMeltanoCli()
        result = cli.run([])

        assert result.success
        assert result.value is not None
        if result.value["status"] != "success":
            msg: str = f"Expected {'success'}, got {result.value['status']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["args"] != []:
            msg: str = f"Expected {[]}, got {result.value['args']}"
            raise AssertionError(msg)

    def test_run_version_flag(self) -> None:
        """Test run method with --version flag."""
        cli = FlextMeltanoCli()
        result = cli.run(["--version"])

        assert result.success
        assert result.value is not None
        if result.value["version"] != "3.9.1":
            msg: str = f"Expected {'3.9.1'}, got {result.value['version']}"
            raise AssertionError(msg)

    def test_run_help_flag(self) -> None:
        """Test run method with --help flag."""
        cli = FlextMeltanoCli()
        result = cli.run(["--help"])

        assert result.success
        assert result.value is not None
        if "commands" not in result.value:
            msg: str = f"Expected {'commands'} in {result.value}"
            raise AssertionError(msg)

    def test_run_help_command(self) -> None:
        """Test run method with help command."""
        cli = FlextMeltanoCli()
        result = cli.run(["help"])

        assert result.success
        assert result.value is not None
        if "commands" not in result.value:
            msg: str = f"Expected {'commands'} in {result.value}"
            raise AssertionError(msg)

    def test_run_version_command(self) -> None:
        """Test run method with version command."""
        cli = FlextMeltanoCli()
        result = cli.run(["version"])

        assert result.success
        assert result.value is not None
        if result.value["version"] != "3.9.1":
            msg: str = f"Expected {'3.9.1'}, got {result.value['version']}"
            raise AssertionError(msg)

    def test_run_custom_args(self) -> None:
        """Test run method with custom arguments."""
        cli = FlextMeltanoCli()
        args = ["install", "tap-csv"]
        result = cli.run(args)

        assert result.success
        assert result.value is not None
        if result.value["status"] != "success":
            msg: str = f"Expected {'success'}, got {result.value['status']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["args"] != args:
            msg: str = f"Expected {args}, got {result.value['args']}"
            raise AssertionError(msg)

    def test_list_commands(self) -> None:
        """Test list_commands method."""
        cli = FlextMeltanoCli()
        result = cli.list_commands()

        assert result.success
        expected_commands = ["version", "help", "health", "run", "discover", "install"]
        assert result.value is not None
        if result.value["commands"] != expected_commands:
            msg: str = f"Expected {expected_commands}, got {result.value['commands']}"
            raise AssertionError(msg)


class TestFlextMeltanoCliSubprocessOperations:
    """Test FlextMeltanoCli subprocess operations."""

    @patch("subprocess.run")
    def test_flext_meltano_run_command_success(self, mock_run: Mock) -> None:
        """Test flext_meltano_run_command success."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Meltano, version 3.9.1"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        cli = FlextMeltanoCli()
        result = cli.flext_meltano_run_command(["--version"])

        assert result.success
        assert result.value is not None
        if not (result.value["success"]):
            msg: str = f"Expected True, got {result.value['success']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["command"] != "meltano --version":
            msg: str = f"Expected {'meltano --version'}, got {result.value['command']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["stdout"] != "Meltano, version 3.9.1":
            msg: str = (
                f"Expected {'Meltano, version 3.9.1'}, got {result.value['stdout']}"
            )
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["returncode"] != 0:
            msg: str = f"Expected {0}, got {result.value['returncode']}"
            raise AssertionError(msg)

    @patch("subprocess.run")
    def test_flext_meltano_run_command_failure(self, mock_run: Mock) -> None:
        """Test flext_meltano_run_command failure."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Command failed"
        mock_run.return_value = mock_result

        cli = FlextMeltanoCli()
        result = cli.flext_meltano_run_command(["invalid-command"])

        assert not result.success
        assert result.error is not None
        if "Command failed" not in result.error:
            msg: str = f"Expected {'Command failed'} in {result.error}"
            raise AssertionError(msg)
        if result.error_data["success"]:
            msg: str = f"Expected False, got {result.error_data['success']}"
            raise AssertionError(msg)
        assert result.error_data["returncode"] == 1

    @patch("subprocess.run")
    def test_flext_meltano_run_command_timeout(self, mock_run: Mock) -> None:
        """Test flext_meltano_run_command timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired("meltano", 300)

        cli = FlextMeltanoCli()
        result = cli.flext_meltano_run_command(["long-running-command"])

        assert not result.success
        assert result.error is not None
        if "Command timed out" not in result.error:
            msg: str = f"Expected {'Command timed out'} in {result.error}"
            raise AssertionError(msg)

    @patch("subprocess.run")
    def test_flext_meltano_run_command_os_error(self, mock_run: Mock) -> None:
        """Test flext_meltano_run_command OSError."""
        mock_run.side_effect = OSError("Command not found")

        cli = FlextMeltanoCli()
        result = cli.flext_meltano_run_command(["nonexistent"])

        assert not result.success
        assert result.error is not None
        if "Command error" not in result.error:
            msg: str = f"Expected {'Command error'} in {result.error}"
            raise AssertionError(msg)

    @patch("subprocess.run")
    def test_flext_meltano_run_command_subprocess_error(self, mock_run: Mock) -> None:
        """Test flext_meltano_run_command SubprocessError."""
        mock_run.side_effect = subprocess.SubprocessError("Subprocess failed")

        cli = FlextMeltanoCli()
        result = cli.flext_meltano_run_command(["failing-command"])

        assert not result.success
        assert result.error is not None
        if "Command error" not in result.error:
            msg: str = f"Expected {'Command error'} in {result.error}"
            raise AssertionError(msg)

    @patch("flext_meltano.cli.FlextMeltanoCli.flext_meltano_run_command")
    def test_flext_meltano_version_success(self, mock_run_command: Mock) -> None:
        """Test flext_meltano_version success."""
        mock_run_command.return_value = FlextResult(
            data={
                "success": True,
                "stdout": "Meltano, version 3.9.1",
                "returncode": 0,
            },
        )

        cli = FlextMeltanoCli()
        result = cli.flext_meltano_version()

        assert result.success
        if result.value != "Meltano, version 3.9.1":
            msg: str = f"Expected {'Meltano, version 3.9.1'}, got {result.value}"
            raise AssertionError(msg)

    @patch("flext_meltano.cli.FlextMeltanoCli.flext_meltano_run_command")
    def test_flext_meltano_version_failure(self, mock_run_command: Mock) -> None:
        """Test flext_meltano_version failure."""
        mock_run_command.return_value = FlextResult(error="Command failed")

        cli = FlextMeltanoCli()
        result = cli.flext_meltano_version()

        assert not result.success
        if result.error != "Command failed":
            msg: str = f"Expected {'Command failed'}, got {result.error}"
            raise AssertionError(msg)

    @patch("flext_meltano.cli.FlextMeltanoCli.flext_meltano_run_command")
    def test_flext_meltano_version_no_data(self, mock_run_command: Mock) -> None:
        """Test flext_meltano_version with no data."""
        mock_run_command.return_value = FlextResult(data=None)

        cli = FlextMeltanoCli()
        result = cli.flext_meltano_version()

        assert result.success
        if result.value != "unknown":
            msg: str = f"Expected {'unknown'}, got {result.value}"
            raise AssertionError(msg)

    @patch("flext_meltano.cli.FlextMeltanoCli.flext_meltano_run_command")
    def test_flext_meltano_install_success(self, mock_run_command: Mock) -> None:
        """Test flext_meltano_install success."""
        mock_run_command.return_value = FlextResult(data={"success": True})

        cli = FlextMeltanoCli()
        result = cli.flext_meltano_install()

        assert result.success
        if not (result.value):
            msg: str = f"Expected True, got {result.value}"
            raise AssertionError(msg)

    @patch("flext_meltano.cli.FlextMeltanoCli.flext_meltano_run_command")
    def test_flext_meltano_install_failure(self, mock_run_command: Mock) -> None:
        """Test flext_meltano_install failure."""
        mock_run_command.return_value = FlextResult(error="Install failed")

        cli = FlextMeltanoCli()
        result = cli.flext_meltano_install()

        assert result.success
        if result.value:
            msg: str = f"Expected False, got {result.value}"
            raise AssertionError(msg)

    @patch("flext_meltano.cli.FlextMeltanoCli.flext_meltano_run_command")
    def test_flext_meltano_invoke_success(self, mock_run_command: Mock) -> None:
        """Test flext_meltano_invoke success."""
        expected_result = FlextResult(
            data={"success": True, "output": "Plugin invoked"},
        )
        mock_run_command.return_value = expected_result

        cli = FlextMeltanoCli()
        result = cli.flext_meltano_invoke("tap-csv", "--discover")

        assert result.success
        assert result.value is not None
        if not (result.value["success"]):
            msg: str = f"Expected True, got {result.value['success']}"
            raise AssertionError(msg)
        mock_run_command.assert_called_once_with(["invoke", "tap-csv", "--discover"])

    @patch("flext_meltano.cli.FlextMeltanoCli.flext_meltano_run_command")
    def test_flext_meltano_invoke_no_args(self, mock_run_command: Mock) -> None:
        """Test flext_meltano_invoke without additional args."""
        expected_result = FlextResult(data={"success": True})
        mock_run_command.return_value = expected_result

        cli = FlextMeltanoCli()
        result = cli.flext_meltano_invoke("tap-csv")

        assert result.success
        mock_run_command.assert_called_once_with(["invoke", "tap-csv"])

    @patch("flext_meltano.cli.FlextMeltanoCli.flext_meltano_run_command")
    def test_flext_meltano_invoke_multiple_args(self, mock_run_command: Mock) -> None:
        """Test flext_meltano_invoke with multiple args."""
        expected_result = FlextResult(data={"success": True})
        mock_run_command.return_value = expected_result

        cli = FlextMeltanoCli()
        result = cli.flext_meltano_invoke("tap-csv", "--discover", "--format", "json")

        assert result.success
        mock_run_command.assert_called_once_with(
            ["invoke", "tap-csv", "--discover", "--format", "json"],
        )


class TestFlextMeltanoCliFactory:
    """Test flext_meltano_run_cli factory function."""

    def test_flext_meltano_run_cli_no_args(self) -> None:
        """Test flext_meltano_run_cli with no args."""
        result = flext_meltano_run_cli()

        assert result.success
        assert result.value is not None
        if result.value["status"] != "success":
            msg: str = f"Expected {'success'}, got {result.value['status']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["args"] != []:
            msg: str = f"Expected {[]}, got {result.value['args']}"
            raise AssertionError(msg)

    def test_flext_meltano_run_cli_empty_args(self) -> None:
        """Test flext_meltano_run_cli with empty args."""
        result = flext_meltano_run_cli([])

        assert result.success
        assert result.value is not None
        if result.value["status"] != "success":
            msg: str = f"Expected {'success'}, got {result.value['status']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["args"] != []:
            msg: str = f"Expected {[]}, got {result.value['args']}"
            raise AssertionError(msg)

    def test_flext_meltano_run_cli_version_args(self) -> None:
        """Test flext_meltano_run_cli with version args."""
        result = flext_meltano_run_cli(["--version"])

        assert result.success
        assert result.value is not None
        if result.value["version"] != "3.9.1":
            msg: str = f"Expected {'3.9.1'}, got {result.value['version']}"
            raise AssertionError(msg)

    def test_flext_meltano_run_cli_custom_args(self) -> None:
        """Test flext_meltano_run_cli with custom args."""
        args = ["install", "tap-postgres"]
        result = flext_meltano_run_cli(args)

        assert result.success
        assert result.value is not None
        if result.value["args"] != args:
            msg: str = f"Expected {args}, got {result.value['args']}"
            raise AssertionError(msg)

    @patch("flext_meltano.cli.FlextMeltanoCli.__init__")
    def test_flext_meltano_run_cli_value_error(self, mock_init: Mock) -> None:
        """Test flext_meltano_run_cli with ValueError."""
        mock_init.side_effect = ValueError("Initialization failed")

        result = flext_meltano_run_cli(["test"])

        assert not result.success
        assert result.error is not None
        if "CLI execution failed" not in result.error:
            msg: str = f"Expected {'CLI execution failed'} in {result.error}"
            raise AssertionError(msg)

    @patch("flext_meltano.cli.FlextMeltanoCli.__init__")
    def test_flext_meltano_run_cli_type_error(self, mock_init: Mock) -> None:
        """Test flext_meltano_run_cli with TypeError."""
        mock_init.side_effect = TypeError("Type mismatch")

        result = flext_meltano_run_cli(["test"])

        assert not result.success
        assert result.error is not None
        if "CLI execution failed" not in result.error:
            msg: str = f"Expected {'CLI execution failed'} in {result.error}"
            raise AssertionError(msg)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
