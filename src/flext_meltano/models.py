# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT pipeline models.

Provides Pydantic models for data pipeline operations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import m as flext_cli_m

from flext_meltano._models.base import FlextMeltanoModelsBase
from flext_meltano._models.cli_inputs import FlextMeltanoModelsCliInputs
from flext_meltano._models.config import FlextMeltanoModelsConfig
from flext_meltano._models.core import FlextMeltanoModelsCore
from flext_meltano._models.discovery import FlextMeltanoModelsDiscovery
from flext_meltano._models.instances import FlextMeltanoModelsInstances
from flext_meltano._models.payloads_data import FlextMeltanoModelsPayloadsData
from flext_meltano._models.results_dbt import FlextMeltanoModelsResultsDbt
from flext_meltano._models.singer import FlextMeltanoModelsSinger
from flext_meltano._models.singer_catalog import FlextMeltanoModelsSingerCatalog
from flext_meltano._models.singer_sdk import FlextMeltanoModelsSingerSdk
from flext_meltano._models.sources import FlextMeltanoModelsSources
from flext_meltano._models.sources_params import FlextMeltanoModelsSourcesParams


class FlextMeltanoModels(flext_cli_m):
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
