"""Tests for FlextMeltanoLibraryRunner - Advanced library integration patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.library_runner import (
    FlextDbtProgrammaticRunner,
    FlextMeltanoLibraryRunner,
    FlextSingerProtocolManager,
)


class TestFlextDbtProgrammaticRunner:
    """Test FlextDbtProgrammaticRunner functionality."""

    def test_initialization(self) -> None:
        """Test dbt runner initialization."""
        runner = FlextDbtProgrammaticRunner()
        assert runner._runner is None
        assert runner._manifest_cache == {}

    @pytest.mark.asyncio
    async def test_run_transformations_programmatic_mock(self) -> None:
        """Test dbt transformations with mocked dependencies."""
        runner = FlextDbtProgrammaticRunner()
        with tempfile.TemporaryDirectory(prefix="test_dbt_project_") as temp_dir:
            project_dir = Path(temp_dir)

        # Mock the dbtRunner and its methods
        with patch("flext_meltano.library_runner.dbtRunner") as mock_dbt_runner_class:
            mock_runner = Mock()
            mock_result = Mock()
            mock_result.exit_code = 0
            mock_result.exception = None
            mock_runner.invoke.return_value = mock_result
            mock_dbt_runner_class.return_value = mock_runner

            # Test the transformation
            result = await runner.run_transformations_programmatic(
                project_dir, models=["model1", "model2"]
            )

            assert result.is_success
            assert result.unwrap()["success"] is True
            assert result.unwrap()["models_run"] == ["model1", "model2"]
            assert result.unwrap()["execution_method"] == "dbt_runner_programmatic"


class TestFlextSingerProtocolManager:
    """Test FlextSingerProtocolManager functionality."""

    def test_initialization(self) -> None:
        """Test Singer protocol manager initialization."""
        manager = FlextSingerProtocolManager()
        assert manager._state_cache == {}

    @pytest.mark.asyncio
    async def test_execute_singer_pipeline_mock(self) -> None:
        """Test Singer pipeline execution with mocked dependencies."""
        manager = FlextSingerProtocolManager()

        # Mock tap and target instances
        mock_tap = Mock()
        mock_tap.name = "test_tap"
        mock_tap.state = {"bookmark": "2023-01-01"}

        mock_target = Mock()
        mock_target.name = "test_target"

        # Mock get_selected_streams
        with patch(
            "flext_meltano.library_runner.get_selected_streams"
        ) as mock_get_streams:
            mock_streams = [Mock()]
            mock_get_streams.return_value = mock_streams

            # Mock tap methods
            mock_tap.get_records.return_value = [{"id": 1, "name": "test"}]
            mock_tap.get_state.return_value = {"bookmark": "2023-01-02"}

            # Test the pipeline execution
            result = await manager.execute_singer_pipeline(mock_tap, mock_target)

            assert result.is_success
            assert result.unwrap()["success"] is True
            assert result.unwrap()["execution_method"] == "singer_protocol_compliant"
            assert result.unwrap()["streams_processed"] == 1


class TestFlextMeltanoLibraryRunner:
    """Test FlextMeltanoLibraryRunner functionality."""

    def test_initialization(self) -> None:
        """Test library runner initialization."""
        runner = FlextMeltanoLibraryRunner()
        assert isinstance(runner._dbt_runner, FlextDbtProgrammaticRunner)
        assert isinstance(runner._singer_manager, FlextSingerProtocolManager)
        assert runner._abstractions is not None

    def test_get_dbt_runner(self) -> None:
        """Test getting dbt runner instance."""
        runner = FlextMeltanoLibraryRunner()
        dbt_runner = runner.get_dbt_runner()
        assert isinstance(dbt_runner, FlextDbtProgrammaticRunner)

    def test_get_singer_manager(self) -> None:
        """Test getting Singer manager instance."""
        runner = FlextMeltanoLibraryRunner()
        singer_manager = runner.get_singer_manager()
        assert isinstance(singer_manager, FlextSingerProtocolManager)

    def test_get_abstractions(self) -> None:
        """Test getting abstractions instance."""
        runner = FlextMeltanoLibraryRunner()
        abstractions = runner.get_abstractions()
        assert abstractions is not None

    @pytest.mark.asyncio
    async def test_execute_complete_elt_pipeline_mock(self) -> None:
        """Test complete E-L-T pipeline execution with mocked dependencies."""
        runner = FlextMeltanoLibraryRunner()

        with tempfile.TemporaryDirectory(prefix="test_project_") as temp_dir:
            project_dir = Path(temp_dir)

            extractor_config = {"name": "test_extractor", "config": {}}
            loader_config = {"name": "test_loader", "config": {}}
            transformer_config = {"name": "test_transformer", "config": {}}

            # Mock the dbt runner
            with patch.object(
                runner._dbt_runner, "run_transformations_programmatic"
            ) as mock_dbt:
                mock_dbt.return_value = runner._dbt_runner._logger.info(
                    "Mocked dbt result"
                )

                # Test the complete pipeline
                result = await runner.execute_complete_elt_pipeline(
                    project_dir, extractor_config, loader_config, transformer_config
                )

                assert result.is_success
                pipeline_data = result.unwrap()
                assert "extraction" in pipeline_data
                assert "loading" in pipeline_data
                assert "transformation" in pipeline_data
                assert "overall_success" in pipeline_data


class TestFlextMeltanoAdapterIntegration:
    """Test integration of library runner with FlextMeltanoAdapter."""

    def test_adapter_has_library_runner(self) -> None:
        """Test that adapter has library runner instance."""
        adapter = FlextMeltanoAdapter()
        library_runner = adapter.get_library_runner()
        assert isinstance(library_runner, FlextMeltanoLibraryRunner)

    @pytest.mark.asyncio
    async def test_adapter_dbt_integration(self) -> None:
        """Test adapter dbt integration."""
        adapter = FlextMeltanoAdapter()

        with tempfile.TemporaryDirectory(prefix="test_project_") as temp_dir:
            project_dir = Path(temp_dir)

            # Mock the library runner
            with patch.object(
                adapter._library_runner, "get_dbt_runner"
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
                result = await adapter.run_dbt_transformations(project_dir)

                assert result.is_success
                assert result.unwrap()["success"] is True
