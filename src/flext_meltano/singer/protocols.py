"""Singer Protocol Definitions for FLEXT Meltano.

This module provides unified protocol definitions for Singer protocol
components (taps, targets) following flext-core and Singer specifications.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol

from flext_core import FlextTypes

from flext_meltano.typings import FlextMeltanoTypes

# Import aliases - using meltano types for domain-specific definitions
t = FlextMeltanoTypes
t_core = FlextTypes


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
        state: t.Singer.TapConfig

        def discover(self) -> t.Singer.StreamCatalog:
            """Discover available streams and schemas.

            Returns:
            Stream catalog with schema definitions

            """
            ...

        def sync(
            self,
            catalog: t.Singer.StreamCatalog,
            state: t.Singer.TapConfig,
        ) -> None:
            """Synchronize data from source to stdout.

            Args:
            catalog: Stream catalog defining what to extract
            state: Current state for incremental sync

            """
            ...

        def get_records(self, stream_name: str) -> t.Singer.MessageBatch:
            """Get records for a specific stream.

            Args:
            stream_name: Name of the stream to extract records from

            Returns:
            List of record dictionaries for the stream

            """
            ...

        def get_state(self) -> t.Singer.TapConfig:
            """Get current state.

            Returns:
            Dictionary containing the current sync state

            """
            ...

    class SingerTarget(Protocol):
        """Singer Target protocol definition.

        Defines the interface for Singer data loading (target) components
        that implement the Singer protocol for data sink integration.
        """

        name: str
        config: t.Singer.TargetConfig

        def consume(self, records: t.Singer.MessageBatch) -> int:
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
