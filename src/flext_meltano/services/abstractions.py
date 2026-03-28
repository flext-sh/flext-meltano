"""FLEXT Pipeline Abstractions - Core Meltano CLI operations via subprocess.

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


class FlextMeltanoAbstractions(FlextMeltanoServiceBase):
    """Core abstraction wrapping Meltano CLI via subprocess with r[T] results."""

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

    # -- Tap-specific operations (discovery, sync, catalog) --

    def process_tap_config(self, config: m.Meltano.TapConfig) -> r[m.Meltano.TapConfig]:
        """Validate and return tap configuration."""
        return r[m.Meltano.TapConfig].ok(config)

    def build_tap_instance(
        self,
        tap_instance: m.Meltano.TapInstance,
    ) -> t.ContainerMapping:
        """Build tap instance representation."""
        return {"tap_id": tap_instance.tap_id, "tap_type": tap_instance.tap_type}

    def discover_streams(
        self,
        tap_instance: m.Meltano.TapInstance,
    ) -> r[t.ContainerMapping]:
        """Discover available streams via ``meltano select --list``."""
        try:
            cmd_result = self._run_meltano(
                ["select", tap_instance.tap_type, "--list", "--all"],
            )
            if cmd_result.is_failure:
                return r[t.ContainerMapping].fail(
                    cmd_result.error or "Stream discovery failed",
                )
            stream_defs: list[t.ContainerMapping] = []
            for line in cmd_result.value.splitlines():
                name = line.strip()
                if name and not name.startswith("["):
                    stream_defs.append({"stream_name": name, "tap_stream_id": name})
                    if name not in self._stream_registry:
                        self._stream_registry[name] = m.Meltano.StreamDefinition(
                            stream_name=name,
                            stream_schema={"type": "object", "properties": {}},
                            source_type=tap_instance.tap_type,
                        )
            return r[t.ContainerMapping].ok({"streams": stream_defs})
        except _OPERATION_ERRORS as e:
            error_msg = f"Failed to discover streams: {e}"
            self.logger.exception(error_msg)
            return r[t.ContainerMapping].fail(error_msg)

    def sync_stream(
        self,
        tap_instance: m.Meltano.TapInstance,
        stream_name: str,
        target_config: m.Meltano.TargetConfig | None = None,
    ) -> r[t.ContainerMapping]:
        """Sync a single stream via ``meltano elt`` with stream selection."""
        try:
            loader_name = (
                target_config.target_type
                if target_config is not None
                else c.IDENTIFIER_UNKNOWN
            )
            cmd_args = [
                "elt",
                tap_instance.tap_type,
                str(loader_name),
                "--select",
                stream_name,
            ]
            cmd_result = self._run_meltano(cmd_args)
            status = (
                c.Meltano.Enums.StreamStatus.COMPLETED
                if cmd_result.is_success
                else c.Meltano.Enums.StreamStatus.FAILED
            )
            result: t.ContainerMapping = {
                "stream_name": stream_name,
                "status": status,
                "target_loaded": target_config is not None,
            }
            if cmd_result.is_failure:
                return r[t.ContainerMapping].fail(
                    cmd_result.error or "Stream sync failed"
                )
            return r[t.ContainerMapping].ok(result)
        except _OPERATION_ERRORS as e:
            error_msg = f"Failed to sync stream {stream_name}: {e}"
            self.logger.exception(error_msg)
            return r[t.ContainerMapping].fail(error_msg)

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
        except _OPERATION_ERRORS as e:
            return r[m.Meltano.TapInstance].fail(f"Failed to create tap: {e}")

    def generate_catalog(
        self,
        tap_instance: m.Meltano.TapInstance,
    ) -> r[t.ContainerMapping]:
        """Generate Singer catalog by discovering streams from the tap."""
        discovery = self.discover_streams(tap_instance)
        if discovery.is_failure:
            return r[t.ContainerMapping].fail(
                discovery.error or "Catalog generation failed"
            )
        raw = discovery.value
        streams: list[t.ContainerMapping] = []
        for s in _extract_raw_streams(raw):
            name = str(s.get("stream_name", ""))
            if name in self._stream_registry:
                entry_r = self._create_catalog_entry_from_stream(
                    self._stream_registry[name],
                )
                if entry_r.is_success:
                    streams.append(entry_r.value)
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
        for stream in _extract_raw_streams(discovery.value):
            if stream.get("stream_name") == stream_name:
                result_stream: t.ContainerMapping = {**stream, "name": stream_name}
                return r[t.ContainerMapping].ok(result_stream)
        return r[t.ContainerMapping].fail(f"Stream '{stream_name}' not found")

    def list_streams(self, tap_instance: m.Meltano.TapInstance) -> Sequence[str]:
        """List stream names available in tap instance."""
        discovery = self.discover_streams(tap_instance)
        if discovery.is_failure:
            return []
        return [
            str(s.get("stream_name", "")) for s in _extract_raw_streams(discovery.value)
        ]

    def get_tap_type(self, tap_instance: m.Meltano.TapInstance) -> str:
        """Get tap type from instance."""
        return tap_instance.tap_type

    def get_registered_streams(self) -> Sequence[str]:
        """Get list of registered stream names."""
        return [*self._stream_registry.keys()]


def _extract_raw_streams(raw: t.ContainerMapping) -> list[t.ContainerMapping]:
    """Extract stream dicts from a discovery result mapping."""
    if isinstance(raw, dict):
        raw_val = raw.get("streams")
        if isinstance(raw_val, list):
            return [s for s in raw_val if isinstance(s, dict)]
    return []


# Backward-compatible alias for code that imported the tap subclass
FlextMeltanoAbstractionsTap = FlextMeltanoAbstractions

__all__ = ["FlextMeltanoAbstractions", "FlextMeltanoAbstractionsTap"]
