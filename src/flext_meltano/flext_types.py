"""Meltano-specific type definitions for the FLEXT ecosystem.

This module provides Meltano-specific types that extend FlextCoreTypes,
organizing all Meltano-related type aliases in a single hierarchical class.

Usage:
    Import types directly from FlextMeltanoTypes::

        from flext_meltano import FlextMeltanoTypes

        # Meltano-specific types
        plugin_config: FlextMeltanoTypes.Plugin.Config = {"name": "tap-csv"}
        tap_instance: FlextMeltanoTypes.Singer.Tap = tap_csv

Architecture:
    - FlextMeltanoTypes: Single hierarchical class extending FlextCoreTypes
    - Domain-organized Meltano type system (Plugin, Singer, DBT, etc.)
    - Modern Python 3.13 type alias syntax throughout
    - All functionality as internal aliases, no implementation
"""

from __future__ import annotations

from collections.abc import Callable

from dbt.cli.main import dbtRunner
from flext_core import FlextCoreTypes
from singer_sdk import (
    Stream as SingerStream,
    Tap as SingerTap,
    Target as SingerTarget,
)


class FlextMeltanoTypes(FlextCoreTypes):
    """Meltano-specific hierarchical type system extending FlextCoreTypes.

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
        """Meltano plugin management types.

        This class contains types used in Meltano plugin management,
        including plugin configurations, discovery, and lifecycle.
        """

        # Plugin identification and metadata
        type Name = str
        type Variant = str
        type Type = str
        type Version = str
        type Config = dict[str, object]
        type Settings = dict[str, object]

        # Plugin discovery and installation
        type DiscoveryResult = list[dict[str, object]]
        type InstallationResult = dict[str, object]
        type PluginInfo = dict[str, object]

        # Plugin execution
        type Command = list[str]
        type Arguments = list[str]
        type Environment = dict[str, str]

    # =========================================================================
    # SINGER TYPES - Singer SDK integration
    # =========================================================================

    class Singer:
        """Singer SDK integration types.

        This class contains types used in Singer SDK integration,
        including taps, targets, streams, and message processing.
        """

        # Core Singer components
        type Tap = SingerTap
        type Target = SingerTarget
        type Stream = SingerStream

        # Singer message system
        type MessageType = str
        type MessageData = dict[str, object]
        type SchemaMessage = dict[str, object]
        type RecordMessage = dict[str, object]
        type StateMessage = dict[str, object]

        # Stream processing
        type StreamName = str
        type StreamSchema = dict[str, object]
        type StreamMetadata = dict[str, object]

        # Configuration and settings
        type TapConfig = dict[str, object]
        type TargetConfig = dict[str, object]
        type PropertiesList = dict[str, object]

    # =========================================================================
    # DBT TYPES - DBT Core transformation
    # =========================================================================

    class DBT:
        """DBT Core transformation types.

        This class contains types used in DBT Core integration,
        including project management, model execution, and testing.
        """

        # DBT Core components
        type Runner = dbtRunner
        type Project = dict[str, object]
        type Profile = dict[str, object]

        # Model and transformation types
        type Model = str
        type ModelPath = str
        type SqlQuery = str
        type CompilationResult = dict[str, object]

        # Execution and results
        type RunResult = dict[str, object]
        type TestResult = dict[str, object]
        type ExecutionResult = dict[str, object]

        # Configuration
        type ProjectConfig = dict[str, object]
        type ProfileConfig = dict[str, object]
        type TargetConfig = dict[str, object]

    # =========================================================================
    # BRIDGE TYPES - Go service integration
    # =========================================================================

    class Bridge:
        """Go service integration types.

        This class contains types used in the Go ↔ Python bridge,
        including JSON API communication and service orchestration.
        """

        # Bridge communication
        type Operation = str
        type Request = dict[str, object]
        type Response = dict[str, object]
        type JsonPayload = dict[str, object]

        # Service integration
        type ServiceStatus = str
        type ServiceInfo = dict[str, object]
        type VersionInfo = dict[str, object]
        type CapabilityInfo = dict[str, object]

        # Error handling
        type ErrorResponse = dict[str, str]
        type SuccessResponse = dict[str, object]

    # =========================================================================
    # CLI TYPES - Command-line interface
    # =========================================================================

    class CLI:
        """Command-line interface types.

        This class contains types used in CLI implementations,
        including command processing and argument handling.
        """

        # Command structure
        type CommandName = str
        type CommandArgs = list[str]
        type CommandResult = dict[str, object]

        # Execution context
        type ExecutionContext = dict[str, object]
        type ProcessResult = dict[str, object]
        type ExitCode = int

    # =========================================================================
    # ELT TYPES - Extract-Load-Transform pipelines
    # =========================================================================

    class ELT:
        """Extract-Load-Transform pipeline types.

        This class contains types used in ELT pipeline orchestration,
        including pipeline stages, execution, and monitoring.
        """

        # Pipeline structure
        type Pipeline = dict[str, object]
        type PipelineStage = str
        type PipelineConfig = dict[str, object]

        # Execution and results
        type ExtractResult = dict[str, object]
        type LoadResult = dict[str, object]
        type TransformResult = dict[str, object]
        type PipelineResult = dict[str, object]

        # Monitoring and observability
        type ExecutionMetrics = dict[str, object]
        type PerformanceData = dict[str, object]
        type PipelineStatus = str

    # =========================================================================
    # ADAPTER TYPES - Service adapter patterns
    # =========================================================================

    class Adapter:
        """Service adapter pattern types.

        This class contains types used in adapter pattern implementations
        for integrating various external services and systems.
        """

        # Adapter identification
        type AdapterName = str
        type AdapterType = str
        type AdapterConfig = dict[str, object]

        # Adapter operation types
        type OperationResult = dict[str, object]
        type AdapterResponse = dict[str, object]
        type ServiceCall = Callable[
            [str], object
        ]  # Specific signature for service calls

        # Integration patterns
        type WrapperResult = dict[str, object]
        type BridgeResult = dict[str, object]


# =============================================================================
# CONVENIENCE ALIASES - For backward compatibility and shorter names
# =============================================================================

# Universal config dictionary type for all configuration objects
ConfigDict = dict[str, object]

# Plugin aliases for easy access
MeltanoPluginConfig = FlextMeltanoTypes.Plugin.Config
MeltanoPluginInfo = FlextMeltanoTypes.Plugin.PluginInfo

# Singer aliases for easy access
SingerTapConfig = FlextMeltanoTypes.Singer.TapConfig
SingerTargetConfig = FlextMeltanoTypes.Singer.TargetConfig
SingerMessageData = FlextMeltanoTypes.Singer.MessageData

# DBT aliases for easy access
DbtProjectConfig = FlextMeltanoTypes.DBT.ProjectConfig
DbtRunResult = FlextMeltanoTypes.DBT.RunResult

# Bridge aliases for easy access
BridgeRequest = FlextMeltanoTypes.Bridge.Request
BridgeResponse = FlextMeltanoTypes.Bridge.Response

# ELT aliases for easy access
ELTPipelineResult = FlextMeltanoTypes.ELT.PipelineResult
ELTExecutionMetrics = FlextMeltanoTypes.ELT.ExecutionMetrics


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Bridge aliases
    "BridgeRequest",
    "BridgeResponse",
    # Configuration dictionary type
    "ConfigDict",
    # DBT aliases
    "DbtProjectConfig",
    "DbtRunResult",
    "ELTExecutionMetrics",
    # ELT aliases
    "ELTPipelineResult",
    # Main hierarchical class
    "FlextMeltanoTypes",
    # Plugin aliases
    "MeltanoPluginConfig",
    "MeltanoPluginInfo",
    "SingerMessageData",
    # Singer aliases
    "SingerTapConfig",
    "SingerTargetConfig",
]
