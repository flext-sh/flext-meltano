"""FLEXT Meltano CLI - Professional command-line interface.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from typing import override

from flext_cli import cli
from flext_core import r
from pydantic import PrivateAttr

from flext_meltano.base import FlextMeltanoServiceBase
from flext_meltano.constants import FlextMeltanoConstants as c
from flext_meltano.protocols import FlextMeltanoProtocols as p
from flext_meltano.services.cli_managers import (
    FlextMeltanoCommandRouter,
    FlextMeltanoDbtManager,
    FlextMeltanoPipelineManager,
    FlextMeltanoPluginManager,
    FlextMeltanoSingerManager,
    FlextMeltanoStatusManager,
)
from flext_meltano.typings import FlextMeltanoTypes as t


class FlextMeltanoCLI(FlextMeltanoServiceBase):
    """SOLID-compliant CLI for FLEXT Meltano operations."""

    service_name: str = "FlextMeltanoCLI"
    _output: p.Meltano.Output = PrivateAttr()
    _pipeline_manager: p.Meltano.CLIManager = PrivateAttr()
    _singer_manager: p.Meltano.SingerManager = PrivateAttr()
    _dbt_manager: p.Meltano.CLIManager = PrivateAttr()
    _plugin_manager: p.Meltano.CLIManager = PrivateAttr()
    _status_manager: p.Meltano.StatusManager = PrivateAttr()
    _command_router: FlextMeltanoCommandRouter = PrivateAttr()

    @override
    def model_post_init(self, __context: t.ScalarMapping | None, /) -> None:
        """Bind CLI collaborators after Pydantic service initialization."""
        super().model_post_init(__context)
        self._output = cli
        self._pipeline_manager = FlextMeltanoPipelineManager(self)
        self._singer_manager = FlextMeltanoSingerManager(self)
        self._dbt_manager = FlextMeltanoDbtManager(self)
        self._plugin_manager = FlextMeltanoPluginManager(self)
        self._status_manager = FlextMeltanoStatusManager(self)
        self._command_router = FlextMeltanoCommandRouter(self)

    @property
    def output(self) -> p.Meltano.Output:
        """CLI output backend."""
        return self._output

    @property
    def pipeline_manager(self) -> p.Meltano.CLIManager:
        """Pipeline manager."""
        return self._pipeline_manager

    @property
    def singer_manager(self) -> p.Meltano.SingerManager:
        """Singer manager."""
        return self._singer_manager

    @property
    def dbt_manager(self) -> p.Meltano.CLIManager:
        """DBT manager."""
        return self._dbt_manager

    @property
    def plugin_manager(self) -> p.Meltano.CLIManager:
        """Plugin manager."""
        return self._plugin_manager

    @property
    def status_manager(self) -> p.Meltano.StatusManager:
        """Status manager."""
        return self._status_manager

    @property
    def command_router(self) -> FlextMeltanoCommandRouter:
        """Command router."""
        return self._command_router

    def main(self, args: t.StrSequence | None = None) -> int:
        """Main CLI entry point."""
        command_args = sys.argv[1:] if args is None else args
        return self.command_router.route_command(command_args)

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

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute CLI service."""
        return r[t.Meltano.MeltanoConfigDict].ok({
            "status": c.Meltano.Enums.StreamStatus.COMPLETED,
        })


def main() -> int:
    """Main entry point for FLEXT Meltano CLI."""
    return FlextMeltanoCLI().main()


__all__ = ["FlextMeltanoCLI", "main"]
