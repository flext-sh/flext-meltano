"""Plugin Application Service - NEW SEMANTIC ARCHITECTURE (STUB).

This is a placeholder stub for MeltanoPluginService to resolve import errors.
"""

from __future__ import annotations

# 🚨 ARCHITECTURAL COMPLIANCE: Using local DI container imports
from flext_meltano.infrastructure.di_container import AbstractService


# Initialize types via DI container
class MeltanoPluginService(AbstractService):
    """Plugin application service placeholder."""

    def __init__(self) -> None:
        """Initialize plugin service."""

    def validate_invariants(self) -> bool:
        """Validate service invariants."""
        # Plugin service is stateless - always valid
        return True
