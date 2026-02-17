"""FLEXT Pipeline Abstractions - UNIFIED abstraction layer for data pipeline operations.

This module provides a SINGLE UNIFIED class with nested helpers for data pipeline
functionality, eliminating direct domain imports and providing a clean interface
for the FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextLogger, r, u

from flext_meltano.models import FlextMeltanoModels
from flext_meltano.protocols import p
from flext_meltano.typings import FlextMeltanoTypes as t

# Import aliases for concise usage following order: c -> t -> p -> r -> m -> u
m = FlextMeltanoModels


class FlextMeltanoAbstractions:
    """UNIFIED abstraction class providing pipeline functionality with nested helpers.

    This class consolidates all pipeline wrapper functionality into a single unified
    class following FLEXT 'one class per module' pattern with nested helper classes.
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
            self,
            project_path: Path,
            source_name: str,
            sink_name: str,
        ) -> r[t.MeltanoCore.NestedJsonDict]:
            """Create pipeline context for data pipeline operations."""
            try:
                pipeline_context: t.MeltanoCore.NestedJsonDict = {
                    "project_path": str(project_path),
                    "source_name": source_name,
                    "sink_name": sink_name,
                    "status": "initialized",
                }
                return r[t.MeltanoCore.NestedJsonDict].ok(pipeline_context)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                error_msg = f"Failed to create pipeline context: {e}"
                self.logger.exception(error_msg)
                return r[t.MeltanoCore.NestedJsonDict].fail(error_msg)

        def execute_data_pipeline(
            self,
            _pipeline_context: t.MeltanoCore.NestedJsonDict,
            source_config: t.MeltanoCore.MeltanoConfigDict,
            sink_config: t.MeltanoCore.MeltanoConfigDict,
        ) -> r[t.ELT.PipelineResult]:
            """Execute data pipeline with given context and configurations."""
            try:
                # This is a simplified implementation
                # In production, would orchestrate the actual data pipeline
                result: t.ELT.PipelineResult = {
                    "status": "completed",
                    "source": u.get(source_config, "name", default="unknown"),
                    "sink": u.get(sink_config, "name", default="unknown"),
                    "records_processed": 0,
                }
                return r[t.ELT.PipelineResult].ok(result)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                error_msg = f"Failed to execute data pipeline: {e}"
                self.logger.exception(error_msg)
                return r[t.ELT.PipelineResult].fail(error_msg)

    # MAIN UNIFIED CLASS INTERFACE
    # ========================================================================

    def __init__(self) -> None:
        """Initialize unified abstractions with FLEXT patterns."""
        super().__init__()
        self.logger = FlextLogger(__name__)
        self._project_path: Path | None = None
        self._runner_helper = self._RunnerHelper(self.logger)

    # Project operations
    def find_project(self, project_root: Path) -> r[Path]:
        """Find and validate pipeline project directory."""
        try:
            if not project_root.exists() or not project_root.is_dir():
                return r[Path].fail(
                    f"Project path is not a valid directory: {project_root}",
                )

            self._project_path = project_root

            self.logger.info(
                "Pipeline project loaded successfully",
                project_root=str(project_root),
            )

            return r[Path].ok(project_root)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to load pipeline project: {e}"
            self.logger.exception(error_msg)
            return r[Path].fail(error_msg)

    def get_project_root(self) -> r[Path]:
        """Get the root directory of the current project."""
        if not self._project_path:
            return r[Path].fail("No project loaded")

        try:
            return r[Path].ok(self._project_path)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Path].fail(f"Failed to get project root: {e}")

    # Component operations
    def get_components_of_type(
        self,
        component_type: str,
    ) -> r[list[t.Plugin.PluginDefinition]]:
        """Get components of specified type."""
        try:
            # Generic component listing - would be implemented based on actual needs
            components: list[t.Plugin.PluginDefinition] = [
                {"name": "source-csv", "type": "sources", "status": "available"},
                {"name": "sink-postgres", "type": "sinks", "status": "available"},
                {
                    "name": "transform-dbt",
                    "type": "transformers",
                    "status": "available",
                },
            ]

            # DSL: Use filter for unified filtering
            filtered_components = u.filter(
                components,
                lambda comp: u.get(comp, "type", default="") == component_type,
            )
            # Type narrowing: ensure list[t.Plugin.PluginDefinition]
            if isinstance(filtered_components, (list, tuple)):
                result_list: list[t.Plugin.PluginDefinition] = list(filtered_components)
                return r[list[t.Plugin.PluginDefinition]].ok(result_list)
            return r[list[t.Plugin.PluginDefinition]].ok([])

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to get components of type {component_type}: {e}"
            self.logger.exception(error_msg)
            return r[list[t.Plugin.PluginDefinition]].fail(error_msg)

    # Runner operations
    def create_pipeline_context(
        self,
        source_name: str,
        sink_name: str,
    ) -> r[t.MeltanoCore.NestedJsonDict]:
        """Create pipeline context."""
        if not self._project_path:
            return r[t.MeltanoCore.NestedJsonDict].fail("No project loaded")

        return self._runner_helper.create_pipeline_context(
            self._project_path,
            source_name,
            sink_name,
        )

    def execute_data_pipeline(
        self,
        source_config: t.MeltanoCore.MeltanoConfigDict,
        sink_config: t.MeltanoCore.MeltanoConfigDict,
    ) -> r[t.ELT.PipelineResult]:
        """Execute data pipeline."""
        pipeline_context: t.MeltanoCore.NestedJsonDict = {
            "project_path": str(self._project_path) if self._project_path else None,
            "status": "initialized",
        }

        return self._runner_helper.execute_data_pipeline(
            pipeline_context,
            source_config,
            sink_config,
        )

    # ELT operations
    def create_elt_context(
        self,
        project: p.Meltano.MeltanoProjectProtocol,
        extractor_name: str,
        loader_name: str,
    ) -> r[t.MeltanoCore.MeltanoConfigDict]:
        """Create ELT context for pipeline execution."""
        try:
            elt_context: t.MeltanoCore.MeltanoConfigDict = {
                "project": str(project.root_dir),
                "extractor_name": extractor_name,
                "loader_name": loader_name,
                "status": "initialized",
            }
            return r[t.MeltanoCore.MeltanoConfigDict].ok(elt_context)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to create ELT context: {e}"
            self.logger.exception(error_msg)
            return r[t.MeltanoCore.MeltanoConfigDict].fail(error_msg)

    def execute_singer_pipeline(
        self,
        elt_context: t.MeltanoCore.MeltanoConfigDict,
        _extractor_plugin: p.Meltano.PluginProtocol[t.JsonValue],
        _loader_plugin: p.Meltano.PluginProtocol[t.JsonValue],
    ) -> r[t.ELT.PipelineResult]:
        """Execute singer pipeline."""
        try:
            # Simplified implementation - in production would orchestrate actual
            # singer pipeline
            result: t.ELT.PipelineResult = {
                "status": "completed",
                "records_processed": 0,
                "elt_context": elt_context,
            }
            return r[t.ELT.PipelineResult].ok(result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to execute singer pipeline: {e}"
            self.logger.exception(error_msg)
            return r[t.ELT.PipelineResult].fail(error_msg)

    # Plugin operations
    def get_plugins_of_type(
        self,
        _project: p.Meltano.MeltanoProjectProtocol,
        plugin_type: str,
    ) -> r[dict[str, t.Plugin.PluginDefinition]]:
        """Get plugins of specified type."""
        try:
            # Simplified implementation - would need actual plugin discovery
            plugins: dict[str, t.Plugin.PluginDefinition] = {
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

            # DSL: Use dict comprehension for filtering (u.filter expects single-arg predicate)
            filtered_plugins: dict[str, t.Plugin.PluginDefinition] = {
                k: v
                for k, v in plugins.items()
                if u.get(v, "type", default="") == plugin_type
            }
            return r[dict[str, t.Plugin.PluginDefinition]].ok(filtered_plugins)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to get plugins of type {plugin_type}: {e}"
            self.logger.exception(error_msg)
            return r[dict[str, t.Plugin.PluginDefinition]].fail(error_msg)

    def add_plugin(self, plugin_config: t.Plugin.PluginConfiguration) -> r[bool]:
        """Add a plugin."""
        try:
            # Simplified implementation - would validate and add plugin
            self.logger.info(
                "Adding plugin",
                plugin_config=plugin_config,
            )
            return r[bool].ok(value=True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to add plugin: {e}"
            self.logger.exception(error_msg)
            return r[bool].fail(error_msg)


__all__ = [
    "FlextMeltanoAbstractions",
]
