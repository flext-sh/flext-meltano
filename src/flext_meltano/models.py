"""Domain models for flext-meltano.

- Centralized Pydantic-based models extending flext-core entities/models
- No duplication across modules
- Comprehensive domain modeling following DDD patterns
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4

from flext_core import (
    FlextEntity,
    FlextModel,
    FlextResult,
    FlextValueObject,
)
from pydantic import Field, field_validator

from .constants import (
    SUPPORTED_ENVIRONMENTS,
    FlextMeltanoPluginType,
    FlextSingerMessageType,
)

# =============================================================================
# EXECUTION AND PIPELINE MODELS
# =============================================================================


class FlextMeltanoExecutionStatus(str, Enum):
    """Execution status enumeration."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class FlextMeltanoEvent(FlextEntity):
    """Event entity using flext-core patterns."""

    id: str = Field(default_factory=lambda: str(uuid4()), description="Event ID")
    event_type: str = Field(..., description="Type of event")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source: str = Field(..., description="Event source component")
    data: dict[str, object] = Field(default_factory=dict)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate domain constraints for the event."""
        if not self.event_type.strip():
            return FlextResult.fail("Event type cannot be empty")
        if not self.source.strip():
            return FlextResult.fail("Event source cannot be empty")
        return FlextResult.ok(data=None)


class FlextMeltanoExecutionState(FlextModel):
    """Execution state using flext-core model pattern."""

    current_pipeline: str | None = Field(default=None)
    execution_id: str | None = Field(default=None)
    status: FlextMeltanoExecutionStatus = Field(default=FlextMeltanoExecutionStatus.PENDING)
    metadata: dict[str, object] = Field(default_factory=dict)
    started_at: datetime | None = Field(default=None)
    completed_at: datetime | None = Field(default=None)


class FlextMeltanoPipelineExecution(FlextEntity):
    """Pipeline execution entity with complete tracking."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    pipeline_name: str = Field(...)
    tap_name: str = Field(...)
    target_name: str = Field(...)
    status: FlextMeltanoExecutionStatus = Field(default=FlextMeltanoExecutionStatus.PENDING)
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = Field(default=None)
    error_message: str | None = Field(default=None)
    records_processed: int = Field(default=0)
    execution_context: dict[str, object] = Field(default_factory=dict)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate pipeline execution constraints."""
        if not self.pipeline_name.strip():
            return FlextResult.fail("Pipeline name cannot be empty")
        if not self.tap_name.strip():
            return FlextResult.fail("Tap name cannot be empty")
        if not self.target_name.strip():
            return FlextResult.fail("Target name cannot be empty")
        return FlextResult.ok(data=None)

    def mark_completed(self, records_processed: int = 0) -> None:
        """Mark execution as completed."""
        self.status = FlextMeltanoExecutionStatus.COMPLETED
        self.completed_at = datetime.now(UTC)
        self.records_processed = records_processed

    def mark_failed(self, error_message: str) -> None:
        """Mark execution as failed."""
        self.status = FlextMeltanoExecutionStatus.FAILED
        self.completed_at = datetime.now(UTC)
        self.error_message = error_message


# =============================================================================
# PLUGIN MANAGEMENT MODELS
# =============================================================================


class FlextMeltanoPlugin(FlextEntity):
    """Meltano plugin entity with configuration."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(...)
    plugin_type: FlextMeltanoPluginType = Field(...)
    namespace: str = Field(...)
    pip_url: str | None = Field(default=None)
    executable: str | None = Field(default=None)
    config: dict[str, object] = Field(default_factory=dict)
    capabilities: list[str] = Field(default_factory=list)
    settings: dict[str, object] = Field(default_factory=dict)
    installed: bool = Field(default=False)
    plugin_version: str | None = Field(default=None)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate plugin constraints."""
        if not self.name.strip():
            return FlextResult.fail("Plugin name cannot be empty")
        if not self.namespace.strip():
            return FlextResult.fail("Plugin namespace cannot be empty")
        return FlextResult.ok(data=None)

    def is_extractable(self) -> bool:
        """Check if plugin can extract data."""
        return self.plugin_type == FlextMeltanoPluginType.EXTRACTORS

    def is_loadable(self) -> bool:
        """Check if plugin can load data."""
        return self.plugin_type == FlextMeltanoPluginType.LOADERS


class FlextMeltanoPluginRegistry(FlextModel):
    """Registry of available plugins."""

    plugins: dict[str, FlextMeltanoPlugin] = Field(default_factory=dict)
    last_updated: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def add_plugin(self, plugin: FlextMeltanoPlugin) -> FlextResult[None]:
        """Add plugin to registry."""
        validation_result = plugin.validate_business_rules()
        if not validation_result.success:
            return validation_result

        self.plugins[plugin.name] = plugin
        self.last_updated = datetime.now(UTC)
        return FlextResult.ok(data=None)

    def get_plugin(self, name: str) -> FlextResult[FlextMeltanoPlugin]:
        """Get plugin by name."""
        if name not in self.plugins:
            return FlextResult.fail(f"Plugin '{name}' not found in registry")
        return FlextResult.ok(data=self.plugins[name])

    def list_plugins_by_type(self, plugin_type: FlextMeltanoPluginType) -> list[FlextMeltanoPlugin]:
        """List plugins by type."""
        return [plugin for plugin in self.plugins.values() if plugin.plugin_type == plugin_type]


# =============================================================================
# SINGER PROTOCOL MODELS
# =============================================================================


class FlextSingerMessage(FlextValueObject):
    """Singer protocol message value object."""

    message_type: FlextSingerMessageType = Field(...)
    record: dict[str, object] | None = Field(default=None)
    message_schema: dict[str, object] | None = Field(default=None)
    state: dict[str, object] | None = Field(default=None)
    stream: str | None = Field(default=None)
    time_extracted: datetime | None = Field(default=None)
    version: int | None = Field(default=None)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate Singer message constraints."""
        if self.message_type == FlextSingerMessageType.RECORD and not self.record:
            return FlextResult.fail("RECORD message must have record data")
        if self.message_type == FlextSingerMessageType.SCHEMA and not self.message_schema:
            return FlextResult.fail("SCHEMA message must have schema data")
        if self.message_type == FlextSingerMessageType.STATE and not self.state:
            return FlextResult.fail("STATE message must have state data")
        return FlextResult.ok(data=None)


class FlextSingerCatalog(FlextModel):
    """Singer catalog model with stream definitions."""

    streams: list[dict[str, object]] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    tap_name: str | None = Field(default=None)

    def add_stream(self, stream_definition: dict[str, object]) -> FlextResult[None]:
        """Add stream definition to catalog."""
        if "tap_stream_id" not in stream_definition:
            return FlextResult.fail("Stream definition must have tap_stream_id")

        self.streams.append(stream_definition)
        return FlextResult.ok(data=None)

    def get_stream_names(self) -> list[str]:
        """Get list of stream names."""
        return [str(stream.get("tap_stream_id", "")) for stream in self.streams if "tap_stream_id" in stream]


# =============================================================================
# PROJECT CONFIGURATION MODELS
# =============================================================================


class FlextMeltanoProject(FlextEntity):
    """Meltano project entity with metadata."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(...)
    project_root: str = Field(...)
    environment: str = Field(default="dev")
    database_uri: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    plugins: dict[str, FlextMeltanoPlugin] = Field(default_factory=dict)
    schedules: list[dict[str, object]] = Field(default_factory=list)
    jobs: list[dict[str, object]] = Field(default_factory=list)

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        """Validate environment is supported."""
        if value not in SUPPORTED_ENVIRONMENTS:
            supported = ", ".join(SUPPORTED_ENVIRONMENTS)
            msg = f"Environment '{value}' not supported. Use one of: {supported}"
            raise ValueError(msg)
        return value

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate project constraints."""
        if not self.name.strip():
            return FlextResult.fail("Project name cannot be empty")
        if not self.project_root.strip():
            return FlextResult.fail("Project root cannot be empty")
        return FlextResult.ok(data=None)

    def add_plugin(self, plugin: FlextMeltanoPlugin) -> FlextResult[None]:
        """Add plugin to project."""
        validation_result = plugin.validate_business_rules()
        if not validation_result.success:
            return validation_result

        self.plugins[plugin.name] = plugin
        self.updated_at = datetime.now(UTC)
        return FlextResult.ok(data=None)


# =============================================================================
# BRIDGE INTEGRATION MODELS
# =============================================================================


class FlextMeltanoBridgeRequest(FlextModel):
    """Bridge request model for Go integration."""

    operation: str = Field(...)
    parameters: dict[str, object] = Field(default_factory=dict)
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("operation")
    @classmethod
    def validate_operation(cls, value: str) -> str:
        """Validate operation is not empty."""
        if not value.strip():
            msg = "Operation cannot be empty"
            raise ValueError(msg)
        return value


class FlextMeltanoBridgeResponse(FlextModel):
    """Bridge response model for Go integration."""

    success: bool = Field(...)
    data: dict[str, object] | list[object] | str | int | float | None = Field(default=None)
    error: str | None = Field(default=None)
    correlation_id: str | None = Field(default=None)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    execution_time_ms: int | None = Field(default=None)

    @classmethod
    def success_response(
        cls,
        data: dict[str, object] | list[object] | str | float | None = None,
        correlation_id: str | None = None,
    ) -> FlextMeltanoBridgeResponse:
        """Create success response."""
        return cls(success=True, data=data, correlation_id=correlation_id)

    @classmethod
    def error_response(
        cls,
        error: str,
        correlation_id: str | None = None,
    ) -> FlextMeltanoBridgeResponse:
        """Create error response."""
        return cls(success=False, error=error, correlation_id=correlation_id)


__all__ = [
    # Bridge models
    "FlextMeltanoBridgeRequest",
    "FlextMeltanoBridgeResponse",
    # Execution models
    "FlextMeltanoEvent",
    "FlextMeltanoExecutionState",
    "FlextMeltanoExecutionStatus",
    "FlextMeltanoPipelineExecution",
    # Plugin models
    "FlextMeltanoPlugin",
    "FlextMeltanoPluginRegistry",
    # Project models
    "FlextMeltanoProject",
    "FlextSingerCatalog",
    # Singer models
    "FlextSingerMessage",
]
