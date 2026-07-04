"""FLEXT pipeline models.

Provides Pydantic models for data pipeline operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliModels
from flext_meltano._models.cli_inputs import FlextMeltanoModelsCliInputs
from flext_meltano._models.cli_params import FlextMeltanoModelsCliParams
from flext_meltano._models.context import FlextMeltanoModelsContext
from flext_meltano._models.core import FlextMeltanoModelsCore
from flext_meltano._models.discovery import FlextMeltanoModelsDiscovery
from flext_meltano._models.instances import FlextMeltanoModelsInstances
from flext_meltano._models.instances_data import FlextMeltanoModelsInstancesData
from flext_meltano._models.logging_config import FlextMeltanoModelsLogging
from flext_meltano._models.payloads_data import FlextMeltanoModelsPayloadsData
from flext_meltano._models.projects import FlextMeltanoModelsProjects
from flext_meltano._models.results import FlextMeltanoModelsResults
from flext_meltano._models.results_dbt import FlextMeltanoModelsResultsDbt
from flext_meltano._models.results_pipeline import FlextMeltanoModelsResultsPipeline
from flext_meltano._models.singer import FlextMeltanoModelsSinger
from flext_meltano._models.singer_catalog import FlextMeltanoModelsSingerCatalog
from flext_meltano._models.singer_sdk import FlextMeltanoModelsSingerSdk
from flext_meltano._models.sources import FlextMeltanoModelsSources
from flext_meltano._models.sources_params import FlextMeltanoModelsSourcesParams
from flext_meltano._models.transformations import FlextMeltanoModelsTransformations


class FlextMeltanoModels(FlextCliModels):
    """Generic pipeline models.

    Provides reusable Pydantic models for pipeline operations.
    """

    class Meltano(
        FlextMeltanoModelsCore,
        FlextMeltanoModelsLogging,
        FlextMeltanoModelsCliInputs,
        FlextMeltanoModelsCliParams,
        FlextMeltanoModelsSourcesParams,
        FlextMeltanoModelsSources,
        FlextMeltanoModelsInstances,
        FlextMeltanoModelsInstancesData,
        FlextMeltanoModelsSinger,
        FlextMeltanoModelsSingerSdk,
        FlextMeltanoModelsSingerCatalog,
        FlextMeltanoModelsPayloadsData,
        FlextMeltanoModelsContext,
        FlextMeltanoModelsDiscovery,
        FlextMeltanoModelsProjects,
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
