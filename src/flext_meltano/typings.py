"""FLEXT Meltano Types - Domain-specific Meltano type definitions.

This module provides Meltano-specific type definitions extending FlextTypes.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextTypes properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal

from flext_core import FlextTypes
from singer_sdk import typing as singer_sdk_typing

# =============================================================================
# MELTANO-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for Meltano operations
# =============================================================================


# Meltano domain TypeVars
class FlextMeltanoTypes(FlextTypes):
    """Meltano-specific type definitions extending FlextTypes.

    Domain-specific type system for Meltano data integration operations.
    Contains ONLY complex Meltano-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # MELTANO PLUGIN TYPES - Complex plugin management types
    # =========================================================================

    class Plugin:
        """Meltano plugin complex types."""

        type PluginDefinition = dict[
            str, str | FlextTypes.StringList | dict[str, FlextTypes.ConfigValue]
        ]
        type PluginConfiguration = dict[str, FlextTypes.ConfigValue | FlextTypes.Dict]
        type PluginCatalog = dict[str, list[PluginDefinition]]
        type PluginRegistry = dict[str, PluginDefinition | PluginConfiguration]
        type PluginInstallation = dict[str, str | bool | FlextTypes.StringList]
        type PluginExecution = dict[str, FlextTypes.JsonValue | bool]
        type PluginInfo = dict[str, str | bool | int | FlextTypes.Dict]

    # =========================================================================
    # SINGER PROTOCOL TYPES - Complex Singer operations
    # =========================================================================

    class Singer:
        """Singer protocol complex types."""

        type CatalogEntry = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type StreamSchema = dict[str, dict[str, FlextTypes.JsonValue]]
        type TapConfig = dict[str, FlextTypes.ConfigValue | FlextTypes.Dict]
        type TargetConfig = dict[str, FlextTypes.ConfigValue | FlextTypes.Dict]
        type MessageBatch = list[dict[str, FlextTypes.JsonValue]]
        type StreamCatalog = dict[str, list[CatalogEntry]]

        # Singer SDK typing utilities (domain separation from singer_sdk.typing)
        # ALL tap/target projects MUST use these instead of direct singer_sdk.typing imports
        class Typing:
            """Singer SDK typing utilities wrapper (ZERO TOLERANCE for direct imports).

            This class provides access to all Singer SDK typing utilities through FLEXT
            domain separation pattern. ALL tap/target projects MUST use this instead of
            importing directly from singer_sdk.typing.

            Usage:
                from flext_meltano import FlextMeltanoTypes

                schema = FlextMeltanoTypes.Singer.Typing.PropertiesList(
                    FlextMeltanoTypes.Singer.Typing.Property("id", FlextMeltanoTypes.Singer.Typing.StringType),
                    FlextMeltanoTypes.Singer.Typing.Property("count", FlextMeltanoTypes.Singer.Typing.IntegerType),
                ).to_dict()
            """

            ArrayType = singer_sdk_typing.ArrayType
            BooleanType = singer_sdk_typing.BooleanType
            CustomType = singer_sdk_typing.CustomType
            DateTimeType = singer_sdk_typing.DateTimeType
            DateType = singer_sdk_typing.DateType
            DurationType = singer_sdk_typing.DurationType
            IntegerType = singer_sdk_typing.IntegerType
            NumberType = singer_sdk_typing.NumberType
            ObjectType = singer_sdk_typing.ObjectType
            PropertiesList = singer_sdk_typing.PropertiesList
            Property = singer_sdk_typing.Property
            StringType = singer_sdk_typing.StringType
            TimeType = singer_sdk_typing.TimeType

    # =========================================================================
    # DBT TRANSFORMATION TYPES - Complex DBT operations
    # =========================================================================

    class Dbt:
        """DBT transformation complex types."""

        type ModelConfiguration = dict[
            str, FlextTypes.ConfigValue | FlextTypes.StringList
        ]
        type TestConfiguration = dict[
            str, str | FlextTypes.StringList | FlextTypes.Dict
        ]
        type ProfileConfiguration = dict[str, FlextTypes.ConfigDict]
        type ProjectConfiguration = dict[str, FlextTypes.ConfigValue | FlextTypes.Dict]
        type RunResults = dict[str, list[dict[str, FlextTypes.JsonValue]]]
        type ManifestData = dict[str, dict[str, FlextTypes.JsonValue]]
        type Project = dict[str, str | bool | FlextTypes.Dict | FlextTypes.StringList]

    # =========================================================================
    # MELTANO PROJECT TYPES - Complex project management
    # =========================================================================

    class Project(FlextTypes.Project):
        """Meltano-specific project types extending FlextTypes.Project.

        Adds Meltano/ELT-specific project types while inheriting generic types
        from FlextTypes. Follows domain separation principle: Meltano domain owns
        Meltano-specific types.
        """

        # Meltano-specific project types extending the generic ones
        type MeltanoProjectType = Literal[
            # Generic types inherited from FlextTypes.Project
            "library",
            "application",
            "service",
            # Meltano-specific types
            "meltano-project",
            "elt-pipeline",
            "data-pipeline",
            "etl-service",
            "singer-tap",
            "singer-target",
            "dbt-project",
            "data-integration",
            "pipeline-orchestrator",
            "data-extractor",
            "data-loader",
            "transformation-service",
        ]

        # Meltano-specific project configurations
        type MeltanoProjectConfig = dict[str, FlextTypes.ConfigValue | object]
        type PipelineConfig = dict[str, str | int | bool | FlextTypes.StringList]
        type SingerConfig = dict[str, bool | str | FlextTypes.Dict]
        type DbtConfig = dict[str, FlextTypes.ConfigValue | object]

    # =========================================================================
    # ELT PIPELINE TYPES - Complex pipeline operations
    # =========================================================================

    class Pipeline:
        """ELT pipeline complex types."""

        type PipelineDefinition = list[dict[str, str | dict[str, FlextTypes.JsonValue]]]
        type ExecutionContext = dict[str, FlextTypes.JsonValue | FlextTypes.Dict]
        type RuntimeEnvironment = dict[str, str | dict[str, FlextTypes.ConfigValue]]
        type PipelineResults = dict[
            str, FlextTypes.Processing.ProcessingStatus | FlextTypes.Dict
        ]
        type WorkflowConfiguration = dict[
            str, FlextTypes.Processing.WorkflowStatus | FlextTypes.StringList
        ]

    # =========================================================================
    # BRIDGE TYPES - Complex bridge operations
    # =========================================================================

    class Bridge:
        """Bridge operation complex types."""

        type VersionInfo = dict[str, str | int]
        type ConnectionInfo = dict[str, str | int | bool]
        type BridgeConfig = dict[str, FlextTypes.ConfigValue | object]
        type BridgeStatus = dict[str, str | bool | FlextTypes.Dict]

    # =========================================================================
    # CLI TYPES - Complex CLI operations
    # =========================================================================

    class CLI:
        """CLI operation complex types."""

        type ProcessResult = dict[str, str | int | float | bool | FlextTypes.StringList]
        type CommandResult = dict[str, str | int | bool]
        type ExecutionResult = dict[str, str | int | bool | FlextTypes.Dict]
        type CLIStatus = dict[str, str | bool]

    # =========================================================================
    # ELT PIPELINE TYPES - Complex ELT operations
    # =========================================================================

    class ELT:
        """ELT pipeline complex types."""

        type PipelineResult = dict[
            str, str | int | float | bool | FlextTypes.Dict | FlextTypes.List
        ]
        type ExtractionResult = dict[str, str | int | bool | FlextTypes.Dict]
        type LoadingResult = dict[str, str | int | bool | FlextTypes.Dict]
        type TransformationResult = dict[str, str | int | bool | FlextTypes.Dict]

    # =========================================================================
    # PROCESSING TYPES - Data processing results extending FlextTypes.Processing
    # =========================================================================

    class Processing(FlextTypes.Processing):
        """Meltano-specific processing types extending FlextTypes.Processing.

        Inherits all generic processing types and adds Meltano-specific result types.
        Provides structured result types for DBT, Singer, and ELT operations.
        """

        # Direct access to inherited processing types
        type ProcessingStatus = FlextTypes.Processing.ProcessingStatus
        type ProcessingMode = FlextTypes.Processing.ProcessingMode

        # Meltano-specific processing result types
        type DbtTransformationResult = dict[str, FlextTypes.JsonValue]
        type SingerProcessingResult = dict[str, FlextTypes.JsonValue]
        type SingerExecutionResult = dict[str, FlextTypes.JsonValue]
        type EltPipelineResult = dict[str, FlextTypes.JsonValue]

        # HTTP and network types
        type Headers = dict[str, str]  # HTTP headers mapping

    # =========================================================================
    # CORE COMMONLY USED TYPES - Extending FlextTypes for Meltano domain
    # =========================================================================

    class Core(FlextTypes):
        """Commonly used Meltano-specific type aliases extending FlextTypes.

        Provides standardized type aliases for frequent Meltano patterns while
        inheriting all core types from FlextTypes. Reduces generic dict/list
        usage throughout the Meltano codebase.
        """

        # Core aliases for compatibility with FlextTypes
        type Dict = FlextTypes.Dict
        type List = FlextTypes.List
        type StringList = FlextTypes.StringList
        type ConfigValue = (
            str | int | bool | float | FlextTypes.List | FlextTypes.Dict | None
        )
        type JsonValue = (
            str | int | bool | float | FlextTypes.List | FlextTypes.Dict | None
        )

        # Meltano configuration and data types
        type MeltanoConfigDict = FlextTypes.Dict
        type PluginConfigDict = FlextTypes.Dict
        type EnvironmentDict = FlextTypes.StringDict
        type VariablesDict = FlextTypes.StringDict
        type SettingsDict = FlextTypes.Dict
        type CommandDict = FlextTypes.Dict
        type ScheduleDict = FlextTypes.Dict
        type JobDict = FlextTypes.Dict

        # Plugin and execution types
        type PluginList = FlextTypes.StringList
        type PluginNameList = FlextTypes.StringList
        type PluginTypeList = FlextTypes.StringList
        type ExecutionResultDict = FlextTypes.Dict
        type ExecutionStatusDict = FlextTypes.StringDict
        type RuntimeConfigDict = FlextTypes.Dict

        # Singer protocol types
        type SingerRecordDict = FlextTypes.Dict
        type SingerStateDict = FlextTypes.Dict
        type SingerCatalogDict = FlextTypes.Dict
        type SingerConfigDict = FlextTypes.Dict
        type SingerSchemaDict = FlextTypes.Dict
        type SingerMessageList = list[FlextTypes.Dict]
        type StreamNameList = FlextTypes.StringList

        # DBT transformation types
        type DbtModelDict = FlextTypes.Dict
        type DbtProfileDict = FlextTypes.Dict
        type DbtProjectDict = FlextTypes.Dict
        type DbtManifestDict = FlextTypes.Dict
        type DbtResultDict = FlextTypes.Dict
        type DbtModelList = FlextTypes.StringList
        type DbtTestList = FlextTypes.StringList

        # Pipeline and workflow types
        type PipelineConfigDict = FlextTypes.Dict
        type WorkflowDict = FlextTypes.Dict
        type RunContextDict = FlextTypes.Dict
        type ExecutionLogsDict = FlextTypes.Dict
        type MetricsDict = FlextTypes.FloatDict
        type ErrorsDict = FlextTypes.StringDict

        # Library and runner types
        type LibraryDict = FlextTypes.Dict
        type RunnerConfigDict = FlextTypes.Dict
        type ProcessResultDict = FlextTypes.Dict
        type OutputDict = FlextTypes.Dict
        type LogsDict = FlextTypes.Dict
        type MetadataDict = dict[str, str | int | bool | FlextTypes.Dict]
        type ResponseDict = dict[str, str | int | bool | FlextTypes.Dict]


# =============================================================================
# PUBLIC API EXPORTS - Meltano TypeVars and types
# =============================================================================

__all__: FlextTypes.StringList = [
    "FlextMeltanoTypes",
]
