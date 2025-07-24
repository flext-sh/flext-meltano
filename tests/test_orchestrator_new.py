"""Test FLEXT Meltano Orchestrator.

Comprehensive tests for orchestrator functionality to achieve required coverage.
"""

from __future__ import annotations

import tempfile
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from flext_meltano.orchestrator import (
    ExecutionStatus,
    FlextJob,
    FlextMeltanoEngine,
    FlextMeltanoOrchestrationMode,
    FlextMeltanoOrchestrator,
    FlextMeltanoRunMode,
)


class TestFlextMeltanoEngine:
    """Test FlextMeltanoEngine class."""

    @pytest.fixture
    def engine(self) -> FlextMeltanoEngine:
        """Create a FlextMeltanoEngine instance."""
        return FlextMeltanoEngine()

    async def test_engine_initialization(self, engine: FlextMeltanoEngine) -> None:
        """Test engine initialization."""
        assert engine is not None
        assert engine.project_root is None

    async def test_engine_with_project_root(self) -> None:
        """Test engine with project root."""
        with tempfile.TemporaryDirectory() as temp_dir:
            engine = FlextMeltanoEngine(temp_dir)
            assert engine.project_root == temp_dir

    async def test_run_pipeline(self, engine: FlextMeltanoEngine) -> None:
        """Test pipeline execution."""
        result = await engine.run_pipeline(
            extractor="tap-csv",
            loader="target-jsonl",
            transform="dbt:run",
            state_id="test-state",
            env={"TEST": "value"},
        )

        assert result["success"] is True
        assert "message" in result

    async def test_run_command(self, engine: FlextMeltanoEngine) -> None:
        """Test command execution."""
        result = await engine.run_command(
            command=["meltano", "run", "tap-csv", "target-jsonl"],
            project_root="/test/project",
        )

        assert result["success"] is True
        assert "stdout" in result
        assert "stderr" in result


class TestFlextJob:
    """Test FlextJob class."""

    @pytest.fixture
    def job_data(self) -> dict[str, Any]:
        """Create job data for testing."""
        return {
            "job_id": str(uuid4()),
            "run_id": str(uuid4()),
            "project_name": "test-project",
            "environment": "dev",
            "status": ExecutionStatus.PENDING,
            "pipeline_definition": {
                "blocks": [
                    {
                        "block_type": "meltano",
                        "extractor": "tap-csv",
                        "loader": "target-jsonl",
                    },
                ],
            },
        }

    def test_job_creation(self, job_data: dict[str, Any]) -> None:
        """Test job creation."""
        job = FlextJob(**job_data)

        assert job.job_id == job_data["job_id"]
        assert job.run_id == job_data["run_id"]
        assert job.project_name == job_data["project_name"]
        assert job.environment == job_data["environment"]
        assert job.status == ExecutionStatus.PENDING
        assert job.meltano_job is None
        assert job.task is None
        assert job.error is None

    def test_job_with_optional_fields(self, job_data: dict[str, Any]) -> None:
        """Test job with optional fields."""
        job_data["error"] = "Test error"
        job_data["finished_at"] = datetime.now(UTC)

        job = FlextJob(**job_data)
        assert job.error == "Test error"
        assert job.finished_at is not None


class TestFlextMeltanoOrchestrator:
    """Test FlextMeltanoOrchestrator class."""

    @pytest.fixture
    def mock_project_manager(self) -> MagicMock:
        """Create mock project manager."""
        manager = MagicMock()
        manager.load_project_config = AsyncMock()
        return manager

    @pytest.fixture
    def mock_state_manager(self) -> MagicMock:
        """Create mock state manager."""
        return MagicMock()

    @pytest.fixture
    def mock_event_bus(self) -> MagicMock:
        """Create mock event bus."""
        bus = MagicMock()
        bus.publish = AsyncMock()
        return bus

    @pytest.fixture
    def orchestrator(
        self,
        mock_project_manager: MagicMock,
        mock_state_manager: MagicMock,
        mock_event_bus: MagicMock,
    ) -> FlextMeltanoOrchestrator:
        """Create orchestrator instance."""
        return FlextMeltanoOrchestrator(
            project_manager=mock_project_manager,
            state_manager=mock_state_manager,
            event_bus=mock_event_bus,
        )

    async def test_orchestrator_initialization(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Test orchestrator initialization."""
        assert orchestrator is not None
        assert orchestrator.project_manager is not None
        assert orchestrator.state_manager is not None
        assert orchestrator.event_bus is not None
        assert orchestrator.job_manager is not None
        assert orchestrator.event_bridge is not None
        assert orchestrator.meltano_engine is not None

    async def test_run_pipeline_sync(
        self,
        orchestrator: FlextMeltanoOrchestrator,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test synchronous pipeline execution."""
        # Mock successful project config load
        from flext_core import FlextResult
        mock_project_manager.load_project_config.return_value = FlextResult.ok(
            {"project_id": "test", "version": 1},
        )

        pipeline_definition = {
            "blocks": [
                {
                    "block_type": "meltano",
                    "extractor": "tap-csv",
                    "loader": "target-jsonl",
                },
            ],
        }

        result = await orchestrator.run_pipeline(
            project_name="test-project",
            pipeline_definition=pipeline_definition,
            execution_mode=FlextMeltanoOrchestrationMode.SYNC,
            run_mode=FlextMeltanoRunMode.FULL_RUN,
        )

        assert "run_id" in result
        assert "status" in result

    async def test_run_pipeline_async(
        self,
        orchestrator: FlextMeltanoOrchestrator,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test asynchronous pipeline execution."""
        # Mock successful project config load
        from flext_core import FlextResult
        mock_project_manager.load_project_config.return_value = FlextResult.ok(
            {"project_id": "test", "version": 1},
        )

        pipeline_definition = {
            "blocks": [
                {
                    "block_type": "meltano",
                    "extractor": "tap-csv",
                    "loader": "target-jsonl",
                },
            ],
        }

        result = await orchestrator.run_pipeline(
            project_name="test-project",
            pipeline_definition=pipeline_definition,
            execution_mode=FlextMeltanoOrchestrationMode.ASYNC,
            run_mode=FlextMeltanoRunMode.FULL_RUN,
        )

        assert result["status"] == ExecutionStatus.RUNNING.value
        assert "run_id" in result

    async def test_get_pipeline_status_not_found(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Test getting status of non-existent pipeline."""
        result = await orchestrator.get_pipeline_status("non-existent")
        assert result is None

    async def test_cancel_pipeline_not_found(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Test canceling non-existent pipeline."""
        result = await orchestrator.cancel_pipeline("non-existent")
        assert result is False

    async def test_list_running_pipelines_empty(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Test listing pipelines when none are running."""
        result = await orchestrator.list_running_pipelines()
        assert result == []

    async def test_run_pipeline_duplicate_run_id(
        self,
        orchestrator: FlextMeltanoOrchestrator,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test running pipeline with duplicate run_id."""
        from flext_core import FlextResult
        mock_project_manager.load_project_config.return_value = FlextResult.ok(
            {"project_id": "test", "version": 1},
        )

        pipeline_definition = {
            "blocks": [
                {
                    "block_type": "meltano",
                    "extractor": "tap-csv",
                    "loader": "target-jsonl",
                },
            ],
        }

        run_id = "duplicate-run-id"

        # First run
        await orchestrator.run_pipeline(
            project_name="test-project",
            pipeline_definition=pipeline_definition,
            run_id=run_id,
            execution_mode=FlextMeltanoOrchestrationMode.ASYNC,
        )

        # Second run with same run_id should fail
        result = await orchestrator.run_pipeline(
            project_name="test-project",
            pipeline_definition=pipeline_definition,
            run_id=run_id,
            execution_mode=FlextMeltanoOrchestrationMode.ASYNC,
        )

        assert result["status"] == "duplicate"
        assert "error" in result

    async def test_run_pipeline_project_load_failure(
        self,
        orchestrator: FlextMeltanoOrchestrator,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test pipeline execution with project load failure."""
        # Mock failed project config load
        from flext_core import FlextResult
        mock_project_manager.load_project_config.return_value = FlextResult.fail(
            "Project not found",
        )

        pipeline_definition = {
            "blocks": [
                {
                    "block_type": "meltano",
                    "extractor": "tap-csv",
                    "loader": "target-jsonl",
                },
            ],
        }

        result = await orchestrator.run_pipeline(
            project_name="nonexistent-project",
            pipeline_definition=pipeline_definition,
            execution_mode=FlextMeltanoOrchestrationMode.SYNC,
        )

        assert result["status"] == ExecutionStatus.FAILED.value
        assert "error" in result

    def test_create_secure_test_project(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Test secure test project creation."""
        project = orchestrator._create_secure_test_project()

        assert project is not None
        assert project.root.startswith("/tmp/flext_test_") or project.root.startswith("/var/folders/")  # noqa: S108

    async def test_get_state_manager(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Test state manager getter."""
        state_manager = orchestrator._get_state_manager()
        assert state_manager is not None
        assert state_manager == orchestrator.state_manager

    async def test_get_historical_job_status_no_method(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Test historical job status when method doesn't exist."""
        result = await orchestrator._get_historical_job_status("test-run-id")
        assert result is None


class TestOrchestrationModes:
    """Test orchestration mode enums."""

    def test_orchestration_modes(self) -> None:
        """Test orchestration mode values."""
        assert FlextMeltanoOrchestrationMode.SYNC.value == "sync"
        assert FlextMeltanoOrchestrationMode.ASYNC.value == "async"
        assert FlextMeltanoOrchestrationMode.SCHEDULED.value == "scheduled"
        assert FlextMeltanoOrchestrationMode.TRIGGERED.value == "triggered"

    def test_run_modes(self) -> None:
        """Test run mode values."""
        assert FlextMeltanoRunMode.DRY_RUN.value == "dry_run"
        assert FlextMeltanoRunMode.FULL_RUN.value == "full_run"

    def test_execution_status(self) -> None:
        """Test execution status values."""
        assert ExecutionStatus.PENDING.value == "pending"
        assert ExecutionStatus.RUNNING.value == "running"
        assert ExecutionStatus.COMPLETED.value == "completed"
        assert ExecutionStatus.FAILED.value == "failed"
        assert ExecutionStatus.CANCELLED.value == "cancelled"
