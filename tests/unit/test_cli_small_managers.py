"""Behavioral tests for the FLEXT Meltano CLI public run contract.

These tests exercise only the public surface ``FlextMeltanoCli().run(args)``,
which returns ``p.Result[bool]``, plus the text the CLI writes to stdout. No
private attributes, internal collaborators, or Typer application objects are
touched: the assertions describe the observable command contract only.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_meltano.cli import FlextMeltanoCli
from tests import c, t, u


class TestsFlextMeltanoCliSmallManagers:
    """Exercise the public ``run`` contract of the Meltano CLI facade."""

    @staticmethod
    @pytest.fixture
    def meltano_cli() -> FlextMeltanoCli:
        """Provide a freshly constructed CLI facade for each test.

        Returns:
            The resulting ``FlextMeltanoCli``.
        """
        return FlextMeltanoCli()

    @staticmethod
    def test_version_command_succeeds_and_prints_version_string(
        meltano_cli: FlextMeltanoCli,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test version command succeeds and prints version string."""
        result = meltano_cli.run([c.Meltano.CliCommand.VERSION])

        tm.that(result.success, eq=True)
        tm.that("." in capsys.readouterr().out, eq=True)

    @staticmethod
    def test_status_show_succeeds_with_ready_status_payload(
        meltano_cli: FlextMeltanoCli,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test status show succeeds with ready status payload."""
        result = meltano_cli.run([c.Meltano.CliCommand.STATUS, "show"])

        tm.that(result.success, eq=True)

        parsed = u.Cli.json_loads(capsys.readouterr().out)
        tm.ok(parsed)

        payload = t.Cli.JSON_MAPPING_ADAPTER.validate_python(parsed.value)
        tm.that(payload.get("status"), eq=c.Meltano.OperationStatus.READY)

    @staticmethod
    def test_status_health_succeeds_with_status_key_in_payload(
        meltano_cli: FlextMeltanoCli,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test status health succeeds with status key in payload."""
        result = meltano_cli.run([
            c.Meltano.CliCommand.STATUS,
            c.Meltano.ExecutorCommand.HEALTH,
        ])

        tm.that(result.success, eq=True)

        parsed = u.Cli.json_loads(capsys.readouterr().out)
        tm.ok(parsed)

        payload = t.Cli.JSON_MAPPING_ADAPTER.validate_python(parsed.value)
        tm.that("status" in payload, eq=True)

    @staticmethod
    @pytest.mark.parametrize(
        "command",
        [c.Meltano.CliCommand.TAP, c.Meltano.CliCommand.TARGET],
    )
    def test_unsupported_extractor_operation_reports_failure(
        meltano_cli: FlextMeltanoCli,
        command: str,
    ) -> None:
        """Test unsupported extractor operation reports failure."""
        result = meltano_cli.run([command, "--operation", "run", "--args", "demo"])

        tm.that(result.failure, eq=True)

    @staticmethod
    def test_plugin_info_without_plugin_type_reports_failure(
        meltano_cli: FlextMeltanoCli,
    ) -> None:
        """Test plugin info without plugin type reports failure."""
        result = meltano_cli.run([
            c.Meltano.CliCommand.PLUGIN,
            c.Meltano.ExecutorCommand.INFO,
        ])

        tm.that(result.failure, eq=True)

    @staticmethod
    def test_plugin_install_is_unsupported_and_reports_failure(
        meltano_cli: FlextMeltanoCli,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test plugin install is unsupported and reports failure."""
        result = meltano_cli.run([
            c.Meltano.CliCommand.PLUGIN,
            c.Meltano.ExecutorCommand.INSTALL,
            "--plugin-name",
            "tap-demo",
        ])

        tm.that(result.failure, eq=True)
        tm.that(capsys.readouterr().out, has="not supported")

    @staticmethod
    def test_dbt_help_option_succeeds_and_prints_dbt_help(
        meltano_cli: FlextMeltanoCli,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test dbt help option succeeds and prints dbt help."""
        result = meltano_cli.run([c.Meltano.CliCommand.DBT, c.Meltano.CMD_HELP_OPTION])

        tm.that(result.success, eq=True)
        tm.that(capsys.readouterr().out, has="DBT")
