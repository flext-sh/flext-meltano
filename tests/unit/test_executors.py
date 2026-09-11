"""Real-execution tests for the Meltano public executor surface."""

from __future__ import annotations

from pathlib import Path

from flext_tests import tm

from flext_meltano import meltano
from flext_meltano.cli import FlextMeltanoCli


class TestsFlextMeltanoExecutors:
    """Validate the public executor APIs through real Meltano execution paths."""

    def test_executor_initialization(self) -> None:
        """The public Meltano facade is available as a singleton executor."""
        tm.that(meltano, none=False)

    def test_run_command_no_args_returns_one(self) -> None:
        """Empty command execution returns the CLI failure exit code."""
        result = meltano.run_command([])

        tm.ok(result)
        tm.that(result.value, eq=1)

    def test_run_version_and_help_commands_return_payloads(self) -> None:
        """Version and help route through the real public command runner."""
        version_result = meltano.run(["version"])
        help_result = meltano.run(["help"])

        tm.ok(version_result)
        tm.ok(help_result)
        tm.that(version_result.value["command"], eq="version")
        tm.that(version_result.value, has="version")
        tm.that(str(help_result.value["help"]), has="Usage: meltano")

    def test_run_method_empty_args_fails(self) -> None:
        """Empty public run requests fail with the documented validation message."""
        result = meltano.run([])

        tm.fail(result, has="cannot be empty")

    def test_health_version_help_and_execute_surfaces(self) -> None:
        """Health, version, help, and execute expose stable public payloads."""
        health_result = meltano.health()
        version_result = meltano.version()
        help_result = meltano.help()
        execute_result = meltano.execute()

        tm.ok(health_result)
        tm.ok(version_result)
        tm.ok(help_result)
        tm.ok(execute_result)
        tm.that(health_result.value["health"], eq="OK")
        tm.that(health_result.value["status"], eq="healthy")
        tm.that(version_result.value["command"], eq="version")
        tm.that(version_result.value["cli_type"], eq="flext_meltano")
        tm.that(str(help_result.value["help"]), has="Usage: meltano")
        tm.that(execute_result.value["service_name"], eq=meltano.service_name)
        tm.that(execute_result.value["status"], eq="active")

    def test_fetch_version_and_run_cli_surfaces(self) -> None:
        """Version lookup and CLI entrypoints stay available through the public facade."""
        fetch_result = meltano.fetch_version()
        ready_none_result = meltano.run_cli(None)
        ready_empty_result = meltano.run_cli([])
        version_cli_result = meltano.run_cli(["version"])

        tm.ok(fetch_result)
        tm.ok(ready_none_result)
        tm.ok(ready_empty_result)
        tm.ok(version_cli_result)
        tm.that(fetch_result.value, is_=str)
        tm.that(ready_none_result.value["status"], eq="ready")
        tm.that(ready_empty_result.value["status"], eq="ready")
        tm.that(version_cli_result.value["command"], eq="version")

    def test_create_cli_runner_surfaces(self) -> None:
        """CLI runner creation returns ready and version payloads through public APIs."""
        ready_result = meltano.create_cli_runner([])
        version_result = meltano.create_cli_runner(["version"])

        tm.ok(ready_result)
        tm.ok(version_result)
        tm.that(ready_result.value["command_type"], eq="cli_runner")
        tm.that(ready_result.value["status"], eq="ready")
        tm.that(version_result.value["command"], eq="version")

    def test_execute_meltano_command_normalizes_runtime_commands(self) -> None:
        """Executor runtime commands normalize both prefixed and unprefixed forms."""
        prefixed_result = meltano.execute_meltano_command(["meltano", "version"])
        unprefixed_result = meltano.execute_meltano_command(["help"])

        tm.ok(prefixed_result)
        tm.ok(unprefixed_result)
        tm.that(prefixed_result.value.success, eq=True)
        tm.that(unprefixed_result.value.success, eq=True)
        tm.that(prefixed_result.value.command[0], eq="--version")
        tm.that(unprefixed_result.value.command[0], eq="--help")

    def test_execute_meltano_command_rejects_empty_command(self) -> None:
        """Executor runtime commands fail fast on an empty command sequence."""
        result = meltano.execute_meltano_command([])

        tm.fail(result, has="empty")

    def test_multiple_version_calls_are_repeatable(self) -> None:
        """Repeated version queries stay stable across multiple real calls."""
        for _ in range(3):
            result = meltano.version()
            tm.ok(result)
            tm.that(result.value["command"], eq="version")

    def test_project_root_property_returns_path(self) -> None:
        """Executor project_root remains a concrete filesystem path."""
        tm.that(meltano.project_root, is_=Path)

    def test_cli_run_version_returns_successful_result(self) -> None:
        """The public CLI runs the version command and returns a successful result."""
        cli_instance = FlextMeltanoCli()

        result = cli_instance.run(["version"])

        tm.ok(result)
        tm.that(result.value, eq=True)
