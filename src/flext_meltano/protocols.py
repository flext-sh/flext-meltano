"""FLEXT Meltano Protocols - All protocol definitions for the domain.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_core import T_co, t
from flext_core.protocols import FlextProtocols

from flext_meltano.singer.protocols import (
    FlextMeltanoPluginProtocols,
    FlextMeltanoSingerProtocols,
)


class FlextMeltanoProtocols(FlextProtocols):
    """Unified Meltano protocols extending p.

    Extends p to inherit all foundation protocols (Result, Service, etc.)
    and adds Meltano/Singer/DBT-specific protocols in the Meltano namespace.

    Architecture:
    - EXTENDS: p (inherits Foundation, Domain, Application, etc.)
    - ADDS: Meltano/Singer/DBT-specific protocols in Meltano namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_meltano.protocols import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]

    # Meltano-specific protocols
    tap: p.Meltano.TapProtocol
    target: p.Meltano.TargetProtocol
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
            variants: dict[str, object] | None

            def get_config(self) -> dict[str, object]:
                """Get plugin configuration."""
                ...

            def validate_config(self, config: dict[str, object]) -> bool:
                """Validate plugin configuration."""
                ...

            def execute(self, *args: t.JsonValue) -> T_co:
                """Execute plugin with given arguments."""
                ...

        @runtime_checkable
        class StreamProtocol(Protocol):
            """Singer stream interface with type safety."""

            name: str
            tap_stream_id: str
            schema: t.JsonValue

            def sync_records(self) -> t.JsonValue:
                """Sync records from the stream."""
                ...

            def get_records(self) -> t.JsonValue:
                """Get records from the stream."""
                ...

        @runtime_checkable
        class TapProtocol(FlextProtocols.Service, Protocol):
            """Singer Tap protocol extending Service for ELT operations."""

            def discover(self) -> FlextProtocols.Result[t.JsonValue]:
                """Discover catalog with r."""
                ...

            def sync(self, catalog: t.JsonValue) -> FlextProtocols.Result[t.JsonValue]:
                """Sync data from source with r."""
                ...

            def execute(self) -> FlextProtocols.Result[object]:
                """Execute the tap extraction (implements Service)."""
                ...

        @runtime_checkable
        class TargetProtocol(FlextProtocols.Service, Protocol):
            """Singer Target protocol extending Service for ELT operations."""

            def handle_record(
                self,
                record: t.JsonValue,
            ) -> FlextProtocols.Result[t.JsonValue]:
                """Handle a single record with r."""
                ...

            def handle_batch(
                self,
                records: list[t.JsonValue],
            ) -> FlextProtocols.Result[t.JsonValue]:
                """Handle a batch of records with r."""
                ...

            def execute(self) -> FlextProtocols.Result[object]:
                """Execute the target loading (implements Service)."""
                ...

        @runtime_checkable
        class DbtRunnerProtocol(FlextProtocols.Service, Protocol):
            """DBT Runner protocol extending Service for ELT operations."""

            def run(self, models: list[str]) -> FlextProtocols.Result[t.JsonValue]:
                """Run DBT models with r."""
                ...

            def test(self, models: list[str]) -> FlextProtocols.Result[t.JsonValue]:
                """Test DBT models with r."""
                ...

            def execute(self) -> FlextProtocols.Result[object]:
                """Execute DBT transformations (implements Service)."""
                ...

        @runtime_checkable
        class ServiceCallProtocol(FlextProtocols.Service, Protocol):
            """Service call protocol extending Service."""

            def call(
                self,
                operation: str,
                payload: t.JsonValue,
            ) -> FlextProtocols.Result[t.JsonValue]:
                """Execute service call with r."""
                ...

            def execute(self) -> FlextProtocols.Result[object]:
                """Execute service operation (implements Service)."""
                ...

        @runtime_checkable
        class CLIManagerProtocol(Protocol):
            """Base protocol for CLI managers."""

            def handle_command(self, args: list[str]) -> int:
                """Handle CLI command."""
                ...

        @runtime_checkable
        class SingerManagerProtocol(Protocol):
            """Protocol for Singer CLI manager."""

            def handle_command(self, args: list[str]) -> int:
                """Handle CLI command."""
                ...

            def handle_tap_command(self, args: list[str]) -> int:
                """Handle tap command."""
                ...

            def handle_target_command(self, args: list[str]) -> int:
                """Handle target command."""
                ...

        @runtime_checkable
        class StatusManagerProtocol(Protocol):
            """Protocol for Status CLI manager."""

            def handle_command(self, args: list[str]) -> int:
                """Handle CLI command."""
                ...

            def handle_version_command(self) -> int:
                """Handle version command."""
                ...

        @runtime_checkable
        class CLIProtocol(Protocol):
            """CLI protocol for manager composition - avoids circular imports."""

            # Manager attributes with proper protocol types
            pipeline_manager: FlextMeltanoProtocols.Meltano.CLIManagerProtocol
            singer_manager: FlextMeltanoProtocols.Meltano.SingerManagerProtocol
            dbt_manager: FlextMeltanoProtocols.Meltano.CLIManagerProtocol
            plugin_manager: FlextMeltanoProtocols.Meltano.CLIManagerProtocol
            status_manager: FlextMeltanoProtocols.Meltano.StatusManagerProtocol

            def show_banner(self) -> None:
                """Show CLI banner."""
                ...

            def show_pipeline_help(self) -> None:
                """Show pipeline help."""
                ...

            def show_dbt_help(self) -> None:
                """Show DBT help."""
                ...

            def show_plugin_help(self) -> None:
                """Show plugin help."""
                ...

            def show_tap_help(self) -> None:
                """Show tap help."""
                ...

            def show_target_help(self) -> None:
                """Show target help."""
                ...

            def show_status_help(self) -> None:
                """Show status help."""
                ...


# Runtime alias for simplified usage
p = FlextMeltanoProtocols

__all__ = [
    "FlextMeltanoPluginProtocols",
    "FlextMeltanoProtocols",
    "FlextMeltanoSingerProtocols",
    "p",
]
