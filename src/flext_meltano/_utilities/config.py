"""FLEXT Meltano Utilities - Configuration dictionary builders."""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from pathlib import Path

from flext_cli import FlextCliUtilities, r

from flext_meltano import c, m, t


class FlextMeltanoUtilitiesConfig:
    """Configuration creation, normalization, and plugin catalog utilities."""

    @classmethod
    def create_meltano_config_dict(
        cls,
        project_id: str,
        project_name: str = "",
        version: str | None = None,
        default_environment: str | None = None,
        plugins: t.Meltano.MeltanoConfigDict | None = None,
        environments: t.Meltano.MeltanoConfigDict | None = None,
    ) -> r[t.Meltano.MeltanoConfigDict]:
        """Create MELTANO-SPECIFIC configuration dictionary - DOMAIN-SPECIFIC ONLY."""
        try:
            raw_config: t.Meltano.MeltanoConfigDict = {
                "project_id": project_id,
                "project_name": project_name or project_id,
                "version": version or 1,
                "default_environment": default_environment,
                "environments": environments,
                "plugins": plugins,
            }
            default_envs: Sequence[t.StrMapping] = [
                {"name": env} for env in c.Meltano.Metadata.DEFAULT_ENVIRONMENTS
            ]
            project_id_val = str(raw_config.get("project_id", ""))
            project_name_val = str(
                raw_config.get("project_name") or raw_config.get("project_id") or "",
            )
            cfg = FlextCliUtilities.build(
                raw_config,
                ops={"transform": {"normalize": False, "strip_none": False}},
            )
            cfg_dict = m.Meltano.ConfigMappingPayload.model_validate({
                "values": cfg,
            }).values
            plugins_val = cfg_dict.get("plugins")
            plugins_dict: t.Meltano.MeltanoConfigDict = {}
            if isinstance(plugins_val, dict):
                plugins_dict = {str(k): v for k, v in plugins_val.items()}
            result_cfg = {
                "version": cfg_dict.get("version", 1),
                "project_id": FlextCliUtilities.safe_string(project_id_val),
                "project_name": FlextCliUtilities.safe_string(project_name_val),
                "environments": cfg_dict.get("environments") or default_envs,
                "plugins": plugins_dict,
                "metadata": {
                    "created_by": c.Meltano.Metadata.CREATED_BY,
                    "created_at": FlextCliUtilities.generate_iso_timestamp(),
                    "flext_version": c.Meltano.FLEXT_MELTANO_VERSION,
                },
            }
            default_env_val = cfg_dict.get("default_environment")
            if default_env_val is not None:
                result_cfg["default_environment"] = default_env_val
            elif not project_name:
                result_cfg["default_environment"] = (
                    c.Meltano.Metadata.DEFAULT_ENVIRONMENTS[0]
                )
            normalized_values = m.Meltano.ConfigMappingPayload.model_validate({
                "values": result_cfg,
            }).values
            normalized_cfg: t.MutableContainerMapping = {}
            for key, value in normalized_values.items():
                if value is None:
                    continue
                if isinstance(value, Mapping):
                    normalized_cfg[str(key)] = {
                        str(map_key): map_value
                        for map_key, map_value in value.items()
                        if map_value is not None
                    }
                elif isinstance(value, list):
                    normalized_cfg[str(key)] = [
                        item for item in value if item is not None
                    ]
                else:
                    normalized_cfg[str(key)] = value
            return r[t.Meltano.MeltanoConfigDict].ok(normalized_cfg)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as err:
            return r[t.Meltano.MeltanoConfigDict].fail(
                f"Failed to create Meltano config dict: {err}",
            )

    @classmethod
    def create_plugin_config_dict(
        cls,
        name: str,
        plugin_type: str = "extractor",
        namespace: str = "",
        pip_url: str = "",
        executable: str = "",
    ) -> r[t.Meltano.PluginConfigDict]:
        """Create MELTANO-SPECIFIC plugin config using DSL builder pattern."""
        safe = FlextCliUtilities.safe_string
        result: t.Meltano.PluginConfigDict = {
            "name": safe(name),
            "namespace": safe(namespace),
            "pip_url": safe(pip_url),
            "executable": safe(executable),
            "type": plugin_type or "extractor",
            "settings": dict[str, t.ContainerValue](),
            "config": dict[str, t.ContainerValue](),
            "metadata": {
                "created_by": c.Meltano.Metadata.CREATED_BY,
                "created_at": FlextCliUtilities.generate_iso_timestamp(),
            },
        }
        return r[t.Meltano.PluginConfigDict].ok(result)

    @classmethod
    def default_catalog(cls) -> Sequence[t.Meltano.PluginDefinition]:
        """Provide default plugin catalog entries for discovery workflows."""
        return [
            {
                "type": plugin_type.value,
                "variant": c.Meltano.Plugin.DEFAULT_VARIANT,
                "registry": c.Meltano.Plugin.HUB_URL,
                "identifiers": [plugin_type.value],
            }
            for plugin_type in c.Meltano.Enums.PluginType.__members__.values()
        ]

    @classmethod
    def get_all_plugins(cls) -> Sequence[t.Meltano.PluginDefinition]:
        """Compatibility shim for existing discovery logic."""
        return cls.default_catalog()

    @classmethod
    def normalize_container_value(cls, value: t.NormalizedValue) -> t.NormalizedValue:
        """Recursively normalize a value, converting Paths to strings and dropping None."""
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, t.SCALAR_TYPES):
            return value
        if isinstance(value, (list, tuple)):
            return [cls.normalize_container_value(i) for i in value if i is not None]
        if isinstance(value, Mapping):
            return {
                str(k): cls.normalize_container_value(v)
                for k, v in value.items()
                if v is not None
            }
        return str(value)

    @classmethod
    def normalize_config(
        cls,
        value: t.Meltano.MeltanoConfigDict | t.ContainerMapping | None,
    ) -> t.Meltano.MeltanoConfigDict:
        """Normalize a config mapping, recursively converting values and dropping None."""
        if value is None:
            empty: t.Meltano.MeltanoConfigDict = {}
            return empty
        return {
            str(k): cls.normalize_container_value(v)
            for k, v in value.items()
            if v is not None
        }

    @staticmethod
    def supported_types() -> t.StrSequence:
        """Return the supported plugin type identifiers."""
        return [
            plugin_type.value
            for plugin_type in c.Meltano.Enums.PluginType.__members__.values()
        ]

    @staticmethod
    def is_process_running(pid: int) -> bool:
        """Check if a process with the given PID is running."""
        if pid <= 0:
            return False
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        except OSError:
            return False
        return True
