"""State Application Service - NEW SEMANTIC ARCHITECTURE (STUB).

🚨 DEPRECATION WARNING: Direct imports from this file are deprecated.

❌ OLD: from flext_meltano.application.services.state_service import MeltanoStateService
✅ NEW: from flext_meltano import StateService

This is a placeholder stub for MeltanoStateService to resolve import errors.
"""

from __future__ import annotations

import warnings
from typing import Any

# 🚨 ARCHITECTURAL COMPLIANCE: Using local DI container imports
from flext_meltano.infrastructure.di_container import AbstractService


# Initialize types via DI container
class MeltanoStateService(AbstractService):
    """State application service placeholder."""

    def __init__(self) -> None:
        """Initialize state service."""

    def validate_invariants(self) -> bool:
        """Validate service invariants."""
        # State service is stateless - always valid
        return True


# Deprecation warning for direct imports
def __getattr__(name: str) -> Any:
    """Handle direct imports with deprecation warning."""
    if name == "MeltanoStateService":
        warnings.warn(
            "🚨 DEPRECATED: Importing MeltanoStateService from 'flext_meltano.application.services.state_service' is deprecated.\n"
            "✅ Use: from flext_meltano import StateService\n"
            "📖 This import will be removed in version 0.8.0.\n"
            "📚 Migration guide: https://docs.flext.dev/migration/meltano",
            DeprecationWarning,
            stacklevel=2,
        )
        return MeltanoStateService
    msg = f"module 'flext_meltano.application.services.state_service' has no attribute '{name}'"
    raise AttributeError(
        msg,
    )
