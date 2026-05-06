"""FLEXT Meltano Executor - Command routing and convenience methods.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from meltano.core.error import ProjectNotFound

from flext_meltano import (
    FlextMeltanoExecutorBase,
    FlextMeltanoSettings,
    c,
    p,
    r,
    t,
    u,
)


class FlextMeltanoExecutor(FlextMeltanoExecutorBase):
    """Core executor providing Meltano command execution with error handling."""

    def __init__(
        self,
        settings: FlextMeltanoSettings | None = None,
        *,
        service_name: t.NonEmptyStr | None = None,
        service_version: t.NonEmptyStr | None = None,
        source_name: str | None = None,
        sink_name: str | None = None,
        transformation_name: str | None = None,
    ) -> None:
        """Forward canonical Meltano service kwargs through ``FlextMeltanoExecutorBase``."""
        super().__init__(
            settings=settings,
            service_name=service_name,
            service_version=service_version,
            source_name=source_name,
            sink_name=sink_name,
            transformation_name=transformation_name,
        )

    @staticmethod
    def create_cli_runner(args: t.StrSequence) -> p.Result[t.JsonMapping]:
        """Create CLI runner for command execution - static factory."""
        try:
            executor = FlextMeltanoExecutor()
            args_payload: list[t.JsonValue] = list(args)
            ready_payload: t.JsonDict = {
                "status": c.Meltano.OperationStatus.READY,
                "command_type": "cli_runner",
                "args": args_payload,
            }
            return (
                executor.run(args).map(t.Cli.JSON_MAPPING_ADAPTER.validate_python)
                if args
                else r[t.JsonMapping].ok(ready_payload)
            )
        except c.Meltano.OPERATION_ERRORS as e:
            return r[t.JsonMapping].fail(
                f"Failed to create CLI runner: {e}",
            )

    def health(self) -> p.Result[t.JsonMapping]:
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

    def help(self) -> p.Result[t.JsonMapping]:
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

    def run(self, args: t.StrSequence) -> p.Result[t.JsonMapping]:
        """Run command with arguments - delegates to command router."""
        if not args:
            return r[t.JsonMapping].fail("Arguments cannot be empty")
        return self._route_command(args[0], args[1:])

    def run_cli(self, args: t.StrSequence | None) -> p.Result[t.JsonMapping]:
        """Run CLI with arguments - delegates to run or returns help."""
        if args is None or not args:
            ready_payload: t.JsonMapping = {
                "status": c.Meltano.OperationStatus.READY,
                "command_type": "cli",
                "message": "CLI ready for commands",
            }
            return r[t.JsonMapping].ok(ready_payload)
        return self.run(args)

    def run_command(self, args: t.StrSequence) -> p.Result[int]:
        """Execute command and return exit code - delegates to routing."""
        if not args:
            return r[int].ok(1)
        return self._route_command(args[0], args[1:]).map(lambda _: 0)

    def run_pipeline_command(
        self,
        tap_name: str,
        target_name: str,
    ) -> p.Result[t.JsonMapping]:
        """Run complete ELT pipeline command."""
        result = self.execute_pipeline(tap_name, target_name)
        return result.map(
            lambda execution_result: u.Meltano.build_command_execution_payload(
                execution_result,
                extra_fields={"command": f"{tap_name} -> {target_name}"},
                duration_field=None,
            ),
        )

    def version(self) -> p.Result[t.JsonMapping]:
        """Get version information from meltano."""
        return self.fetch_version().map(
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
    ) -> p.Result[t.JsonMapping]:
        """Route command to appropriate handler."""
        try:
            match command:
                case c.Meltano.ExecutorCommand.VERSION:
                    return self.version()
                case c.Meltano.ExecutorCommand.HELP:
                    return self.help()
                case c.Meltano.ExecutorCommand.HEALTH:
                    return self.health()
                case _:
                    full_command: list[str] = [command, *args]
                    result = self.execute_meltano_command(full_command)
                    if result.failure:
                        return r[t.JsonMapping].fail(
                            result.error or f"Command '{command}' failed",
                        )
                    args_payload: list[t.JsonValue] = list(args)
                    extra_fields: t.JsonDict = {
                        "command": command,
                        "action": command,
                        "args": args_payload,
                    }
                    return result.map(
                        lambda cmd_result: u.Meltano.build_command_execution_payload(
                            cmd_result,
                            extra_fields=extra_fields,
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
            return r[t.JsonMapping].fail_op("Command routing", exc)


__all__: list[str] = ["FlextMeltanoExecutor"]
