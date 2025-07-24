"""Integration modules for Go-Meltano bridge.

This package contains integration modules for:
- Go language bindings (gopy)
- Bridge functionality for Go-Python Meltano operations
"""

from __future__ import annotations

from flext_meltano.integrations.bridge import FlextMeltanoBridge
from flext_meltano.integrations.gopy_integration import (
    FlextMeltanoGopyIntegration,
)

__all__ = [
    "FlextMeltanoBridge",
    "FlextMeltanoGopyIntegration",
]
