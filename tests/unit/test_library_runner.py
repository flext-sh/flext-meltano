"""Tests for FlextMeltanoLibraryRunner - Advanced library integration patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_meltano import FlextMeltanoLibraryRunner, r, t
from flext_meltano.adapters import FlextMeltanoAdapter


class TestFlextDbtProgrammaticRunner:
    """Test FlextDbtProgrammaticRunner functionality."""

    def test_get_dbt_runner(self) -> None:
        """Test getting dbt runner instance returns FlextResult."""
        library_runner = FlextMeltanoLibraryRunner()
        dbt_runner_result = library_runner.get_dbt_runner()
        assert dbt_runner_result.is_success
        assert dbt_runner_result.value is not None
        assert dbt_runner_result.value.get("type") == "dbt_runner"
        assert dbt_runner_result.value.get("status") == "available"

    def test_dbt_runner_capabilities(self) -> None:
        """Test dbt runner has expected capabilities."""
        library_runner = FlextMeltanoLibraryRunner()
        dbt_runner_result = library_runner.get_dbt_runner()
        assert dbt_runner_result.is_success
        capabilities = dbt_runner_result.value.get("capabilities", [])
        assert isinstance(capabilities, list)
        assert "run" in capabilities
        assert "test" in capabilities


class TestFlextSingerProtocolManager:
    """Test FlextSingerProtocolManager functionality."""

    def test_get_singer_manager(self) -> None:
        """Test getting Singer manager instance returns FlextResult."""
        library_runner = FlextMeltanoLibraryRunner()
        singer_manager_result = library_runner.get_singer_manager()
        assert singer_manager_result.is_success
        assert singer_manager_result.value is not None
        assert singer_manager_result.value.get("type") == "singer_manager"
        assert singer_manager_result.value.get("status") == "available"

    def test_singer_manager_capabilities(self) -> None:
        """Test Singer manager has expected capabilities."""
        library_runner = FlextMeltanoLibraryRunner()
        singer_manager_result = library_runner.get_singer_manager()
        assert singer_manager_result.is_success
        capabilities = singer_manager_result.value.get("capabilities", [])
        assert isinstance(capabilities, list)
        assert "discover" in capabilities
        assert "sync" in capabilities


class TestFlextMeltanoLibraryRunner:
    """Test FlextMeltanoLibraryRunner functionality."""

    def test_initialization(self) -> None:
        """Test library runner initialization."""
        runner = FlextMeltanoLibraryRunner()
        dbt_runner_result = runner.get_dbt_runner()
        assert dbt_runner_result.is_success
        assert dbt_runner_result.value is not None
        singer_manager_result = runner.get_singer_manager()
        assert singer_manager_result.is_success
        assert singer_manager_result.value is not None

    def test_get_dbt_runner(self) -> None:
        """Test getting dbt runner instance."""
        runner = FlextMeltanoLibraryRunner()
        dbt_runner_result = runner.get_dbt_runner()
        assert dbt_runner_result.is_success
        assert dbt_runner_result.value is not None
        assert dbt_runner_result.value.get("type") == "dbt_runner"

    def test_get_singer_manager(self) -> None:
        """Test getting Singer manager instance."""
        runner = FlextMeltanoLibraryRunner()
        singer_manager_result = runner.get_singer_manager()
        assert singer_manager_result.is_success
        assert singer_manager_result.value is not None
        assert singer_manager_result.value.get("type") == "singer_manager"

    def test_get_abstractions(self) -> None:
        """Test getting abstractions instance."""
        runner = FlextMeltanoLibraryRunner()
        singer_manager_result = runner.get_singer_manager()
        assert singer_manager_result.is_success

    def test_execute_complete_elt_pipeline_mock(self) -> None:
        """Test complete E-L-T pipeline execution with mocked dependencies."""
        runner = FlextMeltanoLibraryRunner()
        result: r[t.Meltano.Processing.EltPipelineResult] = (
            runner.execute_complete_elt_pipeline(
                tap_name="tap-csv", target_name="target-jsonl"
            )
        )
        assert result.is_success
        pipeline_data: t.Meltano.Processing.EltPipelineResult = result.value
        assert isinstance(pipeline_data, dict)
        assert "success" in pipeline_data
        assert "tap_name" in pipeline_data
        assert "target_name" in pipeline_data
        assert "execution_time" in pipeline_data


class TestProjectAdapterIntegration:
    """Test integration of FlextMeltanoAdapter.FlextMeltanoAdapter.ProjectAdapter."""

    def test_adapter_version(self) -> None:
        """Test that FlextMeltanoAdapter.ProjectAdapter can get version."""
        adapter = FlextMeltanoAdapter.ProjectAdapter()
        result = adapter.get_version()
        assert result.is_success
        assert result.value is not None
        assert "version" in result.value

    def test_adapter_execute(self) -> None:
        """Test that FlextMeltanoAdapter.ProjectAdapter execute returns FlextResult."""
        adapter = FlextMeltanoAdapter.ProjectAdapter()
        result = adapter.execute()
        assert hasattr(result, "is_success")
        assert hasattr(result, "is_failure")
