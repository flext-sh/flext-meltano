"""FLEXT Meltano Types - Domain-specific Meltano type definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

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

        type MeltanoValue = Mapping[str, FlextCliTypes.ContainerValue] | None

        type PluginDefinition = Mapping[
            str,
            str | Sequence[str] | Mapping[str, FlextCliTypes.Scalar | None],
        ]
        type PluginConfiguration = FlextCliTypes.ContainerMapping
        type PluginCatalog = Mapping[
            str,
            Sequence[FlextMeltanoTypes.Meltano.PluginDefinition],
        ]
        type PluginRegistry = Mapping[
            str,
            FlextMeltanoTypes.Meltano.PluginDefinition
            | FlextMeltanoTypes.Meltano.PluginConfiguration,
        ]
        type PluginInstallation = Mapping[str, str | bool | Sequence[str]]
        type PluginExecution = Mapping[
            str,
            Mapping[str, FlextCliTypes.ContainerValue] | None,
        ]
        type PluginInfo = Mapping[str, FlextCliTypes.Scalar | None]
        PluginType = c.Meltano.Enums.PluginType
        PluginVariant = str  # "default" | "singer" | "custom"

        class Singer:
            """Singer protocol complex types namespace."""

            type CatalogEntry = Mapping[
                str,
                str | Mapping[str, FlextCliTypes.Scalar | None],
            ]
            type StreamSchema = Mapping[str, Mapping[str, FlextCliTypes.Scalar | None]]
            type TapConfig = Mapping[
                str,
                Mapping[str, FlextCliTypes.ContainerValue] | None,
            ]
            type TargetConfig = Mapping[
                str,
                Mapping[str, FlextCliTypes.ContainerValue] | None,
            ]
            type MessageBatch = Sequence[Mapping[str, FlextCliTypes.Scalar | None]]
            type StreamCatalog = Mapping[
                str,
                Sequence[FlextMeltanoTypes.Meltano.Singer.CatalogEntry],
            ]
            type Record = Mapping[str, FlextCliTypes.Scalar | None]
            type Schema = Mapping[str, FlextCliTypes.Scalar | None]
            type State = Mapping[str, FlextCliTypes.Scalar | None]
            ReplicationMethod = c.Meltano.Enums.ReplicationMethod
            SingerVersion = str  # "0.44.0" | "0.45.0" | ...

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

            type ModelConfiguration = Mapping[str, FlextCliTypes.Scalar | None]
            type TestConfiguration = Mapping[str, str | Sequence[str]]
            type ProfileConfiguration = Mapping[
                str,
                Mapping[str, FlextCliTypes.Scalar | None],
            ]
            type ProjectConfiguration = Mapping[
                str,
                Mapping[str, FlextCliTypes.ContainerValue] | None,
            ]
            type RunResults = Mapping[
                str,
                Sequence[Mapping[str, FlextCliTypes.Scalar | None]],
            ]
            type ManifestData = Mapping[
                str,
                Mapping[str, FlextCliTypes.ContainerValue] | None,
            ]
            type Project = Mapping[str, str | bool | Sequence[str]]

        class Project:
            """Meltano-specific project types."""

            type ProjectConfig = Mapping[
                str,
                Mapping[str, FlextCliTypes.ContainerValue] | None,
            ]
            type ProjectMetadata = Mapping[str, FlextCliTypes.Scalar | None]
            type MeltanoProjectType = c.MeltanoProjectType
            type MeltanoProjectConfig = Mapping[
                str,
                Mapping[str, FlextCliTypes.ContainerValue] | None,
            ]
            type PipelineConfig = Mapping[str, FlextCliTypes.Scalar | Sequence[str]]
            type SingerConfig = Mapping[str, FlextCliTypes.Scalar | None]
            type DbtConfig = Mapping[
                str,
                Mapping[str, FlextCliTypes.ContainerValue] | None,
            ]

        class Bridge:
            """Bridge operation complex types namespace."""

            type BridgeMessage = Mapping[
                str,
                Mapping[str, FlextCliTypes.ContainerValue] | None,
            ]
            type BridgeResponse = Mapping[
                str,
                Mapping[str, FlextCliTypes.ContainerValue] | None,
            ]
            type VersionInfo = Mapping[str, str | int]
            type ConnectionInfo = FlextCliTypes.ConfigurationMapping
            type BridgeConfig = Mapping[
                str,
                Mapping[str, FlextCliTypes.ContainerValue] | None,
            ]
            type BridgeStatus = Mapping[str, FlextCliTypes.Scalar | None]

        class CLI:
            """CLI operation complex types namespace."""

            type Command = Sequence[str]
            type ProcessResult = Mapping[str, FlextCliTypes.Scalar | Sequence[str]]
            type CommandResult = FlextCliTypes.ConfigurationMapping
            type ExecutionResult = Mapping[str, FlextCliTypes.Scalar | None]
            type CLIStatus = Mapping[str, str | bool]

        class ELT:
            """ELT pipeline complex types namespace."""

            type PipelineResult = Mapping[
                str,
                FlextCliTypes.Scalar | None | FlextCliTypes.ScalarList,
            ]
            type ExtractConfig = Mapping[
                str,
                Mapping[str, FlextCliTypes.ContainerValue] | None,
            ]
            type LoadConfig = Mapping[
                str,
                Mapping[str, FlextCliTypes.ContainerValue] | None,
            ]
            type TransformConfig = Mapping[
                str,
                Mapping[str, FlextCliTypes.ContainerValue] | None,
            ]
            type ExtractionResult = Mapping[str, FlextCliTypes.Scalar | None]
            type LoadingResult = Mapping[str, FlextCliTypes.Scalar | None]
            type TransformationResult = Mapping[str, FlextCliTypes.Scalar | None]

        class Processing:
            """Meltano-specific processing types."""

            type DbtTransformationResult = dict[str, FlextCliTypes.ContainerValue]
            type SingerProcessingResult = dict[str, FlextCliTypes.ContainerValue]
            type SingerExecutionResult = dict[str, FlextCliTypes.ContainerValue]
            type EltPipelineResult = dict[str, FlextCliTypes.ContainerValue]
            type Headers = FlextCliTypes.StrMapping

        type NestedJsonValue = (
            Mapping[str, FlextCliTypes.ContainerValue] | FlextCliTypes.Scalar | None
        )
        type NestedJsonDict = Mapping[str, FlextMeltanoTypes.Meltano.NestedJsonValue]
        type MeltanoConfigDict = FlextCliTypes.ContainerMapping
        type PluginConfigDict = Mapping[str, FlextCliTypes.ContainerValue]
        type EnvironmentDict = FlextCliTypes.StrMapping
        type VariablesDict = FlextCliTypes.StrMapping
        type SettingsDict = Mapping[str, FlextCliTypes.ContainerValue]
        type MetadataDict = Mapping[str, FlextCliTypes.ContainerValue]
        type CommandDict = Mapping[str, FlextCliTypes.ContainerValue]
        type ScheduleDict = Mapping[str, FlextCliTypes.ContainerValue]
        type JobDict = Mapping[str, FlextCliTypes.ContainerValue]
        type RecordDict = Mapping[str, FlextCliTypes.Scalar | None]
        type SchemaDict = Mapping[str, FlextCliTypes.Scalar | None]
        type StateDict = Mapping[str, FlextCliTypes.Scalar | None]
        type ResultDict = FlextCliTypes.ContainerMapping
        type RunContextDict = FlextCliTypes.ContainerMapping
        type FileConfigDict = Mapping[
            str,
            FlextCliTypes.NormalizedValue | Sequence[str],
        ]
        PathDict = Mapping[str, str | Path]
        type PluginList = Sequence[str]
        type PluginNameList = Sequence[str]
        type PluginTypeList = Sequence[str]
        type ExecutionResultDict = FlextCliTypes.ContainerMapping
        type ExecutionStatusDict = FlextCliTypes.StrMapping
        type RuntimeConfigDict = Mapping[
            str,
            Mapping[str, FlextCliTypes.ContainerValue] | None,
        ]
        type SingerRecordDict = Mapping[str, FlextCliTypes.Scalar | None]
        type SingerStateDict = Mapping[str, FlextCliTypes.Scalar | None]
        type SingerCatalogDict = FlextCliTypes.ContainerMapping
        type SingerConfigDict = FlextCliTypes.ContainerMapping
        type SingerSchemaDict = Mapping[str, FlextCliTypes.Scalar | None]
        type SingerMessageList = Sequence[Mapping[str, FlextCliTypes.Scalar | None]]
        type StreamNameList = Sequence[str]
        type DbtModelDict = FlextCliTypes.ContainerMapping
        type DbtProfileDict = FlextCliTypes.ContainerMapping
        type DbtProjectDict = FlextCliTypes.ContainerMapping
        type DbtManifestDict = FlextCliTypes.ContainerMapping
        type DbtResultDict = FlextCliTypes.ContainerMapping
        type DbtModelList = Sequence[str]
        type DbtTestList = Sequence[str]

        class Pipeline:
            """Pipeline execution complex types namespace."""

            type PipelineConfig = FlextCliTypes.ContainerMapping
            type PipelineStatus = FlextCliTypes.ConfigurationMapping
            type WorkflowDict = FlextCliTypes.ContainerMapping
            type RunContextDict = FlextCliTypes.ContainerMapping
            type ExecutionLogsDict = FlextCliTypes.ContainerMapping
            type MetricsDict = Mapping[str, float]
            type ErrorsDict = Mapping[str, str]


t = FlextMeltanoTypes
__all__ = ["FlextMeltanoTypes", "t"]
