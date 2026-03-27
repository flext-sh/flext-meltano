"""FLEXT Pipeline Abstractions - UNIFIED abstraction layer for data pipeline operations.

This module provides a SINGLE UNIFIED class with nested helpers for data pipeline
functionality, eliminating direct domain imports and providing a clean interface
for the FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from pathlib import Path
from typing import ClassVar, override

from flext_core import r

from flext_meltano import FlextMeltanoServiceBase, c, m, p, t, u


class FlextMeltanoAbstractions(FlextMeltanoServiceBase):
    """UNIFIED abstraction class providing pipeline functionality with nested helpers.

    This class consolidates all pipeline wrapper functionality into a single unified
    class following FLEXT 'one class per module' pattern with nested helper classes.
    """

    _stream_registry: ClassVar[MutableMapping[str, m.Meltano.StreamDefinition]] = {}
    _project_path: ClassVar[Path | None] = None
    service_name: str = "FlextMeltanoAbstractions"

    class _RunnerHelper:
        """Helper class for data pipeline runner operations."""

        def __init__(self, logger: p.Logger) -> None:
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
                    "status": c.Meltano.Enums.StreamStatus.INITIALIZED,
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
                    "status": c.Meltano.Enums.StreamStatus.COMPLETED,
                    "source": str(
                        source_config.get("name", c.IDENTIFIER_UNKNOWN),
                    ),
                    "sink": str(
                        sink_config.get("name", c.IDENTIFIER_UNKNOWN),
                    ),
                    "records_processed": 0,
                }
                return r[t.Meltano.ELT.PipelineResult].ok(result)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
                error_msg = f"Failed to execute data pipeline: {e}"
                self.logger.exception(error_msg)
                return r[t.Meltano.ELT.PipelineResult].fail(error_msg)

    @property
    def _runner_helper(self) -> _RunnerHelper:
        """Lazy-initialize runner helper."""
        return self._RunnerHelper(self.logger)

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
                "status": c.Meltano.Enums.StreamStatus.INITIALIZED,
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
            "status": c.Meltano.Enums.StreamStatus.INITIALIZED,
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
                "status": c.Meltano.Enums.StreamStatus.COMPLETED,
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
            FlextMeltanoAbstractions._project_path = project_root
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
                {
                    "name": "source-csv",
                    "type": "sources",
                    "status": c.Meltano.Enums.OperationStatus.AVAILABLE,
                },
                {
                    "name": "sink-postgres",
                    "type": "sinks",
                    "status": c.Meltano.Enums.OperationStatus.AVAILABLE,
                },
                {
                    "name": "transform-dbt",
                    "type": "transformers",
                    "status": c.Meltano.Enums.OperationStatus.AVAILABLE,
                },
            ]
            filtered_components = u.filter(
                components,
                lambda comp: dict(comp).get("type", "") == component_type,
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
                    "status": c.Meltano.Enums.OperationStatus.AVAILABLE,
                },
                "target-postgres": {
                    "name": "target-postgres",
                    "type": "loaders",
                    "status": c.Meltano.Enums.OperationStatus.AVAILABLE,
                },
            }
            filtered_plugins: Mapping[str, t.Meltano.PluginDefinition] = {
                k: v for k, v in plugins.items() if v.get("type", "") == plugin_type
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

    def process_tap_config(
        self,
        config: m.Meltano.TapConfig,
    ) -> r[m.Meltano.TapConfig]:
        """Process tap configuration."""
        return r[m.Meltano.TapConfig].ok(config)

    def build_tap_instance(
        self,
        tap_instance: m.Meltano.TapInstance,
    ) -> t.ContainerMapping:
        """Build tap instance representation."""
        return {
            "tap_id": tap_instance.tap_id,
            "tap_type": tap_instance.tap_type,
        }

    def discover_streams(
        self,
        _tap_instance: m.Meltano.TapInstance,
    ) -> r[t.ContainerMapping]:
        """Discover available streams for tap instance."""
        stream_defs: Sequence[t.ContainerMapping] = [
            {"stream_name": "users", "tap_stream_id": "users"},
            {"stream_name": "orders", "tap_stream_id": "orders"},
        ]
        for stream_def in stream_defs:
            name = str(stream_def.get("stream_name", ""))
            if name and name not in self._stream_registry:
                self._stream_registry[name] = m.Meltano.StreamDefinition(
                    stream_name=name,
                    stream_schema={
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                    },
                    source_type=_tap_instance.tap_type,
                )
        return r[t.ContainerMapping].ok({"streams": stream_defs})

    def sync_stream(
        self,
        _tap_instance: m.Meltano.TapInstance,
        stream_name: str,
        target_config: m.Meltano.TargetConfig | None = None,
    ) -> r[t.ContainerMapping]:
        """Sync a stream from tap to target."""
        result: t.ContainerMapping = {
            "stream_name": stream_name,
            "status": c.Meltano.Enums.StreamStatus.COMPLETED,
            "target_loaded": target_config is not None,
            "records_processed": 0,
        }
        return r[t.ContainerMapping].ok(result)

    def get_stream_config(
        self,
        config: m.Meltano.TapConfig,
        stream_name: str,
    ) -> t.ContainerMapping:
        """Get configuration for a specific stream."""
        if config.stream_config and stream_name in config.stream_config:
            val = config.stream_config[stream_name]
            if isinstance(val, dict):
                return val
        return {}

    def create_tap_from_config(
        self,
        tap_type: str,
        connection_config: t.ContainerMapping,
        stream_config: t.ContainerMapping | None = None,
    ) -> r[m.Meltano.TapInstance]:
        """Create a TapInstance from configuration."""
        try:
            tap_cfg = m.Meltano.TapConfig(
                tap_type=tap_type,
                connection_config=connection_config,
                stream_config=stream_config if stream_config is not None else {},
            )
            instance = m.Meltano.TapInstance(
                tap_type=tap_type,
                config=tap_cfg,
                tap_id=f"{tap_type}_auto",
            )
            return r[m.Meltano.TapInstance].ok(instance)
        except (ValueError, TypeError, AttributeError) as e:
            return r[m.Meltano.TapInstance].fail(f"Failed to create tap: {e}")

    def generate_catalog(
        self,
        _tap_instance: m.Meltano.TapInstance,
    ) -> r[t.ContainerMapping]:
        """Generate Singer catalog from tap instance streams."""
        streams: list[t.ContainerMapping] = []
        catalog: t.ContainerMapping = {"version": 1, "streams": streams}
        return r[t.ContainerMapping].ok(catalog)

    def get_stream_by_name(
        self,
        tap_instance: m.Meltano.TapInstance,
        stream_name: str,
    ) -> r[t.ContainerMapping]:
        """Get stream definition by name."""
        discovery = self.discover_streams(tap_instance)
        if discovery.is_failure:
            return r[t.ContainerMapping].fail(discovery.error or "Discovery failed")
        raw = discovery.value
        raw_streams: MutableSequence[t.ContainerMapping] = []
        if isinstance(raw, dict):
            raw_val = raw.get("streams")
            if isinstance(raw_val, list):
                raw_streams = [s for s in raw_val if isinstance(s, dict)]
        for stream in raw_streams:
            if stream.get("stream_name") == stream_name:
                result_stream: t.ContainerMapping = {**stream, "name": stream_name}
                return r[t.ContainerMapping].ok(result_stream)
        return r[t.ContainerMapping].fail(f"Stream '{stream_name}' not found")

    def list_streams(
        self,
        tap_instance: m.Meltano.TapInstance,
    ) -> Sequence[str]:
        """List stream names available in tap instance."""
        discovery = self.discover_streams(tap_instance)
        if discovery.is_failure:
            return []
        raw = discovery.value
        raw_streams: MutableSequence[t.ContainerMapping] = []
        if isinstance(raw, dict):
            raw_val = raw.get("streams")
            if isinstance(raw_val, list):
                raw_streams = [s for s in raw_val if isinstance(s, dict)]
        return [str(s.get("stream_name", "")) for s in raw_streams]

    def get_tap_type(self, tap_instance: m.Meltano.TapInstance) -> str:
        """Get tap type from instance."""
        return tap_instance.tap_type

    def get_registered_streams(self) -> Sequence[str]:
        """Get list of registered stream names."""
        return [*self._stream_registry.keys()]

    def extract_records(
        self,
        _stream: m.Meltano.StreamDefinition,
        _limit: int | None = None,
    ) -> r[Sequence[t.ContainerMapping]]:
        """Extract records from a stream (mock data based on schema properties)."""
        schema = _stream.stream_schema
        properties: Mapping[str, t.ContainerMapping] = {}
        if isinstance(schema, dict):
            props_val = schema.get("properties")
            if isinstance(props_val, dict):
                properties = {
                    field_name: field_definition
                    for field_name, field_definition in props_val.items()
                    if isinstance(field_definition, dict)
                }
        mock_record: MutableMapping[str, str | int | float] = {}
        for field_name, field_def in properties.items():
            field_type = (
                field_def.get("type", "string")
                if isinstance(field_def, dict)
                else "string"
            )
            if field_type == "integer":
                mock_record[field_name] = 1
            elif field_type == "number":
                mock_record[field_name] = 1.0
            else:
                mock_record[field_name] = f"mock_{field_name}"
        if not mock_record:
            mock_record["id"] = 1
        total_records = c.Meltano.Defaults.MOCK_RECORD_COUNT
        if _limit is not None:
            total_records = min(_limit, total_records)
        records: Sequence[t.ContainerMapping] = [
            dict(mock_record) for _ in range(total_records)
        ]
        return r[Sequence[t.ContainerMapping]].ok(records)

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute abstractions service."""
        return r[t.Meltano.MeltanoConfigDict].ok(
            {"status": c.Meltano.Enums.StreamStatus.COMPLETED},
        )

    @staticmethod
    def create_result_instance() -> r[FlextMeltanoAbstractions]:
        """Factory method for creating a FlextMeltanoAbstractions instance."""
        return r[FlextMeltanoAbstractions].ok(FlextMeltanoAbstractions())

    def _create_catalog_entry_from_stream(
        self,
        stream: m.Meltano.StreamDefinition,
    ) -> r[t.ContainerMapping]:
        """Create Singer catalog entry from stream definition."""
        entry: t.ContainerMapping = {
            "tap_stream_id": stream.stream_name,
            "stream": stream.stream_name,
            "schema": stream.stream_schema,
            "metadata": list[t.ContainerMapping](),
        }
        return r[t.ContainerMapping].ok(entry)


__all__ = ["FlextMeltanoAbstractions"]
