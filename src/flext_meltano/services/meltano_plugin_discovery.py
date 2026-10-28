"""Plugin discovery operations for the FlextMeltano facade.

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

from collections.abc import Mapping, MutableSequence, Sequence

from flext_meltano import FlextMeltanoServiceBase, c, m, p, r, t, u
from flext_meltano.services import FlextMeltanoAbstractions, FlextMeltanoProjectService


class FlextMeltanoPluginDiscovery(FlextMeltanoServiceBase):
    """Mixin providing plugin discovery and info retrieval."""

    @staticmethod
    def _is_meltano_project(value: t.Meltano.DbtProject | None) -> bool:
        """Type guard for protocol-compatible Meltano project objects.

        Returns:
            The resulting ``bool``.

        """
        if value is None:
            return False
        return "root_dir" in value

    @staticmethod
    def _build_plugin_info(
        plugin_name: str,
        indexed_plugin: Mapping[str, str],
        plugin_type: str,
    ) -> Mapping[str, str]:
        """Build plugin info dict from a plugin definition.

        Returns:
            The resulting ``Mapping[str, str]``.

        """
        source = m.Meltano.PluginDiscoverySource.model_validate(indexed_plugin)
        return u.Meltano.build_plugin_discovery_item(plugin_name, plugin_type, source)

    @staticmethod
    def _extract_plugin_info(
        plugins_data: Mapping[str, Mapping[str, str]],
        plugin_name: str,
        plugin_type: str,
    ) -> p.Result[Mapping[str, str]]:
        """Extract plugin info from plugins dict.

        Returns:
            The resulting ``p.Result[Mapping[str, str]]``.

        """
        plugins_dict = m.Meltano.PluginDiscoveryCatalog.model_validate({
            "plugins": plugins_data,
        }).plugins
        plugin_value = plugins_dict.get(plugin_name)
        if plugin_value is None:
            return r[Mapping[str, str]].fail(
                f"Plugin '{plugin_name}' not found in {plugin_type}",
            )
        plugin_info = u.Meltano.build_plugin_discovery_item(
            plugin_name,
            plugin_type,
            plugin_value,
        )
        return r[Mapping[str, str]].ok(plugin_info)

    def discover_plugins(
        self,
        project: t.JsonPayload | t.Meltano.DbtProject | None = None,
    ) -> p.Result[Sequence[Mapping[str, str]]]:
        """Discover plugins from Meltano Hub using native API.

        Returns:
            The resulting ``p.Result[Sequence[Mapping[str, str]]]``.

        """
        try:
            return self._discover_plugins(project)
        except c.EXC_ATTR_KEY_OS_TYPE_VALUE as e:
            error_msg = f"Failed to discover plugins: {e}"
            self.logger.exception(error_msg, error=str(e))
            return r[Sequence[Mapping[str, str]]].fail(error_msg)

    def _discover_plugins(
        self,
        project: t.JsonPayload | t.Meltano.DbtProject | None,
    ) -> p.Result[Sequence[Mapping[str, str]]]:
        """Discover plugins without owning the exception boundary.

        Returns:
            The resulting ``p.Result[Sequence[Mapping[str, str]]]``.

        """
        self.logger.info("Discovering Meltano plugins")
        working_project: t.JsonPayload | t.Meltano.DbtProject
        if project:
            working_project = project
        else:
            temp_project_result = (
                FlextMeltanoProjectService().create_temporary_project()
            )
            if temp_project_result.failure:
                return r[Sequence[Mapping[str, str]]].from_failure(temp_project_result)
            temp_project = temp_project_result.value
            if not self._is_meltano_project(temp_project):
                return r[Sequence[Mapping[str, str]]].fail(
                    "Temporary project does not satisfy Project",
                )
            working_project = temp_project
        plugins: MutableSequence[Mapping[str, str]] = []
        abstractions = FlextMeltanoAbstractions()
        extractors_result = abstractions.fetch_plugins_of_type(
            working_project,
            c.Meltano.PluginType.EXTRACTORS.value,
        )
        max_extractors = 10
        max_loaders = 5
        if extractors_result.success:
            for idx, (k, v) in enumerate(extractors_result.value.items()):
                if idx >= max_extractors:
                    break
                plugins.append(self._build_plugin_info(k, v, "extractor"))
        loaders_result = abstractions.fetch_plugins_of_type(
            working_project,
            c.Meltano.PluginType.LOADERS.value,
        )
        if loaders_result.success:
            for idx, (k, v) in enumerate(loaders_result.value.items()):
                if idx >= max_loaders:
                    break
                plugins.append(self._build_plugin_info(k, v, "loader"))
        self.logger.info("Discovered plugins", count=u.count(plugins))
        return r[Sequence[Mapping[str, str]]].ok(plugins)

    def fetch_plugin_info(
        self,
        plugin_name: str,
        plugin_type: str,
    ) -> p.Result[Mapping[str, str]]:
        """Get detailed information about specific plugin.

        Returns:
            The resulting ``p.Result[Mapping[str, str]]``.

        """

        def _run_fetch_plugin_info() -> p.Result[Mapping[str, str]]:
            temp_project_result = FlextMeltanoProjectService().create_temporary_project(
                project_id="temp-info-project",
                prefix="flext_plugin_info_",
            )
            if temp_project_result.failure:
                return r[Mapping[str, str]].from_failure(temp_project_result)
            temp_project = temp_project_result.value
            if not self._is_meltano_project(temp_project):
                return r[Mapping[str, str]].fail(
                    "Temporary project does not satisfy Project",
                )
            abstractions = FlextMeltanoAbstractions()
            plugins_result = abstractions.fetch_plugins_of_type(
                temp_project,
                plugin_type,
            )
            if plugins_result.failure:
                return r[Mapping[str, str]].from_failure(plugins_result)
            return self._extract_plugin_info(
                plugins_result.value,
                plugin_name,
                plugin_type,
            )

        try:
            return _run_fetch_plugin_info()
        except c.EXC_ATTR_KEY_OS_TYPE_VALUE as e:
            error_msg = f"Failed to get plugin info: {e}"
            self.logger.exception(error_msg)
            return r[Mapping[str, str]].fail(error_msg)


__all__: list[str] = ["FlextMeltanoPluginDiscovery"]
