"""FLEXT Meltano Core - Enterprise Services for Pipeline Orchestration."""

from __future__ import annotations

import subprocess
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, auto
from typing import TYPE_CHECKING

from flext_core import (
    FlextAggregateRoot,
    FlextDomainService,
    FlextEntity,
    FlextResult,
    FlextValueObject,
    get_logger,
)

from flext_meltano.common import injectable

if TYPE_CHECKING:
    from flext_meltano.base import FlextMeltanoDbtService
    from flext_meltano.config import FlextMeltanoConfig
    from flext_meltano.execution import FlextMeltanoExecutor

logger = get_logger(__name__)


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
class FlextMeltanoPipelineResult:
    """Pipeline execution result."""

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
            )
        )

    def complete(self, *, is_success: bool = True, error_message: str | None = None) -> None:
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
            )
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
            )
        )

    def complete(
        self, *, is_success: bool = True, error_message: str | None = None
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
            )
        )


# Domain Services
@injectable
class FlextMeltanoSingerService(FlextDomainService[FlextMeltanoPipelineResult]):
    """Singer protocol domain service."""

    def __init__(self, config: FlextMeltanoConfig) -> None:
        super().__init__()
        self.config = config
        self._logger = get_logger(self.__class__.__name__)

    async def discover_catalog(
        self, tap_name: str,
    ) -> FlextResult[dict[str, object]]:
        """Discover tap catalog."""
        try:
            from flext_meltano.config import FlextMeltanoConfig  # noqa: PLC0415
            from flext_meltano.discovery import FlextMeltanoDiscoverer  # noqa: PLC0415

            discovery = FlextMeltanoDiscoverer(FlextMeltanoConfig())
            catalog_result = await discovery.discover_catalog(tap_name)
            if catalog_result.success and catalog_result.data:
                return FlextResult.ok(catalog_result.data)
            return FlextResult.fail(catalog_result.error or "Discovery failed")
        except Exception as e:
            return FlextResult.fail(f"Catalog discovery failed: {e}")

    def validate_stream_selection(
        self, catalog: dict[str, object], selected_streams: list[str],
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
        except Exception as e:
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
        super().__init__()
        self.config = config
        self.singer_service = singer_service
        self.dbt_service = dbt_service
        self._executor = executor
        self._logger = get_logger(self.__class__.__name__)

    def execute_pipeline(
        self, context: FlextMeltanoPipelineContext,
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
                    context.tap_name, context.target_name,
                )
                if not exec_result.success:
                    tap_job.complete(is_success=False, error_message=exec_result.error)
                    pipeline.complete(is_success=False, error_message=exec_result.error)
                    return FlextResult.fail(exec_result.error or "Pipeline failed")

            tap_job.complete(is_success=True)

            # Complete pipeline
            pipeline.complete(is_success=True)

            result = FlextMeltanoPipelineResult(
                success=True,
                job_id=pipeline_id,
                tap_name=context.tap_name,
                target_name=context.target_name,
                started_at=pipeline.started_at or datetime.now(UTC),
                completed_at=pipeline.completed_at,
            )

            return FlextResult.ok(result)

        except Exception as e:
            pipeline.complete(is_success=False, error_message=str(e))
            return FlextResult.fail(f"Pipeline execution failed: {e}")

    async def execute_dbt_models(
        self, models: list[str],
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
        super().__init__()
        self.config = config
        self._logger = get_logger(self.__class__.__name__)

    def execute_extension(
        self, extension_name: str, args: list[str],
    ) -> FlextResult[dict[str, object]]:
        """Execute custom extension."""
        try:
            result = subprocess.run(  # noqa: S603
                ["meltano", "invoke", extension_name, *args],  # noqa: S607
                check=False, capture_output=True,
                text=True,
                cwd=self.config.project_root,
            )

            if result.returncode == 0:
                return FlextResult.ok(
                    {
                        "extension": extension_name,
                        "output": result.stdout,
                        "success": True,
                    },
                )
            return FlextResult.fail(f"Extension failed: {result.stderr}")
        except Exception as e:
            return FlextResult.fail(f"Extension execution failed: {e}")


__all__ = [
    "FlextMeltanoDomainEvent",
    "FlextMeltanoEnvironmentContext",
    "FlextMeltanoEventType",
    "FlextMeltanoExtension",
    "FlextMeltanoJobEntity",
    "FlextMeltanoOrchestrationService",
    "FlextMeltanoPipelineContext",
    "FlextMeltanoPipelineEntity",
    "FlextMeltanoPipelineResult",
    "FlextMeltanoSingerService",
]
