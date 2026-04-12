"""FLEXT pipeline models.

Provides Pydantic models for data pipeline operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliModels

from flext_meltano import (
    FlextMeltanoModelsCliParams,
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
        FlextMeltanoModelsCore,
        FlextMeltanoModelsLogging,
        FlextMeltanoModelsCliParams,
        FlextMeltanoModelsSourcesParams,
        FlextMeltanoModelsSources,
        FlextMeltanoModelsInstances,
        FlextMeltanoModelsInstancesData,
        FlextMeltanoModelsSinger,
        FlextMeltanoModelsSingerSdk,
        FlextMeltanoModelsSingerCatalog,
        FlextMeltanoModelsPayloads,
        FlextMeltanoModelsPayloadsData,
        FlextMeltanoModelsContext,
        FlextMeltanoModelsDiscovery,
        FlextMeltanoModelsProjects,
        FlextMeltanoModelsProjectsPlugin,
        FlextMeltanoModelsTransformations,
        FlextMeltanoModelsResults,
        FlextMeltanoModelsResultsDbt,
        FlextMeltanoModelsResultsPipeline,
    ):
        """Meltano domain namespace."""


m = FlextMeltanoModels

__all__: list[str] = [
    "FlextMeltanoModels",
    "m",
]
