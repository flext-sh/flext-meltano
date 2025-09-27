"""FLEXT Meltano Abstractions - Abstraction layer for meltano.core imports.

This module provides FLEXT-compliant abstractions for meltano.core functionality,
eliminating direct imports and providing a clean interface for the FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, override
from uuid import UUID

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

from flext_core import (
    FlextLogger,
    FlextResult,
    FlextUtilities,
)


class FlextMeltanoProjectWrapper:
    """FLEXT-compliant wrapper for Meltano Project operations."""

    @override
    @override
    @override
    @override
    @override
    def __init__(self) -> None:
        """Initialize the wrapper with FLEXT patterns."""
        self._logger = FlextLogger(__name__)
        self._project: Project | None = None

    def find_project(self, project_root: Path) -> FlextResult[Project]:
        """Find and load Meltano project using internal meltano.core API.

        Args:
            project_root: Path to the Meltano project directory

        Returns:
            FlextResult containing the loaded Project instance

        """
        try:
            project = Project.find(project_root)
            self._project = project

            self._logger.info(
                "Meltano project loaded successfully",
                project_root=str(project_root),
            )

            return FlextResult[Project].ok(data=project)

        except Exception as e:
            error_msg = f"Failed to load Meltano project: {e}"
            self._logger.exception(error_msg)
            return FlextResult[Project].fail(error_msg)

    def get_project_root(self) -> FlextResult[Path]:
        """Get the root directory of the current project.

        Returns:
            FlextResult containing the project root path

        """
        if not self._project:
            return FlextResult[Path].fail("No project loaded")

        try:
            root_path = Path(self._project.root)
            return FlextResult[Path].ok(data=root_path)
        except Exception as e:
            return FlextResult[Path].fail(f"Failed to get project root: {e}")


class FlextMeltanoHubWrapper:
    """FLEXT-compliant wrapper for Meltano Hub operations."""

    @override
    @override
    @override
    @override
    @override
    def __init__(self, project: Project) -> None:
        """Initialize hub wrapper with project instance.

        Args:
            project: Meltano project instance

        """
        self._logger = FlextLogger(__name__)
        self._project = project
        self._hub_service: MeltanoHubService | None = None

    def initialize_hub_service(self) -> FlextResult[MeltanoHubService]:
        """Initialize MeltanoHubService using internal meltano.core API.

        Returns:
            FlextResult containing the hub service instance

        """
        try:
            self._hub_service = MeltanoHubService(self._project)

            self._logger.info("MeltanoHubService initialized successfully")
            return FlextResult[MeltanoHubService].ok(data=self._hub_service)

        except Exception as e:
            error_msg = f"Failed to initialize MeltanoHubService: {e}"
            self._logger.exception(error_msg)
            return FlextResult[MeltanoHubService].fail(error_msg)

    def get_plugins_of_type(self, plugin_type: str) -> FlextResult[dict[str, Any]]:
        """Get plugins of specified type using internal meltano.core API.

        Args:
            plugin_type: Type of plugins to retrieve

        Returns:
            FlextResult containing dictionary of plugins

        """
        try:
            if not self._hub_service:
                init_result = self.initialize_hub_service()
                if init_result.is_failure:
                    return FlextResult[dict[str, Any]].fail(
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
                return FlextResult[dict[str, Any]].fail(
                    f"Invalid plugin type: {plugin_type}. Valid types: {list(type_mapping.keys())}"
                )

            plugins_dict = self._hub_service.get_plugins_of_type(
                type_mapping[plugin_type]
            )

            self._logger.info(
                f"Retrieved {len(plugins_dict)} plugins of type {plugin_type}"
            )

            return FlextResult[dict[str, Any]].ok(data=plugins_dict)

        except Exception as e:
            error_msg = f"Failed to get plugins of type {plugin_type}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[dict[str, Any]].fail(error_msg)


class FlextMeltanoPluginWrapper:
    """FLEXT-compliant wrapper for Meltano plugin operations."""

    @override
    @override
    @override
    @override
    @override
    def __init__(self, project: Project) -> None:
        """Initialize plugin wrapper with project instance.

        Args:
            project: Meltano project instance

        """
        self._logger = FlextLogger(__name__)
        self._project = project

    def add_plugin(self, plugin_type: str, plugin_name: str) -> FlextResult[bool]:
        """Add plugin to project using internal meltano.core API.

        Args:
            plugin_type: Type of plugin to add
            plugin_name: Name of the plugin

        Returns:
            FlextResult indicating success

        """
        try:
            # Map string to PluginType enum
            type_mapping = {
                "extractors": PluginType.EXTRACTORS,
                "loaders": PluginType.LOADERS,
                "transformers": PluginType.TRANSFORMERS,
            }

            if plugin_type not in type_mapping:
                return FlextResult[bool].fail(
                    f"Invalid plugin type: {plugin_type}. Valid types: {list(type_mapping.keys())}"
                )

            # Use ProjectAddService
            add_service = ProjectAddService(self._project)
            add_service.add(type_mapping[plugin_type], plugin_name)

            self._logger.info(
                f"Plugin {plugin_name} of type {plugin_type} added successfully"
            )

            return FlextResult[bool].ok(data=True)

        except Exception as e:
            error_msg = f"Failed to add plugin {plugin_name}: {e}"
            self._logger.exception(error_msg)
            return FlextResult[bool].fail(error_msg)


class FlextMeltanoRunnerWrapper:
    """FLEXT-compliant wrapper for Meltano runner operations."""

    @override
    @override
    @override
    @override
    @override
    def __init__(self) -> None:
        """Initialize runner wrapper."""
        self._logger = FlextLogger(__name__)

    def create_elt_context(
        self, project: Project, extractor_name: str, loader_name: str
    ) -> FlextResult[ELTContext]:
        """Create ELT context using internal meltano.core API.

        Args:
            project: Meltano project instance
            extractor_name: Name of extractor plugin
            loader_name: Name of loader plugin

        Returns:
            FlextResult containing ELT context

        """
        try:
            # Create job
            job = Job(job_name=f"{extractor_name}-to-{loader_name}")

            # Create ELT context
            elt_context = ELTContext(
                project=project,
                job=job,
                run_id=UUID(FlextUtilities.Generators.generate_uuid()),
                dry_run=False,
            )

            self._logger.info(
                f"ELT context created for {extractor_name} -> {loader_name}"
            )

            return FlextResult[ELTContext].ok(data=elt_context)

        except Exception as e:
            error_msg = f"Failed to create ELT context: {e}"
            self._logger.exception(error_msg)
            return FlextResult[ELTContext].fail(error_msg)

    def execute_singer_pipeline(
        self,
        elt_context: ELTContext,
        extractor_plugin: ProjectPlugin,
        loader_plugin: ProjectPlugin,
    ) -> FlextResult[dict[str, object]]:
        """Execute Singer pipeline using internal meltano.core API.

        Args:
            elt_context: ELT context instance
            extractor_plugin: Extractor plugin instance
            loader_plugin: Loader plugin instance

        Returns:
            FlextResult containing execution results

        """
        try:
            # Create plugin invokers
            extractor_invoker = PluginInvoker(elt_context.project, extractor_plugin)
            loader_invoker = PluginInvoker(elt_context.project, loader_plugin)

            # Create and execute SingerRunner
            runner = SingerRunner(elt_context)

            # Execute pipeline
            asyncio.run(runner.run(extractor_invoker, loader_invoker))

            result: dict[str, object] = {
                "success": True,
                "extractor": str(extractor_plugin.name),
                "loader": str(loader_plugin.name),
                "execution_method": "singer_runner_native",
            }

            self._logger.info(
                f"Singer pipeline executed successfully: {extractor_plugin.name} -> {loader_plugin.name}"
            )

            return FlextResult[dict[str, object]].ok(data=result)

        except RunnerError as runner_error:
            error_msg = f"Singer pipeline execution failed: {runner_error}"
            self._logger.exception(error_msg)
            return FlextResult[dict[str, object]].fail(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error in Singer pipeline: {e}"
            self._logger.exception(error_msg)
            return FlextResult[dict[str, object]].fail(error_msg)


class FlextMeltanoAbstractions:
    """Main abstraction class providing unified access to Meltano functionality."""

    @override
    @override
    @override
    @override
    @override
    def __init__(self) -> None:
        """Initialize abstractions with FLEXT patterns."""
        self._logger = FlextLogger(__name__)
        self._project_wrapper = FlextMeltanoProjectWrapper()
        self._hub_wrapper: FlextMeltanoHubWrapper | None = None
        self._plugin_wrapper: FlextMeltanoPluginWrapper | None = None
        self._runner_wrapper = FlextMeltanoRunnerWrapper()

    def get_project_wrapper(self) -> FlextMeltanoProjectWrapper:
        """Get project wrapper instance.

        Returns:
            FlextMeltanoProjectWrapper instance

        """
        return self._project_wrapper

    def get_hub_wrapper(self, project: Project) -> FlextMeltanoHubWrapper:
        """Get hub wrapper instance for project.

        Args:
            project: Meltano project instance

        Returns:
            FlextMeltanoHubWrapper instance

        """
        if not self._hub_wrapper:
            self._hub_wrapper = FlextMeltanoHubWrapper(project)
        return self._hub_wrapper

    def get_plugin_wrapper(self, project: Project) -> FlextMeltanoPluginWrapper:
        """Get plugin wrapper instance for project.

        Args:
            project: Meltano project instance

        Returns:
            FlextMeltanoPluginWrapper instance

        """
        if not self._plugin_wrapper:
            self._plugin_wrapper = FlextMeltanoPluginWrapper(project)
        return self._plugin_wrapper

    def get_runner_wrapper(self) -> FlextMeltanoRunnerWrapper:
        """Get runner wrapper instance.

        Returns:
            FlextMeltanoRunnerWrapper instance

        """
        return self._runner_wrapper


__all__ = [
    "FlextMeltanoAbstractions",
    "FlextMeltanoHubWrapper",
    "FlextMeltanoPluginWrapper",
    "FlextMeltanoProjectWrapper",
    "FlextMeltanoRunnerWrapper",
]
