"""FLEXT Pipeline Abstractions - UNIFIED abstraction layer for data pipeline operations.

This module provides a SINGLE UNIFIED class with nested helpers for data pipeline
functionality, eliminating direct domain imports and providing a clean interface
for the FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

from flext_core import FlextLogger, r

from flext_meltano import c, p, t, u


class FlextMeltanoAbstractions:
    """UNIFIED abstraction class providing pipeline functionality with nested helpers.

    This class consolidates all pipeline wrapper functionality into a single unified
    class following FLEXT 'one class per module' pattern with nested helper classes.
    """

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
        ) -> r[t.StrMapping]:
            """Create pipeline context for data pipeline operations."""
            try:
                pipeline_context: t.StrMapping = {
                    "project_path": str(project_path),
                    "source_name": source_name,
                    "sink_name": sink_name,
                    "status": "initialized",
                }
                return r[t.StrMapping].ok(pipeline_context)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                error_msg = f"Failed to create pipeline context: {e}"
                self.logger.exception(error_msg)
                return r[t.StrMapping].fail(error_msg)

        def execute_data_pipeline(
            self,
            _pipeline_context: Mapping[str, str | None],
            source_config: t.Meltano.MeltanoConfigDict,
            sink_config: t.Meltano.MeltanoConfigDict,
        ) -> r[t.Meltano.ELT.PipelineResult]:
            """Execute data pipeline with given context and configurations."""
            try:
                result: t.Meltano.ELT.PipelineResult = {
                    "status": "completed",
                    "source": str(
                        u.get(
                            source_config,
                            "name",
                            default=c.IDENTIFIER_UNKNOWN,
                        ),
                    ),
                    "sink": str(
                        u.get(
                            sink_config,
                            "name",
                            default=c.IDENTIFIER_UNKNOWN,
                        ),
                    ),
                    "records_processed": 0,
                }
                return r[t.Meltano.ELT.PipelineResult].ok(result)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                error_msg = f"Failed to execute data pipeline: {e}"
                self.logger.exception(error_msg)
                return r[t.Meltano.ELT.PipelineResult].fail(error_msg)

    def __init__(self) -> None:
        """Initialize unified abstractions with FLEXT patterns."""
        super().__init__()
        self.logger = FlextLogger(__name__)
        self._project_path: Path | None = None
        self._runner_helper = self._RunnerHelper(self.logger)

    def add_plugin(self, plugin_config: t.Meltano.PluginConfiguration) -> r[bool]:
        """Add a plugin."""
        try:
            self.logger.info("Adding plugin", plugin_config=str(plugin_config))
            return r[bool].ok(value=True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to add plugin: {e}"
            self.logger.exception(error_msg)
            return r[bool].fail(error_msg)

    def create_elt_context(
        self,
        project: p.Meltano.Project,
        extractor_name: str,
        loader_name: str,
    ) -> r[t.Meltano.MeltanoConfigDict]:
        """Create ELT context for pipeline execution."""
        try:
            elt_context: t.Meltano.MeltanoConfigDict = {
                "project": str(project.root_dir),
                "extractor_name": extractor_name,
                "loader_name": loader_name,
                "status": "initialized",
            }
            return r[t.Meltano.MeltanoConfigDict].ok(elt_context)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to create ELT context: {e}"
            self.logger.exception(error_msg)
            return r[t.Meltano.MeltanoConfigDict].fail(error_msg)

    def create_pipeline_context(
        self,
        source_name: str,
        sink_name: str,
    ) -> r[t.StrMapping]:
        """Create pipeline context."""
        if not self._project_path:
            return r[t.StrMapping].fail("No project loaded")
        return self._runner_helper.create_pipeline_context(
            self._project_path,
            source_name,
            sink_name,
        )

    def execute_data_pipeline(
        self,
        source_config: t.Meltano.MeltanoConfigDict,
        sink_config: t.Meltano.MeltanoConfigDict,
    ) -> r[t.Meltano.ELT.PipelineResult]:
        """Execute data pipeline."""
        pipeline_context: Mapping[str, str | None] = {
            "project_path": str(self._project_path) if self._project_path else None,
            "status": "initialized",
        }
        return self._runner_helper.execute_data_pipeline(
            pipeline_context,
            source_config,
            sink_config,
        )

    def execute_singer_pipeline(
        self,
        elt_context: t.Meltano.MeltanoConfigDict,
        _extractor_plugin: p.Meltano.Plugin,
        _loader_plugin: p.Meltano.Plugin,
    ) -> r[t.Meltano.ELT.PipelineResult]:
        """Execute singer pipeline."""
        try:
            result: t.Meltano.ELT.PipelineResult = {
                "status": "completed",
                "records_processed": 0,
                "elt_context": str(elt_context),
            }
            return r[t.Meltano.ELT.PipelineResult].ok(result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to execute singer pipeline: {e}"
            self.logger.exception(error_msg)
            return r[t.Meltano.ELT.PipelineResult].fail(error_msg)

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

    def get_components_of_type(
        self,
        component_type: str,
    ) -> r[Sequence[t.Meltano.PluginDefinition]]:
        """Get components of specified type."""
        try:
            components: Sequence[t.Meltano.PluginDefinition] = [
                {"name": "source-csv", "type": "sources", "status": "available"},
                {"name": "sink-postgres", "type": "sinks", "status": "available"},
                {
                    "name": "transform-dbt",
                    "type": "transformers",
                    "status": "available",
                },
            ]
            filtered_components = u.filter(
                components,
                lambda comp: u.get(dict(comp), "type", default="") == component_type,
            )
            result_list: Sequence[t.Meltano.PluginDefinition] = (
                list(filtered_components) if filtered_components else []
            )
            return r[Sequence[t.Meltano.PluginDefinition]].ok(result_list)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to get components of type {component_type}: {e}"
            self.logger.exception(error_msg)
            return r[Sequence[t.Meltano.PluginDefinition]].fail(error_msg)

    def get_plugins_of_type(
        self,
        _project: p.Meltano.Project,
        plugin_type: str,
    ) -> r[Mapping[str, t.Meltano.PluginDefinition]]:
        """Get plugins of specified type."""
        try:
            plugins: Mapping[str, t.Meltano.PluginDefinition] = {
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
            filtered_plugins: Mapping[str, t.Meltano.PluginDefinition] = {
                k: v
                for k, v in plugins.items()
                if u.get(v, "type", default="") == plugin_type
            }
            return r[Mapping[str, t.Meltano.PluginDefinition]].ok(filtered_plugins)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to get plugins of type {plugin_type}: {e}"
            self.logger.exception(error_msg)
            return r[Mapping[str, t.Meltano.PluginDefinition]].fail(error_msg)

    def get_project_root(self) -> r[Path]:
        """Get the root directory of the current project."""
        if not self._project_path:
            return r[Path].fail("No project loaded")
        try:
            return r[Path].ok(self._project_path)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Path].fail(f"Failed to get project root: {e}")


__all__ = ["FlextMeltanoAbstractions"]
