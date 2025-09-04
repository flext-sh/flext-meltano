"""FLEXT Meltano Types - Meltano-specific type system extending FlextTypes hierarchical system.

Provides comprehensive Meltano-specific types following the FlextTypes pattern with
domain organization, Python 3.13+ type alias syntax, and hierarchical structure.
All types related to Meltano, Singer SDK, DBT, and ELT pipelines are organized under single class.
"""

from __future__ import annotations

from dbt.cli.main import dbtRunner
from flext_core import FlextTypes
from singer_sdk import (
    Stream as SingerStream,
    Tap as SingerTap,
    Target as SingerTarget,
)


class FlextMeltanoTypes(FlextTypes):
    """Meltano-specific hierarchical type system extending FlextTypes.

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
        type Config = (
            FlextTypes.Config.ConfigDict
        )  # Use Config.ConfigDict from flext-core
        type Settings = FlextTypes.Config.ConfigDict  # Settings are configuration

        # Plugin discovery and installation (using flext-core patterns)
        type DiscoveryResult = list[
            FlextTypes.Core.JsonObject
        ]  # List of Core.JsonObject
        type InstallationResult = FlextTypes.Core.JsonObject  # Single JsonObject result
        type PluginInfo = FlextTypes.Core.JsonObject  # Plugin info as JsonObject

        # Plugin execution (using flext-core patterns)
        type Command = list[str]  # Command as list of strings
        type Arguments = list[str]  # Arguments as list of strings
        type Environment = dict[str, str]  # Keep specific str->str mapping

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
        type MessageType = FlextTypes.Payload.MessageType  # Use Payload.MessageType
        type MessageData = FlextTypes.Payload.MessageData  # Consistent message data
        type SchemaMessage = FlextTypes.Core.JsonObject  # Schema as JsonObject
        type RecordMessage = FlextTypes.Core.JsonObject  # Record as JsonObject
        type StateMessage = FlextTypes.Core.JsonObject  # State as JsonObject

        # Stream processing (using flext-core identifiers)
        type StreamName = str  # Stream name as identifier
        type StreamSchema = FlextTypes.Core.JsonObject  # Schema as JsonObject
        type StreamMetadata = FlextTypes.Core.JsonObject  # Metadata as JsonObject

        # Configuration and settings (using flext-core config types)
        type TapConfig = FlextTypes.Config.ConfigDict  # Tap config from Config domain
        type TargetConfig = (
            FlextTypes.Config.ConfigDict
        )  # Target config from Config domain
        type PropertiesList = FlextTypes.Core.JsonObject  # Properties as JsonObject

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
        type Project = FlextTypes.Config.ConfigDict  # Project as ConfigDict
        type Profile = FlextTypes.Config.ConfigDict  # Profile as ConfigDict

        # Model and transformation types (using flext-core identifiers and JSON)
        type Model = str  # Model name as identifier
        type ModelPath = str  # Keep as str for file paths
        type SqlQuery = str  # Keep as str for SQL content
        type CompilationResult = FlextTypes.Core.JsonObject  # Result as JsonObject

        # Execution and results (using flext-core result patterns)
        type RunResult = FlextTypes.Core.JsonObject  # Run result as JsonObject
        type TestResult = FlextTypes.Core.JsonObject  # Test result as JsonObject
        type ExecutionResult = (
            FlextTypes.Core.JsonObject
        )  # Execution result as JsonObject

        # Configuration (using flext-core config types)
        type ProjectConfig = FlextTypes.Config.ConfigDict  # Project config
        type ProfileConfig = FlextTypes.Config.ConfigDict  # Profile config
        type TargetConfig = FlextTypes.Config.ConfigDict  # Target config

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
        type Request = FlextTypes.Payload.MessageData  # Request as message data
        type Response = FlextTypes.Payload.MessageData  # Response as message data
        type JsonPayload = FlextTypes.Core.JsonObject  # Payload as JsonObject

        # Service integration (using flext-core service types)
        type ServiceStatus = str  # Status as identifier
        type ServiceInfo = FlextTypes.Core.JsonObject  # Service info as JsonObject
        type VersionInfo = FlextTypes.Core.JsonObject  # Version info as JsonObject
        type CapabilityInfo = FlextTypes.Core.JsonObject  # Capability as JsonObject

        # Error handling (using flext-core error patterns)
        type ErrorResponse = FlextTypes.Core.JsonObject  # Error response as JsonObject
        type SuccessResponse = (
            FlextTypes.Core.JsonObject
        )  # Success response as JsonObject

    # =========================================================================
    # CLI TYPES - Command-line interface
    # =========================================================================

    class CLI:
        """Command-line interface types extending flext-core base types.

        This class contains types used in CLI implementations,
        leveraging FlextTypes.Commands and FlextTypes.Handler for command processing.
        """

        # Command structure (using flext-core command types)
        type CommandName = (
            FlextTypes.Commands.CommandName
        )  # Command name from Commands domain
        type CommandArgs = list[str]  # Arguments as list of strings
        type CommandResult = (
            FlextTypes.Commands.CommandResult
        )  # Result from Commands domain

        # Execution context (using flext-core handler types)
        type ExecutionContext = (
            FlextTypes.Handler.Context
        )  # Context from Handler domain
        type ProcessResult = FlextTypes.Core.JsonObject  # Process result as JsonObject
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
        type Pipeline = FlextTypes.Config.ConfigDict  # Pipeline as config dict
        type PipelineStage = str  # Stage as identifier
        type PipelineConfig = FlextTypes.Config.ConfigDict  # Pipeline config

        # Execution and results (using basic FlextTypes.Core types)
        type ExtractResult = FlextTypes.Core.JsonObject  # Extract result
        type LoadResult = FlextTypes.Core.JsonObject  # Load result
        type TransformResult = FlextTypes.Core.JsonObject  # Transform result
        type PipelineResult = FlextTypes.Core.JsonObject  # Pipeline result

        # Monitoring and observability (using basic FlextTypes.Core types)
        type ExecutionMetrics = FlextTypes.Core.JsonObject  # Metrics data
        type PerformanceData = FlextTypes.Core.JsonObject  # Performance as JsonObject
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
        type AdapterConfig = FlextTypes.Config.ConfigDict  # Adapter config

        # Adapter operation types (using basic FlextTypes.Core types)
        type OperationResult = FlextTypes.Core.JsonObject  # Operation result
        type AdapterResponse = FlextTypes.Core.JsonObject  # Response as JsonObject
        type ServiceCall = object  # Service call as callable type

        # Integration patterns (using basic FlextTypes.Core types)
        type WrapperResult = FlextTypes.Core.JsonObject  # Wrapper result as JsonObject
        type BridgeResult = FlextTypes.Core.JsonObject  # Bridge result as JsonObject


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    "FlextMeltanoTypes",
]
