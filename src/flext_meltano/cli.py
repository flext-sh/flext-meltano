"""FLEXT Meltano CLI public facade."""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Annotated

from flext_cli import cli as flext_cli_output
from flext_meltano import FlextMeltano, c, p, r, t, u
from flext_meltano.pipeline_mgr import FlextMeltanoPipelineManager


class FlextMeltanoCLI(FlextMeltano):
    """Flat public CLI facade for FLEXT Meltano operations."""

    service_name: Annotated[
        t.NonEmptyStr,
        u.Field(
            default="FlextMeltanoCLI",
            description="Canonical Meltano CLI service name.",
            validate_default=True,
        ),
    ] = "FlextMeltanoCLI"

    def handle_pipeline_command(self, args: t.StrSequence) -> p.Result[str]:
        """Handle top-level pipeline commands through the public CLI."""
        return FlextMeltanoPipelineManager(self).handle_command(args)

    def handle_tap_command(self, args: t.StrSequence) -> p.Result[str]:
        """Handle top-level tap commands through the public CLI."""
        if not args or u.Meltano.is_help_request(args):
            self.show_tap_help()
            return r[str].ok(c.Meltano.ExecutorCommand.HELP.value)
        return r[str].fail(f"Tap operation '{args[0]}' is not supported")

    def handle_target_command(self, args: t.StrSequence) -> p.Result[str]:
        """Handle top-level target commands through the public CLI."""
        if not args or u.Meltano.is_help_request(args):
            self.show_target_help()
            return r[str].ok(c.Meltano.ExecutorCommand.HELP.value)
        return r[str].fail(f"Target operation '{args[0]}' is not supported")

    def handle_dbt_command(self, args: t.StrSequence) -> p.Result[str]:
        """Handle top-level DBT commands through the public CLI."""
        if not args or u.Meltano.is_help_request(args):
            self.show_dbt_help()
            return r[str].ok(c.Meltano.ExecutorCommand.HELP.value)
        result = self.execute_dbt_command(args[0], args[1:])
        if result.failure:
            return r[str].fail(result.error or "DBT command failed")
        if not result.value.success:
            return r[str].fail(result.value.error or result.value.output)
        return r[str].ok(result.value.output)

    def handle_plugin_command(self, args: t.StrSequence) -> p.Result[str]:
        """Handle top-level plugin commands through the public CLI."""
        if not args or u.Meltano.is_help_request(args):
            self.show_plugin_help()
            result = r[str].ok(c.Meltano.ExecutorCommand.HELP.value)
        else:
            command, command_args = args[0], args[1:]
            match command:
                case c.Meltano.ExecutorCommand.LIST:
                    plugin_type = (
                        u.Meltano.normalize_plugin_group(command_args[0])
                        if command_args
                        else None
                    )
                    result = (
                        self
                        .discover_plugins()
                        .map(
                            lambda plugins: [
                                t.json_dict_adapter().validate_python(plugin)
                                for plugin in plugins
                                if plugin_type is None
                                or plugin.get("type") == plugin_type
                            ]
                        )
                        .flat_map(
                            lambda payload: u.Cli.json_dumps(
                                list(t.Cli.JSON_LIST_ADAPTER.validate_python(payload))
                            )
                        )
                    )
                case c.Meltano.ExecutorCommand.INFO:
                    if len(command_args) < c.Meltano.PLUGIN_INFO_ARG_COUNT:
                        result = r[str].fail(
                            "Plugin info requires plugin type and plugin name"
                        )
                    else:
                        plugin_type = u.Meltano.normalize_plugin_group(command_args[0])
                        result = (
                            r[str].fail("Plugin info requires a valid plugin type")
                            if plugin_type is None
                            else self.fetch_plugin_info(
                                command_args[1],
                                plugin_type,
                            ).flat_map(
                                lambda payload: u.Cli.json_dumps(
                                    t.json_dict_adapter().validate_python(payload),
                                )
                            )
                        )
                case c.Meltano.ExecutorCommand.INSTALL:
                    result = r[str].fail("Plugin install is not supported by this CLI")
                case _:
                    result = r[str].fail(f"Unknown plugin command: {command}")
        return result

    def handle_status_command(self, args: t.StrSequence) -> p.Result[str]:
        """Handle top-level status commands through the public CLI."""
        if not args or u.Meltano.is_help_request(args):
            self.show_status_help()
            return r[str].ok(c.Meltano.ExecutorCommand.HELP.value)
        match args[0]:
            case "show":
                return self.run_cli([]).flat_map(
                    lambda payload: u.Cli.json_dumps(
                        t.json_dict_adapter().validate_python(payload),
                    )
                )
            case c.Meltano.ExecutorCommand.HEALTH:
                return self.health().flat_map(
                    lambda payload: u.Cli.json_dumps(
                        t.json_dict_adapter().validate_python(payload),
                    )
                )
            case _:
                return r[str].fail(f"Unknown status command: {args[0]}")

    def handle_version_command(self, args: t.StrSequence) -> p.Result[str]:
        """Handle top-level version commands through the public CLI."""
        if args and not u.Meltano.is_help_request(args):
            return r[str].fail("Version command does not accept arguments")
        return self.fetch_version()

    def route_command(self, args: t.StrSequence) -> int:
        """Route one CLI command through the flat public handlers."""
        if not args or u.Meltano.is_help_request(args):
            self.show_banner()
            return 0
        command_map: dict[str, Callable[[t.StrSequence], p.Result[str]]] = {
            c.Meltano.CliCommand.PIPELINE: self.handle_pipeline_command,
            c.Meltano.CliCommand.TAP: self.handle_tap_command,
            c.Meltano.CliCommand.TARGET: self.handle_target_command,
            c.Meltano.CliCommand.DBT: self.handle_dbt_command,
            c.Meltano.CliCommand.PLUGIN: self.handle_plugin_command,
            c.Meltano.CliCommand.STATUS: self.handle_status_command,
            c.Meltano.CliCommand.VERSION: self.handle_version_command,
        }
        handler = command_map.get(args[0])
        if handler is None:
            self.print_message(f"Unknown command: {args[0]}")
            return 1
        result = handler(args[1:])
        if result.failure:
            self.print_message(str(result.error))
            return 1
        if result.value != c.Meltano.ExecutorCommand.HELP.value:
            self.print_message(result.value)
        return 0

    def show_banner(self) -> None:
        """Render the root CLI banner."""
        flext_cli_output.print("FLEXT Meltano CLI")
        flext_cli_output.print(
            "Commands: pipeline, tap, target, dbt, plugin, status, version"
        )

    def show_dbt_help(self) -> None:
        """Render DBT help."""
        flext_cli_output.print("dbt <run|test|compile|docs> [args]")

    def show_pipeline_help(self) -> None:
        """Render pipeline help."""
        flext_cli_output.print("pipeline <create|run|list|status|stop|delete> [args]")

    def show_plugin_help(self) -> None:
        """Render plugin help."""
        flext_cli_output.print("plugin <list|info|install> [args]")

    def show_status_help(self) -> None:
        """Render status help."""
        flext_cli_output.print("status <show|health>")

    def show_tap_help(self) -> None:
        """Render tap help."""
        flext_cli_output.print("tap <operation> [args]")

    def show_target_help(self) -> None:
        """Render target help."""
        flext_cli_output.print("target <operation> [args]")

    def print_message(self, message: str, style: str | None = None) -> None:
        """Render a CLI message through flext-cli output."""
        flext_cli_output.print(message, style=style)

    def main(self, args: t.StrSequence | None = None) -> int:
        """Run the public CLI entrypoint."""
        active_args = list(args) if args is not None else sys.argv[1:]
        return self.route_command(active_args)


def main() -> int:
    """Main entry point for FLEXT Meltano CLI."""
    return FlextMeltanoCLI.fetch_global().main()


cli = FlextMeltanoCLI.fetch_global()


__all__: list[str] = ["FlextMeltanoCLI", "cli", "main"]
