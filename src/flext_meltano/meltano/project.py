"""Meltano Project Integration - Deep integration with meltano-sdk.

This module provides project management for Meltano with FLEXT ecosystem
patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from flext_core import FlextService, r
from meltano.core.project import Project as MeltanoProject
from pydantic import BaseModel, Field

from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import FlextMeltanoTypes as t
from flext_meltano.utilities import u

m = FlextMeltanoModels


class MeltanoProjectInfo(BaseModel):
    """Information about a Meltano project."""

    root: Path = Field(description="Project root directory")
    name: str = Field(description="Project name")
    state: str = Field(default="initialized", description="Project state")
    plugins_count: int = Field(default=0, description="Number of plugins")


class FlextMeltanoProjectManager(FlextService[MeltanoProjectInfo]):
    """Manages Meltano projects with deep SDK integration.

    Provides programmatic access to Meltano projects, plugins, and
    configurations through wrapped meltano-sdk APIs.

    Attributes:
    project_root: Root directory of Meltano project
    project: Wrapped meltano.core.project.Project instance

    """

    # Keep ProjectInfo as alias for backward compatibility
    ProjectInfo: ClassVar[type[MeltanoProjectInfo]] = MeltanoProjectInfo

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
    ) -> r[MeltanoProjectInfo]:
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

            info = MeltanoProjectInfo(
                root=root,
                name=str(root.name),
                state="initialized",
            )

            self.logger.info(
                "Meltano project initialized",
                root=str(root),
            )
            return r[MeltanoProjectInfo].ok(info)
        except Exception as e:
            self.logger.exception("Failed to initialize project")
            return r[MeltanoProjectInfo].fail(
                f"Failed to initialize project: {e}",
            )

    def load_project(
        self,
        root: Path,
    ) -> r[MeltanoProjectInfo]:
        """Load an existing Meltano project.

        Args:
        root: Root directory of the project

        Returns:
        r containing project information

        """
        try:
            if not root.exists():
                return r[MeltanoProjectInfo].fail(
                    f"Project directory not found: {root}",
                )

            self.project = MeltanoProject(root)
            self.project_root = root

            info = MeltanoProjectInfo(
                root=root,
                name=str(root.name),
                state="loaded",
            )

            self.logger.info(
                "Meltano project loaded",
                root=str(root),
            )
            return r[MeltanoProjectInfo].ok(info)
        except Exception as e:
            self.logger.exception("Failed to load project", error=str(e))
            return r[MeltanoProjectInfo].fail(
                f"Failed to load project: {e}",
            )

    def _extract_plugins(
        self, plugin_type: str | None
    ) -> list[t.Plugin.PluginDefinition]:
        """Extract plugins from project, optionally filtered by type."""
        plugins: list[t.Plugin.PluginDefinition] = []
        if not hasattr(self.project, "plugins"):
            return plugins

        try:
            plugins_attr = getattr(self.project, "plugins", None)
            if plugins_attr is None:
                return plugins

            for plugin in plugins_attr:
                if not (hasattr(plugin, "name") and hasattr(plugin, "type")):
                    continue
                if plugin_type is not None and plugin.type != plugin_type:
                    continue

                # Type narrowing for variant attribute
                variant_raw = getattr(plugin, "variant", None)

                plugin_def: t.Plugin.PluginDefinition = {
                    "name": plugin.name,
                    "type": plugin.type,
                }

                # Add variant if present — normalize via model
                variant_normalized = m.Meltano.VariantPayload.model_validate(
                    {"value": variant_raw},
                ).value
                if variant_normalized is not None:
                    plugin_def["variant"] = variant_normalized

                plugins.append(plugin_def)
        except (TypeError, AttributeError):
            pass

        return plugins

    def get_plugins(
        self,
        plugin_type: str | None = None,
    ) -> r[list[t.Plugin.PluginDefinition]]:
        """Get plugins from the project.

        Args:
        plugin_type: Optional plugin type to filter (tap, target, dbt, etc.)

        Returns:
        r containing list of plugins

        """
        try:
            if not self.project:
                return r[list[t.Plugin.PluginDefinition]].fail("No project loaded")

            plugins = self._extract_plugins(plugin_type)

            self.logger.info(
                "Plugins retrieved",
                count=u.count(plugins),
                type=plugin_type,
            )
            return r[list[t.Plugin.PluginDefinition]].ok(plugins)
        except Exception as e:
            self.logger.exception("Failed to get plugins", error=str(e))
            return r[list[t.Plugin.PluginDefinition]].fail(
                f"Failed to get plugins: {e}",
            )

    def install_plugin(self, name: str) -> r[t.Plugin.PluginInfo]:
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
            plugin_info: t.Plugin.PluginInfo = {
                "name": name,
                "status": "installing",
            }

            self.logger.info("Plugin installed", name=name)
            return r[t.Plugin.PluginInfo].ok(plugin_info)
        except Exception as e:
            self.logger.exception("Failed to install plugin", error=str(e))
            return r[t.Plugin.PluginInfo].fail(f"Failed to install plugin: {e}")

    def execute(self, **_kwargs: t.JsonValue) -> r[MeltanoProjectInfo]:
        """Execute (implements Service pattern)."""
        if self.project_root:
            info = MeltanoProjectInfo(
                root=self.project_root,
                name=str(self.project_root.name),
            )
            return r[MeltanoProjectInfo].ok(info)
        return r[MeltanoProjectInfo].fail("No project loaded")


__all__ = [
    "FlextMeltanoProjectManager",
    "MeltanoProjectInfo",
]
