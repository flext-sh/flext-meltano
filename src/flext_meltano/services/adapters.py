"""FLEXT Meltano Adapters - SOLID-compliant adapter classes following FLEXT patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from collections.abc import Sequence
from pathlib import Path
from typing import override

from flext_core import FlextSettings, r, s
from flext_meltano import (
    FlextMeltanoExecutorBase,
    FlextMeltanoServiceBase,
    FlextMeltanoSettings,
    c,
    t,
    u,
)


class FlextMeltanoAdapter(FlextMeltanoServiceBase):
    """Base adapter namespace class for focused integrations."""

    class ProjectAdapter(s[t.Meltano.ExecutionResultDict]):
        """Focused adapter for Meltano project management following SOLID principles."""

        @classmethod
        @override
        def _get_service_config_type(cls) -> type[FlextSettings]:
            return FlextMeltanoSettings

        def create_project(
            self,
            project_name: str,
            project_dir: Path,
        ) -> r[t.Meltano.ExecutionResultDict]:
            """Create a new Meltano project via the imported library."""
            project_path = Path(project_dir) / project_name
            init_result = FlextMeltanoExecutorBase.initialize_project_root(
                project_path,
            )
            if init_result.is_failure:
                return r[t.Meltano.ExecutionResultDict].fail(
                    init_result.error or "Project creation failed",
                )
            result: t.Meltano.ExecutionResultDict = u.Meltano.build_status_payload(
                c.Meltano.Enums.OperationStatus.CREATED,
                extra_fields={
                    "project_name": project_name,
                    "project_path": str(project_path),
                    "output": f"Initialized {c.Meltano.Paths.MELTANO_PROJECT_FILE}",
                    "error": "",
                    "created_at": str(time.time()),
                },
            )
            return r[t.Meltano.ExecutionResultDict].ok(result)

        @override
        def execute(self) -> r[t.Meltano.ExecutionResultDict]:
            """Execute default project operation."""
            return self.get_version()

        def get_version(self) -> r[t.Meltano.ExecutionResultDict]:
            """Get Meltano version information using native API."""
            version_result = FlextMeltanoExecutorBase.get_version()
            if version_result.is_failure:
                return r[t.Meltano.ExecutionResultDict].fail(
                    version_result.error or "Failed to get Meltano version",
                )
            meltano_version = version_result.value
            version_info: t.Meltano.ExecutionResultDict = {
                "version": meltano_version,
                "meltano": meltano_version,
                "cli_type": "native_meltano_api",
                "integration": "flext-core",
            }
            return r[t.Meltano.ExecutionResultDict].ok(version_info)

        def initialize_project(
            self, project_root: Path
        ) -> r[t.Meltano.ExecutionResultDict]:
            """Initialize Meltano project using railway pattern."""
            return self.create_project(
                project_name=project_root.name,
                project_dir=project_root.parent,
            )

    class PluginAdapter(s[Sequence[t.Meltano.PluginDefinition]]):
        """Focused adapter for Meltano plugin management following SOLID principles."""

        @classmethod
        @override
        def _get_service_config_type(cls) -> type[FlextSettings]:
            return FlextMeltanoSettings

        def discover_plugins(
            self,
            plugin_type: str | None = None,
        ) -> r[Sequence[t.Meltano.PluginDefinition]]:
            """Discover available plugins via Meltano project runtime."""
            try:
                executor = FlextMeltanoExecutorBase()
                plugins_result = executor.get_project_plugins(
                    plugin_type=plugin_type,
                    _cwd=u.Meltano.resolve_project_root(self.settings.model_dump()),
                )
                if plugins_result.is_failure:
                    return r[Sequence[t.Meltano.PluginDefinition]].fail(
                        plugins_result.error or "Plugin discovery failed",
                    )
                plugins: list[t.Meltano.PluginDefinition] = []
                for plugin in plugins_result.value:
                    plugin_name = str(plugin.get("name", ""))
                    plugin_group = str(plugin.get("type", ""))
                    if not plugin_name:
                        continue
                    plugins.append({
                        "name": plugin_name,
                        "type": u.Meltano.normalize_discovered_plugin_type(
                            plugin_group,
                            plugin_name,
                        ),
                    })
                return r[Sequence[t.Meltano.PluginDefinition]].ok(plugins)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as ex:
                return r[Sequence[t.Meltano.PluginDefinition]].fail(
                    f"Plugin discovery failed: {ex}"
                )

        @override
        def execute(self) -> r[Sequence[t.Meltano.PluginDefinition]]:
            """Execute default plugin operation."""
            return self.discover_plugins()

    @override
    def execute(self) -> r[t.ContainerMapping]:
        """Execute adapter service returning current settings."""
        return r[t.ContainerMapping].ok(u.Meltano.coerce_config_mapping(self.settings))


__all__ = ["FlextMeltanoAdapter"]
