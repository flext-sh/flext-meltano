"""FLEXT Meltano Executor - Core command execution service.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import override

from flext_core import r

from flext_meltano import (
    FlextMeltanoCLI,
    FlextMeltanoServiceBase,
    c,
    m,
    t,
    u,
)


class FlextMeltanoExecutor(FlextMeltanoServiceBase):
    """Core executor providing Meltano command execution with error handling."""

    service_name: str = "FlextMeltanoExecutor"

    @property
    def project_root(self) -> Path:
        """Get project root directory - delegates to settings."""
        project_root = getattr(self.settings, "project_root", None)
        if project_root is not None:
            return m.Meltano.PathPayload(value=project_root).value
        return Path.cwd()

    @staticmethod
    def create_flext_cli() -> r[FlextMeltanoCLI]:
        """Create FLEXT CLI instance - delegates to CLI module."""
        try:
            cli = FlextMeltanoCLI()
            return r[FlextMeltanoCLI].ok(cli)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[FlextMeltanoCLI].fail(f"Failed to create CLI: {e}")

    @staticmethod
    def get_version() -> r[str]:
        """Get version information from Meltano CLI."""
        try:
            proc = subprocess.run(
                ["meltano", "version"],  # noqa: S607
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            version = (
                proc.stdout.strip()
                if proc.returncode == 0
                else c.Meltano.Defaults.SERVICE_VERSION
            )
            return r[str].ok(version)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[str].fail(f"Failed to get version: {e}")

    @override
    def execute(self) -> r[t.Meltano.ExecutionResultDict]:
        """Execute the Meltano executor service."""
        try:
            config_data: t.Meltano.ExecutionResultDict = {
                "executor_type": "flext_meltano_executor",
                "status": c.Meltano.Enums.OperationStatus.READY,
                "execution_timestamp": str(time.time()),
                "config": self.settings.model_dump()
                if u.is_pydantic_model(self.settings)
                else dict[str, t.NormalizedValue](),
            }
            self.logger.info("FlextMeltanoExecutor executed successfully")
            return r[t.Meltano.ExecutionResultDict].ok(config_data)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Executor execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.Meltano.ExecutionResultDict].fail(error_msg)

    def execute_meltano_command(
        self,
        command: t.StrSequence,
        timeout: int = c.Meltano.Network.MELTANO_DEFAULT_TIMEOUT,
        _cwd: Path | None = None,
    ) -> r[m.Meltano.CommandExecutionResult]:
        """Execute a Meltano command with timeout and error handling."""
        try:
            start_time = time.time()
            cwd = str(self.project_root) if _cwd is None else str(_cwd)
            self.logger.info(
                "Executing command",
                command=str(command),
                timeout=timeout,
                cwd=cwd,
            )
            proc = subprocess.run(
                list(command),
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                check=False,
            )
            execution_time = time.time() - start_time
            result = m.Meltano.CommandExecutionResult(
                command=command,
                success=proc.returncode == 0,
                exit_code=proc.returncode,
                output=proc.stdout,
                error=proc.stderr,
                execution_time=execution_time,
            )
            return r[m.Meltano.CommandExecutionResult].ok(result)
        except subprocess.TimeoutExpired as e:
            error_msg = f"Command timed out after {timeout}s: {e}"
            self.logger.exception(error_msg)
            return r[m.Meltano.CommandExecutionResult].fail(error_msg)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Command execution failed: {e}"
            self.logger.exception(error_msg)
            return r[m.Meltano.CommandExecutionResult].fail(error_msg)

    def execute_dbt_command(
        self,
        dbt_command: str,
        args: t.StrSequence | None = None,
    ) -> r[m.Meltano.CommandExecutionResult]:
        """Execute a DBT command."""
        try:
            command: list[str] = ["dbt", dbt_command]
            if args:
                command.extend(args)
            return self.execute_meltano_command(command)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[m.Meltano.CommandExecutionResult].fail(f"DBT command failed: {e}")

    def execute_pipeline(
        self,
        tap_name: str,
        target_name: str,
        _config: t.Meltano.MeltanoConfigDict | None = None,
    ) -> r[m.Meltano.CommandExecutionResult]:
        """Execute a complete ELT pipeline."""
        try:
            command: list[str] = ["meltano", "run", tap_name, target_name]
            return self.execute_meltano_command(command)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[m.Meltano.CommandExecutionResult].fail(
                f"Pipeline execution failed: {e}",
            )

    # -- Command routing and convenience methods --

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
