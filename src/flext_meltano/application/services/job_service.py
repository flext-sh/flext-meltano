"""Job Application Service - NEW SEMANTIC ARCHITECTURE (STUB).

This is a placeholder stub for MeltanoJobService to resolve import errors.
"""

from __future__ import annotations

from flext_core.foundation import AbstractService


class MeltanoJobService(AbstractService):
    """Job application service placeholder."""

    def __init__(self) -> None:
        """Initialize job service."""

    def validate_invariants(self) -> bool:
        """Validate service invariants."""
        # Job service is stateless - always valid
        return True
