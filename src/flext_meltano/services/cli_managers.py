"""FLEXT Meltano CLI Managers - Command router and Singer manager.

Includes re-exports of pipeline, DBT, plugin, and status managers from private modules.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable, Mapping

from flext_core import FlextLogger, r

from flext_meltano import (
    FlextMeltanoDbtManager,
    FlextMeltanoPipelineManager,
    FlextMeltanoPluginManager,
    FlextMeltanoStatusManager,
    c,
    p,
    t,
    u,
)


class FlextMeltanoCommandRouter:
    """Routes CLI commands to appropriate handlers."""

    def __init__(self, cli: p.Meltano.CommandRouterCli) -> None:
        """Initialize command router with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def route_command(self, args: t.StrSequence) -> int:
        """Route command to appropriate handler using composition."""
        if u.Meltano.is_help_request(args):
            self.cli.show_banner()
            self.logger.info("FLEXT Meltano CLI - Main Help")
            return 0
        command, command_args = args[0], args[1:]
        handler_result = self._get_command_handler(command)
        if handler_result.is_failure:
            self.logger.error("Command error", error=str(handler_result.error))
            return 1
        execute_result = handler_result.value(command_args)
        if execute_result.is_failure:
            self.logger.error("Execution error", error=str(execute_result.error))
            return 1
        return 0

    def _get_command_handler(
        self,
        command: str,
    ) -> r[Callable[[t.StrSequence], r[str]]]:
        """Get command handler for given command."""
        command_map: Mapping[str, Callable[[t.StrSequence], r[str]]] = {
            c.Meltano.Enums.CliCommand.PIPELINE: self.cli.pipeline_manager.handle_command,
            c.Meltano.Enums.CliCommand.TAP: self.cli.singer_manager.handle_tap_command,
            c.Meltano.Enums.CliCommand.TARGET: self.cli.singer_manager.handle_target_command,
            c.Meltano.Enums.CliCommand.DBT: self.cli.dbt_manager.handle_command,
            c.Meltano.Enums.CliCommand.PLUGIN: self.cli.plugin_manager.handle_command,
            c.Meltano.Enums.CliCommand.STATUS: self.cli.status_manager.handle_command,
            c.Meltano.Enums.CliCommand.VERSION: self.cli.status_manager.handle_version_command,
        }
        handler = command_map.get(command)
        if handler is None:
            return r[Callable[[t.StrSequence], r[str]]].fail(
                f"Unknown command: {command}",
            )
        return r[Callable[[t.StrSequence], r[str]]].ok(handler)


class FlextMeltanoSingerManager:
    """Handle Singer tap/target CLI commands."""

    def __init__(self, cli: p.Meltano.SingerCli) -> None:
        """Initialize Singer manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def handle_command(self, args: t.StrSequence) -> r[str]:
        """Handle Singer command by routing to tap or target subcommands."""
        if u.Meltano.is_help_request(args):
            self.cli.show_tap_help()
            return r[str].ok(c.Meltano.Enums.ExecutorCommand.HELP)
        subcommand, subcommand_args = args[0], args[1:]
        if subcommand == c.Meltano.Enums.CliCommand.TAP:
            return self.handle_tap_command(subcommand_args)
        if subcommand == c.Meltano.Enums.CliCommand.TARGET:
            return self.handle_target_command(subcommand_args)
        return r[str].fail(f"Unknown Singer command: {subcommand}")

    def handle_tap_command(self, args: t.StrSequence) -> r[str]:
        """Handle tap command."""
        if u.Meltano.is_help_request(args):
            self.cli.show_tap_help()
            return r[str].ok(c.Meltano.Enums.ExecutorCommand.HELP)
        return self._execute_tap_operation(args[0], args[1:])

    def handle_target_command(self, args: t.StrSequence) -> r[str]:
        """Handle target command."""
        if u.Meltano.is_help_request(args):
            self.cli.show_target_help()
            return r[str].ok(c.Meltano.Enums.ExecutorCommand.HELP)
        return self._execute_target_operation(args[0], args[1:])

    def _execute_tap_operation(self, operation: str, _args: t.StrSequence) -> r[str]:
        self.logger.info(
            "Tap operation '%s' not implemented in this refactor",
            operation,
        )
        return r[str].ok("not implemented")

    def _execute_target_operation(self, operation: str, _args: t.StrSequence) -> r[str]:
        self.logger.info(
            "Target operation '%s' not implemented in this refactor",
            operation,
        )
        return r[str].ok("not implemented")


__all__ = [
    "FlextMeltanoCommandRouter",
    "FlextMeltanoDbtManager",
    "FlextMeltanoPipelineManager",
    "FlextMeltanoPluginManager",
    "FlextMeltanoSingerManager",
    "FlextMeltanoStatusManager",
]
