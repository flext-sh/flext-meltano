"""FLEXT Meltano Utilities - Runtime command normalization helpers.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from flext_cli import u

from flext_meltano import c, m, t

if TYPE_CHECKING:
    from meltano.core.plugin.base import PluginType as MeltanoPluginType
    from meltano.core.plugin.project_plugin import ProjectPlugin

    from flext_meltano import p


class FlextMeltanoUtilitiesRuntime:
    """Runtime-focused helpers for in-process Meltano execution."""

    @staticmethod
    def _normalized_parts(values: Sequence[str]) -> Sequence[str]:
        """Normalize a sequence of CLI-like values to stripped non-empty strings.

        Returns:
            The resulting ``Sequence[str]``.

        """

        def _strip_part(part: str) -> str:
            return u.to_str(part).strip()

        def _is_non_empty_part(part: str) -> bool:
            return u.string_non_empty(part)

        stripped_values = u.map(u.to_str_list(values), _strip_part)
        return list(u.filter(stripped_values, _is_non_empty_part))

    @staticmethod
    def normalize_runtime_command(command: Sequence[str]) -> Sequence[str]:
        """Normalize legacy Meltano command arguments for in-process execution.

        Returns:
            The resulting ``Sequence[str]``.

        """
        normalized = FlextMeltanoUtilitiesRuntime._normalized_parts(command)
        if normalized and normalized[0] == c.Meltano.CMD_BINARY:
            normalized = normalized[1:]
        if not normalized:
            return normalized
        match normalized[0]:
            case c.Meltano.ExecutorCommand.VERSION:
                return [c.Meltano.CMD_VERSION_OPTION, *normalized[1:]]
            case c.Meltano.ExecutorCommand.HELP:
                return [c.Meltano.CMD_HELP_OPTION, *normalized[1:]]
            case _:
                return normalized

    @staticmethod
    def normalize_plugin_group(plugin_type: str | None) -> str | None:
        """Normalize public plugin labels to Meltano project plugin groups.

        Returns:
            The resulting ``str | None``.

        """
        if plugin_type is None:
            return None
        normalized = u.normalize(u.to_str(plugin_type), case="lower").strip()
        resolved = c.Meltano.PLUGIN_GROUP_ALIASES.get(normalized)
        return resolved.value if resolved is not None else normalized

    @staticmethod
    def requests_help(args: Sequence[str]) -> bool:
        """Return whether the provided args request CLI help."""
        normalized_args = FlextMeltanoUtilitiesRuntime._normalized_parts(args)
        return not normalized_args or normalized_args[0] in {
            c.Meltano.CMD_HELP_OPTION,
            c.Meltano.CMD_SHORT_HELP_OPTION,
        }

    @staticmethod
    def resolve_project_root(settings: t.JsonPayload | p.Settings) -> Path | None:
        """Extract and normalize project_root from a settings-like object.

        Returns:
            The resulting ``Path | None``.

        """
        if isinstance(settings, Mapping):
            raw = settings.get("project_root")
        elif isinstance(settings, m.BaseModel):
            model_data = settings.model_dump()
            raw = model_data.get("project_root")
        elif isinstance(settings, (Path, str)):
            raw = settings
        else:
            raw = None
        if raw is None or raw == Path():
            return None
        if isinstance(raw, Path):
            return raw
        if isinstance(raw, str) and raw:
            return m.Meltano.PathPayload(value=Path(raw)).value
        return None

    @staticmethod
    def normalize_environment_name(environment_name: str | None) -> str:
        """Normalize settings environment values to Meltano runtime aliases.

        Returns:
            The resulting ``str``.

        """
        raw_environment_name = "" if environment_name is None else environment_name
        normalized = u.normalize(
            u.to_str(raw_environment_name, default=""),
            case="lower",
        ).strip()
        runtime_alias = c.Meltano.ENVIRONMENT_RUNTIME_ALIASES.get(normalized)
        return runtime_alias if runtime_alias is not None else normalized

    @staticmethod
    def build_dbt_runtime_command(
        dbt_command: str,
        args: Sequence[str] | None = None,
    ) -> Sequence[str]:
        """Build the canonical Meltano DBT invoke runtime command.

        Returns:
            The resulting ``Sequence[str]``.

        """
        command = [
            c.Meltano.CMD_INVOKE,
            f"{c.Meltano.PLUGIN_DBT_DEFAULT_NAME}:{dbt_command}",
        ]
        if args:
            command.extend(FlextMeltanoUtilitiesRuntime._normalized_parts(args))
        return FlextMeltanoUtilitiesRuntime._normalized_parts(command)

    @staticmethod
    def build_discovered_project_plugin(
        raw_type: str,
        raw_plugin: ProjectPlugin,
    ) -> Mapping[str, str] | None:
        """Normalize a Meltano project plugin object into discovery payload shape.

        Returns:
            The resulting ``Mapping[str, str] | None``.

        """
        raw_mapping: t.JsonMapping = {
            "name": raw_plugin.name,
            "namespace": raw_plugin.namespace,
            "pip_url": raw_plugin.pip_url,
            "variant": raw_plugin.variant,
        }
        name_val = raw_mapping.get("name", "")
        plugin_name = str(name_val).strip() if name_val is not None else ""
        if not u.string_non_empty(plugin_name):
            return None
        ns_val = raw_mapping.get("namespace", "")
        pip_val = raw_mapping.get("pip_url", "")
        variant_val = raw_mapping.get("variant", "")
        plugin_data: t.JsonMapping = {
            "name": plugin_name,
            "type": FlextMeltanoUtilitiesRuntime.normalize_plugin_group(raw_type)
            or u.to_str(raw_type),
            "namespace": str(ns_val).strip() if ns_val is not None else "",
            "pip_url": str(pip_val).strip() if pip_val is not None else "",
            "variant": str(variant_val).strip() if variant_val is not None else "",
        }
        return {
            key: value
            for key, value in plugin_data.items()
            if u.string_non_empty(value)
        }

    @staticmethod
    def discover_project_plugins(
        current_plugins: Mapping[MeltanoPluginType, Sequence[ProjectPlugin]],
        *,
        selected_type: str | None = None,
    ) -> list[Mapping[str, str]]:
        """Normalize Meltano current_plugins catalog into canonical discovery mappings.

        Returns:
            The resulting ``list[Mapping[str, str]]``.

        """
        discovered: list[Mapping[str, str]] = []
        for raw_type, raw_plugins in current_plugins.items():
            normalized_type = raw_type.value
            for raw_plugin in raw_plugins:
                plugin_data = (
                    FlextMeltanoUtilitiesRuntime.build_discovered_project_plugin(
                        normalized_type,
                        raw_plugin,
                    )
                )
                if plugin_data is None:
                    continue
                if selected_type is not None and plugin_data["type"] != selected_type:
                    continue
                discovered.append(plugin_data)
        return discovered

    @staticmethod
    def build_plugin_discovery_item(
        plugin_name: str,
        plugin_type: str,
        source: m.Meltano.PluginDiscoverySource,
    ) -> Mapping[str, str]:
        """Build canonical plugin discovery payload from raw Meltano metadata.

        ``source`` carries the plugin's own normalized discovery metadata
        (default variant, variants, description, logo URL) as one cohesive
        domain object instead of four independent keyword arguments.

        Returns:
            The resulting ``Mapping[str, str]``.

        """
        variants_str = (
            u.join(list(source.variants.keys()), separator=",")
            if source.variants
            else ""
        )
        item = m.Meltano.PluginDiscoveryItem.model_validate({
            "name": plugin_name,
            "type": plugin_type,
            "default_variant": source.default_variant,
            "variants": variants_str,
            "description": source.description,
            "logo_url": source.logo_url,
        })
        return {
            "name": item.name,
            "type": item.type,
            "default_variant": item.default_variant,
            "variants": item.variants,
            "description": item.description,
            "logo_url": item.logo_url,
        }


__all__: list[str] = ["FlextMeltanoUtilitiesRuntime"]
