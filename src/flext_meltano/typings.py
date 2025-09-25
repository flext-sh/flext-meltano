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

from typing import TypeVar

from flext_core import FlextTypes

# =============================================================================
# MELTANO-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for Meltano operations
# =============================================================================

# Meltano domain TypeVars
TMeltanoProject = TypeVar("TMeltanoProject")
TSingerTap = TypeVar("TSingerTap")
TSingerTarget = TypeVar("TSingerTarget")
TSingerStream = TypeVar("TSingerStream")
TDbtModel = TypeVar("TDbtModel")
TDbtRunner = TypeVar("TDbtRunner")
TMeltanoPlugin = TypeVar("TMeltanoPlugin")
TMeltanoEnvironment = TypeVar("TMeltanoEnvironment")
TPipelineConfig = TypeVar("TPipelineConfig")


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

    # =========================================================================
    # MELTANO PROJECT TYPES - Complex project management
    # =========================================================================

    class Project:
        """Meltano project complex types."""

        type ProjectDefinition = dict[
            str, FlextTypes.Core.ConfigValue | list[dict[str, object]]
        ]
        type EnvironmentConfig = dict[str, FlextTypes.Core.ConfigDict]
        type ScheduleDefinition = dict[str, str | int | list[str]]
        type JobDefinition = dict[str, str | list[str] | dict[str, object]]
        type PipelineConfiguration = list[dict[str, str | dict[str, object]]]
        type StateManagement = dict[str, FlextTypes.Core.JsonValue | dict[str, object]]

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


# =============================================================================
# PUBLIC API EXPORTS - Meltano TypeVars and types
# =============================================================================

__all__: list[str] = [
    # Meltano Types class
    "FlextMeltanoTypes",
    # Meltano-specific TypeVars
    "TDbtModel",
    "TDbtRunner",
    "TMeltanoEnvironment",
    "TMeltanoPlugin",
    "TMeltanoProject",
    "TPipelineConfig",
    "TSingerStream",
    "TSingerTap",
    "TSingerTarget",
]
