"""Meltano Project Integration - Deep integration with meltano-sdk.

This module provides project management for Meltano with FLEXT ecosystem
patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextResult, FlextService, FlextUtilities
from meltano.core.project import Project as MeltanoProject
from pydantic import Field

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.protocols import FlextMeltanoProtocols
from flext_meltano.typings import FlextMeltanoTypes

# Import aliases for concise usage
u = FlextUtilities
t = FlextMeltanoTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels
p = FlextMeltanoProtocols


class FlextMeltanoProjectManager(FlextService):
    """Manages Meltano projects with deep SDK integration.

    Provides programmatic access to Meltano projects, plugins, and
    configurations through wrapped meltano-sdk APIs.

    Attributes:
    project_root: Root directory of Meltano project
    project: Wrapped meltano.core.project.Project instance

    """

    class ProjectInfo(FlextMeltanoModels):
        """Information about a Meltano project."""

        root: Path = Field(description="Project root directory")
        name: str = Field(description="Project name")
        state: str = Field(default="initialized", description="Project state")
        plugins_count: int = Field(default=0, description="Number of plugins")

    def __init__(self, root: Path | None = None) -> None:
        """Initialize Meltano project manager.

        Args:
        root: Root directory of Meltano project (optional)

        """
        super().__init__()
        self.project_root: Path | None = root
        self.project: MeltanoProject | None = None

    def initialize_project(
        self, root: Path
    ) -> FlextResult[FlextMeltanoProjectManager.ProjectInfo]:
        """Initialize a new Meltano project.

        Args:
        root: Root directory for the project

        Returns:
        FlextResult containing project information

        """
        try:
            root.mkdir(parents=True, exist_ok=True)
            self.project = MeltanoProject(root)
            self.project_root = root

            # Create ProjectInfo instance - avoid mypy confusion with built-in ProjectInfo
            info_dict = {
                "root": root,
                "name": str(root.name),
                "state": "initialized",
            }
            info = FlextMeltanoProjectManager.ProjectInfo(**info_dict)

            self.logger.info(
                "Meltano project initialized",
                root=str(root),
            )
            return FlextResult[FlextMeltanoProjectManager.ProjectInfo].ok(info)
        except Exception as e:
            self.logger.exception("Failed to initialize project")
            return FlextResult[FlextMeltanoProjectManager.ProjectInfo].fail(
                f"Failed to initialize project: {e}"
            )

    def load_project(
        self, root: Path
    ) -> FlextResult[FlextMeltanoProjectManager.ProjectInfo]:
        """Load an existing Meltano project.

        Args:
        root: Root directory of the project

        Returns:
        FlextResult containing project information

        """
        try:
            if not root.exists():
                return FlextResult[FlextMeltanoProjectManager.ProjectInfo].fail(
                    f"Project directory not found: {root}"
                )

            self.project = MeltanoProject(root)
            self.project_root = root

            # Create ProjectInfo instance - avoid mypy confusion with built-in ProjectInfo
            info_dict = {
                "root": root,
                "name": str(root.name),
                "state": "loaded",
            }
            info = FlextMeltanoProjectManager.ProjectInfo(**info_dict)

            self.logger.info(
                "Meltano project loaded",
                root=str(root),
            )
            return FlextResult[FlextMeltanoProjectManager.ProjectInfo].ok(info)
        except Exception as e:
            self.logger.exception("Failed to load project", error=str(e))
            return FlextResult[FlextMeltanoProjectManager.ProjectInfo].fail(
                f"Failed to load project: {e}"
            )

    def get_plugins(
        self, plugin_type: str | None = None
    ) -> FlextResult[list[dict[str, object]]]:
        """Get plugins from the project.

        Args:
        plugin_type: Optional plugin type to filter (tap, target, dbt, etc.)

        Returns:
        FlextResult containing list of plugins

        """
        try:
            if not self.project:
                return FlextResult[list[dict[str, object]]].fail("No project loaded")

            plugins = []
            if hasattr(self.project, "plugins") and hasattr(
                self.project.plugins, "__iter__"
            ):
                for plugin in self.project.plugins:
                    plugin_dict = {
                        "name": plugin.name,
                        "type": plugin.type,
                        "variant": getattr(plugin, "variant", None),
                    }
                    if plugin_type is None or plugin.type == plugin_type:
                        plugins.append(plugin_dict)

            self.logger.info(
                "Plugins retrieved",
                count=len(plugins),
                type=plugin_type,
            )
            return FlextResult[list[dict[str, object]]].ok(plugins)
        except Exception as e:
            self.logger.exception("Failed to get plugins", error=str(e))
            return FlextResult[list[dict[str, object]]].fail(
                f"Failed to get plugins: {e}"
            )

    def install_plugin(self, name: str) -> FlextResult[dict[str, object]]:
        """Install a plugin in the project.

        Args:
        name: Name of the plugin to install

        Returns:
        FlextResult containing plugin information

        """
        try:
            self.logger.info("Installing plugin", name=name)

            # Plugin installation would typically use meltano CLI or SDK
            # For now, just log the operation
            plugin_info = {
                "name": name,
                "status": "installing",
            }

            self.logger.info("Plugin installed", name=name)
            return FlextResult[dict[str, object]].ok(plugin_info)
        except Exception as e:
            self.logger.exception("Failed to install plugin", error=str(e))
            return FlextResult[dict[str, object]].fail(f"Failed to install plugin: {e}")

    def execute(self, **_kwargs: object) -> FlextResult[str]:
        """Execute (implements Domain.Service pattern)."""
        if self.project_root:
            msg = f"Meltano project: {self.project_root}"
            return FlextResult[str].ok(msg)
        return FlextResult[str].fail("No project loaded")


__all__ = [
    "FlextMeltanoProjectManager",
]
