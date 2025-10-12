"""FLEXT Meltano Abstractions - UNIFIED abstraction layer for meltano.core imports.

This module provides a SINGLE UNIFIED class with nested helpers for meltano.core functionality,
eliminating direct imports and providing a clean interface for the FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextCore
from meltano.core.elt_context import ELTContext
from meltano.core.hub import MeltanoHubService
from meltano.core.plugin.base import PluginType
from meltano.core.plugin.project_plugin import ProjectPlugin
from meltano.core.project import Project
from meltano.core.project_add_service import ProjectAddService


class FlextMeltanoAbstractions:
    """UNIFIED abstraction class providing Meltano functionality with nested helpers.

    This class consolidates all Meltano wrapper functionality into a single unified class
    following FLEXT 'one class per module' pattern with nested helper classes.
    """

    # MAIN UNIFIED CLASS INTERFACE
    # ========================================================================

    def __init__(self) -> None:
        """Initialize unified abstractions with FLEXT patterns."""
        self.logger = FlextCore.Logger(__name__)
        self._project: Project | None = None
        self._hub_services: dict[str, MeltanoHubService] = {}

    # Project operations
    def find_project(self, project_root: Path) -> FlextCore.Result[Project]:
        """Find and load Meltano project using internal meltano.core API."""
        try:
            project = Project.find(project_root)
            self._project = project

            self.logger.info(
                "Meltano project loaded successfully",
                project_root=str(project_root),
            )

            return FlextCore.Result[Project].ok(data=project)

        except Exception as e:
            error_msg = f"Failed to load Meltano project: {e}"
            self.logger.exception(error_msg)
            return FlextCore.Result[Project].fail(error_msg)

    def get_project_root(self) -> FlextCore.Result[Path]:
        """Get the root directory of the current project."""
        if not self._project:
            return FlextCore.Result[Path].fail("No project loaded")

        try:
            root_path = Path(self._project.root)
            return FlextCore.Result[Path].ok(data=root_path)
        except Exception as e:
            return FlextCore.Result[Path].fail(f"Failed to get project root: {e}")

    # Hub operations
    def get_plugins_of_type(
        self, project: Project, plugin_type: str
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Get plugins of specified type using MeltanoHubService."""
        try:
            project_id = str(id(project))
            if project_id not in self._hub_services:
                self._hub_services[project_id] = MeltanoHubService(project)

            hub_service = self._hub_services[project_id]

            # Get plugins based on type
            if plugin_type == "extractors":
                plugins = hub_service.get_extractors()
            elif plugin_type == "loaders":
                plugins = hub_service.get_loaders()
            elif plugin_type == "transformers":
                plugins = hub_service.get_transformers()
            elif plugin_type == "orchestrators":
                plugins = hub_service.get_orchestrators()
            else:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"Unknown plugin type: {plugin_type}"
                )

            self.logger.info(
                f"Retrieved {len(plugins)} {plugin_type} plugins",
                plugin_type=plugin_type,
                count=len(plugins),
            )

            return FlextCore.Result[FlextCore.Types.Dict].ok(data=plugins)

        except Exception as e:
            error_msg = f"Failed to get plugins of type {plugin_type}: {e}"
            self.logger.exception(error_msg)
            return FlextCore.Result[FlextCore.Types.Dict].fail(error_msg)

    # Plugin operations
    def add_plugin(
        self, project: Project, plugin_type: str, plugin_name: str
    ) -> FlextCore.Result[bool]:
        """Add plugin to project using ProjectAddService."""
        try:
            # Map string plugin types to PluginType enum
            plugin_type_enum = PluginType(plugin_type)

            # Create add service and add plugin
            add_service = ProjectAddService(project)
            add_service.add(
                plugin_type=plugin_type_enum,
                plugin_name=plugin_name,
            )

            self.logger.info(
                "Plugin added successfully",
                plugin_type=plugin_type,
                plugin_name=plugin_name,
            )

            return FlextCore.Result[bool].ok(data=True)

        except Exception as e:
            error_msg = f"Failed to add plugin {plugin_name}: {e}"
            self.logger.exception(error_msg)
            return FlextCore.Result[bool].fail(error_msg)

    # Runner operations
    def create_elt_context(
        self, project: Project, extractor_name: str, loader_name: str
    ) -> FlextCore.Result[ELTContext]:
        """Create ELT context."""
        return self._runner_helper.create_elt_context(
            project, extractor_name, loader_name
        )

    def execute_singer_pipeline(
        self,
        elt_context: ELTContext,
        extractor_plugin: ProjectPlugin,
        loader_plugin: ProjectPlugin,
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Execute Singer pipeline."""
        return self._runner_helper.execute_singer_pipeline(
            elt_context, extractor_plugin, loader_plugin
        )


__all__ = [
    "FlextMeltanoAbstractions",
]
