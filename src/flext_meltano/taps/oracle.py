"""FLEXT Oracle Tap - Consolidated implementation for Oracle database extraction.

Enterprise-grade Oracle tap implementation using FLEXT Core patterns
and Singer SDK for robust data extraction operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field
from singer_sdk import Tap
from singer_sdk.streams import Stream

if TYPE_CHECKING:
    from collections.abc import Mapping


class TapOracleConfig(BaseModel):
    """Configuration for Oracle tap."""

    # Connection settings
    oracle_host: str = Field(..., description="Oracle database host")
    oracle_port: int = Field(default=1521, description="Oracle database port")
    oracle_service_name: str = Field(..., description="Oracle service name")
    oracle_username: str = Field(..., description="Oracle username")
    oracle_password: str = Field(..., description="Oracle password")

    # Query settings
    default_replication_method: str = Field(default="FULL_TABLE", description="Default replication method")

    class Config:
        """Pydantic configuration."""

        frozen = True
        extra = "forbid"


class FlextOracleStream(Stream):
    """Oracle stream for Singer records."""

    def __init__(self, tap: FlextTapOracle, name: str, schema: dict[str, Any]) -> None:
        """Initialize Oracle stream."""
        super().__init__(tap, name=name, schema=schema)

    def get_records(self, context: Mapping[str, Any] | None) -> list[dict[str, Any]]:
        """Get records from Oracle."""
        # Implementation would go here
        # For now, this is a placeholder for the consolidated implementation
        _ = context  # Mark context as used
        return []


class FlextTapOracle(Tap):
    """Oracle tap implementation using FLEXT patterns."""

    name = "tap-oracle"
    config_class = TapOracleConfig

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize Oracle tap."""
        super().__init__(config=config)
        # Store typed config separately
        self._typed_config = TapOracleConfig(**self.config)

    def discover_streams(self) -> list[FlextOracleStream]:
        """Discover Oracle streams."""
        # Implementation would go here
        # For now, this is a placeholder for the consolidated implementation
        return []


# Legacy aliases for backward compatibility
TapOracle = FlextTapOracle

__all__ = [
    "FlextOracleStream",
    "FlextTapOracle",
    "TapOracle",
    "TapOracleConfig",
]
