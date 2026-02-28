"""Meltano Plugin Protocols - Single unified class following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_meltano import t


class FlextMeltanoPluginProtocols:
    """Single unified class for all Meltano plugin protocols following FLEXT standards.

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
    "FlextMeltanoPluginProtocols",  # Main unified class - NO ALIASES
]
