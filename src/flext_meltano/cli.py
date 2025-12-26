"""FLEXT Meltano CLI - Professional Command-Line Interface.

Complete CLI for Meltano/Singer/DBT operations using flext-cli exclusively.
Zero Tolerance: NO direct click/rich/typer imports allowed.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import sys
from typing import Protocol

from flext_cli import FlextCli
from flext_cli.protocols import FlextCliProtocols
from flext_core import FlextLogger, FlextResult

from flext_meltano.api import FlextMeltano
from flext_meltano.cli_managers import (
    FlextMeltanoCommandRouter,
    FlextMeltanoDbtManager,
    FlextMeltanoPipelineManager,
    FlextMeltanoPluginManager,
    FlextMeltanoSingerManager,
    FlextMeltanoStatusManager,
    _ManagerProtocol,
    _SingerManagerProtocol,
    _StatusManagerProtocol,
)

# Import alias for protocol types
p_cli = FlextCliProtocols
r = FlextResult


class _OutputProtocol(Protocol):
    """Protocol for CLI output with print_message method."""

    def print_message(self, message: str, style: str | None = None) -> r[bool]: ...


class FlextMeltanoCLI:
    """SOLID-compliant CLI for FLEXT Meltano operations.

    Uses composition for pipeline management, Singer operations, DBT operations,
    plugin management, and monitoring. Railway-oriented programming for maximum maintainability.
    Single class per module following SOLID principles strictly.
    """

    # Declare attributes to satisfy _CLIProtocol at class level
    # Use protocol types to match _CLIProtocol expectations
    logger: FlextLogger
    output: _OutputProtocol  # FlextCliOutput (actual type from flext_cli)
    _api: FlextMeltano
    pipeline_manager: _ManagerProtocol
    singer_manager: _SingerManagerProtocol
    dbt_manager: _ManagerProtocol
    plugin_manager: _ManagerProtocol
    status_manager: _StatusManagerProtocol
    command_router: FlextMeltanoCommandRouter

    def __init__(self) -> None:
        """Initialize CLI with SOLID delegation.

        Uses composition for command routing, pipeline operations, Singer operations,
        DBT operations, plugin management, and monitoring.
        """
        super().__init__()
        self.logger = FlextLogger(__name__)

        # Initialize core dependencies
        self._cli = FlextCli()
        self._api = FlextMeltano()
        self.output = self._cli.output

        # Chicken-and-egg: managers need self, but self needs managers for _CLIProtocol
        # Solution: Create a temporary typed variable that we know will satisfy the protocol
        # after all managers are assigned
        temp_self = self

        # Initialize specialized components using composition
        self.pipeline_manager = FlextMeltanoPipelineManager(temp_self)
        self.singer_manager = FlextMeltanoSingerManager(temp_self)
        self.dbt_manager = FlextMeltanoDbtManager(temp_self)
        self.plugin_manager = FlextMeltanoPluginManager(temp_self)
        self.status_manager = FlextMeltanoStatusManager(temp_self)
        self.command_router = FlextMeltanoCommandRouter(temp_self)

    def show_pipeline_help(self) -> None:
        """Show pipeline help."""
        self.output.print_message(
            "Pipeline commands: create, run, list, status, stop, delete",
        )

    def show_tap_help(self) -> None:
        """Show tap help."""
        self.output.print_message("Tap commands: run, discover, test")

    def show_target_help(self) -> None:
        """Show target help."""
        self.output.print_message("Target commands: run, test")

    def show_dbt_help(self) -> None:
        """Show DBT help."""
        self.output.print_message("DBT commands: run, test, docs")

    def show_plugin_help(self) -> None:
        """Show plugin help."""
        self.output.print_message("Plugin commands: install, list, info")

    def show_status_help(self) -> None:
        """Show status help."""
        self.output.print_message("Status commands: show, health")

    # =============================================================================
    # MAIN CLI ENTRY POINT
    # =============================================================================

    def main(self, args: list[str] | None = None) -> int:
        """Main CLI entry point."""
        if args is None:
            args = sys.argv[1:]

        return self.command_router.route_command(args)

    def show_banner(self) -> None:
        """Show CLI banner."""
        self.output.print_message("FLEXT Meltano CLI - Use flext-cli patterns")


def main() -> int:
    """Main entry point for FLEXT Meltano CLI."""
    cli = FlextMeltanoCLI()
    return cli.main()
