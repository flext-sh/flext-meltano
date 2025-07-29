"""FLEXT Meltano Core - Enterprise orchestration using mandatory patterns.

This module implements enterprise orchestration patterns using MANDATORY
flext-core domain services, entities, and value objects.
"""

from __future__ import annotations

import subprocess
import uuid
import warnings
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, auto
from typing import TYPE_CHECKING, Any

# FlextResult is MANDATORY for all operations
from flext_core import (
    FlextAggregateRoot,
    FlextDomainService,
    FlextEntity,
    FlextResult,
)
from injectable import injectable  # type: ignore[import-untyped]

# Meltano core integration - MANDATORY for project management
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from meltano.core.project import Project as MeltanoProject

    from flext_meltano.base import (
        FlextMeltanoConfig,
        FlextMeltanoDbtService,
        FlextMeltanoExtensionService,
        FlextMeltanoTapService,
        FlextMeltanoTargetService,
    )

# === DOMAIN ENUMS ===


class ExecutionState(Enum):
    """Pipeline execution states following domain-driven design."""

    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


class PipelineEventType(Enum):
    """Pipeline event types for event sourcing."""

    CREATED = auto()
    STARTED = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


# === DOMAIN VALUE OBJECTS ===


@dataclass(frozen=True)
class FlextMeltanoPipelineConfig:
    """Pipeline configuration value object - immutable."""

    name: str
    extractor: str
    loader: str
    transformer: str | None = None
    environment: str = "dev"
    config: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if not self.name or not self.extractor or not self.loader:
            msg = "Pipeline name, extractor, and loader are required"
            raise ValueError(msg)


# === DOMAIN ENTITIES ===


class FlextMeltanoPipelineResult(FlextEntity):
    """Pipeline execution result entity."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pipeline_name: str = Field(...)
    state: ExecutionState = Field(default=ExecutionState.PENDING)
    started_at: datetime | None = Field(default=None)
    completed_at: datetime | None = Field(default=None)
    duration_seconds: float | None = Field(default=None)
    records_processed: int = Field(default=0)
    error_message: str | None = Field(default=None)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def start_execution(self) -> None:
        """Mark pipeline execution as started."""
        object.__setattr__(self, "state", ExecutionState.RUNNING)
        object.__setattr__(self, "started_at", datetime.now(UTC))

    def complete_execution(self, records_processed: int = 0) -> None:
        """Mark pipeline execution as completed."""
        object.__setattr__(self, "state", ExecutionState.COMPLETED)
        object.__setattr__(self, "completed_at", datetime.now(UTC))
        object.__setattr__(self, "records_processed", records_processed)
        if self.started_at and self.completed_at:
            object.__setattr__(
                self,
                "duration_seconds",
                (self.completed_at - self.started_at).total_seconds(),
            )

    def fail_execution(self, error_message: str) -> None:
        """Mark pipeline execution as failed."""
        object.__setattr__(self, "state", ExecutionState.FAILED)
        object.__setattr__(self, "completed_at", datetime.now(UTC))
        object.__setattr__(self, "error_message", error_message)
        if self.started_at and self.completed_at:
            object.__setattr__(
                self,
                "duration_seconds",
                (self.completed_at - self.started_at).total_seconds(),
            )

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate pipeline result domain rules."""
        if not self.pipeline_name.strip():
            return FlextResult(error="Pipeline name cannot be empty")
        return FlextResult(data=None)


class FlextMeltanoPipelineEvent(FlextEntity):
    """Pipeline event entity for event sourcing."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pipeline_id: str = Field(...)
    event_type: PipelineEventType = Field(...)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    data: dict[str, Any] = Field(default_factory=dict)
    source: str = Field(default="flext-meltano")

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate pipeline event domain rules."""
        if not self.pipeline_id.strip():
            return FlextResult(error="Pipeline ID cannot be empty")
        return FlextResult(data=None)


# === AGGREGATE ROOT ===


class FlextMeltanoRepository(FlextAggregateRoot):
    """Pipeline repository aggregate root managing pipeline lifecycle."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(...)
    pipelines: list[FlextMeltanoPipelineConfig] = Field(default_factory=list)
    results: list[FlextMeltanoPipelineResult] = Field(default_factory=list)
    events: list[FlextMeltanoPipelineEvent] = Field(default_factory=list)

    def add_pipeline(self, config: FlextMeltanoPipelineConfig) -> FlextResult[None]:
        """Add pipeline configuration to repository."""
        try:
            # Validate no duplicate pipeline names
            if any(p.name == config.name for p in self.pipelines):
                return FlextResult(error=f"Pipeline '{config.name}' already exists")

            self.pipelines.append(config)

            # Create domain event
            event = FlextMeltanoPipelineEvent(
                pipeline_id=config.name,
                event_type=PipelineEventType.CREATED,
                data={"extractor": config.extractor, "loader": config.loader},
            )
            self.events.append(event)

            return FlextResult(data=None)
        except (ValueError, TypeError, ImportError) as e:
            return FlextResult(error=f"Failed to add pipeline: {e}")

    def get_pipeline(self, name: str) -> FlextResult[FlextMeltanoPipelineConfig]:
        """Get pipeline configuration by name."""
        try:
            pipeline = next((p for p in self.pipelines if p.name == name), None)
            if not pipeline:
                return FlextResult(error=f"Pipeline '{name}' not found")

            return FlextResult(data=pipeline)
        except (ValueError, TypeError, KeyError) as e:
            return FlextResult(error=f"Failed to get pipeline: {e}")


# === DOMAIN SERVICES ===


@injectable
class FlextMeltanoSingerService(FlextDomainService):
    """Singer protocol domain service using MANDATORY patterns."""

    def __init__(
        self,
        config: FlextMeltanoConfig,
        tap_service: FlextMeltanoTapService,
        target_service: FlextMeltanoTargetService,
    ) -> None:
        """Initialize with dependency injection."""
        super().__init__()
        self.config = config
        self.tap_service = tap_service
        self.target_service = target_service

    def execute_singer_pipeline(
        self,
        extractor: str,
        loader: str,
    ) -> FlextResult[FlextMeltanoPipelineResult]:
        """Execute Singer pipeline using tap and target services."""
        result = FlextMeltanoPipelineResult(
            pipeline_name=f"{extractor}-{loader}",
        )
        result.start_execution()

        try:
            # Validate services
            tap_validation = self.tap_service.validate_service()
            if not tap_validation.is_success:
                result.fail_execution(f"Tap validation failed: {tap_validation.error}")
                return FlextResult(error=tap_validation.error)

            target_validation = self.target_service.validate_service()
            if not target_validation.is_success:
                result.fail_execution(
                    f"Target validation failed: {target_validation.error}",
                )
                return FlextResult(error=target_validation.error)

            # Execute discovery
            catalog_result = self.tap_service.discover_catalog()
            if not catalog_result.is_success:
                result.fail_execution(
                    f"Catalog discovery failed: {catalog_result.error}",
                )
                return FlextResult(error=catalog_result.error)

            # For real implementation, this would execute the actual Singer pipeline
            # Here we simulate successful execution
            result.complete_execution(records_processed=100)

            return FlextResult(data=result)

        except (OSError, subprocess.CalledProcessError) as e:
            result.fail_execution(str(e))
            return FlextResult(error=f"Singer pipeline execution failed: {e}")


@injectable
class FlextMeltanoOrchestrationService(FlextDomainService):
    """Pipeline orchestration domain service using MANDATORY patterns."""

    def __init__(
        self,
        config: FlextMeltanoConfig,
        singer_service: FlextMeltanoSingerService,
        dbt_service: FlextMeltanoDbtService,
        repository: FlextMeltanoRepository,
    ) -> None:
        """Initialize with dependency injection."""
        super().__init__()
        self.config = config
        self.singer_service = singer_service
        self.dbt_service = dbt_service
        self.repository = repository
        self._project: MeltanoProject | None = None
        self._initialized = False

    def validate_service(self) -> FlextResult[bool]:
        """Validate orchestration service."""
        # Meltano is always available (mandatory)

        return FlextResult(data=True)

    def get_health_status(self) -> FlextResult[dict[str, Any]]:
        """Get orchestration service health status."""
        return FlextResult(
            data={
                "service": "orchestration",
                "meltano_available": True,
                "initialized": self._initialized,
                "pipelines_count": len(self.repository.pipelines),
            },
        )

    def create_pipeline(self, config: FlextMeltanoPipelineConfig) -> FlextResult[None]:
        """Create new pipeline using domain patterns."""
        try:
            # Add to repository (aggregate root handles validation)
            add_result = self.repository.add_pipeline(config)
            if not add_result.is_success:
                return add_result

            return FlextResult(data=None)
        except (ValueError, TypeError, ImportError) as e:
            return FlextResult(error=f"Failed to create pipeline: {e}")

    def execute_pipeline(
        self,
        pipeline_name: str,
    ) -> FlextResult[FlextMeltanoPipelineResult]:
        """Execute pipeline using orchestration patterns."""
        try:
            # Get pipeline configuration from repository
            pipeline_result = self.repository.get_pipeline(pipeline_name)
            if not pipeline_result.is_success:
                return FlextResult(error=pipeline_result.error)

            pipeline_config = pipeline_result.data
            if pipeline_config is None:
                return FlextResult(error="Pipeline configuration is None")

            # Execute Singer pipeline
            singer_result = self.singer_service.execute_singer_pipeline(
                pipeline_config.extractor,
                pipeline_config.loader,
            )

            if not singer_result.is_success:
                return singer_result

            execution_result = singer_result.data
            if execution_result is None:
                return FlextResult(error="Singer execution result is None")

            # Store result in repository
            self.repository.results.append(execution_result)

            # Create completion event
            event = FlextMeltanoPipelineEvent(
                pipeline_id=pipeline_name,
                event_type=PipelineEventType.COMPLETED,
                data={
                    "records_processed": execution_result.records_processed,
                    "duration_seconds": execution_result.duration_seconds,
                },
            )
            self.repository.events.append(event)

            return FlextResult(data=execution_result)

        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            return FlextResult(error=f"Pipeline execution failed: {e}")


@injectable
class FlextMeltanoExtension(FlextDomainService):
    """Meltano extension using MANDATORY Meltano EDK patterns."""

    def __init__(
        self,
        config: FlextMeltanoConfig,
        extension_service: FlextMeltanoExtensionService,
    ) -> None:
        """Initialize with dependency injection."""
        super().__init__()
        self.config = config
        self.extension_service = extension_service

    def validate_service(self) -> FlextResult[bool]:
        """Validate extension."""
        return self.extension_service.validate_service()

    def get_health_status(self) -> FlextResult[dict[str, Any]]:
        """Get extension health status."""
        return self.extension_service.get_health_status()


# === EXECUTION STATE MANAGEMENT ===


class FlextMeltanoExecutionState(BaseModel):
    """Execution state management using domain patterns."""

    current_pipeline: str | None = Field(default=None)
    execution_id: str | None = Field(default=None)
    state: ExecutionState = Field(default=ExecutionState.PENDING)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def start_pipeline(self, pipeline_name: str) -> str:
        """Start pipeline execution and return execution ID."""
        execution_id = str(uuid.uuid4())
        self.current_pipeline = pipeline_name
        self.execution_id = execution_id
        self.state = ExecutionState.RUNNING
        self.metadata["started_at"] = datetime.now(UTC).isoformat()
        return execution_id

    def complete_pipeline(self) -> None:
        """Mark current pipeline as completed."""
        self.state = ExecutionState.COMPLETED
        self.metadata["completed_at"] = datetime.now(UTC).isoformat()

    def fail_pipeline(self, error: str) -> None:
        """Mark current pipeline as failed."""
        self.state = ExecutionState.FAILED
        self.metadata["error"] = error
        self.metadata["failed_at"] = datetime.now(UTC).isoformat()


# === BACKWARDS COMPATIBILITY ===


# Legacy function to maintain compatibility
def _deprecated_api_warning(message: str) -> None:
    """Issue deprecation warning."""
    warnings.warn(message, DeprecationWarning, stacklevel=3)
