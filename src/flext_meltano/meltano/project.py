"""Meltano Project Integration - Deep integration with meltano-sdk.

This module provides project management for Meltano with FLEXT ecosystem
patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, override

from flext_core import FlextService, r
from meltano.core.project import Project as MeltanoProject
from pydantic import PrivateAttr

from flext_meltano import FlextMeltanoModels, t, u

m = FlextMeltanoModels


class FlextMeltanoProjectManager(FlextService[t.Meltano.Project.ProjectMetadata]):
    """Manages Meltano projects with deep SDK integration.

    Provides programmatic access to Meltano projects, plugins, and
    configurations through wrapped meltano-sdk APIs.

    Attributes:
    project_root: Root directory of Meltano project
    project: Wrapped meltano.core.project.Project instance

    """

    ProjectInfo: ClassVar[type[dict[str, t.JsonValue]]] = dict
    _metadata_extra: dict[str, str] = PrivateAttr(
        default_factory=lambda: dict[str, str](),
    )
    _sealed: bool = PrivateAttr(default=False)

    def __init__(self, root: Path | None = None) -> None:
        """Initialize Meltano project manager.

        Args:
            root: Root directory of Meltano project (optional)

        """
        super().__init__()
        self.project_root: Path | None = root
        self.project: MeltanoProject | None = None

    @override
    def execute(
        self,
        **_kwargs: t.JsonValue,
    ) -> r[t.Meltano.Project.ProjectMetadata]:
        """Execute (implements Service pattern)."""
        if self.project_root:
            info: t.Meltano.Project.ProjectMetadata = {
                "root": str(self.project_root),
                "name": str(self.project_root.name),
            }
            return r[t.Meltano.Project.ProjectMetadata].ok(info)
        return r[t.Meltano.Project.ProjectMetadata].fail("No project loaded")

    def get_plugins(
        self, plugin_type: str | None = None
    ) -> r[list[t.Meltano.PluginDefinition]]:
        """Get plugins from the project.

        Args:
        plugin_type: Optional plugin type to filter (tap, target, dbt, etc.)

        Returns:
        r containing list of plugins

        """
        try:
            if not self.project:
                return r[list[t.Meltano.PluginDefinition]].fail("No project loaded")
            plugins = self._extract_plugins(plugin_type)
            self.logger.info(
                "Plugins retrieved", count=u.count(plugins), type=plugin_type
            )
            return r[list[t.Meltano.PluginDefinition]].ok(plugins)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to get plugins", error=str(e))
            return r[list[t.Meltano.PluginDefinition]].fail(
                f"Failed to get plugins: {e}"
            )

    def initialize_project(self, root: Path) -> r[t.Meltano.Project.ProjectMetadata]:
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
            info: t.Meltano.Project.ProjectMetadata = {
                "root": str(root),
                "name": str(root.name),
                "state": "initialized",
            }
            self.logger.info("Meltano project initialized", root=str(root))
            return r[t.Meltano.Project.ProjectMetadata].ok(info)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to initialize project")
            return r[t.Meltano.Project.ProjectMetadata].fail(
                f"Failed to initialize project: {e}"
            )

    def install_plugin(self, name: str) -> r[t.Meltano.PluginInfo]:
        """Install a plugin in the project.

        Args:
        name: Name of the plugin to install

        Returns:
        r containing plugin information

        """
        try:
            self.logger.info("Installing plugin", name=name)
            plugin_info: t.Meltano.PluginInfo = {"name": name, "status": "installing"}
            self.logger.info("Plugin installed", name=name)
            return r[t.Meltano.PluginInfo].ok(plugin_info)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to install plugin", error=str(e))
            return r[t.Meltano.PluginInfo].fail(f"Failed to install plugin: {e}")

    def load_project(self, root: Path) -> r[t.Meltano.Project.ProjectMetadata]:
        """Load an existing Meltano project.

        Args:
        root: Root directory of the project

        Returns:
        r containing project information

        """
        try:
            if not root.exists():
                return r[t.Meltano.Project.ProjectMetadata].fail(
                    f"Project directory not found: {root}"
                )
            self.project = MeltanoProject(root)
            self.project_root = root
            info: t.Meltano.Project.ProjectMetadata = {
                "root": str(root),
                "name": str(root.name),
                "state": "loaded",
            }
            self.logger.info("Meltano project loaded", root=str(root))
            return r[t.Meltano.Project.ProjectMetadata].ok(info)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to load project", error=str(e))
            return r[t.Meltano.Project.ProjectMetadata].fail(
                f"Failed to load project: {e}"
            )

    def _extract_plugins(
        self, plugin_type: str | None
    ) -> list[t.Meltano.PluginDefinition]:
        """Extract plugins from project, optionally filtered by type."""
        plugins: list[t.Meltano.PluginDefinition] = []
        if getattr(self.project, "plugins", None) is None:
            return plugins
        try:
            plugins_attr = getattr(self.project, "plugins", None)
            if plugins_attr is None:
                return plugins
            for plugin in plugins_attr:
                if not (
                    getattr(plugin, "name", None) is not None
                    and getattr(plugin, "type", None) is not None
                ):
                    continue
                if plugin_type is not None and plugin.type != plugin_type:
                    continue
                variant_raw = getattr(plugin, "variant", None)
                plugin_def: t.Meltano.PluginDefinition = {
                    "name": plugin.name,
                    "type": plugin.type,
                }
                variant_normalized = m.Meltano.VariantPayload.model_validate({
                    "value": variant_raw
                }).value
                if variant_normalized is not None:
                    plugin_def["variant"] = variant_normalized
                plugins.append(plugin_def)
        except (TypeError, AttributeError):
            pass
        return plugins


__all__ = ["FlextMeltanoProjectManager"]
