"""FLEXT Meltano Types - Domain-specific Meltano type definitions.

This module provides Meltano-specific type definitions extending t.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends t properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from flext_core import FlextTypes
from singer_sdk import typing as singer_sdk_typing


class FlextMeltanoTypes(FlextTypes):
    """Meltano-specific type definitions extending t.

    Domain-specific type system for Meltano data integration operations.
    Contains ONLY complex Meltano-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # MELTANO DOMAIN NAMESPACES - Following FLEXT pattern
    # =========================================================================

    class Meltano:
        """Meltano plugin complex types namespace."""

        type PluginDefinition = dict[
            str,
            str | list[str] | dict[str, FlextTypes.JsonValue],
        ]
        type PluginConfiguration = dict[str, FlextTypes.JsonValue]
        type PluginCatalog = dict[str, list[PluginDefinition]]
        type PluginRegistry = dict[str, "PluginDefinition" | "PluginConfiguration"]
        type PluginInstallation = dict[str, str | bool | list[str]]
        type PluginExecution = dict[str, FlextTypes.JsonValue]
        type PluginInfo = dict[str, str | bool | int | FlextTypes.JsonValue]

        # Plugin type literals
        PluginType = Literal["extractors", "loaders", "transforms", "orchestrators"]
        PluginVariant = Literal["default", "singer", "custom"]

    # Namespace bridge so t.Plugin.PluginDefinition resolves in type checkers.
    class Plugin(Meltano):
        """Compatibility namespace for plugin-related aliases."""

    class Singer:
        """Singer protocol complex types namespace."""

        type CatalogEntry = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type StreamSchema = dict[str, dict[str, FlextTypes.JsonValue]]
        type TapConfig = dict[str, FlextTypes.GeneralValueType]
        type TargetConfig = dict[str, FlextTypes.GeneralValueType]
        type MessageBatch = list[dict[str, FlextTypes.JsonValue]]
        type StreamCatalog = dict[str, list[CatalogEntry]]
        type Record = dict[str, FlextTypes.JsonValue]
        type Schema = dict[str, FlextTypes.JsonValue]
        type State = dict[str, FlextTypes.JsonValue]

        # Singer protocol Literal types
        ReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL", "LOG_BASED"]
        SingerVersion = Literal["0.44.0", "0.45.0", "0.46.0", "0.47.0", "0.48.0"]

        # Singer SDK typing utilities (domain separation from singer_sdk.typing)
        class Typing:
            """Singer SDK typing utilities wrapper (Zero Tolerance for direct imports).

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

        type ModelConfiguration = dict[str, FlextTypes.JsonValue]
        type TestConfiguration = dict[str, str | list[str] | FlextTypes.JsonValue]
        type ProfileConfiguration = dict[str, dict[str, FlextTypes.JsonValue]]
        type ProjectConfiguration = dict[str, FlextTypes.JsonValue]
        type RunResults = dict[str, list[dict[str, FlextTypes.JsonValue]]]
        type ManifestData = dict[str, dict[str, FlextTypes.JsonValue]]
        type Project = dict[str, str | bool | FlextTypes.JsonValue | list[str]]

    class Project:
        """Meltano-specific project types."""

        type ProjectConfig = dict[str, FlextTypes.JsonValue]
        type ProjectMetadata = dict[str, str | int | bool | FlextTypes.JsonValue]

        # Meltano-specific project types extending the generic ones
        type MeltanoProjectType = Literal[
            # Generic types inherited from t
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
        type MeltanoProjectConfig = dict[str, FlextTypes.JsonValue]
        type PipelineConfig = dict[str, str | int | bool | list[str]]
        type SingerConfig = dict[str, bool | str | FlextTypes.JsonValue]
        type DbtConfig = dict[str, FlextTypes.JsonValue]

    class Bridge:
        """Bridge operation complex types namespace."""

        type BridgeMessage = dict[str, FlextTypes.JsonValue]
        type BridgeResponse = dict[str, FlextTypes.JsonValue]
        type VersionInfo = dict[str, str | int]
        type ConnectionInfo = dict[str, str | int | bool]
        type BridgeConfig = dict[str, FlextTypes.JsonValue]
        type BridgeStatus = dict[str, str | bool | FlextTypes.JsonValue]

    class CLI:
        """CLI operation complex types namespace."""

        type Command = list[str]
        type ProcessResult = dict[str, str | int | float | bool | list[str]]
        type CommandResult = dict[str, str | int | bool]
        type ExecutionResult = dict[str, str | int | bool | FlextTypes.JsonValue]
        type CLIStatus = dict[str, str | bool]

    class ELT:
        """ELT pipeline complex types namespace."""

        type PipelineResult = dict[
            str,
            str
            | int
            | float
            | bool
            | FlextTypes.JsonValue
            | list[FlextTypes.JsonValue],
        ]
        type ExtractConfig = dict[str, FlextTypes.JsonValue]
        type LoadConfig = dict[str, FlextTypes.JsonValue]
        type TransformConfig = dict[str, FlextTypes.JsonValue]
        type ExtractionResult = dict[str, str | int | bool | FlextTypes.JsonValue]
        type LoadingResult = dict[str, str | int | bool | FlextTypes.JsonValue]
        type TransformationResult = dict[str, str | int | bool | FlextTypes.JsonValue]

    class Processing:
        """Meltano-specific processing types."""

        # Meltano-specific processing result types
        type DbtTransformationResult = dict[str, FlextTypes.JsonValue]
        type SingerProcessingResult = dict[str, FlextTypes.JsonValue]
        type SingerExecutionResult = dict[str, FlextTypes.JsonValue]
        type EltPipelineResult = dict[str, FlextTypes.JsonValue]

        # HTTP and network types
        type Headers = dict[str, str]  # HTTP headers mapping

    class MeltanoCore:
        """Commonly used Meltano-specific type aliases extending t."""

        # =====================================================================
        # NESTED JSON TYPES - Support deeply nested dictionary structures
        # =====================================================================

        # Recursive JSON type supporting nested dictionaries
        type NestedJsonValue = (
            bool
            | float
            | int
            | str
            | list[FlextTypes.JsonValue]
            | dict[str, FlextTypes.JsonValue]
            | None
        )
        type NestedJsonDict = dict[str, NestedJsonValue]

        # Meltano configuration and data types
        type MeltanoConfigDict = dict[str, FlextTypes.GeneralValueType]
        type PluginConfigDict = dict[str, FlextTypes.GeneralValueType]
        type EnvironmentDict = dict[str, str]
        type VariablesDict = dict[str, str]
        type SettingsDict = dict[str, FlextTypes.GeneralValueType]
        type MetadataDict = dict[str, FlextTypes.GeneralValueType]
        type CommandDict = dict[str, FlextTypes.GeneralValueType]
        type ScheduleDict = dict[str, FlextTypes.GeneralValueType]
        type JobDict = dict[str, FlextTypes.GeneralValueType]

        # Type aliases for singer.py
        RecordDict = dict[str, FlextTypes.JsonValue]
        SchemaDict = dict[str, FlextTypes.JsonValue]
        StateDict = dict[str, FlextTypes.JsonValue]
        ResultDict = dict[str, FlextTypes.JsonValue]

        # Type aliases for protocols.py
        type JsonObject = FlextTypes.JsonValue

        # JSON value type (re-export from FlextTypes for convenience)
        type JsonValue = FlextTypes.GeneralValueType

        # Run context for pipeline execution
        type RunContextDict = dict[str, FlextTypes.GeneralValueType]

        # Type aliases for file_managers.py
        FileConfigDict = dict[
            str,
            FlextTypes.GeneralValueType,
        ]
        PathDict = dict[str, str | Path]

        # Plugin and execution types
        type PluginList = list[str]
        type PluginNameList = list[str]
        type PluginTypeList = list[str]
        type ExecutionResultDict = dict[str, FlextTypes.GeneralValueType]
        type ExecutionStatusDict = dict[str, str]
        type RuntimeConfigDict = dict[str, FlextTypes.GeneralValueType]

        # Singer protocol types
        type SingerRecordDict = dict[str, FlextTypes.JsonValue]
        type SingerStateDict = dict[str, FlextTypes.JsonValue]
        type SingerCatalogDict = dict[str, FlextTypes.JsonValue]
        type SingerConfigDict = dict[str, FlextTypes.JsonValue]
        type SingerSchemaDict = dict[str, FlextTypes.JsonValue]
        type SingerMessageList = list[dict[str, FlextTypes.JsonValue]]
        type StreamNameList = list[str]

        # DBT transformation types
        type DbtModelDict = dict[str, FlextTypes.JsonValue]
        type DbtProfileDict = dict[str, FlextTypes.JsonValue]
        type DbtProjectDict = dict[str, FlextTypes.JsonValue]
        type DbtManifestDict = dict[str, FlextTypes.JsonValue]
        type DbtResultDict = dict[str, FlextTypes.JsonValue]
        type DbtModelList = list[str]
        type DbtTestList = list[str]

    class Pipeline:
        """Pipeline execution complex types namespace."""

        type PipelineConfig = dict[str, FlextTypes.JsonValue]
        type PipelineStatus = dict[str, str | int | bool]
        type WorkflowDict = dict[str, FlextTypes.JsonValue]
        type RunContextDict = dict[str, FlextTypes.JsonValue]
        type ExecutionLogsDict = dict[str, FlextTypes.JsonValue]
        type MetricsDict = dict[str, float]
        type ErrorsDict = dict[str, str]


t = FlextMeltanoTypes

__all__ = [
    "FlextMeltanoTypes",
    "t",
]
