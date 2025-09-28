"""FLEXT Meltano Protocols - All protocol definitions for the domain.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult, FlextTypes, T_co

# Type aliases for protocol type safety
ConfigDict = FlextTypes.Core.ConfigDict
JsonValue = FlextTypes.Core.JsonValue
JsonObject = FlextTypes.Core.JsonObject


class FlextMeltanoProtocols(FlextProtocols):
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
    class SingerTapProtocol(FlextProtocols.Domain.Service, Protocol):
        """Singer Tap protocol extending Domain.Service for ELT operations."""

        def discover(self: object) -> FlextResult[JsonObject]:
            """Discover catalog with FlextResult."""
            ...

        def sync(self, catalog: JsonObject) -> FlextResult[JsonValue]:
            """Sync data from source with FlextResult."""
            ...

        def execute(self: object) -> FlextResult[object]:
            """Execute the tap extraction (implements Domain.Service)."""
            ...

    @runtime_checkable
    class SingerTargetProtocol(FlextProtocols.Domain.Service, Protocol):
        """Singer Target protocol extending Domain.Service for ELT operations."""

        def handle_record(self, record: JsonObject) -> FlextResult[JsonValue]:
            """Handle a single record with FlextResult."""
            ...

        def handle_batch(self, records: list[JsonObject]) -> FlextResult[JsonValue]:
            """Handle a batch of records with FlextResult."""
            ...

        def execute(self: object) -> FlextResult[object]:
            """Execute the target loading (implements Domain.Service)."""
            ...

    @runtime_checkable
    class DbtRunnerProtocol(FlextProtocols.Domain.Service, Protocol):
        """DBT Runner protocol extending Domain.Service for ELT operations."""

        def run(self, models: list[str]) -> FlextResult[JsonObject]:
            """Run DBT models with FlextResult."""
            ...

        def test(self, models: list[str]) -> FlextResult[JsonObject]:
            """Test DBT models with FlextResult."""
            ...

        def execute(self: object) -> FlextResult[object]:
            """Execute DBT transformations (implements Domain.Service)."""
            ...

    @runtime_checkable
    class ServiceCallProtocol(FlextProtocols.Domain.Service, Protocol):
        """Service call protocol extending Domain.Service."""

        def call(self, operation: str, payload: JsonValue) -> FlextResult[JsonValue]:
            """Execute service call with FlextResult."""
            ...

        def execute(self: object) -> FlextResult[object]:
            """Execute service operation (implements Domain.Service)."""
            ...


__all__ = [
    "FlextMeltanoProtocols",
]
