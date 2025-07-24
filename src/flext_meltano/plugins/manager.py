"""FLEXT Meltano Plugin Manager.

Plugin management with Clean Architecture patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextResult

from flext_meltano.plugins.models import FlextMeltanoPlugin

if TYPE_CHECKING:
    from pathlib import Path


class FlextMeltanoPluginManager:
    """Plugin manager for Meltano plugins with enterprise patterns."""

    def __init__(self, project_root: Path | None = None) -> None:
        """Initialize plugin manager.

        Args:
            project_root: Meltano project root directory

        """
        from pathlib import Path

        self.project_root = project_root or Path.cwd()

    def install_plugin(
        self,
        plugin_type: str,
        plugin_name: str,
        variant: str | None = None,
    ) -> FlextResult[FlextMeltanoPlugin]:
        """Install a Meltano plugin.

        Args:
            plugin_type: Type of plugin (extractor, loader, etc.)
            plugin_name: Name of the plugin to install
            variant: Optional plugin variant

        Returns:
            FlextResult with installed plugin model

        """
        try:
            from flext_meltano.helpers.installation import (
                flext_meltano_install_plugin,
            )

            result = flext_meltano_install_plugin(
                plugin_type=plugin_type,
                plugin_name=plugin_name,
                variant=variant,
                project_root=self.project_root,
            )

            if not result.is_success:
                return FlextResult.fail(f"Failed to install plugin: {result.error}")

            plugin = FlextMeltanoPlugin(
                name=plugin_name,
                plugin_type=plugin_type,
                variant=variant,
                installed=True,
            )

            return FlextResult.ok(plugin)

        except Exception as e:
            return FlextResult.fail(f"Plugin installation failed: {e}")

    def list_plugins(
        self,
        plugin_type: str | None = None,
    ) -> FlextResult[list[FlextMeltanoPlugin]]:
        """List installed Meltano plugins.

        Args:
            plugin_type: Optional filter by plugin type

        Returns:
            FlextResult with list of plugins

        """
        try:
            from flext_meltano.helpers.cli import flext_run_meltano_command

            args = ["config", "meltano", "list-plugins"]
            if plugin_type:
                args.append(plugin_type)

            result = flext_run_meltano_command(
                args=args,
                project_root=self.project_root,
            )

            if not result.is_success:
                return FlextResult.fail(f"Failed to list plugins: {result.error}")

            # For now, return empty list as implementation would require parsing meltano output
            plugins: list[FlextMeltanoPlugin] = []
            return FlextResult.ok(plugins)

        except Exception as e:
            return FlextResult.fail(f"Plugin listing failed: {e}")

    def get_plugin_config(
        self,
        plugin_name: str,
    ) -> FlextResult[dict[str, Any]]:
        """Get configuration for a specific plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            FlextResult with plugin configuration

        """
        try:
            from flext_meltano.helpers.cli import flext_run_meltano_command

            result = flext_run_meltano_command(
                args=["config", plugin_name, "list"],
                project_root=self.project_root,
            )

            if not result.is_success:
                return FlextResult.fail(f"Failed to get plugin config: {result.error}")

            # Return basic config structure
            config = {
                "plugin_name": plugin_name,
                "settings": {},
                "commands": {},
            }

            return FlextResult.ok(config)

        except Exception as e:
            return FlextResult.fail(f"Plugin config retrieval failed: {e}")
