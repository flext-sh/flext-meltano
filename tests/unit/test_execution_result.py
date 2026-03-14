"""Comprehensive tests for FlextMeltanoExecutionResult module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from pydantic import TypeAdapter

from flext_meltano.execution_result import FlextMeltanoExecutionResult

_JSON_ADAPTER: TypeAdapter[dict[str, object]] = TypeAdapter(dict[str, object])


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
        result = FlextMeltanoExecutionResult(
            command=command,
            success=True,
            exit_code=0,
            output="Successfully executed",
            error="",
            execution_time=1.5,
        )
        assert result.command == command
        assert result.success is True
        assert result.exit_code == 0
        assert result.output == "Successfully executed"
        assert not result.error
        assert result.execution_time == self.TEST_EXECUTION_TIME_SUCCESS

    def test_initialization_with_failure(self) -> None:
        """Test initialization with failure scenario."""
        command = ["meltano", "run", "invalid-plugin"]
        result = FlextMeltanoExecutionResult(
            command=command,
            success=False,
            exit_code=1,
            output="",
            error="Plugin not found",
            execution_time=0.5,
        )
        assert result.command == command
        assert result.success is False
        assert result.exit_code == 1
        assert not result.output
        assert result.error == "Plugin not found"
        assert result.execution_time == self.TEST_EXECUTION_TIME_FAILURE

    def test_initialization_with_empty_command(self) -> None:
        """Test initialization with empty command."""
        command: list[str] = []
        result = FlextMeltanoExecutionResult(
            command=command,
            success=False,
            exit_code=-1,
            output="",
            error="No command provided",
            execution_time=0.0,
        )
        assert result.command == []
        assert result.success is False
        assert result.exit_code == -1
        assert not result.output
        assert result.error == "No command provided"
        assert result.execution_time == pytest.approx(0.0)

    def test_to_dict_success(self) -> None:
        """Test to_dict method with successful execution."""
        command = ["meltano", "version"]
        result = FlextMeltanoExecutionResult(
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
            assert result_dict["command"] == command
            assert result_dict["success"] is True
            assert result_dict["exit_code"] == 0
            assert result_dict["output"] == "meltano, version 1.0.0"
            assert not result_dict["error"]
            assert (
                result_dict["execution_time"] == self.TEST_EXECUTION_TIME_DICT_SUCCESS
            )
            assert result_dict["timestamp"] == "2025-01-01T12:00:00Z"

    def test_to_dict_failure(self) -> None:
        """Test to_dict method with failed execution."""
        command = ["meltano", "run", "invalid"]
        result = FlextMeltanoExecutionResult(
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
            assert result_dict["command"] == command
            assert result_dict["success"] is False
            assert result_dict["exit_code"] == 1
            assert not result_dict["output"]
            assert result_dict["error"] == "Plugin 'invalid' not found"
            assert (
                result_dict["execution_time"] == self.TEST_EXECUTION_TIME_DICT_FAILURE
            )
            assert result_dict["timestamp"] == "2025-01-01T12:01:00Z"

    def test_model_dump_json_success(self) -> None:
        """Test model_dump_json with successful execution."""
        command = ["meltano", "invoke", "tap-postgres", "discover"]
        result = FlextMeltanoExecutionResult(
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
            assert parsed["command"] == command
            assert parsed["success"] is True
            assert parsed["exit_code"] == 0
            assert parsed["output"] == '{"streams": []}'
            assert not parsed["error"]
            assert parsed["execution_time"] == self.TEST_EXECUTION_TIME_JSON_SUCCESS
            assert parsed["timestamp"] == "2025-01-01T12:02:00Z"

    def test_model_dump_json_failure(self) -> None:
        """Test model_dump_json with failed execution."""
        command = ["meltano", "config", "invalid-plugin"]
        result = FlextMeltanoExecutionResult(
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
            assert parsed["command"] == command
            assert parsed["success"] is False
            assert parsed["exit_code"] == 2
            assert not parsed["output"]
            assert parsed["error"] == "Configuration error: invalid settings"
            assert parsed["execution_time"] == self.TEST_EXECUTION_TIME_JSON_FAILURE
            assert parsed["timestamp"] == "2025-01-01T12:03:00Z"

    def test_model_dump_json_with_complex_command(self) -> None:
        """Test model_dump_json with complex command arguments."""
        command = ["meltano", "run", "--full-refresh", "tap-postgres", "target-csv"]
        result = FlextMeltanoExecutionResult(
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
            assert parsed["command"] == command
            assert parsed["success"] is True
            assert parsed["exit_code"] == 0
            assert parsed["output"] == "Pipeline completed successfully"
            assert not parsed["error"]
            assert parsed["execution_time"] == self.TEST_EXECUTION_TIME_JSON_ERROR
            assert parsed["timestamp"] == "2025-01-01T12:04:00Z"

    def test_execution_result_with_special_characters(self) -> None:
        """Test execution result with special characters in output and error."""
        command = ["meltano", "run", "tap-postgres"]
        result = FlextMeltanoExecutionResult(
            command=command,
            success=False,
            exit_code=1,
            output="",
            error="Error: Connection failed to host 'localhost:5432'\nCheck your credentials!",
            execution_time=1.2,
        )
        result_dict = result.to_dict()
        assert (
            result_dict["error"]
            == "Error: Connection failed to host 'localhost:5432'\nCheck your credentials!"
        )
        assert result_dict["command"] == command
        assert result_dict["success"] is False

    def test_execution_result_with_long_execution_time(self) -> None:
        """Test execution result with long execution time."""
        command = ["meltano", "run", "tap-large-database", "target-warehouse"]
        result = FlextMeltanoExecutionResult(
            command=command,
            success=True,
            exit_code=0,
            output="Large dataset processed successfully",
            error="",
            execution_time=3600.5,
        )
        result_dict = result.to_dict()
        assert result_dict["execution_time"] == self.TEST_EXECUTION_TIME_HOUR
        assert result_dict["success"] is True
        assert result_dict["command"] == command
