"""FLEXT Meltano Protocols - All protocol definitions for the domain.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Protocol, override, runtime_checkable

from flext_cli.protocols import FlextCliProtocols
from flext_core.protocols import FlextProtocols
from flext_core import FlextTypes

# Import aliases following order: c -> t -> p -> r -> m -> u
# Runtime aliases defined at module level per FLEXT standards
t = FlextTypes

# Lazy import to break circular dependency - imported on-demand when needed
# from flext_meltano.singer.protocols import (
#     FlextMeltanoPluginProtocols,
#     FlextMeltanoSingerProtocols,
# )


class FlextMeltanoProtocols(FlextCliProtocols):
    """Unified Meltano protocols extending FlextProtocols.

    Extends p to inherit all foundation protocols (Result, Service, etc.)
    and adds Meltano/Singer/DBT-specific protocols in the Meltano namespace.

    Architecture:
    - EXTENDS: p (inherits Foundation, Domain, Application, etc.)
    - ADDS: Meltano/Singer/DBT-specific protocols in Meltano namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_meltano.protocols import p

    # Foundation protocols (inherited)
    result: FlextProtocols.Result[str]
    service: FlextProtocols.Service[str]

    # Meltano-specific protocols
    tap: FlextProtocols.Meltano.TapProtocol
    target: FlextProtocols.Meltano.TargetProtocol
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
        class PluginProtocol(Protocol):
            """Meltano plugin interface with covariant return type."""

            # Plugin attributes (matching actual Meltano plugin objects)
            name: str
            default_variant: str | None
            variants: Mapping[str, FlextTypes.JsonValue] | None

            def get_config(self) -> Mapping[str, FlextTypes.JsonValue]:
                """Get plugin configuration."""
                ...

            def validate_config(
                self,
                config: Mapping[str, FlextTypes.JsonValue],
            ) -> bool:
                """Validate plugin configuration. # INTERFACE."""
                ...

            def execute(self, *args: FlextTypes.JsonValue) -> FlextTypes.JsonValue:
                """Execute plugin with given arguments. # INTERFACE."""
                ...

        @runtime_checkable
        class StreamProtocol(Protocol):
            """Singer stream interface with type safety."""

            name: str
            tap_stream_id: str
            schema: FlextTypes.JsonValue

            def sync_records(self) -> FlextTypes.JsonValue:
                """Sync records from the stream. # INTERFACE."""
                ...

            def get_records(self) -> FlextTypes.JsonValue:
                """Get records from the stream. # INTERFACE."""
                ...

        @runtime_checkable
        class TapProtocol(FlextProtocols.Service[FlextTypes.JsonValue], Protocol):
            """Singer Tap protocol extending Service for ELT operations."""

            def discover(self) -> FlextProtocols.Result[FlextTypes.JsonValue]:
                """Discover catalog with r."""
                ...

            def sync(
                self, catalog: FlextTypes.JsonValue
            ) -> FlextProtocols.Result[FlextTypes.JsonValue]:
                """Sync data from source with r."""
                ...

            @override
            def execute(self) -> FlextProtocols.Result[FlextTypes.JsonValue]:
                """Execute the tap extraction (implements Service)."""
                ...

        @runtime_checkable
        class TargetProtocol(FlextProtocols.Service[FlextTypes.JsonValue], Protocol):
            """Singer Target protocol extending Service for ELT operations."""

            def handle_record(
                self,
                record: FlextTypes.JsonValue,
            ) -> FlextProtocols.Result[FlextTypes.JsonValue]:
                """Handle a single record with r."""
                ...

            def handle_batch(
                self,
                records: list[FlextTypes.JsonValue],
            ) -> FlextProtocols.Result[FlextTypes.JsonValue]:
                """Handle a batch of records with r."""
                ...

            @override
            def execute(self) -> FlextProtocols.Result[FlextTypes.JsonValue]:
                """Execute the target loading (implements Service)."""
                ...

        @runtime_checkable
        class DbtRunnerProtocol(FlextProtocols.Service[FlextTypes.JsonValue], Protocol):
            """DBT Runner protocol extending Service for ELT operations."""

            def run(
                self, models: list[str]
            ) -> FlextProtocols.Result[FlextTypes.JsonValue]:
                """Run DBT models with r."""
                ...

            def test(
                self, models: list[str]
            ) -> FlextProtocols.Result[FlextTypes.JsonValue]:
                """Test DBT models with r."""
                ...

            @override
            def execute(self) -> FlextProtocols.Result[FlextTypes.JsonValue]:
                """Execute DBT transformations (implements Service)."""
                ...

        @runtime_checkable
        class ServiceCallProtocol(
            FlextProtocols.Service[FlextTypes.JsonValue], Protocol
        ):
            """Service call protocol extending Service."""

            def call(
                self,
                operation: str,
                payload: FlextTypes.JsonValue,
            ) -> FlextProtocols.Result[FlextTypes.JsonValue]:
                """Execute service call with r."""
                ...

            @override
            def execute(self) -> FlextProtocols.Result[FlextTypes.JsonValue]:
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
                """Show pipeline helFlextProtocols."""
                ...

            def show_dbt_help(self) -> None:
                """Show DBT helFlextProtocols."""
                ...

            def show_plugin_help(self) -> None:
                """Show plugin helFlextProtocols."""
                ...

            def show_tap_help(self) -> None:
                """Show tap helFlextProtocols."""
                ...

            def show_target_help(self) -> None:
                """Show target helFlextProtocols."""
                ...

            def show_status_help(self) -> None:
                """Show status helFlextProtocols."""
                ...

        @runtime_checkable
        class MeltanoProjectProtocol(Protocol):
            """Meltano Project protocol for type-safe project operations.

            Represents the interface for a Meltano project object that can be
            passed to plugin discovery, pipeline execution, and other operations.
            """

            @property
            def root_dir(self) -> Path:
                """Get project root directory."""
                ...

            def find_plugins(self, plugin_type: str) -> list[FlextTypes.JsonValue]:
                """Find plugins of specified type."""
                ...

        @runtime_checkable
        class AdapterProtocol(Protocol):
            """Protocol for data adapters (tap/target/sink adapters).

            Represents the interface for adapters used in data extraction,
            loading, and transformation operations.
            """

            def connect(self) -> FlextProtocols.Result[bool]:
                """Establish connection to the data source/sink."""
                ...

            def disconnect(self) -> FlextProtocols.Result[bool]:
                """Close connection to the data source/sink."""
                ...

            @property
            def is_connected(self) -> bool:
                """Check if adapter is currently connected."""
                ...

        @runtime_checkable
        class IndexedPluginProtocol(Protocol):
            """Protocol for indexed plugin objects used in plugin discovery.

            Represents plugin metadata accessed via u.get() for attributes
            like variants, default_variant, logo_url.
            """

            @property
            def name(self) -> str:
                """Plugin name."""
                ...

            @property
            def default_variant(self) -> str | None:
                """Default variant name."""
                ...

            @property
            def variants(self) -> Mapping[str, FlextTypes.JsonValue] | None:
                """Available variants."""
                ...

            @property
            def logo_url(self) -> str | None:
                """Plugin logo URL."""
                ...


# Runtime alias for simplified usage
p = FlextMeltanoProtocols

__all__ = [
    "FlextMeltanoProtocols",
    "p",
]
