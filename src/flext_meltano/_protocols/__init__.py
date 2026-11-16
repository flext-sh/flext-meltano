# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._protocols.base import FlextMeltanoProtocolsBase
    from flext_meltano._protocols.cli_inputs import FlextMeltanoProtocolsCliInputs
    from flext_meltano._protocols.config import FlextMeltanoProtocolsConfig
    from flext_meltano._protocols.core import FlextMeltanoProtocolsCore
    from flext_meltano._protocols.discovery import FlextMeltanoProtocolsDiscovery
    from flext_meltano._protocols.instances import FlextMeltanoProtocolsInstances
    from flext_meltano._protocols.payloads_data import FlextMeltanoProtocolsPayloadsData
    from flext_meltano._protocols.results_dbt import FlextMeltanoProtocolsResultsDbt
    from flext_meltano._protocols.singer import FlextMeltanoProtocolsSinger
    from flext_meltano._protocols.singer_catalog import (
        FlextMeltanoProtocolsSingerCatalog,
    )
    from flext_meltano._protocols.sources import FlextMeltanoProtocolsSources
    from flext_meltano._protocols.sources_params import (
        FlextMeltanoProtocolsSourcesParams,
    )


__all__: tuple[str, ...] = (
    "FlextMeltanoProtocolsBase",
    "FlextMeltanoProtocolsCliInputs",
    "FlextMeltanoProtocolsConfig",
    "FlextMeltanoProtocolsCore",
    "FlextMeltanoProtocolsDiscovery",
    "FlextMeltanoProtocolsInstances",
    "FlextMeltanoProtocolsPayloadsData",
    "FlextMeltanoProtocolsResultsDbt",
    "FlextMeltanoProtocolsSinger",
    "FlextMeltanoProtocolsSingerCatalog",
    "FlextMeltanoProtocolsSources",
    "FlextMeltanoProtocolsSourcesParams",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextMeltanoProtocolsBase": ".base",
        "FlextMeltanoProtocolsCliInputs": ".cli_inputs",
        "FlextMeltanoProtocolsConfig": ".config",
        "FlextMeltanoProtocolsCore": ".core",
        "FlextMeltanoProtocolsDiscovery": ".discovery",
        "FlextMeltanoProtocolsInstances": ".instances",
        "FlextMeltanoProtocolsPayloadsData": ".payloads_data",
        "FlextMeltanoProtocolsResultsDbt": ".results_dbt",
        "FlextMeltanoProtocolsSinger": ".singer",
        "FlextMeltanoProtocolsSingerCatalog": ".singer_catalog",
        "FlextMeltanoProtocolsSources": ".sources",
        "FlextMeltanoProtocolsSourcesParams": ".sources_params",
    },
    public_exports=__all__,
    deferred_members={
        "FlextMeltanoProtocolsBase": (
            "MeltanoExecutor",
            "DbtConnectionProfile",
        ),
        "FlextMeltanoProtocolsCliInputs": (
            "PipelineCreateInput",
            "PipelineRunInput",
            "PipelineNameInput",
            "PipelineListInput",
            "PluginListInput",
            "PluginInfoInput",
            "PluginInstallInput",
            "StatusShowInput",
            "StatusHealthInput",
            "DbtInput",
            "TapInput",
            "TargetInput",
            "VersionInput",
        ),
        "FlextMeltanoProtocolsConfig": ("MeltanoNamespace",),
        "FlextMeltanoProtocolsCore": ("StringListValue",),
        "FlextMeltanoProtocolsDiscovery": (
            "PluginDiscoverySource",
            "PluginDiscoveryItem",
            "PluginDiscoveryCatalog",
        ),
        "FlextMeltanoProtocolsInstances": (
            "StreamInfo",
            "TapInstance",
        ),
        "FlextMeltanoProtocolsPayloadsData": (
            "ConfigMappingPayload",
            "PathPayload",
        ),
        "FlextMeltanoProtocolsResultsDbt": ("CommandExecutionResult",),
        "FlextMeltanoProtocolsSinger": (
            "SingerTapInstance",
            "RecordFetcher",
            "SingerDrainSink",
            "SinkFactory",
            "SingerTargetHandler",
            "SingerSchemaMessage",
            "SingerRecordMessage",
            "SingerStateMessage",
            "SingerActivateVersionMessage",
            "StreamSpec",
            "TapSpec",
            "FetchRequest",
            "FetchResult",
        ),
        "FlextMeltanoProtocolsSingerCatalog": (
            "SingerCatalogMetadata",
            "SingerCatalogEntry",
            "SingerCatalog",
        ),
        "FlextMeltanoProtocolsSources": (
            "TapConfig",
            "TargetConfig",
        ),
        "FlextMeltanoProtocolsSourcesParams": ("StreamDefinition",),
    },
)
