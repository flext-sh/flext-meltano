"""FLEXT Meltano CLI Managers - SOLID-compliant CLI manager classes.

This module provides focused CLI manager functionality following SOLID principles
with one class per module architecture, consolidated for better organization.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os
import shutil
import signal
import time
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Protocol

from flext_core import FlextLogger, r
from flext_infra import FlextInfraUtilitiesSubprocess

from flext_meltano import c, m, p, t, u


class _CommandRouterCli(Protocol):
    @property
    def pipeline_manager(self) -> p.Meltano.CLIManager: ...

    @property
    def singer_manager(self) -> p.Meltano.SingerManager: ...

    @property
    def dbt_manager(self) -> p.Meltano.CLIManager: ...

    @property
    def plugin_manager(self) -> p.Meltano.CLIManager: ...

    @property
    def status_manager(self) -> p.Meltano.StatusManager: ...

    def show_banner(self) -> None: ...


class _PipelineCli(Protocol):
    def show_pipeline_help(self) -> None: ...


class _SingerCli(Protocol):
    def show_tap_help(self) -> None: ...

    def show_target_help(self) -> None: ...


class _DbtCli(Protocol):
    def show_dbt_help(self) -> None: ...


class _PluginCli(Protocol):
    def show_plugin_help(self) -> None: ...


class _StatusCli(Protocol):
    def show_status_help(self) -> None: ...


class FlextMeltanoCommandRouter:
    """SOLID-compliant command router for FLEXT Meltano CLI.

    Single responsibility: route CLI commands to appropriate handlers.
    Uses composition and railway-oriented programming for maintainability.
    """

    def __init__(self, cli: _CommandRouterCli) -> None:
        """Initialize command router with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    @staticmethod
    def _execute_command(
        handler: Callable[[t.StrSequence], r[str]],
        args: t.StrSequence,
    ) -> r[str]:
        """Execute command handler."""
        return handler(args)

    def route_command(self, args: t.StrSequence) -> int:
        """Route command to appropriate handler using composition."""
        if not args or args[0] in {"--help", "-h"}:
            self.cli.show_banner()
            self.logger.info("FLEXT Meltano CLI - Main Help")
            return 0
        command = args[0]
        command_args = args[1:]
        handler_result = self._get_command_handler(command)
        if handler_result.is_failure:
            self.logger.error(f"Command error: {handler_result.error}")
            return 1
        handler = handler_result.value
        execute_result = self._execute_command(handler, command_args)
        if execute_result.is_failure:
            self.logger.error(f"Execution error: {execute_result.error}")
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


class FlextMeltanoPipelineManager:
    """SOLID-compliant pipeline manager for FLEXT Meltano CLI.

    Single responsibility: handle pipeline-related CLI commands.
    Uses composition and railway-oriented programming for maintainability.
    """

    _PIPELINES_ROOT_ENV = c.Meltano.CliDefaults.PIPELINES_ROOT_ENV
    _PIPELINE_CONFIG_FILE = c.Meltano.CliDefaults.PIPELINE_CONFIG_FILE
    _PIPELINE_PID_FILE = c.Meltano.CliDefaults.PIPELINE_PID_FILE

    def __init__(self, cli: _PipelineCli) -> None:
        """Initialize pipeline manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    @staticmethod
    def _pipelines_root_dir() -> Path:
        configured_root = os.environ.get(
            FlextMeltanoPipelineManager._PIPELINES_ROOT_ENV,
        )
        if configured_root and configured_root.strip():
            return Path(configured_root).expanduser().resolve()
        return (Path.cwd() / ".flext-meltano" / "pipelines").resolve()

    @staticmethod
    def _pipeline_dir(pipeline_name: str) -> Path:
        return FlextMeltanoPipelineManager._pipelines_root_dir() / pipeline_name

    @staticmethod
    def _pipeline_config_path(pipeline_name: str) -> Path:
        return (
            FlextMeltanoPipelineManager._pipeline_dir(pipeline_name)
            / FlextMeltanoPipelineManager._PIPELINE_CONFIG_FILE
        )

    @staticmethod
    def _pipeline_pid_path(pipeline_name: str) -> Path:
        return (
            FlextMeltanoPipelineManager._pipeline_dir(pipeline_name)
            / FlextMeltanoPipelineManager._PIPELINE_PID_FILE
        )

    @staticmethod
    def _execute_pipeline_operation(
        handler: Callable[[t.StrSequence], r[str]],
        args: t.StrSequence,
    ) -> r[str]:
        """Execute pipeline operation."""
        return handler(args)

    @staticmethod
    def create_pipeline(
        pipeline_name: str,
        config: Mapping[
            str,
            t.Scalar | Sequence[t.Scalar | None] | Mapping[str, t.Scalar | None] | None,
        ]
        | None,
    ) -> r[str]:
        """Create a new Meltano pipeline with the given configuration."""
        if not pipeline_name.strip():
            return r[str].fail("Pipeline creation requires a non-empty pipeline name")
        if config is None:
            return r[str].fail("Pipeline creation not configured")
        pipeline_dir = FlextMeltanoPipelineManager._pipeline_dir(pipeline_name)
        if pipeline_dir.exists():
            return r[str].fail(f"Pipeline '{pipeline_name}' already exists")
        try:
            pipeline_dir.mkdir(parents=True, exist_ok=False)
            config_path = FlextMeltanoPipelineManager._pipeline_config_path(
                pipeline_name,
            )
            validated = m.Meltano.ConfigMappingPayload.model_validate({
                "values": dict(config),
            })
            config_path.write_text(
                validated.model_dump_json(indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            return r[str].fail(f"Failed to create pipeline '{pipeline_name}': {exc}")
        return r[str].ok(str(pipeline_dir))

    @staticmethod
    def execute_pipeline(
        pipeline_name: str,
        command_args: t.StrSequence | None = None,
    ) -> r[str]:
        """Execute a Meltano pipeline."""
        pipeline_dir = FlextMeltanoPipelineManager._pipeline_dir(pipeline_name)
        if not pipeline_dir.exists() or not pipeline_dir.is_dir():
            return r[str].fail(f"Pipeline '{pipeline_name}' not found")
        configured_command: t.StrSequence | None = None
        config_path = FlextMeltanoPipelineManager._pipeline_config_path(pipeline_name)
        if config_path.exists():
            try:
                config_mapping = m.Meltano.ConfigMappingPayload.model_validate_json(
                    config_path.read_text(encoding="utf-8"),
                )
            except (ValueError, OSError) as exc:
                return r[str].fail(
                    f"Failed to read pipeline '{pipeline_name}' configuration: {exc}",
                )
            validated_payload = config_mapping.values
            command_value = validated_payload.get("command")
            if isinstance(command_value, list):
                configured_command = m.Meltano.StringListValue.model_validate({
                    "items": command_value,
                }).items
        meltano_args = command_args or configured_command
        if not meltano_args:
            return r[str].fail("Pipeline execution not configured")
        command = ["meltano", *meltano_args]
        runner = FlextInfraUtilitiesSubprocess()
        run_result = runner.run_raw(command, cwd=pipeline_dir)
        if run_result.is_failure:
            error_msg = run_result.error or "Unknown error"
            if "FileNotFoundError" in error_msg or "not found" in error_msg.lower():
                return r[str].fail("Meltano CLI executable not found")
            return r[str].fail(f"Failed to execute Meltano CLI command: {error_msg}")
        completed = run_result.value
        if completed.exit_code != 0:
            command_error = completed.stderr.strip() or completed.stdout.strip()
            if not command_error:
                command_error = (
                    f"Meltano command failed with exit code {completed.exit_code}"
                )
            return r[str].fail(command_error)
        logger = FlextLogger(__name__)
        if completed.stdout.strip():
            logger.info(completed.stdout.strip())
        return r[str].ok(completed.stdout.strip() or "executed")

    @staticmethod
    def list_pipelines() -> r[t.StrSequence]:
        """List all available Meltano pipelines."""
        pipelines_root = FlextMeltanoPipelineManager._pipelines_root_dir()
        if not pipelines_root.exists():
            return r[t.StrSequence].ok([])
        if not pipelines_root.is_dir():
            return r[t.StrSequence].fail(
                f"Pipelines root path is not a directory: {pipelines_root}",
            )
        try:
            pipeline_names = sorted(
                entry.name for entry in pipelines_root.iterdir() if entry.is_dir()
            )
        except OSError as exc:
            return r[t.StrSequence].fail(f"Failed to list pipelines: {exc}")
        return r[t.StrSequence].ok(pipeline_names)

    @staticmethod
    def get_pipeline_status(pipeline_name: str) -> r[str]:
        """Get the status of a specific Meltano pipeline."""
        pipeline_dir = FlextMeltanoPipelineManager._pipeline_dir(pipeline_name)
        if not pipeline_dir.exists() or not pipeline_dir.is_dir():
            return r[str].fail(f"Pipeline '{pipeline_name}' not found")
        pid_path = FlextMeltanoPipelineManager._pipeline_pid_path(pipeline_name)
        if not pid_path.exists():
            return r[str].ok("stopped")
        try:
            pid = int(pid_path.read_text(encoding="utf-8").strip())
        except (ValueError, OSError) as exc:
            return r[str].fail(
                f"Failed to read status for pipeline '{pipeline_name}': {exc}",
            )
        if u.Meltano.is_process_running(pid):
            return r[str].ok("running")
        pid_path.unlink(missing_ok=True)
        return r[str].ok("stopped")

    @staticmethod
    def stop_pipeline(pipeline_name: str, timeout_seconds: float = 10.0) -> r[str]:
        """Stop a running Meltano pipeline."""
        pipeline_dir = FlextMeltanoPipelineManager._pipeline_dir(pipeline_name)
        if not pipeline_dir.exists() or not pipeline_dir.is_dir():
            return r[str].fail(f"Pipeline '{pipeline_name}' not found")
        pid_path = FlextMeltanoPipelineManager._pipeline_pid_path(pipeline_name)
        if not pid_path.exists():
            return r[str].fail(f"Pipeline '{pipeline_name}' is not running")
        try:
            pid = int(pid_path.read_text(encoding="utf-8").strip())
        except (ValueError, OSError) as exc:
            return r[str].fail(
                f"Failed to read PID for pipeline '{pipeline_name}': {exc}",
            )
        if not u.Meltano.is_process_running(pid):
            try:
                pid_path.unlink()
            except FileNotFoundError:
                pass
            except OSError:
                pass
            return r[str].fail(f"Pipeline '{pipeline_name}' is not running")
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            try:
                pid_path.unlink()
            except FileNotFoundError:
                pass
            except OSError:
                pass
            return r[str].fail(f"Pipeline '{pipeline_name}' is not running")
        except OSError as exc:
            return r[str].fail(f"Failed to stop pipeline '{pipeline_name}': {exc}")
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            if not u.Meltano.is_process_running(pid):
                try:
                    pid_path.unlink()
                except FileNotFoundError:
                    pass
                except OSError:
                    pass
                return r[str].ok("stopped")
            time.sleep(0.1)
        return r[str].fail(
            f"Pipeline '{pipeline_name}' did not stop within"
            f" {timeout_seconds:.1f} seconds",
        )

    @staticmethod
    def delete_pipeline(pipeline_name: str) -> r[str]:
        """Delete a Meltano pipeline."""
        pipeline_dir = FlextMeltanoPipelineManager._pipeline_dir(pipeline_name)
        if not pipeline_dir.exists() or not pipeline_dir.is_dir():
            return r[str].fail(f"Pipeline '{pipeline_name}' not found")
        status_result = FlextMeltanoPipelineManager.get_pipeline_status(pipeline_name)
        if status_result.is_failure:
            return r[str].fail(status_result.error)
        if status_result.value == "running":
            return r[str].fail(
                f"Pipeline '{pipeline_name}' is running. Stop it before deletion",
            )
        try:
            shutil.rmtree(pipeline_dir)
        except OSError as exc:
            return r[str].fail(f"Failed to delete pipeline '{pipeline_name}': {exc}")
        if pipeline_dir.exists():
            return r[str].fail(f"Pipeline '{pipeline_name}' deletion was not confirmed")
        return r[str].ok("deleted")

    def handle_command(self, args: t.StrSequence) -> r[str]:
        """Handle pipeline command using composition."""
        if not args or args[0] in {"--help", "-h"}:
            self.cli.show_pipeline_help()
            return r[str].ok("help")
        subcommand = args[0]
        subcommand_args = args[1:]
        handler_result = self._get_pipeline_handler(subcommand)
        if handler_result.is_failure:
            return r[str].fail(handler_result.error)
        handler = handler_result.value
        return self._execute_pipeline_operation(handler, subcommand_args)

    def _create_pipeline(self, _args: t.StrSequence) -> r[str]:
        """Create new pipeline."""
        if not _args:
            return r[str].fail(
                "Pipeline creation requires pipeline name and JSON configuration",
            )
        pipeline_name = _args[0]
        config_payload: (
            Mapping[
                str,
                t.Scalar
                | Sequence[t.Scalar | None]
                | Mapping[str, t.Scalar | None]
                | None,
            ]
            | None
        ) = None
        if len(_args) >= c.Meltano.CliDefaults.MIN_ARGS_WITH_CONFIG:
            try:
                config_mapping = m.Meltano.ConfigMappingPayload.model_validate_json(
                    _args[1],
                )
            except ValueError as exc:
                return r[str].fail(f"Invalid pipeline configuration JSON: {exc}")
            config_payload = config_mapping.values
        result = FlextMeltanoPipelineManager.create_pipeline(
            pipeline_name,
            config_payload,
        )
        if result.is_failure:
            return r[str].fail(result.error)
        self.logger.info("Pipeline created", pipeline=pipeline_name)
        return r[str].ok(result.value)

    def _delete_pipeline(self, _args: t.StrSequence) -> r[str]:
        """Delete pipeline."""
        if not _args:
            return r[str].fail("Pipeline delete requires pipeline name")
        result = FlextMeltanoPipelineManager.delete_pipeline(_args[0])
        if result.is_failure:
            return r[str].fail(result.error)
        return r[str].ok(result.value)

    def _get_pipeline_handler(
        self,
        subcommand: str,
    ) -> r[Callable[[t.StrSequence], r[str]]]:
        """Get pipeline operation handler."""
        operation_map: Mapping[str, Callable[[t.StrSequence], r[str]]] = {
            c.Meltano.Enums.PipelineCommand.CREATE: self._create_pipeline,
            c.Meltano.Enums.PipelineCommand.RUN: self._run_pipeline,
            c.Meltano.Enums.PipelineCommand.LIST: self._list_pipelines,
            c.Meltano.Enums.PipelineCommand.STATUS: self._get_pipeline_status,
            c.Meltano.Enums.PipelineCommand.STOP: self._stop_pipeline,
            c.Meltano.Enums.PipelineCommand.DELETE: self._delete_pipeline,
        }
        handler = operation_map.get(subcommand)
        if handler is None:
            return r[Callable[[t.StrSequence], r[str]]].fail(
                f"Unknown pipeline command: {subcommand}",
            )
        return r[Callable[[t.StrSequence], r[str]]].ok(handler)

    def _get_pipeline_status(self, _args: t.StrSequence) -> r[str]:
        """Get pipeline status."""
        if not _args:
            return r[str].fail("Pipeline status requires pipeline name")
        status_result = FlextMeltanoPipelineManager.get_pipeline_status(_args[0])
        if status_result.is_failure:
            return r[str].fail(status_result.error)
        self.logger.info(
            "Pipeline status",
            pipeline=_args[0],
            status=status_result.value,
        )
        return r[str].ok(status_result.value)

    def _list_pipelines(self, _args: t.StrSequence) -> r[str]:
        """List pipelines."""
        result = FlextMeltanoPipelineManager.list_pipelines()
        if result.is_failure:
            return r[str].fail(result.error)
        self.logger.info("Configured pipelines", pipelines=", ".join(result.value))
        return r[str].ok(", ".join(result.value) or "none")

    def _run_meltano_command(self, command: t.StrSequence) -> r[str]:
        runner = FlextInfraUtilitiesSubprocess()
        run_result = runner.run_raw(command)
        if run_result.is_failure:
            error_msg = run_result.error or "Unknown error"
            if "FileNotFoundError" in error_msg or "not found" in error_msg.lower():
                return r[str].fail("Meltano CLI executable not found")
            return r[str].fail(f"Failed to execute Meltano CLI command: {error_msg}")
        completed = run_result.value
        if completed.exit_code != 0:
            command_error = completed.stderr.strip() or completed.stdout.strip()
            if not command_error:
                command_error = (
                    f"Meltano command failed with exit code {completed.exit_code}"
                )
            self.logger.error(
                "Meltano pipeline command failed",
                command=" ".join(command),
                exit_code=completed.exit_code,
                stderr=completed.stderr,
            )
            return r[str].fail(command_error)
        if completed.stdout.strip():
            self.logger.info(completed.stdout.strip())
        return r[str].ok(completed.stdout.strip() or "executed")

    def _run_pipeline(self, _args: t.StrSequence) -> r[str]:
        """Run pipeline."""
        if not _args:
            return r[str].fail("Pipeline execution requires pipeline name")
        pipeline_name = _args[0]
        command_args = _args[1:] if len(_args) > 1 else None
        result = FlextMeltanoPipelineManager.execute_pipeline(
            pipeline_name,
            command_args,
        )
        if result.is_failure:
            return r[str].fail(result.error)
        return r[str].ok(result.value)

    def _stop_pipeline(self, _args: t.StrSequence) -> r[str]:
        """Stop pipeline."""
        if not _args:
            return r[str].fail("Pipeline stop requires pipeline name")
        result = FlextMeltanoPipelineManager.stop_pipeline(_args[0])
        if result.is_failure:
            return r[str].fail(result.error)
        return r[str].ok(result.value)


class FlextMeltanoSingerManager:
    """SOLID-compliant Singer manager for FLEXT Meltano CLI.

    Single responsibility: handle Singer tap/target CLI commands.
    Uses composition and railway-oriented programming for maintainability.
    """

    def __init__(self, cli: _SingerCli) -> None:
        """Initialize Singer manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def handle_command(self, args: t.StrSequence) -> r[str]:
        """Handle Singer command by routing to tap or target subcommands."""
        if not args or args[0] in {"--help", "-h"}:
            self.cli.show_tap_help()
            return r[str].ok("help")
        subcommand = args[0]
        subcommand_args = args[1:]
        if subcommand == "tap":
            return self.handle_tap_command(subcommand_args)
        if subcommand == "target":
            return self.handle_target_command(subcommand_args)
        return r[str].fail(f"Unknown Singer command: {subcommand}")

    def handle_tap_command(self, args: t.StrSequence) -> r[str]:
        """Handle tap command."""
        if not args or args[0] in {"--help", "-h"}:
            self.cli.show_tap_help()
            return r[str].ok("help")
        subcommand = args[0]
        return self._execute_tap_operation(subcommand, args[1:])

    def handle_target_command(self, args: t.StrSequence) -> r[str]:
        """Handle target command."""
        if not args or args[0] in {"--help", "-h"}:
            self.cli.show_target_help()
            return r[str].ok("help")
        subcommand = args[0]
        return self._execute_target_operation(subcommand, args[1:])

    def _execute_tap_operation(self, operation: str, _args: t.StrSequence) -> r[str]:
        """Execute tap operation."""
        self.logger.info(
            "Tap operation '%s' not implemented in this refactor",
            operation,
        )
        return r[str].ok("not implemented")

    def _execute_target_operation(self, operation: str, _args: t.StrSequence) -> r[str]:
        """Execute target operation."""
        self.logger.info(
            "Target operation '%s' not implemented in this refactor",
            operation,
        )
        return r[str].ok("not implemented")


class _FlextMeltanoSimpleCommandManager:
    logger: FlextLogger

    def _handle_command(
        self,
        args: t.StrSequence,
        help_handler: Callable[[], None],
        operation_handler: Callable[[str, t.StrSequence], r[str]],
    ) -> r[str]:
        if not args or args[0] in {"--help", "-h"}:
            help_handler()
            return r[str].ok("help")
        return operation_handler(args[0], args[1:])

    def _log_unimplemented_operation(
        self,
        operation_label: str,
        operation: str,
    ) -> r[str]:
        self.logger.info(
            "%s operation '%s' not implemented in this refactor",
            operation_label,
            operation,
        )
        return r[str].ok("not implemented")


class FlextMeltanoDbtManager(_FlextMeltanoSimpleCommandManager):
    """SOLID-compliant DBT manager for FLEXT Meltano CLI.

    Single responsibility: handle DBT CLI commands.
    Uses composition and railway-oriented programming for maintainability.
    """

    def __init__(self, cli: _DbtCli) -> None:
        """Initialize DBT manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def handle_command(self, args: t.StrSequence) -> r[str]:
        """Handle DBT command."""
        return self._handle_command(
            args,
            self.cli.show_dbt_help,
            self._execute_dbt_operation,
        )

    def _execute_dbt_operation(self, operation: str, _args: t.StrSequence) -> r[str]:
        """Execute DBT operation."""
        return self._log_unimplemented_operation("DBT", operation)


class FlextMeltanoPluginManager(_FlextMeltanoSimpleCommandManager):
    """SOLID-compliant plugin manager for FLEXT Meltano CLI.

    Single responsibility: handle plugin CLI commands.
    Uses composition and railway-oriented programming for maintainability.
    """

    def __init__(self, cli: _PluginCli) -> None:
        """Initialize plugin manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self.logger = FlextLogger(__name__)

    def handle_command(self, args: t.StrSequence) -> r[str]:
        """Handle plugin command."""
        return self._handle_command(
            args,
            self.cli.show_plugin_help,
            self._execute_plugin_operation,
        )

    def _execute_plugin_operation(self, operation: str, _args: t.StrSequence) -> r[str]:
        """Execute plugin operation."""
        return self._log_unimplemented_operation("Plugin", operation)


class FlextMeltanoStatusManager:
    """SOLID-compliant status manager for FLEXT Meltano CLI.

    Single responsibility: handle status and monitoring CLI commands.
    Uses composition and railway-oriented programming for maintainability.
    """

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
        subcommand = args[0]
        return self._execute_status_operation(subcommand, args[1:])

    def handle_version_command(self, args: t.StrSequence) -> r[str]:
        """Handle version command."""
        _ = args
        self.logger.info("FLEXT Meltano version not implemented in this refactor")
        return r[str].ok("not implemented")

    def _execute_status_operation(self, operation: str, _args: t.StrSequence) -> r[str]:
        """Execute status operation."""
        self.logger.info(
            "Status operation '%s' not implemented in this refactor",
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
