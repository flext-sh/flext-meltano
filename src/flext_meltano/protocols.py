"""FLEXT Meltano Protocols - All protocol definitions for the domain.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Protocol, override, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_meltano.models import FlextMeltanoModels as m
from flext_meltano.typings import FlextMeltanoTypes as t


class FlextMeltanoProtocols(FlextCliProtocols):
    """Unified Meltano protocols extending FlextCliProtocols.

    Extends p to inherit all foundation protocols (Result, Service, etc.)
    and adds Meltano/Singer/DBT-specific protocols in the Meltano namespace.

    Architecture:
    - EXTENDS: p (inherits Foundation, Domain, Application, etc.)
    - ADDS: Meltano/Singer/DBT-specific protocols in Meltano namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_core.protocols import FlextProtocols as p

    # Foundation protocols (inherited)
    result: FlextCliProtocols.Result[str]
    service: FlextCliProtocols.Service[str]

    # Meltano-specific protocols
    tap: FlextCliProtocols.Meltano.Tap
    target: FlextCliProtocols.Meltano.Target
    """

    class Meltano:
        """Meltano ELT domain-specific protocols.

        Provides protocols for Meltano plugins, Singer taps/targets/streams,
        DBT runners, and service operations.
        """

        @runtime_checkable
        class Plugin(Protocol):
            """Meltano plugin interface with covariant return type."""

            name: str
            default_variant: str | None
            variants: Mapping[str, t.Scalar] | None

            def execute(self, *args: t.Scalar, **kwargs: t.Scalar) -> t.Container:
                """Execute plugin with given arguments. # INTERFACE."""
                ...

            def get_config(self) -> Mapping[str, t.Scalar]:
                """Get plugin configuration."""
                ...

            def validate_config(self, config: Mapping[str, t.Scalar]) -> bool:
                """Validate plugin configuration. # INTERFACE."""
                ...

        @runtime_checkable
        class Stream(Protocol):
            """Singer stream interface with type safety."""

            name: str
            tap_stream_id: str
            schema: Mapping[str, t.Container]

            def get_records(self) -> list[Mapping[str, t.Container]]:
                """Get records from the stream. # INTERFACE."""
                ...

            def sync_records(self) -> list[Mapping[str, t.Container]]:
                """Sync records from the stream. # INTERFACE."""
                ...

        @runtime_checkable
        class Tap(FlextCliProtocols.Service[t.Meltano.ResultDict], Protocol):
            """Singer Tap protocol extending Service for ELT operations."""

            def discover(self) -> FlextCliProtocols.Result[t.Meltano.ResultDict]:
                """Discover catalog with r."""
                ...

            @override
            def execute(self) -> FlextCliProtocols.Result[t.Meltano.ResultDict]:
                """Execute the tap extraction (implements Service)."""
                ...

            def sync(
                self,
                catalog: Mapping[str, t.Container],
            ) -> FlextCliProtocols.Result[t.Meltano.ResultDict]:
                """Sync data from source with r."""
                ...

        @runtime_checkable
        class Target(FlextCliProtocols.Service[t.Meltano.ResultDict], Protocol):
            """Singer Target protocol extending Service for ELT operations."""

            @override
            def execute(self) -> FlextCliProtocols.Result[t.Meltano.ResultDict]:
                """Execute the target loading (implements Service)."""
                ...

            def handle_batch(
                self,
                records: list[t.Meltano.RecordDict],
            ) -> FlextCliProtocols.Result[t.Meltano.ResultDict]:
                """Handle a batch of records with r."""
                ...

            def handle_record(
                self,
                record: t.Meltano.RecordDict,
            ) -> FlextCliProtocols.Result[t.Meltano.ResultDict]:
                """Handle a single record with r."""
                ...

        @runtime_checkable
        class DbtRunner(
            FlextCliProtocols.Service[t.Meltano.MeltanoConfigDict],
            Protocol,
        ):
            """DBT Runner protocol extending Service for ELT operations."""

            @override
            def execute(self) -> FlextCliProtocols.Result[t.Meltano.MeltanoConfigDict]:
                """Execute DBT transformations (implements Service)."""
                ...

            def run(
                self,
                models: list[str],
            ) -> FlextCliProtocols.Result[t.Meltano.MeltanoConfigDict]:
                """Run DBT models with r."""
                ...

            def test(
                self,
                models: list[str],
            ) -> FlextCliProtocols.Result[t.Meltano.MeltanoConfigDict]:
                """Test DBT models with r."""
                ...

        @runtime_checkable
        class ServiceCall(FlextCliProtocols.Service[t.Container], Protocol):
            """Service call protocol extending Service."""

            def call(
                self,
                operation: str,
                payload: Mapping[str, t.Scalar],
            ) -> FlextCliProtocols.Result[t.Container]:
                """Execute service call with r."""
                ...

            @override
            def execute(self) -> FlextCliProtocols.Result[t.Container]:
                """Execute service operation (implements Service)."""
                ...

        @runtime_checkable
        class Output(Protocol):
            """Protocol for CLI output with print_message method."""

            def print_message(self, message: str, style: str | None = None) -> None:
                """Print a message to output."""
                ...

        @runtime_checkable
        class CLIManager(Protocol):
            """Base protocol for CLI managers."""

            def handle_command(self, args: list[str]) -> FlextCliProtocols.Result[None]:
                """Handle CLI command."""
                ...

        @runtime_checkable
        class SingerManager(Protocol):
            """Protocol for Singer CLI manager."""

            def handle_command(self, args: list[str]) -> FlextCliProtocols.Result[None]:
                """Handle CLI command."""
                ...

            def handle_tap_command(
                self, args: list[str]
            ) -> FlextCliProtocols.Result[None]:
                """Handle tap command."""
                ...

            def handle_target_command(
                self, args: list[str]
            ) -> FlextCliProtocols.Result[None]:
                """Handle target command."""
                ...

        @runtime_checkable
        class StatusManager(Protocol):
            """Protocol for Status CLI manager."""

            def handle_command(self, args: list[str]) -> FlextCliProtocols.Result[None]:
                """Handle CLI command."""
                ...

            def handle_version_command(self) -> FlextCliProtocols.Result[None]:
                """Handle version command."""
                ...

        @runtime_checkable
        class CLI(Protocol):
            """CLI protocol for manager composition - avoids circular imports."""

            pipeline_manager: FlextMeltanoProtocols.Meltano.CLIManager
            singer_manager: FlextMeltanoProtocols.Meltano.SingerManager
            dbt_manager: FlextMeltanoProtocols.Meltano.CLIManager
            plugin_manager: FlextMeltanoProtocols.Meltano.CLIManager
            status_manager: FlextMeltanoProtocols.Meltano.StatusManager

            def show_banner(self) -> None:
                """Show CLI banner."""
                ...

            def show_dbt_help(self) -> None:
                """Show DBT helFlextProtocols."""
                ...

            def show_pipeline_help(self) -> None:
                """Show pipeline helFlextProtocols."""
                ...

            def show_plugin_help(self) -> None:
                """Show plugin helFlextProtocols."""
                ...

            def show_status_help(self) -> None:
                """Show status helFlextProtocols."""
                ...

            def show_tap_help(self) -> None:
                """Show tap helFlextProtocols."""
                ...

            def show_target_help(self) -> None:
                """Show target helFlextProtocols."""
                ...

        @runtime_checkable
        class Project(Protocol):
            """Meltano Project protocol for type-safe project operations.

            Represents the interface for a Meltano project object that can be
            passed to plugin discovery, pipeline execution, and other operations.
            """

            @property
            def root_dir(self) -> Path:
                """Get project root directory."""
                ...

            def find_plugins(
                self,
                plugin_type: str,
            ) -> list[t.Meltano.PluginDefinition]:
                """Find plugins of specified type."""
                ...

        @runtime_checkable
        class Adapter(Protocol):
            """Protocol for data adapters (tap/target/sink adapters).

            Represents the interface for adapters used in data extraction,
            loading, and transformation operations.
            """

            @property
            def is_connected(self) -> bool:
                """Check if adapter is currently connected."""
                ...

            def connect(self) -> FlextCliProtocols.Result[bool]:
                """Establish connection to the data source/sink."""
                ...

            def disconnect(self) -> FlextCliProtocols.Result[bool]:
                """Close connection to the data source/sink."""
                ...

        @runtime_checkable
        class IndexedPlugin(Protocol):
            """Protocol for indexed plugin objects used in plugin discovery.

            Represents plugin metadata accessed via u.get() for attributes
            like variants, default_variant, logo_url.
            """

            @property
            def default_variant(self) -> str | None:
                """Default variant name."""
                ...

            @property
            def logo_url(self) -> str | None:
                """Plugin logo URL."""
                ...

            @property
            def name(self) -> str:
                """Plugin name."""
                ...

            @property
            def variants(self) -> Mapping[str, t.Scalar] | None:
                """Available variants."""
                ...

        class SingerTap(Protocol):
            """Singer Tap protocol definition for data extraction.

            Defines the interface for Singer data extraction (tap) components
            that implement the Singer protocol for data source integration.
            """

            streams: list[str]
            name: str
            state: m.Meltano.SingerStateMessage

            def discover(self) -> m.Meltano.SingerCatalog:
                """Discover available streams and schemas."""
                ...

            def get_records(
                self,
                stream_name: str,
            ) -> list[m.Meltano.SingerRecordMessage]:
                """Get records for a specific stream."""
                ...

            def get_state(self) -> m.Meltano.SingerStateMessage:
                """Get current state."""
                ...

            def sync(
                self,
                catalog: m.Meltano.SingerCatalog,
                state: m.Meltano.SingerStateMessage,
            ) -> None:
                """Synchronize data from source to stdout."""
                ...

        class SingerTarget(Protocol):
            """Singer Target protocol definition for data loading.

            Defines the interface for Singer data loading (target) components
            that implement the Singer protocol for data sink integration.
            """

            name: str
            config: m.Meltano.TargetConfig

            def consume(self, records: list[m.Meltano.SingerRecordMessage]) -> int:
                """Consume records batch.

                Args:
                records: Batch of records to consume

                Returns:
                Number of records consumed

                """
                ...


p = FlextMeltanoProtocols
__all__ = ["FlextMeltanoProtocols", "p"]
