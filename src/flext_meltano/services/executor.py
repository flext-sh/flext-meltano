"""FLEXT Meltano Executor - Command routing and convenience methods.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from meltano.core.error import ProjectNotFound

from flext_core import r
from flext_meltano import FlextMeltanoExecutorBase, c, t, u


class FlextMeltanoExecutor(FlextMeltanoExecutorBase):
    """Core executor providing Meltano command execution with error handling."""

    @staticmethod
    def create_cli_runner(args: t.StrSequence) -> r[t.ContainerMapping]:
        """Create CLI runner for command execution - static factory."""
        try:
            executor = FlextMeltanoExecutor()
            return (
                executor.run(args)
                if args
                else r[t.ContainerMapping].ok({
                    "status": c.Meltano.OperationStatus.READY,
                    "command_type": "cli_runner",
                    "args": list(args),
                })
            )
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.ContainerMapping].fail(
                f"Failed to create CLI runner: {e}",
            )

    def health(self) -> r[t.ContainerMapping]:
        """Check system health by running meltano invoke."""
        result = self.execute_meltano_command([c.Meltano.ExecutorCommand.VERSION])
        return result.map(
            lambda cmd_result: {
                "status": c.Meltano.OperationStatus.HEALTHY
                if cmd_result.success
                else c.Meltano.OperationStatus.ERROR,
                "command": "health",
                "command_type": "health",
                "health": "OK" if cmd_result.success else "DEGRADED",
                "exit_code": cmd_result.exit_code,
            }
        )

    def help(self) -> r[t.ContainerMapping]:
        """Get help information from meltano --help."""
        result = self.execute_meltano_command([c.Meltano.ExecutorCommand.HELP])
        return result.map(
            lambda cmd_result: {
                "status": c.Meltano.OperationStatus.SUCCESS
                if cmd_result.success
                else c.Meltano.OperationStatus.ERROR,
                "command": c.Meltano.ExecutorCommand.HELP,
                "command_type": c.Meltano.ExecutorCommand.HELP,
                "help": cmd_result.output,
            }
        )

    def run(self, args: t.StrSequence) -> r[t.ContainerMapping]:
        """Run command with arguments - delegates to command router."""
        if not args:
            return r[t.ContainerMapping].fail("Arguments cannot be empty")
        return self._route_command(args[0], args[1:])

    def run_cli(self, args: t.StrSequence | None) -> r[t.ContainerMapping]:
        """Run CLI with arguments - delegates to run or returns help."""
        if args is None or not args:
            return r[t.ContainerMapping].ok({
                "status": c.Meltano.OperationStatus.READY,
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
    ) -> r[t.ContainerMapping]:
        """Run complete ELT pipeline command."""
        result = self.execute_pipeline(tap_name, target_name)
        return result.map(
            lambda execution_result: u.Meltano.build_command_execution_payload(
                execution_result,
                extra_fields={"command": f"{tap_name} -> {target_name}"},
                duration_field=None,
            ),
        )

    def version(self) -> r[t.ContainerMapping]:
        """Get version information from meltano."""
        return self.get_version().map(
            lambda ver: {
                "status": c.Meltano.OperationStatus.SUCCESS,
                "command": c.Meltano.ExecutorCommand.VERSION,
                "command_type": c.Meltano.ExecutorCommand.VERSION,
                "version": ver,
                "success": True,
                "cli_type": "flext_meltano",
            }
        )

    def _route_command(
        self,
        command: str,
        args: t.StrSequence,
    ) -> r[t.ContainerMapping]:
        """Route command to appropriate handler."""
        try:
            if command == c.Meltano.ExecutorCommand.VERSION:
                return self.version()
            if command == c.Meltano.ExecutorCommand.HELP:
                return self.help()
            if command == c.Meltano.ExecutorCommand.HEALTH:
                return self.health()
            full_command: list[str] = [command, *args]
            result = self.execute_meltano_command(full_command)
            if result.is_failure:
                return r[t.ContainerMapping].fail(
                    result.error or f"Command '{command}' failed",
                )
            return result.map(
                lambda cmd_result: u.Meltano.build_command_execution_payload(
                    cmd_result,
                    extra_fields={
                        "command": command,
                        "action": command,
                        "args": list(args),
                    },
                    success_status=c.Meltano.OperationStatus.EXECUTED,
                    duration_field=None,
                ),
            )
        except (
            ProjectNotFound,
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
        ) as exc:
            return r[t.ContainerMapping].fail(
                f"Command routing failed: {exc}",
            )


__all__ = ["FlextMeltanoExecutor"]
