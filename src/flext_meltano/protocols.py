"""FLEXT Meltano Protocols - All protocol definitions for the domain.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

from flext_core import FlextCore

T_co = TypeVar("T_co", covariant=True)


class FlextMeltanoProtocols(FlextCore.Protocols):
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

            # Plugin attributes (matching actual Meltano plugin objects)
            name: str
            default_variant: str | None
            variants: FlextCore.Types.Dict | None

            def get_config(self) -> FlextCore.Types.Dict:
                """Get plugin configuration."""
                ...

            def validate_config(self, config: FlextCore.Types.Dict) -> bool:
                """Validate plugin configuration."""
                ...

            def execute(self, *args: FlextCore.Types.JsonValue) -> T_co:
                """Execute plugin with given arguments."""
                ...

        @runtime_checkable
        class StreamProtocol(Protocol):
            """Singer stream interface with type safety."""

            name: str
            tap_stream_id: str
            schema: FlextCore.Types.JsonValue

            def sync_records(self) -> FlextCore.Types.JsonValue:
                """Sync records from the stream."""
                ...

            def get_records(self) -> FlextCore.Types.JsonValue:
                """Get records from the stream."""
                ...

        @runtime_checkable
        class TapProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Singer Tap protocol extending Domain.Service for ELT operations."""

            def discover(self) -> FlextCore.Result[FlextCore.Types.JsonValue]:
                """Discover catalog with FlextCore.Result."""
                ...

            def sync(
                self, catalog: FlextCore.Types.JsonValue
            ) -> FlextCore.Result[FlextCore.Types.JsonValue]:
                """Sync data from source with FlextCore.Result."""
                ...

            def execute(self) -> FlextCore.Result[object]:
                """Execute the tap extraction (implements Domain.Service)."""
                ...

        @runtime_checkable
        class TargetProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Singer Target protocol extending Domain.Service for ELT operations."""

            def handle_record(
                self, record: FlextCore.Types.JsonValue
            ) -> FlextCore.Result[FlextCore.Types.JsonValue]:
                """Handle a single record with FlextCore.Result."""
                ...

            def handle_batch(
                self, records: list[FlextCore.Types.JsonValue]
            ) -> FlextCore.Result[FlextCore.Types.JsonValue]:
                """Handle a batch of records with FlextCore.Result."""
                ...

            def execute(self) -> FlextCore.Result[object]:
                """Execute the target loading (implements Domain.Service)."""
                ...

        @runtime_checkable
        class DbtRunnerProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """DBT Runner protocol extending Domain.Service for ELT operations."""

            def run(
                self, models: FlextCore.Types.StringList
            ) -> FlextCore.Result[FlextCore.Types.JsonValue]:
                """Run DBT models with FlextCore.Result."""
                ...

            def test(
                self, models: FlextCore.Types.StringList
            ) -> FlextCore.Result[FlextCore.Types.JsonValue]:
                """Test DBT models with FlextCore.Result."""
                ...

            def execute(self) -> FlextCore.Result[object]:
                """Execute DBT transformations (implements Domain.Service)."""
                ...

        @runtime_checkable
        class ServiceCallProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Service call protocol extending Domain.Service."""

            def call(
                self, operation: str, payload: FlextCore.Types.JsonValue
            ) -> FlextCore.Result[FlextCore.Types.JsonValue]:
                """Execute service call with FlextCore.Result."""
                ...

            def execute(self) -> FlextCore.Result[object]:
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
