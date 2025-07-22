"""Plugin Application Service - NEW SEMANTIC ARCHITECTURE (STUB).

This is a placeholder stub for MeltanoPluginService to resolve import errors.
"""

from __future__ import annotations

from flext_core.foundation import AbstractService


class MeltanoPluginService(AbstractService):
    """Plugin application service placeholder."""

    def __init__(self) -> None:
        """Initialize plugin service."""

    def validate_invariants(self) -> bool:
        """Validate service invariants."""
        # Plugin service is stateless - always valid
        return True
