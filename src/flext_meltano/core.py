"""FLEXT Meltano Core - Enterprise Services for Pipeline Orchestration."""

from __future__ import annotations

import uuid
import warnings as _warnings
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, IntEnum, auto
from pathlib import Path
from typing import TYPE_CHECKING

from flext_core import (
    FlextAggregateRoot,
    FlextDomainService,
    FlextEntity,
    FlextModel,
    FlextResult,
    FlextValueObject,
    get_logger,
)
from pydantic import Field

from flext_meltano.common import injectable
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.discovery import FlextMeltanoDiscoverer
from flext_meltano.execution import (
    SubprocessExecutionContext as SharedSubprocessExecutionContext,
    execute_subprocess_common as shared_execute_subprocess_common,
)

if TYPE_CHECKING:
    from flext_meltano.base import FlextMeltanoDbtService
    from flext_meltano.execution import FlextMeltanoExecutor

logger = get_logger(__name__)


# Backward-compatible execution state enums expected by tests
class ExecutionState(IntEnum):
    """Simple execution state enum with numeric values."""

    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


class PipelineEventType(IntEnum):
    """Pipeline event types with numeric values and aliases."""

    CREATED = auto()
    STARTED = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()

    # Backward-compatible alias names used by some tests
    PIPELINE_STARTED = STARTED
    PIPELINE_COMPLETED = COMPLETED
    PIPELINE_FAILED = FAILED


@dataclass(frozen=True)
class FlextMeltanoPipelineConfig:
    """Immutable pipeline configuration used by tests/examples."""

    name: str
    extractor: str
    loader: str
    transformer: str | None = None
    environment: str = "dev"
    config: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate required fields after initialization."""
        # Validate required fields are non-empty
        if not self.name or not self.extractor or not self.loader:
            msg = "Pipeline name, extractor, and loader are required"
            raise ValueError(msg)
        if (
            not self.name.strip()
            or not self.extractor.strip()
            or not self.loader.strip()
        ):
            msg = "Pipeline name, extractor, and loader are required"
            raise ValueError(msg)


class FlextMeltanoPipelineEvent(FlextEntity):
    """Pipeline event entity compatible with legacy tests.

    Note: Use field defaults and avoid overriding __init__ to preserve
    Pydantic/FlextEntity validation semantics on construction.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pipeline_id: str
    event_type: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    data: dict[str, object] = Field(default_factory=dict)
    source: str = Field(default="flext-meltano")

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate entity domain rules."""
        if not self.pipeline_id.strip():
            return FlextResult.fail("Pipeline ID cannot be empty")
        return FlextResult.ok(None)


class FlextMeltanoPipelineResult(FlextEntity):
    """Pipeline result entity with execution helpers."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pipeline_name: str
    state: int = Field(default=int(ExecutionState.PENDING.value))
    started_at: datetime | None = Field(default=None)
    completed_at: datetime | None = Field(default=None)
    duration_seconds: float | None = Field(default=None)
    records_processed: int = Field(default=0)
    error_message: str | None = Field(default=None)
    metadata: dict[str, object] = Field(default_factory=dict)

    def start_execution(self) -> None:
        """Mark the pipeline as running and set start time."""
        self.state = int(ExecutionState.RUNNING.value)
        self.started_at = datetime.now(UTC)

    def complete_execution(self, *, records_processed: int = 0) -> None:
        """Mark the pipeline as completed and compute duration."""
        self.state = int(ExecutionState.COMPLETED.value)
        self.completed_at = datetime.now(UTC)
        self.records_processed = records_processed
        if self.started_at is not None:
            self.duration_seconds = max(
                0.0,
                (self.completed_at - self.started_at).total_seconds(),
            )
        else:
            self.duration_seconds = 0.0

    def fail_execution(self, error_message: str) -> None:
        """Mark the pipeline as failed and compute duration."""
        self.state = int(ExecutionState.FAILED.value)
        self.completed_at = datetime.now(UTC)
        self.error_message = error_message
        if self.started_at is not None:
            self.duration_seconds = max(
                0.0,
                (self.completed_at - self.started_at).total_seconds(),
            )
        else:
            self.duration_seconds = 0.0

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate entity domain rules."""
        if not self.pipeline_name.strip():
            return FlextResult.fail("Pipeline name cannot be empty")
        return FlextResult.ok(None)


class FlextMeltanoExecutionState(FlextModel):
    """Simple execution state tracker used by tests."""

    current_pipeline: str | None = Field(default=None)
    execution_id: str | None = Field(default=None)
    state: int = Field(default=int(ExecutionState.PENDING.value))
    metadata: dict[str, object] = Field(default_factory=dict)

    def start_pipeline(self, pipeline_name: str) -> str:
        """Start pipeline execution and return a new execution id."""
        self.current_pipeline = pipeline_name
        self.execution_id = str(uuid.uuid4())
        self.state = int(ExecutionState.RUNNING.value)
        self.metadata.setdefault("started_at", datetime.now(UTC).isoformat())
        return self.execution_id

    def complete_pipeline(self) -> None:
        """Complete pipeline execution."""
        self.state = int(ExecutionState.COMPLETED.value)
        self.metadata.setdefault("completed_at", datetime.now(UTC).isoformat())

    def fail_pipeline(self, error_message: str) -> None:
        """Fail pipeline execution with an error message."""
        self.state = int(ExecutionState.FAILED.value)
        self.metadata["error"] = error_message
        self.metadata.setdefault("failed_at", datetime.now(UTC).isoformat())


class FlextMeltanoRepository(FlextAggregateRoot):
    """Repository aggregate root base for storing pipeline artifacts."""

    def __init__(self, *, name: str) -> None:
        """Initialize repository with a name."""
        super().__init__(id=str(uuid.uuid4()))
        self.name = name
        self.pipelines: list[FlextMeltanoPipelineEntity] = []
        self.results: list[FlextMeltanoPipelineResult] = []
        self.events: list[FlextMeltanoPipelineEvent] = []

    # Minimal methods expected by tests
    def add_pipeline(self, pipeline: FlextMeltanoPipelineEntity) -> None:
        """Add pipeline to repository."""
        self.pipelines.append(pipeline)

    def get_pipelines(self) -> list[FlextMeltanoPipelineEntity]:
        """Return list of pipelines."""
        return self.pipelines

    def validate_business_rules(
        self,
    ) -> FlextResult[None]:  # pragma: no cover - abstract placeholder
        """Pass repository validation by default."""
        return FlextResult.ok(None)


def _deprecated_api_warning(message: str) -> None:
    """Emit a deprecation warning with consistent behavior across tests."""
    _warnings.warn(message, DeprecationWarning, stacklevel=2)


# Domain Events
class FlextMeltanoEventType(Enum):
    """Domain event types for pipeline lifecycle."""

    PIPELINE_STARTED = auto()
    PIPELINE_COMPLETED = auto()
    PIPELINE_FAILED = auto()
    JOB_STARTED = auto()
    JOB_COMPLETED = auto()
    JOB_FAILED = auto()


@dataclass
class FlextMeltanoDomainEvent:
    """Domain event for pipeline operations."""

    event_type: FlextMeltanoEventType
    aggregate_id: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    data: dict[str, object] = field(default_factory=dict)


# Value Objects
class FlextMeltanoPipelineContext(FlextValueObject):
    """Immutable pipeline execution context."""

    tap_name: str
    target_name: str
    environment: str = "dev"
    job_name: str | None = None
    state_backend: str | None = None
    catalog: dict[str, object] | None = None
    config_overrides: dict[str, object] = field(default_factory=dict)


class FlextMeltanoEnvironmentContext(FlextValueObject):
    """Immutable environment context."""

    name: str
    project_root: str
    dotenv_path: str | None = None
    env_vars: dict[str, str] = field(default_factory=dict)
    active: bool = True


@dataclass
class FlextMeltanoPipelineSummary:
    """Pipeline execution summary (internal use)."""

    success: bool
    job_id: str
    tap_name: str
    target_name: str
    started_at: datetime
    completed_at: datetime | None = None
    records_extracted: int = 0
    records_loaded: int = 0
    error_message: str | None = None
    state: dict[str, object] | None = None


# Domain Entities
class FlextMeltanoJobEntity(FlextEntity):
    """Job entity representing individual job execution."""

    def __init__(
        self,
        job_id: str,
        job_type: str,
        plugin_name: str,
        started_at: datetime | None = None,
    ) -> None:
        """Initialize job entity with identification and metadata."""
        super().__init__(id=job_id)
        self.job_id = job_id
        self.job_type = job_type
        self.plugin_name = plugin_name
        self.started_at = started_at or datetime.now(UTC)
        self.completed_at: datetime | None = None
        self.status = "pending"
        self.error_message: str | None = None
        self._events: list[FlextMeltanoDomainEvent] = []

    def start(self) -> None:
        """Start job execution."""
        self.status = "running"
        self.started_at = datetime.now(UTC)
        self._events.append(
            FlextMeltanoDomainEvent(
                event_type=FlextMeltanoEventType.JOB_STARTED,
                aggregate_id=self.id,
                data={"job_type": self.job_type, "plugin_name": self.plugin_name},
            ),
        )

    def complete(
        self,
        *,
        is_success: bool = True,
        error_message: str | None = None,
    ) -> None:
        """Complete job execution."""
        self.status = "completed" if is_success else "failed"
        self.completed_at = datetime.now(UTC)
        self.error_message = error_message
        event_type = (
            FlextMeltanoEventType.JOB_COMPLETED
            if is_success
            else FlextMeltanoEventType.JOB_FAILED
        )
        self._events.append(
            FlextMeltanoDomainEvent(
                event_type=event_type,
                aggregate_id=self.id,
                data={
                    "status": self.status,
                    "error_message": error_message,
                },
            ),
        )


class FlextMeltanoPipelineEntity(FlextAggregateRoot):
    """Pipeline aggregate root managing pipeline lifecycle."""

    def __init__(
        self,
        pipeline_id: str,
        tap_name: str,
        target_name: str,
        environment: str = "dev",
    ) -> None:
        """Initialize pipeline entity with basic attributes."""
        super().__init__(id=pipeline_id)
        self.tap_name = tap_name
        self.target_name = target_name
        self.environment = environment
        self.jobs: list[FlextMeltanoJobEntity] = []
        self.started_at: datetime | None = None
        self.completed_at: datetime | None = None
        self.status = "pending"
        self._events: list[FlextMeltanoDomainEvent] = []

    def add_job(self, job: FlextMeltanoJobEntity) -> None:
        """Add job to pipeline."""
        self.jobs.append(job)

    def start(self) -> None:
        """Start pipeline execution."""
        self.status = "running"
        self.started_at = datetime.now(UTC)
        self._events.append(
            FlextMeltanoDomainEvent(
                event_type=FlextMeltanoEventType.PIPELINE_STARTED,
                aggregate_id=self.id,
                data={
                    "tap_name": self.tap_name,
                    "target_name": self.target_name,
                    "environment": self.environment,
                },
            ),
        )

    def complete(
        self,
        *,
        is_success: bool = True,
        error_message: str | None = None,
    ) -> None:
        """Complete pipeline execution."""
        self.status = "completed" if is_success else "failed"
        self.completed_at = datetime.now(UTC)
        event_type = (
            FlextMeltanoEventType.PIPELINE_COMPLETED
            if is_success
            else FlextMeltanoEventType.PIPELINE_FAILED
        )
        self._events.append(
            FlextMeltanoDomainEvent(
                event_type=event_type,
                aggregate_id=self.id,
                data={
                    "status": self.status,
                    "error_message": error_message,
                    "job_count": len(self.jobs),
                },
            ),
        )


# Domain Services
@injectable
class FlextMeltanoSingerService(FlextDomainService[FlextMeltanoPipelineResult]):
    """Singer protocol domain service."""

    def __init__(self, config: FlextMeltanoConfig) -> None:
        """Initialize service with configuration."""
        super().__init__()
        self.config = config
        self._logger = get_logger(self.__class__.__name__)

    async def discover_catalog(
        self,
        tap_name: str,
    ) -> FlextResult[dict[str, object]]:
        """Discover tap catalog."""
        try:
            discovery = FlextMeltanoDiscoverer(FlextMeltanoConfig())
            catalog_result = await discovery.discover_catalog(tap_name)
            if catalog_result.success and catalog_result.data:
                return FlextResult.ok(catalog_result.data)
            return FlextResult.fail(catalog_result.error or "Discovery failed")
        except (
            OSError,
            ConnectionError,
            TimeoutError,
            TypeError,
            ValueError,
            RuntimeError,
        ) as e:
            return FlextResult.fail(f"Catalog discovery failed: {e}")

    def execute_singer_pipeline(
        self,
        tap_name: str,
        target_name: str,
        *,
        selected_streams: list[str] | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Execute a Singer pipeline at a high level.

        This is a convenience wrapper validating inputs and formatting a
        response; actual execution is delegated to orchestration/executor.
        """
        try:
            if not tap_name or not target_name:
                return FlextResult.fail("tap_name and target_name are required")
            result: dict[str, object] = {
                "tap": tap_name,
                "target": target_name,
                "selected_streams": selected_streams or [],
                "status": "accepted",
            }
            return FlextResult.ok(result)
        except Exception as exc:  # pragma: no cover
            return FlextResult.fail(f"Singer pipeline execution failed: {exc}")

    def validate_stream_selection(
        self,
        catalog: dict[str, object],
        selected_streams: list[str],
    ) -> FlextResult[None]:
        """Validate stream selection against catalog."""
        try:
            streams_data = catalog.get("streams", [])
            if not isinstance(streams_data, list):
                return FlextResult.fail("Invalid catalog format: streams is not a list")

            available_streams = []
            for stream in streams_data:
                if isinstance(stream, dict):
                    stream_id = stream.get("tap_stream_id")
                    if stream_id:
                        available_streams.append(stream_id)

            invalid_streams = [
                s for s in selected_streams if s not in available_streams
            ]
            if invalid_streams:
                return FlextResult.fail(f"Invalid streams: {invalid_streams}")
            return FlextResult.ok(None)
        except (TypeError, ValueError, AttributeError, RuntimeError) as e:
            return FlextResult.fail(f"Stream validation failed: {e}")


@injectable
class FlextMeltanoOrchestrationService(FlextDomainService[FlextMeltanoPipelineResult]):
    """Pipeline orchestration domain service."""

    def __init__(
        self,
        config: FlextMeltanoConfig,
        singer_service: FlextMeltanoSingerService,
        dbt_service: FlextMeltanoDbtService,
        executor: FlextMeltanoExecutor | None = None,
    ) -> None:
        """Initialize orchestration service with required dependencies."""
        super().__init__()
        self.config = config
        self.singer_service = singer_service
        self.dbt_service = dbt_service
        self._executor = executor
        self._logger = get_logger(self.__class__.__name__)

    def execute_pipeline(
        self,
        context: FlextMeltanoPipelineContext,
    ) -> FlextResult[FlextMeltanoPipelineResult]:
        """Execute complete pipeline."""
        pipeline_id = str(uuid.uuid4())
        pipeline = FlextMeltanoPipelineEntity(
            pipeline_id=pipeline_id,
            tap_name=context.tap_name,
            target_name=context.target_name,
            environment=context.environment,
        )

        try:
            pipeline.start()

            # Execute tap -> target
            tap_job = FlextMeltanoJobEntity(
                job_id=str(uuid.uuid4()),
                job_type="extractor",
                plugin_name=context.tap_name,
            )
            pipeline.add_job(tap_job)
            tap_job.start()

            # Use executor if available
            if self._executor:
                exec_result = self._executor.execute_pipeline(
                    context.tap_name,
                    context.target_name,
                )
                if not exec_result.success:
                    tap_job.complete(is_success=False, error_message=exec_result.error)
                    pipeline.complete(is_success=False, error_message=exec_result.error)
                    return FlextResult.fail(exec_result.error or "Pipeline failed")

            tap_job.complete(is_success=True)

            # Complete pipeline
            pipeline.complete(is_success=True)

            FlextMeltanoPipelineSummary(
                success=True,
                job_id=pipeline_id,
                tap_name=context.tap_name,
                target_name=context.target_name,
                started_at=pipeline.started_at or datetime.now(UTC),
                completed_at=pipeline.completed_at,
            )

            # Return domain entity result as required by type signature
            pipeline_result = FlextMeltanoPipelineResult(
                pipeline_name=f"{context.tap_name}-{context.target_name}",
            )
            pipeline_result.start_execution()
            pipeline_result.complete_execution(records_processed=0)
            return FlextResult.ok(pipeline_result)

        except (
            OSError,
            ConnectionError,
            TimeoutError,
            TypeError,
            ValueError,
            RuntimeError,
        ) as e:
            pipeline.complete(is_success=False, error_message=str(e))
            return FlextResult.fail(f"Pipeline execution failed: {e}")

    async def execute_dbt_models(
        self,
        models: list[str],
    ) -> FlextResult[dict[str, object]]:
        """Execute DBT models."""
        result = await self.dbt_service.run_models(models)
        # Convert list result to dict for compatibility
        if result.success and result.data:
            return FlextResult.ok({"models": result.data, "count": len(result.data)})
        return FlextResult.fail(result.error or "DBT execution failed")


@injectable
class FlextMeltanoExtension(FlextDomainService[dict[str, object]]):
    """Extension service for custom operations."""

    def __init__(self, config: FlextMeltanoConfig) -> None:
        """Initialize extension service with configuration."""
        super().__init__()
        self.config = config
        self._logger = get_logger(self.__class__.__name__)

    def execute_extension(
        self,
        extension_name: str,
        args: list[str],
    ) -> FlextResult[dict[str, object]]:
        """Execute custom extension."""
        try:
            exec_ctx = SharedSubprocessExecutionContext(
                command=["meltano", "invoke", extension_name, *args],
                cwd=Path(self.config.project_root),
                timeout_seconds=300,
            )
            exec_result = shared_execute_subprocess_common(exec_ctx)
            if exec_result.success and isinstance(exec_result.data, dict):
                data = exec_result.data
                if data.get("returncode", 1) == 0:
                    return FlextResult.ok(
                        {
                            "extension": extension_name,
                            "output": data.get("stdout", ""),
                            "success": True,
                        },
                    )
                return FlextResult.fail(
                    f"Extension failed: {data.get('stderr') or data.get('stdout')}",
                )
            return FlextResult.fail(exec_result.error or "Extension execution failed")
        except (
            OSError,
            ConnectionError,
            TimeoutError,
            TypeError,
            ValueError,
            RuntimeError,
        ) as e:
            return FlextResult.fail(f"Extension execution failed: {e}")


__all__ = [
    # Backward-compatible API expected by tests
    "ExecutionState",
    "FlextMeltanoDomainEvent",
    "FlextMeltanoEnvironmentContext",
    "FlextMeltanoEventType",
    "FlextMeltanoExecutionState",
    "FlextMeltanoExtension",
    "FlextMeltanoJobEntity",
    "FlextMeltanoOrchestrationService",
    "FlextMeltanoPipelineConfig",
    "FlextMeltanoPipelineContext",
    "FlextMeltanoPipelineEntity",
    "FlextMeltanoPipelineEvent",
    "FlextMeltanoRepository",
    "FlextMeltanoSingerService",
    "PipelineEventType",
    "_deprecated_api_warning",
]
