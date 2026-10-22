# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
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


__all__: tuple[str, ...] = (
    "FlextMeltanoModelsBase",
    "FlextMeltanoModelsCliInputs",
    "FlextMeltanoModelsConfig",
    "FlextMeltanoModelsCore",
    "FlextMeltanoModelsDiscovery",
    "FlextMeltanoModelsInstances",
    "FlextMeltanoModelsPayloadsData",
    "FlextMeltanoModelsResultsDbt",
    "FlextMeltanoModelsSinger",
    "FlextMeltanoModelsSingerCatalog",
    "FlextMeltanoModelsSingerSdk",
    "FlextMeltanoModelsSources",
    "FlextMeltanoModelsSourcesParams",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextMeltanoModelsBase": ".base",
        "FlextMeltanoModelsCliInputs": ".cli_inputs",
        "FlextMeltanoModelsConfig": ".config",
        "FlextMeltanoModelsCore": ".core",
        "FlextMeltanoModelsDiscovery": ".discovery",
        "FlextMeltanoModelsInstances": ".instances",
        "FlextMeltanoModelsPayloadsData": ".payloads_data",
        "FlextMeltanoModelsResultsDbt": ".results_dbt",
        "FlextMeltanoModelsSinger": ".singer",
        "FlextMeltanoModelsSingerCatalog": ".singer_catalog",
        "FlextMeltanoModelsSingerSdk": ".singer_sdk",
        "FlextMeltanoModelsSources": ".sources",
        "FlextMeltanoModelsSourcesParams": ".sources_params",
    }),
    public_exports=__all__,
)
