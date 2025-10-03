"""FLEXT Meltano Protocols - All protocol definitions for the domain.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult, FlextTypes, T_co

# Type aliases for protocol type safety
ConfigDict = FlextTypes.ConfigDict
JsonValue = FlextTypes.JsonValue
JsonObject = FlextTypes.JsonValue


class FlextMeltanoProtocols:
    """Unified Meltano protocols following FLEXT domain extension pattern.

    This class consolidates Meltano ELT pipeline protocols while explicitly
    re-exporting foundation protocols for backward compatibility and clean access.

    Architecture:
        - RE-EXPORTS: Foundation protocols from flext-core for unified access
        - EXTENDS: Meltano/Singer/DBT-specific protocols in Meltano namespace
        - MAINTAINS: Zero breaking changes through explicit re-export pattern

    Usage:
        from flext_meltano.protocols import FlextMeltanoProtocols

        # Foundation access (re-exported)
        FlextMeltanoProtocols.Foundation.ResultProtocol

        # Meltano ELT-specific access
        FlextMeltanoProtocols.Meltano.TapProtocol
    """

    # =========================================================================
    # FOUNDATION PROTOCOL RE-EXPORTS (from flext-core)
    # =========================================================================
    # Explicitly re-export foundation protocols for unified access.
    # This maintains backward compatibility while providing clean namespace access.

    Foundation = FlextProtocols.Foundation
    Domain = FlextProtocols.Domain
    Application = FlextProtocols.Application
    Infrastructure = FlextProtocols.Infrastructure
    Extensions = FlextProtocols.Extensions
    Commands = FlextProtocols.Commands

    # =========================================================================
    # MELTANO ELT-SPECIFIC PROTOCOLS
    # =========================================================================
    # Domain-specific protocols for Meltano, Singer, and DBT operations.

    class Meltano:
        """Meltano ELT domain-specific protocols.

        Provides protocols for Meltano plugins, Singer taps/targets/streams,
        DBT runners, and service operations.
        """

        @runtime_checkable
        class PluginProtocol(Protocol[T_co]):
            """Meltano plugin interface with covariant return type."""

            def get_config(self: object) -> ConfigDict:
                """Get plugin configuration."""
                # pragma: no cover

            def validate_config(self, config: ConfigDict) -> bool:
                """Validate plugin configuration."""
                # pragma: no cover

            def execute(self, *args: JsonValue) -> T_co:
                """Execute plugin with given arguments."""
                # pragma: no cover

        @runtime_checkable
        class StreamProtocol(Protocol):
            """Singer stream interface with type safety."""

            name: str
            tap_stream_id: str
            schema: JsonObject

            def sync_records(self: object) -> JsonValue:
                """Sync records from the stream."""

            def get_records(self: object) -> JsonValue:
                """Get records from the stream."""

        @runtime_checkable
        class TapProtocol(FlextProtocols.Domain.Service, Protocol):
            """Singer Tap protocol extending Domain.Service for ELT operations."""

            def discover(self: object) -> FlextResult[JsonObject]:
                """Discover catalog with FlextResult."""

            def sync(self, catalog: JsonObject) -> FlextResult[JsonValue]:
                """Sync data from source with FlextResult."""

            def execute(self: object) -> FlextResult[object]:
                """Execute the tap extraction (implements Domain.Service)."""

        @runtime_checkable
        class TargetProtocol(FlextProtocols.Domain.Service, Protocol):
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

            def run(self, models: FlextTypes.StringList) -> FlextResult[JsonObject]:
                """Run DBT models with FlextResult."""
                ...

            def test(self, models: FlextTypes.StringList) -> FlextResult[JsonObject]:
                """Test DBT models with FlextResult."""
                ...

            def execute(self: object) -> FlextResult[object]:
                """Execute DBT transformations (implements Domain.Service)."""
                ...

        @runtime_checkable
        class ServiceCallProtocol(FlextProtocols.Domain.Service, Protocol):
            """Service call protocol extending Domain.Service."""

            def call(
                self, operation: str, payload: JsonValue
            ) -> FlextResult[JsonValue]:
                """Execute service call with FlextResult."""
                ...

            def execute(self: object) -> FlextResult[object]:
                """Execute service operation (implements Domain.Service)."""
                ...

    # =========================================================================
    # BACKWARD COMPATIBILITY ALIASES
    # =========================================================================
    # Maintain existing attribute names for zero breaking changes.

    MeltanoPluginProtocol = Meltano.PluginProtocol
    SingerStreamProtocol = Meltano.StreamProtocol
    SingerTapProtocol = Meltano.TapProtocol
    SingerTargetProtocol = Meltano.TargetProtocol
    DbtRunnerProtocol = Meltano.DbtRunnerProtocol
    ServiceCallProtocol = Meltano.ServiceCallProtocol


__all__ = [
    "FlextMeltanoProtocols",
]
