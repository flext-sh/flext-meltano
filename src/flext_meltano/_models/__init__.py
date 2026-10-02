# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._models.base import FlextMeltanoModelsBase
    from flext_meltano._models.cli_inputs import FlextMeltanoModelsCliInputs
    from flext_meltano._models.cli_params import FlextMeltanoModelsCliParams
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

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("FlextMeltanoModelsBase",),
            ".cli_inputs": ("FlextMeltanoModelsCliInputs",),
            ".cli_params": ("FlextMeltanoModelsCliParams",),
            ".context": ("FlextMeltanoModelsContext",),
            ".core": ("FlextMeltanoModelsCore",),
            ".discovery": ("FlextMeltanoModelsDiscovery",),
            ".instances": ("FlextMeltanoModelsInstances",),
            ".instances_data": ("FlextMeltanoModelsInstancesData",),
            ".logging_config": ("FlextMeltanoModelsLogging",),
            ".payloads": ("FlextMeltanoModelsPayloads",),
            ".payloads_data": ("FlextMeltanoModelsPayloadsData",),
            ".projects": ("FlextMeltanoModelsProjects",),
            ".projects_plugin": ("FlextMeltanoModelsProjectsPlugin",),
            ".results": ("FlextMeltanoModelsResults",),
            ".results_dbt": ("FlextMeltanoModelsResultsDbt",),
            ".results_pipeline": ("FlextMeltanoModelsResultsPipeline",),
            ".singer": ("FlextMeltanoModelsSinger",),
            ".singer_catalog": ("FlextMeltanoModelsSingerCatalog",),
            ".singer_sdk": ("FlextMeltanoModelsSingerSdk",),
            ".sources": ("FlextMeltanoModelsSources",),
            ".sources_params": ("FlextMeltanoModelsSourcesParams",),
            ".transformations": ("FlextMeltanoModelsTransformations",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
