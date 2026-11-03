# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_meltano/_protocols/discovery
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_meltano import t


class FlextMeltanoProtocolsDiscovery:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class PluginDiscoverySource(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def default_variant(self) -> str:
            """Plugin default variant."""
            ...

        variants: t.FlatContainerMapping

        @property
        def logo_url(self) -> str:
            """Plugin logo URL."""
            ...

        @property
        def description(self) -> str:
            """Plugin description."""
            ...

    @runtime_checkable
    class PluginDiscoveryItem(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def name(self) -> t.NonEmptyStr:
            """Plugin name."""
            ...

        @property
        def type(self) -> t.NonEmptyStr:
            """Plugin type."""
            ...

        @property
        def default_variant(self) -> str:
            """Default plugin variant."""
            ...

        @property
        def variants(self) -> str:
            """Comma-separated variants."""
            ...

        @property
        def logo_url(self) -> str:
            """Plugin logo URL."""
            ...

        @property
        def description(self) -> str:
            """Plugin description."""
            ...

    @runtime_checkable
    class PluginDiscoveryCatalog(FlextCliProtocols.Model, Protocol):
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
