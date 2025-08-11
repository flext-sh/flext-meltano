"""FLEXT Meltano Models - Consolidated Domain Models and Singer Schemas.

**Architecture Layer**: Domain and Schema Definition Layer
**Status**: ✅ STABLE - Domain models and Singer schema patterns consolidation
**Dependencies**: flext-core (FlextEntity, FlextModel, FlextValueObject), Singer SDK

## Module Purpose

This module provides **consolidated domain models and Singer schema definitions**
for FLEXT Meltano's bridge architecture, combining domain modeling following DDD
patterns with centralized Singer schema definitions for maximum code reuse.

**CONSOLIDATION**: This module consolidates:
- models.py: Domain models, entities, and business logic
- common_schemas.py: Singer schema definitions and factory functions

## Design Principles

1. **Domain-Driven Design**: Complete domain modeling with FlextResult integration
2. **DRY Implementation**: Eliminate schema duplication across Singer projects
3. **Type Safety**: Singer SDK typing integration with validation
4. **Extensibility**: Factory functions for customized schema creation
5. **Bridge Integration**: JSON-serializable models for Go service consumption

## Core Components

### Domain Models (from models.py)
- Execution and pipeline models
- Plugin management models
- Singer protocol models
- Project configuration models
- Bridge integration models

### Singer Schemas (from common_schemas.py)
- Connection schemas for various data sources
- Extraction configuration patterns
- Factory functions for schema creation
- Bridge integration patterns

All code is production-grade, fully typed, and SOLID compliant.
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING, ClassVar
from uuid import uuid4

from flext_core import (
    FlextEntity,
    FlextModel,
    FlextResult,
    FlextValueObject,
)
from pydantic import Field, field_validator
from singer_sdk import typing as th

if TYPE_CHECKING:
    pass

# Import constants from the new consolidated module
from .meltano_config import (
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
        return FlextResult.ok(None)


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
        return FlextResult.ok(None)

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
        return FlextResult.ok(None)

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
        return FlextResult.ok(None)

    def get_plugin(self, name: str) -> FlextResult[FlextMeltanoPlugin]:
        """Get plugin by name."""
        if name not in self.plugins:
            return FlextResult.fail(f"Plugin '{name}' not found in registry")
        return FlextResult.ok(self.plugins[name])

    def list_plugins_by_type(self, plugin_type: FlextMeltanoPluginType) -> list[FlextMeltanoPlugin]:
        """List plugins by type."""
        return [plugin for plugin in self.plugins.values() if plugin.plugin_type == plugin_type]


class FlextMeltanoPluginInfo(FlextModel):
    """Centralized plugin information model - NO DUPLICATION."""

    name: str = Field(..., description="Plugin name")
    type: str = Field(..., description="Plugin type (extractor/loader/transformer)")
    namespace: str = Field(..., description="Plugin namespace")
    description: str = Field(default="", description="Plugin description")
    version: str = Field(default="latest", description="Plugin version")
    pip_url: str | None = Field(default=None, description="Pip installation URL")
    executable: str | None = Field(default=None, description="Plugin executable")
    installed: bool = Field(default=False, description="Whether plugin is installed")
    capabilities: list[str] = Field(default_factory=list, description="Plugin capabilities")


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
        return FlextResult.ok(None)


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
        return FlextResult.ok(None)

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
        return FlextResult.ok(None)

    def add_plugin(self, plugin: FlextMeltanoPlugin) -> FlextResult[None]:
        """Add plugin to project."""
        validation_result = plugin.validate_business_rules()
        if not validation_result.success:
            return validation_result

        self.plugins[plugin.name] = plugin
        self.updated_at = datetime.now(UTC)
        return FlextResult.ok(None)


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


# =============================================================================
# SINGER SCHEMA DEFINITIONS (from common_schemas.py)
# =============================================================================


class CommonSingerSchemas:
    """REAL centralization of common Singer schema patterns."""

    # Common database connection schemas
    DATABASE_CONNECTION_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
        th.Property(
            "host",
            th.StringType,
            required=True,
            description="Database host",
        ),
        th.Property(
            "port",
            th.IntegerType,
            description="Database port",
        ),
        th.Property(
            "username",
            th.StringType,
            required=True,
            description="Database username",
        ),
        th.Property(
            "password",
            th.StringType,
            required=True,
            secret=True,
            description="Database password",
        ),
        th.Property(
            "database",
            th.StringType,
            required=True,
            description="Database name",
        ),
    )

    # Oracle-specific connection schema
    ORACLE_CONNECTION_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
        *DATABASE_CONNECTION_SCHEMA.wrapped.values(),
        th.Property(
            "service_name",
            th.StringType,
            description="Oracle service name",
        ),
        th.Property(
            "sid",
            th.StringType,
            description="Oracle SID",
        ),
    )

    # LDAP connection schema
    LDAP_CONNECTION_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
        th.Property(
            "ldap_host",
            th.StringType,
            required=True,
            description="LDAP server host",
        ),
        th.Property(
            "ldap_port",
            th.IntegerType,
            default=389,
            description="LDAP server port",
        ),
        th.Property(
            "bind_dn",
            th.StringType,
            required=True,
            description="LDAP bind DN",
        ),
        th.Property(
            "bind_password",
            th.StringType,
            required=True,
            secret=True,
            description="LDAP bind password",
        ),
        th.Property(
            "base_dn",
            th.StringType,
            required=True,
            description="LDAP base DN",
        ),
        th.Property(
            "use_tls",
            th.BooleanType,
            default=False,
            description="Use TLS connection",
        ),
    )

    # File source schema
    FILE_SOURCE_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
        th.Property(
            "file_path",
            th.StringType,
            required=True,
            description="File path or URL",
        ),
        th.Property(
            "file_format",
            th.StringType,
            default="csv",
            description="File format (csv, json, parquet)",
        ),
        th.Property(
            "encoding",
            th.StringType,
            default="utf-8",
            description="File encoding",
        ),
    )

    # OAuth2 API schema
    OAUTH2_API_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            description="OAuth2 client ID",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            secret=True,
            description="OAuth2 client secret",
        ),
        th.Property(
            "auth_url",
            th.StringType,
            required=True,
            description="OAuth2 authorization URL",
        ),
        th.Property(
            "token_url",
            th.StringType,
            required=True,
            description="OAuth2 token URL",
        ),
        th.Property(
            "api_base_url",
            th.StringType,
            required=True,
            description="API base URL",
        ),
    )

    # Oracle OIC schema
    ORACLE_OIC_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
        th.Property(
            "oic_host",
            th.StringType,
            required=True,
            description="Oracle Integration Cloud host",
        ),
        th.Property(
            "username",
            th.StringType,
            required=True,
            description="OIC username",
        ),
        th.Property(
            "password",
            th.StringType,
            required=True,
            secret=True,
            description="OIC password",
        ),
        th.Property(
            "api_version",
            th.StringType,
            default="v1",
            description="OIC API version",
        ),
    )

    # Common extraction configuration
    EXTRACTION_CONFIG_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Start date for extraction",
        ),
        th.Property(
            "end_date",
            th.DateTimeType,
            description="End date for extraction",
        ),
        th.Property(
            "batch_size",
            th.IntegerType,
            default=1000,
            description="Batch size for extraction",
        ),
        th.Property(
            "max_records",
            th.IntegerType,
            description="Maximum records to extract",
        ),
        th.Property(
            "stream_maps",
            th.ObjectType(),
            description="Stream mappings configuration",
        ),
        th.Property(
            "stream_map_config",
            th.ObjectType(),
            description="Stream map configuration",
        ),
    )

    @classmethod
    def create_tap_schema(
        cls,
        connection_type: str,
        *,
        include_extraction_config: bool = True,
        additional_properties: th.PropertiesList | None = None,
    ) -> th.PropertiesList:
        """Create tap schemas with REAL reusability.

        Args:
            connection_type: Type of connection (oracle, ldap, file)
            include_extraction_config: Include common extraction settings
            additional_properties: Additional tap-specific properties

        Returns:
            Complete schema for the tap

        """
        # Get base connection schema properties
        if connection_type == "oracle":
            base_properties = list(cls.ORACLE_CONNECTION_SCHEMA.wrapped.values())
        elif connection_type == "ldap":
            base_properties = list(cls.LDAP_CONNECTION_SCHEMA.wrapped.values())
        elif connection_type == "file":
            base_properties = list(cls.FILE_SOURCE_SCHEMA.wrapped.values())
        elif connection_type == "oauth2":
            base_properties = list(cls.OAUTH2_API_SCHEMA.wrapped.values())
        elif connection_type == "oracle_oic":
            base_properties = list(cls.ORACLE_OIC_SCHEMA.wrapped.values())
        else:
            base_properties = list(cls.DATABASE_CONNECTION_SCHEMA.wrapped.values())

        # Build complete properties list
        all_properties = base_properties.copy()

        # Add extraction configuration if requested
        if include_extraction_config:
            all_properties.extend(cls.EXTRACTION_CONFIG_SCHEMA.wrapped.values())

        if additional_properties:
            all_properties.extend(additional_properties.wrapped.values())

        return th.PropertiesList(*all_properties)


# Factory functions for easy usage
def create_oracle_tap_schema(
    additional_properties: th.PropertiesList | None = None,
) -> th.PropertiesList:
    """Create Oracle tap schema with common patterns."""
    return CommonSingerSchemas.create_tap_schema(
        "oracle",
        include_extraction_config=True,
        additional_properties=additional_properties,
    )


def create_ldap_tap_schema(
    additional_properties: th.PropertiesList | None = None,
) -> th.PropertiesList:
    """Create LDAP tap schema with common patterns."""
    return CommonSingerSchemas.create_tap_schema(
        "ldap",
        include_extraction_config=True,
        additional_properties=additional_properties,
    )


def create_file_tap_schema(
    additional_properties: th.PropertiesList | None = None,
) -> th.PropertiesList:
    """Create file-based tap schema with common patterns."""
    return CommonSingerSchemas.create_tap_schema(
        "file",
        include_extraction_config=True,
        additional_properties=additional_properties,
    )


def create_oauth2_api_tap_schema(
    additional_properties: th.PropertiesList | None = None,
) -> th.PropertiesList:
    """Create OAuth2 API tap schema with common patterns."""
    return CommonSingerSchemas.create_tap_schema(
        "oauth2",
        include_extraction_config=True,
        additional_properties=additional_properties,
    )


def create_oracle_oic_tap_schema(
    additional_properties: th.PropertiesList | None = None,
) -> th.PropertiesList:
    """Create Oracle OIC tap schema with common patterns."""
    return CommonSingerSchemas.create_tap_schema(
        "oracle_oic",
        include_extraction_config=True,
        additional_properties=additional_properties,
    )


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
    "FlextMeltanoPluginInfo",
    "FlextMeltanoPluginRegistry",
    # Project models
    "FlextMeltanoProject",
    "FlextSingerCatalog",
    # Singer models
    "FlextSingerMessage",
    # Singer schemas
    "CommonSingerSchemas",
    "create_file_tap_schema",
    "create_ldap_tap_schema",
    "create_oauth2_api_tap_schema",
    "create_oracle_oic_tap_schema",
    "create_oracle_tap_schema",
]