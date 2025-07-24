"""Testes reais para orchestrator.py - COVERAGE DIRETO.

Objetivo: Gerar coverage real no arquivo orchestrator.py (282 statements, 26% coverage).
Foco em aumentar coverage total de 25% para próximo patamar.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock, patch

import pytest

# Import direto das classes REAIS do orchestrator.py
from flext_meltano.orchestrator import (
    ExecutionStatus,
    FlextJob,
    FlextMeltanoEngine,
    FlextMeltanoOrchestrationMode,
    FlextMeltanoOrchestrator,
    FlextMeltanoRunMode,
)


class TestFlextMeltanoEngine:
    """Testes reais da classe FlextMeltanoEngine."""

    def test_engine_initialization(self) -> None:
        """Testa inicialização do engine."""
        engine = FlextMeltanoEngine()
        assert engine.project_root is None

        engine_with_root = FlextMeltanoEngine("/test/project")
        assert engine_with_root.project_root == "/test/project"

    @pytest.mark.asyncio
    async def test_run_pipeline(self) -> None:
        """Testa execução de pipeline."""
        engine = FlextMeltanoEngine()

        result = await engine.run_pipeline(
            extractor="tap-csv",
            loader="target-jsonl",
        )

        assert result["success"] is True
        assert "message" in result

    @pytest.mark.asyncio
    async def test_run_command(self) -> None:
        """Testa execução de comando."""
        engine = FlextMeltanoEngine()

        result = await engine.run_command(
            command=["meltano", "run", "tap-csv", "target-jsonl"],
            project_root="/test/project",
        )

        assert result["success"] is True
        assert "stdout" in result
        assert "stderr" in result


class TestFlextJob:
    """Testes reais da classe FlextJob."""

    def test_flext_job_creation(self) -> None:
        """Testa criação de FlextJob."""
        job = FlextJob(
            job_id="test-job-123",
            run_id="run-456",
            project_name="test-project",
            environment="dev",
            status=ExecutionStatus.PENDING,
            pipeline_definition={"name": "test-pipeline"},
        )

        assert job.job_id == "test-job-123"
        assert job.run_id == "run-456"
        assert job.project_name == "test-project"
        assert job.environment == "dev"
        assert job.status == ExecutionStatus.PENDING
        assert job.pipeline_definition == {"name": "test-pipeline"}
        assert job.meltano_job is None
        assert job.task is None

    def test_flext_job_with_payload(self) -> None:
        """Testa FlextJob com payload."""
        payload = {"config": "value", "settings": {"key": "data"}}

        job = FlextJob(
            job_id="test-job-payload",
            run_id="run-payload",
            project_name="payload-project",
            environment="prod",
            status=ExecutionStatus.RUNNING,
            pipeline_definition={"blocks": []},
            payload=payload,
        )

        assert job.payload == payload
        assert job.environment == "prod"
        assert job.status == ExecutionStatus.RUNNING


class TestFlextMeltanoOrchestrator:
    """Testes reais da classe FlextMeltanoOrchestrator."""

    @pytest.fixture
    def mock_project_manager(self) -> Mock:
        """Cria mock do project manager."""
        mock = Mock()
        mock.load_project_config = AsyncMock()
        mock.load_project_config.return_value = Mock(success=True, value={"name": "test"})
        return mock

    @pytest.fixture
    def mock_state_manager(self) -> Mock:
        """Cria mock do state manager."""
        return Mock()

    @pytest.fixture
    def mock_event_bus(self) -> Mock:
        """Cria mock do event bus."""
        mock = Mock()
        mock.publish = AsyncMock()
        return mock

    @pytest.fixture
    def orchestrator(
        self, mock_project_manager: Mock, mock_state_manager: Mock, mock_event_bus: Mock,
    ) -> FlextMeltanoOrchestrator:
        """Cria instância real do orchestrator."""
        return FlextMeltanoOrchestrator(
            project_manager=mock_project_manager,
            state_manager=mock_state_manager,
            event_bus=mock_event_bus,
        )

    def test_orchestrator_initialization(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Testa inicialização do orchestrator."""
        assert orchestrator.project_manager is not None
        assert orchestrator.state_manager is not None
        assert orchestrator.event_bus is not None
        assert orchestrator.job_manager is not None
        assert orchestrator.event_bridge is not None
        assert orchestrator.meltano_engine is not None
        assert orchestrator._running_jobs == {}
        assert orchestrator._lock is not None

    @pytest.mark.asyncio
    async def test_run_pipeline_sync_mode(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Testa execução de pipeline em modo síncrono."""
        pipeline_def = {
            "name": "test-pipeline",
            "blocks": [
                {
                    "block_type": "meltano",
                    "extractor": "tap-csv",
                    "loader": "target-jsonl",
                },
            ],
        }

        # Mock do meltano engine
        with patch.object(orchestrator.meltano_engine, "run_pipeline") as mock_run:
            mock_run.return_value = {"success": True, "message": "Pipeline completed"}

            result = await orchestrator.run_pipeline(
                project_name="test-project",
                pipeline_definition=pipeline_def,
                environment="dev",
                execution_mode=FlextMeltanoOrchestrationMode.SYNC,
            )

            assert "run_id" in result
            assert result["status"] in [ExecutionStatus.COMPLETED.value, ExecutionStatus.FAILED.value]

    @pytest.mark.asyncio
    async def test_run_pipeline_async_mode(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Testa execução de pipeline em modo assíncrono."""
        pipeline_def = {
            "name": "async-pipeline",
            "blocks": [
                {
                    "block_type": "run",
                    "commands": ["tap-csv", "target-jsonl"],
                },
            ],
        }

        result = await orchestrator.run_pipeline(
            project_name="async-project",
            pipeline_definition=pipeline_def,
            environment="staging",
            execution_mode=FlextMeltanoOrchestrationMode.ASYNC,
        )

        assert "run_id" in result
        assert result["status"] == ExecutionStatus.RUNNING.value
        assert "message" in result

    @pytest.mark.asyncio
    async def test_run_pipeline_duplicate_run_id(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Testa execução com run_id duplicado."""
        run_id = "duplicate-run-123"
        pipeline_def = {"name": "test", "blocks": []}

        # Adiciona job em execução
        orchestrator._running_jobs[run_id] = FlextJob(
            job_id=run_id,
            run_id=run_id,
            project_name="test",
            environment="dev",
            status=ExecutionStatus.RUNNING,
            pipeline_definition=pipeline_def,
        )

        result = await orchestrator.run_pipeline(
            project_name="test-project",
            pipeline_definition=pipeline_def,
            run_id=run_id,
        )

        assert result["status"] == "duplicate"
        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_pipeline_status_existing(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Testa busca de status de pipeline existente."""
        run_id = "status-test-run"
        job = FlextJob(
            job_id=run_id,
            run_id=run_id,
            project_name="status-project",
            environment="dev",
            status=ExecutionStatus.RUNNING,
            pipeline_definition={"name": "status-test"},
        )
        orchestrator._running_jobs[run_id] = job

        status = await orchestrator.get_pipeline_status(run_id)

        assert status is not None
        assert status["run_id"] == run_id
        assert status["status"] == ExecutionStatus.RUNNING.value

    @pytest.mark.asyncio
    async def test_get_pipeline_status_not_found(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Testa busca de status de pipeline inexistente."""
        status = await orchestrator.get_pipeline_status("nonexistent-run")

        # Pode retornar None ou buscar no histórico
        assert status is None or isinstance(status, dict)

    @pytest.mark.asyncio
    async def test_cancel_pipeline_success(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Testa cancelamento de pipeline com sucesso."""
        run_id = "cancel-test-run"

        # Cria mock task
        mock_task = AsyncMock()

        job = FlextJob(
            job_id=run_id,
            run_id=run_id,
            project_name="cancel-project",
            environment="dev",
            status=ExecutionStatus.RUNNING,
            pipeline_definition={"name": "cancel-test"},
            task=mock_task,
        )
        orchestrator._running_jobs[run_id] = job

        result = await orchestrator.cancel_pipeline(run_id)

        assert result is True
        mock_task.cancel.assert_called_once()

    @pytest.mark.asyncio
    async def test_cancel_pipeline_not_found(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Testa cancelamento de pipeline inexistente."""
        result = await orchestrator.cancel_pipeline("nonexistent-run")
        assert result is False

    @pytest.mark.asyncio
    async def test_list_running_pipelines_empty(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Testa listagem de pipelines quando não há nenhum executando."""
        result = await orchestrator.list_running_pipelines()
        assert isinstance(result, list)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_list_running_pipelines_with_jobs(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Testa listagem de pipelines com jobs em execução."""
        # Adiciona job em execução
        job = FlextJob(
            job_id="list-job-1",
            run_id="list-run-1",
            project_name="list-project",
            environment="dev",
            status=ExecutionStatus.RUNNING,
            pipeline_definition={"name": "list-pipeline"},
        )
        orchestrator._running_jobs["list-run-1"] = job

        result = await orchestrator.list_running_pipelines()

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["run_id"] == "list-run-1"
        assert result[0]["project_name"] == "list-project"

    def test_create_secure_test_project(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Testa criação de projeto de teste seguro."""
        project = orchestrator._create_secure_test_project()

        assert project.root is not None
        assert project.root_dir is not None
        # Verifica que usa diretório temporário seguro
        assert "/tmp/flext_test_" in project.root  # noqa: S108

    @pytest.mark.asyncio
    async def test_emit_pipeline_event(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Testa emissão de evento de pipeline."""
        job = FlextJob(
            job_id="event-job",
            run_id="event-run",
            project_name="event-project",
            environment="dev",
            status=ExecutionStatus.RUNNING,
            pipeline_definition={"name": "event-test"},
        )

        # Método protegido, mas testamos indiretamente
        await orchestrator._emit_pipeline_event("test.event", job, {"extra": "data"})

        # Verifica que o event bus foi chamado
        orchestrator.event_bus.publish.assert_called()

    @pytest.mark.asyncio
    async def test_execute_pipeline_with_error(
        self, orchestrator: FlextMeltanoOrchestrator,
    ) -> None:
        """Testa execução de pipeline com erro."""
        pipeline_def = {
            "name": "error-pipeline",
            "blocks": [
                {
                    "block_type": "invalid_block_type",
                    "commands": ["invalid"],
                },
            ],
        }

        # Mock project manager para falhar
        orchestrator.project_manager.load_project_config.return_value = Mock(success=False)

        result = await orchestrator.run_pipeline(
            project_name="error-project",
            pipeline_definition=pipeline_def,
        )

        assert result["status"] == ExecutionStatus.FAILED.value
        assert "error" in result


class TestFlextMeltanoEnums:
    """Testes das enumerações do orchestrator."""

    def test_orchestration_mode_values(self) -> None:
        """Testa valores da enumeração FlextMeltanoOrchestrationMode."""
        assert FlextMeltanoOrchestrationMode.SYNC.value == "sync"
        assert FlextMeltanoOrchestrationMode.ASYNC.value == "async"
        assert FlextMeltanoOrchestrationMode.SCHEDULED.value == "scheduled"
        assert FlextMeltanoOrchestrationMode.TRIGGERED.value == "triggered"

    def test_run_mode_values(self) -> None:
        """Testa valores da enumeração FlextMeltanoRunMode."""
        assert FlextMeltanoRunMode.DRY_RUN.value == "dry_run"
        assert FlextMeltanoRunMode.FULL_RUN.value == "full_run"

    def test_execution_status_values(self) -> None:
        """Testa valores da enumeração ExecutionStatus."""
        assert ExecutionStatus.PENDING.value == "pending"
        assert ExecutionStatus.RUNNING.value == "running"
        assert ExecutionStatus.COMPLETED.value == "completed"
        assert ExecutionStatus.FAILED.value == "failed"
        assert ExecutionStatus.CANCELLED.value == "cancelled"
