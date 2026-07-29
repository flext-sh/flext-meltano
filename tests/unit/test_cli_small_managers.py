"""Behavioral tests for the FLEXT Meltano CLI public run contract.

These tests exercise only the public surface ``FlextMeltanoCli().run(args)``,
which returns ``p.Result[bool]``, plus the text the CLI writes to stdout. No
private attributes, internal collaborators, or Typer application objects are
touched: the assertions describe the observable command contract only.
"""

from __future__ import annotations

import pytest

from flext_meltano.cli import FlextMeltanoCli
from flext_tests import tm
from tests import c, t, u

__all__: list[str] = ["TestsFlextMeltanoCliSmallManagers"]


class TestsFlextMeltanoCliSmallManagers:
    """Exercise the public ``run`` contract of the Meltano CLI facade."""

    @pytest.fixture
    def meltano_cli(self) -> FlextMeltanoCli:
        """Provide a freshly constructed CLI facade for each test."""
        return FlextMeltanoCli()

    def test_version_command_succeeds_and_prints_version_string(
        self, meltano_cli: FlextMeltanoCli, capsys: pytest.CaptureFixture[str]
    ) -> None:
        result = meltano_cli.run([c.Meltano.CliCommand.VERSION])

        tm.that(result.success, eq=True)
        tm.that("." in capsys.readouterr().out, eq=True)

    def test_status_show_succeeds_with_ready_status_payload(
        self, meltano_cli: FlextMeltanoCli, capsys: pytest.CaptureFixture[str]
    ) -> None:
        result = meltano_cli.run([c.Meltano.CliCommand.STATUS, "show"])

        tm.that(result.success, eq=True)

        parsed = u.Cli.json_loads(capsys.readouterr().out)
        tm.ok(parsed)

        payload = t.Cli.JSON_MAPPING_ADAPTER.validate_python(parsed.value)
        tm.that(payload.get("status"), eq=c.Meltano.OperationStatus.READY)

    def test_status_health_succeeds_with_status_key_in_payload(
        self, meltano_cli: FlextMeltanoCli, capsys: pytest.CaptureFixture[str]
    ) -> None:
        result = meltano_cli.run([
            c.Meltano.CliCommand.STATUS,
            c.Meltano.ExecutorCommand.HEALTH,
        ])

        tm.that(result.success, eq=True)

        parsed = u.Cli.json_loads(capsys.readouterr().out)
        tm.ok(parsed)

        payload = t.Cli.JSON_MAPPING_ADAPTER.validate_python(parsed.value)
        tm.that("status" in payload, eq=True)

    @pytest.mark.parametrize(
        "command", [c.Meltano.CliCommand.TAP, c.Meltano.CliCommand.TARGET]
    )
    def test_unsupported_extractor_operation_reports_failure(
        self, meltano_cli: FlextMeltanoCli, command: str
    ) -> None:
        result = meltano_cli.run([command, "--operation", "run", "--args", "demo"])

        tm.that(result.failure, eq=True)

    def test_plugin_info_without_plugin_type_reports_failure(
        self, meltano_cli: FlextMeltanoCli
    ) -> None:
        result = meltano_cli.run([
            c.Meltano.CliCommand.PLUGIN,
            c.Meltano.ExecutorCommand.INFO,
        ])

        tm.that(result.failure, eq=True)

    def test_plugin_install_is_unsupported_and_reports_failure(
        self, meltano_cli: FlextMeltanoCli, capsys: pytest.CaptureFixture[str]
    ) -> None:
        result = meltano_cli.run([
            c.Meltano.CliCommand.PLUGIN,
            c.Meltano.ExecutorCommand.INSTALL,
            "--plugin-name",
            "tap-demo",
        ])

        tm.that(result.failure, eq=True)
        tm.that(capsys.readouterr().out, has="not supported")

    def test_dbt_help_option_succeeds_and_prints_dbt_help(
        self, meltano_cli: FlextMeltanoCli, capsys: pytest.CaptureFixture[str]
    ) -> None:
        result = meltano_cli.run([c.Meltano.CliCommand.DBT, c.Meltano.CMD_HELP_OPTION])

        tm.that(result.success, eq=True)
        tm.that(capsys.readouterr().out, has="DBT")
