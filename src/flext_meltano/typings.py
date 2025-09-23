"""FLEXT Meltano Types - Unified Meltano type definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextTypes

# Python 3.13+ Type aliases - USE FlextTypes directly (eliminate duplication)
type ConfigValue = FlextTypes.Core.ConfigValue
type ConfigDict = FlextTypes.Core.ConfigDict
type JsonValue = FlextTypes.Core.JsonValue
type JsonObject = FlextTypes.Core.JsonObject

# Advanced Python 3.13+ Union and Intersection Types
type MessageType = str
type MessageData = FlextTypes.Core.Dict
type CommandName = str
type CommandResult = JsonObject
type HandlerContext = FlextTypes.Core.Dict

# Singer SDK external types (JSON-based for type safety)
type SingerTapProtocol = JsonObject
type SingerTargetProtocol = JsonObject
type SingerStreamProtocol = JsonObject

# DBT Core external types (JSON-based for type safety)
type DbtRunnerProtocol = JsonObject

# Service call types (JSON-based for type safety)
type ServiceCallProtocol = JsonValue


class FlextMeltanoTypes:
    """UNIFIED Meltano Types - SINGLE RESPONSIBILITY PATTERN.

    Domain-specific type system using FlextTypes.Core as SOURCE OF TRUTH.
    Contains ONLY Meltano-specific types that cannot be generalized.

    ZERO DUPLICATION PRINCIPLE:
    - FlextTypes.Core is SOURCE OF TRUTH for common types
    - Contains ONLY Meltano ELT domain-specific types
    - All type aliases use FlextTypes directly

    The type system organizes Meltano-specific domains:
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
    # PLUGIN TYPES - Meltano plugin management (DOMAIN-SPECIFIC)
    # =========================================================================

    class Plugin:
        """Meltano plugin management types using FlextTypes.Core foundation."""

        # Plugin identification (domain-specific identifiers)
        type Name = str
        type Variant = str
        type Type = str
        type Version = str

        # Configuration using FlextTypes.Core
        type Config = FlextTypes.Core.ConfigDict
        type Settings = FlextTypes.Core.ConfigDict

        # Plugin operations using FlextTypes.Core
        type DiscoveryResult = list[FlextTypes.Core.JsonObject]
        type InstallationResult = FlextTypes.Core.JsonObject
        type PluginInfo = FlextTypes.Core.JsonObject

        # Execution using FlextTypes.Core
        type Command = FlextTypes.Core.StringList
        type Arguments = FlextTypes.Core.StringList
        type Environment = FlextTypes.Core.Headers

    # =========================================================================
    # SINGER TYPES - Singer SDK integration (DOMAIN-SPECIFIC)
    # =========================================================================

    class Singer:
        """Singer SDK integration types using FlextTypes.Core foundation."""

        # Core Singer components (domain-specific protocols)
        type Tap = SingerTapProtocol
        type Target = SingerTargetProtocol
        type Stream = SingerStreamProtocol

        # Singer message system using FlextTypes.Core
        type MessageType = str
        type MessageData = FlextTypes.Core.Dict
        type SchemaMessage = FlextTypes.Core.JsonObject
        type RecordMessage = FlextTypes.Core.JsonObject
        type StateMessage = FlextTypes.Core.JsonObject

        # Stream processing using FlextTypes.Core
        type StreamName = str
        type StreamSchema = FlextTypes.Core.JsonObject
        type StreamMetadata = FlextTypes.Core.JsonObject

        # Configuration using FlextTypes.Core
        type TapConfig = FlextTypes.Core.ConfigDict
        type TargetConfig = FlextTypes.Core.ConfigDict
        type PropertiesList = FlextTypes.Core.JsonObject

    # =========================================================================
    # DBT TYPES - DBT Core transformation (DOMAIN-SPECIFIC)
    # =========================================================================

    class DBT:
        """DBT Core transformation types using FlextTypes.Core foundation."""

        # DBT Core components (domain-specific protocols)
        type Runner = DbtRunnerProtocol
        type Project = FlextTypes.Core.ConfigDict
        type Profile = FlextTypes.Core.ConfigDict

        # Model and transformation types (domain-specific)
        type Model = str
        type ModelPath = str
        type SqlQuery = str
        type CompilationResult = FlextTypes.Core.JsonObject

        # Execution and results using FlextTypes.Core
        type RunResult = FlextTypes.Core.JsonObject
        type TestResult = FlextTypes.Core.JsonObject
        type ExecutionResult = FlextTypes.Core.JsonObject

        # Configuration using FlextTypes.Core
        type ProjectConfig = FlextTypes.Core.ConfigDict
        type ProfileConfig = FlextTypes.Core.ConfigDict
        type TargetConfig = FlextTypes.Core.ConfigDict

    # =========================================================================
    # BRIDGE TYPES - Go service integration (DOMAIN-SPECIFIC)
    # =========================================================================

    class Bridge:
        """Go service integration types using FlextTypes.Core foundation."""

        # Bridge communication using FlextTypes.Core
        type Operation = str
        type Request = FlextTypes.Core.Dict
        type Response = FlextTypes.Core.Dict
        type JsonPayload = FlextTypes.Core.JsonObject

        # Service integration using FlextTypes.Core
        type ServiceStatus = str
        type ServiceInfo = FlextTypes.Core.JsonObject
        type VersionInfo = FlextTypes.Core.JsonObject
        type CapabilityInfo = FlextTypes.Core.JsonObject

        # Error handling using FlextTypes.Core
        type ErrorResponse = FlextTypes.Core.JsonObject
        type SuccessResponse = FlextTypes.Core.JsonObject

    # =========================================================================
    # CLI TYPES - Command-line interface (DOMAIN-SPECIFIC)
    # =========================================================================

    class CLI:
        """Command-line interface types using FlextTypes.Core foundation."""

        # Command structure using FlextTypes.Core
        type CommandName = str
        type CommandArgs = FlextTypes.Core.StringList
        type CommandResult = FlextTypes.Core.JsonObject

        # Execution context using FlextTypes.Core
        type ExecutionContext = FlextTypes.Core.Dict
        type ProcessResult = FlextTypes.Core.JsonObject
        type ExitCode = int

    # =========================================================================
    # ELT TYPES - Extract-Load-Transform pipelines (DOMAIN-SPECIFIC)
    # =========================================================================

    class ELT:
        """Extract-Load-Transform pipeline types using FlextTypes.Core foundation."""

        # Pipeline structure using FlextTypes.Core
        type Pipeline = FlextTypes.Core.ConfigDict
        type PipelineStage = str
        type PipelineConfig = FlextTypes.Core.ConfigDict

        # Execution and results using FlextTypes.Core
        type ExtractResult = FlextTypes.Core.JsonObject
        type LoadResult = FlextTypes.Core.JsonObject
        type TransformResult = FlextTypes.Core.JsonObject
        type PipelineResult = FlextTypes.Core.JsonObject

        # Monitoring and observability using FlextTypes.Core
        type ExecutionMetrics = FlextTypes.Core.JsonObject
        type PerformanceData = FlextTypes.Core.JsonObject
        type PipelineStatus = str

    # =========================================================================
    # ADAPTER TYPES - Service adapter patterns (DOMAIN-SPECIFIC)
    # =========================================================================

    class Adapter:
        """Service adapter pattern types using FlextTypes.Core foundation."""

        # Adapter identification using FlextTypes.Core
        type AdapterName = str
        type AdapterType = str
        type AdapterConfig = FlextTypes.Core.ConfigDict

        # Adapter operation types using FlextTypes.Core
        type OperationResult = FlextTypes.Core.JsonObject
        type AdapterResponse = FlextTypes.Core.JsonObject
        type ServiceCall = FlextTypes.Core.JsonValue

        # Integration patterns using FlextTypes.Core
        type WrapperResult = FlextTypes.Core.JsonObject
        type BridgeResult = FlextTypes.Core.JsonObject  # Bridge result as JsonObject


__all__ = [
    "FlextMeltanoTypes",
]
