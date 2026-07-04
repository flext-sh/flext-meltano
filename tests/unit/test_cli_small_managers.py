"""Real-execution tests for small Meltano CLI command handlers."""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_cli import cli
from flext_meltano.cli import FlextMeltanoCli
from tests.constants import c
from tests.typings import t
from tests.utilities import u


class TestsFlextMeltanoCliSmallManagers:
    """Exercise the public CLI handlers through a Typer CliRunner."""

    @pytest.fixture
    def runner(self) -> t.Cli.TyperRunner:
        """Provide a fresh CliRunner for each test."""
        runner_result = cli.create_cli_runner()
        tm.ok(runner_result)
        return runner_result.value

    @pytest.fixture
    def app(self) -> t.Cli.CliApp:
        """Provide the compiled Typer application under test."""
        return FlextMeltanoCli()._app

    def test_version_command_returns_real_version_string(
        self,
        runner: t.Cli.TyperRunner,
        app: t.Cli.CliApp,
    ) -> None:
        result = runner.invoke(app, [c.Meltano.CliCommand.VERSION])

        tm.that(result.exit_code, eq=0)
        tm.that("." in result.output, eq=True)

    def test_status_commands_return_json_payloads(
        self,
        runner: t.Cli.TyperRunner,
        app: t.Cli.CliApp,
    ) -> None:
        show_result = runner.invoke(app, [
            c.Meltano.CliCommand.STATUS,
            "show",
        ])
        health_result = runner.invoke(app, [
            c.Meltano.CliCommand.STATUS,
            c.Meltano.ExecutorCommand.HEALTH,
        ])

        tm.that(show_result.exit_code, eq=0)
        tm.that(health_result.exit_code, eq=0)

        show_json = u.Cli.json_loads(show_result.output)
        health_json = u.Cli.json_loads(health_result.output)

        tm.ok(show_json)
        tm.ok(health_json)

        show_payload = t.Cli.JSON_MAPPING_ADAPTER.validate_python(show_json.value)
        health_payload = t.Cli.JSON_MAPPING_ADAPTER.validate_python(health_json.value)

        tm.that(show_payload.get("status"), eq=c.Meltano.OperationStatus.READY)
        tm.that("status" in health_payload, eq=True)

    def test_tap_and_target_commands_fail_for_unsupported_operations(
        self,
        runner: t.Cli.TyperRunner,
        app: t.Cli.CliApp,
    ) -> None:
        tap_result = runner.invoke(app, [
            c.Meltano.CliCommand.TAP,
            "--operation",
            "run",
            "--args",
            "tap-demo",
        ])
        target_result = runner.invoke(app, [
            c.Meltano.CliCommand.TARGET,
            "--operation",
            "run",
            "--args",
            "target-demo",
        ])

        tm.that(tap_result.exit_code, eq=1)
        tm.that(target_result.exit_code, eq=1)
        tm.that(tap_result.output, has="not supported")
        tm.that(target_result.output, has="not supported")

    def test_plugin_commands_enforce_real_argument_contracts(
        self,
        runner: t.Cli.TyperRunner,
        app: t.Cli.CliApp,
    ) -> None:
        info_result = runner.invoke(app, [
            c.Meltano.CliCommand.PLUGIN,
            c.Meltano.ExecutorCommand.INFO,
        ])
        install_result = runner.invoke(app, [
            c.Meltano.CliCommand.PLUGIN,
            c.Meltano.ExecutorCommand.INSTALL,
            "--plugin-name",
            "tap-demo",
        ])

        tm.that(info_result.exit_code, eq=1)
        tm.that(install_result.exit_code, eq=1)
        tm.that(info_result.output, has="required")
        tm.that(install_result.output, has="not supported")

    def test_dbt_help_path_returns_help_output(
        self,
        runner: t.Cli.TyperRunner,
        app: t.Cli.CliApp,
    ) -> None:
        result = runner.invoke(app, [c.Meltano.CliCommand.DBT, c.Meltano.CMD_HELP_OPTION])

        tm.that(result.exit_code, eq=0)
        tm.that(result.output, has="DBT")

    def test_route_command_prints_real_version_output(
        self,
        runner: t.Cli.TyperRunner,
        app: t.Cli.CliApp,
    ) -> None:
        result = runner.invoke(app, [c.Meltano.CliCommand.VERSION])

        tm.that(result.exit_code, eq=0)
        tm.that(result.output, has=".")
