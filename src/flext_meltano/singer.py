"""FLEXT Meltano Singer - Singer SDK integration with flext-core patterns.

Provides Singer SDK classes integrated with flext-core patterns for enterprise use.
"""

from __future__ import annotations

# Re-export Singer SDK classes from the main package
from flext_meltano import FlextMeltanoTapService as FlextMeltanoTap, FlextMeltanoTargetService as FlextMeltanoTarget

# Legacy compatibility
__all__ = [
    "FlextMeltanoTap",
    "FlextMeltanoTarget",
]
