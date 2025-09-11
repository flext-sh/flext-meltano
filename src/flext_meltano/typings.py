"""FLEXT Meltano Types - Meltano-specific type system extending FlextTypes hierarchical system.

Provides comprehensive Meltano-specific types following the FlextTypes pattern with
domain organization, hierarchical structure, and type-safe annotations for Meltano operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import (
    Protocol,
    TypeVar,
    runtime_checkable,
)

from dbt.cli.main import dbtRunner
from flext_core import FlextTypes  # Use flext-core type variables
from singer_sdk import (
    Stream as SingerStream,
    Tap as SingerTap,
    Target as SingerTarget,
)

# Use flext-core type variables - eliminate duplication
T_co = TypeVar("T_co", covariant=True)  # Keep this one as it needs covariance
# U and V now come from flext-core

# Python 3.13+ Type aliases - USE FlextTypes directly (eliminate duplication)
type ConfigValue = FlextTypes.Core.ConfigValue  # ✅ ALIAS to eliminate duplication
type ConfigDict = FlextTypes.Core.ConfigDict  # ✅ ALIAS to eliminate duplication
type JsonValue = FlextTypes.Core.JsonValue  # ✅ ALIAS to eliminate duplication
type JsonObject = FlextTypes.Core.JsonObject  # ✅ ALIAS to eliminate duplication

# Advanced Python 3.13+ Union and Intersection Types
type MessageType = str
type MessageData = FlextTypes.Core.Dict
type CommandName = str
type CommandResult = object
type HandlerContext = FlextTypes.Core.Dict


class FlextMeltanoTypes:
    """UNIFIED Meltano Types - SINGLE RESPONSIBILITY PATTERN.

    Meltano-specific hierarchical type system extending FlextTypes with consolidated protocols.

    This class inherits all core FLEXT types and adds Meltano-specific
    type definitions organized by domain functionality.

    The type system adds the following Meltano domains:
        - Plugin: Meltano plugin management types
        - Singer: Singer SDK tap/target types
        - DBT: DBT Core transformation types
        - Bridge: Go service integration types
        - CLI: Command-line interface types
        - ELT: Extract-Load-Transform pipeline types

    Examples:
        Using Meltano-specific types::

            from flext_meltano import FlextMeltanoTypes

            plugin_config: FlextMeltanoTypes.Plugin.Config = {
                "name": "tap-csv",
                "variant": "meltanolabs",
            }

            tap: FlextMeltanoTypes.Singer.Tap = csv_tap
            pipeline_result: FlextMeltanoTypes.ELT.PipelineResult = success_result

    """

    # =========================================================================
    # NESTED PROTOCOL DEFINITIONS - Domain-specific structural typing
    # =========================================================================

    @runtime_checkable
    class MeltanoPluginProtocol(Protocol[T_co]):
        """Advanced protocol for Meltano plugin interface with covariant constraints."""

        def get_config(self) -> ConfigDict:
            """Get plugin configuration."""
            ...

        def validate_config(self, config: ConfigDict) -> bool:
            """Validate plugin configuration."""
            ...

        def execute(self, *args: object) -> T_co:
            """Execute plugin with given arguments."""
            ...

    @runtime_checkable
    class SingerStreamProtocol(Protocol):
        """Protocol for Singer stream implementations with type safety."""

        name: str
        tap_stream_id: str
        schema: JsonObject

        def sync_records(self) -> JsonValue:
            """Sync records from the stream."""
            ...

        def get_records(self) -> JsonValue:
            """Get records from the stream."""
            ...

    # =========================================================================
    # DOMAIN TYPE CLASSES
    # =========================================================================

    # =========================================================================
    # PLUGIN TYPES - Meltano plugin management
    # =========================================================================

    class Plugin:
        """Meltano plugin management types extending flext-core base types.

        This class contains types used in Meltano plugin management,
        using FlextTypes.Core and FlextTypes.Config as foundation for type safety.
        """

        # Plugin identification and metadata (using appropriate types)
        type Name = str  # Plugin name identifier
        type Variant = str  # Plugin variant identifier
        type Type = str  # Plugin type identifier
        type Version = str  # Keep as str since versions have specific format
        type Config = ConfigDict  # ConfigDict type
        type Settings = ConfigDict  # Settings are configuration

        # Plugin discovery and installation (using flext-core patterns)
        type DiscoveryResult = list[JsonObject]  # List of JsonObject
        type InstallationResult = JsonObject  # Single JsonObject result
        type PluginInfo = JsonObject  # Plugin info as JsonObject

        # Plugin execution (using flext-core patterns)
        type Command = FlextTypes.Core.StringList  # Command as list of strings
        type Arguments = FlextTypes.Core.StringList  # Arguments as list of strings
        type Environment = FlextTypes.Core.Headers  # Keep specific str->str mapping

    # =========================================================================
    # SINGER TYPES - Singer SDK integration
    # =========================================================================

    class Singer:
        """Singer SDK integration types extending flext-core base types.

        This class contains types used in Singer SDK integration,
        leveraging FlextTypes.Core and FlextTypes.Payload for message processing.
        """

        # Core Singer components (keep external Singer SDK types)
        type Tap = SingerTap
        type Target = SingerTarget
        type Stream = SingerStream

        # Singer message system (using flext-core message types)
        type MessageType = MessageType  # Use Payload.MessageType
        type MessageData = MessageData  # Consistent message data
        type SchemaMessage = JsonObject  # Schema as JsonObject
        type RecordMessage = JsonObject  # Record as JsonObject
        type StateMessage = JsonObject  # State as JsonObject

        # Stream processing (using flext-core identifiers)
        type StreamName = str  # Stream name as identifier
        type StreamSchema = JsonObject  # Schema as JsonObject
        type StreamMetadata = JsonObject  # Metadata as JsonObject

        # Configuration and settings (using flext-core config types)
        type TapConfig = ConfigDict  # Tap config from Config domain
        type TargetConfig = ConfigDict  # Target config from Config domain
        type PropertiesList = JsonObject  # Properties as JsonObject

    # =========================================================================
    # DBT TYPES - DBT Core transformation
    # =========================================================================

    class DBT:
        """DBT Core transformation types extending flext-core base types.

        This class contains types used in DBT Core integration,
        leveraging FlextTypes.Core and FlextTypes.Config for configuration management.
        """

        # DBT Core components (keep external DBT types)
        type Runner = dbtRunner
        type Project = ConfigDict  # Project as ConfigDict
        type Profile = ConfigDict  # Profile as ConfigDict

        # Model and transformation types (using flext-core identifiers and JSON)
        type Model = str  # Model name as identifier
        type ModelPath = str  # Keep as str for file paths
        type SqlQuery = str  # Keep as str for SQL content
        type CompilationResult = JsonObject  # Result as JsonObject

        # Execution and results (using flext-core result patterns)
        type RunResult = JsonObject  # Run result as JsonObject
        type TestResult = JsonObject  # Test result as JsonObject
        type ExecutionResult = JsonObject  # Execution result as JsonObject

        # Configuration (using flext-core config types)
        type ProjectConfig = ConfigDict  # Project config
        type ProfileConfig = ConfigDict  # Profile config
        type TargetConfig = ConfigDict  # Target config

    # =========================================================================
    # BRIDGE TYPES - Go service integration
    # =========================================================================

    class Bridge:
        """Go service integration types extending flext-core base types.

        This class contains types used in the Go ↔ Python bridge,
        leveraging FlextTypes.Network and FlextTypes.Payload for communication.
        """

        # Bridge communication (using flext-core network and payload types)
        type Operation = str  # Operation as identifier
        type Request = MessageData  # Request as message data
        type Response = MessageData  # Response as message data
        type JsonPayload = JsonObject  # Payload as JsonObject

        # Service integration (using flext-core service types)
        type ServiceStatus = str  # Status as identifier
        type ServiceInfo = JsonObject  # Service info as JsonObject
        type VersionInfo = JsonObject  # Version info as JsonObject
        type CapabilityInfo = JsonObject  # Capability as JsonObject

        # Error handling (using flext-core error patterns)
        type ErrorResponse = JsonObject  # Error response as JsonObject
        type SuccessResponse = JsonObject  # Success response as JsonObject

    # =========================================================================
    # CLI TYPES - Command-line interface
    # =========================================================================

    class CLI:
        """Command-line interface types extending flext-core base types.

        This class contains types used in CLI implementations,
        leveraging FlextTypes.Commands and FlextTypes.Handler for command processing.
        """

        # Command structure (using flext-core command types)
        type CommandName = CommandName  # Command name from Commands domain
        type CommandArgs = FlextTypes.Core.StringList  # Arguments as list of strings
        type CommandResult = CommandResult  # Result from Commands domain

        # Execution context (using flext-core handler types)
        type ExecutionContext = HandlerContext  # Context from Handler domain
        type ProcessResult = JsonObject  # Process result as JsonObject
        type ExitCode = int  # Keep as int for exit codes

    # =========================================================================
    # ELT TYPES - Extract-Load-Transform pipelines
    # =========================================================================

    class ELT:
        """Extract-Load-Transform pipeline types extending flext-core base types.

        This class contains types used in ELT pipeline orchestration,
        leveraging FlextTypes.Config for pipeline management.
        """

        # Pipeline structure (using flext-core config types)
        type Pipeline = ConfigDict  # Pipeline as config dict
        type PipelineStage = str  # Stage as identifier
        type PipelineConfig = ConfigDict  # Pipeline config

        # Execution and results (using basic FlextTypes.Core types)
        type ExtractResult = JsonObject  # Extract result
        type LoadResult = JsonObject  # Load result
        type TransformResult = JsonObject  # Transform result
        type PipelineResult = JsonObject  # Pipeline result

        # Monitoring and observability (using basic FlextTypes.Core types)
        type ExecutionMetrics = JsonObject  # Metrics data
        type PerformanceData = JsonObject  # Performance as JsonObject
        type PipelineStatus = str  # Status as identifier

    # =========================================================================
    # ADAPTER TYPES - Service adapter patterns
    # =========================================================================

    class Adapter:
        """Service adapter pattern types extending flext-core base types.

        This class contains types used in adapter pattern implementations
        leveraging FlextTypes.Service and FlextTypes.Core for service integration.
        """

        # Adapter identification (using flext-core service types)
        type AdapterName = str  # Adapter name as service identifier
        type AdapterType = str  # Adapter type as identifier
        type AdapterConfig = ConfigDict  # Adapter config

        # Adapter operation types (using basic FlextTypes.Core types)
        type OperationResult = JsonObject  # Operation result
        type AdapterResponse = JsonObject  # Response as JsonObject
        type ServiceCall = object  # Service call as callable type

        # Integration patterns (using basic FlextTypes.Core types)
        type WrapperResult = JsonObject  # Wrapper result as JsonObject
        type BridgeResult = JsonObject  # Bridge result as JsonObject


__all__ = [
    "FlextMeltanoTypes",
]
