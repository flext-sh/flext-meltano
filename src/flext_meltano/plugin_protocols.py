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

    # Service protocols (equal to plugins for compatibility)
    TapServiceProtocol = TapPlugin
    TargetServiceProtocol = TargetPlugin
    DbtServiceProtocol = DbtPlugin

    # Additional compatibility aliases required by tests
    FlextTapPlugin = TapPlugin
    FlextTargetPlugin = TargetPlugin
    FlextDbtPlugin = DbtPlugin
    DbtService = DbtServiceProtocol

    # Backward compatibility properties (accessed via class)
    @classmethod
    def get_tap_plugin(cls) -> type:
        """Get tap plugin type."""
        return cls.TapPlugin

    @classmethod
    def get_target_plugin(cls) -> type:
        """Get target plugin type."""
        return cls.TargetPlugin

    @classmethod
    def get_dbt_plugin(cls) -> type:
        """Get dbt plugin type."""
        return cls.DbtPlugin

    @classmethod
    def get_tap_service_protocol(cls) -> type:
        """Get tap service protocol."""
        return cls.TapServiceProtocol

    @classmethod
    def get_target_service_protocol(cls) -> type:
        """Get target service protocol."""
        return cls.TargetServiceProtocol

    @classmethod
    def get_dbt_service_protocol(cls) -> type:
        """Get dbt service protocol."""
        return cls.DbtServiceProtocol


# Create single instance of unified class for module access
_protocols = FlextMeltanoPluginProtocols()

# Module-level aliases for backward compatibility - SIMPLIFIED
FlextTapPlugin = _protocols.TapPlugin
FlextTargetPlugin = _protocols.TargetPlugin
FlextDbtPlugin = _protocols.DbtPlugin
TapServiceProtocol = _protocols.TapServiceProtocol
TargetServiceProtocol = _protocols.TargetServiceProtocol
DbtServiceProtocol = _protocols.DbtServiceProtocol

__all__ = [
    "DbtServiceProtocol",
    "FlextDbtPlugin",              # Backward compatibility
    "FlextMeltanoPluginProtocols",  # Main unified class
    "FlextTapPlugin",              # Backward compatibility
    "FlextTargetPlugin",           # Backward compatibility
    "TapServiceProtocol",          # Service protocols
    "TargetServiceProtocol",
]
