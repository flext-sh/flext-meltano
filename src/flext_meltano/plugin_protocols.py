"""Meltano Plugin Protocols - Single unified class following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextCore


class FlextMeltanoPluginProtocols:
    """Single unified class for all Meltano plugin protocols following FLEXT standards.

    Consolidates all plugin types and service protocols into one unified class
    per FLEXT architectural requirements. Eliminates multiple classes per module.

    All protocol types are accessed through this single class - NO ALIASES.
    """

    # Core plugin types (JSON-based for external Meltano plugins)
    TapPlugin = FlextCore.Types.JsonValue
    TargetPlugin = FlextCore.Types.JsonValue
    DbtPlugin = FlextCore.Types.JsonValue

    # Service protocols (JSON-based for service integration)
    TapServiceProtocol = FlextCore.Types.JsonValue
    TargetServiceProtocol = FlextCore.Types.JsonValue
    DbtServiceProtocol = FlextCore.Types.JsonValue


__all__ = [
    "FlextMeltanoPluginProtocols",  # Main unified class - NO ALIASES
]
