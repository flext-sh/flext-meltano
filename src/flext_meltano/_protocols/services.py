"""FLEXT Meltano Protocols - Service, CLI, and Manager protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Protocol, override, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_core import r
from flext_meltano import m, t


class FlextMeltanoProtocolsServices:
    """Service, CLI, and Manager protocol definitions."""

    @runtime_checkable
    class MeltanoExecutor(Protocol):
        """Protocol for Meltano command execution."""

        def execute_meltano_command(
            self,
            command: t.StrSequence,
            timeout: int = ...,
            _cwd: Path | None = None,
        ) -> r[m.Meltano.CommandExecutionResult]:
            """Execute a Meltano runtime command."""
            ...

        def get_project_plugins(
            self,
            plugin_type: str | None = None,
            _cwd: Path | None = None,
        ) -> r[Sequence[t.StrMapping]]:
            """Return project-scoped plugin definitions."""
            ...

    @runtime_checkable
    class ServiceCall(FlextCliProtocols.Service[t.Container], Protocol):
        """Service call protocol extending Service."""

        def call(
            self,
            operation: str,
            payload: t.ConfigurationMapping,
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

        def handle_command(self, args: t.StrSequence) -> r[str]:
            """Handle CLI command."""
            ...

    @runtime_checkable
    class SingerManager(Protocol):
        """Protocol for Singer CLI manager."""

        def handle_command(self, args: t.StrSequence) -> r[str]:
            """Handle CLI command."""
            ...

        def handle_tap_command(self, args: t.StrSequence) -> r[str]:
            """Handle tap command."""
            ...

        def handle_target_command(self, args: t.StrSequence) -> r[str]:
            """Handle target command."""
            ...

    @runtime_checkable
    class StatusManager(Protocol):
        """Protocol for Status CLI manager."""

        def handle_command(self, args: t.StrSequence) -> r[str]:
            """Handle CLI command."""
            ...

        def handle_version_command(self, args: t.StrSequence) -> r[str]:
            """Handle version command."""
            ...

    @runtime_checkable
    class CLI(Protocol):
        """CLI protocol for manager composition - avoids circular imports."""

        @property
        def pipeline_manager(self) -> FlextMeltanoProtocolsServices.CLIManager: ...

        @property
        def singer_manager(self) -> FlextMeltanoProtocolsServices.SingerManager: ...

        @property
        def dbt_manager(self) -> FlextMeltanoProtocolsServices.CLIManager: ...

        @property
        def plugin_manager(self) -> FlextMeltanoProtocolsServices.CLIManager: ...

        @property
        def status_manager(self) -> FlextMeltanoProtocolsServices.StatusManager: ...

        def show_banner(self) -> None:
            """Show CLI banner."""
            ...

        def show_dbt_help(self) -> None:
            """Show DBT help."""
            ...

        def show_pipeline_help(self) -> None:
            """Show pipeline help."""
            ...

        def show_plugin_help(self) -> None:
            """Show plugin help."""
            ...

        def show_status_help(self) -> None:
            """Show status help."""
            ...

        def show_tap_help(self) -> None:
            """Show tap help."""
            ...

        def show_target_help(self) -> None:
            """Show target help."""
            ...
