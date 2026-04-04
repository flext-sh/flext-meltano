"""FLEXT Meltano Executor - Command routing and convenience methods.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import r
from flext_meltano import FlextMeltanoExecutorBase, c, t, u


class FlextMeltanoExecutor(FlextMeltanoExecutorBase):
    """Core executor providing Meltano command execution with error handling."""

    @staticmethod
    def create_cli_runner(args: t.StrSequence) -> r[t.Meltano.ExecutionResultDict]:
        """Create CLI runner for command execution - static factory."""
        try:
            executor = FlextMeltanoExecutor()
            return (
                executor.run(args)
                if args
                else r[t.Meltano.ExecutionResultDict].ok(
                    u.Meltano.build_status_payload(
                        c.Meltano.Enums.OperationStatus.READY,
                        extra_fields={
                            "command_type": "cli_runner",
                            "args": list(args),
                        },
                    )
                )
            )
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.Meltano.ExecutionResultDict].fail(
                f"Failed to create CLI runner: {e}",
            )

    def health(self) -> r[t.Meltano.ExecutionResultDict]:
        """Check system health by running meltano invoke."""
        result = self.execute_meltano_command([c.Meltano.Enums.ExecutorCommand.VERSION])
        return result.map(
            lambda cmd_result: u.Meltano.build_status_payload(
                c.Meltano.Enums.OperationStatus.HEALTHY
                if cmd_result.success
                else c.Meltano.Enums.OperationStatus.ERROR,
                extra_fields={
                    "command": "health",
                    "command_type": "health",
                    "health": "OK" if cmd_result.success else "DEGRADED",
                    "exit_code": cmd_result.exit_code,
                },
            ),
        )

    def help(self) -> r[t.Meltano.ExecutionResultDict]:
        """Get help information from meltano --help."""
        result = self.execute_meltano_command([c.Meltano.Enums.ExecutorCommand.HELP])
        return result.map(
            lambda cmd_result: u.Meltano.build_status_payload(
                c.Meltano.Enums.OperationStatus.SUCCESS
                if cmd_result.success
                else c.Meltano.Enums.OperationStatus.ERROR,
                extra_fields={
                    "command": c.Meltano.Enums.ExecutorCommand.HELP,
                    "command_type": c.Meltano.Enums.ExecutorCommand.HELP,
                    "help": cmd_result.output,
                },
            ),
        )

    @override
    def run(self, args: t.StrSequence) -> r[t.Meltano.ExecutionResultDict]:
        """Run command with arguments - delegates to command router."""
        if not args:
            return r[t.Meltano.ExecutionResultDict].fail("Arguments cannot be empty")
        return self._route_command(args[0], args[1:])

    def run_cli(self, args: t.StrSequence | None) -> r[t.Meltano.ExecutionResultDict]:
        """Run CLI with arguments - delegates to run or returns help."""
        if args is None or not args:
            return r[t.Meltano.ExecutionResultDict].ok(
                u.Meltano.build_status_payload(
                    c.Meltano.Enums.OperationStatus.READY,
                    extra_fields={
                        "command_type": "cli",
                        "message": "CLI ready for commands",
                    },
                )
            )
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
            lambda execution_result: u.Meltano.build_command_execution_payload(
                execution_result,
                extra_fields={"command": f"{tap_name} -> {target_name}"},
                duration_field=None,
            ),
        )

    def version(self) -> r[t.Meltano.ExecutionResultDict]:
        """Get version information from meltano."""
        return self.get_version().map(
            lambda ver: u.Meltano.build_status_payload(
                c.Meltano.Enums.OperationStatus.SUCCESS,
                extra_fields={
                    "command": c.Meltano.Enums.ExecutorCommand.VERSION,
                    "command_type": c.Meltano.Enums.ExecutorCommand.VERSION,
                    "version": ver,
                    "success": True,
                    "cli_type": "flext_meltano",
                },
            ),
        )

    def _route_command(
        self,
        command: str,
        args: t.StrSequence,
    ) -> r[t.Meltano.ExecutionResultDict]:
        """Route command to appropriate handler."""
        if command == c.Meltano.Enums.ExecutorCommand.VERSION:
            return self.version()
        if command == c.Meltano.Enums.ExecutorCommand.HELP:
            return self.help()
        if command == c.Meltano.Enums.ExecutorCommand.HEALTH:
            return self.health()
        full_command: list[str] = [command, *args]
        result = self.execute_meltano_command(full_command)
        return result.map(
            lambda cmd_result: u.Meltano.build_command_execution_payload(
                cmd_result,
                extra_fields={
                    "command": command,
                    "action": command,
                    "args": list(args),
                },
                success_status=c.Meltano.Enums.OperationStatus.EXECUTED,
                duration_field=None,
            ),
        )


__all__ = ["FlextMeltanoExecutor"]
