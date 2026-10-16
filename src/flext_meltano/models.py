# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT pipeline models.

Provides Pydantic models for data pipeline operations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliModels

from flext_meltano._models import (
    FlextMeltanoModelsBase,
    FlextMeltanoModelsCliInputs,
    FlextMeltanoModelsCliParams,
    FlextMeltanoModelsConfig,
    FlextMeltanoModelsContext,
    FlextMeltanoModelsCore,
    FlextMeltanoModelsDiscovery,
    FlextMeltanoModelsInstances,
    FlextMeltanoModelsInstancesData,
    FlextMeltanoModelsLogging,
    FlextMeltanoModelsPayloads,
    FlextMeltanoModelsPayloadsData,
    FlextMeltanoModelsProjects,
    FlextMeltanoModelsProjectsPlugin,
    FlextMeltanoModelsResults,
    FlextMeltanoModelsResultsDbt,
    FlextMeltanoModelsResultsPipeline,
    FlextMeltanoModelsSinger,
    FlextMeltanoModelsSingerCatalog,
    FlextMeltanoModelsSingerSdk,
    FlextMeltanoModelsSources,
    FlextMeltanoModelsSourcesParams,
    FlextMeltanoModelsTransformations,
)


class FlextMeltanoModels(FlextCliModels):
    """Generic pipeline models.

    Provides reusable Pydantic models for pipeline operations.
    """

    class Meltano(
        FlextMeltanoModelsBase,
        FlextMeltanoModelsCliInputs,
        FlextMeltanoModelsCliParams,
        FlextMeltanoModelsConfig,
        FlextMeltanoModelsContext,
        FlextMeltanoModelsCore,
        FlextMeltanoModelsDiscovery,
        FlextMeltanoModelsInstances,
        FlextMeltanoModelsInstancesData,
        FlextMeltanoModelsLogging,
        FlextMeltanoModelsPayloads,
        FlextMeltanoModelsPayloadsData,
        FlextMeltanoModelsProjects,
        FlextMeltanoModelsProjectsPlugin,
        FlextMeltanoModelsResults,
        FlextMeltanoModelsResultsDbt,
        FlextMeltanoModelsResultsPipeline,
        FlextMeltanoModelsSinger,
        FlextMeltanoModelsSingerCatalog,
        FlextMeltanoModelsSingerSdk,
        FlextMeltanoModelsSources,
        FlextMeltanoModelsSourcesParams,
        FlextMeltanoModelsTransformations,
    ):
        """Meltano domain namespace."""


m = FlextMeltanoModels

__all__ = ["FlextMeltanoModels", "m"]
