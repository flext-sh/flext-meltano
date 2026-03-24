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

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Literal

import singer_sdk.typing as singer_sdk_typing
from flext_cli import FlextCliTypes

from flext_meltano import c


class FlextMeltanoTypes(FlextCliTypes):
    """Meltano-specific type definitions extending t.

    Domain-specific type system for Meltano data integration operations.
    Contains ONLY complex Meltano-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    class Meltano:
        """Meltano plugin complex types namespace."""

        type MeltanoValue = Mapping[str, t.ContainerValue] | None

        type PluginDefinition = Mapping[
            str,
            str | Sequence[str] | Mapping[str, t.Scalar | None],
        ]
        type PluginConfiguration = t.ContainerMapping
        type PluginCatalog = Mapping[str, Sequence[t.Meltano.PluginDefinition]]
        type PluginRegistry = Mapping[
            str,
            t.Meltano.PluginDefinition | t.Meltano.PluginConfiguration,
        ]
        type PluginInstallation = Mapping[str, str | bool | Sequence[str]]
        type PluginExecution = Mapping[str, Mapping[str, t.ContainerValue] | None]
        type PluginInfo = Mapping[str, t.Scalar | None]
        PluginType = Literal["extractors", "loaders", "transforms", "orchestrators"]
        PluginVariant = Literal["default", "singer", "custom"]

        class Singer:
            """Singer protocol complex types namespace."""

            type CatalogEntry = Mapping[str, str | Mapping[str, t.Scalar | None]]
            type StreamSchema = Mapping[str, Mapping[str, t.Scalar | None]]
            type TapConfig = Mapping[str, Mapping[str, t.ContainerValue] | None]
            type TargetConfig = Mapping[str, Mapping[str, t.ContainerValue] | None]
            type MessageBatch = Sequence[Mapping[str, t.Scalar | None]]
            type StreamCatalog = Mapping[str, Sequence[t.Meltano.Singer.CatalogEntry]]
            type Record = Mapping[str, t.Scalar | None]
            type Schema = Mapping[str, t.Scalar | None]
            type State = Mapping[str, t.Scalar | None]
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

            type ModelConfiguration = Mapping[str, t.Scalar | None]
            type TestConfiguration = Mapping[str, str | Sequence[str]]
            type ProfileConfiguration = Mapping[str, Mapping[str, t.Scalar | None]]
            type ProjectConfiguration = Mapping[
                str,
                Mapping[str, t.ContainerValue] | None,
            ]
            type RunResults = Mapping[str, Sequence[Mapping[str, t.Scalar | None]]]
            type ManifestData = Mapping[str, Mapping[str, t.ContainerValue] | None]
            type Project = Mapping[str, str | bool | Sequence[str]]

        class Project:
            """Meltano-specific project types."""

            type ProjectConfig = Mapping[str, Mapping[str, t.ContainerValue] | None]
            type ProjectMetadata = Mapping[str, t.Scalar | None]
            type MeltanoProjectType = c.MeltanoProjectType
            type MeltanoProjectConfig = Mapping[
                str,
                Mapping[str, t.ContainerValue] | None,
            ]
            type PipelineConfig = Mapping[str, str | int | bool | Sequence[str]]
            type SingerConfig = Mapping[str, t.Scalar | None]
            type DbtConfig = Mapping[str, Mapping[str, t.ContainerValue] | None]

        class Bridge:
            """Bridge operation complex types namespace."""

            type BridgeMessage = Mapping[str, Mapping[str, t.ContainerValue] | None]
            type BridgeResponse = Mapping[str, Mapping[str, t.ContainerValue] | None]
            type VersionInfo = Mapping[str, str | int]
            type ConnectionInfo = Mapping[str, str | int | bool]
            type BridgeConfig = Mapping[str, Mapping[str, t.ContainerValue] | None]
            type BridgeStatus = Mapping[str, t.Scalar | None]

        class CLI:
            """CLI operation complex types namespace."""

            type Command = Sequence[str]
            type ProcessResult = Mapping[str, t.Scalar | Sequence[str]]
            type CommandResult = Mapping[str, str | int | bool]
            type ExecutionResult = Mapping[str, t.Scalar | None]
            type CLIStatus = Mapping[str, str | bool]

        class ELT:
            """ELT pipeline complex types namespace."""

            type PipelineResult = Mapping[str, t.Scalar | None | Sequence[t.Scalar]]
            type ExtractConfig = Mapping[str, Mapping[str, t.ContainerValue] | None]
            type LoadConfig = Mapping[str, Mapping[str, t.ContainerValue] | None]
            type TransformConfig = Mapping[str, Mapping[str, t.ContainerValue] | None]
            type ExtractionResult = Mapping[str, t.Scalar | None]
            type LoadingResult = Mapping[str, t.Scalar | None]
            type TransformationResult = Mapping[str, t.Scalar | None]

        class Processing:
            """Meltano-specific processing types."""

            type DbtTransformationResult = Mapping[str, t.ContainerValue]
            type SingerProcessingResult = Mapping[str, t.ContainerValue]
            type SingerExecutionResult = Mapping[str, t.ContainerValue]
            type EltPipelineResult = Mapping[str, t.ContainerValue]
            type Headers = Mapping[str, str]

        type NestedJsonValue = Mapping[str, t.ContainerValue] | t.Scalar | None
        type NestedJsonDict = Mapping[str, t.Meltano.NestedJsonValue]
        type MeltanoConfigDict = t.ContainerMapping
        type PluginConfigDict = Mapping[str, t.ContainerValue]
        type EnvironmentDict = Mapping[str, str]
        type VariablesDict = Mapping[str, str]
        type SettingsDict = Mapping[str, t.ContainerValue]
        type MetadataDict = Mapping[str, t.ContainerValue]
        type CommandDict = Mapping[str, t.ContainerValue]
        type ScheduleDict = Mapping[str, t.ContainerValue]
        type JobDict = Mapping[str, t.ContainerValue]
        type RecordDict = Mapping[str, t.Scalar | None]
        type SchemaDict = Mapping[str, t.Scalar | None]
        type StateDict = Mapping[str, t.Scalar | None]
        type ResultDict = t.ContainerMapping
        type RunContextDict = t.ContainerMapping
        type FileConfigDict = Mapping[str, t.NormalizedValue | Sequence[str]]
        PathDict = Mapping[str, str | Path]
        type PluginList = Sequence[str]
        type PluginNameList = Sequence[str]
        type PluginTypeList = Sequence[str]
        type ExecutionResultDict = t.ContainerMapping
        type ExecutionStatusDict = Mapping[str, str]
        type RuntimeConfigDict = Mapping[str, Mapping[str, t.ContainerValue] | None]
        type SingerRecordDict = Mapping[str, t.Scalar | None]
        type SingerStateDict = Mapping[str, t.Scalar | None]
        type SingerCatalogDict = t.ContainerMapping
        type SingerConfigDict = t.ContainerMapping
        type SingerSchemaDict = Mapping[str, t.Scalar | None]
        type SingerMessageList = Sequence[Mapping[str, t.Scalar | None]]
        type StreamNameList = Sequence[str]
        type DbtModelDict = t.ContainerMapping
        type DbtProfileDict = t.ContainerMapping
        type DbtProjectDict = t.ContainerMapping
        type DbtManifestDict = t.ContainerMapping
        type DbtResultDict = t.ContainerMapping
        type DbtModelList = Sequence[str]
        type DbtTestList = Sequence[str]

        class Pipeline:
            """Pipeline execution complex types namespace."""

            type PipelineConfig = t.ContainerMapping
            type PipelineStatus = Mapping[str, str | int | bool]
            type WorkflowDict = t.ContainerMapping
            type RunContextDict = t.ContainerMapping
            type ExecutionLogsDict = t.ContainerMapping
            type MetricsDict = Mapping[str, float]
            type ErrorsDict = Mapping[str, str]


t = FlextMeltanoTypes
__all__ = ["FlextMeltanoTypes", "t"]
