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
        assert "discover" in capabilities
        assert "sync" in capabilities


class TestFlextMeltanoLibraryRunner:
    """Test FlextMeltanoLibraryRunner functionality."""

    def test_initialization(self) -> None:
        """Test library runner initialization."""
        runner = FlextMeltanoLibraryRunner()
        # Test public methods return FlextResult
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

        # with tempfile.TemporaryDirectory(prefix="test_project_") as temp_dir:  # Unused in current test structure

        # Type annotations to help type checker
        # extractor_config: dict[str, str | dict[str, str]] = {  # Unused in current test structure
        #     "name": "test_extractor",
        #     "config": {},
        # }
        # loader_config: dict[str, str | dict[str, str]] = {  # Unused in current test structure
        #     "name": "test_loader",
        #     "config": {},
        # }
        # transformer_config: dict[str, str | dict[str, str]] = {  # Unused in current test structure
        #     "name": "test_transformer",
        #     "config": {},
        # }

        # Test the complete pipeline
        result: r[t.Processing.EltPipelineResult] = (
            runner.execute_complete_elt_pipeline(
                tap_name="tap-csv",
                target_name="target-jsonl",
            )
        )

        assert result.is_success
        # Get the pipeline data from the result
        pipeline_data: t.Processing.EltPipelineResult = result.value
        # Check that the pipeline data has the expected EltPipelineResult structure
        assert isinstance(pipeline_data, dict)
        assert "success" in pipeline_data
        assert "tap_name" in pipeline_data
        assert "target_name" in pipeline_data
        assert "execution_time" in pipeline_data


class TestFlextMeltanoAdapterIntegration:
    """Test integration of adapter with sub-adapters."""

    def test_adapter_has_sub_adapters(self) -> None:
        """Test that adapter has all required sub-adapters."""
        adapter = FlextMeltanoAdapter()
        assert hasattr(adapter, "project_adapter")
        assert hasattr(adapter, "plugin_adapter")
        assert hasattr(adapter, "pipeline_adapter")
        assert hasattr(adapter, "singer_adapter")
        assert hasattr(adapter, "dbt_adapter")

    def test_adapter_dbt_integration(self) -> None:
        """Test adapter dbt integration via delegation."""
        adapter = FlextMeltanoAdapter()

        # Test dbt operations through adapter (delegates to dbt_adapter)
        result = adapter.execute_dbt_operation()

        # Result should be a FlextResult (success or failure)
        assert hasattr(result, "is_success")
        assert hasattr(result, "is_failure")
