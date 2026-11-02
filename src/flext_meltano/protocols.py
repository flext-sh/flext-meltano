# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Meltano Protocols - All protocol definitions for the domain.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import p as flext_cli_p

from flext_meltano._protocols.base import FlextMeltanoProtocolsBase
from flext_meltano._protocols.cli_inputs import FlextMeltanoProtocolsCliInputs
from flext_meltano._protocols.config import FlextMeltanoProtocolsConfig
from flext_meltano._protocols.core import FlextMeltanoProtocolsCore
from flext_meltano._protocols.discovery import FlextMeltanoProtocolsDiscovery
from flext_meltano._protocols.instances import FlextMeltanoProtocolsInstances
from flext_meltano._protocols.payloads_data import FlextMeltanoProtocolsPayloadsData
from flext_meltano._protocols.results_dbt import FlextMeltanoProtocolsResultsDbt
from flext_meltano._protocols.singer import FlextMeltanoProtocolsSinger
from flext_meltano._protocols.singer_catalog import FlextMeltanoProtocolsSingerCatalog
from flext_meltano._protocols.sources import FlextMeltanoProtocolsSources
from flext_meltano._protocols.sources_params import FlextMeltanoProtocolsSourcesParams


class FlextMeltanoProtocols(flext_cli_p):
    """Unified Meltano protocols extending FlextCliProtocols."""

    class Meltano(
        FlextMeltanoProtocolsBase,
        FlextMeltanoProtocolsCliInputs,
        FlextMeltanoProtocolsConfig,
        FlextMeltanoProtocolsCore,
        FlextMeltanoProtocolsDiscovery,
        FlextMeltanoProtocolsInstances,
        FlextMeltanoProtocolsPayloadsData,
        FlextMeltanoProtocolsResultsDbt,
        FlextMeltanoProtocolsSinger,
        FlextMeltanoProtocolsSingerCatalog,
        FlextMeltanoProtocolsSources,
        FlextMeltanoProtocolsSourcesParams,
    ):
        """Meltano ELT domain-specific protocols."""


p = FlextMeltanoProtocols
__all__: list[str] = ["FlextMeltanoProtocols", "p"]
