"""FLEXT Pipeline Abstractions - in-process Meltano runtime operations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from collections.abc import Mapping, MutableMapping, Sequence
from pathlib import Path
from typing import override

from flext_meltano import (
    FlextMeltanoServiceBase,
    FlextMeltanoSettings,
    c,
    e,
    m,
    p,
    r,
    t,
    u,
)
from flext_meltano.services import FlextMeltanoExecutorBase


class FlextMeltanoAbstractions(FlextMeltanoServiceBase):
    """Core abstraction wrapping the imported Meltano runtime with r[T] results."""

    service_name: t.NonEmptyStr = m.Field(
        default="FlextMeltanoAbstractions",
        description="Canonical Meltano abstractions service name.",
        validate_default=True,
    )

    @staticmethod
    def _settings() -> FlextMeltanoSettings:
        """Resolve the shared settings singleton at the point of use.

        Importing this module must not materialize settings, so composition
        happens here instead of at module scope (NS-CONTRACT-001).
        ``fetch_global`` is a lazy thread-safe singleton, so every access
        yields the same instance without extra work.

        Returns:
            The resulting ``FlextMeltanoSettings``.

        """
        return FlextMeltanoSettings.fetch_global()

    def _run_meltano(self, args: Sequence[str]) -> p.Result[str]:
        """Run a Meltano runtime command and return stdout on success.

        Returns:
            The resulting ``p.Result[str]``.

        """
        cwd = Path(self._settings().Meltano.project_root)
        run_result: p.Result[m.Meltano.CommandExecutionResult] = (
            FlextMeltanoExecutorBase().execute_meltano_command(list(args), _cwd=cwd)
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

    @staticmethod
    def _resolve_project_root(
        project: t.JsonPayload | t.JsonMapping | None,
    ) -> Path | None:
        """Extract a project root path from supported project-like objects.

        Returns:
            The resulting ``Path | None``.

        """
        if isinstance(project, Mapping):
            project_mapping = u.Cli.JSON_MAPPING_ADAPTER.validate_python(project)
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
        """List installed project plugins of *plugin_type* via Meltano runtime.

        Returns:
            The resulting ``p.Result[t.Meltano.NestedStrMapping]``.

        """
        try:
            cwd = self._resolve_project_root(_project)
            plugins_result = FlextMeltanoExecutorBase().fetch_project_plugins(
                plugin_type=u.Meltano.normalize_plugin_group(plugin_type),
                _cwd=cwd,
            )
        except c.EXC_ATTR_KEY_OS_TYPE_VALUE as exc:
            error_msg = f"Failed to get plugins of type {plugin_type}: {exc}"
            return r[t.Meltano.NestedStrMapping].fail(error_msg)
        if plugins_result.failure:
            return r[t.Meltano.NestedStrMapping].from_failure(plugins_result)
        plugins: MutableMapping[str, Mapping[str, str]] = {}
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

    @staticmethod
    def find_project(project_root: Path) -> p.Result[Path]:
        """Find and validate a Meltano project directory.

        Returns:
            The resulting ``p.Result[Path]``.

        """
        try:
            if not project_root.exists() or not project_root.is_dir():
                return r[Path].fail(
                    f"Project path is not a valid directory: {project_root}",
                )
            return r[Path].ok(project_root)
        except c.EXC_ATTR_KEY_OS_TYPE_VALUE as exc:
            error_msg = f"Failed to load pipeline project: {exc}"
            return r[Path].fail(error_msg)

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute abstractions service and return real configuration state.

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """
        meltano_settings = self._settings().Meltano
        payload: t.JsonMapping = {
            "status": c.Meltano.StreamStatus.COMPLETED,
            "project_root": meltano_settings.project_root,
            "environment": meltano_settings.environment,
            "meltano_version": meltano_settings.meltano_version,
        }
        return r[t.JsonMapping].ok(payload)

    def discover_streams(
        self,
        tap_instance: m.Meltano.TapInstance,
    ) -> p.Result[t.JsonMapping]:
        """Discover available streams via ``meltano select --list``.

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """

        def _run_discover_streams() -> p.Result[t.JsonMapping]:
            cmd_result = self._run_meltano([
                c.Meltano.CMD_SELECT,
                tap_instance.tap_type,
                c.Meltano.CMD_LIST_OPTION,
                c.Meltano.CMD_ALL_OPTION,
            ])
            if cmd_result.failure:
                return r[t.JsonMapping].from_failure(cmd_result)
            stream_defs: t.JsonValueList = []
            for line in cmd_result.value.splitlines():
                name = line.strip()
                if name and not name.startswith("["):
                    stream_defs.append({
                        c.Meltano.PayloadKey.STREAM_NAME: name,
                        c.Meltano.PayloadKey.TAP_STREAM_ID: name,
                    })
            payload: t.JsonDict = {c.Meltano.PayloadKey.STREAMS: stream_defs}
            return r[t.JsonMapping].ok(payload)

        try:
            return _run_discover_streams()
        except c.EXC_ATTR_KEY_OS_TYPE_VALUE as exc:
            self.logger.exception(
                c.Meltano.LOG_MESSAGE_DISCOVER_STREAMS_FAILED,
                error=str(exc),
            )
            return e.fail_operation(
                c.Meltano.OPERATION_DISCOVER_STREAMS,
                exc,
                result_type=r[t.JsonMapping],
            )


__all__: list[str] = ["FlextMeltanoAbstractions"]
