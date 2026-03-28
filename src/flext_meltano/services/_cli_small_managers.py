"""FLEXT Meltano CLI Small Managers - DBT, plugin, and status managers.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from flext_core import FlextLogger, r

from flext_meltano import t


class _DbtCli(Protocol):
    """Protocol for DBT CLI help display."""

    def show_dbt_help(self) -> None: ...


class _PluginCli(Protocol):
    """Protocol for plugin CLI help display."""

    def show_plugin_help(self) -> None: ...


class _StatusCli(Protocol):
    """Protocol for status CLI help display."""

    def show_status_help(self) -> None: ...


class _FlextMeltanoSimpleCommandManager:
    """Base for simple command managers with help + unimplemented handlers."""

    logger: FlextLogger

    def _handle_command(
        self,
        args: t.StrSequence,
        help_handler: Callable[[], None],
        operation_handler: Callable[[str, t.StrSequence], r[str]],
    ) -> r[str]:
        """Route command to help or operation handler."""
        if not args or args[0] in {"--help", "-h"}:
            help_handler()
            return r[str].ok("help")
        return operation_handler(args[0], args[1:])

    def _log_unimplemented(self, label: str, operation: str) -> r[str]:
        """Log and return 'not implemented' for stub operations."""
        self.logger.info(
            "%s operation '%s' not implemented in this refactor", label, operation
        )
        return r[str].ok("not implemented")


class FlextMeltanoDbtManager(_FlextMeltanoSimpleCommandManager):
    """Handle DBT CLI commands."""

    def __init__(self, cli: _DbtCli) -> None:
        """Initialize DBT manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def handle_command(self, args: t.StrSequence) -> r[str]:
        """Handle DBT command."""
        return self._handle_command(
            args, self.cli.show_dbt_help, self._execute_dbt_operation
        )

    def _execute_dbt_operation(self, operation: str, _args: t.StrSequence) -> r[str]:
        return self._log_unimplemented("DBT", operation)


class FlextMeltanoPluginManager(_FlextMeltanoSimpleCommandManager):
    """Handle plugin CLI commands."""

    def __init__(self, cli: _PluginCli) -> None:
        """Initialize plugin manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def handle_command(self, args: t.StrSequence) -> r[str]:
        """Handle plugin command."""
        return self._handle_command(
            args, self.cli.show_plugin_help, self._execute_plugin_operation
        )

    def _execute_plugin_operation(self, operation: str, _args: t.StrSequence) -> r[str]:
        return self._log_unimplemented("Plugin", operation)


class FlextMeltanoStatusManager:
    """Handle status and monitoring CLI commands."""

    def __init__(self, cli: _StatusCli) -> None:
        """Initialize status manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def handle_command(self, args: t.StrSequence) -> r[str]:
        """Handle status command."""
        if not args or args[0] in {"--help", "-h"}:
            self.cli.show_status_help()
            return r[str].ok("help")
        return self._execute_status_operation(args[0], args[1:])

    def handle_version_command(self, args: t.StrSequence) -> r[str]:
        """Handle version command."""
        _ = args
        self.logger.info("FLEXT Meltano version not implemented in this refactor")
        return r[str].ok("not implemented")

    def _execute_status_operation(self, operation: str, _args: t.StrSequence) -> r[str]:
        self.logger.info(
            "Status operation '%s' not implemented in this refactor", operation
        )
        return r[str].ok("not implemented")
