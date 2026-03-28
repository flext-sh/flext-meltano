"""FLEXT Pipeline Abstractions - Base class with core Meltano CLI operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from pathlib import Path
from typing import ClassVar, override

from flext_core import r
from flext_infra import FlextInfraUtilitiesSubprocess

from flext_meltano import FlextMeltanoServiceBase, c, m, p, t

_OPERATION_ERRORS = (ValueError, TypeError, KeyError, AttributeError, OSError)


class _FlextMeltanoAbstractionsBase(FlextMeltanoServiceBase):
    """Base abstraction wrapping Meltano CLI via subprocess with r[T] results."""

    _stream_registry: ClassVar[MutableMapping[str, m.Meltano.StreamDefinition]] = {}
    service_name: str = "FlextMeltanoAbstractions"

    def _run_meltano(self, args: Sequence[str]) -> r[str]:
        """Run a meltano CLI command and return stdout on success."""
        cmd: Sequence[str] = ["meltano", *args]
        cwd = (
            self.settings.project_root if self.settings.project_root != Path() else None
        )
        run_result = FlextInfraUtilitiesSubprocess.run_raw(cmd, cwd=cwd)
        if run_result.is_failure:
            error_msg = run_result.error or "Unknown error"
            if "FileNotFoundError" in error_msg or "not found" in error_msg.lower():
                return r[str].fail("Meltano CLI executable not found")
            return r[str].fail(f"Meltano command failed: {error_msg}")
        completed = run_result.value
        if completed.exit_code != 0:
            stderr_out = completed.stderr.strip() or completed.stdout.strip()
            return r[str].fail(
                stderr_out or f"meltano exited with code {completed.exit_code}",
            )
        return r[str].ok(completed.stdout.strip())

    def add_plugin(self, plugin_config: t.Meltano.PluginConfiguration) -> r[bool]:
        """Add a plugin to the Meltano project via ``meltano add``."""
        try:
            plugin_type = str(plugin_config.get("plugin_type", ""))
            plugin_name = str(plugin_config.get("plugin_name", ""))
            if not plugin_type or not plugin_name:
                return r[bool].fail("plugin_type and plugin_name are required")
            cmd_result = self._run_meltano(["add", plugin_type, plugin_name])
            if cmd_result.is_failure:
                return r[bool].fail(cmd_result.error or "Failed to add plugin")
            self.logger.info(
                "Plugin added",
                plugin_type=plugin_type,
                plugin_name=plugin_name,
            )
            return r[bool].ok(value=True)
        except _OPERATION_ERRORS as e:
            error_msg = f"Failed to add plugin: {e}"
            self.logger.exception(error_msg)
            return r[bool].fail(error_msg)

    def get_plugins_of_type(
        self,
        _project: p.Meltano.Project | t.Meltano.Dbt.Project | FlextMeltanoServiceBase,
        plugin_type: str,
    ) -> r[Mapping[str, t.Meltano.PluginDefinition]]:
        """List installed plugins of *plugin_type* via ``meltano list``."""
        try:
            cmd_result = self._run_meltano(["list", plugin_type])
            if cmd_result.is_failure:
                return r[Mapping[str, t.Meltano.PluginDefinition]].fail(
                    cmd_result.error or f"Failed to list {plugin_type}",
                )
            plugins: MutableMapping[str, t.Meltano.PluginDefinition] = {}
            for line in cmd_result.value.splitlines():
                name = line.strip()
                if name:
                    plugins[name] = {
                        "name": name,
                        "type": plugin_type,
                        "status": c.Meltano.Enums.OperationStatus.AVAILABLE,
                    }
            return r[Mapping[str, t.Meltano.PluginDefinition]].ok(plugins)
        except _OPERATION_ERRORS as e:
            error_msg = f"Failed to get plugins of type {plugin_type}: {e}"
            self.logger.exception(error_msg)
            return r[Mapping[str, t.Meltano.PluginDefinition]].fail(error_msg)

    def execute_singer_pipeline(
        self,
        elt_context: t.Meltano.MeltanoConfigDict,
        extractor_plugin: p.Meltano.Plugin,
        loader_plugin: p.Meltano.Plugin,
    ) -> r[t.Meltano.ELT.PipelineResult]:
        """Execute a Singer ELT pipeline via ``meltano elt``."""
        try:
            extractor_name = str(
                getattr(extractor_plugin, "name", None)
                or elt_context.get("extractor_name", c.IDENTIFIER_UNKNOWN),
            )
            loader_name = str(
                getattr(loader_plugin, "name", None)
                or elt_context.get("loader_name", c.IDENTIFIER_UNKNOWN),
            )
            cmd_result = self._run_meltano(["elt", extractor_name, loader_name])
            if cmd_result.is_failure:
                return r[t.Meltano.ELT.PipelineResult].fail(
                    cmd_result.error or "Pipeline execution failed",
                )
            result: t.Meltano.ELT.PipelineResult = {
                "status": c.Meltano.Enums.StreamStatus.COMPLETED,
                "source": extractor_name,
                "sink": loader_name,
                "records_processed": 0,
            }
            return r[t.Meltano.ELT.PipelineResult].ok(result)
        except _OPERATION_ERRORS as e:
            error_msg = f"Failed to execute singer pipeline: {e}"
            self.logger.exception(error_msg)
            return r[t.Meltano.ELT.PipelineResult].fail(error_msg)

    def find_project(self, project_root: Path) -> r[Path]:
        """Find and validate a Meltano project directory."""
        try:
            if not project_root.exists() or not project_root.is_dir():
                return r[Path].fail(
                    f"Project path is not a valid directory: {project_root}",
                )
            self.logger.info(
                "Pipeline project loaded successfully",
                project_root=str(project_root),
            )
            return r[Path].ok(project_root)
        except _OPERATION_ERRORS as e:
            error_msg = f"Failed to load pipeline project: {e}"
            self.logger.exception(error_msg)
            return r[Path].fail(error_msg)

    def get_project_root(self) -> r[Path]:
        """Get the root directory from settings."""
        project_root = self.settings.project_root
        if project_root == Path():
            return r[Path].fail("No project root configured in settings")
        try:
            return r[Path].ok(project_root)
        except _OPERATION_ERRORS as e:
            return r[Path].fail(f"Failed to get project root: {e}")

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute abstractions service and return real configuration state."""
        return r[t.Meltano.MeltanoConfigDict].ok({
            "status": c.Meltano.Enums.StreamStatus.COMPLETED,
            "project_root": str(self.settings.project_root),
            "environment": self.settings.environment,
            "meltano_version": self.settings.meltano_version,
        })

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

    def get_tap_type(self, tap_instance: m.Meltano.TapInstance) -> str:
        """Get tap type from instance."""
        return tap_instance.tap_type

    def get_registered_streams(self) -> Sequence[str]:
        """Get list of registered stream names."""
        return [*self._stream_registry.keys()]
