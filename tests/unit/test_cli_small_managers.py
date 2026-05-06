"""Real-execution tests for small Meltano CLI command handlers."""

from __future__ import annotations

import re

import pytest
from flext_tests import tm

from flext_meltano.cli import FlextMeltanoCLI, cli
from tests import c, t, u


class TestsFlextMeltanoCliSmallManagers:
    """Exercise the public CLI handlers without mocks or monkeypatching."""

    def test_version_command_returns_real_version_string(self) -> None:
        result = FlextMeltanoCLI.fetch_global().handle_version_command([])

        tm.ok(result)
        tm.that("." in result.value, eq=True)

    def test_status_commands_return_json_payloads(self) -> None:
        cli_instance = FlextMeltanoCLI.fetch_global()

        show_result = cli_instance.handle_status_command(["show"])
        health_result = cli_instance.handle_status_command([
            c.Meltano.ExecutorCommand.HEALTH
        ])

        tm.ok(show_result)
        tm.ok(health_result)

        show_json = u.Cli.json_loads(show_result.value)
        health_json = u.Cli.json_loads(health_result.value)

        tm.ok(show_json)
        tm.ok(health_json)

        show_payload = t.Cli.JSON_MAPPING_ADAPTER.validate_python(show_json.value)
        health_payload = t.Cli.JSON_MAPPING_ADAPTER.validate_python(health_json.value)

        tm.that(show_payload.get("status"), eq=c.Meltano.OperationStatus.READY)
        tm.that("status" in health_payload, eq=True)

    def test_tap_and_target_commands_fail_for_unsupported_operations(self) -> None:
        cli_instance = FlextMeltanoCLI.fetch_global()

        tap_result = cli_instance.handle_tap_command(["run", "tap-demo"])
        target_result = cli_instance.handle_target_command(["run", "target-demo"])

        tm.fail(tap_result)
        tm.fail(target_result)
        tm.that(str(tap_result.error), has="not supported")
        tm.that(str(target_result.error), has="not supported")

    def test_plugin_commands_enforce_real_argument_contracts(self) -> None:
        cli_instance = FlextMeltanoCLI.fetch_global()

        info_result = cli_instance.handle_plugin_command(["info"])
        install_result = cli_instance.handle_plugin_command([
            c.Meltano.ExecutorCommand.INSTALL,
            "extractors",
            "tap-demo",
        ])

        tm.fail(info_result)
        tm.fail(install_result)
        tm.that(str(info_result.error), has="requires")
        tm.that(str(install_result.error), has="not supported")

    def test_dbt_help_path_returns_help_sentinel(self) -> None:
        result = FlextMeltanoCLI.fetch_global().handle_dbt_command([
            c.Meltano.CMD_HELP_OPTION
        ])

        tm.ok(result)
        tm.that(result.value, eq=c.Meltano.ExecutorCommand.HELP)

    def test_route_command_prints_real_version_output(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        version_result = cli.handle_version_command([])

        tm.ok(version_result)

        exit_code = cli.route_command([c.Meltano.CliCommand.VERSION])
        captured = capsys.readouterr()
        normalized_output = re.sub(r"\x1b\[[0-9;]*m", "", captured.out)

        tm.that(exit_code, eq=0)
        tm.that(normalized_output, has=version_result.value)
