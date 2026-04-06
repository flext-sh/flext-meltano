"""FLEXT Pipeline Abstractions - Base class with in-process Meltano operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, override

from pydantic import Field, ValidationError

import flext_meltano.services as meltano_services
from flext_meltano import FlextMeltanoServiceBase, FlextMeltanoSettings, c, m, r, t, u

if TYPE_CHECKING:
    from flext_meltano import FlextMeltanoExecutorBase, FlextMeltanoProjectService


class FlextMeltanoAbstractionsBase(FlextMeltanoServiceBase):
    """Base abstraction wrapping the imported Meltano runtime with r[T] results."""

    _stream_registry: ClassVar[MutableMapping[str, m.Meltano.StreamDefinition]] = {}
    service_name: str = Field(
        default="FlextMeltanoAbstractions",
        description="Canonical abstractions service instance name",
    )

    @staticmethod
    def _build_executor(
        _settings: FlextMeltanoSettings | t.ContainerMapping | None,
    ) -> FlextMeltanoExecutorBase:
        """Create an executor lazily to avoid import cycles during package init."""
        return meltano_services.FlextMeltanoExecutorBase()

    @staticmethod
    def _coerce_container_mapping(
        value: t.ContainerMapping | None,
    ) -> t.ContainerMapping | None:
        """Normalize runtime objects to canonical container mappings when possible."""
        if not isinstance(value, Mapping):
            return None
        try:
            return t.Meltano.CONTAINER_MAP_ADAPTER.validate_python(value)
        except ValidationError:
            return None

    def _run_meltano(self, args: t.StrSequence) -> r[str]:
        """Run a Meltano runtime command and return stdout on success."""
        cwd = u.Meltano.resolve_project_root(self.settings)
        run_result: r[m.Meltano.CommandExecutionResult] = self._build_executor(
            self.settings,
        ).execute_meltano_command(
            list(args),
            _cwd=cwd,
        )
        if run_result.is_failure:
            error_msg = str(run_result.error or "Unknown error")
            return r[str].fail(f"Meltano command failed: {error_msg}")
        completed: m.Meltano.CommandExecutionResult = run_result.value
        if completed.exit_code != 0:
            stderr_out = completed.error.strip() or completed.output.strip()
            return r[str].fail(
                stderr_out or f"meltano exited with code {completed.exit_code}",
            )
        return r[str].ok(completed.output.strip())

    def add_plugin_by_config(self, plugin_config: t.ContainerMapping) -> r[bool]:
        """Add a plugin to the Meltano project via ``meltano add``."""
        try:
            plugin_type = str(plugin_config.get("plugin_type", ""))
            plugin_name = str(plugin_config.get("plugin_name", ""))
            if not plugin_type or not plugin_name:
                return r[bool].fail("plugin_type and plugin_name are required")
            cmd_result = self._run_meltano(
                [c.Meltano.CMD_ADD, plugin_type, plugin_name],
            )
            if cmd_result.is_failure:
                return r[bool].fail(cmd_result.error or "Failed to add plugin")
            return r[bool].ok(value=True)
        except c.Meltano.OPERATION_ERRORS as e:
            error_msg = f"Failed to add plugin: {e}"
            return r[bool].fail(error_msg)

    @staticmethod
    def _resolve_project_root(
        project: FlextMeltanoProjectService | t.ContainerMapping | None,
    ) -> Path | None:
        """Extract a project root path from supported project-like objects."""
        project_mapping = FlextMeltanoAbstractionsBase._coerce_container_mapping(
            project if isinstance(project, Mapping) else None,
        )
        if project_mapping is not None:
            for key in ("root_dir", "root"):
                mapping_value = project_mapping.get(key)
                if isinstance(mapping_value, Path):
                    return mapping_value
                if isinstance(mapping_value, str) and mapping_value:
                    return Path(mapping_value)
        return None

    def get_plugins_of_type(
        self,
        _project: FlextMeltanoProjectService | t.ContainerMapping | None,
        plugin_type: str,
    ) -> r[t.Meltano.NestedStrMapping]:
        """List installed project plugins of *plugin_type* via Meltano runtime."""
        try:
            cwd = self._resolve_project_root(_project)
            plugins_result = self._build_executor(self.settings).get_project_plugins(
                plugin_type=u.Meltano.normalize_plugin_group(plugin_type),
                _cwd=cwd,
            )
            if plugins_result.is_failure:
                return r[t.Meltano.NestedStrMapping].fail(
                    plugins_result.error or f"Failed to list {plugin_type}",
                )
            plugins: dict[str, t.StrMapping] = {}
            for plugin in plugins_result.value:
                plugin_name = str(plugin.get("name", ""))
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
        elt_context: t.ContainerMapping,
        extractor_plugin: t.ContainerMapping | None,
        loader_plugin: t.ContainerMapping | None,
    ) -> r[t.HeaderMapping]:
        """Execute a Singer ELT pipeline via ``meltano elt``."""
        try:
            extractor_mapping = self._coerce_container_mapping(extractor_plugin)
            loader_mapping = self._coerce_container_mapping(loader_plugin)
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
            if cmd_result.is_failure:
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

    def find_project(self, project_root: Path) -> r[Path]:
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

    def get_project_root(self) -> r[Path]:
        """Get the root directory from settings."""
        project_root = self.settings.project_root
        if project_root == Path():
            return r[Path].fail("No project root configured in settings")
        try:
            return r[Path].ok(project_root)
        except c.Meltano.OPERATION_ERRORS as e:
            return r[Path].fail(f"Failed to get project root: {e}")

    @override
    def execute(self) -> r[t.ContainerMapping]:
        """Execute abstractions service and return real configuration state."""
        project_root = u.Meltano.resolve_project_root(self.settings)
        return r[t.ContainerMapping].ok({
            "status": c.Meltano.StreamStatus.COMPLETED,
            "project_root": str(project_root) if project_root is not None else "",
            "environment": self.settings.environment,
            "meltano_version": self.settings.meltano_version,
        })

    def _create_catalog_entry_from_stream(
        self,
        stream: m.Meltano.StreamDefinition,
    ) -> r[t.ContainerMapping]:
        """Create Singer catalog entry from stream definition."""
        entry: t.MutableContainerMapping = {
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

    def get_registered_streams(self) -> t.StrSequence:
        """Get list of registered stream names."""
        return [*self._stream_registry.keys()]
