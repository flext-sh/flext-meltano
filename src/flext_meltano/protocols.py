"""FLEXT Meltano Protocols - All protocol definitions for the domain.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

from flext_core import (
    FlextProtocols,
    FlextResult,
    t as t_core,
)

# Import Singer protocols from subdirectory
from flext_meltano.singer.protocols import (
    FlextMeltanoPluginProtocols,
    FlextMeltanoSingerProtocols,
)

T_co = TypeVar("T_co", covariant=True)

# Import aliases for simplified usage
p_base = FlextProtocols
r = FlextResult
t_base = t_core


class FlextMeltanoProtocols(p_base):
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
            variants: dict[str, object] | None

            def get_config(self) -> dict[str, object]:
                """Get plugin configuration."""
                ...

            def validate_config(self, config: dict[str, object]) -> bool:
                """Validate plugin configuration."""
                ...

            def execute(self, *args: t_base.JsonValue) -> T_co:
                """Execute plugin with given arguments."""
                ...

        @runtime_checkable
        class StreamProtocol(Protocol):
            """Singer stream interface with type safety."""

            name: str
            tap_stream_id: str
            schema: t_base.JsonValue

            def sync_records(self) -> t_base.JsonValue:
                """Sync records from the stream."""
                ...

            def get_records(self) -> t_base.JsonValue:
                """Get records from the stream."""
                ...

        @runtime_checkable
        class TapProtocol(p_base.Service, Protocol):
            """Singer Tap protocol extending Domain.Service for ELT operations."""

            def discover(self) -> r[t_base.JsonValue]:
                """Discover catalog with FlextResult."""
                ...

            def sync(self, catalog: t_base.JsonValue) -> r[t_base.JsonValue]:
                """Sync data from source with FlextResult."""
                ...

            def execute(self) -> p_base.ResultProtocol[object]:
                """Execute the tap extraction (implements Domain.Service)."""
                ...

        @runtime_checkable
        class TargetProtocol(p_base.Service, Protocol):
            """Singer Target protocol extending Domain.Service for ELT operations."""

            def handle_record(self, record: t_base.JsonValue) -> r[t_base.JsonValue]:
                """Handle a single record with FlextResult."""
                ...

            def handle_batch(
                self,
                records: list[t_base.JsonValue],
            ) -> r[t_base.JsonValue]:
                """Handle a batch of records with FlextResult."""
                ...

            def execute(self) -> p_base.ResultProtocol[object]:
                """Execute the target loading (implements Domain.Service)."""
                ...

        @runtime_checkable
        class DbtRunnerProtocol(p_base.Service, Protocol):
            """DBT Runner protocol extending Domain.Service for ELT operations."""

            def run(self, models: list[str]) -> r[t_base.JsonValue]:
                """Run DBT models with FlextResult."""
                ...

            def test(self, models: list[str]) -> r[t_base.JsonValue]:
                """Test DBT models with FlextResult."""
                ...

            def execute(self) -> p_base.ResultProtocol[object]:
                """Execute DBT transformations (implements Domain.Service)."""
                ...

        @runtime_checkable
        class ServiceCallProtocol(p_base.Service, Protocol):
            """Service call protocol extending Domain.Service."""

            def call(
                self,
                operation: str,
                payload: t_base.JsonValue,
            ) -> r[t_base.JsonValue]:
                """Execute service call with FlextResult."""
                ...

            def execute(self) -> p_base.ResultProtocol[object]:
                """Execute service operation (implements Domain.Service)."""
                ...

    # =========================================================================
    # BACKWARD COMPATIBILITY ALIASES
    # =========================================================================
    # Maintain existing attribute names for zero breaking changes.

    @runtime_checkable
    class MeltanoPluginProtocol(Meltano.PluginProtocol):
        """MeltanoPluginProtocol - real inheritance."""

    @runtime_checkable
    class SingerStreamProtocol(Meltano.StreamProtocol):
        """SingerStreamProtocol - real inheritance."""

    @runtime_checkable
    class SingerTapProtocol(Meltano.TapProtocol):
        """SingerTapProtocol - real inheritance."""

    @runtime_checkable
    class SingerTargetProtocol(Meltano.TargetProtocol):
        """SingerTargetProtocol - real inheritance."""

    @runtime_checkable
    class DbtRunnerProtocol(Meltano.DbtRunnerProtocol):
        """DbtRunnerProtocol - real inheritance."""

    @runtime_checkable
    class ServiceCallProtocol(Meltano.ServiceCallProtocol):
        """ServiceCallProtocol - real inheritance."""


__all__ = [
    "FlextMeltanoPluginProtocols",
    "FlextMeltanoProtocols",
    "FlextMeltanoSingerProtocols",
]
