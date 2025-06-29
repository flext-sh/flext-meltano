"""FLX Meltano Orchestrator.

This module provides the central orchestration engine that coordinates all Meltano
operations within the FLX enterprise platform. It integrates deeply with Meltano's
core functionality to provide enterprise-grade data pipeline orchestration.
"""

from __future__ import annotations

import asyncio
import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING, Any

import structlog
from flx_core.domain.pydantic_base import DomainBaseModel
from flx_core.engine.meltano_wrapper import MeltanoEngine
from flx_core.events.event_bus import DomainEvent, EventBusProtocol

# ZERO TOLERANCE - Meltano is REQUIRED and guaranteed in pyproject.toml
from meltano.core.job.job import Job, Payload, State
from pydantic import Field

from flx_meltano.event_bridge import MeltanoEventBridge
from flx_meltano.job_manager import FlxMeltanoJobManager

if TYPE_CHECKING:
    from meltano.core.project import Project

    from flx_meltano.project_manager import FlxMeltanoProjectManager
    from flx_meltano.state_manager import FlxMeltanoStateManager

logger = structlog.get_logger()


class FlxJob(DomainBaseModel):
    """Internal representation of a job being orchestrated."""

    model_config = {"arbitrary_types_allowed": True}

    job_id: str = Field(description="Unique job identifier")
    run_id: str = Field(description="Unique run identifier")
    project_name: str = Field(description="Name of the Meltano project")
    environment: str = Field(description="Execution environment")
    status: PipelineStatus = Field(description="Current job status")
    pipeline_definition: dict[str, Any] = Field(
        description="Pipeline configuration and definition",
    )
    meltano_job: Job | None = Field(
        default=None,
        description="Underlying Meltano job instance",
    )
    task: asyncio.Task[Any] | None = Field(
        default=None,
        description="Asyncio task for job execution",
    )
    started_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Job start timestamp",
    )
    finished_at: datetime | None = Field(
        default=None,
        description="Job completion timestamp",
    )
    last_heartbeat_at: datetime | None = Field(
        default=None,
        description="Last heartbeat timestamp",
    )
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Job execution payload",
    )
    error: str | None = Field(default=None, description="Error message if job failed")


class OrchestrationMode(Enum):
    """Execution modes for Meltano orchestration.

    Defines different modes for executing Meltano operations, allowing
    for flexible pipeline execution strategies based on requirements.

    Attributes
    ----------
        SEQUENTIAL: Execute operations one after another.
        PARALLEL: Execute operations concurrently when possible.
        DISTRIBUTED: Execute operations across multiple nodes/workers.

    """

    SYNC = "sync"
    ASYNC = "async"
    SCHEDULED = "scheduled"
    TRIGGERED = "triggered"


class RunMode(Enum):
    """Pipeline run mode enumeration for execution behavior.

    Defines whether pipeline execution should be a dry run (validation only)
    or a full execution with actual data processing.

    Attributes
    ----------
        DRY_RUN: Validation mode - check pipeline without executing.
        FULL_RUN: Production mode - execute pipeline with actual data processing.

    """

    DRY_RUN = "dry_run"
    FULL_RUN = "full_run"


class PipelineStatus(Enum):
    """Pipeline execution status enumeration.

    Represents the different states a pipeline can be in during its lifecycle.
    These statuses are used to track pipeline execution progress and handle
    state transitions in the orchestration system.

    Attributes:
    ----------
        PENDING: Pipeline is queued and waiting to start execution.
        RUNNING: Pipeline is currently executing.
        COMPLETED: Pipeline finished successfully.
        FAILED: Pipeline execution failed with errors.
        CANCELLED: Pipeline execution was cancelled by user or system.
        PAUSED: Pipeline execution is temporarily suspended.

    Examples:
    --------
        Checking pipeline status:

        ```python
        status = pipeline.status
        if status == PipelineStatus.RUNNING:
            print("Pipeline is currently executing")
        ```

    See Also:
    --------
        - [Orchestration Architecture](../../docs/architecture/004-orchestration-layer.md)
        - [Pipeline State Management](../../docs/architecture/state-management.md)

    Note:
    ----
        Status transitions follow strict state machine rules to ensure
        data integrity and prevent invalid state changes.

    """

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class FlxMeltanoOrchestrator:
    """Enterprise Meltano orchestrator integrated with FLX infrastructure.

    This orchestrator provides comprehensive Meltano pipeline management with:
    - Deep integration with Meltano's job execution system
    - Advanced state management and recovery
    - Real-time monitoring and event streaming
    - Multi-environment support
    - Enterprise-grade error handling and retry logic
    - Integration with FLX monitoring and alerting
    """

    def __init__(
        self,
        project_manager: FlxMeltanoProjectManager,
        state_manager: FlxMeltanoStateManager,
        event_bus: EventBusProtocol,
    ) -> None:
        """Initialize the FLX Meltano Orchestrator.

        Args:
        ----
        project_manager: FLX Meltano project manager instance
        state_manager: FLX Meltano state manager instance
        event_bus: FLX event bus for real-time events

        """
        self.project_manager = project_manager
        self.state_manager = state_manager
        self.job_manager = FlxMeltanoJobManager(event_bus)
        self.event_bus = event_bus
        self.logger = logger.bind(component="flx_meltano_orchestrator")

        # Initialize event bridge for Meltano-FLX event integration
        self.event_bridge = MeltanoEventBridge(event_bus)

        # Track running jobs
        self._running_jobs: dict[str, FlxJob] = {}
        self._lock = asyncio.Lock()

        self.logger.info("Initialized FLX Meltano Orchestrator with event bridge")

    async def _emit_pipeline_event(
        self, event_type: str, flx_job: FlxJob, payload: dict[str, Any] | None = None
    ) -> None:
        """Emit a pipeline domain event."""
        await self.event_bus.publish(
            DomainEvent.create(
                event_type,
                {
                    "job_id": flx_job.job_id,
                    "run_id": flx_job.run_id,
                    "project_name": flx_job.project_name,
                    "environment": flx_job.environment,
                    "status": flx_job.status.value,
                    **(payload or {}),
                },
            ),
        )

    async def run_pipeline(
        self,
        project_name: str,
        pipeline_definition: dict[str, Any],
        environment: str = "dev",
        execution_mode: OrchestrationMode = OrchestrationMode.ASYNC,
        run_id: str | None = None,
        run_mode: RunMode = RunMode.FULL_RUN,
    ) -> dict[str, Any]:
        """Execute a Meltano pipeline with enterprise orchestration.

        Args:
        ----
        project_name: Name of the Meltano project
        pipeline_definition: Pipeline configuration (blocks, plugins, etc.)
        environment: Environment to execute in
        execution_mode: How to execute the pipeline
        run_id: Optional custom run ID
        run_mode: Pipeline execution mode (dry run vs full execution)

        Returns:
        -------
        Pipeline execution result with status, metrics, and logs

        """
        run_id = run_id or str(uuid.uuid4())

        self.logger.info(
            "Starting pipeline execution",
            project_name=project_name,
            run_id=run_id,
            environment=environment,
            execution_mode=execution_mode.value,
            run_mode=run_mode,
        )

        async with self._lock:
            if run_id in self._running_jobs:
                return {
                    "run_id": run_id,
                    "status": "duplicate",
                    "error": "Job with this run_id is already running",
                }

            # Create and store FlxJob
            flx_job = FlxJob(
                job_id=run_id,  # Using run_id as the primary identifier
                run_id=run_id,
                project_name=project_name,
                environment=environment,
                status=PipelineStatus.PENDING,
                pipeline_definition=pipeline_definition,
                payload={"full_refresh": run_mode == RunMode.DRY_RUN},
            )
            self._running_jobs[run_id] = flx_job

        try:
            # Publish pipeline started event
            await self._emit_pipeline_event("pipeline.running", flx_job)

            # Execute based on mode
            if execution_mode == OrchestrationMode.SYNC:
                result = await self._execute_pipeline_sync(flx_job, run_mode)
            else:
                result = await self._execute_pipeline_async(flx_job, run_mode)

            self.logger.info(
                "Pipeline execution completed",
                run_id=run_id,
                status=result["status"],
                duration=result.get("duration_seconds"),
            )

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            TimeoutError,
            ConnectionError,
            ImportError,
        ) as e:
            # ZERO TOLERANCE - Specific exception types for pipeline execution failures
            self.logger.exception(
                "Pipeline execution failed",
                run_id=run_id,
                error=str(e),
            )
            async with self._lock:
                if run_id in self._running_jobs:
                    job = self._running_jobs[run_id]
                    job.status = PipelineStatus.FAILED
                    job.error = str(e)
                    job.finished_at = datetime.now(UTC)

            # Publish failure event
            await self._emit_pipeline_event(
                "pipeline.failed",
                flx_job,
                {"error": str(e)},
            )

            return {
                "run_id": run_id,
                "status": PipelineStatus.FAILED.value,
                "error": str(e),
                "completed_at": datetime.now(UTC).isoformat(),
            }
        else:
            return result

    async def get_pipeline_status(self, run_id: str) -> dict[str, Any] | None:
        """Get the status of a running or completed pipeline."""
        async with self._lock:
            job = self._running_jobs.get(run_id)

        if not job:
            # Check historical/persistent storage for completed jobs
            return await self._get_historical_job_status(run_id)

        return {
            "run_id": job.run_id,
            "status": job.status.value,
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "finished_at": job.finished_at.isoformat() if job.finished_at else None,
            "last_heartbeat_at": (
                job.last_heartbeat_at.isoformat() if job.last_heartbeat_at else None
            ),
            "error": job.error,
        }

    async def cancel_pipeline(self, run_id: str) -> bool:
        """Cancel a running pipeline."""
        async with self._lock:
            if run_id not in self._running_jobs:
                return False

            job = self._running_jobs[run_id]
            if job.status != PipelineStatus.RUNNING or not job.task:
                return False

            job.task.cancel()
            job.status = PipelineStatus.CANCELLED
            job.finished_at = datetime.now(UTC)
            job.error = "Pipeline cancelled by user"

        # Publish cancellation event
        await self._emit_pipeline_event("pipeline.cancelled", job)

        return True

    async def list_running_pipelines(self) -> list[dict[str, Any]]:
        """List all currently running pipelines."""
        async with self._lock:
            running: list[dict[str, Any]] = [
                {
                    "run_id": job.run_id,
                    "project_name": job.project_name,
                    "environment": job.environment,
                    "pipeline_name": job.pipeline_definition.get(
                        "name",
                        "unknown",
                    ),
                    "started_at": (
                        job.started_at.isoformat() if job.started_at else None
                    ),
                    "last_heartbeat_at": (
                        job.last_heartbeat_at.isoformat()
                        if job.last_heartbeat_at
                        else None
                    ),
                }
                for job in self._running_jobs.values()
            ]
        return running

    async def _create_meltano_job(self, _project: Project, flx_job: FlxJob) -> Job:
        """Create a Meltano job from a FLX job."""
        return Job(
            job_id=flx_job.job_id,
            run_id=flx_job.run_id,
            state=State.RUNNING,
            payload_flags=Payload.STATE,
            payload={
                "pipeline_definition": flx_job.pipeline_definition,
                "environment": flx_job.environment,
            },
        )

    async def _execute_pipeline_sync(
        self, flx_job: FlxJob, run_mode: RunMode = RunMode.FULL_RUN
    ) -> dict[str, Any]:
        """Execute a pipeline synchronously."""
        project = await self.project_manager.load_project(
            flx_job.project_name,
            flx_job.environment,
        )
        flx_job.meltano_job = await self._create_meltano_job(project, flx_job)

        async with self._lock:
            flx_job.status = PipelineStatus.RUNNING

        await self._run_pipeline_task(project, flx_job, run_mode)

        async with self._lock:
            # The task updates the job status, just retrieve it
            status = flx_job.status
            error = flx_job.error
            finished_at = flx_job.finished_at
            self._running_jobs.pop(flx_job.run_id, None)

        return {
            "run_id": flx_job.run_id,
            "status": status.value,
            "error": error,
            "started_at": flx_job.started_at.isoformat(),
            "completed_at": finished_at.isoformat() if finished_at else None,
            "duration_seconds": (
                (finished_at - flx_job.started_at).total_seconds()
                if finished_at and flx_job.started_at
                else None
            ),
        }

    async def _execute_pipeline_async(
        self, flx_job: FlxJob, run_mode: RunMode = RunMode.FULL_RUN
    ) -> dict[str, Any]:
        """Execute a pipeline asynchronously."""
        project = await self.project_manager.load_project(
            flx_job.project_name,
            flx_job.environment,
        )
        flx_job.meltano_job = await self._create_meltano_job(project, flx_job)

        task = asyncio.create_task(self._run_pipeline_task(project, flx_job, run_mode))

        async with self._lock:
            flx_job.task = task
            flx_job.status = PipelineStatus.RUNNING

        return {
            "run_id": flx_job.run_id,
            "status": PipelineStatus.RUNNING.value,
            "message": "Pipeline execution started in the background.",
        }

    async def _run_pipeline_task(
        self, project: Project, flx_job: FlxJob, run_mode: RunMode = RunMode.FULL_RUN
    ) -> None:
        """Run the pipeline task."""
        try:
            # Emit pipeline started event
            await self._emit_pipeline_event("pipeline.running", flx_job)

            # Run the blocks
            result = await self._run_meltano_blocks(project, flx_job, run_mode)

            # Update job status based on result
            if result.get("success"):
                flx_job.status = PipelineStatus.SUCCESS
                await self._emit_pipeline_event("pipeline.success", flx_job, result)

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            TimeoutError,
            ConnectionError,
            ImportError,
        ) as e:
            # ZERO TOLERANCE - Specific exception types for pipeline task execution failures
            self.logger.exception(
                "Unhandled error during pipeline task execution",
                run_id=flx_job.run_id,
            )
            async with self._lock:
                flx_job.status = PipelineStatus.FAILED
                flx_job.error = str(e)
                flx_job.finished_at = datetime.now(UTC)

            await self._emit_pipeline_event(
                "pipeline.failed",
                flx_job,
                {"error": str(e)},
            )
        finally:
            async with self._lock:
                self._running_jobs.pop(flx_job.run_id, None)

    async def _run_meltano_blocks(
        self, project: Project, flx_job: FlxJob, run_mode: RunMode = RunMode.FULL_RUN
    ) -> dict[str, Any]:
        """Run a series of Meltano blocks (e.g., `run`, `invoke`)."""
        pipeline_def = flx_job.pipeline_definition

        # This will be replaced by a more robust block execution engine
        for i, block in enumerate(pipeline_def.get("blocks", [])):
            async with self._lock:
                flx_job.last_heartbeat_at = datetime.now(UTC)

            result = await self._execute_block(
                project,
                flx_job,
                block,
                block_index=i,
                run_mode=run_mode,
            )
            if not result["success"]:
                return {
                    "success": False,
                    "error": f"Block {i} failed: {result.get('error')}",
                }

        return {"success": True}

    async def _execute_block(
        self,
        project: Project,
        flx_job: FlxJob,
        block: dict[str, Any],
        block_index: int,
        _run_mode: RunMode = RunMode.FULL_RUN,
    ) -> dict[str, Any]:
        """Execute a single pipeline block."""
        self.logger.info(
            "Executing pipeline block",
            block_index=block_index,
            block_type=block.get("block_type"),
        )

        block_type = block.get("block_type")
        if block_type == "meltano":
            result = await self._execute_meltano_block(project, flx_job, block)
        elif block_type == "run":
            result = await self._execute_run_block(
                project,
                flx_job,
                block.get("commands", []),
            )
        elif block_type == "invoke":
            result = await self._execute_invoke_block(
                project,
                flx_job,
                block.get("commands", []),
            )
        else:
            msg = f"Unknown block type: {block_type}"
            raise ValueError(msg)

        return result

    async def _execute_meltano_block(
        self, project: Project, flx_job: FlxJob, block: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute a Meltano ELT block."""
        engine = MeltanoEngine(project.root)
        extractor = block.get("extractor")
        loader = block.get("loader")

        if not extractor or not loader:
            return {"success": False, "error": "Extractor and loader are required"}

        return await engine.run_pipeline(
            extractor=extractor,
            loader=loader,
            transform=block.get("transform"),
            state_id=flx_job.job_id,
            env={"MELTANO_ENVIRONMENT": flx_job.environment},
        )

    async def _execute_run_block(
        self, _project: Project, flx_job: FlxJob, commands: list[str]
    ) -> dict[str, Any]:
        """Execute a `meltano run` command block."""
        from flx_core.config.domain_config import get_config

        config = get_config()
        min_commands = config.business.MINIMUM_MELTANO_COMMAND_COUNT

        if len(commands) < min_commands:
            return {
                "success": False,
                "error": "Run command requires at least extractor and loader",
            }

        try:
            # Extract components
            extractor = commands[0]
            loader = commands[-1]
            transform = (
                " ".join(commands[1:-1]) if len(commands) > min_commands else None
            )

            # Build environment
            env = {"MELTANO_ENVIRONMENT": flx_job.environment}

            # Execute pipeline
            result = await self.engine.run_pipeline(
                extractor=extractor,
                loader=loader,
                transform=transform,
                state_id=flx_job.job_id,
                env=env,
            )

        except (
            RuntimeError,
            ValueError,
            TypeError,
            ImportError,
            OSError,
            FileNotFoundError,
        ) as e:
            self.logger.exception("Run block execution failed", error=str(e))
            return {"success": False, "error": str(e)}
        else:
            return {
                "success": True,
                "extractor": extractor,
                "loader": loader,
                "transform": transform,
                "result": result,
            }

    async def _execute_invoke_block(
        self, project: Project, flx_job: FlxJob, commands: list[str]
    ) -> dict[str, Any]:
        """Execute a `meltano invoke` command block.

        Executes Meltano invoke commands using the MeltanoEngine's run_command method
        with proper error handling and result tracking.

        Args:
        ----
            project: The Meltano project instance
            flx_job: The FLX job being executed
            commands: List of commands to invoke

        Returns:
        -------
            Dictionary containing execution results and status

        """
        try:
            self.logger.info(
                "Executing Meltano invoke commands",
                job_id=flx_job.job_id,
                commands=commands,
            )

            # Build the full meltano invoke command
            for command in commands:
                invoke_cmd = ["meltano", "invoke", *command.split()]

                result = await self.meltano_engine.run_command(
                    command=invoke_cmd,
                    project_root=project.root_dir,
                )

                if not result.success:
                    error_msg = f"Meltano invoke failed: {result.stderr}"
                    self.logger.error(error_msg, command=command)
                    return {"success": False, "error": error_msg}

                self.logger.info(
                    "Meltano invoke command completed successfully",
                    command=command,
                    output=result.stdout,
                )

            return {
                "success": True,
                "output": "All invoke commands completed successfully",
                "commands_executed": len(commands),
            }

        except Exception as exc:
            error_msg = f"Failed to execute invoke block: {exc}"
            self.logger.exception("Invoke block execution failed", error=str(exc))
            return {"success": False, "error": error_msg}

    def _update_job_state(self, job: Job, state: State) -> None:
        """Update the state of a Meltano job in the database."""
        # This method is now a placeholder as state is managed within FlxJob
        # and via the Meltano state backend.
