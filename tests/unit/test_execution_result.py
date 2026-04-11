"""Comprehensive tests for FlextMeltanoExecutionResult module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import patch

from flext_tests import tm
from pydantic import BaseModel, TypeAdapter

from tests import m, t


class _ExecutionResultJson(BaseModel):
    command: t.StrSequence
    success: bool
    exit_code: int
    output: str
    error: str
    execution_time: float
    timestamp: str


_JSON_ADAPTER: TypeAdapter[_ExecutionResultJson] = TypeAdapter(_ExecutionResultJson)


class TestFlextMeltanoExecutionResult:
    """Test FlextMeltanoExecutionResult class functionality."""

    TEST_EXECUTION_TIME_SUCCESS: float = 1.5
    TEST_EXECUTION_TIME_FAILURE: float = 0.5
    TEST_EXECUTION_TIME_DICT_SUCCESS: float = 0.2
    TEST_EXECUTION_TIME_DICT_FAILURE: float = 0.1
    TEST_EXECUTION_TIME_JSON_SUCCESS: float = 2.0
    TEST_EXECUTION_TIME_JSON_FAILURE: float = 0.3
    TEST_EXECUTION_TIME_JSON_ERROR: float = 5.5
    TEST_EXECUTION_TIME_HOUR: float = 3600.5
    TEST_COMMAND_COUNT: int = 2

    def test_initialization_with_all_parameters(self) -> None:
        """Test initialization with all parameters."""
        command = ["meltano", "run", "tap-postgres", "target-csv"]
        result = m.Meltano.CommandExecutionResult(
            command=command,
            success=True,
            exit_code=0,
            output="Successfully executed",
            error="",
            execution_time=1.5,
        )
        tm.that(result.command, eq=command)
        tm.that(result.success is True, eq=True)
        tm.that(result.exit_code, eq=0)
        tm.that(result.output, eq="Successfully executed")
        tm.that(result.error, eq="")
        tm.that(result.execution_time, eq=self.TEST_EXECUTION_TIME_SUCCESS)

    def test_initialization_with_failure(self) -> None:
        """Test initialization with failure scenario."""
        command = ["meltano", "run", "invalid-plugin"]
        result = m.Meltano.CommandExecutionResult(
            command=command,
            success=False,
            exit_code=1,
            output="",
            error="Plugin not found",
            execution_time=0.5,
        )
        tm.that(result.command, eq=command)
        tm.that(result.success is False, eq=True)
        tm.that(result.exit_code, eq=1)
        tm.that(result.output, eq="")
        tm.that(result.error, eq="Plugin not found")
        tm.that(result.execution_time, eq=self.TEST_EXECUTION_TIME_FAILURE)

    def test_initialization_with_empty_command(self) -> None:
        """Test initialization with empty command."""
        command: t.StrSequence = []
        result = m.Meltano.CommandExecutionResult(
            command=command,
            success=False,
            exit_code=-1,
            output="",
            error="No command provided",
            execution_time=0.0,
        )
        tm.that(result.command, eq=[])
        tm.that(result.success is False, eq=True)
        tm.that(result.exit_code, eq=-1)
        tm.that(result.output, eq="")
        tm.that(result.error, eq="No command provided")
        tm.that(abs(result.execution_time - 0.0), lt=1e-9)

    def test_to_dict_success(self) -> None:
        """Test to_dict method with successful execution."""
        command = ["meltano", "version"]
        result = m.Meltano.CommandExecutionResult(
            command=command,
            success=True,
            exit_code=0,
            output="meltano, version 1.0.0",
            error="",
            execution_time=0.2,
        )
        with patch("flext_core.u.generate_iso_timestamp") as mock_timestamp:
            mock_timestamp.return_value = "2025-01-01T12:00:00Z"
            result_dict = result.to_dict()
            tm.that(result_dict["command"], eq=command)
            tm.that(result_dict["success"] is True, eq=True)
            tm.that(result_dict["exit_code"], eq=0)
            tm.that(result_dict["output"], eq="meltano, version 1.0.0")
            tm.that(result_dict["error"], eq="")
            tm.that(
                (
                    result_dict["execution_time"]
                    == self.TEST_EXECUTION_TIME_DICT_SUCCESS
                ),
                eq=True,
            )
            tm.that(result_dict["timestamp"], eq="2025-01-01T12:00:00Z")

    def test_to_dict_failure(self) -> None:
        """Test to_dict method with failed execution."""
        command = ["meltano", "run", "invalid"]
        result = m.Meltano.CommandExecutionResult(
            command=command,
            success=False,
            exit_code=1,
            output="",
            error="Plugin 'invalid' not found",
            execution_time=0.1,
        )
        with patch("flext_core.u.generate_iso_timestamp") as mock_timestamp:
            mock_timestamp.return_value = "2025-01-01T12:01:00Z"
            result_dict = result.to_dict()
            tm.that(result_dict["command"], eq=command)
            tm.that(result_dict["success"] is False, eq=True)
            tm.that(result_dict["exit_code"], eq=1)
            tm.that(result_dict["output"], eq="")
            tm.that(result_dict["error"], eq="Plugin 'invalid' not found")
            tm.that(
                (
                    result_dict["execution_time"]
                    == self.TEST_EXECUTION_TIME_DICT_FAILURE
                ),
                eq=True,
            )
            tm.that(result_dict["timestamp"], eq="2025-01-01T12:01:00Z")

    def test_model_dump_json_success(self) -> None:
        """Test model_dump_json with successful execution."""
        command = ["meltano", "invoke", "tap-postgres", "discover"]
        result = m.Meltano.CommandExecutionResult(
            command=command,
            success=True,
            exit_code=0,
            output='{"streams": []}',
            error="",
            execution_time=2.0,
        )
        with patch("flext_core.u.generate_iso_timestamp") as mock_timestamp:
            mock_timestamp.return_value = "2025-01-01T12:02:00Z"
            json_str = result.model_dump_json()
            parsed = _JSON_ADAPTER.validate_json(json_str)
            tm.that(parsed.command, eq=command)
            tm.that(parsed.success is True, eq=True)
            tm.that(parsed.exit_code, eq=0)
            tm.that(parsed.output, eq='{"streams": []}')
            tm.that(parsed.error, eq="")
            tm.that(parsed.execution_time, eq=self.TEST_EXECUTION_TIME_JSON_SUCCESS)
            tm.that(parsed.timestamp, eq="2025-01-01T12:02:00Z")

    def test_model_dump_json_failure(self) -> None:
        """Test model_dump_json with failed execution."""
        command = ["meltano", "settings", "invalid-plugin"]
        result = m.Meltano.CommandExecutionResult(
            command=command,
            success=False,
            exit_code=2,
            output="",
            error="Configuration error: invalid settings",
            execution_time=0.3,
        )
        with patch("flext_core.u.generate_iso_timestamp") as mock_timestamp:
            mock_timestamp.return_value = "2025-01-01T12:03:00Z"
            json_str = result.model_dump_json()
            parsed = _JSON_ADAPTER.validate_json(json_str)
            tm.that(parsed.command, eq=command)
            tm.that(parsed.success is False, eq=True)
            tm.that(parsed.exit_code, eq=2)
            tm.that(parsed.output, eq="")
            tm.that(parsed.error, eq="Configuration error: invalid settings")
            tm.that(parsed.execution_time, eq=self.TEST_EXECUTION_TIME_JSON_FAILURE)
            tm.that(parsed.timestamp, eq="2025-01-01T12:03:00Z")

    def test_model_dump_json_with_complex_command(self) -> None:
        """Test model_dump_json with complex command arguments."""
        command = ["meltano", "run", "--full-refresh", "tap-postgres", "target-csv"]
        result = m.Meltano.CommandExecutionResult(
            command=command,
            success=True,
            exit_code=0,
            output="Pipeline completed successfully",
            error="",
            execution_time=5.5,
        )
        with patch("flext_core.u.generate_iso_timestamp") as mock_timestamp:
            mock_timestamp.return_value = "2025-01-01T12:04:00Z"
            json_str = result.model_dump_json()
            parsed = _JSON_ADAPTER.validate_json(json_str)
            tm.that(parsed.command, eq=command)
            tm.that(parsed.success is True, eq=True)
            tm.that(parsed.exit_code, eq=0)
            tm.that(parsed.output, eq="Pipeline completed successfully")
            tm.that(parsed.error, eq="")
            tm.that(parsed.execution_time, eq=self.TEST_EXECUTION_TIME_JSON_ERROR)
            tm.that(parsed.timestamp, eq="2025-01-01T12:04:00Z")

    def test_execution_result_with_special_characters(self) -> None:
        """Test execution result with special characters in output and error."""
        command = ["meltano", "run", "tap-postgres"]
        result = m.Meltano.CommandExecutionResult(
            command=command,
            success=False,
            exit_code=1,
            output="",
            error="Error: Connection failed to host 'localhost:5432'\nCheck your credentials!",
            execution_time=1.2,
        )
        result_dict = result.to_dict()
        tm.that(
            (
                result_dict["error"]
                == "Error: Connection failed to host 'localhost:5432'\nCheck your credentials!"
            ),
            eq=True,
        )
        tm.that(result_dict["command"], eq=command)
        tm.that(result_dict["success"] is False, eq=True)

    def test_execution_result_with_long_execution_time(self) -> None:
        """Test execution result with long execution time."""
        command = ["meltano", "run", "tap-large-database", "target-warehouse"]
        result = m.Meltano.CommandExecutionResult(
            command=command,
            success=True,
            exit_code=0,
            output="Large dataset processed successfully",
            error="",
            execution_time=3600.5,
        )
        result_dict = result.to_dict()
        tm.that(result_dict["execution_time"], eq=self.TEST_EXECUTION_TIME_HOUR)
        tm.that(result_dict["success"] is True, eq=True)
        tm.that(result_dict["command"], eq=command)
