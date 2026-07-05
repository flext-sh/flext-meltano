"""Behavioral tests for FlextMeltanoExecutionResult module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest
from flext_tests import tm

from tests.models import m

if TYPE_CHECKING:
    from tests.typings import t

_ISO_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")


class _ExecutionResultJson(m.BaseModel):
    command: list[str]
    success: bool
    exit_code: int
    output: str
    error: str
    execution_time: float
    timestamp: str


class TestsFlextMeltanoExecutionResult:
    """Behavioral contract of ``m.Meltano.CommandExecutionResult``."""

    @pytest.mark.parametrize(
        ("command", "success", "exit_code", "output", "error", "execution_time"),
        [
            (
                ["meltano", "run", "tap-postgres", "target-csv"],
                True,
                0,
                "Successfully executed",
                "",
                1.5,
            ),
            (
                ["meltano", "run", "invalid-plugin"],
                False,
                1,
                "",
                "Plugin not found",
                0.5,
            ),
            ([], False, -1, "", "No command provided", 0.0),
        ],
    )
    def test_public_fields_reflect_constructor_arguments(
        self,
        command: t.StrSequence,
        *,
        success: bool,
        exit_code: int,
        output: str,
        error: str,
        execution_time: float,
    ) -> None:
        """Public fields expose exactly the values supplied at construction."""
        result = m.Meltano.CommandExecutionResult(
            command=command,
            success=success,
            exit_code=exit_code,
            output=output,
            error=error,
            execution_time=execution_time,
        )
        tm.that(list(result.command), eq=list(command))
        tm.that(result.success, eq=success)
        tm.that(result.exit_code, eq=exit_code)
        tm.that(result.output, eq=output)
        tm.that(result.error, eq=error)
        tm.that(abs(result.execution_time - execution_time), lt=1e-9)

    def test_timestamp_is_populated_iso_string(self) -> None:
        """The computed ``timestamp`` field is a non-empty ISO-8601 string."""
        result = m.Meltano.CommandExecutionResult(
            command=["meltano", "version"],
            success=True,
            exit_code=0,
            output="meltano, version 1.0.0",
            error="",
            execution_time=0.2,
        )
        tm.that(result.timestamp, match=_ISO_TIMESTAMP.pattern)

    @pytest.mark.parametrize(
        ("command", "success", "exit_code", "output", "error", "execution_time"),
        [
            (["meltano", "version"], True, 0, "meltano, version 1.0.0", "", 0.2),
            (
                ["meltano", "run", "invalid"],
                False,
                1,
                "",
                "Plugin 'invalid' not found",
                0.1,
            ),
            (
                ["meltano", "run", "tap-large-database", "target-warehouse"],
                True,
                0,
                "Large dataset processed successfully",
                "",
                3600.5,
            ),
        ],
    )
    def test_to_dict_carries_full_public_contract(
        self,
        command: t.StrSequence,
        *,
        success: bool,
        exit_code: int,
        output: str,
        error: str,
        execution_time: float,
    ) -> None:
        """``to_dict`` mirrors every public field plus an ISO timestamp."""
        result = m.Meltano.CommandExecutionResult(
            command=command,
            success=success,
            exit_code=exit_code,
            output=output,
            error=error,
            execution_time=execution_time,
        )
        result_dict = result.to_dict()
        tm.that(result_dict["command"], eq=command)
        tm.that(result_dict["success"], eq=success)
        tm.that(result_dict["exit_code"], eq=exit_code)
        tm.that(result_dict["output"], eq=output)
        tm.that(result_dict["error"], eq=error)
        tm.that(result_dict["execution_time"], eq=execution_time)
        tm.that(str(result_dict["timestamp"]), match=_ISO_TIMESTAMP.pattern)

    @pytest.mark.parametrize(
        ("command", "success", "exit_code", "output", "error", "execution_time"),
        [
            (
                ["meltano", "invoke", "tap-postgres", "discover"],
                True,
                0,
                '{"streams": []}',
                "",
                2.0,
            ),
            (
                ["meltano", "settings", "invalid-plugin"],
                False,
                2,
                "",
                "Configuration error: invalid settings",
                0.3,
            ),
            (
                ["meltano", "run", "--full-refresh", "tap-postgres", "target-csv"],
                True,
                0,
                "Pipeline completed successfully",
                "",
                5.5,
            ),
        ],
    )
    def test_model_dump_json_round_trips_through_public_schema(
        self,
        command: t.StrSequence,
        *,
        success: bool,
        exit_code: int,
        output: str,
        error: str,
        execution_time: float,
    ) -> None:
        """Serialized JSON validates back into the documented public shape."""
        result = m.Meltano.CommandExecutionResult(
            command=command,
            success=success,
            exit_code=exit_code,
            output=output,
            error=error,
            execution_time=execution_time,
        )
        json_str = result.model_dump_json()
        parsed = _ExecutionResultJson.model_validate_json(json_str)
        tm.that(list(parsed.command), eq=list(command))
        tm.that(parsed.success, eq=success)
        tm.that(parsed.exit_code, eq=exit_code)
        tm.that(parsed.output, eq=output)
        tm.that(parsed.error, eq=error)
        tm.that(abs(parsed.execution_time - execution_time), lt=1e-9)
        tm.that(parsed.timestamp, match=_ISO_TIMESTAMP.pattern)

    def test_special_characters_survive_serialization(self) -> None:
        """Newlines and quotes in output/error are preserved verbatim."""
        error = (
            "Error: Connection failed to host 'localhost:5432'\nCheck your credentials!"
        )
        result = m.Meltano.CommandExecutionResult(
            command=["meltano", "run", "tap-postgres"],
            success=False,
            exit_code=1,
            output="",
            error=error,
            execution_time=1.2,
        )
        result_dict = result.to_dict()
        tm.that(result_dict["error"], eq=error)
        tm.that(result_dict["command"], eq=["meltano", "run", "tap-postgres"])
        tm.that(result_dict["success"], eq=False)

    def test_negative_execution_time_is_rejected(self) -> None:
        """The non-negative execution-time invariant is enforced on construction."""
        with pytest.raises(m.ValidationError):
            m.Meltano.CommandExecutionResult(
                command=["meltano", "run"],
                success=True,
                exit_code=0,
                output="",
                error="",
                execution_time=-1.0,
            )


__all__: list[str] = ["TestsFlextMeltanoExecutionResult"]
