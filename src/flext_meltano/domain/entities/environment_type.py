"""Environment Type Domain Value Object - NEW SEMANTIC ARCHITECTURE (STUB).

This is a placeholder stub for EnvironmentType to resolve import errors.
"""

from __future__ import annotations

from enum import StrEnum


class FlextMeltanoEnvironmentType(StrEnum):
    """Environment type enumeration."""

    DEVELOPMENT = "dev"
    STAGING = "staging"
    PRODUCTION = "prod"
    TEST = "test"

    # Aliases for backward compatibility
    @classmethod
    def _missing_(cls, value: object) -> FlextMeltanoEnvironmentType | None:
        """Handle legacy values."""
        if value == "dev":
            return cls.DEVELOPMENT
        if value == "prod":
            return cls.PRODUCTION
        return None
