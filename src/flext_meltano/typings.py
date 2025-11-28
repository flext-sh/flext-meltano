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
            str,
            str | list[str] | dict[str, object],
        ]
        type PluginConfiguration = dict[str, object | dict[str, object]]
        type PluginCatalog = dict[str, list[PluginDefinition]]
        type PluginRegistry = dict[str, PluginDefinition | PluginConfiguration]
        type PluginInstallation = dict[str, str | bool | list[str]]
        type PluginExecution = dict[str, FlextTypes.JsonValue | bool]
        type PluginInfo = dict[str, str | bool | int | dict[str, object]]

        # Plugin type literals
        PluginType = Literal["extractors", "loaders", "transforms", "orchestrators"]

    class Singer:
        """Singer protocol complex types namespace."""

        type CatalogEntry = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type StreamSchema = dict[str, dict[str, FlextTypes.JsonValue]]
        type TapConfig = dict[str, object | dict[str, object]]
        type TargetConfig = dict[str, object | dict[str, object]]
        type MessageBatch = list[dict[str, FlextTypes.JsonValue]]
        type StreamCatalog = dict[str, list[CatalogEntry]]

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

        type ModelConfiguration = dict[str, object | list[str]]
        type TestConfiguration = dict[str, str | list[str] | dict[str, object]]
        type ProfileConfiguration = dict[str, dict[str, object]]
        type ProjectConfiguration = dict[str, object | dict[str, object]]
        type RunResults = dict[str, list[dict[str, FlextTypes.JsonValue]]]
        type ManifestData = dict[str, dict[str, FlextTypes.JsonValue]]
        type Project = dict[str, str | bool | dict[str, object] | list[str]]

    class Project(FlextTypes):
        """Meltano-specific project types extending FlextTypes."""

        # Meltano-specific project types extending the generic ones
        type MeltanoProjectType = Literal[
            # Generic types inherited from FlextTypes
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
        type MeltanoProjectConfig = dict[str, object]
        type PipelineConfig = dict[str, str | int | bool | list[str]]
        type SingerConfig = dict[str, bool | str | dict[str, object]]
        type DbtConfig = dict[str, object]

    class Bridge:
        """Bridge operation complex types namespace."""

        type VersionInfo = dict[str, str | int]
        type ConnectionInfo = dict[str, str | int | bool]
        type BridgeConfig = dict[str, object]
        type BridgeStatus = dict[str, str | bool | dict[str, object]]

    class CLI:
        """CLI operation complex types namespace."""

        type ProcessResult = dict[str, str | int | float | bool | list[str]]
        type CommandResult = dict[str, str | int | bool]
        type ExecutionResult = dict[str, str | int | bool | dict[str, object]]
        type CLIStatus = dict[str, str | bool]

    class ELT:
        """ELT pipeline complex types namespace."""

        type PipelineResult = dict[
            str, str | int | float | bool | dict[str, object] | list[object]
        ]
        type ExtractionResult = dict[str, str | int | bool | dict[str, object]]
        type LoadingResult = dict[str, str | int | bool | dict[str, object]]
        type TransformationResult = dict[str, str | int | bool | dict[str, object]]

    class Processing(FlextTypes):
        """Meltano-specific processing types extending FlextTypes."""

        # Meltano-specific processing result types
        type DbtTransformationResult = dict[str, FlextTypes.JsonValue]
        type SingerProcessingResult = dict[str, FlextTypes.JsonValue]
        type SingerExecutionResult = dict[str, FlextTypes.JsonValue]
        type EltPipelineResult = dict[str, FlextTypes.JsonValue]

        # HTTP and network types
        type Headers = dict[str, str]  # HTTP headers mapping

    class MeltanoCore:
        """Commonly used Meltano-specific type aliases extending FlextTypes."""

        # =====================================================================
        # NESTED JSON TYPES - Support deeply nested dictionary structures
        # =====================================================================

        # Recursive JSON type supporting nested dictionaries
        type NestedJsonValue = (
            bool
            | float
            | int
            | str
            | list[object]
            | dict[str, object]
            | dict[
                str, bool | dict[str, object] | float | int | list[object] | str | None
            ]
            | None
        )
        type NestedJsonDict = dict[str, NestedJsonValue]

        # Meltano configuration and data types
        type MeltanoConfigDict = dict[str, FlextTypes.JsonValue]
        type PluginConfigDict = dict[str, object]
        type EnvironmentDict = dict[str, str]
        type VariablesDict = dict[str, str]
        type SettingsDict = dict[str, object]
        type CommandDict = dict[str, object]
        type ScheduleDict = dict[str, object]
        type JobDict = dict[str, object]

        # JsonValue type alias for compatibility
        JsonValue = FlextTypes.JsonValue

        # Type aliases for singer.py
        RecordDict = dict[str, object]
        SchemaDict = dict[str, object]
        StateDict = dict[str, object]
        ResultDict = dict[str, object]

        # Type aliases for protocols.py
        JsonObject = FlextTypes.JsonValue

        # Type aliases for file_managers.py
        FileConfigDict = dict[str, str | int | list[str]] | dict[str, str | list[str]]
        PathDict = dict[str, str | Path]

        # Plugin and execution types
        type PluginList = list[str]
        type PluginNameList = list[str]
        type PluginTypeList = list[str]
        type ExecutionResultDict = dict[str, object]
        type ExecutionStatusDict = dict[str, str]
        type RuntimeConfigDict = dict[str, object]

        # Singer protocol types
        type SingerRecordDict = dict[str, object]
        type SingerStateDict = dict[str, object]
        type SingerCatalogDict = dict[str, object]
        type SingerConfigDict = dict[str, object]
        type SingerSchemaDict = dict[str, object]
        type SingerMessageList = list[dict[str, object]]
        type StreamNameList = list[str]

        # DBT transformation types
        type DbtModelDict = dict[str, object]
        type DbtProfileDict = dict[str, object]
        type DbtProjectDict = dict[str, object]
        type DbtManifestDict = dict[str, object]
        type DbtResultDict = dict[str, object]
        type DbtModelList = list[str]
        type DbtTestList = list[str]

    class Pipeline:
        """Pipeline execution complex types namespace."""

        type PipelineConfig = dict[str, object]
        type PipelineStatus = dict[str, str | int | bool]
        type WorkflowDict = dict[str, object]
        type RunContextDict = dict[str, object]
        type ExecutionLogsDict = dict[str, object]
        type MetricsDict = dict[str, float]
        type ErrorsDict = dict[str, str]


__all__ = [
    "FlextMeltanoTypes",
]
