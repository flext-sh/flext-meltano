"""FLEXT Meltano CLI Small Managers - DBT, plugin, and status managers."""

from __future__ import annotations

import json
from collections.abc import (
    Callable,
)
from pathlib import Path
from typing import Final, override

from flext_meltano import (
    FlextMeltanoDbtRunnerMixin,
    FlextMeltanoExecutorBase,
    FlextMeltanoProjectManager,
    FlextMeltanoServiceBase,
    c,
    e,
    p,
    r,
    t,
    u,
)


class _FlextMeltanoCliDbtService(FlextMeltanoDbtRunnerMixin):
    """Execute DBT commands for the CLI manager via the existing runner mixin."""

    def __init__(self) -> None:
        """Initialize DBT CLI helper with configured project root."""
        super().__init__()
        if self.settings.project_root != Path():
            self.configure_dbt_project_root(self.settings.project_root)

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Return current CLI DBT helper state."""
        return r[t.JsonMapping].ok(self.settings.model_dump(mode="json"))

    def run_operation(self, operation: str, args: t.StrSequence) -> p.Result[str]:
        """Execute a DBT subcommand using the runner mixin."""
        normalized_operation = operation.strip().lower()
        command = self._build_dbt_command(
            normalized_operation,
            extra_args=list(args),
        )
        return self._run_dbt_subprocess(command, normalized_operation)


class _FlextMeltanoCliPluginService(FlextMeltanoProjectManager):
    """Provide project-scoped plugin operations for CLI routing."""

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Return current CLI plugin helper state."""
        return r[t.JsonMapping].ok(self.settings.model_dump(mode="json"))

    def _resolve_project_root(self) -> Path:
        """Resolve the project root used for plugin operations."""
        if self.settings.project_root != Path():
            return self.settings.project_root
        return Path.cwd()

    def _load_project(self) -> p.Result[None]:
        """Load the active SDK project before project-scoped operations."""
        return self.load_sdk_project(self._resolve_project_root()).map(lambda _: None)

    @staticmethod
    def _format_plugin_rows(
        plugins: t.SequenceOf[t.JsonMapping],
    ) -> str:
        """Render SDK plugin definitions as deterministic JSON."""
        items: list[dict[str, str]] = []
        for plugin in plugins:
            plugin_name = str(plugin.get("name", "")).strip()
            if not plugin_name:
                continue
            plugin_type = str(plugin.get("type", "")).strip()
            variant = str(plugin.get("variant", "")).strip()
            item: dict[str, str] = {
                "name": plugin_name,
                "type": plugin_type,
            }
            if variant:
                item["variant"] = variant
            items.append(item)
        return json.dumps(items, sort_keys=True)

    def install_plugin(self, plugin_type: str, plugin_name: str) -> p.Result[str]:
        """Install a Meltano plugin using the real Meltano CLI."""
        return FlextMeltanoExecutorBase().execute_meltano_command(
            [c.Meltano.CMD_ADD, plugin_type, plugin_name],
            timeout=c.Meltano.PLUGIN_INSTALLATION_TIMEOUT,
            _cwd=self._resolve_project_root(),
        ).flat_map(
            lambda output: r[str].ok(
                output.output.strip() or f"Installed {plugin_type}:{plugin_name}"
            )
            if output.success
            else r[str].fail(
                u.Meltano.command_failure_message(
                    output, default="Plugin installation failed"
                )
            )
        )

    def fetch_plugin_info(self, plugin_name: str) -> p.Result[str]:
        """Return deterministic plugin information for one installed plugin."""

        def _select_plugin(
            plugins: t.SequenceOf[t.JsonMapping],
        ) -> p.Result[str]:
            for plugin in plugins:
                current_name = str(plugin.get("name", "")).strip()
                if current_name != plugin_name:
                    continue
                plugin_type = str(plugin.get("type", "")).strip()
                variant = str(plugin.get("variant", "")).strip()
                payload: dict[str, str] = {
                    "name": current_name,
                    "type": plugin_type,
                }
                if variant:
                    payload["variant"] = variant
                return r[str].ok(json.dumps(payload, sort_keys=True))
            return e.fail_not_found("Plugin", plugin_name, result_type=r[str])

        return self._load_project().flat_map(
            lambda _: self.fetch_sdk_plugins(None).flat_map(_select_plugin)
        )

    def list_plugins(self, plugin_type: str | None = None) -> p.Result[str]:
        """List installed plugins from the active Meltano project."""
        return self._load_project().flat_map(
            lambda _: self.fetch_sdk_plugins(plugin_type).map(self._format_plugin_rows)
        )


class _FlextMeltanoCliStatusService(FlextMeltanoServiceBase):
    """Provide status and version operations for the CLI manager."""

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Return current CLI status helper state."""
        return r[t.JsonMapping].ok(self.settings.model_dump(mode="json"))

    def _resolve_project_root(self) -> Path | None:
        """Return a project root when one is configured."""
        if self.settings.project_root == Path():
            return None
        return self.settings.project_root

    def _run_version_command(self) -> p.Result[str]:
        """Execute the canonical Meltano version command through the executor DSL."""
        return FlextMeltanoExecutorBase().execute_meltano_command(
            [c.Meltano.ExecutorCommand.VERSION],
            _cwd=self._resolve_project_root(),
        ).flat_map(
            lambda output: r[str].ok((output.output or output.error).strip())
            if output.success
            else r[str].fail(
                u.Meltano.command_failure_message(
                    output, default="Version command failed"
                )
            )
        )

    def fetch_version(self) -> p.Result[str]:
        """Return Meltano version as a string."""
        return self._run_version_command()

    def run_health_check(self) -> p.Result[str]:
        """Use the version command as a real runtime health probe."""
        return self._run_version_command().map(
            lambda version_output: json.dumps(
                {
                    "status": c.Meltano.OperationStatus.HEALTHY,
                    "version": version_output,
                },
                sort_keys=True,
            )
        )

    def show_status(self) -> p.Result[str]:
        """Render configured Meltano status data."""
        payload = {
            "environment": self.settings.environment,
            "meltano_version": self.settings.meltano_version,
            "project_root": str(self._resolve_project_root() or Path.cwd()),
            "status": c.Meltano.OperationStatus.READY,
        }
        return r[str].ok(json.dumps(payload, sort_keys=True))


class _FlextMeltanoSimpleCommandManager:
    """Base for simple command managers with help + unimplemented handlers."""

    logger: p.Logger

    def _handle_command(
        self,
        args: t.StrSequence,
        help_handler: Callable[[], None],
        operation_handler: Callable[[str, t.StrSequence], p.Result[str]],
    ) -> p.Result[str]:
        """Route command to help or operation handler."""
        if u.Meltano.is_help_request(args):
            help_handler()
            return r[str].ok(c.Meltano.ExecutorCommand.HELP)
        return operation_handler(args[0], args[1:])

    def _unsupported_operation(self, label: str, operation: str) -> p.Result[str]:
        """Return an explicit failure for unsupported CLI operations."""
        self.logger.info(
            "%s operation '%s' is not supported by the current CLI manager",
            label,
            operation,
        )
        return r[str].fail(f"{label} operation '{operation}' is not supported")


class FlextMeltanoDbtManager(_FlextMeltanoSimpleCommandManager):
    """Handle DBT CLI commands."""

    def __init__(
        self,
        cli: p.Meltano.DbtCli,
        service: p.Meltano.DbtOperationService | None = None,
    ) -> None:
        """Initialize DBT manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self._service = service or _FlextMeltanoCliDbtService()
        self.logger = u.fetch_logger(__name__)

    def handle_command(self, args: t.StrSequence) -> p.Result[str]:
        """Handle DBT command."""
        return self._handle_command(
            args, self.cli.show_dbt_help, self._execute_dbt_operation
        )

    def _execute_dbt_operation(
        self, operation: str, args: t.StrSequence
    ) -> p.Result[str]:
        if operation not in c.Meltano.DBT_COMMANDS:
            return self._unsupported_operation("DBT", operation)
        return self._service.run_operation(operation, args)


class FlextMeltanoPluginManager(_FlextMeltanoSimpleCommandManager):
    """Handle plugin CLI commands."""

    _PLUGIN_INSTALL_ARG_COUNT: Final[int] = c.Meltano.PLUGIN_INSTALL_ARG_COUNT

    def __init__(
        self,
        cli: p.Meltano.PluginCli,
        service: p.Meltano.PluginOperationService | None = None,
    ) -> None:
        """Initialize plugin manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self._service = service or _FlextMeltanoCliPluginService()
        self.logger = u.fetch_logger(__name__)

    def handle_command(self, args: t.StrSequence) -> p.Result[str]:
        """Handle plugin command."""
        return self._handle_command(
            args, self.cli.show_plugin_help, self._execute_plugin_operation
        )

    def _execute_plugin_operation(
        self, operation: str, args: t.StrSequence
    ) -> p.Result[str]:
        match operation:
            case c.Meltano.ExecutorCommand.LIST:
                plugin_type = args[0] if args else None
                return self._service.list_plugins(plugin_type)
            case "info":
                if not args:
                    return r[str].fail("Plugin info requires a plugin name")
                return self._service.fetch_plugin_info(args[0])
            case c.Meltano.ExecutorCommand.INSTALL:
                if len(args) < self._PLUGIN_INSTALL_ARG_COUNT:
                    return r[str].fail(
                        "Plugin install requires <plugin_type> <plugin_name>",
                    )
                return self._service.install_plugin(args[0], args[1])
            case _:
                return self._unsupported_operation("Plugin", operation)


class FlextMeltanoStatusManager:
    """Handle status and monitoring CLI commands."""

    def __init__(
        self,
        cli: p.Meltano.StatusCli,
        service: p.Meltano.StatusOperationService | None = None,
    ) -> None:
        """Initialize status manager with CLI reference."""
        super().__init__()
        self.cli = cli
        self._service = service or _FlextMeltanoCliStatusService()
        self.logger = u.fetch_logger(__name__)

    def handle_command(self, args: t.StrSequence) -> p.Result[str]:
        """Handle status command."""
        if u.Meltano.is_help_request(args):
            self.cli.show_status_help()
            return r[str].ok(c.Meltano.ExecutorCommand.HELP)
        return self._execute_status_operation(args[0], args[1:])

    def handle_version_command(self, args: t.StrSequence) -> p.Result[str]:
        """Handle version command."""
        _ = args
        return self._service.fetch_version()

    def _execute_status_operation(
        self, operation: str, args: t.StrSequence
    ) -> p.Result[str]:
        _ = args
        if operation in {c.Meltano.CliCommand.STATUS, "show"}:
            return self._service.show_status()
        if operation == c.Meltano.ExecutorCommand.HEALTH:
            return self._service.run_health_check()
        self.logger.info(
            "Status operation '%s' is not supported by the current CLI manager",
            operation,
        )
        return r[str].fail(f"Status operation '{operation}' is not supported")
