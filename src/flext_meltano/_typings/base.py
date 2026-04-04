"""FLEXT Meltano typings - Base type aliases and plugin types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import ClassVar

from flext_cli import FlextCliTypes
from pydantic import TypeAdapter

from flext_meltano import c


class FlextMeltanoTypingsBase:
    """Base Meltano type aliases and plugin type definitions."""

    CONTAINER_MAP_ADAPTER: ClassVar[TypeAdapter[FlextCliTypes.ContainerMapping]] = (
        TypeAdapter(FlextCliTypes.ContainerMapping)
    )
    INTEGER_ADAPTER: ClassVar[TypeAdapter[FlextCliTypes.IntegerValue]] = TypeAdapter(
        FlextCliTypes.IntegerValue
    )

    type ValidatorInput = (
        FlextCliTypes.ContainerMapping
        | Mapping[str, FlextCliTypes.ContainerMapping | None]
        | Sequence[FlextCliTypes.ContainerMapping | None]
        | tuple[FlextCliTypes.ContainerMapping | None, ...]
        | set[FlextCliTypes.ContainerMapping | None]
        | None
    )

    type MeltanoValue = Mapping[str, FlextCliTypes.ContainerValue] | None

    type PluginDefinition = Mapping[
        str,
        str | FlextCliTypes.StrSequence | Mapping[str, FlextCliTypes.Scalar | None],
    ]
    type PluginConfiguration = FlextCliTypes.ContainerMapping
    type PluginCatalog = Mapping[
        str,
        Sequence[FlextMeltanoTypingsBase.PluginDefinition],
    ]
    type PluginRegistry = Mapping[
        str,
        FlextMeltanoTypingsBase.PluginDefinition
        | FlextMeltanoTypingsBase.PluginConfiguration,
    ]
    type PluginInstallation = Mapping[str, str | bool | FlextCliTypes.StrSequence]
    type PluginExecution = Mapping[
        str,
        Mapping[str, FlextCliTypes.ContainerValue] | None,
    ]
    type PluginInfo = Mapping[str, FlextCliTypes.Scalar | None]
    PluginType = c.Meltano.Enums.PluginType
    PluginVariant = str  # "default" | "singer" | "custom"

    type VariantValue = str | FlextCliTypes.StrSequence | FlextCliTypes.ScalarMapping | None
    "Normalized plugin variant: string, string list, scalar mapping, or null."

    type NestedJsonValue = (
        Mapping[str, FlextCliTypes.ContainerValue] | FlextCliTypes.Scalar | None
    )
    type NestedJsonDict = Mapping[str, FlextMeltanoTypingsBase.NestedJsonValue]
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
        FlextCliTypes.NormalizedValue | FlextCliTypes.StrSequence,
    ]
    PathDict = Mapping[str, str | Path]
    type PluginList = FlextCliTypes.StrSequence
    type PluginNameList = FlextCliTypes.StrSequence
    type PluginTypeList = FlextCliTypes.StrSequence
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
    type StreamNameList = FlextCliTypes.StrSequence
    type DbtModelDict = FlextCliTypes.ContainerMapping
    type DbtProfileDict = FlextCliTypes.ContainerMapping
    type DbtProjectDict = FlextCliTypes.ContainerMapping
    type DbtManifestDict = FlextCliTypes.ContainerMapping
    type DbtResultDict = FlextCliTypes.ContainerMapping
    type DbtModelList = FlextCliTypes.StrSequence
    type DbtTestList = FlextCliTypes.StrSequence

    class Pipeline:
        """Pipeline execution complex types namespace."""

        type PipelineConfig = FlextCliTypes.ContainerMapping
        type PipelineStatus = FlextCliTypes.ConfigurationMapping
        type WorkflowDict = FlextCliTypes.ContainerMapping
        type RunContextDict = FlextCliTypes.ContainerMapping
        type ExecutionLogsDict = FlextCliTypes.ContainerMapping
        type MetricsDict = Mapping[str, float]
        type ErrorsDict = FlextCliTypes.StrMapping
