"""FLEXT Meltano CLI Managers - SOLID-compliant CLI manager classes.

This module provides focused CLI manager functionality following SOLID principles
with one class per module architecture, consolidated for better organization.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from flext_core import FlextLogger, FlextResult

if TYPE_CHECKING:
    from flext_meltano.cli import FlextMeltanoCLI


class FlextMeltanoCommandRouter:
    """SOLID-compliant command router for FLEXT Meltano CLI.

    Single responsibility: route CLI commands to appropriate handlers.
    Uses composition and railway-oriented programming for maintainability.
    """

    def __init__(self, cli: FlextMeltanoCLI) -> None:
        """Initialize command router with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def route_command(self, args: list[str]) -> int:
        """Route command to appropriate handler using composition."""
        if not args or args[0] in {"--help", "-h"}:
            self.cli.show_banner()
            # Use proper FLEXT logging service instead of non-existent method
            self.logger.info("FLEXT Meltano CLI - Main Help")
            return 0

        command = args[0]
        command_args = args[1:]

        # Use railway-oriented command mapping
        handler_result = self._get_command_handler(command)
        if handler_result.is_failure:
            self.logger.error(f"Command error: {handler_result.error}")
            return 1

        handler = handler_result.unwrap()
        execute_result = self._execute_command(handler, command_args)
        if execute_result.is_failure:
            self.logger.error(f"Execution error: {execute_result.error}")
            return 1

        return 0

    def _get_command_handler(
        self, command: str
    ) -> FlextResult[Callable[[list[str]], FlextResult[None]]]:
        """Get command handler for given command."""
        command_map: dict[str, Callable[[list[str]], FlextResult[None]]] = {
            "pipeline": self.cli.pipeline_manager.handle_command,
            "tap": self.cli.singer_manager.handle_tap_command,
            "target": self.cli.singer_manager.handle_target_command,
            "dbt": self.cli.dbt_manager.handle_command,
            "plugin": self.cli.plugin_manager.handle_command,
            "status": self.cli.status_manager.handle_command,
            "version": self.cli.status_manager.handle_version_command,
        }

        handler = command_map.get(command)
        if handler is None:
            return FlextResult[Callable[[list[str]], FlextResult[None]]].fail(
                f"Unknown command: {command}"
            )

        return FlextResult[Callable[[list[str]], FlextResult[None]]].ok(handler)

    def _execute_command(
        self, handler: Callable[[list[str]], FlextResult[None]], args: list[str]
    ) -> FlextResult[None]:
        """Execute command handler."""
        return handler(args)


class FlextMeltanoPipelineManager:
    """SOLID-compliant pipeline manager for FLEXT Meltano CLI.

    Single responsibility: handle pipeline-related CLI commands.
    Uses composition and railway-oriented programming for maintainability.
    """

    def __init__(self, cli: FlextMeltanoCLI) -> None:
        """Initialize pipeline manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def handle_command(self, args: list[str]) -> FlextResult[None]:
        """Handle pipeline command using composition."""
        if not args or args[0] in {"--help", "-h"}:
            self.cli.show_pipeline_help()
            return FlextResult[None].ok(None)

        subcommand = args[0]
        subcommand_args = args[1:]

        # Route to specific pipeline operations
        handler_result = self._get_pipeline_handler(subcommand)
        if handler_result.is_failure:
            return FlextResult[None].fail(handler_result.error)

        handler = handler_result.unwrap()
        return self._execute_pipeline_operation(handler, subcommand_args)

    def _get_pipeline_handler(
        self, subcommand: str
    ) -> FlextResult[Callable[[list[str]], FlextResult[None]]]:
        """Get pipeline operation handler."""
        operation_map: dict[str, Callable[[list[str]], FlextResult[None]]] = {
            "create": self._create_pipeline,
            "run": self._run_pipeline,
            "list": self._list_pipelines,
            "status": self._get_pipeline_status,
            "stop": self._stop_pipeline,
            "delete": self._delete_pipeline,
        }

        handler = operation_map.get(subcommand)
        if handler is None:
            return FlextResult[Callable[[list[str]], FlextResult[None]]].fail(
                f"Unknown pipeline command: {subcommand}"
            )

        return FlextResult[Callable[[list[str]], FlextResult[None]]].ok(handler)

    def _execute_pipeline_operation(
        self, handler: Callable[[list[str]], FlextResult[None]], args: list[str]
    ) -> FlextResult[None]:
        """Execute pipeline operation."""
        return handler(args)

    def _create_pipeline(self, _args: list[str]) -> FlextResult[None]:
        """Create new pipeline."""
        self.logger.info("Pipeline creation not implemented in this refactor")
        return FlextResult[None].ok(None)

    def _run_pipeline(self, _args: list[str]) -> FlextResult[None]:
        """Run pipeline."""
        self.logger.info("Pipeline execution not implemented in this refactor")
        return FlextResult[None].ok(None)

    def _list_pipelines(self, _args: list[str]) -> FlextResult[None]:
        """List pipelines."""
        self.logger.info("Pipeline listing not implemented in this refactor")
        return FlextResult[None].ok(None)

    def _get_pipeline_status(self, _args: list[str]) -> FlextResult[None]:
        """Get pipeline status."""
        self.logger.info("Pipeline status not implemented in this refactor")
        return FlextResult[None].ok(None)

    def _stop_pipeline(self, _args: list[str]) -> FlextResult[None]:
        """Stop pipeline."""
        self.logger.info("Pipeline stopping not implemented in this refactor")
        return FlextResult[None].ok(None)

    def _delete_pipeline(self, _args: list[str]) -> FlextResult[None]:
        """Delete pipeline."""
        self.logger.info("Pipeline deletion not implemented in this refactor")
        return FlextResult[None].ok(None)


class FlextMeltanoSingerManager:
    """SOLID-compliant Singer manager for FLEXT Meltano CLI.

    Single responsibility: handle Singer tap/target CLI commands.
    Uses composition and railway-oriented programming for maintainability.
    """

    def __init__(self, cli: FlextMeltanoCLI) -> None:
        """Initialize Singer manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def handle_tap_command(self, args: list[str]) -> FlextResult[None]:
        """Handle tap command."""
        if not args or args[0] in {"--help", "-h"}:
            self.cli.show_tap_help()
            return FlextResult[None].ok(None)

        subcommand = args[0]
        return self._execute_tap_operation(subcommand, args[1:])

    def handle_target_command(self, args: list[str]) -> FlextResult[None]:
        """Handle target command."""
        if not args or args[0] in {"--help", "-h"}:
            self.cli.show_target_help()
            return FlextResult[None].ok(None)

        subcommand = args[0]
        return self._execute_target_operation(subcommand, args[1:])

    def _execute_tap_operation(
        self,
        operation: str,
        _args: list[str],
    ) -> FlextResult[None]:
        """Execute tap operation."""
        self.logger.info(
            f"Tap operation '{operation}' not implemented in this refactor"
        )
        return FlextResult[None].ok(None)

    def _execute_target_operation(
        self,
        operation: str,
        _args: list[str],
    ) -> FlextResult[None]:
        """Execute target operation."""
        self.logger.info(
            f"Target operation '{operation}' not implemented in this refactor"
        )
        return FlextResult[None].ok(None)


class FlextMeltanoDbtManager:
    """SOLID-compliant DBT manager for FLEXT Meltano CLI.

    Single responsibility: handle DBT CLI commands.
    Uses composition and railway-oriented programming for maintainability.
    """

    def __init__(self, cli: FlextMeltanoCLI) -> None:
        """Initialize DBT manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def handle_command(self, args: list[str]) -> FlextResult[None]:
        """Handle DBT command."""
        if not args or args[0] in {"--help", "-h"}:
            self.cli.show_dbt_help()
            return FlextResult[None].ok(None)

        subcommand = args[0]
        return self._execute_dbt_operation(subcommand, args[1:])

    def _execute_dbt_operation(
        self,
        operation: str,
        _args: list[str],
    ) -> FlextResult[None]:
        """Execute DBT operation."""
        self.logger.info(
            f"DBT operation '{operation}' not implemented in this refactor"
        )
        return FlextResult[None].ok(None)


class FlextMeltanoPluginManager:
    """SOLID-compliant plugin manager for FLEXT Meltano CLI.

    Single responsibility: handle plugin CLI commands.
    Uses composition and railway-oriented programming for maintainability.
    """

    def __init__(self, cli: FlextMeltanoCLI) -> None:
        """Initialize plugin manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def handle_command(self, args: list[str]) -> FlextResult[None]:
        """Handle plugin command."""
        if not args or args[0] in {"--help", "-h"}:
            self.cli.show_plugin_help()
            return FlextResult[None].ok(None)

        subcommand = args[0]
        return self._execute_plugin_operation(subcommand, args[1:])

    def _execute_plugin_operation(
        self,
        operation: str,
        _args: list[str],
    ) -> FlextResult[None]:
        """Execute plugin operation."""
        self.logger.info(
            f"Plugin operation '{operation}' not implemented in this refactor"
        )
        return FlextResult[None].ok(None)


class FlextMeltanoStatusManager:
    """SOLID-compliant status manager for FLEXT Meltano CLI.

    Single responsibility: handle status and monitoring CLI commands.
    Uses composition and railway-oriented programming for maintainability.
    """

    def __init__(self, cli: FlextMeltanoCLI) -> None:
        """Initialize status manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def handle_command(self, args: list[str]) -> FlextResult[None]:
        """Handle status command."""
        if not args or args[0] in {"--help", "-h"}:
            self.cli.show_status_help()
            return FlextResult[None].ok(None)

        subcommand = args[0]
        return self._execute_status_operation(subcommand, args[1:])

    def handle_version_command(self, _args: list[str]) -> FlextResult[None]:
        """Handle version command."""
        self.logger.info("FLEXT Meltano version not implemented in this refactor")
        return FlextResult[None].ok(None)

    def _execute_status_operation(
        self,
        operation: str,
        _args: list[str],
    ) -> FlextResult[None]:
        """Execute status operation."""
        self.logger.info(
            f"Status operation '{operation}' not implemented in this refactor"
        )
        return FlextResult[None].ok(None)


__all__ = [
    "FlextMeltanoCommandRouter",
    "FlextMeltanoDbtManager",
    "FlextMeltanoPipelineManager",
    "FlextMeltanoPluginManager",
    "FlextMeltanoSingerManager",
    "FlextMeltanoStatusManager",
]
