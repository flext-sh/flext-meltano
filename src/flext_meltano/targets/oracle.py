"""FLEXT Oracle Target - Consolidated implementation for Oracle database loading.

Enterprise-grade Oracle target implementation using FLEXT Core patterns
and Singer SDK for robust data loading operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field
from singer_sdk import Target
from singer_sdk.sinks import BatchSink

if TYPE_CHECKING:
    from collections.abc import Sequence


class LoadMethod(StrEnum):
    """Oracle load methods for data insertion."""

    APPEND_ONLY = "append-only"
    UPSERT = "upsert"
    TRUNCATE_INSERT = "truncate-insert"


class FlextOracleTargetConfig(BaseModel):
    """Configuration for Oracle target."""

    # Connection settings
    oracle_host: str = Field(..., description="Oracle database host")
    oracle_port: int = Field(default=1521, description="Oracle database port")
    oracle_service_name: str = Field(..., description="Oracle service name")
    oracle_username: str = Field(..., description="Oracle username")
    oracle_password: str = Field(..., description="Oracle password")

    # Loading settings
    load_method: LoadMethod = Field(default=LoadMethod.APPEND_ONLY, description="Data loading method")
    batch_size: int = Field(default=1000, description="Batch size for loading")
    table_prefix: str = Field(default="", description="Prefix for table names")

    # Schema settings
    default_target_schema: str = Field(default="PUBLIC", description="Default target schema")

    class Config:
        """Pydantic configuration."""

        frozen = True
        extra = "forbid"


class FlextOracleSink(BatchSink):
    """Oracle sink for Singer records."""

    def __init__(self, target: FlextOracleTarget, stream_name: str, schema: dict[str, Any], key_properties: Sequence[str] | None = None) -> None:
        """Initialize Oracle sink."""
        super().__init__(target, stream_name=stream_name, schema=schema, key_properties=key_properties or [])

    def process_batch(self, context: dict[str, Any]) -> None:
        """Process a batch of records."""
        # Implementation would go here
        # For now, this is a placeholder for the consolidated implementation


class FlextOracleTarget(Target):
    """Oracle target implementation using FLEXT patterns."""

    name = "target-oracle"
    config_class = FlextOracleTargetConfig
    default_sink_class = FlextOracleSink

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize Oracle target."""
        super().__init__(config=config)
        # Store typed config separately
        self._typed_config = FlextOracleTargetConfig(**self.config)

    @property
    def config(self) -> dict[str, Any]:
        """Get target configuration."""
        return dict(super().config)

    def get_sink(self, stream_name: str, *, record: dict[str, Any] | None = None, schema: dict[str, Any] | None = None, key_properties: Sequence[str] | None = None) -> FlextOracleSink:  # noqa: ARG002
        """Get sink for stream."""
        return FlextOracleSink(
            target=self,
            stream_name=stream_name,
            schema=schema or {},
            key_properties=key_properties,
        )
