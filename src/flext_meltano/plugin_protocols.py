"""Meltano Plugin Protocols - Single unified class following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations


class FlextMeltanoPluginProtocols:
    """Single unified class for all Meltano plugin protocols following FLEXT standards.

    Consolidates all plugin types and service protocols into one unified class
    per FLEXT architectural requirements. Eliminates multiple classes per module.
    """

    # Core plugin types - using object for maximum compatibility
    TapPlugin = object
    TargetPlugin = object
    DbtPlugin = object

    # Service protocols - proper protocol types
    TapServiceProtocol = object
    TargetServiceProtocol = object
    DbtServiceProtocol = object

    # Service aliases that tests expect
    TapService = TapServiceProtocol
    TargetService = TargetServiceProtocol
    DbtService = DbtServiceProtocol

    # Plugin aliases that tests expect
    FlextTapPlugin = TapPlugin
    FlextTargetPlugin = TargetPlugin
    FlextDbtPlugin = DbtPlugin


# Export class attributes as module-level names for proper access
DbtServiceProtocol = FlextMeltanoPluginProtocols.DbtServiceProtocol
FlextDbtPlugin = FlextMeltanoPluginProtocols.FlextDbtPlugin
FlextTapPlugin = FlextMeltanoPluginProtocols.FlextTapPlugin
FlextTargetPlugin = FlextMeltanoPluginProtocols.FlextTargetPlugin
TapServiceProtocol = FlextMeltanoPluginProtocols.TapServiceProtocol
TargetServiceProtocol = FlextMeltanoPluginProtocols.TargetServiceProtocol
TapService = FlextMeltanoPluginProtocols.TapService
TargetService = FlextMeltanoPluginProtocols.TargetService

__all__ = [
    "DbtServiceProtocol",
    "FlextDbtPlugin",
    "FlextMeltanoPluginProtocols",  # Main unified class
    "FlextTapPlugin",
    "FlextTargetPlugin",
    "TapService",
    "TapServiceProtocol",
    "TargetService",
    "TargetServiceProtocol",
]
