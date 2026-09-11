"""FLEXT pipeline models.

Provides Pydantic models for data pipeline operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import m

from ._models.cli_inputs import FlextMeltanoModelsCliInputs
from ._models.cli_params import FlextMeltanoModelsCliParams
from ._models.context import FlextMeltanoModelsContext
from ._models.core import FlextMeltanoModelsCore
from ._models.discovery import FlextMeltanoModelsDiscovery
from ._models.instances import FlextMeltanoModelsInstances
from ._models.instances_data import FlextMeltanoModelsInstancesData
from ._models.logging_config import FlextMeltanoModelsLogging
from ._models.payloads import FlextMeltanoModelsPayloads
from ._models.payloads_data import FlextMeltanoModelsPayloadsData
from ._models.projects import FlextMeltanoModelsProjects
from ._models.projects_plugin import FlextMeltanoModelsProjectsPlugin
from ._models.results import FlextMeltanoModelsResults
from ._models.results_dbt import FlextMeltanoModelsResultsDbt
from ._models.results_pipeline import FlextMeltanoModelsResultsPipeline
from ._models.singer import FlextMeltanoModelsSinger
from ._models.singer_catalog import FlextMeltanoModelsSingerCatalog
from ._models.singer_sdk import FlextMeltanoModelsSingerSdk
from ._models.sources import FlextMeltanoModelsSources
from ._models.sources_params import FlextMeltanoModelsSourcesParams
from ._models.transformations import FlextMeltanoModelsTransformations


class FlextMeltanoModels(m):
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
        FlextMeltanoModelsSingerCatalog,
        FlextMeltanoModelsSingerSdk,
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

__all__ = ["FlextMeltanoModels", "m"]
