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

from flext_meltano import c


class FlextMeltanoTypes(FlextCliTypes):
    """Meltano-specific type definitions extending t.

    Domain-specific type system for Meltano data integration operations.
    Contains ONLY complex Meltano-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    class Meltano:
        """Meltano plugin complex types namespace."""

        type MeltanoValue = dict[str, t.ContainerValue] | None

        type PluginDefinition = dict[
            str,
            str | list[str] | Mapping[str, t.Scalar | None],
        ]
        type PluginConfiguration = dict[str, t.NormalizedValue]
        type PluginCatalog = dict[str, list[t.Meltano.PluginDefinition]]
        type PluginRegistry = Mapping[
            str,
            t.Meltano.PluginDefinition | t.Meltano.PluginConfiguration,
        ]
        type PluginInstallation = dict[str, str | bool | list[str]]
        type PluginExecution = Mapping[str, dict[str, t.ContainerValue] | None]
        type PluginInfo = dict[str, t.Scalar | None]
        PluginType = Literal["extractors", "loaders", "transforms", "orchestrators"]
        PluginVariant = Literal["default", "singer", "custom"]

        class _PluginMeta(type):
            """Metaclass that proxies attribute access to the Meltano class."""

            def __getattr__(cls, name: str) -> type | str:
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

            type CatalogEntry = dict[str, str | Mapping[str, t.Scalar | None]]
            type StreamSchema = dict[str, dict[str, t.Scalar | None]]
            type TapConfig = Mapping[str, dict[str, t.ContainerValue] | None]
            type TargetConfig = Mapping[str, dict[str, t.ContainerValue] | None]
            type MessageBatch = list[dict[str, t.Scalar | None]]
            type StreamCatalog = dict[str, list[t.Meltano.Singer.CatalogEntry]]
            type Record = dict[str, t.Scalar | None]
            type Schema = dict[str, t.Scalar | None]
            type State = dict[str, t.Scalar | None]
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

            type ModelConfiguration = dict[str, t.Scalar | None]
            type TestConfiguration = dict[str, str | list[str]]
            type ProfileConfiguration = dict[str, dict[str, t.Scalar | None]]
            type ProjectConfiguration = Mapping[
                str,
                dict[str, t.ContainerValue] | None,
            ]
            type RunResults = dict[str, list[dict[str, t.Scalar | None]]]
            type ManifestData = Mapping[str, dict[str, t.ContainerValue] | None]
            type Project = dict[str, str | bool | list[str]]

        class Project:
            """Meltano-specific project types."""

            type ProjectConfig = Mapping[str, dict[str, t.ContainerValue] | None]
            type ProjectMetadata = dict[str, t.Scalar | None]
            type MeltanoProjectType = c.MeltanoProjectType
            type MeltanoProjectConfig = Mapping[
                str,
                dict[str, t.ContainerValue] | None,
            ]
            type PipelineConfig = dict[str, str | int | bool | list[str]]
            type SingerConfig = dict[str, t.Scalar | None]
            type DbtConfig = Mapping[str, dict[str, t.ContainerValue] | None]

        class Bridge:
            """Bridge operation complex types namespace."""

            type BridgeMessage = Mapping[str, dict[str, t.ContainerValue] | None]
            type BridgeResponse = Mapping[str, dict[str, t.ContainerValue] | None]
            type VersionInfo = dict[str, str | int]
            type ConnectionInfo = dict[str, str | int | bool]
            type BridgeConfig = Mapping[str, dict[str, t.ContainerValue] | None]
            type BridgeStatus = dict[str, t.Scalar | None]

        class CLI:
            """CLI operation complex types namespace."""

            type Command = list[str]
            type ProcessResult = dict[str, t.Scalar | list[str]]
            type CommandResult = dict[str, str | int | bool]
            type ExecutionResult = dict[str, t.Scalar | None]
            type CLIStatus = dict[str, str | bool]

        class ELT:
            """ELT pipeline complex types namespace."""

            type PipelineResult = dict[str, t.Scalar | None | list[t.Scalar]]
            type ExtractConfig = Mapping[str, dict[str, t.ContainerValue] | None]
            type LoadConfig = Mapping[str, dict[str, t.ContainerValue] | None]
            type TransformConfig = Mapping[str, dict[str, t.ContainerValue] | None]
            type ExtractionResult = dict[str, t.Scalar | None]
            type LoadingResult = dict[str, t.Scalar | None]
            type TransformationResult = dict[str, t.Scalar | None]

        class Processing:
            """Meltano-specific processing types."""

            type DbtTransformationResult = dict[str, t.ContainerValue]
            type SingerProcessingResult = dict[str, t.ContainerValue]
            type SingerExecutionResult = dict[str, t.ContainerValue]
            type EltPipelineResult = dict[str, t.ContainerValue]
            type Headers = dict[str, str]

        type NestedJsonValue = dict[str, t.ContainerValue] | t.Scalar | None
        type NestedJsonDict = dict[str, t.Meltano.NestedJsonValue]
        type MeltanoConfigDict = Mapping[str, t.NormalizedValue]
        type PluginConfigDict = dict[str, t.ContainerValue]
        type EnvironmentDict = dict[str, str]
        type VariablesDict = dict[str, str]
        type SettingsDict = dict[str, t.ContainerValue]
        type MetadataDict = dict[str, t.ContainerValue]
        type CommandDict = dict[str, t.ContainerValue]
        type ScheduleDict = dict[str, t.ContainerValue]
        type JobDict = dict[str, t.ContainerValue]
        type RecordDict = Mapping[str, t.Scalar | None]
        type SchemaDict = Mapping[str, t.Scalar | None]
        type StateDict = Mapping[str, t.Scalar | None]
        type ResultDict = Mapping[str, t.NormalizedValue]
        type RunContextDict = dict[str, t.NormalizedValue]
        type FileConfigDict = dict[str, t.NormalizedValue | list[str]]
        PathDict = Mapping[str, str | Path]
        type PluginList = list[str]
        type PluginNameList = list[str]
        type PluginTypeList = list[str]
        type ExecutionResultDict = Mapping[str, t.NormalizedValue]
        type ExecutionStatusDict = Mapping[str, str]
        type RuntimeConfigDict = Mapping[str, dict[str, t.ContainerValue] | None]
        type SingerRecordDict = dict[str, t.Scalar | None]
        type SingerStateDict = dict[str, t.Scalar | None]
        type SingerCatalogDict = dict[str, t.NormalizedValue]
        type SingerConfigDict = dict[str, t.NormalizedValue]
        type SingerSchemaDict = dict[str, t.Scalar | None]
        type SingerMessageList = list[dict[str, t.Scalar | None]]
        type StreamNameList = list[str]
        type DbtModelDict = dict[str, t.NormalizedValue]
        type DbtProfileDict = dict[str, t.NormalizedValue]
        type DbtProjectDict = dict[str, t.NormalizedValue]
        type DbtManifestDict = dict[str, t.NormalizedValue]
        type DbtResultDict = dict[str, t.NormalizedValue]
        type DbtModelList = list[str]
        type DbtTestList = list[str]

        class Pipeline:
            """Pipeline execution complex types namespace."""

            type PipelineConfig = dict[str, t.NormalizedValue]
            type PipelineStatus = dict[str, str | int | bool]
            type WorkflowDict = dict[str, t.NormalizedValue]
            type RunContextDict = dict[str, t.NormalizedValue]
            type ExecutionLogsDict = dict[str, t.NormalizedValue]
            type MetricsDict = dict[str, float]
            type ErrorsDict = dict[str, str]

    Singer = Meltano.Singer


t = FlextMeltanoTypes
__all__ = ["FlextMeltanoTypes", "t"]
