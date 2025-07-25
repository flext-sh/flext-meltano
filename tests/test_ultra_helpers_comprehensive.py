"""Comprehensive tests for FlextMeltano ultra helpers.

Tests for all ultra helper functions and classes with real functionality validation.
"""

from __future__ import annotations

import tempfile
import uuid
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from flext_meltano.core import FlextMeltanoExecutionState
from flext_meltano.flext_meltano_ultra_helpers import (
    FlextMeltanoUltraExecutor,
    flext_meltano_batch_execute_ultra,
    flext_meltano_discover_and_run_ultra,
    flext_meltano_get_pipeline_metrics_ultra,
    flext_meltano_run_pipeline_sync,
    flext_meltano_run_pipeline_ultra,
    flext_meltano_setup_project_ultra,
)


class TestFlextMeltanoUltraExecutor:
    """Test FlextMeltanoUltraExecutor class."""

    @pytest.fixture
    def executor(self) -> FlextMeltanoUltraExecutor:
        """Create executor instance for testing."""
        return FlextMeltanoUltraExecutor()

    @pytest.mark.asyncio
    async def test_executor_initialization(self, executor: FlextMeltanoUltraExecutor) -> None:
        """Test executor initializes with required services."""
        assert hasattr(executor, "repository")
        assert hasattr(executor, "singer_service")
        assert hasattr(executor, "event_bus")

    @pytest.mark.asyncio
    async def test_create_tap_instance(self, executor: FlextMeltanoUltraExecutor) -> None:
        """Test tap instance creation."""
        tap_instance = await executor._create_tap_instance("tap-postgres", ".")

        assert tap_instance.name == "tap-postgres"
        assert hasattr(tap_instance, "sync_all")
        assert hasattr(tap_instance, "catalog_dict")

    @pytest.mark.asyncio
    async def test_create_target_instance(self, executor: FlextMeltanoUltraExecutor) -> None:
        """Test target instance creation."""
        target_instance = await executor._create_target_instance("target-csv", ".")

        assert target_instance.name == "target-csv"

    @pytest.mark.asyncio
    async def test_execute_pipeline_ultra_success(self, executor: FlextMeltanoUltraExecutor) -> None:
        """Test successful ultra pipeline execution."""
        with patch.object(executor, "_create_tap_instance") as mock_tap, \
             patch.object(executor, "_create_target_instance") as mock_target:

            # Setup mocks
            tap_mock = Mock()
            tap_mock.name = "tap-postgres"
            tap_mock.sync_all = Mock()
            mock_tap.return_value = tap_mock

            target_mock = Mock()
            target_mock.name = "target-csv"
            mock_target.return_value = target_mock

            # Mock the orchestration service
            with patch("flext_meltano.flext_meltano_ultra_helpers.FlextMeltanoOrchestrationService") as mock_service:
                mock_service_instance = Mock()
                mock_service.return_value = mock_service_instance

                # Mock successful execution
                from flext_core import FlextResult

                from flext_meltano.core import (
                    FlextMeltanoExecutionState,
                    FlextMeltanoPipelineResult,
                )

                result = FlextMeltanoPipelineResult(
                    pipeline_id=str(uuid.uuid4()),
                    state=FlextMeltanoExecutionState.COMPLETED,
                    records_processed=100,
                    duration_seconds=10.5,
                )
                mock_service_instance.execute_pipeline.return_value = FlextResult.success(result)

                # Execute
                execution_result = await executor.flext_meltano_execute_pipeline_ultra(
                    "tap-postgres", "target-csv",
                )

                # Verify
                assert execution_result.is_success
                assert execution_result.data.state == FlextMeltanoExecutionState.COMPLETED
                assert execution_result.data.records_processed == 100

    @pytest.mark.asyncio
    async def test_execute_pipeline_ultra_with_streams(self, executor: FlextMeltanoUltraExecutor) -> None:
        """Test ultra pipeline execution with selected streams."""
        with patch.object(executor, "_create_tap_instance") as mock_tap, \
             patch.object(executor, "_create_target_instance") as mock_target:

            tap_mock = Mock()
            target_mock = Mock()
            mock_tap.return_value = tap_mock
            mock_target.return_value = target_mock

            with patch("flext_meltano.flext_meltano_ultra_helpers.FlextMeltanoOrchestrationService") as mock_service:
                mock_service_instance = Mock()
                mock_service.return_value = mock_service_instance

                from flext_core import FlextResult

                from flext_meltano.core import (
                    FlextMeltanoExecutionState,
                    FlextMeltanoPipelineResult,
                )

                result = FlextMeltanoPipelineResult(
                    pipeline_id=str(uuid.uuid4()),
                    state=FlextMeltanoExecutionState.COMPLETED,
                )
                mock_service_instance.execute_pipeline.return_value = FlextResult.success(result)

                # Execute with selected streams
                execution_result = await executor.flext_meltano_execute_pipeline_ultra(
                    "tap-postgres", "target-csv",
                    selected_streams=["users", "orders"],
                )

                assert execution_result.is_success

                # Verify configuration was created with selected streams
                call_args = mock_service_instance.execute_pipeline.call_args
                config = call_args[0][0]  # First argument is config
                assert config.selected_streams == ["users", "orders"]

    @pytest.mark.asyncio
    async def test_execute_pipeline_ultra_failure(self, executor: FlextMeltanoUltraExecutor) -> None:
        """Test ultra pipeline execution failure handling."""
        with patch.object(executor, "_create_tap_instance", side_effect=Exception("Tap creation failed")):

            execution_result = await executor.flext_meltano_execute_pipeline_ultra(
                "tap-invalid", "target-csv",
            )

            assert execution_result.is_failure
            assert "Ultra pipeline execution failed" in execution_result.error
            assert "Tap creation failed" in execution_result.error


class TestUltraHelperFunctions:
    """Test ultra helper functions."""

    @pytest.mark.asyncio
    async def test_flext_meltano_run_pipeline_ultra_success(self) -> None:
        """Test ultra pipeline run function with success."""
        with patch("flext_meltano.flext_meltano_ultra_helpers._flext_meltano_ultra_executor") as mock_executor:
            # Mock successful execution
            from flext_core import FlextResult

            from flext_meltano.core import (
                FlextMeltanoExecutionState,
                FlextMeltanoPipelineResult,
            )

            result = FlextMeltanoPipelineResult(
                pipeline_id=str(uuid.uuid4()),
                state=FlextMeltanoExecutionState.COMPLETED,
                records_processed=50,
            )
            mock_executor.flext_meltano_execute_pipeline_ultra.return_value = FlextResult.success(result)

            pipeline_result = await flext_meltano_run_pipeline_ultra("tap-csv", "target-csv")

            assert pipeline_result.state == FlextMeltanoExecutionState.COMPLETED
            assert pipeline_result.records_processed == 50

    @pytest.mark.asyncio
    async def test_flext_meltano_run_pipeline_ultra_failure(self) -> None:
        """Test ultra pipeline run function with failure."""
        with patch("flext_meltano.flext_meltano_ultra_helpers._flext_meltano_ultra_executor") as mock_executor:
            from flext_core import FlextResult

            mock_executor.flext_meltano_execute_pipeline_ultra.return_value = FlextResult.failure("Pipeline failed")

            pipeline_result = await flext_meltano_run_pipeline_ultra("tap-csv", "target-csv")

            from flext_meltano.core import FlextMeltanoExecutionState
            assert pipeline_result.state == FlextMeltanoExecutionState.FAILED
            assert pipeline_result.error_message == "Pipeline failed"

    def test_flext_meltano_run_pipeline_sync(self) -> None:
        """Test synchronous pipeline run function."""
        with patch("flext_meltano.flext_meltano_ultra_helpers.flext_meltano_run_pipeline_ultra") as mock_async:
            from flext_meltano.core import (
                FlextMeltanoExecutionState,
                FlextMeltanoPipelineResult,
            )

            result = FlextMeltanoPipelineResult(
                pipeline_id=str(uuid.uuid4()),
                state=FlextMeltanoExecutionState.COMPLETED,
            )
            mock_async.return_value = result

            with patch("asyncio.run") as mock_run:
                mock_run.return_value = result

                pipeline_result = flext_meltano_run_pipeline_sync("tap-csv", "target-csv")

                assert pipeline_result.state == FlextMeltanoExecutionState.COMPLETED
                mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_flext_meltano_discover_and_run_ultra_success(self) -> None:
        """Test discover and run ultra function with success."""
        with patch("flext_meltano.flext_meltano_ultra_helpers._flext_meltano_ultra_executor") as mock_executor, \
             patch("flext_meltano.flext_meltano_ultra_helpers.flext_meltano_run_pipeline_ultra") as mock_run:

            # Mock tap creation
            tap_mock = Mock()
            tap_mock.name = "tap-postgres"
            mock_executor._create_tap_instance.return_value = tap_mock

            # Mock catalog discovery
            from flext_core import FlextResult
            catalog = {
                "streams": [
                    {"tap_stream_id": "users"},
                    {"tap_stream_id": "orders"},
                ],
            }
            mock_executor.singer_service.discover_catalog.return_value = FlextResult.success(catalog)

            # Mock pipeline execution
            from flext_meltano.core import (
                FlextMeltanoExecutionState,
                FlextMeltanoPipelineResult,
            )
            result = FlextMeltanoPipelineResult(
                pipeline_id=str(uuid.uuid4()),
                state=FlextMeltanoExecutionState.COMPLETED,
            )
            mock_run.return_value = result

            # Execute
            catalog_result, pipeline_result = await flext_meltano_discover_and_run_ultra(
                "tap-postgres", "target-csv",
            )

            assert "streams" in catalog_result
            assert len(catalog_result["streams"]) == 2
            assert pipeline_result.state == FlextMeltanoExecutionState.COMPLETED

            # Verify auto-selected streams were passed
            mock_run.assert_called_once()
            call_kwargs = mock_run.call_args[1]
            assert "selected_streams" in call_kwargs
            assert "users" in call_kwargs["selected_streams"]
            assert "orders" in call_kwargs["selected_streams"]

    @pytest.mark.asyncio
    async def test_flext_meltano_discover_and_run_ultra_discovery_failure(self) -> None:
        """Test discover and run ultra function with discovery failure."""
        with patch("flext_meltano.flext_meltano_ultra_helpers._flext_meltano_ultra_executor") as mock_executor, \
             patch("flext_meltano.flext_meltano_ultra_helpers.flext_meltano_run_pipeline_ultra") as mock_run:

            # Mock tap creation
            tap_mock = Mock()
            mock_executor._create_tap_instance.return_value = tap_mock

            # Mock catalog discovery failure
            from flext_core import FlextResult
            mock_executor.singer_service.discover_catalog.return_value = FlextResult.failure("Discovery failed")

            # Mock pipeline execution
            from flext_meltano.core import (
                FlextMeltanoExecutionState,
                FlextMeltanoPipelineResult,
            )
            result = FlextMeltanoPipelineResult(
                pipeline_id=str(uuid.uuid4()),
                state=FlextMeltanoExecutionState.COMPLETED,
            )
            mock_run.return_value = result

            # Execute
            catalog_result, pipeline_result = await flext_meltano_discover_and_run_ultra(
                "tap-postgres", "target-csv",
            )

            # Should return empty catalog but still run pipeline
            assert catalog_result == {}
            assert pipeline_result.state == FlextMeltanoExecutionState.COMPLETED

    @pytest.mark.asyncio
    async def test_flext_meltano_batch_execute_ultra_parallel(self) -> None:
        """Test batch execution in parallel mode."""
        with patch("flext_meltano.flext_meltano_ultra_helpers.flext_meltano_run_pipeline_ultra") as mock_run:
            from flext_meltano.core import (
                FlextMeltanoExecutionState,
                FlextMeltanoPipelineResult,
            )

            # Mock pipeline execution to return different results
            def mock_pipeline_run(tap, target, **kwargs):
                return FlextMeltanoPipelineResult(
                    pipeline_id=f"{tap}-{target}-{uuid.uuid4()}",
                    state=FlextMeltanoExecutionState.COMPLETED,
                    records_processed=100,
                )

            mock_run.side_effect = mock_pipeline_run

            pipelines = [
                ("tap-postgres", "target-csv"),
                ("tap-csv", "target-postgres"),
                ("tap-api", "target-warehouse"),
            ]

            results = await flext_meltano_batch_execute_ultra(pipelines, parallel=True, max_workers=2)

            assert len(results) == 3
            assert "tap-postgres-to-target-csv" in results
            assert "tap-csv-to-target-postgres" in results
            assert "tap-api-to-target-warehouse" in results

            for result in results.values():
                assert result.state == FlextMeltanoExecutionState.COMPLETED
                assert result.records_processed == 100

    @pytest.mark.asyncio
    async def test_flext_meltano_batch_execute_ultra_sequential(self) -> None:
        """Test batch execution in sequential mode."""
        with patch("flext_meltano.flext_meltano_ultra_helpers.flext_meltano_run_pipeline_ultra") as mock_run:
            from flext_meltano.core import (
                FlextMeltanoExecutionState,
                FlextMeltanoPipelineResult,
            )

            # Track call order
            call_order = []

            def mock_pipeline_run(tap, target, **kwargs):
                call_order.append(f"{tap}-{target}")
                return FlextMeltanoPipelineResult(
                    pipeline_id=f"{tap}-{target}-{uuid.uuid4()}",
                    state=FlextMeltanoExecutionState.COMPLETED,
                )

            mock_run.side_effect = mock_pipeline_run

            pipelines = [
                ("tap-1", "target-1"),
                ("tap-2", "target-2"),
            ]

            results = await flext_meltano_batch_execute_ultra(pipelines, parallel=False)

            assert len(results) == 2
            # Verify sequential execution order
            assert call_order == ["tap-1-target-1", "tap-2-target-2"]

    @pytest.mark.asyncio
    async def test_flext_meltano_setup_project_ultra_success(self) -> None:
        """Test ultra project setup function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir) / "test_project"

            result = await flext_meltano_setup_project_ultra(
                project_path,
                taps=["tap-postgres", "tap-csv"],
                targets=["target-postgres", "target-csv"],
                environments=["dev", "staging", "prod"],
            )

            assert result.is_success
            assert result.data["project_path"] == str(project_path)
            assert result.data["taps_installed"] == ["tap-postgres", "tap-csv"]
            assert result.data["targets_installed"] == ["target-postgres", "target-csv"]
            assert result.data["environments_created"] == ["dev", "staging", "prod"]
            assert result.data["ready"] is True

            # Verify project directory was created
            assert project_path.exists()

    @pytest.mark.asyncio
    async def test_flext_meltano_setup_project_ultra_defaults(self) -> None:
        """Test ultra project setup with default values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir) / "default_project"

            result = await flext_meltano_setup_project_ultra(project_path)

            assert result.is_success
            assert result.data["taps_installed"] == ["tap-csv"]
            assert result.data["targets_installed"] == ["target-csv"]
            assert result.data["environments_created"] == ["dev", "staging", "prod"]

    @pytest.mark.asyncio
    async def test_flext_meltano_get_pipeline_metrics_ultra_empty(self) -> None:
        """Test metrics function with empty repository."""
        with patch("flext_meltano.flext_meltano_ultra_helpers.FlextMeltanoRepository") as mock_repo_class:
            mock_repo = Mock()
            mock_repo_class.return_value = mock_repo

            from flext_core import FlextResult
            mock_repo.get_all.return_value = FlextResult.success([])

            metrics_result = await flext_meltano_get_pipeline_metrics_ultra()

            assert metrics_result.is_success
            metrics = metrics_result.data

            assert metrics["overview"]["total_pipelines"] == 0
            assert metrics["overview"]["successful_pipelines"] == 0
            assert metrics["overview"]["failed_pipelines"] == 0
            assert metrics["overview"]["success_rate_percent"] == 0.0

            assert metrics["performance"]["total_records_processed"] == 0
            assert metrics["performance"]["total_duration_seconds"] == 0.0

    @pytest.mark.asyncio
    async def test_flext_meltano_get_pipeline_metrics_ultra_with_data(self) -> None:
        """Test metrics function with pipeline data."""
        with patch("flext_meltano.flext_meltano_ultra_helpers.FlextMeltanoRepository") as mock_repo_class:
            mock_repo = Mock()
            mock_repo_class.return_value = mock_repo

            from flext_core import FlextResult

            from flext_meltano.core import (
                FlextMeltanoExecutionState,
                FlextMeltanoPipelineResult,
            )

            # Create test pipeline results
            results = [
                FlextMeltanoPipelineResult(
                    pipeline_id="pipeline-1",
                    state=FlextMeltanoExecutionState.COMPLETED,
                    records_processed=100,
                    duration_seconds=10.0,
                ),
                FlextMeltanoPipelineResult(
                    pipeline_id="pipeline-2",
                    state=FlextMeltanoExecutionState.FAILED,
                    records_processed=0,
                    duration_seconds=5.0,
                    error_message="Connection failed",
                ),
                FlextMeltanoPipelineResult(
                    pipeline_id="pipeline-3",
                    state=FlextMeltanoExecutionState.COMPLETED,
                    records_processed=200,
                    duration_seconds=15.0,
                ),
            ]

            mock_repo.get_all.return_value = FlextResult.success(results)

            metrics_result = await flext_meltano_get_pipeline_metrics_ultra()

            assert metrics_result.is_success
            metrics = metrics_result.data

            # Verify overview metrics
            assert metrics["overview"]["total_pipelines"] == 3
            assert metrics["overview"]["successful_pipelines"] == 2
            assert metrics["overview"]["failed_pipelines"] == 1
            assert metrics["overview"]["success_rate_percent"] == 66.67

            # Verify performance metrics
            assert metrics["performance"]["total_records_processed"] == 300
            assert metrics["performance"]["total_duration_seconds"] == 30.0
            assert metrics["performance"]["average_duration_seconds"] == 10.0
            assert metrics["performance"]["records_per_second"] == 10.0

            # Verify recent results
            assert len(metrics["recent_results"]) == 3

            # Check that failed pipeline has error info
            failed_result = next(r for r in metrics["recent_results"] if r["pipeline_id"] == "pipeline-2")
            assert failed_result["error"] == "Connection failed"

    @pytest.mark.asyncio
    async def test_flext_meltano_get_pipeline_metrics_ultra_filtered(self) -> None:
        """Test metrics function with pipeline name filter."""
        with patch("flext_meltano.flext_meltano_ultra_helpers.FlextMeltanoRepository") as mock_repo_class:
            mock_repo = Mock()
            mock_repo_class.return_value = mock_repo

            from flext_core import FlextResult

            from flext_meltano.core import (
                FlextMeltanoExecutionState,
                FlextMeltanoPipelineResult,
            )

            results = [
                FlextMeltanoPipelineResult(
                    pipeline_id="postgres-pipeline-1",
                    state=FlextMeltanoExecutionState.COMPLETED,
                    records_processed=100,
                ),
                FlextMeltanoPipelineResult(
                    pipeline_id="csv-pipeline-1",
                    state=FlextMeltanoExecutionState.COMPLETED,
                    records_processed=50,
                ),
            ]

            mock_repo.get_all.return_value = FlextResult.success(results)

            # Filter by pipeline name
            metrics_result = await flext_meltano_get_pipeline_metrics_ultra("postgres")

            assert metrics_result.is_success
            metrics = metrics_result.data

            # Should only include postgres pipeline
            assert metrics["overview"]["total_pipelines"] == 1
            assert metrics["performance"]["total_records_processed"] == 100


class TestErrorHandling:
    """Test error handling in ultra helpers."""

    @pytest.mark.asyncio
    async def test_batch_execute_with_exception(self) -> None:
        """Test batch execution handles exceptions properly."""
        with patch("flext_meltano.flext_meltano_ultra_helpers.flext_meltano_run_pipeline_ultra") as mock_run:
            # First pipeline succeeds, second raises exception
            def mock_pipeline_run(tap, target, **kwargs):
                if tap == "tap-failing":
                    msg = "Pipeline execution failed"
                    raise Exception(msg)

                from flext_meltano.core import (
                    FlextMeltanoExecutionState,
                    FlextMeltanoPipelineResult,
                )
                return FlextMeltanoPipelineResult(
                    pipeline_id=f"{tap}-{target}",
                    state=FlextMeltanoExecutionState.COMPLETED,
                )

            mock_run.side_effect = mock_pipeline_run

            pipelines = [
                ("tap-success", "target-csv"),
                ("tap-failing", "target-csv"),
            ]

            results = await flext_meltano_batch_execute_ultra(pipelines, parallel=True)

            assert len(results) == 2
            assert results["tap-success-to-target-csv"].state == FlextMeltanoExecutionState.COMPLETED
            assert results["unknown-pipeline"].state == FlextMeltanoExecutionState.FAILED

    @pytest.mark.asyncio
    async def test_metrics_repository_failure(self) -> None:
        """Test metrics function handles repository failures."""
        with patch("flext_meltano.flext_meltano_ultra_helpers.FlextMeltanoRepository") as mock_repo_class:
            mock_repo = Mock()
            mock_repo_class.return_value = mock_repo

            from flext_core import FlextResult
            mock_repo.get_all.return_value = FlextResult.failure("Repository error")

            metrics_result = await flext_meltano_get_pipeline_metrics_ultra()

            assert metrics_result.is_failure
            assert "Failed to retrieve pipeline results" in metrics_result.error


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
