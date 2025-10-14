"""FLEXT Meltano Types - Domain-specific Meltano type definitions.

This module provides Meltano-specific type definitions extending FlextCore.Types.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextCore.Types properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from flext_core import FlextCore
from singer_sdk import typing as singer_sdk_typing


class FlextMeltanoTypes(FlextCore.Types):
    """Meltano-specific type definitions extending FlextCore.Types.

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
            str,
            str | FlextCore.Types.StringList | dict[str, FlextCore.Types.ConfigValue],
        ]
        type PluginConfiguration = dict[
            str, FlextCore.Types.ConfigValue | FlextCore.Types.Dict
        ]
        type PluginCatalog = dict[str, list[PluginDefinition]]
        type PluginRegistry = dict[str, PluginDefinition | PluginConfiguration]
        type PluginInstallation = dict[str, str | bool | FlextCore.Types.StringList]
        type PluginExecution = dict[str, FlextCore.Types.JsonValue | bool]
        type PluginInfo = dict[str, str | bool | int | FlextCore.Types.Dict]

    class Singer:
        """Singer protocol complex types namespace."""

        type CatalogEntry = dict[str, str | dict[str, FlextCore.Types.JsonValue]]
        type StreamSchema = dict[str, dict[str, FlextCore.Types.JsonValue]]
        type TapConfig = dict[str, FlextCore.Types.ConfigValue | FlextCore.Types.Dict]
        type TargetConfig = dict[
            str, FlextCore.Types.ConfigValue | FlextCore.Types.Dict
        ]
        type MessageBatch = list[dict[str, FlextCore.Types.JsonValue]]
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
            str, FlextCore.Types.ConfigValue | FlextCore.Types.StringList
        ]
        type TestConfiguration = dict[
            str, str | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]
        type ProfileConfiguration = dict[str, FlextCore.Types.ConfigDict]
        type ProjectConfiguration = dict[
            str, FlextCore.Types.ConfigValue | FlextCore.Types.Dict
        ]
        type RunResults = dict[str, list[dict[str, FlextCore.Types.JsonValue]]]
        type ManifestData = dict[str, dict[str, FlextCore.Types.JsonValue]]
        type Project = dict[
            str, str | bool | FlextCore.Types.Dict | FlextCore.Types.StringList
        ]

    class Project(FlextCore.Types.Project):
        """Meltano-specific project types extending FlextCore.Types.Project."""

        # Meltano-specific project types extending the generic ones
        type MeltanoProjectType = Literal[
            # Generic types inherited from FlextCore.Types.Project
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
        type MeltanoProjectConfig = dict[str, FlextCore.Types.ConfigValue | object]
        type PipelineConfig = dict[str, str | int | bool | FlextCore.Types.StringList]
        type SingerConfig = dict[str, bool | str | FlextCore.Types.Dict]
        type DbtConfig = dict[str, FlextCore.Types.ConfigValue | object]

    class Pipeline:
        """ELT pipeline complex types namespace."""

        type PipelineDefinition = list[
            dict[str, str | dict[str, FlextCore.Types.JsonValue]]
        ]
        type ExecutionContext = dict[
            str, FlextCore.Types.JsonValue | FlextCore.Types.Dict
        ]
        type RuntimeEnvironment = dict[
            str, str | dict[str, FlextCore.Types.ConfigValue]
        ]
        type PipelineResults = dict[
            str, FlextCore.Types.Processing.ProcessingStatus | FlextCore.Types.Dict
        ]
        type WorkflowConfiguration = dict[
            str, FlextCore.Types.Processing.WorkflowStatus | FlextCore.Types.StringList
        ]

    class Bridge:
        """Bridge operation complex types namespace."""

        type VersionInfo = dict[str, str | int]
        type ConnectionInfo = dict[str, str | int | bool]
        type BridgeConfig = dict[str, FlextCore.Types.ConfigValue | object]
        type BridgeStatus = dict[str, str | bool | FlextCore.Types.Dict]

    class CLI:
        """CLI operation complex types namespace."""

        type ProcessResult = dict[
            str, str | int | float | bool | FlextCore.Types.StringList
        ]
        type CommandResult = dict[str, str | int | bool]
        type ExecutionResult = dict[str, str | int | bool | FlextCore.Types.Dict]
        type CLIStatus = dict[str, str | bool]

    class ELT:
        """ELT pipeline complex types namespace."""

        type PipelineResult = dict[
            str, str | int | float | bool | FlextCore.Types.Dict | FlextCore.Types.List
        ]
        type ExtractionResult = dict[str, str | int | bool | FlextCore.Types.Dict]
        type LoadingResult = dict[str, str | int | bool | FlextCore.Types.Dict]
        type TransformationResult = dict[str, str | int | bool | FlextCore.Types.Dict]

    class Processing(FlextCore.Types.Processing):
        """Meltano-specific processing types extending FlextCore.Types.Processing."""

        # Meltano-specific processing result types
        type DbtTransformationResult = dict[str, FlextCore.Types.JsonValue]
        type SingerProcessingResult = dict[str, FlextCore.Types.JsonValue]
        type SingerExecutionResult = dict[str, FlextCore.Types.JsonValue]
        type EltPipelineResult = dict[str, FlextCore.Types.JsonValue]

        # HTTP and network types
        type Headers = dict[str, str]  # HTTP headers mapping

    class MeltanoCore:
        """Commonly used Meltano-specific type aliases extending FlextCore.Types."""

        # Meltano configuration and data types
        type MeltanoConfigDict = dict[str, FlextCore.Types.JsonValue]
        type PluginConfigDict = FlextCore.Types.Dict
        type EnvironmentDict = FlextCore.Types.StringDict
        type VariablesDict = FlextCore.Types.StringDict
        type SettingsDict = FlextCore.Types.Dict
        type CommandDict = FlextCore.Types.Dict
        type ScheduleDict = FlextCore.Types.Dict
        type JobDict = FlextCore.Types.Dict

        # JsonValue type alias for compatibility
        JsonValue = FlextCore.Types.JsonValue

        # Type aliases for singer.py
        RecordDict = FlextCore.Types.Dict
        SchemaDict = FlextCore.Types.Dict
        StateDict = FlextCore.Types.Dict
        ResultDict = FlextCore.Types.Dict

        # Type aliases for protocols.py
        JsonObject = FlextCore.Types.JsonValue

        # Type aliases for file_managers.py
        FileConfigDict = (
            dict[str, str | int | FlextCore.Types.StringList]
            | dict[str, str | FlextCore.Types.StringList]
        )
        PathDict = dict[str, str | Path]

        # Plugin and execution types
        type PluginList = FlextCore.Types.StringList
        type PluginNameList = FlextCore.Types.StringList
        type PluginTypeList = FlextCore.Types.StringList
        type ExecutionResultDict = FlextCore.Types.Dict
        type ExecutionStatusDict = FlextCore.Types.StringDict
        type RuntimeConfigDict = FlextCore.Types.Dict

        # Singer protocol types
        type SingerRecordDict = FlextCore.Types.Dict
        type SingerStateDict = FlextCore.Types.Dict
        type SingerCatalogDict = FlextCore.Types.Dict
        type SingerConfigDict = FlextCore.Types.Dict
        type SingerSchemaDict = FlextCore.Types.Dict
        type SingerMessageList = list[FlextCore.Types.Dict]
        type StreamNameList = FlextCore.Types.StringList

        # DBT transformation types
        type DbtModelDict = FlextCore.Types.Dict
        type DbtProfileDict = FlextCore.Types.Dict
        type DbtProjectDict = FlextCore.Types.Dict
        type DbtManifestDict = FlextCore.Types.Dict
        type DbtResultDict = FlextCore.Types.Dict
        type DbtModelList = FlextCore.Types.StringList
        type DbtTestList = FlextCore.Types.StringList

        # Pipeline and workflow types
        type PipelineConfigDict = FlextCore.Types.Dict
        type WorkflowDict = FlextCore.Types.Dict
        type RunContextDict = FlextCore.Types.Dict
        type ExecutionLogsDict = FlextCore.Types.Dict
        type MetricsDict = FlextCore.Types.FloatDict
        type ErrorsDict = FlextCore.Types.StringDict

        # Library and runner types
        type LibraryDict = FlextCore.Types.Dict
        type RunnerConfigDict = FlextCore.Types.Dict
        type ProcessResultDict = FlextCore.Types.Dict
        type OutputDict = FlextCore.Types.Dict
        type LogsDict = FlextCore.Types.Dict
        type MetadataDict = dict[str, str | int | bool | FlextCore.Types.Dict]
        type ResponseDict = dict[str, str | int | bool | FlextCore.Types.Dict]


__all__ = [
    "FlextMeltanoTypes",
]
