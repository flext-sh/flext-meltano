"""Singer Protocol Definitions for FLEXT Meltano.

This module provides unified protocol definitions for Singer protocol
components (taps, targets) following flext-core and Singer specifications.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol

from flext_meltano import FlextMeltanoModels, FlextMeltanoTypes

# Import aliases
t = FlextMeltanoTypes
m = FlextMeltanoModels


class FlextMeltanoSingerProtocols:
    """Unified Singer protocols for Meltano ELT operations.

    This class consolidates all Singer protocol definitions into a single
    namespace following FLEXT 'one class per module' pattern.

    All protocol types are accessed through this single class with no aliases
    exposed at module level to maintain consistency with FLEXT standards.
    """

    class SingerTap(Protocol):
        """Singer Tap protocol definition.

        Defines the interface for Singer data extraction (tap) components
        that implement the Singer protocol for data source integration.
        """

        streams: list[str]
        name: str
        state: m.Meltano.SingerStateMessage

        def discover(self) -> m.Meltano.SingerCatalog:
            """Discover available streams and schemas.

            Returns:
            Singer catalog model

            """
            ...

        def sync(
            self,
            catalog: m.Meltano.SingerCatalog,
            state: m.Meltano.SingerStateMessage,
        ) -> None:
            """Synchronize data from source to stdout.

            Args:
            catalog: Singer catalog model
            state: Current state for incremental sync

            """
            ...

        def get_records(self, stream_name: str) -> list[m.Meltano.SingerRecordMessage]:
            """Get records for a specific stream.

            Args:
            stream_name: Name of the stream to extract records from

            Returns:
            List of Singer record messages for the stream

            """
            ...

        def get_state(self) -> m.Meltano.SingerStateMessage:
            """Get current state.

            Returns:
            Singer state message containing sync state

            """
            ...

    class SingerTarget(Protocol):
        """Singer Target protocol definition.

        Defines the interface for Singer data loading (target) components
        that implement the Singer protocol for data sink integration.
        """

        name: str
        config: m.Meltano.TargetConfig

        def consume(self, records: list[m.Meltano.SingerRecordMessage]) -> int:
            """Consume records batch.

            Args:
            records: Batch of records to consume

            Returns:
            Number of records consumed

            """
            ...


class FlextMeltanoPluginProtocols:
    """Unified Meltano plugin protocols following FLEXT standards.

    Consolidates all plugin types and service protocols into one unified class
    per FLEXT architectural requirements. Eliminates multiple classes per module.

    All protocol types are accessed through this single class - NO ALIASES.
    """

    # Core plugin types - use proper type aliases
    TapPlugin = t.Plugin.PluginDefinition
    TargetPlugin = t.Plugin.PluginDefinition
    DbtPlugin = t.Plugin.PluginDefinition

    # Service protocols - use proper configuration types
    TapServiceProtocol = t.Plugin.PluginConfiguration
    TargetServiceProtocol = t.Plugin.PluginConfiguration
    DbtServiceProtocol = t.Plugin.PluginConfiguration


__all__ = [
    "FlextMeltanoPluginProtocols",
    "FlextMeltanoSingerProtocols",
]
