"""Comprehensive tests for CLI to Model integration.

Tests direct CLI model conversion integration with Meltano models:
- Dict to Pydantic model conversion
- Validation error propagation
- Round-trip conversion
- r railway pattern throughout

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests import tm

from tests.models import m
from tests.utilities import u

if TYPE_CHECKING:
    from tests.typings import t


class TestsFlextMeltanoCliIntegration:
    """Behavioral tests for Meltano CLI model conversion."""

    def test_tap_run_params_minimal(self) -> None:
        cli_args: t.JsonMapping = {
            "tap_name": "tap-postgres",
            "discover": False,
        }
        result = u.Cli.cli_args_to_model(m.Meltano.TapRunParams, cli_args)
        tm.ok(result)
        model = result.value
        tm.that(model.tap_name, eq="tap-postgres")
        tm.that(model.config_file, none=True)
        tm.that(model.discover is False, eq=True)

    def test_tap_run_params_with_config(self) -> None:
        cli_args: t.JsonMapping = {
            "tap_name": "tap-postgres",
            "config_file": "/path/to/settings.json",
            "discover": False,
        }
        result = u.Cli.cli_args_to_model(m.Meltano.TapRunParams, cli_args)
        tm.ok(result)
        model = result.value
        tm.that(model.config_file, eq="/path/to/settings.json")

    def test_tap_run_params_discover_mode(self) -> None:
        cli_args: t.JsonMapping = {
            "tap_name": "tap-postgres",
            "discover": True,
        }
        result = u.Cli.cli_args_to_model(m.Meltano.TapRunParams, cli_args)
        tm.ok(result)
        model = result.value
        tm.that(model.discover is True, eq=True)

    def test_tap_run_params_all_fields(self) -> None:
        cli_args: t.JsonMapping = {
            "tap_name": "tap-postgres",
            "config_file": "/settings.json",
            "catalog_file": "/catalog.json",
            "state_file": "/state.json",
            "properties_file": "/properties.json",
            "discover": False,
        }
        result = u.Cli.cli_args_to_model(m.Meltano.TapRunParams, cli_args)
        tm.ok(result)
        model = result.value
        tm.that(model.config_file, eq="/settings.json")
        tm.that(model.catalog_file, eq="/catalog.json")
        tm.that(model.state_file, eq="/state.json")
        tm.that(model.properties_file, eq="/properties.json")

    def test_tap_run_params_missing_required(self) -> None:
        result = u.Cli.cli_args_to_model(m.Meltano.TapRunParams, {"discover": False})
        tm.fail(result)
        tm.that(str(result.error).lower(), has="validation")
        tm.that(str(result.error).lower(), has="tap_name")

    def test_tap_run_params_invalid_type(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.TapRunParams,
            {"tap_name": "tap-postgres", "discover": "not-a-boolean"},
        )
        tm.fail(result)
        tm.that(str(result.error).lower(), has="validation")

    def test_pipeline_run_params_with_tap_args(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.TapRunParams,
            {"tap_name": "tap-postgres", "config_file": "/path/to/settings.json"},
        )
        tm.ok(result)
        tm.that(result.value.tap_name, eq="tap-postgres")
        tm.that(result.value.config_file, eq="/path/to/settings.json")
