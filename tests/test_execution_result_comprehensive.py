"""Comprehensive test module for FlextMeltanoExecutionResult - 100% coverage.

Tests the FlextMeltanoExecutionResult class following FLEXT standards.
Ensures complete coverage of all methods and edge cases.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from flext_meltano import FlextMeltanoExecutionResult


class TestFlextMeltanoExecutionResultComprehensive:
    """Comprehensive test suite for FlextMeltanoExecutionResult - 100% coverage."""

    def test_initialization_success_case(self) -> None:
        """Test FlextMeltanoExecutionResult initialization with success case."""
        command = ["meltano", "run", "tap-csv", "target-jsonl"]
        result = FlextMeltanoExecutionResult(
            command=command,
            success=True,
            exit_code=0,
            output="Pipeline completed successfully",
            error="",
            execution_time=45.2,
        )

        assert result.command == command
        assert result.success is True
        assert result.exit_code == 0
        assert result.output == "Pipeline completed successfully"
        assert not result.error
        assert result.execution_time == 45.2

    def test_initialization_failure_case(self) -> None:
        """Test FlextMeltanoExecutionResult initialization with failure case."""
        command = ["meltano", "run", "tap-invalid", "target-invalid"]
        result = FlextMeltanoExecutionResult(
            command=command,
            success=False,
            exit_code=1,
            output="",
            error="Plugin not found: tap-invalid",
            execution_time=2.1,
        )

        assert result.command == command
        assert result.success is False
        assert result.exit_code == 1
        assert not result.output
        assert result.error == "Plugin not found: tap-invalid"
        assert result.execution_time == 2.1

    def test_initialization_empty_command(self) -> None:
        """Test FlextMeltanoExecutionResult with empty command."""
        result = FlextMeltanoExecutionResult(
            command=[],
            success=False,
            exit_code=2,
            output="",
            error="No command provided",
            execution_time=0.0,
        )

        assert result.command == []
        assert result.success is False
        assert result.exit_code == 2
        assert result.error == "No command provided"
        assert result.execution_time == 0.0

    def test_to_dict_success_case(self) -> None:
        """Test to_dict method with successful execution."""
        command = ["meltano", "version"]
        result = FlextMeltanoExecutionResult(
            command=command,
            success=True,
            exit_code=0,
            output="Meltano version 3.0.0",
            error="",
            execution_time=1.5,
        )

        with patch(
            "flext_core.FlextUtilities.Generators.generate_iso_timestamp",
        ) as mock_timestamp:
            mock_timestamp.return_value = "2025-01-08T10:30:00Z"

            result_dict = result.to_dict()

        expected_dict = {
            "command": ["meltano", "version"],
            "success": True,
            "exit_code": 0,
            "output": "Meltano version 3.0.0",
            "error": "",
            "execution_time": 1.5,
            "timestamp": "2025-01-08T10:30:00Z",
        }

        assert result_dict == expected_dict
        assert isinstance(result_dict, dict)
        assert "timestamp" in result_dict

    def test_to_dict_failure_case(self) -> None:
        """Test to_dict method with failed execution."""
        command = ["meltano", "invalid-command"]
        result = FlextMeltanoExecutionResult(
            command=command,
            success=False,
            exit_code=127,
            output="",
            error="Command not found",
            execution_time=0.1,
        )

        with patch(
            "flext_core.FlextUtilities.Generators.generate_iso_timestamp",
        ) as mock_timestamp:
            mock_timestamp.return_value = "2025-01-08T10:35:00Z"

            result_dict = result.to_dict()

        expected_dict = {
            "command": ["meltano", "invalid-command"],
            "success": False,
            "exit_code": 127,
            "output": "",
            "error": "Command not found",
            "execution_time": 0.1,
            "timestamp": "2025-01-08T10:35:00Z",
        }

        assert result_dict == expected_dict

    def test_to_json_success_case(self) -> None:
        """Test to_json method with successful execution."""
        command = ["meltano", "discover", "tap-csv"]
        result = FlextMeltanoExecutionResult(
            command=command,
            success=True,
            exit_code=0,
            output='{"streams": []}',
            error="",
            execution_time=3.7,
        )

        with patch(
            "flext_core.FlextUtilities.Generators.generate_iso_timestamp",
        ) as mock_timestamp:
            mock_timestamp.return_value = "2025-01-08T10:40:00Z"

            result_json = result.to_json()

        # Parse JSON to verify it's valid
        parsed_json = json.loads(result_json)

        expected_data = {
            "command": ["meltano", "discover", "tap-csv"],
            "success": True,
            "exit_code": 0,
            "output": '{"streams": []}',
            "error": "",
            "execution_time": 3.7,
            "timestamp": "2025-01-08T10:40:00Z",
        }

        assert parsed_json == expected_data
        assert isinstance(result_json, str)

    def test_to_json_failure_case(self) -> None:
        """Test to_json method with failed execution."""
        command = ["meltano", "install"]
        result = FlextMeltanoExecutionResult(
            command=command,
            success=False,
            exit_code=1,
            output="Installing plugins...",
            error="Connection timeout",
            execution_time=30.0,
        )

        with patch(
            "flext_core.FlextUtilities.Generators.generate_iso_timestamp",
        ) as mock_timestamp:
            mock_timestamp.return_value = "2025-01-08T10:45:00Z"

            result_json = result.to_json()

        # Parse JSON to verify it's valid
        parsed_json = json.loads(result_json)

        expected_data = {
            "command": ["meltano", "install"],
            "success": False,
            "exit_code": 1,
            "output": "Installing plugins...",
            "error": "Connection timeout",
            "execution_time": 30.0,
            "timestamp": "2025-01-08T10:45:00Z",
        }

        assert parsed_json == expected_data

    def test_to_json_empty_strings(self) -> None:
        """Test to_json method with empty output and error strings."""
        result = FlextMeltanoExecutionResult(
            command=["meltano", "config"],
            success=True,
            exit_code=0,
            output="",
            error="",
            execution_time=0.2,
        )

        result_json = result.to_json()
        parsed_json = json.loads(result_json)

        assert not parsed_json["output"]
        assert not parsed_json["error"]
        assert parsed_json["success"] is True

    def test_all_edge_cases(self) -> None:
        """Test edge cases for comprehensive coverage."""
        # Test with very long command
        long_command = ["meltano"] + [f"arg{i}" for i in range(100)]
        result = FlextMeltanoExecutionResult(
            command=long_command,
            success=True,
            exit_code=0,
            output="Long command executed",
            error="",
            execution_time=120.5,
        )

        assert len(result.command) == 101
        assert result.command[0] == "meltano"
        assert result.command[-1] == "arg99"

        # Test JSON serialization with long command
        result_json = result.to_json()
        parsed_json = json.loads(result_json)
        assert len(parsed_json["command"]) == 101

    def test_special_characters_handling(self) -> None:
        """Test handling of special characters in output and error."""
        result = FlextMeltanoExecutionResult(
            command=["meltano", "run"],
            success=False,
            exit_code=1,
            output="Output with special chars: áéíóú çñ 中文 🎉",
            error="Error with quotes: 'single' \"double\" and\nnewlines",
            execution_time=5.0,
        )

        # Test dict conversion
        result_dict = result.to_dict()
        output_str = str(result_dict["output"])
        error_str = str(result_dict["error"])
        assert "áéíóú çñ 中文 🎉" in output_str
        assert "'single' \"double\"" in error_str
        assert "\n" in error_str

        # Test JSON conversion
        result_json = result.to_json()
        parsed_json = json.loads(result_json)
        assert parsed_json["output"] == result.output
        assert parsed_json["error"] == result.error

    def test_numeric_edge_cases(self) -> None:
        """Test numeric edge cases for exit codes and execution time."""
        # Test with maximum realistic values
        result = FlextMeltanoExecutionResult(
            command=["meltano", "stress-test"],
            success=False,
            exit_code=255,  # Maximum exit code
            output="Stress test output",
            error="Memory exhausted",
            execution_time=3600.0,  # 1 hour
        )

        assert result.exit_code == 255
        assert result.execution_time == 3600.0

        # Test with zero execution time
        result_zero = FlextMeltanoExecutionResult(
            command=["meltano", "quick"],
            success=True,
            exit_code=0,
            output="Quick execution",
            error="",
            execution_time=0.0,
        )

        assert result_zero.execution_time == 0.0

    def test_object_consistency(self) -> None:
        """Test object consistency across multiple operations."""
        result = FlextMeltanoExecutionResult(
            command=["meltano", "test"],
            success=True,
            exit_code=0,
            output="Test passed",
            error="",
            execution_time=10.5,
        )

        # Multiple calls should be consistent
        dict1 = result.to_dict()
        dict2 = result.to_dict()

        # Remove timestamps for comparison (they may differ)
        dict1_no_timestamp = {k: v for k, v in dict1.items() if k != "timestamp"}
        dict2_no_timestamp = {k: v for k, v in dict2.items() if k != "timestamp"}

        assert dict1_no_timestamp == dict2_no_timestamp

        # JSON should be parseable consistently
        json1 = result.to_json()
        json2 = result.to_json()

        parsed1 = json.loads(json1)
        parsed2 = json.loads(json2)

        # Remove timestamps for comparison
        parsed1_no_timestamp = {k: v for k, v in parsed1.items() if k != "timestamp"}
        parsed2_no_timestamp = {k: v for k, v in parsed2.items() if k != "timestamp"}

        assert parsed1_no_timestamp == parsed2_no_timestamp


if __name__ == "__main__":
    pytest.main([__file__])
