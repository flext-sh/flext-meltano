"""Meltano Project Integration - Deep integration with meltano-sdk.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from pathlib import Path
from typing import override

from flext_core import FlextService, r
from meltano.core.project import Project

from flext_meltano import m, t, u


class FlextMeltanoProjectManager(FlextService[t.Meltano.Project.ProjectMetadata]):
    """Manages Meltano projects with deep SDK integration."""

    def __init__(self, root: Path | None = None) -> None:
        """Initialize Meltano project manager."""
        super().__init__()
        self.project_root: Path | None = root
        self.project: Project | None = None

    @override
    def execute(self, **_kwargs: t.Container) -> r[t.Meltano.Project.ProjectMetadata]:
        """Execute (implements Service pattern)."""
        if self.project_root:
            info: t.Meltano.Project.ProjectMetadata = {
                "root": str(self.project_root),
                "name": str(self.project_root.name),
            }
            return r[t.Meltano.Project.ProjectMetadata].ok(info)
        return r[t.Meltano.Project.ProjectMetadata].fail("No project loaded")

    def get_plugins(
        self,
        plugin_type: str | None = None,
    ) -> r[Sequence[t.Meltano.PluginDefinition]]:
        """Get plugins from the project, optionally filtered by type."""
        try:
            if not self.project:
                return r[Sequence[t.Meltano.PluginDefinition]].fail("No project loaded")
            plugins = self._extract_plugins(plugin_type)
            self.logger.info(
                "Plugins retrieved", count=u.count(plugins), type=plugin_type or ""
            )
            return r[Sequence[t.Meltano.PluginDefinition]].ok(plugins)
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
            return r[Sequence[t.Meltano.PluginDefinition]].fail(
                f"Failed to get plugins: {e}"
            )

    def initialize_project(self, root: Path) -> r[t.Meltano.Project.ProjectMetadata]:
        """Initialize a new Meltano project."""
        try:
            root.mkdir(parents=True, exist_ok=True)
            self.project = Project(root)
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
        """Install a plugin in the project."""
        msg = f"Plugin installation requires meltano-core SDK integration: install_plugin({name!r})"
        raise NotImplementedError(msg)

    def load_project(self, root: Path) -> r[t.Meltano.Project.ProjectMetadata]:
        """Load an existing Meltano project."""
        try:
            if not root.exists():
                return r[t.Meltano.Project.ProjectMetadata].fail(
                    f"Project directory not found: {root}",
                )
            self.project = Project(root)
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
        self,
        plugin_type: str | None,
    ) -> Sequence[t.Meltano.PluginDefinition]:
        """Extract plugins from project, optionally filtered by type."""
        plugins: MutableSequence[t.Meltano.PluginDefinition] = []
        plugins_attr = getattr(self.project, "plugins", None)
        if plugins_attr is None:
            return plugins
        try:
            for plugin in plugins_attr:
                if not (
                    getattr(plugin, "name", None) is not None
                    and getattr(plugin, "type", None) is not None
                ):
                    continue
                if plugin_type is not None and plugin.type != plugin_type:
                    continue
                plugin_def: MutableMapping[
                    str,
                    str | Sequence[str] | Mapping[str, t.Scalar | None],
                ] = {"name": plugin.name, "type": plugin.type}
                variant_raw = getattr(plugin, "variant", None)
                variant_normalized = m.Meltano.VariantPayload.model_validate(
                    {"value": variant_raw},
                ).value
                if variant_normalized is not None:
                    plugin_def["variant"] = variant_normalized
                plugins.append(plugin_def)
        except (TypeError, AttributeError) as e:
            self.logger.warning(f"Failed to extract plugins: {e}")
        return plugins


__all__ = ["FlextMeltanoProjectManager"]
