# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._models.base import FlextMeltanoModelsBase
    from flext_meltano._models.cli_inputs import FlextMeltanoModelsCliInputs
    from flext_meltano._models.cli_params import FlextMeltanoModelsCliParams
    from flext_meltano._models.config import FlextMeltanoModelsConfig
    from flext_meltano._models.context import FlextMeltanoModelsContext
    from flext_meltano._models.core import FlextMeltanoModelsCore
    from flext_meltano._models.discovery import FlextMeltanoModelsDiscovery
    from flext_meltano._models.instances import FlextMeltanoModelsInstances
    from flext_meltano._models.instances_data import FlextMeltanoModelsInstancesData
    from flext_meltano._models.logging_config import FlextMeltanoModelsLogging
    from flext_meltano._models.payloads import FlextMeltanoModelsPayloads
    from flext_meltano._models.payloads_data import FlextMeltanoModelsPayloadsData
    from flext_meltano._models.projects import FlextMeltanoModelsProjects
    from flext_meltano._models.projects_plugin import FlextMeltanoModelsProjectsPlugin
    from flext_meltano._models.results import FlextMeltanoModelsResults
    from flext_meltano._models.results_dbt import FlextMeltanoModelsResultsDbt
    from flext_meltano._models.results_pipeline import FlextMeltanoModelsResultsPipeline
    from flext_meltano._models.singer import FlextMeltanoModelsSinger
    from flext_meltano._models.singer_catalog import FlextMeltanoModelsSingerCatalog
    from flext_meltano._models.singer_sdk import FlextMeltanoModelsSingerSdk
    from flext_meltano._models.sources import FlextMeltanoModelsSources
    from flext_meltano._models.sources_params import FlextMeltanoModelsSourcesParams
    from flext_meltano._models.transformations import FlextMeltanoModelsTransformations


__all__: tuple[str, ...] = (
    "FlextMeltanoModelsBase",
    "FlextMeltanoModelsCliInputs",
    "FlextMeltanoModelsCliParams",
    "FlextMeltanoModelsConfig",
    "FlextMeltanoModelsContext",
    "FlextMeltanoModelsCore",
    "FlextMeltanoModelsDiscovery",
    "FlextMeltanoModelsInstances",
    "FlextMeltanoModelsInstancesData",
    "FlextMeltanoModelsLogging",
    "FlextMeltanoModelsPayloads",
    "FlextMeltanoModelsPayloadsData",
    "FlextMeltanoModelsProjects",
    "FlextMeltanoModelsProjectsPlugin",
    "FlextMeltanoModelsResults",
    "FlextMeltanoModelsResultsDbt",
    "FlextMeltanoModelsResultsPipeline",
    "FlextMeltanoModelsSinger",
    "FlextMeltanoModelsSingerCatalog",
    "FlextMeltanoModelsSingerSdk",
    "FlextMeltanoModelsSources",
    "FlextMeltanoModelsSourcesParams",
    "FlextMeltanoModelsTransformations",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextMeltanoModelsBase": ".base",
        "FlextMeltanoModelsCliInputs": ".cli_inputs",
        "FlextMeltanoModelsCliParams": ".cli_params",
        "FlextMeltanoModelsConfig": ".config",
        "FlextMeltanoModelsContext": ".context",
        "FlextMeltanoModelsCore": ".core",
        "FlextMeltanoModelsDiscovery": ".discovery",
        "FlextMeltanoModelsInstances": ".instances",
        "FlextMeltanoModelsInstancesData": ".instances_data",
        "FlextMeltanoModelsLogging": ".logging_config",
        "FlextMeltanoModelsPayloads": ".payloads",
        "FlextMeltanoModelsPayloadsData": ".payloads_data",
        "FlextMeltanoModelsProjects": ".projects",
        "FlextMeltanoModelsProjectsPlugin": ".projects_plugin",
        "FlextMeltanoModelsResults": ".results",
        "FlextMeltanoModelsResultsDbt": ".results_dbt",
        "FlextMeltanoModelsResultsPipeline": ".results_pipeline",
        "FlextMeltanoModelsSinger": ".singer",
        "FlextMeltanoModelsSingerCatalog": ".singer_catalog",
        "FlextMeltanoModelsSingerSdk": ".singer_sdk",
        "FlextMeltanoModelsSources": ".sources",
        "FlextMeltanoModelsSourcesParams": ".sources_params",
        "FlextMeltanoModelsTransformations": ".transformations",
    }),
    public_exports=__all__,
)
