"""FLEXT Pipeline Abstractions - UNIFIED abstraction layer for data pipeline operations.

This module provides a SINGLE UNIFIED class with nested helpers for data pipeline functionality,
eliminating direct domain imports and providing a clean interface for the FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextLogger, FlextResult
from flext_meltano.typings import FlextMeltanoTypes


class FlextMeltanoAbstractions:
    """UNIFIED abstraction class providing pipeline functionality with nested helpers.

    This class consolidates all pipeline wrapper functionality into a single unified class
    following FLEXT 'one class per module' pattern with nested helper classes.
    """

    # NESTED RUNNER HELPER CLASS
    # ========================================================================

    class _RunnerHelper:
        """Helper class for data pipeline runner operations."""

        def __init__(self, logger: FlextLogger) -> None:
            """Initialize runner helper."""
            super().__init__()
            self.logger = logger

        def create_pipeline_context(
            self, project_path: Path, source_name: str, sink_name: str
        ) -> FlextResult[FlextMeltanoTypes.MeltanoCore.NestedJsonDict]:
            """Create pipeline context for data pipeline operations."""
            try:
                pipeline_context: FlextMeltanoTypes.MeltanoCore.NestedJsonDict = {
                    "project_path": str(project_path),
                    "source_name": source_name,
                    "sink_name": sink_name,
                    "status": "initialized",
                }
                return FlextResult[FlextMeltanoTypes.MeltanoCore.NestedJsonDict].ok(pipeline_context)
            except Exception as e:
                error_msg = f"Failed to create pipeline context: {e}"
                self.logger.exception(error_msg)
                return FlextResult[FlextMeltanoTypes.MeltanoCore.NestedJsonDict].fail(error_msg)

        def execute_data_pipeline(
            self,
            _pipeline_context: dict[str, object],
            source_config: dict[str, object],
            sink_config: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Execute data pipeline with given context and configurations."""
            try:
                # This is a simplified implementation
                # In production, would orchestrate the actual data pipeline
                result: dict[str, object] = {
                    "status": "completed",
                    "source": source_config.get("name", "unknown"),
                    "sink": sink_config.get("name", "unknown"),
                    "records_processed": 0,
                }
                return FlextResult[dict[str, object]].ok(data=result)
            except Exception as e:
                error_msg = f"Failed to execute data pipeline: {e}"
                self.logger.exception(error_msg)
                return FlextResult[dict[str, object]].fail(error_msg)

    # MAIN UNIFIED CLASS INTERFACE
    # ========================================================================

    def __init__(self) -> None:
        """Initialize unified abstractions with FLEXT patterns."""
        super().__init__()
        self.logger = FlextLogger(__name__)
        self._project_path: Path | None = None
        self._runner_helper = self._RunnerHelper(self.logger)

    # Project operations
    def find_project(self, project_root: Path) -> FlextResult[Path]:
        """Find and validate pipeline project directory."""
        try:
            if not project_root.exists() or not project_root.is_dir():
                return FlextResult[Path].fail(
                    f"Project path is not a valid directory: {project_root}"
                )

            self._project_path = project_root

            self.logger.info(
                "Pipeline project loaded successfully",
                project_root=str(project_root),
            )

            return FlextResult[Path].ok(project_root)

        except Exception as e:
            error_msg = f"Failed to load pipeline project: {e}"
            self.logger.exception(error_msg)
            return FlextResult[Path].fail(error_msg)

    def get_project_root(self) -> FlextResult[Path]:
        """Get the root directory of the current project."""
        if not self._project_path:
            return FlextResult[Path].fail("No project loaded")

        try:
            return FlextResult[Path].ok(self._project_path)
        except Exception as e:
            return FlextResult[Path].fail(f"Failed to get project root: {e}")

    # Component operations
    def get_components_of_type(
        self, component_type: str
    ) -> FlextResult[list[dict[str, object]]]:
        """Get components of specified type."""
        try:
            # Generic component listing - would be implemented based on actual needs
            components: list[dict[str, object]] = [
                {"name": "source-csv", "type": "sources", "status": "available"},
                {"name": "sink-postgres", "type": "sinks", "status": "available"},
                {
                    "name": "transform-dbt",
                    "type": "transformers",
                    "status": "available",
                },
            ]

            filtered_components = [c for c in components if c["type"] == component_type]
            return FlextResult[list[dict[str, object]]].ok(filtered_components)

        except Exception as e:
            error_msg = f"Failed to get components of type {component_type}: {e}"
            self.logger.exception(error_msg)
            return FlextResult[list[dict[str, object]]].fail(error_msg)

    # Runner operations
    def create_pipeline_context(
        self, source_name: str, sink_name: str
    ) -> FlextResult[FlextMeltanoTypes.MeltanoCore.NestedJsonDict]:
        """Create pipeline context."""
        if not self._project_path:
            return FlextResult[FlextMeltanoTypes.MeltanoCore.NestedJsonDict].fail("No project loaded")

        return self._runner_helper.create_pipeline_context(
            self._project_path, source_name, sink_name
        )

    def execute_data_pipeline(
        self,
        source_config: dict[str, object],
        sink_config: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Execute data pipeline."""
        pipeline_context = {
            "project_path": self._project_path,
            "status": "initialized",
        }

        return self._runner_helper.execute_data_pipeline(
            pipeline_context, source_config, sink_config
        )

    # ELT operations
    def create_elt_context(
        self,
        project: object,
        extractor_name: str,
        loader_name: str,
    ) -> FlextResult[dict[str, object]]:
        """Create ELT context for pipeline execution."""
        try:
            elt_context = {
                "project": project,
                "extractor_name": extractor_name,
                "loader_name": loader_name,
                "status": "initialized",
            }
            return FlextResult[dict[str, object]].ok(elt_context)
        except Exception as e:
            error_msg = f"Failed to create ELT context: {e}"
            self.logger.exception(error_msg)
            return FlextResult[dict[str, object]].fail(error_msg)

    def execute_singer_pipeline(
        self,
        elt_context: dict[str, object],
        _extractor_plugin: object,
        _loader_plugin: object,
    ) -> FlextResult[dict[str, object]]:
        """Execute singer pipeline."""
        try:
            # Simplified implementation - in production would orchestrate actual singer pipeline
            result = {
                "status": "completed",
                "records_processed": 0,
                "elt_context": elt_context,
            }
            return FlextResult[dict[str, object]].ok(result)
        except Exception as e:
            error_msg = f"Failed to execute singer pipeline: {e}"
            self.logger.exception(error_msg)
            return FlextResult[dict[str, object]].fail(error_msg)

    # Plugin operations
    def get_plugins_of_type(
        self, _project: object, plugin_type: str
    ) -> FlextResult[dict[str, dict[str, object]]]:
        """Get plugins of specified type."""
        try:
            # Simplified implementation - would need actual plugin discovery
            plugins: dict[str, dict[str, object]] = {
                "tap-csv": {
                    "name": "tap-csv",
                    "type": "extractors",
                    "status": "available",
                },
                "target-postgres": {
                    "name": "target-postgres",
                    "type": "loaders",
                    "status": "available",
                },
            }

            filtered_plugins = {
                k: v for k, v in plugins.items() if v["type"] == plugin_type
            }
            return FlextResult[dict[str, dict[str, object]]].ok(filtered_plugins)

        except Exception as e:
            error_msg = f"Failed to get plugins of type {plugin_type}: {e}"
            self.logger.exception(error_msg)
            return FlextResult[dict[str, dict[str, object]]].fail(error_msg)

    def add_plugin(self, plugin_config: dict[str, object]) -> FlextResult[bool]:
        """Add a plugin."""
        try:
            # Simplified implementation - would validate and add plugin
            self.logger.info("Adding plugin", plugin_config=plugin_config)
            return FlextResult[bool].ok(True)
        except Exception as e:
            error_msg = f"Failed to add plugin: {e}"
            self.logger.exception(error_msg)
            return FlextResult[bool].fail(error_msg)


__all__ = [
    "FlextMeltanoAbstractions",
]
