"""Tests for FLEXT Meltano execution helpers.

Comprehensive tests for job execution functionality.
Zero tolerance for untested code.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

from flext_meltano.helpers.execution import (
    FlextMeltanoResult,
    flext_meltano_execute_job,
)


class TestFlextMeltanoExecuteJob:
    """Test flext_meltano_execute_job function."""

    def test_execute_job_minimal_params(self) -> None:
        """Test job execution with minimal parameters."""
        result = flext_meltano_execute_job("test-tap", "test-target")

        assert result.success
        assert result.data is not None
        data = result.data
        assert data["job_name"] == "test-job"
        assert data["environment"] == "dev"  # default
        assert data["status"] == "success"
        assert data["execution_time"] == "10.5s"
        assert data["records_processed"] == 1000
        assert data["kwargs"] == {}

    def test_execute_job_with_environment(self) -> None:
        """Test job execution with custom environment."""
        result = flext_meltano_execute_job(
            "test-tap",
            "test-target",
            environment="production",
        )

        assert result.success
        assert result.data is not None
        data = result.data
        assert data["job_name"] == "prod-job"
        assert data["environment"] == "production"
        assert data["status"] == "success"

    def test_execute_job_with_kwargs(self) -> None:
        """Test job execution with additional parameters."""
        kwargs = {
            "batch_size": 500,
            "debug": True,
            "custom_config": {"timeout": 300},
        }

        result = flext_meltano_execute_job(
            "test-tap",
            "test-target",
            environment="staging",
        )

        assert result.success
        assert result.data is not None
        data = result.data
        assert data["job_name"] == "complex-job"
        assert data["environment"] == "staging"
        assert data["kwargs"] == kwargs

    def test_execute_job_with_all_params(self) -> None:
        """Test job execution with all possible parameters."""
        result = flext_meltano_execute_job(
            "test-tap",
            "test-target",
            environment="test",
        )

        assert result.success
        assert result.data is not None
        data = result.data
        assert data["job_name"] == "full-job"
        assert data["environment"] == "test"
        assert "retries" in data["kwargs"]
        assert data["kwargs"]["retries"] == 3
        assert data["kwargs"]["timeout"] == 600
        assert data["kwargs"]["parallel"] is True
        assert data["kwargs"]["log_level"] == "DEBUG"

    def test_execute_job_empty_job_name(self) -> None:
        """Test job execution with empty job name."""
        result = flext_meltano_execute_job("", "test-target")

        # Should still succeed with simulation
        assert result.success
        assert result.data is not None
        data = result.data
        assert data["job_name"] == ""

    def test_execute_job_special_characters(self) -> None:
        """Test job execution with special characters in job name."""
        special_job_name = "job-with-special_chars.123"
        result = flext_meltano_execute_job(special_job_name, "test-target")

        assert result.success
        assert result.data is not None
        data = result.data
        assert data["job_name"] == special_job_name

    def test_execute_job_unicode_job_name(self) -> None:
        """Test job execution with unicode characters."""
        unicode_job_name = "job-тест-ジョブ"
        result = flext_meltano_execute_job(unicode_job_name, "test-target")

        assert result.success
        assert result.data is not None
        data = result.data
        assert data["job_name"] == unicode_job_name

    def test_execute_job_long_job_name(self) -> None:
        """Test job execution with very long job name."""
        long_job_name = "a" * 500  # Very long name
        result = flext_meltano_execute_job(long_job_name, "test-target")

        assert result.success
        assert result.data is not None
        data = result.data
        assert data["job_name"] == long_job_name

    def test_execute_job_none_kwargs(self) -> None:
        """Test job execution with None values in kwargs."""
        result = flext_meltano_execute_job(
            "test-tap",
            "test-target",
        )

        assert result.success
        assert result.data is not None
        data = result.data
        assert data["kwargs"]["optional_param"] is None
        assert data["kwargs"]["another_param"] is None

    def test_execute_job_complex_kwargs(self) -> None:
        """Test job execution with complex data structures in kwargs."""
        complex_kwargs = {
            "config": {
                "database": {
                    "host": "localhost",
                    "port": 5432,
                    "credentials": {"username": "user", "password": "pass"},
                },
                "features": ["feature1", "feature2", "feature3"],
            },
            "metadata": {
                "created_by": "test_user",
                "tags": ["ETL", "production", "critical"],
            },
        }

        result = flext_meltano_execute_job(
            "test-tap",
            "test-target",
            environment="dev",
        )

        assert result.success
        assert result.data is not None
        data = result.data
        assert data["kwargs"] == complex_kwargs

    def test_execute_job_result_structure(self) -> None:
        """Test that the result structure is consistent."""
        result = flext_meltano_execute_job("test-tap", "test-target")

        assert isinstance(result, FlextMeltanoResult)
        assert result.success
        assert result.error == ""

        data = result.data
        assert data is not None
        assert isinstance(data, dict)

        # Verify all expected keys are present
        expected_keys = {
            "job_name",
            "environment",
            "status",
            "execution_time",
            "records_processed",
            "kwargs",
        }
        assert set(data.keys()) == expected_keys

        # Verify data types
        assert isinstance(data["job_name"], str)
        assert isinstance(data["environment"], str)
        assert isinstance(data["status"], str)
        assert isinstance(data["execution_time"], str)
        assert isinstance(data["records_processed"], int)
        assert isinstance(data["kwargs"], dict)

    def test_execute_job_simulation_values(self) -> None:
        """Test that simulation returns expected values."""
        result = flext_meltano_execute_job("test-tap", "test-target")

        assert result.success
        assert result.data is not None
        data = result.data

        # Verify simulated values
        assert data["status"] == "success"
        assert data["execution_time"] == "10.5s"
        assert data["records_processed"] == 1000

    @patch("flext_meltano.helpers.execution.FlextResult.ok")
    def test_execute_job_error_handling_in_result_creation(
        self,
        mock_ok: Any,
    ) -> None:
        """Test error handling when FlextResult.ok fails."""
        mock_ok.side_effect = Exception("FlextResult creation failed")

        result = flext_meltano_execute_job("test-tap", "test-target")

        assert not result.success
        assert result.error is not None
        assert "Failed to execute job error-test" in result.error

    def test_execute_job_multiple_calls_independence(self) -> None:
        """Test that multiple calls are independent."""
        result1 = flext_meltano_execute_job("test-tap1", "test-target1")
        result2 = flext_meltano_execute_job("test-tap2", "test-target2")

        assert result1.success
        assert result2.success

        # Verify independence
        data1 = result1.data
        assert data1 is not None
        assert data1["job_name"] == "job1"
        assert data1["kwargs"] == {"param1": "value1"}

        data2 = result2.data
        assert data2 is not None
        assert data2["job_name"] == "job2"
        assert data2["kwargs"] == {"param2": "value2"}

    def test_execute_job_environment_variations(self) -> None:
        """Test different environment variations."""
        environments = [
            "dev",
            "development",
            "test",
            "testing",
            "staging",
            "prod",
            "production",
        ]

        for env in environments:
            result = flext_meltano_execute_job("test-tap", "test-target", environment=env)
            assert result.success
            data = result.data
            assert data is not None
            assert data["environment"] == env
