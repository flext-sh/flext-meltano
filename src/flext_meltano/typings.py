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

from pathlib import Path
from typing import Literal

from flext_core import FlextTypes
from pydantic import ConfigDict as PydanticConfigDict
from singer_sdk import typing as singer_sdk_typing


class FlextMeltanoTypes(FlextTypes):
    """Meltano-specific type definitions extending FlextTypes.

    Domain-specific type system for Meltano data integration operations.
    Contains ONLY complex Meltano-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # MELTANO DOMAIN NAMESPACES - Following FLEXT pattern
    # =========================================================================

    class Plugin:
        """Meltano plugin complex types namespace."""

        type PluginDefinition = dict[
            str, str | FlextTypes.StringList | dict[str, FlextTypes.ConfigValue]
        ]
        type PluginConfiguration = dict[str, FlextTypes.ConfigValue | FlextTypes.Dict]
        type PluginCatalog = dict[str, list[PluginDefinition]]
        type PluginRegistry = dict[str, PluginDefinition | PluginConfiguration]
        type PluginInstallation = dict[str, str | bool | FlextTypes.StringList]
        type PluginExecution = dict[str, FlextTypes.JsonValue | bool]
        type PluginInfo = dict[str, str | bool | int | FlextTypes.Dict]

    class Singer:
        """Singer protocol complex types namespace."""

        type CatalogEntry = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type StreamSchema = dict[str, dict[str, FlextTypes.JsonValue]]
        type TapConfig = dict[str, FlextTypes.ConfigValue | FlextTypes.Dict]
        type TargetConfig = dict[str, FlextTypes.ConfigValue | FlextTypes.Dict]
        type MessageBatch = list[dict[str, FlextTypes.JsonValue]]
        type StreamCatalog = dict[str, list[CatalogEntry]]

        # Singer SDK typing utilities (domain separation from singer_sdk.typing)
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

    class Dbt:
        """DBT transformation complex types namespace."""

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

    class Project(FlextTypes.Project):
        """Meltano-specific project types extending FlextTypes.Project."""

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

    class Pipeline:
        """ELT pipeline complex types namespace."""

        type PipelineDefinition = list[dict[str, str | dict[str, FlextTypes.JsonValue]]]
        type ExecutionContext = dict[str, FlextTypes.JsonValue | FlextTypes.Dict]
        type RuntimeEnvironment = dict[str, str | dict[str, FlextTypes.ConfigValue]]
        type PipelineResults = dict[
            str, FlextTypes.Processing.ProcessingStatus | FlextTypes.Dict
        ]
        type WorkflowConfiguration = dict[
            str, FlextTypes.Processing.WorkflowStatus | FlextTypes.StringList
        ]

    class Bridge:
        """Bridge operation complex types namespace."""

        type VersionInfo = dict[str, str | int]
        type ConnectionInfo = dict[str, str | int | bool]
        type BridgeConfig = dict[str, FlextTypes.ConfigValue | object]
        type BridgeStatus = dict[str, str | bool | FlextTypes.Dict]

    class CLI:
        """CLI operation complex types namespace."""

        type ProcessResult = dict[str, str | int | float | bool | FlextTypes.StringList]
        type CommandResult = dict[str, str | int | bool]
        type ExecutionResult = dict[str, str | int | bool | FlextTypes.Dict]
        type CLIStatus = dict[str, str | bool]

    class ELT:
        """ELT pipeline complex types namespace."""

        type PipelineResult = dict[
            str, str | int | float | bool | FlextTypes.Dict | FlextTypes.List
        ]
        type ExtractionResult = dict[str, str | int | bool | FlextTypes.Dict]
        type LoadingResult = dict[str, str | int | bool | FlextTypes.Dict]
        type TransformationResult = dict[str, str | int | bool | FlextTypes.Dict]

    class Processing(FlextTypes.Processing):
        """Meltano-specific processing types extending FlextTypes.Processing."""

        # Meltano-specific processing result types
        type DbtTransformationResult = dict[str, FlextTypes.JsonValue]
        type SingerProcessingResult = dict[str, FlextTypes.JsonValue]
        type SingerExecutionResult = dict[str, FlextTypes.JsonValue]
        type EltPipelineResult = dict[str, FlextTypes.JsonValue]

        # HTTP and network types
        type Headers = dict[str, str]  # HTTP headers mapping

    class MeltanoCore:
        """Commonly used Meltano-specific type aliases extending FlextTypes."""

        # Meltano configuration and data types
        type MeltanoConfigDict = dict[str, FlextTypes.JsonValue]
        type PluginConfigDict = FlextTypes.Dict
        type EnvironmentDict = FlextTypes.StringDict
        type VariablesDict = FlextTypes.StringDict
        type SettingsDict = FlextTypes.Dict
        type CommandDict = FlextTypes.Dict
        type ScheduleDict = FlextTypes.Dict
        type JobDict = FlextTypes.Dict

        # JsonValue type alias for compatibility
        JsonValue = FlextTypes.JsonValue

        # Type aliases for singer.py
        RecordDict = FlextTypes.Dict
        SchemaDict = FlextTypes.Dict
        StateDict = FlextTypes.Dict
        ResultDict = FlextTypes.Dict

        # Type aliases for protocols.py
        JsonObject = FlextTypes.JsonValue

        # Type aliases for file_managers.py
        FileConfigDict = (
            dict[str, str | int | FlextTypes.StringList]
            | dict[str, str | FlextTypes.StringList]
        )
        PathDict = dict[str, str | Path]

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


# Export ConfigDict for backward compatibility
ConfigDict = PydanticConfigDict

__all__ = [
    "ConfigDict",
    "FlextMeltanoTypes",
]
