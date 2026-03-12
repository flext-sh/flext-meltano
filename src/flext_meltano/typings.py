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

from collections.abc import Mapping
from pathlib import Path
from typing import Literal

import singer_sdk.typing as singer_sdk_typing
from flext_cli import FlextCliTypes


class FlextMeltanoTypes(FlextCliTypes):
    """Meltano-specific type definitions extending t.

    Domain-specific type system for Meltano data integration operations.
    Contains ONLY complex Meltano-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    class Meltano:
        """Meltano plugin complex types namespace."""

        type PluginDefinition = dict[str, str | list[str] | Mapping[str, object]]
        type PluginConfiguration = dict[str, object]
        type PluginCatalog = dict[str, list[PluginDefinition]]
        type PluginRegistry = dict[str, "PluginDefinition" | "PluginConfiguration"]
        type PluginInstallation = dict[str, str | bool | list[str]]
        type PluginExecution = dict[str, object]
        type PluginInfo = dict[str, str | bool | int | object]
        PluginType = Literal["extractors", "loaders", "transforms", "orchestrators"]
        PluginVariant = Literal["default", "singer", "custom"]

        class _PluginMeta(type):
            """Metaclass that proxies attribute access to the Meltano class."""

            def __getattr__(cls, name: str) -> object:
                meltano_cls = FlextMeltanoTypes.Meltano
                try:
                    return getattr(meltano_cls, name)
                except AttributeError:
                    msg = f"type object 'Plugin' has no attribute {name!r}"
                    raise AttributeError(msg) from None

        class Plugin(metaclass=_PluginMeta):
            """Plugin namespace bridging t.Meltano.* to t.Meltano.* types."""

        class Singer:
            """Singer protocol complex types namespace."""

            type CatalogEntry = dict[str, str | Mapping[str, object]]
            type StreamSchema = dict[str, dict[str, object]]
            type TapConfig = dict[str, object]
            type TargetConfig = dict[str, object]
            type MessageBatch = list[dict[str, object]]
            type StreamCatalog = dict[str, list[CatalogEntry]]
            type Record = dict[str, object]
            type Schema = dict[str, object]
            type State = dict[str, object]
            ReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL", "LOG_BASED"]
            SingerVersion = Literal["0.44.0", "0.45.0", "0.46.0", "0.47.0", "0.48.0"]

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

            type ModelConfiguration = dict[str, object]
            type TestConfiguration = dict[str, str | list[str] | object]
            type ProfileConfiguration = dict[str, dict[str, object]]
            type ProjectConfiguration = dict[str, object]
            type RunResults = dict[str, list[dict[str, object]]]
            type ManifestData = dict[str, dict[str, object]]
            type Project = dict[str, str | bool | object | list[str]]

        class Project:
            """Meltano-specific project types."""

            type ProjectConfig = dict[str, object]
            type ProjectMetadata = dict[str, str | int | bool | object]
            type MeltanoProjectType = Literal[
                "library",
                "application",
                "service",
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
            type MeltanoProjectConfig = dict[str, object]
            type PipelineConfig = dict[str, str | int | bool | list[str]]
            type SingerConfig = dict[str, bool | str | object]
            type DbtConfig = dict[str, object]

        class Bridge:
            """Bridge operation complex types namespace."""

            type BridgeMessage = dict[str, object]
            type BridgeResponse = dict[str, object]
            type VersionInfo = dict[str, str | int]
            type ConnectionInfo = dict[str, str | int | bool]
            type BridgeConfig = dict[str, object]
            type BridgeStatus = dict[str, str | bool | object]

        class CLI:
            """CLI operation complex types namespace."""

            type Command = list[str]
            type ProcessResult = dict[str, t.Scalar | list[str]]
            type CommandResult = dict[str, str | int | bool]
            type ExecutionResult = dict[str, str | int | bool | object]
            type CLIStatus = dict[str, str | bool]

        class ELT:
            """ELT pipeline complex types namespace."""

            type PipelineResult = dict[str, t.Scalar | object | list[object]]
            type ExtractConfig = dict[str, object]
            type LoadConfig = dict[str, object]
            type TransformConfig = dict[str, object]
            type ExtractionResult = dict[str, str | int | bool | object]
            type LoadingResult = dict[str, str | int | bool | object]
            type TransformationResult = dict[str, str | int | bool | object]

        class Processing:
            """Meltano-specific processing types."""

            type DbtTransformationResult = dict[str, object]
            type SingerProcessingResult = dict[str, object]
            type SingerExecutionResult = dict[str, object]
            type EltPipelineResult = dict[str, object]
            type Headers = dict[str, str]

        type NestedJsonValue = (
            bool | float | int | str | list[object] | Mapping[str, object] | None
        )
        type NestedJsonDict = dict[str, NestedJsonValue]
        type MeltanoConfigDict = dict[str, object]
        type PluginConfigDict = dict[str, object]
        type EnvironmentDict = dict[str, str]
        type VariablesDict = dict[str, str]
        type SettingsDict = dict[str, object]
        type MetadataDict = dict[str, object]
        type CommandDict = dict[str, object]
        type ScheduleDict = dict[str, object]
        type JobDict = dict[str, object]
        RecordDict = Mapping[str, object]
        SchemaDict = Mapping[str, object]
        StateDict = Mapping[str, object]
        ResultDict = Mapping[str, object]
        type RunContextDict = dict[str, object]
        FileConfigDict = Mapping[str, object]
        PathDict = Mapping[str, str | Path]
        type PluginList = list[str]
        type PluginNameList = list[str]
        type PluginTypeList = list[str]
        type ExecutionResultDict = dict[str, object]
        type ExecutionStatusDict = dict[str, str]
        type RuntimeConfigDict = dict[str, object]
        type SingerRecordDict = dict[str, object]
        type SingerStateDict = dict[str, object]
        type SingerCatalogDict = dict[str, object]
        type SingerConfigDict = dict[str, object]
        type SingerSchemaDict = dict[str, object]
        type SingerMessageList = list[dict[str, object]]
        type StreamNameList = list[str]
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

    Singer = Meltano.Singer


t = FlextMeltanoTypes
__all__ = ["FlextMeltanoTypes", "t"]
