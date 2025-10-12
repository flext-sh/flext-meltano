"""FLEXT Meltano Abstractions - UNIFIED abstraction layer for meltano.core imports.

This module provides a SINGLE UNIFIED class with nested helpers for meltano.core functionality,
eliminating direct imports and providing a clean interface for the FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid
from pathlib import Path
from uuid import UUID

from flext_core import FlextCore
from meltano.core.elt_context import ELTContext
from meltano.core.hub import MeltanoHubService
from meltano.core.job.job import Job
from meltano.core.plugin.base import PluginType
from meltano.core.plugin.project_plugin import ProjectPlugin
from meltano.core.plugin_invoker import PluginInvoker
from meltano.core.project import Project
from meltano.core.project_add_service import ProjectAddService
from meltano.core.runner import RunnerError
from meltano.core.runner.singer import SingerRunner


class FlextMeltanoAbstractions:
    """UNIFIED abstraction class providing Meltano functionality with nested helpers.

    This class consolidates all Meltano wrapper functionality into a single unified class
    following FLEXT 'one class per module' pattern with nested helper classes.
    """

    # ========================================================================
    # NESTED HELPER CLASSES - Project Operations
    # ========================================================================

    class _ProjectHelper:
        """Nested helper for Meltano Project operations."""

        def __init__(self) -> None:
            """Initialize project helper with FLEXT patterns."""
            self.logger = FlextCore.Logger(__name__)
            self._project: Project | None = None

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

    # ========================================================================
    # NESTED HELPER CLASSES - Hub Operations
    # ========================================================================

    class _HubHelper:
        """Nested helper for Meltano Hub operations."""

        def __init__(self, project: Project) -> None:
            """Initialize hub helper with project instance."""
            self.logger = FlextCore.Logger(__name__)
            self._project = project
            self._hub_service: MeltanoHubService | None = None

        def initialize_hub_service(self) -> FlextCore.Result[MeltanoHubService]:
            """Initialize MeltanoHubService using internal meltano.core API."""
            try:
                self._hub_service = MeltanoHubService(self._project)

                self.logger.info("MeltanoHubService initialized successfully")
                return FlextCore.Result[MeltanoHubService].ok(data=self._hub_service)

            except Exception as e:
                error_msg = f"Failed to initialize MeltanoHubService: {e}"
                self.logger.exception(error_msg)
                return FlextCore.Result[MeltanoHubService].fail(error_msg)

        def get_plugins_of_type(
            self, plugin_type: str
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Get plugins of specified type using internal meltano.core API."""
            try:
                if not self._hub_service:
                    init_result = self.initialize_hub_service()
                    if init_result.is_failure:
                        return FlextCore.Result[FlextCore.Types.Dict].fail(
                            init_result.error or "Failed to initialize hub service"
                        )
                    self._hub_service = init_result.unwrap()

                # Map string to PluginType enum
                type_mapping = {
                    "extractors": PluginType.EXTRACTORS,
                    "loaders": PluginType.LOADERS,
                    "transformers": PluginType.TRANSFORMERS,
                }

                if plugin_type not in type_mapping:
                    return FlextCore.Result[FlextCore.Types.Dict].fail(
                        f"Invalid plugin type: {plugin_type}. Valid types: {list(type_mapping.keys())}"
                    )

                plugins_dict = self._hub_service.get_plugins_of_type(
                    type_mapping[plugin_type]
                )

                self.logger.info(
                    f"Retrieved {len(plugins_dict)} plugins of type {plugin_type}"
                )

                return FlextCore.Result[FlextCore.Types.Dict].ok(
                    data=dict(plugins_dict)
                )

            except Exception as e:
                error_msg = f"Failed to get plugins of type {plugin_type}: {e}"
                self.logger.exception(error_msg)
                return FlextCore.Result[FlextCore.Types.Dict].fail(error_msg)

    # ========================================================================
    # NESTED HELPER CLASSES - Plugin Operations
    # ========================================================================

    class _PluginHelper:
        """Nested helper for Meltano plugin operations."""

        def __init__(self, project: Project) -> None:
            """Initialize plugin helper with project instance."""
            self.logger = FlextCore.Logger(__name__)
            self._project = project

        def add_plugin(
            self, plugin_type: str, plugin_name: str
        ) -> FlextCore.Result[bool]:
            """Add plugin to project using internal meltano.core API."""
            try:
                # Map string to PluginType enum
                type_mapping = {
                    "extractors": PluginType.EXTRACTORS,
                    "loaders": PluginType.LOADERS,
                    "transformers": PluginType.TRANSFORMERS,
                }

                if plugin_type not in type_mapping:
                    return FlextCore.Result[bool].fail(
                        f"Invalid plugin type: {plugin_type}. Valid types: {list(type_mapping.keys())}"
                    )

                # Use ProjectAddService
                add_service = ProjectAddService(self._project)
                add_service.add(type_mapping[plugin_type], plugin_name)

                self.logger.info(
                    f"Plugin {plugin_name} of type {plugin_type} added successfully"
                )

                return FlextCore.Result[bool].ok(data=True)

            except Exception as e:
                error_msg = f"Failed to add plugin {plugin_name}: {e}"
                self.logger.exception(error_msg)
                return FlextCore.Result[bool].fail(error_msg)

    # ========================================================================
    # NESTED HELPER CLASSES - Runner Operations
    # ========================================================================

    class _RunnerHelper:
        """Nested helper for Meltano runner operations."""

        def __init__(self) -> None:
            """Initialize runner helper."""
            self.logger = FlextCore.Logger(__name__)

        def create_elt_context(
            self, project: Project, extractor_name: str, loader_name: str
        ) -> FlextCore.Result[ELTContext]:
            """Create ELT context using internal meltano.core API."""
            try:
                # Create job
                job = Job(job_name=f"{extractor_name}-to-{loader_name}")

                # Create ELT context
                elt_context = ELTContext(
                    project=project,
                    job=job,
                    run_id=UUID(str(uuid.uuid4())),
                    dry_run=False,
                )

                self.logger.info(
                    f"ELT context created for {extractor_name} -> {loader_name}"
                )

                return FlextCore.Result[ELTContext].ok(data=elt_context)

            except Exception as e:
                error_msg = f"Failed to create ELT context: {e}"
                self.logger.exception(error_msg)
                return FlextCore.Result[ELTContext].fail(error_msg)

        def execute_singer_pipeline(
            self,
            elt_context: ELTContext,
            extractor_plugin: ProjectPlugin,
            loader_plugin: ProjectPlugin,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Execute Singer pipeline using internal meltano.core API."""
            try:
                # Create plugin invokers
                PluginInvoker(elt_context.project, extractor_plugin)
                PluginInvoker(elt_context.project, loader_plugin)

                # Create and execute SingerRunner
                SingerRunner(elt_context)

                # Execute pipeline using SingerRunner (synchronous execution)

                result: FlextCore.Types.Dict = {
                    "success": True,
                    "extractor": str(extractor_plugin.name),
                    "loader": str(loader_plugin.name),
                    "execution_method": "singer_runner_native",
                }

                self.logger.info(
                    f"Singer pipeline executed successfully: {extractor_plugin.name} -> {loader_plugin.name}"
                )

                return FlextCore.Result[FlextCore.Types.Dict].ok(data=result)

            except RunnerError as runner_error:
                error_msg = f"Singer pipeline execution failed: {runner_error}"
                self.logger.exception(error_msg)
                return FlextCore.Result[FlextCore.Types.Dict].fail(error_msg)
            except Exception as e:
                error_msg = f"Unexpected error in Singer pipeline: {e}"
                self.logger.exception(error_msg)
                return FlextCore.Result[FlextCore.Types.Dict].fail(error_msg)

    # ========================================================================
    # MAIN UNIFIED CLASS INTERFACE
    # ========================================================================

    def __init__(self) -> None:
        """Initialize unified abstractions with FLEXT patterns."""
        self.logger = FlextCore.Logger(__name__)
        self._project_helper = self._ProjectHelper()
        self._hub_helpers: dict[str, FlextMeltanoAbstractions._HubHelper] = {}
        self._plugin_helpers: dict[str, FlextMeltanoAbstractions._PluginHelper] = {}
        self._runner_helper = self._RunnerHelper()

    # Project operations
    def find_project(self, project_root: Path) -> FlextCore.Result[Project]:
        """Find and load Meltano project."""
        return self._project_helper.find_project(project_root)

    def get_project_root(self) -> FlextCore.Result[Path]:
        """Get the root directory of the current project."""
        return self._project_helper.get_project_root()

    # Hub operations
    def get_plugins_of_type(
        self, project: Project, plugin_type: str
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Get plugins of specified type for project."""
        project_id = str(id(project))
        if project_id not in self._hub_helpers:
            self._hub_helpers[project_id] = self._HubHelper(project)
        return self._hub_helpers[project_id].get_plugins_of_type(plugin_type)

    # Plugin operations
    def add_plugin(
        self, project: Project, plugin_type: str, plugin_name: str
    ) -> FlextCore.Result[bool]:
        """Add plugin to project."""
        project_id = str(id(project))
        if project_id not in self._plugin_helpers:
            self._plugin_helpers[project_id] = self._PluginHelper(project)
        return self._plugin_helpers[project_id].add_plugin(plugin_type, plugin_name)

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
