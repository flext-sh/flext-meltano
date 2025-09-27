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

from typing import Literal

from flext_core import FlextTypes

# =============================================================================
# MELTANO-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for Meltano operations
# =============================================================================


# Meltano domain TypeVars
class FlextMeltanoTypes(FlextTypes):
    """Meltano-specific type definitions extending FlextTypes.

    Domain-specific type system for Meltano data integration operations.
    Contains ONLY complex Meltano-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # MELTANO PLUGIN TYPES - Complex plugin management types
    # =========================================================================

    class Plugin:
        """Meltano plugin complex types."""

        type PluginDefinition = dict[
            str, str | list[str] | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type PluginConfiguration = dict[
            str, FlextTypes.Core.ConfigValue | dict[str, object]
        ]
        type PluginCatalog = dict[str, list[PluginDefinition]]
        type PluginRegistry = dict[str, PluginDefinition | PluginConfiguration]
        type PluginInstallation = dict[str, str | bool | list[str]]
        type PluginExecution = dict[str, FlextTypes.Core.JsonValue | bool]
        type PluginInfo = dict[str, str | bool | int | dict[str, object]]

    # =========================================================================
    # SINGER PROTOCOL TYPES - Complex Singer operations
    # =========================================================================

    class Singer:
        """Singer protocol complex types."""

        type CatalogEntry = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]
        type StreamSchema = dict[str, dict[str, FlextTypes.Core.JsonValue]]
        type TapConfig = dict[str, FlextTypes.Core.ConfigValue | dict[str, object]]
        type TargetConfig = dict[str, FlextTypes.Core.ConfigValue | dict[str, object]]
        type MessageBatch = list[dict[str, FlextTypes.Core.JsonValue]]
        type StreamCatalog = dict[str, list[CatalogEntry]]

    # =========================================================================
    # DBT TRANSFORMATION TYPES - Complex DBT operations
    # =========================================================================

    class Dbt:
        """DBT transformation complex types."""

        type ModelConfiguration = dict[str, FlextTypes.Core.ConfigValue | list[str]]
        type TestConfiguration = dict[str, str | list[str] | dict[str, object]]
        type ProfileConfiguration = dict[str, FlextTypes.Core.ConfigDict]
        type ProjectConfiguration = dict[
            str, FlextTypes.Core.ConfigValue | dict[str, object]
        ]
        type RunResults = dict[str, list[dict[str, FlextTypes.Core.JsonValue]]]
        type ManifestData = dict[str, dict[str, FlextTypes.Core.JsonValue]]
        type Project = dict[str, str | bool | dict[str, object] | list[str]]

    # =========================================================================
    # MELTANO PROJECT TYPES - Complex project management
    # =========================================================================

    class Project(FlextTypes.Project):
        """Meltano-specific project types extending FlextTypes.Project.

        Adds Meltano/ELT-specific project types while inheriting generic types
        from FlextTypes. Follows domain separation principle: Meltano domain owns
        Meltano-specific types.
        """

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
        type MeltanoProjectConfig = dict[str, FlextTypes.Core.ConfigValue | object]
        type PipelineConfig = dict[str, str | int | bool | list[str]]
        type SingerConfig = dict[str, bool | str | dict[str, object]]
        type DbtConfig = dict[str, FlextTypes.Core.ConfigValue | object]

    # =========================================================================
    # ELT PIPELINE TYPES - Complex pipeline operations
    # =========================================================================

    class Pipeline:
        """ELT pipeline complex types."""

        type PipelineDefinition = list[
            dict[str, str | dict[str, FlextTypes.Core.JsonValue]]
        ]
        type ExecutionContext = dict[str, FlextTypes.Core.JsonValue | dict[str, object]]
        type RuntimeEnvironment = dict[
            str, str | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type PipelineResults = dict[
            str, FlextTypes.Processing.ProcessingStatus | dict[str, object]
        ]
        type WorkflowConfiguration = dict[
            str, FlextTypes.Processing.WorkflowStatus | list[str]
        ]

    # =========================================================================
    # BRIDGE TYPES - Complex bridge operations
    # =========================================================================

    class Bridge:
        """Bridge operation complex types."""

        type VersionInfo = dict[str, str | int]
        type ConnectionInfo = dict[str, str | int | bool]
        type BridgeConfig = dict[str, FlextTypes.Core.ConfigValue | object]
        type BridgeStatus = dict[str, str | bool | dict[str, object]]

    # =========================================================================
    # CLI TYPES - Complex CLI operations
    # =========================================================================

    class CLI:
        """CLI operation complex types."""

        type ProcessResult = dict[str, str | int | float | bool | list[str]]
        type CommandResult = dict[str, str | int | bool]
        type ExecutionResult = dict[str, str | int | bool | dict[str, object]]
        type CLIStatus = dict[str, str | bool]

    # =========================================================================
    # ELT PIPELINE TYPES - Complex ELT operations
    # =========================================================================

    class ELT:
        """ELT pipeline complex types."""

        type PipelineResult = dict[
            str, str | int | float | bool | dict[str, object] | list[object]
        ]
        type ExtractionResult = dict[str, str | int | bool | dict[str, object]]
        type LoadingResult = dict[str, str | int | bool | dict[str, object]]
        type TransformationResult = dict[str, str | int | bool | dict[str, object]]

    # =========================================================================
    # CORE COMMONLY USED TYPES - Extending FlextTypes.Core for Meltano domain
    # =========================================================================

    class Core(FlextTypes.Core):
        """Commonly used Meltano-specific type aliases extending FlextTypes.Core.

        Provides standardized type aliases for frequent Meltano patterns while
        inheriting all core types from FlextTypes.Core. Reduces generic dict/list
        usage throughout the Meltano codebase.
        """

        # Meltano configuration and data types
        type MeltanoConfigDict = dict[str, object]
        type PluginConfigDict = dict[str, object]
        type EnvironmentDict = dict[str, str]
        type VariablesDict = dict[str, str]
        type SettingsDict = dict[str, object]
        type CommandDict = dict[str, object]
        type ScheduleDict = dict[str, object]
        type JobDict = dict[str, object]

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

        # Pipeline and workflow types
        type PipelineConfigDict = dict[str, object]
        type WorkflowDict = dict[str, object]
        type RunContextDict = dict[str, object]
        type ExecutionLogsDict = dict[str, object]
        type MetricsDict = dict[str, float]
        type ErrorsDict = dict[str, str]

        # Library and runner types
        type LibraryDict = dict[str, object]
        type RunnerConfigDict = dict[str, object]
        type ProcessResultDict = dict[str, object]
        type OutputDict = dict[str, object]
        type LogsDict = dict[str, object]
        type MetadataDict = dict[str, str | int | bool | dict[str, object]]
        type ResponseDict = dict[str, str | int | bool | dict[str, object]]


# =============================================================================
# PUBLIC API EXPORTS - Meltano TypeVars and types
# =============================================================================

__all__: list[str] = [
    "FlextMeltanoTypes",
]
