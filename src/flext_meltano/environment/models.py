"""FLEXT Meltano environment models."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class FlextMeltanoEnvironmentType(Enum):
    """Environment types for Meltano projects."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


# Alias for backward compatibility
EnvironmentType = FlextMeltanoEnvironmentType


class FlextMeltanoEnvironment(BaseModel):
    """FLEXT Meltano environment configuration."""

    name: str = Field(..., description="Environment name")
    type: FlextMeltanoEnvironmentType = Field(..., description="Environment type")
    config: dict[str, Any] = Field(
        default_factory=dict, description="Environment config",
    )
    variables: dict[str, str] = Field(
        default_factory=dict, description="Environment variables",
    )
    enabled: bool = Field(default=True, description="Whether environment is enabled")

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
        validate_assignment = True
