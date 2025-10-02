"""FLEXT Meltano CLI - Professional Command-Line Interface.

Comprehensive CLI for Meltano/Singer/DBT operations using flext-cli exclusively.
ZERO TOLERANCE: NO direct click/rich/typer imports allowed.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys

from flext_cli import FlextCli
from flext_core import FlextLogger, FlextResult
from flext_meltano.api import FlextMeltanoAPI


class FlextMeltanoCLI:
    """Professional CLI for FLEXT Meltano operations using flext-cli exclusively.

    Provides comprehensive command-line interface for:
    - Pipeline management (create, execute, monitor)
    - Singer tap/target operations (run, configure, test)
    - DBT model operations (run, test, document)
    - Plugin management (install, list, configure)
    - Status and monitoring (health, metrics, logs)

    ZERO TOLERANCE: Uses flext-cli for ALL CLI operations.
    """

    def __init__(self) -> None:
        """Initialize CLI with flext-cli API and Meltano API."""
        self._cli = FlextCli()
        self._logger = FlextLogger(__name__)
        self._api = FlextMeltanoAPI()

    # =============================================================================
    # MAIN CLI ENTRY POINT
    # =============================================================================

    def main(self, args: list[str] | None = None) -> int:
        """Main CLI entry point.

        Args:
            args: Command-line arguments (defaults to sys.argv[1:])

        Returns:
            Exit code (0 for success, non-zero for failure)

        """
        if args is None:
            args = sys.argv[1:]

        # Show banner for main command
        if not args or args[0] in {"--help", "-h"}:
            self._show_banner()
            self._show_main_help()
            return 0

        # Route to command handlers
        command = args[0]
        command_args = args[1:]

        command_map = {
            "pipeline": self._handle_pipeline_command,
            "tap": self._handle_tap_command,
            "target": self._handle_target_command,
            "dbt": self._handle_dbt_command,
            "plugin": self._handle_plugin_command,
            "status": self._handle_status_command,
            "version": self._handle_version_command,
        }

        handler = command_map.get(command)
        if not handler:
            self._cli.error(f"Unknown command: {command}")
            self._show_main_help()
            return 1

        try:
            result = handler(command_args)
            return 0 if result.is_success else 1
        except Exception:
            self._logger.exception("Command failed")
            self._cli.error("Command failed")
            return 1

    # =============================================================================
    # PIPELINE COMMANDS
    # =============================================================================

    def _handle_pipeline_command(self, args: list[str]) -> FlextResult[None]:
        """Handle pipeline subcommands."""
        if not args or args[0] in {"--help", "-h"}:
            self._show_pipeline_help()
            return FlextResult[None].ok(None)

        subcommand = args[0]
        subcommand_args = args[1:]

        if subcommand == "create":
            return self._pipeline_create(subcommand_args)
        if subcommand == "execute":
            return self._pipeline_execute(subcommand_args)
        if subcommand == "list":
            return self._pipeline_list(subcommand_args)

        self._cli.error(f"Unknown pipeline subcommand: {subcommand}")
        self._show_pipeline_help()
        return FlextResult[None].fail(f"Unknown subcommand: {subcommand}")

    def _pipeline_create(self, args: list[str]) -> FlextResult[None]:
        """Create a new pipeline."""
        # Parse arguments
        parsed = self._parse_pipeline_create_args(args)
        if not parsed:
            return FlextResult[None].fail("Invalid arguments")

        name, tap, target, transform = parsed

        self._cli.info(f"Creating pipeline: {name}")
        self._cli.info(f"  Tap: {tap}")
        self._cli.info(f"  Target: {target}")
        if transform:
            self._cli.info(f"  Transform: {transform}")

        # Create pipeline via API
        result = self._api.create_pipeline(
            name=name,
            tap_name=tap,
            target_name=target,
            transform_name=transform,
        )

        if result.is_failure:
            self._cli.error(f"Pipeline creation failed: {result.error}")
            return FlextResult[None].fail(result.error)

        self._cli.success(f"Pipeline '{name}' created successfully")
        return FlextResult[None].ok(None)

    def _pipeline_execute(self, args: list[str]) -> FlextResult[None]:
        """Execute a pipeline."""
        if not args:
            self._cli.error("Pipeline name required")
            return FlextResult[None].fail("Missing pipeline name")

        pipeline_name = args[0]

        self._cli.info(f"Executing pipeline: {pipeline_name}")

        # Execute pipeline via API
        result = self._api.execute_pipeline(pipeline_name=pipeline_name)

        if result.is_failure:
            self._cli.error(f"Pipeline execution failed: {result.error}")
            return FlextResult[None].fail(result.error)

        execution_data = result.unwrap()
        self._cli.success("Pipeline executed successfully")

        # Display execution metrics
        self._display_execution_metrics(execution_data)

        return FlextResult[None].ok(None)

    def _pipeline_list(self, _args: list[str]) -> FlextResult[None]:
        """List available pipelines."""
        self._cli.info("Listing pipelines...")

        # Get pipelines via API
        result = self._api.list_pipelines()

        if result.is_failure:
            self._cli.error(f"Failed to list pipelines: {result.error}")
            return FlextResult[None].fail(result.error)

        pipelines = result.unwrap()

        if not pipelines:
            self._cli.warning("No pipelines configured")
            return FlextResult[None].ok(None)

        # Display pipelines in table format
        self._display_pipelines_table(pipelines)

        return FlextResult[None].ok(None)

    # =============================================================================
    # TAP COMMANDS
    # =============================================================================

    def _handle_tap_command(self, args: list[str]) -> FlextResult[None]:
        """Handle tap subcommands."""
        if not args or args[0] in {"--help", "-h"}:
            self._show_tap_help()
            return FlextResult[None].ok(None)

        subcommand = args[0]
        subcommand_args = args[1:]

        if subcommand == "run":
            return self._tap_run(subcommand_args)
        if subcommand == "list":
            return self._tap_list(subcommand_args)
        if subcommand == "install":
            return self._tap_install(subcommand_args)

        self._cli.error(f"Unknown tap subcommand: {subcommand}")
        self._show_tap_help()
        return FlextResult[None].fail(f"Unknown subcommand: {subcommand}")

    def _tap_run(self, args: list[str]) -> FlextResult[None]:
        """Run a Singer tap."""
        if not args:
            self._cli.error("Tap name required")
            return FlextResult[None].fail("Missing tap name")

        tap_name = args[0]
        config_file = self._parse_config_arg(args[1:])

        self._cli.info(f"Running tap: {tap_name}")
        if config_file:
            self._cli.info(f"  Config: {config_file}")

        # Run tap via API
        result = self._api.run_tap(tap_name=tap_name, config_path=config_file)

        if result.is_failure:
            self._cli.error(f"Tap execution failed: {result.error}")
            return FlextResult[None].fail(result.error)

        tap_data = result.unwrap()
        self._cli.success(f"Tap '{tap_name}' completed successfully")

        # Display tap metrics
        self._display_tap_metrics(tap_data)

        return FlextResult[None].ok(None)

    def _tap_list(self, _args: list[str]) -> FlextResult[None]:
        """List available taps."""
        self._cli.info("Listing available taps...")

        # Get taps via API
        result = self._api.list_plugins(plugin_type="extractors")

        if result.is_failure:
            self._cli.error(f"Failed to list taps: {result.error}")
            return FlextResult[None].fail(result.error)

        taps = result.unwrap()

        if not taps:
            self._cli.warning("No taps installed")
            return FlextResult[None].ok(None)

        # Display taps in table format
        self._display_plugins_table(taps, "Taps")

        return FlextResult[None].ok(None)

    def _tap_install(self, args: list[str]) -> FlextResult[None]:
        """Install a Singer tap."""
        if not args:
            self._cli.error("Tap name required")
            return FlextResult[None].fail("Missing tap name")

        tap_name = args[0]

        self._cli.info(f"Installing tap: {tap_name}")

        # Install tap via API
        result = self._api.install_plugin(plugin_type="extractor", plugin_name=tap_name)

        if result.is_failure:
            self._cli.error(f"Tap installation failed: {result.error}")
            return FlextResult[None].fail(result.error)

        self._cli.success(f"Tap '{tap_name}' installed successfully")
        return FlextResult[None].ok(None)

    # =============================================================================
    # TARGET COMMANDS
    # =============================================================================

    def _handle_target_command(self, args: list[str]) -> FlextResult[None]:
        """Handle target subcommands."""
        if not args or args[0] in {"--help", "-h"}:
            self._show_target_help()
            return FlextResult[None].ok(None)

        subcommand = args[0]
        subcommand_args = args[1:]

        if subcommand == "run":
            return self._target_run(subcommand_args)
        if subcommand == "list":
            return self._target_list(subcommand_args)
        if subcommand == "install":
            return self._target_install(subcommand_args)

        self._cli.error(f"Unknown target subcommand: {subcommand}")
        self._show_target_help()
        return FlextResult[None].fail(f"Unknown subcommand: {subcommand}")

    def _target_run(self, args: list[str]) -> FlextResult[None]:
        """Run a Singer target."""
        if not args:
            self._cli.error("Target name required")
            return FlextResult[None].fail("Missing target name")

        target_name = args[0]
        config_file = self._parse_config_arg(args[1:])

        self._cli.info(f"Running target: {target_name}")
        if config_file:
            self._cli.info(f"  Config: {config_file}")

        # Run target via API
        result = self._api.run_target(target_name=target_name, config_path=config_file)

        if result.is_failure:
            self._cli.error(f"Target execution failed: {result.error}")
            return FlextResult[None].fail(result.error)

        target_data = result.unwrap()
        self._cli.success(f"Target '{target_name}' completed successfully")

        # Display target metrics
        self._display_target_metrics(target_data)

        return FlextResult[None].ok(None)

    def _target_list(self, _args: list[str]) -> FlextResult[None]:
        """List available targets."""
        self._cli.info("Listing available targets...")

        # Get targets via API
        result = self._api.list_plugins(plugin_type="loaders")

        if result.is_failure:
            self._cli.error(f"Failed to list targets: {result.error}")
            return FlextResult[None].fail(result.error)

        targets = result.unwrap()

        if not targets:
            self._cli.warning("No targets installed")
            return FlextResult[None].ok(None)

        # Display targets in table format
        self._display_plugins_table(targets, "Targets")

        return FlextResult[None].ok(None)

    def _target_install(self, args: list[str]) -> FlextResult[None]:
        """Install a Singer target."""
        if not args:
            self._cli.error("Target name required")
            return FlextResult[None].fail("Missing target name")

        target_name = args[0]

        self._cli.info(f"Installing target: {target_name}")

        # Install target via API
        result = self._api.install_plugin(plugin_type="loader", plugin_name=target_name)

        if result.is_failure:
            self._cli.error(f"Target installation failed: {result.error}")
            return FlextResult[None].fail(result.error)

        self._cli.success(f"Target '{target_name}' installed successfully")
        return FlextResult[None].ok(None)

    # =============================================================================
    # DBT COMMANDS
    # =============================================================================

    def _handle_dbt_command(self, args: list[str]) -> FlextResult[None]:
        """Handle DBT subcommands."""
        if not args or args[0] in {"--help", "-h"}:
            self._show_dbt_help()
            return FlextResult[None].ok(None)

        subcommand = args[0]
        subcommand_args = args[1:]

        if subcommand == "run":
            return self._dbt_run(subcommand_args)
        if subcommand == "test":
            return self._dbt_test(subcommand_args)
        if subcommand == "docs":
            return self._dbt_docs(subcommand_args)

        self._cli.error(f"Unknown dbt subcommand: {subcommand}")
        self._show_dbt_help()
        return FlextResult[None].fail(f"Unknown subcommand: {subcommand}")

    def _dbt_run(self, args: list[str]) -> FlextResult[None]:
        """Run DBT models."""
        models = self._parse_models_arg(args)

        self._cli.info("Running DBT models...")
        if models:
            self._cli.info(f"  Models: {', '.join(models)}")

        # Run DBT via API
        result = self._api.run_dbt_models(models=models or None)

        if result.is_failure:
            self._cli.error(f"DBT run failed: {result.error}")
            return FlextResult[None].fail(result.error)

        dbt_data = result.unwrap()
        self._cli.success("DBT models executed successfully")

        # Display DBT metrics
        self._display_dbt_metrics(dbt_data)

        return FlextResult[None].ok(None)

    def _dbt_test(self, args: list[str]) -> FlextResult[None]:
        """Test DBT models."""
        models = self._parse_models_arg(args)

        self._cli.info("Testing DBT models...")
        if models:
            self._cli.info(f"  Models: {', '.join(models)}")

        # Test DBT via API
        result = self._api.test_dbt_models(models=models or None)

        if result.is_failure:
            self._cli.error(f"DBT test failed: {result.error}")
            return FlextResult[None].fail(result.error)

        test_data = result.unwrap()
        self._cli.success("DBT tests completed successfully")

        # Display test results
        self._display_dbt_test_results(test_data)

        return FlextResult[None].ok(None)

    def _dbt_docs(self, _args: list[str]) -> FlextResult[None]:
        """Generate DBT documentation."""
        self._cli.info("Generating DBT documentation...")

        # Generate docs via API
        result = self._api.generate_dbt_docs()

        if result.is_failure:
            self._cli.error(f"DBT docs generation failed: {result.error}")
            return FlextResult[None].fail(result.error)

        self._cli.success("DBT documentation generated successfully")
        return FlextResult[None].ok(None)

    # =============================================================================
    # PLUGIN COMMANDS
    # =============================================================================

    def _handle_plugin_command(self, args: list[str]) -> FlextResult[None]:
        """Handle plugin subcommands."""
        if not args or args[0] in {"--help", "-h"}:
            self._show_plugin_help()
            return FlextResult[None].ok(None)

        subcommand = args[0]
        subcommand_args = args[1:]

        if subcommand == "list":
            return self._plugin_list(subcommand_args)
        if subcommand == "install":
            return self._plugin_install(subcommand_args)

        self._cli.error(f"Unknown plugin subcommand: {subcommand}")
        self._show_plugin_help()
        return FlextResult[None].fail(f"Unknown subcommand: {subcommand}")

    def _plugin_list(self, _args: list[str]) -> FlextResult[None]:
        """List all installed plugins."""
        self._cli.info("Listing all plugins...")

        # Get all plugins via API
        result = self._api.list_plugins()

        if result.is_failure:
            self._cli.error(f"Failed to list plugins: {result.error}")
            return FlextResult[None].fail(result.error)

        plugins = result.unwrap()

        if not plugins:
            self._cli.warning("No plugins installed")
            return FlextResult[None].ok(None)

        # Display plugins in table format
        self._display_plugins_table(plugins, "Plugins")

        return FlextResult[None].ok(None)

    def _plugin_install(self, args: list[str]) -> FlextResult[None]:
        """Install a plugin."""
        min_args_required = 2
        if len(args) < min_args_required:
            self._cli.error("Plugin type and name required")
            return FlextResult[None].fail("Missing arguments")

        plugin_type = args[0]
        plugin_name = args[1]

        self._cli.info(f"Installing {plugin_type}: {plugin_name}")

        # Install plugin via API
        result = self._api.install_plugin(
            plugin_type=plugin_type, plugin_name=plugin_name
        )

        if result.is_failure:
            self._cli.error(f"Plugin installation failed: {result.error}")
            return FlextResult[None].fail(result.error)

        self._cli.success(f"Plugin '{plugin_name}' installed successfully")
        return FlextResult[None].ok(None)

    # =============================================================================
    # STATUS COMMANDS
    # =============================================================================

    def _handle_status_command(self, _args: list[str]) -> FlextResult[None]:
        """Handle status command."""
        self._cli.info("Checking Meltano service status...")

        # Get status via API
        result = self._api.get_service_status()

        if result.is_failure:
            self._cli.error(f"Failed to get status: {result.error}")
            return FlextResult[None].fail(result.error)

        status_data = result.unwrap()

        # Display status information
        self._display_status(status_data)

        return FlextResult[None].ok(None)

    def _handle_version_command(self, _args: list[str]) -> FlextResult[None]:
        """Handle version command."""
        # Get version info via API
        result = self._api.get_version_info()

        if result.is_failure:
            self._cli.error(f"Failed to get version: {result.error}")
            return FlextResult[None].fail(result.error)

        version_data = result.unwrap()

        # Display version information
        self._display_version(version_data)

        return FlextResult[None].ok(None)

    # =============================================================================
    # DISPLAY METHODS (using flext-cli exclusively)
    # =============================================================================

    def _display_execution_metrics(self, data: dict[str, object]) -> None:
        """Display pipeline execution metrics."""
        self._cli.header("Execution Metrics")
        for key, value in data.items():
            self._cli.info(f"  {key}: {value}")

    def _display_pipelines_table(self, pipelines: list[dict[str, object]]) -> None:
        """Display pipelines in table format."""
        self._cli.table(
            data=pipelines,
            headers=["Name", "Tap", "Target", "Transform", "Status"],
            title="Configured Pipelines",
        )

    def _display_tap_metrics(self, data: dict[str, object]) -> None:
        """Display tap execution metrics."""
        self._cli.header("Tap Metrics")
        for key, value in data.items():
            self._cli.info(f"  {key}: {value}")

    def _display_target_metrics(self, data: dict[str, object]) -> None:
        """Display target execution metrics."""
        self._cli.header("Target Metrics")
        for key, value in data.items():
            self._cli.info(f"  {key}: {value}")

    def _display_dbt_metrics(self, data: dict[str, object]) -> None:
        """Display DBT execution metrics."""
        self._cli.header("DBT Metrics")
        for key, value in data.items():
            self._cli.info(f"  {key}: {value}")

    def _display_dbt_test_results(self, data: dict[str, object]) -> None:
        """Display DBT test results."""
        self._cli.header("DBT Test Results")
        for key, value in data.items():
            self._cli.info(f"  {key}: {value}")

    def _display_plugins_table(
        self, plugins: list[dict[str, object]], title: str
    ) -> None:
        """Display plugins in table format."""
        self._cli.table(
            data=plugins, headers=["Name", "Type", "Version", "Status"], title=title
        )

    def _display_status(self, status_data: dict[str, object]) -> None:
        """Display service status."""
        self._cli.header("Service Status")
        for key, value in status_data.items():
            self._cli.info(f"  {key}: {value}")

    def _display_version(self, version_data: dict[str, object]) -> None:
        """Display version information."""
        self._cli.header("Version Information")
        for key, value in version_data.items():
            self._cli.info(f"  {key}: {value}")

    # =============================================================================
    # HELP METHODS
    # =============================================================================

    def _show_banner(self) -> None:
        """Show CLI banner."""
        self._cli.header("FLEXT Meltano - Data Integration Platform")
        self._cli.info("Professional CLI for Meltano, Singer, and DBT operations")
        self._cli.info("")

    def _show_main_help(self) -> None:
        """Show main help message."""
        self._cli.info("Usage: flext-meltano <command> [options]")
        self._cli.info("")
        self._cli.info("Commands:")
        self._cli.info("  pipeline    Pipeline management (create, execute, list)")
        self._cli.info("  tap         Singer tap operations (run, list, install)")
        self._cli.info("  target      Singer target operations (run, list, install)")
        self._cli.info("  dbt         DBT operations (run, test, docs)")
        self._cli.info("  plugin      Plugin management (list, install)")
        self._cli.info("  status      Service status")
        self._cli.info("  version     Version information")
        self._cli.info("")
        self._cli.info("Use 'flext-meltano <command> --help' for command-specific help")

    def _show_pipeline_help(self) -> None:
        """Show pipeline help."""
        self._cli.info("Usage: flext-meltano pipeline <subcommand> [options]")
        self._cli.info("")
        self._cli.info("Subcommands:")
        self._cli.info("  create      Create a new pipeline")
        self._cli.info("  execute     Execute a pipeline")
        self._cli.info("  list        List available pipelines")

    def _show_tap_help(self) -> None:
        """Show tap help."""
        self._cli.info("Usage: flext-meltano tap <subcommand> [options]")
        self._cli.info("")
        self._cli.info("Subcommands:")
        self._cli.info("  run         Run a Singer tap")
        self._cli.info("  list        List available taps")
        self._cli.info("  install     Install a Singer tap")

    def _show_target_help(self) -> None:
        """Show target help."""
        self._cli.info("Usage: flext-meltano target <subcommand> [options]")
        self._cli.info("")
        self._cli.info("Subcommands:")
        self._cli.info("  run         Run a Singer target")
        self._cli.info("  list        List available targets")
        self._cli.info("  install     Install a Singer target")

    def _show_dbt_help(self) -> None:
        """Show DBT help."""
        self._cli.info("Usage: flext-meltano dbt <subcommand> [options]")
        self._cli.info("")
        self._cli.info("Subcommands:")
        self._cli.info("  run         Run DBT models")
        self._cli.info("  test        Test DBT models")
        self._cli.info("  docs        Generate DBT documentation")

    def _show_plugin_help(self) -> None:
        """Show plugin help."""
        self._cli.info("Usage: flext-meltano plugin <subcommand> [options]")
        self._cli.info("")
        self._cli.info("Subcommands:")
        self._cli.info("  list        List installed plugins")
        self._cli.info("  install     Install a plugin")

    # =============================================================================
    # ARGUMENT PARSING HELPERS
    # =============================================================================

    def _parse_pipeline_create_args(
        self, args: list[str]
    ) -> tuple[str, str, str, str | None] | None:
        """Parse pipeline create arguments."""
        min_args_required = 3
        transform_arg_index = 3
        if len(args) < min_args_required:
            self._cli.error("Usage: pipeline create <name> <tap> <target> [transform]")
            return None

        name = args[0]
        tap = args[1]
        target = args[2]
        transform = (
            args[transform_arg_index] if len(args) > transform_arg_index else None
        )

        return name, tap, target, transform

    def _parse_config_arg(self, args: list[str]) -> str | None:
        """Parse config file argument."""
        for i, arg in enumerate(args):
            if arg in {"--config", "-c"} and i + 1 < len(args):
                return args[i + 1]
        return None

    def _parse_models_arg(self, args: list[str]) -> list[str]:
        """Parse models argument."""
        for i, arg in enumerate(args):
            if arg in {"--models", "-m"} and i + 1 < len(args):
                return args[i + 1].split(",")
        return []


def main() -> int:
    """Main entry point for flext-meltano CLI."""
    cli = FlextMeltanoCLI()
    return cli.main()


if __name__ == "__main__":
    sys.exit(main())
