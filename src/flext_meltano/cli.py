"""FLEXT Meltano CLI - Professional Command-Line Interface.

Complete CLI for Meltano/Singer/DBT operations using flext-cli exclusively.
Zero Tolerance: NO direct click/rich/typer imports allowed.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import sys
from typing import cast

from flext_cli import FlextCli
from flext_core import FlextLogger

from flext_meltano import (
    FlextMeltano,
    FlextMeltanoPluginManager,
    FlextMeltanoSingerManager,
    FlextMeltanoStatusManager,
    p,
)
from flext_meltano.cli_managers import (
    FlextMeltanoCommandRouter,
    FlextMeltanoDbtManager,
    FlextMeltanoPipelineManager,
)


class FlextMeltanoCLI:
    """SOLID-compliant CLI for FLEXT Meltano operations.

    Uses composition for pipeline management, Singer operations, DBT operations,
    plugin management, and monitoring. Railway-oriented programming for maximum maintainability.
    Single class per module following SOLID principles strictly.
    """

    logger: p.Logger
    output: p.Meltano.Output
    _api: FlextMeltano
    pipeline_manager: p.Meltano.CLIManager
    singer_manager: p.Meltano.SingerManager
    dbt_manager: p.Meltano.CLIManager
    plugin_manager: p.Meltano.CLIManager
    status_manager: p.Meltano.StatusManager
    command_router: FlextMeltanoCommandRouter

    def __init__(self) -> None:
        """Initialize CLI with SOLID delegation.

        Uses composition for command routing, pipeline operations, Singer operations,
        DBT operations, plugin management, and monitoring.
        """
        super().__init__()
        self.logger = FlextLogger(__name__)
        self._cli = FlextCli()
        self._api = FlextMeltano()
        self.output = self._cli.output
        temp_self = self
        self.pipeline_manager = cast(
            "p.Meltano.CLIManager", FlextMeltanoPipelineManager(temp_self)
        )
        self.singer_manager = cast(
            "p.Meltano.SingerManager", FlextMeltanoSingerManager(temp_self)
        )
        self.dbt_manager = cast(
            "p.Meltano.CLIManager", FlextMeltanoDbtManager(temp_self)
        )
        self.plugin_manager = cast(
            "p.Meltano.CLIManager", FlextMeltanoPluginManager(temp_self)
        )
        self.status_manager = cast(
            "p.Meltano.StatusManager", FlextMeltanoStatusManager(temp_self)
        )
        self.command_router = FlextMeltanoCommandRouter(temp_self)

    def main(self, args: list[str] | None = None) -> int:
        """Main CLI entry point."""
        if args is None:
            args = sys.argv[1:]
        return self.command_router.route_command(args)

    def show_banner(self) -> None:
        """Show CLI banner."""
        self.output.print_message("FLEXT Meltano CLI - Use flext-cli patterns")

    def show_dbt_help(self) -> None:
        """Show DBT help."""
        self.output.print_message("DBT commands: run, test, docs")

    def show_pipeline_help(self) -> None:
        """Show pipeline help."""
        self.output.print_message(
            "Pipeline commands: create, run, list, status, stop, delete",
        )

    def show_plugin_help(self) -> None:
        """Show plugin help."""
        self.output.print_message("Plugin commands: install, list, info")

    def show_status_help(self) -> None:
        """Show status help."""
        self.output.print_message("Status commands: show, health")

    def show_tap_help(self) -> None:
        """Show tap help."""
        self.output.print_message("Tap commands: run, discover, test")

    def show_target_help(self) -> None:
        """Show target help."""
        self.output.print_message("Target commands: run, test")


def main() -> int:
    """Main entry point for FLEXT Meltano CLI."""
    cli = FlextMeltanoCLI()
    return cli.main()
