"""FLEXT Meltano Executor - Command routing and convenience methods.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import r

from flext_meltano import c, t
from flext_meltano.services._executor_base import _FlextMeltanoExecutorBase


class FlextMeltanoExecutor(_FlextMeltanoExecutorBase):
    """Core executor providing Meltano command execution with error handling."""

    @staticmethod
    def create_cli_runner(args: t.StrSequence) -> r[t.Meltano.ExecutionResultDict]:
        """Create CLI runner for command execution - static factory."""
        try:
            executor = FlextMeltanoExecutor()
            return (
                executor.run(args)
                if args
                else r[t.Meltano.ExecutionResultDict].ok({
                    "status": c.Meltano.Enums.OperationStatus.READY,
                    "command_type": "cli_runner",
                    "args": args,
                })
            )
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.Meltano.ExecutionResultDict].fail(
                f"Failed to create CLI runner: {e}",
            )

    def health(self) -> r[t.Meltano.ExecutionResultDict]:
        """Check system health by running meltano invoke."""
        result = self.execute_meltano_command(["meltano", "version"])
        return result.map(
            lambda cmd_result: {
                "command": "health",
                "command_type": "health",
                "status": c.Meltano.Enums.OperationStatus.HEALTHY
                if cmd_result.success
                else c.Meltano.Enums.OperationStatus.ERROR,
                "health": "OK" if cmd_result.success else "DEGRADED",
                "exit_code": cmd_result.exit_code,
            },
        )

    def help(self) -> r[t.Meltano.ExecutionResultDict]:
        """Get help information from meltano --help."""
        result = self.execute_meltano_command(["meltano", "--help"])
        return result.map(
            lambda cmd_result: {
                "command": "help",
                "command_type": "help",
                "status": "success" if cmd_result.success else "failed",
                "help": cmd_result.output,
            },
        )

    def run(self, args: t.StrSequence) -> r[t.Meltano.ExecutionResultDict]:
        """Run command with arguments - delegates to command router."""
        if not args:
            return r[t.Meltano.ExecutionResultDict].fail("Arguments cannot be empty")
        return self._route_command(args[0], args[1:])

    def run_cli(self, args: t.StrSequence | None) -> r[t.Meltano.ExecutionResultDict]:
        """Run CLI with arguments - delegates to run or returns help."""
        if args is None or not args:
            return r[t.Meltano.ExecutionResultDict].ok({
                "status": c.Meltano.Enums.OperationStatus.READY,
                "command_type": "cli",
                "message": "CLI ready for commands",
            })
        return self.run(args)

    def run_command(self, args: t.StrSequence) -> r[int]:
        """Execute command and return exit code - delegates to routing."""
        if not args:
            return r[int].ok(1)
        return self._route_command(args[0], args[1:]).map(lambda _: 0)

    def run_pipeline_command(
        self,
        tap_name: str,
        target_name: str,
    ) -> r[t.Meltano.ExecutionResultDict]:
        """Run complete ELT pipeline command."""
        result = self.execute_pipeline(tap_name, target_name)
        return result.map(
            lambda execution_result: {
                "status": "success" if execution_result.success else "failed",
                "command": f"{tap_name} -> {target_name}",
                "exit_code": execution_result.exit_code,
                "output": execution_result.output,
            },
        )

    def version(self) -> r[t.Meltano.ExecutionResultDict]:
        """Get version information from meltano."""
        return self.get_version().map(
            lambda ver: {
                "command": "version",
                "command_type": "version",
                "status": "success",
                "version": ver,
                "success": True,
                "cli_type": "flext_meltano",
            },
        )

    def _route_command(
        self,
        command: str,
        args: t.StrSequence,
    ) -> r[t.Meltano.ExecutionResultDict]:
        """Route command to appropriate handler."""
        if command == "version":
            return self.version()
        if command == "help":
            return self.help()
        if command == "health":
            return self.health()
        full_command: list[str] = ["meltano", command, *args]
        result = self.execute_meltano_command(full_command)
        return result.map(
            lambda cmd_result: {
                "command": command,
                "action": command,
                "args": args,
                "status": c.Meltano.Enums.OperationStatus.EXECUTED
                if cmd_result.success
                else c.Meltano.Enums.OperationStatus.ERROR,
                "exit_code": cmd_result.exit_code,
                "output": cmd_result.output,
                "error": cmd_result.error,
            },
        )


# Backward-compatible alias for code that imported the commands subclass
FlextMeltanoExecutorCommands = FlextMeltanoExecutor

__all__ = ["FlextMeltanoExecutor", "FlextMeltanoExecutorCommands"]
