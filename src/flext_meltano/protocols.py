"""FLEXT Meltano Protocols - All protocol definitions for the domain.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_core import FlextTypes, T_co

# Type aliases for protocol type safety
ConfigDict = FlextTypes.Core.ConfigDict
JsonValue = FlextTypes.Core.JsonValue
JsonObject = FlextTypes.Core.JsonObject


class FlextMeltanoProtocols:
    """UNIFIED Meltano Protocols - SINGLE RESPONSIBILITY PATTERN.

    Contains ALL protocol definitions for the Meltano domain.
    Follows flext-core standards with proper protocol organization.
    """

    @runtime_checkable
    class MeltanoPluginProtocol(Protocol[T_co]):
        """Meltano plugin interface with covariant return type."""

        def get_config(self: object) -> ConfigDict:
            """Get plugin configuration."""
            ...  # pragma: no cover

        def validate_config(self, config: ConfigDict) -> bool:
            """Validate plugin configuration."""
            ...  # pragma: no cover

        def execute(self, *args: JsonValue) -> T_co:
            """Execute plugin with given arguments."""
            ...  # pragma: no cover

    @runtime_checkable
    class SingerStreamProtocol(Protocol):
        """Singer stream interface with type safety."""

        name: str
        tap_stream_id: str
        schema: JsonObject

        def sync_records(self: object) -> JsonValue:
            """Sync records from the stream."""
            ...

        def get_records(self: object) -> JsonValue:
            """Get records from the stream."""
            ...

    @runtime_checkable
    class SingerTapProtocol(Protocol):
        """Singer Tap protocol for type safety."""

        def discover(self: object) -> JsonObject:
            """Discover catalog."""
            ...

        def sync(self, catalog: JsonObject) -> JsonValue:
            """Sync data from source."""
            ...

    @runtime_checkable
    class SingerTargetProtocol(Protocol):
        """Singer Target protocol for type safety."""

        def handle_record(self, record: JsonObject) -> JsonValue:
            """Handle a single record."""
            ...

        def handle_batch(self, records: list[JsonObject]) -> JsonValue:
            """Handle a batch of records."""
            ...

    @runtime_checkable
    class DbtRunnerProtocol(Protocol):
        """DBT Runner protocol for type safety."""

        def run(self, models: list[str]) -> JsonObject:
            """Run DBT models."""
            ...

        def test(self, models: list[str]) -> JsonObject:
            """Test DBT models."""
            ...

    @runtime_checkable
    class ServiceCallProtocol(Protocol):
        """Service call protocol for type safety."""

        def call(self, operation: str, payload: JsonValue) -> JsonValue:
            """Execute service call."""
            ...


__all__ = [
    "FlextMeltanoProtocols",
]
