"""FLEXT Meltano Adapters - SOLID-compliant adapter classes following FLEXT patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import override

from flext_core import FlextSettings

from flext_meltano import (
    FlextMeltanoExecutorBase,
    FlextMeltanoServiceBase,
    FlextMeltanoSettings,
    c,
    p,
    r,
    t,
    u,
)


class FlextMeltanoAdapter(FlextMeltanoServiceBase):
    """Base adapter namespace class for focused integrations."""

    class ProjectAdapter(FlextMeltanoServiceBase):
        """Focused adapter for Meltano project management following SOLID principles."""

        @classmethod
        def _get_service_config_type(cls) -> type[FlextSettings]:
            return FlextMeltanoSettings

        def create_project(
            self,
            project_name: str,
            project_dir: Path,
        ) -> p.Result[t.JsonMapping]:
            """Create a new Meltano project via the imported library."""
            project_path = Path(project_dir) / project_name
            init_result = FlextMeltanoExecutorBase.initialize_project_root(
                project_path,
            )
            if init_result.failure:
                return r[t.JsonMapping].fail(
                    init_result.error or "Project creation failed",
                )
            result: t.JsonMapping = {
                "status": c.Meltano.OperationStatus.CREATED,
                "project_name": project_name,
                "project_path": str(project_path),
                "output": f"Initialized {c.Meltano.PATH_MELTANO_PROJECT_FILE}",
                "error": "",
                "created_at": str(time.time()),
            }
            return r[t.JsonMapping].ok(result)

        @override
        def execute(self) -> p.Result[t.JsonMapping]:
            """Execute default project operation."""
            return self.fetch_version()

        def fetch_version(self) -> p.Result[t.JsonMapping]:
            """Get Meltano version information using native API."""
            version_result = FlextMeltanoExecutorBase.fetch_version()
            if version_result.failure:
                return r[t.JsonMapping].fail(
                    version_result.error or "Failed to get Meltano version",
                )
            meltano_version = version_result.value
            version_info: t.JsonMapping = {
                "version": meltano_version,
                "meltano": meltano_version,
                "cli_type": "native_meltano_api",
                "integration": "flext-core",
            }
            return r[t.JsonMapping].ok(version_info)

        def initialize_project(self, project_root: Path) -> p.Result[t.JsonMapping]:
            """Initialize Meltano project using railway pattern."""
            return self.create_project(
                project_name=project_root.name,
                project_dir=project_root.parent,
            )

    class PluginAdapter(FlextMeltanoServiceBase):
        """Focused adapter for Meltano plugin management following SOLID principles."""

        @classmethod
        def _get_service_config_type(cls) -> type[FlextSettings]:
            return FlextMeltanoSettings

        def discover_plugins(
            self,
            plugin_type: str | None = None,
        ) -> p.Result[t.JsonMapping]:
            """Discover available plugins via Meltano project runtime."""
            try:
                executor = FlextMeltanoExecutorBase()
                project_root = u.Meltano.resolve_project_root(self.settings)
                plugins_result = executor.fetch_project_plugins(
                    plugin_type=plugin_type,
                    _cwd=project_root,
                )
                if plugins_result.failure:
                    return r[t.JsonMapping].fail(
                        plugins_result.error or "Plugin discovery failed",
                    )
                plugins: list[t.JsonValue] = []
                for plugin in plugins_result.value:
                    plugin_name = str(plugin.get("name", ""))
                    plugin_group = str(plugin.get("type", ""))
                    if not plugin_name:
                        continue
                    plugins.append({
                        "name": plugin_name,
                        "type": plugin_group,
                    })
                return r[t.JsonMapping].ok({"plugins": plugins})
            except c.Meltano.OPERATION_ERRORS as ex:
                return r[t.JsonMapping].fail(f"Plugin discovery failed: {ex}")

        @override
        def execute(self) -> p.Result[t.JsonMapping]:
            """Execute default plugin operation."""
            return self.discover_plugins()

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute adapter service returning current settings."""
        return r[t.JsonMapping].ok(self.settings.model_dump(mode="json"))


__all__: list[str] = ["FlextMeltanoAdapter"]
