"""Plugin discovery operations for FlextMeltanoComponentService.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableSequence, Sequence
from datetime import datetime

from flext_meltano import (
    FlextMeltanoAbstractions,
    FlextMeltanoProjectService,
    FlextMeltanoServiceBase,
    m,
    r,
    t,
    u,
)


class FlextMeltanoPluginDiscoveryMixin(FlextMeltanoServiceBase):
    """Mixin providing plugin discovery and info retrieval."""

    def discover_plugins(
        self,
        project: FlextMeltanoProjectService | None = None,
    ) -> r[Sequence[t.StrMapping]]:
        """Discover plugins from Meltano Hub using native API."""
        try:
            self.logger.info("Discovering Meltano plugins")
            working_project: FlextMeltanoProjectService | t.Meltano.Dbt.Project
            if project:
                working_project = project
            else:
                temp_project_result = (
                    FlextMeltanoProjectService().create_temporary_project()
                )
                if temp_project_result.is_failure:
                    return r[Sequence[t.StrMapping]].fail(
                        temp_project_result.error
                        or "Failed to create temporary project",
                    )
                temp_project = temp_project_result.value
                if not _is_meltano_project(temp_project):
                    return r[Sequence[t.StrMapping]].fail(
                        "Temporary project does not satisfy Project",
                    )
                working_project = temp_project
            plugins: MutableSequence[t.StrMapping] = []
            abstractions: FlextMeltanoAbstractions = FlextMeltanoAbstractions()
            extractors_result: r[Mapping[str, t.Meltano.PluginDefinition]] = (
                abstractions.get_plugins_of_type(working_project, "extractors")
            )
            max_extractors = 10
            max_loaders = 5
            if extractors_result.is_success:
                for idx, (k, v) in enumerate(extractors_result.value.items()):
                    if idx >= max_extractors:
                        break
                    plugins.append(_build_plugin_info(k, v, "extractor"))
            loaders_result: r[Mapping[str, t.Meltano.PluginDefinition]] = (
                abstractions.get_plugins_of_type(working_project, "loaders")
            )
            if loaders_result.is_success:
                for idx, (k, v) in enumerate(loaders_result.value.items()):
                    if idx >= max_loaders:
                        break
                    plugins.append(_build_plugin_info(k, v, "loader"))
            self.logger.info(f"Discovered {u.count(plugins)} plugins")
            return r[Sequence[t.StrMapping]].ok(plugins)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to discover plugins: {e}"
            self.logger.exception(error_msg, error=str(e))
            return r[Sequence[t.StrMapping]].fail(error_msg)

    def get_plugin_info(self, plugin_name: str, plugin_type: str) -> r[t.StrMapping]:
        """Get detailed information about specific plugin."""
        try:
            temp_project_result = FlextMeltanoProjectService().create_temporary_project(
                project_id="temp-info-project",
                prefix="flext_plugin_info_",
            )
            if temp_project_result.is_failure:
                return r[t.StrMapping].fail(
                    temp_project_result.error or "Failed to create temporary project",
                )
            temp_project = temp_project_result.value
            if not _is_meltano_project(temp_project):
                return r[t.StrMapping].fail(
                    "Temporary project does not satisfy Project"
                )
            abstractions: FlextMeltanoAbstractions = FlextMeltanoAbstractions()
            plugins_result: r[Mapping[str, t.Meltano.PluginDefinition]] = (
                abstractions.get_plugins_of_type(temp_project, plugin_type)
            )
            if plugins_result.is_failure:
                return r[t.StrMapping].fail(
                    plugins_result.error or "Failed to get plugins"
                )
            return _extract_plugin_info(plugins_result.value, plugin_name, plugin_type)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to get plugin info: {e}"
            self.logger.exception(error_msg)
            return r[t.StrMapping].fail(error_msg)


def _is_meltano_project(value: Mapping[str, t.NormalizedValue] | None) -> bool:
    """Type guard for protocol-compatible Meltano project objects."""
    return hasattr(value, "root_dir") and callable(getattr(value, "find_plugins", None))


def _build_plugin_info(
    plugin_name: str,
    indexed_plugin: t.Meltano.PluginDefinition,
    plugin_type: str,
) -> t.StrMapping:
    """Build plugin info dict from a plugin definition."""
    source = m.Meltano.PluginDiscoverySource.model_validate(indexed_plugin)
    return u.Meltano.build_plugin_discovery_item(
        plugin_name,
        plugin_type,
        default_variant=source.default_variant,
        variants=source.variants,
        description=source.description,
        logo_url=source.logo_url,
    )


def _extract_plugin_info(
    plugins_data: Mapping[
        str,
        Mapping[
            str,
            Mapping[str, bool | datetime | float | int | str | None]
            | t.StrSequence
            | str,
        ],
    ],
    plugin_name: str,
    plugin_type: str,
) -> r[t.StrMapping]:
    """Extract plugin info from plugins dict."""
    plugins_dict = m.Meltano.PluginDiscoveryCatalog.model_validate({
        "plugins": plugins_data,
    }).plugins
    plugin_value = plugins_dict.get(plugin_name)
    if plugin_value is None:
        return r[t.StrMapping].fail(
            f"Plugin '{plugin_name}' not found in {plugin_type}"
        )
    plugin_info = u.Meltano.build_plugin_discovery_item(
        plugin_name,
        plugin_type,
        default_variant=plugin_value.default_variant,
        variants=plugin_value.variants,
        description=plugin_value.description,
        logo_url=plugin_value.logo_url,
    )
    return r[t.StrMapping].ok(plugin_info)


__all__ = ["FlextMeltanoPluginDiscoveryMixin"]
