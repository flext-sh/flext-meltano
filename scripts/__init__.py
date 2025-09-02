"""FLEXT Meltano Scripts - Utility scripts for development and operations.

This package contains utility scripts for the FLEXT Meltano project following
strict type safety and FlextMeltano[Module] class patterns.

All scripts must:
- Use FlextResult[T] for error handling
- Follow FlextMeltano[Module] class patterns
- Have 100% type safety (MyPy strict, PyRight, Ruff)
- Zero ignore hints or Any types

Scripts:
    FlextMeltanoScripts.DevelopmentTools: Development utilities
    FlextMeltanoScripts.ProductionTools: Production utilities
    FlextMeltanoScripts.BridgeTools: Go-Python bridge utilities
"""

from __future__ import annotations

# =============================================================================
# PUBLIC API EXPORTS - Class-based only
# =============================================================================

__all__ = [
    # Will be populated when script modules are added
]
