"""FLEXT Meltano typings - Domain-specific types (Dbt, Project, Bridge, CLI, ELT, Processing).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from flext_cli import FlextCliTypes

from flext_meltano import c


class FlextMeltanoTypingsDomains:
    """Domain-specific type definitions for Meltano subsystems."""

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
        type MeltanoProjectType = c.Meltano.MeltanoProjectType
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
            FlextCliTypes.Scalar | FlextCliTypes.ScalarList | None,
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

        type DbtTransformationResult = FlextCliTypes.MutableContainerMapping
        type SingerProcessingResult = FlextCliTypes.MutableContainerMapping
        type SingerExecutionResult = FlextCliTypes.MutableContainerMapping
        type EltPipelineResult = FlextCliTypes.MutableContainerMapping
        type Headers = FlextCliTypes.StrMapping
