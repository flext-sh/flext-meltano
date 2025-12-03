"""Singer Protocol Definitions for FLEXT Meltano.

This module provides unified protocol definitions for Singer protocol
components (taps, targets) following flext-core and Singer specifications.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol

from flext_core import t


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
        state: dict[str, object]

        def get_records(self, stream_name: str) -> list[dict[str, object]]:
            """Get records for a specific stream.

            Args:
            stream_name: Name of the stream to extract records from

            Returns:
            List of record dictionaries for the stream

            """
            ...

        def get_state(self) -> dict[str, object]:
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


class FlextMeltanoPluginProtocols:
    """Unified Meltano plugin protocols following FLEXT standards.

    Consolidates all plugin types and service protocols into one unified class
    per FLEXT architectural requirements. Eliminates multiple classes per module.

    All protocol types are accessed through this single class - NO ALIASES.
    """

    # Core plugin types (JSON-based for external Meltano plugins)
    TapPlugin = t.JsonValue
    TargetPlugin = t.JsonValue
    DbtPlugin = t.JsonValue

    # Service protocols (JSON-based for service integration)
    TapServiceProtocol = t.JsonValue
    TargetServiceProtocol = t.JsonValue
    DbtServiceProtocol = t.JsonValue


__all__ = [
    "FlextMeltanoPluginProtocols",
    "FlextMeltanoSingerProtocols",
]
