# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_meltano/_protocols/discovery
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_meltano import t


class FlextMeltanoProtocolsDiscovery:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class PluginDiscoverySource(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        default_variant: str
        variants: t.FlatContainerMapping
        logo_url: str
        description: str

    @runtime_checkable
    class PluginDiscoveryItem(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        name: t.NonEmptyStr
        type: t.NonEmptyStr
        default_variant: str
        variants: str
        logo_url: str
        description: str

    @runtime_checkable
    class PluginDiscoveryCatalog(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def plugins(
            self,
        ) -> Mapping[str, FlextMeltanoProtocolsDiscovery.PluginDiscoverySource]:
            """Discovered plugins catalog."""
            ...


__all__: list[str] = [
    "FlextMeltanoProtocolsDiscovery",
]
