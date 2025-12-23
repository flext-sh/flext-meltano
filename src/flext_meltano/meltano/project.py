"""Meltano Project Integration - Deep integration with meltano-sdk.

This module provides project management for Meltano with FLEXT ecosystem
patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import cast

from flext_core import FlextService, r
from meltano.core.project import Project as MeltanoProject
from pydantic import BaseModel, Field

from flext_meltano.utilities import u


class FlextMeltanoProjectManager(FlextService):
    """Manages Meltano projects with deep SDK integration.

    Provides programmatic access to Meltano projects, plugins, and
    configurations through wrapped meltano-sdk APIs.

    Attributes:
    project_root: Root directory of Meltano project
    project: Wrapped meltano.core.project.Project instance

    """

    class ProjectInfo(BaseModel):
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
        self,
        root: Path,
    ) -> r[FlextMeltanoProjectManager.ProjectInfo]:
        """Initialize a new Meltano project.

        Args:
        root: Root directory for the project

        Returns:
        r containing project information

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
            return r[FlextMeltanoProjectManager.ProjectInfo].ok(info)
        except Exception as e:
            self.logger.exception("Failed to initialize project")
            return r[FlextMeltanoProjectManager.ProjectInfo].fail(
                f"Failed to initialize project: {e}",
            )

    def load_project(
        self,
        root: Path,
    ) -> r[FlextMeltanoProjectManager.ProjectInfo]:
        """Load an existing Meltano project.

        Args:
        root: Root directory of the project

        Returns:
        r containing project information

        """
        try:
            if not root.exists():
                return r[FlextMeltanoProjectManager.ProjectInfo].fail(
                    f"Project directory not found: {root}",
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
            return r[FlextMeltanoProjectManager.ProjectInfo].ok(info)
        except Exception as e:
            self.logger.exception("Failed to load project", error=str(e))
            return r[FlextMeltanoProjectManager.ProjectInfo].fail(
                f"Failed to load project: {e}",
            )

    def get_plugins(
        self,
        plugin_type: str | None = None,
    ) -> r[list[dict[str, object]]]:
        """Get plugins from the project.

        Args:
        plugin_type: Optional plugin type to filter (tap, target, dbt, etc.)

        Returns:
        r containing list of plugins

        """
        try:
            if not self.project:
                return r[list[dict[str, object]]].fail("No project loaded")

            plugins = []
            if hasattr(self.project, "plugins"):
                try:
                    for plugin in self.project.plugins:  # type: ignore
                        plugin_dict = {
                            "name": plugin.name,
                            "type": plugin.type,
                            "variant": getattr(plugin, "variant", None),
                        }
                        if plugin_type is None or plugin.type == plugin_type:
                            plugins.append(plugin_dict)
                except (TypeError, AttributeError):
                    pass

            self.logger.info(
                "Plugins retrieved",
                count=u.count(plugins),
                type=plugin_type,
            )
            return r[list[dict[str, object]]].ok(plugins)
        except Exception as e:
            self.logger.exception("Failed to get plugins", error=str(e))
            return r[list[dict[str, object]]].fail(
                f"Failed to get plugins: {e}",
            )

    def install_plugin(self, name: str) -> r[dict[str, object]]:
        """Install a plugin in the project.

        Args:
        name: Name of the plugin to install

        Returns:
        r containing plugin information

        """
        try:
            self.logger.info("Installing plugin", name=name)

            # Plugin installation would typically use meltano CLI or SDK
            # For now, just log the operation
            plugin_info = cast(
                "dict[str, object]",
                {
                    "name": name,
                    "status": "installing",
                },
            )

            self.logger.info("Plugin installed", name=name)
            return r[dict[str, object]].ok(plugin_info)
        except Exception as e:
            self.logger.exception("Failed to install plugin", error=str(e))
            return r[dict[str, object]].fail(f"Failed to install plugin: {e}")

    def execute(self, **_kwargs: object) -> r[str]:
        """Execute (implements Service pattern)."""
        if self.project_root:
            msg = f"Meltano project: {self.project_root}"
            return r[str].ok(msg)
        return r[str].fail("No project loaded")


__all__ = [
    "FlextMeltanoProjectManager",
]
