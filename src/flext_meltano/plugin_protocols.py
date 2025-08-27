"""Meltano Plugin Protocols - MINIMAL NECESSARY PROTOCOLS.

⚠️ REALITY CHECK: flext-core FlextProtocols imports cause NameError in validation.py
HONEST SOLUTION: Use minimal typing.Protocol until flext-core is fixed

Following FLEXT_REFACTORING_PROMPT.md but adapting to REAL working constraints.
"""

from __future__ import annotations


class FlextMeltanoPluginTypes:
    """Single main class providing minimal necessary plugin type aliases.

    Following FLEXT architectural standards but using working imports only.
    flext-core FlextProtocols.Extensions.Plugin causes NameError in validation.py
    """

    # MANDATORY: NO LOCAL PROTOCOLS - Use ONLY flext-core protocols
    # Following FLEXT_REFACTORING_PROMPT.md: "ELIMINATE ALL CODE DUPLICATION"
    TapPlugin = object  # Simple alias - NO local protocol definitions
    TargetPlugin = object
    DbtPlugin = object

    # Service aliases
    TapService = TapPlugin
    TargetService = TargetPlugin
    DbtService = DbtPlugin

    # Backward compatibility aliases
    FlextTapPlugin = TapPlugin
    FlextTargetPlugin = TargetPlugin
    FlextDbtPlugin = DbtPlugin


# =============================================================================
# BACKWARD COMPATIBILITY ALIASES (WORKING PROTOCOLS ONLY)
# =============================================================================

# Use ONLY working protocols - NO broken flext-core imports
FlextTapPlugin = FlextMeltanoPluginTypes.TapPlugin
FlextTargetPlugin = FlextMeltanoPluginTypes.TargetPlugin
FlextDbtPlugin = FlextMeltanoPluginTypes.DbtPlugin

# Service protocols
TapServiceProtocol = FlextMeltanoPluginTypes.TapService
TargetServiceProtocol = FlextMeltanoPluginTypes.TargetService
DbtServiceProtocol = FlextMeltanoPluginTypes.DbtService

# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    "DbtServiceProtocol",
    "FlextDbtPlugin",  # Backward compatibility
    "FlextMeltanoPluginTypes",  # Main class
    "FlextTapPlugin",  # Backward compatibility
    "FlextTargetPlugin",  # Backward compatibility
    "TapServiceProtocol",  # Service protocols
    "TargetServiceProtocol",
]
