"""Real-execution tests for the Meltano public executor surface."""

from __future__ import annotations

from pathlib import Path

from flext_meltano import meltano
from flext_meltano.cli import cli


class TestsFlextMeltanoExecutors:
    """Validate the public executor APIs through real Meltano execution paths."""

    def test_executor_initialization(self) -> None:
        """The public Meltano facade is available as a singleton executor."""
        assert meltano is not None

    def test_run_command_no_args_returns_one(self) -> None:
        """Empty command execution returns the CLI failure exit code."""
        result = meltano.run_command([])

        assert result.success
        assert result.value == 1

    def test_run_version_and_help_commands_return_payloads(self) -> None:
        """Version and help route through the real public command runner."""
        version_result = meltano.run(["version"])
        help_result = meltano.run(["help"])

        assert version_result.success
        assert help_result.success
        assert version_result.value["command"] == "version"
        assert "version" in version_result.value
        assert "Usage: meltano" in str(help_result.value["help"])

    def test_run_method_empty_args_fails(self) -> None:
        """Empty public run requests fail with the documented validation message."""
        result = meltano.run([])

        assert result.failure
        assert result.error is not None
        assert "cannot be empty" in result.error.lower()

    def test_health_version_help_and_execute_surfaces(self) -> None:
        """Health, version, help, and execute expose stable public payloads."""
        health_result = meltano.health()
        version_result = meltano.version()
        help_result = meltano.help()
        execute_result = meltano.execute()

        assert health_result.success
        assert version_result.success
        assert help_result.success
        assert execute_result.success
        assert health_result.value["health"] == "OK"
        assert health_result.value["status"] == "healthy"
        assert version_result.value["command"] == "version"
        assert version_result.value["cli_type"] == "flext_meltano"
        assert "Usage: meltano" in str(help_result.value["help"])
        assert execute_result.value["service_name"] == meltano.service_name
        assert execute_result.value["status"] == "active"

    def test_fetch_version_and_run_cli_surfaces(self) -> None:
        """Version lookup and CLI entrypoints stay available through the public facade."""
        fetch_result = meltano.fetch_version()
        ready_none_result = meltano.run_cli(None)
        ready_empty_result = meltano.run_cli([])
        version_cli_result = meltano.run_cli(["version"])

        assert fetch_result.success
        assert ready_none_result.success
        assert ready_empty_result.success
        assert version_cli_result.success
        assert isinstance(fetch_result.value, str)
        assert ready_none_result.value["status"] == "ready"
        assert ready_empty_result.value["status"] == "ready"
        assert version_cli_result.value["command"] == "version"

    def test_create_cli_runner_surfaces(self) -> None:
        """CLI runner creation returns ready and version payloads through public APIs."""
        ready_result = meltano.create_cli_runner([])
        version_result = meltano.create_cli_runner(["version"])

        assert ready_result.success
        assert version_result.success
        assert ready_result.value["command_type"] == "cli_runner"
        assert ready_result.value["status"] == "ready"
        assert version_result.value["command"] == "version"

    def test_execute_meltano_command_normalizes_runtime_commands(self) -> None:
        """Executor runtime commands normalize both prefixed and unprefixed forms."""
        prefixed_result = meltano.execute_meltano_command(["meltano", "version"])
        unprefixed_result = meltano.execute_meltano_command(["help"])

        assert prefixed_result.success
        assert unprefixed_result.success
        assert prefixed_result.value.success is True
        assert unprefixed_result.value.success is True
        assert prefixed_result.value.command[0] == "--version"
        assert unprefixed_result.value.command[0] == "--help"

    def test_execute_meltano_command_rejects_empty_command(self) -> None:
        """Executor runtime commands fail fast on an empty command sequence."""
        result = meltano.execute_meltano_command([])

        assert result.failure
        assert result.error is not None
        assert "empty" in result.error.lower()

    def test_multiple_version_calls_are_repeatable(self) -> None:
        """Repeated version queries stay stable across multiple real calls."""
        for _ in range(3):
            result = meltano.version()
            assert result.success
            assert result.value["command"] == "version"

    def test_project_root_property_returns_path(self) -> None:
        """Executor project_root remains a concrete filesystem path."""
        assert isinstance(meltano.project_root, Path)

    def test_cli_uses_flat_public_handlers(self) -> None:
        """The public CLI exposes only the flat handler surface exercised by tests."""
        assert callable(cli.handle_pipeline_command)
        assert callable(cli.handle_tap_command)
        assert callable(cli.handle_target_command)
        assert callable(cli.handle_dbt_command)
        assert callable(cli.handle_plugin_command)
        assert callable(cli.handle_status_command)
        assert callable(cli.handle_version_command)
