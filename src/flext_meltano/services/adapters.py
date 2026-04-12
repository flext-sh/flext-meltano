"""FLEXT Meltano Adapters - SOLID-compliant adapter classes following FLEXT patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import override

from flext_core import FlextSettings, r
from flext_meltano.base import FlextMeltanoServiceBase
from flext_meltano.constants import FlextMeltanoConstants as c
from flext_meltano.services._executor_base import FlextMeltanoExecutorBase
from flext_meltano.settings import FlextMeltanoSettings
from flext_meltano.typings import FlextMeltanoTypes as t


class FlextMeltanoAdapter(FlextMeltanoServiceBase):
    """Base adapter namespace class for focused integrations."""

    class ProjectAdapter(FlextMeltanoServiceBase):
        """Focused adapter for Meltano project management following SOLID principles."""

        @classmethod
        @override
        def _get_service_config_type(cls) -> type[FlextSettings]:
            return FlextMeltanoSettings

        def create_project(
            self,
            project_name: str,
            project_dir: Path,
        ) -> r[t.ContainerMapping]:
            """Create a new Meltano project via the imported library."""
            project_path = Path(project_dir) / project_name
            init_result = FlextMeltanoExecutorBase.initialize_project_root(
                project_path,
            )
            if init_result.failure:
                return r[t.ContainerMapping].fail(
                    init_result.error or "Project creation failed",
                )
            result: t.ContainerMapping = {
                "status": c.Meltano.OperationStatus.CREATED,
                "project_name": project_name,
                "project_path": str(project_path),
                "output": f"Initialized {c.Meltano.PATH_MELTANO_PROJECT_FILE}",
                "error": "",
                "created_at": str(time.time()),
            }
            return r[t.ContainerMapping].ok(result)

        @override
        def execute(self) -> r[t.ContainerMapping]:
            """Execute default project operation."""
            return self.get_version()

        def get_version(self) -> r[t.ContainerMapping]:
            """Get Meltano version information using native API."""
            version_result = FlextMeltanoExecutorBase.get_version()
            if version_result.failure:
                return r[t.ContainerMapping].fail(
                    version_result.error or "Failed to get Meltano version",
                )
            meltano_version = version_result.value
            version_info: t.ContainerMapping = {
                "version": meltano_version,
                "meltano": meltano_version,
                "cli_type": "native_meltano_api",
                "integration": "flext-core",
            }
            return r[t.ContainerMapping].ok(version_info)

        def initialize_project(self, project_root: Path) -> r[t.ContainerMapping]:
            """Initialize Meltano project using railway pattern."""
            return self.create_project(
                project_name=project_root.name,
                project_dir=project_root.parent,
            )

    class PluginAdapter(FlextMeltanoServiceBase):
        """Focused adapter for Meltano plugin management following SOLID principles."""

        @classmethod
        @override
        def _get_service_config_type(cls) -> type[FlextSettings]:
            return FlextMeltanoSettings

        def discover_plugins(
            self,
            plugin_type: str | None = None,
        ) -> r[t.ContainerMapping]:
            """Discover available plugins via Meltano project runtime."""
            try:
                executor = FlextMeltanoExecutorBase()
                plugins_result = executor.get_project_plugins(
                    plugin_type=plugin_type,
                    _cwd=self.settings.project_root,
                )
                if plugins_result.failure:
                    return r[t.ContainerMapping].fail(
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
                        "type": plugin_group,
                    })
                return r[t.ContainerMapping].ok({"plugins": plugins})
            except c.Meltano.OPERATION_ERRORS as ex:
                return r[t.ContainerMapping].fail(f"Plugin discovery failed: {ex}")

        @override
        def execute(self) -> r[t.ContainerMapping]:
            """Execute default plugin operation."""
            return self.discover_plugins()

    @override
    def execute(self) -> r[t.ContainerMapping]:
        """Execute adapter service returning current settings."""
        return r[t.ContainerMapping].ok(self.settings.model_dump())


__all__: list[str] = ["FlextMeltanoAdapter"]
