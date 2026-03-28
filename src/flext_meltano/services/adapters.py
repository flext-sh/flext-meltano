"""FLEXT Meltano Adapters - SOLID-compliant adapter classes following FLEXT patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import subprocess
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import override

import meltano
from flext_core import FlextSettings, r, s

from flext_meltano import FlextMeltanoServiceBase, FlextMeltanoSettings, c, t


class FlextMeltanoAdapter(FlextMeltanoServiceBase):
    """Base adapter namespace class for focused integrations."""

    class ProjectAdapter(s[t.Meltano.ExecutionResultDict]):
        """Focused adapter for Meltano project management following SOLID principles."""

        @classmethod
        @override
        def _get_service_config_type(cls) -> type[FlextSettings]:
            """Return FlextMeltanoSettings for this service."""
            return FlextMeltanoSettings

        def create_project(
            self,
            project_name: str,
            project_dir: Path,
        ) -> r[t.Meltano.ExecutionResultDict]:
            """Create new Meltano project via CLI."""
            try:
                project_path = Path(project_dir) / project_name
                proc = subprocess.run(
                    ["meltano", "init", project_name],  # noqa: S607
                    capture_output=True,
                    text=True,
                    cwd=str(project_dir),
                    timeout=60,
                    check=False,
                )
                result: t.Meltano.ExecutionResultDict = {
                    "project_name": project_name,
                    "project_path": str(project_path),
                    "status": (
                        c.Meltano.Enums.OperationStatus.CREATED
                        if proc.returncode == 0
                        else c.Meltano.Enums.OperationStatus.ERROR
                    ),
                    "output": proc.stdout,
                    "error": proc.stderr,
                    "created_at": str(time.time()),
                }
                return r[t.Meltano.ExecutionResultDict].ok(result)
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                subprocess.TimeoutExpired,
            ) as ex:
                return r[t.Meltano.ExecutionResultDict].fail(
                    f"Project creation failed: {ex}",
                )

        @override
        def execute(self) -> r[t.Meltano.ExecutionResultDict]:
            """Execute default project operation."""
            return self.get_version()

        def get_version(self) -> r[t.Meltano.ExecutionResultDict]:
            """Get Meltano version information using native API."""
            meltano_version = getattr(meltano, "__version__", "unknown")
            version_info: t.Meltano.ExecutionResultDict = {
                "version": meltano_version,
                "meltano": meltano_version,
                "cli_type": "native_meltano_api",
                "integration": "flext-core",
            }
            return r[t.Meltano.ExecutionResultDict].ok(version_info)

        def initialize_project(
            self,
            project_root: Path,
        ) -> r[t.Meltano.ExecutionResultDict]:
            """Initialize Meltano project using railway pattern for composable steps."""
            return self.create_project(
                project_name=project_root.name,
                project_dir=project_root,
            )

    class PluginAdapter(s[Sequence[t.Meltano.PluginDefinition]]):
        """Focused adapter for Meltano plugin management following SOLID principles."""

        @classmethod
        @override
        def _get_service_config_type(cls) -> type[FlextSettings]:
            """Return FlextMeltanoSettings for this service."""
            return FlextMeltanoSettings

        def discover_plugins(
            self,
            plugin_type: str | None = None,
        ) -> r[Sequence[t.Meltano.PluginDefinition]]:
            """Discover available plugins via Meltano CLI."""
            try:
                proc = subprocess.run(
                    ["meltano", "list"],  # noqa: S607
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                if proc.returncode != 0:
                    return r[Sequence[t.Meltano.PluginDefinition]].fail(
                        f"meltano list failed: {proc.stderr}",
                    )
                plugins: list[t.Meltano.PluginDefinition] = []
                for line in proc.stdout.splitlines():
                    stripped = line.strip()
                    if not stripped:
                        continue
                    ptype = (
                        "tap"
                        if stripped.startswith("tap-")
                        else "target"
                        if stripped.startswith("target-")
                        else "transformer"
                        if stripped.startswith("dbt-")
                        else "other"
                    )
                    plugins.append({"name": stripped, "type": ptype})
                if plugin_type:
                    plugins = [
                        plugin
                        for plugin in plugins
                        if plugin.get("type") == plugin_type
                    ]
                return r[Sequence[t.Meltano.PluginDefinition]].ok(plugins)
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                subprocess.TimeoutExpired,
            ) as ex:
                return r[Sequence[t.Meltano.PluginDefinition]].fail(
                    f"Plugin discovery failed: {ex}",
                )

        @override
        def execute(self) -> r[Sequence[t.Meltano.PluginDefinition]]:
            """Execute default plugin operation."""
            return self.discover_plugins()

    class PipelineAdapter(s[t.Meltano.ExecutionResultDict]):
        """Focused adapter for Meltano pipeline execution following SOLID principles."""

        @classmethod
        @override
        def _get_service_config_type(cls) -> type[FlextSettings]:
            """Return FlextMeltanoSettings for this service."""
            return FlextMeltanoSettings

        @override
        def execute(self) -> r[t.Meltano.ExecutionResultDict]:
            """Execute default pipeline operation."""
            return r[t.Meltano.ExecutionResultDict].ok({
                "status": c.Meltano.Enums.OperationStatus.READY,
            })

        def execute_pipeline(
            self,
            tap_name: str,
            target_name: str,
        ) -> r[t.Meltano.ExecutionResultDict]:
            """Execute ELT pipeline using Meltano CLI."""
            try:
                if not tap_name.startswith("tap-"):
                    return r[t.Meltano.ExecutionResultDict].fail(
                        f"Invalid tap name format: {tap_name}",
                    )
                if not target_name.startswith("target-"):
                    return r[t.Meltano.ExecutionResultDict].fail(
                        f"Invalid target name format: {target_name}",
                    )
                start = time.monotonic()
                proc = subprocess.run(
                    ["meltano", "elt", tap_name, target_name],  # noqa: S607
                    capture_output=True,
                    text=True,
                    timeout=300,
                    check=False,
                )
                duration = time.monotonic() - start
                execution_result: t.Meltano.ExecutionResultDict = {
                    "tap": tap_name,
                    "target": target_name,
                    "status": (
                        c.Meltano.Enums.StreamStatus.COMPLETED
                        if proc.returncode == 0
                        else c.Meltano.Enums.StreamStatus.FAILED
                    ),
                    "success": proc.returncode == 0,
                    "output": proc.stdout,
                    "error": proc.stderr,
                    "execution_duration": duration,
                }
                return r[t.Meltano.ExecutionResultDict].ok(execution_result)
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                subprocess.TimeoutExpired,
            ) as ex:
                return r[t.Meltano.ExecutionResultDict].fail(
                    f"Pipeline execution failed: {ex}",
                )

    class DbtAdapter(s[t.Meltano.DbtResultDict]):
        """Focused adapter for DBT operations following SOLID principles."""

        @override
        @classmethod
        def _get_service_config_type(cls) -> type[FlextSettings]:
            """Return FlextMeltanoSettings for this service."""
            return FlextMeltanoSettings

        @override
        def execute(self) -> r[t.Meltano.DbtResultDict]:
            """Execute default DBT operation."""
            return self.execute_dbt_operation()

        def execute_dbt_operation(self) -> r[t.Meltano.DbtResultDict]:
            """Execute DBT operation via Meltano invoke."""
            try:
                start = time.monotonic()
                proc = subprocess.run(
                    ["meltano", "invoke", "dbt-postgres:run"],  # noqa: S607
                    capture_output=True,
                    text=True,
                    timeout=600,
                    check=False,
                )
                duration = time.monotonic() - start
                dbt_result: t.Meltano.DbtResultDict = {
                    "status": (
                        c.Meltano.Enums.StreamStatus.COMPLETED
                        if proc.returncode == 0
                        else c.Meltano.Enums.StreamStatus.FAILED
                    ),
                    "success": proc.returncode == 0,
                    "output": proc.stdout,
                    "error": proc.stderr,
                    "execution_time": duration,
                }
                return r[t.Meltano.DbtResultDict].ok(dbt_result)
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                subprocess.TimeoutExpired,
            ) as ex:
                return r[t.Meltano.DbtResultDict].fail(f"DBT operation failed: {ex}")

    @override
    def execute(self) -> r[Mapping[str, t.NormalizedValue]]:
        """Execute adapter service returning current settings."""
        return r[Mapping[str, t.NormalizedValue]].ok(self.settings.model_dump())


__all__ = ["FlextMeltanoAdapter"]
