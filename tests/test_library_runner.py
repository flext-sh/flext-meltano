"""Tests for FlextMeltanoLibraryRunner - Advanced library integration patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from flext_core import FlextResult, FlextTypes
from flext_meltano import (
    DbtTransformationResult,
    EltPipelineResult,
    SingerExecutionResult,
)
from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.library_runner import FlextMeltanoLibraryRunner


class TestFlextDbtProgrammaticRunner:
    """Test FlextDbtProgrammaticRunner functionality."""

    def test_get_dbt_runner(self) -> None:
        """Test getting dbt runner instance."""
        library_runner = FlextMeltanoLibraryRunner()
        dbt_runner = library_runner.get_dbt_runner()
        assert dbt_runner is not None
        assert hasattr(dbt_runner, "_parent")

    def test_run_transformations_programmatic_mock(self) -> None:
        """Test dbt transformations with mocked dependencies."""
        library_runner = FlextMeltanoLibraryRunner()
        dbt_runner = library_runner.get_dbt_runner()

        with tempfile.TemporaryDirectory(prefix="test_dbt_project_") as temp_dir:
            project_dir = Path(temp_dir)

            # Mock the DbtRunner and its methods
            with patch(
                "flext_meltano.library_runner.DbtRunner"
            ) as mock_dbt_runner_class:
                mock_runner = Mock()
                mock_result = Mock()
                mock_result.exit_code = 0
                mock_result.exception = None
                mock_runner.invoke.return_value = mock_result
                mock_dbt_runner_class.return_value = mock_runner

                # Test the transformation
                result: FlextResult[DbtTransformationResult] = (
                    dbt_runner.run_transformations_programmatic(
                        project_dir, models=["model1", "model2"]
                    )
                )

                # Type annotation to help type checker
                assert result.is_success
                assert result.unwrap()["success"] is True
                assert result.unwrap()["models_run"] == ["model1", "model2"]
                assert result.unwrap()["execution_method"] == "dbt_runner_programmatic"


class TestFlextSingerProtocolManager:
    """Test FlextSingerProtocolManager functionality."""

    def test_get_singer_manager(self) -> None:
        """Test getting Singer manager instance."""
        library_runner = FlextMeltanoLibraryRunner()
        singer_manager = library_runner.get_singer_manager()
        assert singer_manager is not None
        assert hasattr(singer_manager, "_parent")

    def test_execute_singer_pipeline_mock(self) -> None:
        """Test Singer pipeline execution with mocked dependencies."""
        library_runner = FlextMeltanoLibraryRunner()
        singer_manager = library_runner.get_singer_manager()

        # Mock tap and target instances
        mock_tap = Mock()
        mock_tap.name = "test_tap"
        mock_tap.state = {"bookmark": "2023-01-01"}
        mock_tap.streams = ["stream1"]
        mock_tap.get_records.return_value = [{"id": 1, "name": "test"}]
        mock_tap.get_state.return_value = {"bookmark": "2023-01-02"}

        mock_target = Mock()
        mock_target.name = "test_target"
        mock_target.write_record.return_value = None
        mock_target.write_state.return_value = None

        # Test the pipeline execution
        result: FlextResult[SingerExecutionResult] = (
            singer_manager.execute_singer_pipeline(mock_tap, mock_target)
        )

        # Type annotation to help type checker
        assert result.is_success
        assert result.unwrap()["success"] == "True"
        assert result.unwrap()["execution_method"] == "singer_protocol_compliant"
        assert result.unwrap()["streams_processed"] == 1


class TestFlextMeltanoLibraryRunner:
    """Test FlextMeltanoLibraryRunner functionality."""

    def test_initialization(self) -> None:
        """Test library runner initialization."""
        runner = FlextMeltanoLibraryRunner()
        # Test public methods instead of accessing protected members
        dbt_runner = runner.get_dbt_runner()
        assert dbt_runner is not None

        singer_manager = runner.get_singer_manager()
        assert singer_manager is not None

        abstractions = runner.get_abstractions()
        assert abstractions is not None

    def test_get_dbt_runner(self) -> None:
        """Test getting dbt runner instance."""
        runner = FlextMeltanoLibraryRunner()
        dbt_runner = runner.get_dbt_runner()
        assert dbt_runner is not None
        assert hasattr(dbt_runner, "_parent")

    def test_get_singer_manager(self) -> None:
        """Test getting Singer manager instance."""
        runner = FlextMeltanoLibraryRunner()
        singer_manager = runner.get_singer_manager()
        assert singer_manager is not None
        assert hasattr(singer_manager, "_parent")

    def test_get_abstractions(self) -> None:
        """Test getting abstractions instance."""
        runner = FlextMeltanoLibraryRunner()
        abstractions = runner.get_abstractions()
        assert abstractions is not None

    def test_execute_complete_elt_pipeline_mock(self) -> None:
        """Test complete E-L-T pipeline execution with mocked dependencies."""
        runner = FlextMeltanoLibraryRunner()

        with tempfile.TemporaryDirectory(prefix="test_project_") as temp_dir:
            project_dir = Path(temp_dir)

            # Type annotations to help type checker
            extractor_config: dict[str, str | FlextTypes.StringDict] = {
                "name": "test_extractor",
                "config": {},
            }
            loader_config: dict[str, str | FlextTypes.StringDict] = {
                "name": "test_loader",
                "config": {},
            }
            transformer_config: dict[str, str | FlextTypes.StringDict] = {
                "name": "test_transformer",
                "config": {},
            }

            # Test the complete pipeline
            result: FlextResult[EltPipelineResult] = (
                runner.execute_complete_elt_pipeline(
                    project_dir, extractor_config, loader_config, transformer_config
                )
            )

            assert result.is_success
            # Get the pipeline data from the result
            pipeline_data: EltPipelineResult = result.unwrap()
            # Check that the pipeline data has the expected structure
            assert isinstance(pipeline_data, dict)
            assert "extraction" in pipeline_data
            assert "loading" in pipeline_data
            assert "transformation" in pipeline_data
            assert "overall_success" in pipeline_data


class TestFlextMeltanoAdapterIntegration:
    """Test integration of library runner with FlextMeltanoAdapter."""

    def test_adapter_has_library_runner(self) -> None:
        """Test that adapter has library runner instance."""
        adapter = FlextMeltanoAdapter()
        # Access private attribute for testing p
        library_runner = adapter._library_runner
        assert isinstance(library_runner, FlextMeltanoLibraryRunner)

    def test_adapter_dbt_integration(self) -> None:
        """Test adapter dbt integration."""
        adapter = FlextMeltanoAdapter()

        with tempfile.TemporaryDirectory(prefix="test_project_") as temp_dir:
            Path(temp_dir)

            # Mock the library runner dbt methods
            library_runner = adapter.get_library_runner()
            with patch.object(
                library_runner,
                "get_dbt_runner",
            ) as mock_get_dbt:
                mock_dbt_runner = Mock()
                mock_result = Mock()
                mock_result.is_success = True
                mock_result.unwrap.return_value = {"success": True, "models_run": "all"}
                mock_dbt_runner.run_transformations_programmatic.return_value = (
                    mock_result
                )
                mock_get_dbt.return_value = mock_dbt_runner

                # Test dbt transformations through adapter
                result = adapter.execute_dbt_operation()

                assert result.is_success
