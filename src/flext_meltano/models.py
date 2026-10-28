# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT pipeline models.

Provides Pydantic models for data pipeline operations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import m

from flext_meltano._models import (
    FlextMeltanoModelsBase,
    FlextMeltanoModelsCliInputs,
    FlextMeltanoModelsConfig,
    FlextMeltanoModelsCore,
    FlextMeltanoModelsDiscovery,
    FlextMeltanoModelsInstances,
    FlextMeltanoModelsPayloadsData,
    FlextMeltanoModelsResultsDbt,
    FlextMeltanoModelsSinger,
    FlextMeltanoModelsSingerCatalog,
    FlextMeltanoModelsSingerSdk,
    FlextMeltanoModelsSources,
    FlextMeltanoModelsSourcesParams,
)


class FlextMeltanoModels(m):
    """Generic pipeline models.

    Provides reusable Pydantic models for pipeline operations.
    """

    class Meltano(
        FlextMeltanoModelsBase,
        FlextMeltanoModelsCliInputs,
        FlextMeltanoModelsConfig,
        FlextMeltanoModelsCore,
        FlextMeltanoModelsDiscovery,
        FlextMeltanoModelsInstances,
        FlextMeltanoModelsPayloadsData,
        FlextMeltanoModelsResultsDbt,
        FlextMeltanoModelsSinger,
        FlextMeltanoModelsSingerCatalog,
        FlextMeltanoModelsSingerSdk,
        FlextMeltanoModelsSources,
        FlextMeltanoModelsSourcesParams,
    ):
        """Meltano domain namespace."""


m = FlextMeltanoModels
__all__: list[str] = ["FlextMeltanoModels", "m"]
