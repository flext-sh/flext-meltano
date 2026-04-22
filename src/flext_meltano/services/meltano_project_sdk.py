"""Meltano SDK Project Management — MRO mixin for FlextMeltano facade.

Deep integration with meltano-core Project SDK. Moved from meltano/project.py
and converted from standalone s to facade mixin.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    MutableSequence,
    Sequence,
)
from pathlib import Path

from meltano.core.project import Project

from flext_meltano import FlextMeltanoServiceBase, c, m, p, r, t, u


class FlextMeltanoProjectManager(FlextMeltanoServiceBase):
    """Mixin providing Meltano SDK project management for MRO composition.

    Wraps ``meltano.core.project.Project`` for direct SDK operations
    (initialize, load, get plugins).
    """

    _sdk_project_root: Path | None = u.PrivateAttr(default_factory=lambda: None)
    _sdk_project: Project | None = u.PrivateAttr(default_factory=lambda: None)

    def fetch_sdk_plugins(
        self,
        plugin_type: str | None = None,
    ) -> p.Result[Sequence[t.Meltano.PluginDefinition]]:
        """Get plugins from the SDK project, optionally filtered by type."""
        try:
            if not self._sdk_project:
                return r[Sequence[t.Meltano.PluginDefinition]].fail("No project loaded")
            plugins = self._extract_sdk_plugins(plugin_type)
            self.logger.info(
                "Plugins retrieved",
                count=u.count(plugins),
                type=plugin_type or "",
            )
            return r[Sequence[t.Meltano.PluginDefinition]].ok(plugins)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Failed to get plugins", error=str(e))
            return r[Sequence[t.Meltano.PluginDefinition]].fail(
                f"Failed to get plugins: {e}"
            )

    def initialize_sdk_project(
        self, root: Path
    ) -> p.Result[t.Meltano.OptionalScalarMap]:
        """Initialize a new Meltano project via SDK."""
        try:
            try:
                root.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                return r[t.Meltano.OptionalScalarMap].fail(
                    f"Failed to prepare project directory: {e}",
                )
            self._sdk_project = Project(root)
            self._sdk_project_root = root
            info = {
                "project_root": str(root),
                "state": c.Meltano.ProjectSdkState.INITIALIZED,
            }
            self.logger.info("Meltano project initialized", root=str(root))
            return r[t.Meltano.OptionalScalarMap].ok(info)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Failed to initialize project")
            return r[t.Meltano.OptionalScalarMap].fail(
                f"Failed to initialize project: {e}"
            )

    def load_sdk_project(self, root: Path) -> p.Result[t.Meltano.OptionalScalarMap]:
        """Load an existing Meltano project via SDK."""
        try:
            if not root.exists():
                return r[t.Meltano.OptionalScalarMap].fail(
                    f"Project directory not found: {root}",
                )
            self._sdk_project = Project(root)
            self._sdk_project_root = root
            info = {
                "project_root": str(root),
                "state": c.Meltano.ProjectSdkState.LOADED,
            }
            self.logger.info("Meltano project loaded", root=str(root))
            return r[t.Meltano.OptionalScalarMap].ok(info)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Failed to load project", error=str(e))
            return r[t.Meltano.OptionalScalarMap].fail(f"Failed to load project: {e}")

    def _extract_sdk_plugins(
        self,
        plugin_type: str | None,
    ) -> Sequence[t.Meltano.PluginDefinition]:
        """Extract plugins from SDK project, optionally filtered by type."""
        plugins: MutableSequence[t.Meltano.PluginDefinition] = []
        if self._sdk_project is None:
            return plugins
        try:
            sdk_plugins_service = self._sdk_project.plugins
        except AttributeError:
            return plugins
        try:
            for plugin in sdk_plugins_service.plugins():
                try:
                    name = plugin.name
                    plugin_kind = plugin.type
                except AttributeError:
                    continue
                if plugin_type is not None and plugin_kind != plugin_type:
                    continue
                plugin_def: dict[str, t.Cli.JsonValue] = {
                    "name": name,
                    "type": plugin_kind,
                }
                try:
                    variant_raw = plugin.variant
                except AttributeError:
                    variant_raw = None
                variant_normalized = m.Meltano.VariantPayload.model_validate(
                    {"value": variant_raw},
                ).value
                if variant_normalized is not None:
                    plugin_def["variant"] = (
                        {str(key): value for key, value in variant_normalized.items()}
                        if isinstance(variant_normalized, Mapping)
                        else list(variant_normalized)
                        if isinstance(variant_normalized, Sequence)
                        and not isinstance(variant_normalized, str)
                        else variant_normalized
                    )
                plugins.append(plugin_def)
        except (TypeError, AttributeError) as e:
            self.logger.warning("Failed to extract plugins", error=str(e))
        return plugins


__all__: list[str] = ["FlextMeltanoProjectManager"]
