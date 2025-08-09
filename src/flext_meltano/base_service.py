"""Base services for flext-meltano.

This module centralizes service base classes that were previously spread in `base.py`.
Concrete implementations should live in dedicated modules and extend these bases.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, cast

from flext_core import FlextResult, get_logger

if TYPE_CHECKING:
    from .config import FlextMeltanoConfig


class FlextMeltanoBaseService:
    """Base service using flext-core patterns."""

    def __init__(self, config: FlextMeltanoConfig) -> None:
        self.config = config
        self._initialized = False
        self.logger = get_logger(self.__class__.__name__)

    def initialize(self) -> FlextResult[bool]:
        """Initialize the service after validating state."""
        try:
            validation_result = self.validate_service()
            if not validation_result.success:
                return FlextResult.fail(validation_result.error or "Validation failed")
            self._initialized = True
            return FlextResult.ok(data=True)
        except Exception as e:
            return FlextResult.fail(f"Service initialization failed: {e}")

    def validate_service(self) -> FlextResult[bool]:  # To be overridden
        """Validate concrete service requirements."""
        return FlextResult.ok(data=True)

    def get_health_status(self) -> FlextResult[dict[str, object]]:  # To be overridden
        """Return health information for monitoring."""
        return FlextResult.ok({"initialized": self._initialized})


__all__ = ["FlextMeltanoBaseService"]
