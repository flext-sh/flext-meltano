"""FLEXT Meltano Scripts - Utility scripts for development and operations.

This package contains utility scripts for the FLEXT Meltano project following
strict type safety and FlextMeltano[Module] class patterns.

All scripts must:
- Use FlextResult[T] for error handling
- Follow FlextMeltano[Module] class patterns
- Have 100% type safety (MyPy strict, PyRight, Ruff)
- Zero ignore hints or object types

Scripts:
    FlextMeltanoScripts.DevelopmentTools: Development utilities
    FlextMeltanoScripts.ProductionTools: Production utilities
    FlextMeltanoScripts.BridgeTools: Go-Python bridge utilities
"""

from __future__ import annotations

from flext_core import FlextTypes

__all__: FlextTypes.Core.StringList = [
    # Will be populated when script modules are added
]
