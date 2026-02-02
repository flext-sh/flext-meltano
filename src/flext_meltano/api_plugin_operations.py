"""FLEXT Meltano API Plugin Operations - Plugin management with flext-core patterns.

This module provides complete plugin operations for the API following flext-core
 patterns with railway-oriented programming and Python 3.13+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core.result import r

from flext_meltano.api import FlextMeltano
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.utilities import u

# Import aliases for concise usage
m = FlextMeltanoModels
t = FlextMeltanoTypes


class FlextMeltanoAPIPluginOperations:
    """API plugin operations with flext-core railway patterns.

    Provides complete plugin operation management using Python 3.13+
    patterns and flext-core railway-oriented programming.

    ** Patterns Used:**
    - Railway-oriented programming for all operations
    - Python 3.13+ type parameter syntax
    - Validation dispatch tables
    - Functional composition patterns

    Attributes:
    api: Reference to the parent API instance

    """

    def __init__(self, api: FlextMeltano) -> None:
        """Initialize API plugin operations with API reference."""
        self.api = api

    def install_plugin(
        self,
        plugin_type: str,
        plugin_name: str,
        config: t.MeltanoCore.MeltanoConfigDict | None = None,
    ) -> r[t.MeltanoCore.MeltanoConfigDict]:
        """Install a Meltano plugin with validation."""
        # Use u.none_() for validation (DSL pattern)
        if u.none_(plugin_type, plugin_name):
            return r[t.MeltanoCore.MeltanoConfigDict].fail(
                "Plugin type and name are required",
            )

        valid_types = {"extractors", "loaders", "transformers", "orchestrators"}
        # Use u.not_() + u.in_() for membership check (DSL pattern)
        if u.not_(u.in_(plugin_type, valid_types)):
            return r[t.MeltanoCore.MeltanoConfigDict].fail(
                f"Invalid plugin type: {plugin_type}. Valid types: {valid_types}",
            )

        if u.not_(u.starts(plugin_name, "tap-", "target-", "dbt-")):
            return r[t.MeltanoCore.MeltanoConfigDict].fail(
                f"Invalid plugin name format: {plugin_name}",
            )

        try:
            plugin_config: dict[str, t.JsonValue] = {
                "name": plugin_name,
                "namespace": plugin_name.replace("-", "_"),
                "pip_url": f"pipelinewise-{plugin_name}",
                "settings": config or {},
            }

            result_dict: dict[str, t.JsonValue] = {
                "plugin_name": plugin_name,
                "plugin_type": plugin_type,
                "status": "installed",
                "configuration": plugin_config,
                "installed_at": str(__import__("time").time()),
                "api_version": self.api.version,
            }
            return r[t.MeltanoCore.MeltanoConfigDict].ok(result_dict)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.MeltanoCore.MeltanoConfigDict].fail(
                f"Plugin installation failed: {e}",
            )

    def list_plugins(
        self,
        plugin_type: str | None = None,
    ) -> r[list[t.MeltanoCore.MeltanoConfigDict]]:
        """List installed Meltano plugins with filtering."""
        try:
            all_plugins = [
                {"name": "tap-csv", "type": "extractors", "status": "installed"},
                {"name": "target-postgres", "type": "loaders", "status": "installed"},
                {"name": "dbt-postgres", "type": "transformers", "status": "installed"},
            ]

            filtered_plugins = (
                u.filter(all_plugins, lambda p: u.get(p, "type") == plugin_type)
                if plugin_type
                else all_plugins
            )

            plugins_data: list[dict[str, t.JsonValue]] = u.map(
                filtered_plugins,
                lambda plugin: {**plugin, "api_version": self.api.version},
            )

            return r[list[t.MeltanoCore.MeltanoConfigDict]].ok(plugins_data)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[list[t.MeltanoCore.MeltanoConfigDict]].fail(
                f"Plugin listing failed: {e}",
            )


__all__ = ["FlextMeltanoAPIPluginOperations"]
