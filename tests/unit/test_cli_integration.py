"""Behavioral tests for CLI-args to Meltano model conversion.

Exercises the public contract of ``u.Cli.cli_args_to_model`` when targeting
``m.Meltano.TapRunParams``:

- successful conversion yields a validated model via the ``r[T]`` success channel
- optional fields default to ``None`` / ``False`` when omitted
- all fields round-trip through the public model surface (``model_dump``)
- validation failures surface as ``r[T]`` failures carrying a descriptive error

Pure in-memory dict -> model conversion; no file, network, or database I/O.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from flext_tests import tm

from tests.models import m
from tests.utilities import u

if TYPE_CHECKING:
    from tests.typings import t


class TestsFlextMeltanoCliIntegration:
    """Behavioral tests for Meltano CLI model conversion."""

    def test_minimal_args_produce_model_with_defaulted_optionals(self) -> None:
        cli_args: t.JsonMapping = {"tap_name": "tap-postgres", "discover": False}

        model = tm.ok(u.Cli.cli_args_to_model(m.Meltano.TapRunParams, cli_args))

        tm.that(model.tap_name, eq="tap-postgres")
        tm.that(model.discover, eq=False)
        tm.that(model.config_file, none=True)
        tm.that(model.catalog_file, none=True)
        tm.that(model.state_file, none=True)
        tm.that(model.properties_file, none=True)

    def test_tap_name_only_defaults_discover_to_false(self) -> None:
        cli_args: t.JsonMapping = {"tap_name": "tap-postgres"}

        model = tm.ok(u.Cli.cli_args_to_model(m.Meltano.TapRunParams, cli_args))

        tm.that(model.discover, eq=False)

    @pytest.mark.parametrize("discover", [True, False])
    def test_discover_flag_is_preserved(self, *, discover: bool) -> None:
        cli_args: t.JsonMapping = {"tap_name": "tap-postgres", "discover": discover}

        model = tm.ok(u.Cli.cli_args_to_model(m.Meltano.TapRunParams, cli_args))

        tm.that(model.discover, eq=discover)

    @pytest.mark.parametrize(
        "field_name",
        ["config_file", "catalog_file", "state_file", "properties_file"],
    )
    def test_each_optional_path_field_round_trips(self, *, field_name: str) -> None:
        cli_args: t.JsonMapping = {
            "tap_name": "tap-postgres",
            field_name: f"/path/to/{field_name}.json",
        }

        model = tm.ok(u.Cli.cli_args_to_model(m.Meltano.TapRunParams, cli_args))

        tm.that(getattr(model, field_name), eq=f"/path/to/{field_name}.json")

    def test_all_fields_round_trip_through_model_dump(self) -> None:
        cli_args: t.JsonMapping = {
            "tap_name": "tap-postgres",
            "config_file": "/settings.json",
            "catalog_file": "/catalog.json",
            "state_file": "/state.json",
            "properties_file": "/properties.json",
            "discover": True,
        }

        model = tm.ok(u.Cli.cli_args_to_model(m.Meltano.TapRunParams, cli_args))
        dumped = model.model_dump()

        for key, expected in cli_args.items():
            tm.that(dumped[key], eq=expected)

    def test_conversion_is_idempotent_over_dumped_state(self) -> None:
        cli_args: t.JsonMapping = {
            "tap_name": "tap-postgres",
            "config_file": "/settings.json",
            "discover": True,
        }

        first = tm.ok(u.Cli.cli_args_to_model(m.Meltano.TapRunParams, cli_args))
        second = tm.ok(
            u.Cli.cli_args_to_model(m.Meltano.TapRunParams, first.model_dump()),
        )

        tm.that(second.model_dump(), eq=first.model_dump())

    def test_missing_required_tap_name_fails_with_validation_error(self) -> None:
        result = u.Cli.cli_args_to_model(m.Meltano.TapRunParams, {"discover": False})

        tm.fail(result, has=["Validation error", "TapRunParams", "tap_name"])

    def test_invalid_discover_type_fails_validation(self) -> None:
        result = u.Cli.cli_args_to_model(
            m.Meltano.TapRunParams,
            {"tap_name": "tap-postgres", "discover": "not-a-boolean"},
        )

        tm.fail(result, has=["Validation error", "TapRunParams"])


__all__: list[str] = ["TestsFlextMeltanoCliIntegration"]
