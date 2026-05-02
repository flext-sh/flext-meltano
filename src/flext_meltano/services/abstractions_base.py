"""FLEXT Pipeline Abstractions - Base class with in-process Meltano operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    MutableMapping,
)
from pathlib import Path
from typing import ClassVar, override

from flext_meltano import (
    FlextMeltanoExecutorBase,
    FlextMeltanoServiceBase,
    c,
    m,
    p,
    r,
    t,
    u,
)


class FlextMeltanoAbstractionsBase(FlextMeltanoServiceBase):
    """Base abstraction wrapping the imported Meltano runtime with r[T] results."""

    _stream_registry: ClassVar[MutableMapping[str, m.Meltano.StreamDefinition]] = {}
    service_name: t.NonEmptyStr = u.Field(
        default="FlextMeltanoAbstractions",
        description="Canonical Meltano abstractions service name.",
        validate_default=True,
    )

    def _run_meltano(self, args: t.StrSequence) -> p.Result[str]:
        """Run a Meltano runtime command and return stdout on success."""
        cwd = u.Meltano.resolve_project_root(self.settings)
        run_result: p.Result[m.Meltano.CommandExecutionResult] = (
            FlextMeltanoExecutorBase().execute_meltano_command(
                list(args),
                _cwd=cwd,
            )
        )
        if run_result.failure:
            error_msg = run_result.error or "Unknown error"
            return r[str].fail_op("Meltano command", error_msg)
        completed: m.Meltano.CommandExecutionResult = run_result.value
        if completed.exit_code != 0:
            stderr_out = completed.error.strip() or completed.output.strip()
            return r[str].fail(
                stderr_out or f"meltano exited with code {completed.exit_code}",
            )
        return r[str].ok(completed.output.strip())

    def add_plugin_by_config(self, plugin_config: t.JsonMapping) -> p.Result[bool]:
        """Add a plugin to the Meltano project via ``meltano add``."""
        try:
            plugin_type = str(plugin_config.get("plugin_type", ""))
            plugin_name = str(plugin_config.get("plugin_name", ""))
            if not plugin_type or not plugin_name:
                return r[bool].fail("plugin_type and plugin_name are required")
            cmd_result = self._run_meltano(
                [c.Meltano.CMD_ADD, plugin_type, plugin_name],
            )
            if cmd_result.failure:
                return r[bool].fail(cmd_result.error or "Failed to add plugin")
            return r[bool].ok(value=True)
        except c.Meltano.OPERATION_ERRORS as e:
            error_msg = f"Failed to add plugin: {e}"
            return r[bool].fail(error_msg)

    @staticmethod
    def _resolve_project_root(
        project: t.JsonPayload | t.JsonMapping | None,
    ) -> Path | None:
        """Extract a project root path from supported project-like objects."""
        if isinstance(project, Mapping):
            project_mapping = t.Cli.JSON_MAPPING_ADAPTER.validate_python(project)
            for key in ("root_dir", "root"):
                mapping_value = project_mapping.get(key)
                if isinstance(mapping_value, str) and mapping_value:
                    return Path(mapping_value)
        return None

    def fetch_plugins_of_type(
        self,
        _project: t.JsonPayload | t.JsonMapping | None,
        plugin_type: str,
    ) -> p.Result[t.Meltano.NestedStrMapping]:
        """List installed project plugins of *plugin_type* via Meltano runtime."""
        try:
            cwd = self._resolve_project_root(_project)
            plugins_result = FlextMeltanoExecutorBase().fetch_project_plugins(
                plugin_type=u.Meltano.normalize_plugin_group(plugin_type),
                _cwd=cwd,
            )
            if plugins_result.failure:
                return r[t.Meltano.NestedStrMapping].fail(
                    plugins_result.error or f"Failed to list {plugin_type}",
                )
            plugins: dict[str, t.StrMapping] = {}
            for plugin in plugins_result.value:
                plugin_name = plugin.get("name", "")
                if not plugin_name:
                    continue
                plugins[plugin_name] = {
                    "name": plugin_name,
                    "type": plugin_type,
                    "status": c.Meltano.OperationStatus.AVAILABLE,
                }
            return r[t.Meltano.NestedStrMapping].ok(plugins)
        except c.Meltano.OPERATION_ERRORS as e:
            error_msg = f"Failed to get plugins of type {plugin_type}: {e}"
            return r[t.Meltano.NestedStrMapping].fail(error_msg)

    def execute_singer_pipeline(
        self,
        elt_context: t.JsonMapping,
        extractor_plugin: t.JsonMapping | None,
        loader_plugin: t.JsonMapping | None,
    ) -> p.Result[t.HeaderMapping]:
        """Execute a Singer ELT pipeline via ``meltano elt``."""
        try:
            extractor_mapping = extractor_plugin
            loader_mapping = loader_plugin
            extractor_name = str(
                elt_context.get("extractor_name", c.IDENTIFIER_UNKNOWN)
                if extractor_mapping is None
                else extractor_mapping.get("name") or c.IDENTIFIER_UNKNOWN,
            )
            loader_name = str(
                elt_context.get("loader_name", c.IDENTIFIER_UNKNOWN)
                if loader_mapping is None
                else loader_mapping.get("name") or c.IDENTIFIER_UNKNOWN,
            )
            cmd_result = self._run_meltano(
                [c.Meltano.CMD_ELT, extractor_name, loader_name],
            )
            if cmd_result.failure:
                return r[t.HeaderMapping].fail(
                    cmd_result.error or "Pipeline execution failed",
                )
            result: t.MutableHeaderMapping = {
                "status": c.Meltano.StreamStatus.COMPLETED,
                "source": extractor_name,
                "sink": loader_name,
                "records_processed": 0,
            }
            return r[t.HeaderMapping].ok(result)
        except c.Meltano.OPERATION_ERRORS as e:
            error_msg = f"Failed to execute singer pipeline: {e}"
            return r[t.HeaderMapping].fail(error_msg)

    def find_project(self, project_root: Path) -> p.Result[Path]:
        """Find and validate a Meltano project directory."""
        try:
            if not project_root.exists() or not project_root.is_dir():
                return r[Path].fail(
                    f"Project path is not a valid directory: {project_root}",
                )
            return r[Path].ok(project_root)
        except c.Meltano.OPERATION_ERRORS as e:
            error_msg = f"Failed to load pipeline project: {e}"
            return r[Path].fail(error_msg)

    def fetch_project_root(self) -> p.Result[Path]:
        """Get the root directory from settings."""
        project_root = self.settings.project_root
        if project_root == Path():
            return r[Path].fail("No project root configured in settings")
        try:
            return r[Path].ok(project_root)
        except c.Meltano.OPERATION_ERRORS as e:
            return r[Path].fail(f"Failed to get project root: {e}")

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute abstractions service and return real configuration state."""
        payload: t.JsonMapping = {
            "status": c.Meltano.StreamStatus.COMPLETED,
            "project_root": str(self.settings.project_root),
            "environment": self.settings.environment,
            "meltano_version": self.settings.meltano_version,
        }
        return r[t.JsonMapping].ok(payload)

    def _create_catalog_entry_from_stream(
        self,
        stream: m.Meltano.StreamDefinition,
    ) -> p.Result[t.JsonMapping]:
        """Create Singer catalog entry from stream definition."""
        entry: t.JsonMapping = t.Cli.JSON_MAPPING_ADAPTER.validate_python({
            "tap_stream_id": stream.stream_name,
            "stream": stream.stream_name,
            "schema": stream.stream_schema,
            "metadata": list[t.JsonValue](),
        })
        return r[t.JsonMapping].ok(entry)

    def fetch_stream_config(
        self,
        settings: m.Meltano.TapConfig,
        stream_name: str,
    ) -> t.JsonMapping:
        """Get configuration for a specific stream."""
        if settings.stream_config and stream_name in settings.stream_config:
            val = settings.stream_config[stream_name]
            if isinstance(val, Mapping):
                return t.Cli.JSON_MAPPING_ADAPTER.validate_python(val)
        return {}

    def fetch_tap_type(self, tap_instance: m.Meltano.TapInstance) -> str:
        """Get tap type from instance."""
        return tap_instance.tap_type

    def fetch_registered_streams(self) -> t.StrSequence:
        """Get list of registered stream names."""
        return [*self._stream_registry.keys()]
