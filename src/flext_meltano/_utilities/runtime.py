"""FLEXT Meltano Utilities - Runtime command normalization helpers."""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from pathlib import Path

from flext_infra import u
from meltano.core.plugin.base import PluginType as MeltanoPluginType
from meltano.core.plugin.project_plugin import ProjectPlugin

from flext_meltano import c, m, p, t


class FlextMeltanoUtilitiesRuntime:
    """Runtime-focused helpers for in-process Meltano execution."""

    @staticmethod
    def coerce_container_mapping(
        value: t.Container | None,
    ) -> Mapping[str, t.Container] | None:
        """Normalize runtime objects to canonical container mappings when possible."""
        if not isinstance(value, Mapping):
            return None
        try:
            return t.Meltano.CONTAINER_MAP_ADAPTER.validate_python(value)
        except c.ValidationError:
            return None

    @staticmethod
    def coerce_container_mapping_list(
        value: t.Container | None,
    ) -> list[Mapping[str, t.Container]] | None:
        """Normalize runtime objects to canonical mapping lists when possible."""
        if not isinstance(value, list):
            return None
        try:
            return t.Meltano.CONTAINER_MAP_LIST_ADAPTER.validate_python(value)
        except c.ValidationError:
            return None

    @staticmethod
    def _normalized_parts(values: t.StrSequence) -> t.StrSequence:
        """Normalize a sequence of CLI-like values to stripped non-empty strings."""
        stripped_values = u.map(
            u.to_str_list(values),
            lambda part: u.to_str(part).strip(),
        )
        return list(
            u.filter(
                stripped_values,
                lambda part: u.chk(part, empty=False),
            ),
        )

    @staticmethod
    def normalize_runtime_command(command: t.StrSequence) -> t.StrSequence:
        """Normalize legacy Meltano command arguments for in-process execution."""
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
        """Normalize public plugin labels to Meltano project plugin groups."""
        if plugin_type is None:
            return None
        normalized = u.normalize(u.to_str(plugin_type), case="lower").strip()
        mapping = {
            "extractor": c.Meltano.PluginType.EXTRACTORS.value,
            c.Meltano.PluginType.EXTRACTORS.value: (
                c.Meltano.PluginType.EXTRACTORS.value
            ),
            c.Meltano.PREFIX_TAP.rstrip("-"): c.Meltano.PluginType.EXTRACTORS.value,
            "loader": c.Meltano.PluginType.LOADERS.value,
            c.Meltano.PluginType.LOADERS.value: (c.Meltano.PluginType.LOADERS.value),
            c.Meltano.PREFIX_TARGET.rstrip("-"): c.Meltano.PluginType.LOADERS.value,
            "transformer": c.Meltano.PluginType.TRANSFORMS.value,
            "transformers": c.Meltano.PluginType.TRANSFORMS.value,
            c.Meltano.PluginType.TRANSFORMS.value: (
                c.Meltano.PluginType.TRANSFORMS.value
            ),
            c.Meltano.PREFIX_DBT.rstrip("-"): c.Meltano.PluginType.TRANSFORMS.value,
        }
        return mapping.get(normalized, normalized)

    @staticmethod
    def is_help_request(args: t.StrSequence) -> bool:
        """Return whether the provided args request CLI help."""
        normalized_args = FlextMeltanoUtilitiesRuntime._normalized_parts(args)
        return not normalized_args or normalized_args[0] in {
            c.Meltano.CMD_HELP_OPTION,
            c.Meltano.CMD_SHORT_HELP_OPTION,
        }

    @staticmethod
    def resolve_project_root(settings: t.ValueOrModel | p.Settings) -> Path | None:
        """Extract and normalize project_root from a settings-like object."""
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
        """Normalize settings environment values to Meltano runtime aliases."""
        normalized = u.normalize(
            u.to_str(environment_name, default=""),
            case="lower",
        ).strip()
        aliases: t.StrMapping = {
            c.Meltano.Environment.DEVELOPMENT.value: "dev",
            c.Meltano.Environment.TESTING.value: "test",
            c.Meltano.Environment.PRODUCTION.value: "prod",
        }
        return aliases.get(normalized, normalized)

    @staticmethod
    def build_pipeline_runtime_command(
        tap_name: str,
        target_name: str,
    ) -> t.StrSequence:
        """Build the canonical Meltano ELT runtime command."""
        return FlextMeltanoUtilitiesRuntime._normalized_parts(
            [c.Meltano.CMD_ELT, tap_name, target_name],
        )

    @staticmethod
    def build_dbt_runtime_command(
        dbt_command: str,
        args: t.StrSequence | None = None,
    ) -> t.StrSequence:
        """Build the canonical Meltano DBT invoke runtime command."""
        command = [
            c.Meltano.CMD_INVOKE,
            f"{c.Meltano.PLUGIN_DBT_DEFAULT_NAME}:{dbt_command}",
        ]
        if args:
            command.extend(FlextMeltanoUtilitiesRuntime._normalized_parts(args))
        return FlextMeltanoUtilitiesRuntime._normalized_parts(command)

    @staticmethod
    def build_bridge_command_args(
        command: str,
        args: t.ConfigurationMapping | None = None,
    ) -> t.StrSequence:
        """Build Meltano bridge command arguments from command + key/value args."""
        command_args = FlextMeltanoUtilitiesRuntime._normalized_parts([command])
        if args is None:
            return command_args
        option_args = [
            f"--{u.to_str(key).strip()}={u.to_str(value)}"
            for key, value in args.items()
            if u.chk(u.to_str(key).strip(), empty=False)
        ]
        return [*command_args, *option_args]

    @staticmethod
    def build_discovered_plugin(
        raw_type: str,
        raw_plugin: Mapping[str, t.Container],
    ) -> t.StrMapping | None:
        """Normalize a Meltano runtime plugin mapping to discovery payload shape."""
        name_val = raw_plugin.get("name", "")
        plugin_name = str(name_val).strip() if name_val is not None else ""
        if not u.chk(plugin_name, empty=False):
            return None
        ns_val = raw_plugin.get("namespace", "")
        pip_val = raw_plugin.get("pip_url", "")
        variant_val = raw_plugin.get("variant", "")
        plugin_data: Mapping[str, t.Container] = {
            "name": plugin_name,
            "type": FlextMeltanoUtilitiesRuntime.normalize_plugin_group(raw_type)
            or u.to_str(raw_type),
            "namespace": str(ns_val).strip() if ns_val is not None else "",
            "pip_url": str(pip_val).strip() if pip_val is not None else "",
            "variant": str(variant_val).strip() if variant_val is not None else "",
        }
        filtered = u.filter(plugin_data, lambda value: u.chk(value, empty=False))
        return {str(key): str(value) for key, value in filtered.items()}

    @staticmethod
    def build_discovered_project_plugin(
        raw_type: str,
        raw_plugin: ProjectPlugin,
    ) -> t.StrMapping | None:
        """Normalize a Meltano project plugin object into discovery payload shape."""
        plugin_mapping: Mapping[str, t.Container] = {
            "name": raw_plugin.name,
            "namespace": raw_plugin.namespace,
            "pip_url": raw_plugin.pip_url,
            "variant": raw_plugin.variant,
        }
        return FlextMeltanoUtilitiesRuntime.build_discovered_plugin(
            raw_type,
            plugin_mapping,
        )

    @staticmethod
    def discover_project_plugins(
        current_plugins: Mapping[MeltanoPluginType, Sequence[ProjectPlugin]],
        *,
        selected_type: str | None = None,
    ) -> list[t.StrMapping]:
        """Normalize Meltano current_plugins catalog into canonical discovery mappings."""
        discovered: list[t.StrMapping] = []
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
    def extract_plugin_names(
        plugins: Sequence[t.StrMapping],
    ) -> t.StrSequence:
        """Extract non-empty plugin names from normalized plugin mappings."""
        return list(
            u.map(
                u.filter(
                    plugins,
                    lambda plugin: u.chk(
                        u.to_str(plugin.get("name", "")).strip(),
                        empty=False,
                    ),
                ),
                lambda plugin: u.to_str(plugin.get("name", "")).strip(),
            ),
        )

    @staticmethod
    def build_plugin_discovery_item(
        plugin_name: str,
        plugin_type: str,
        *,
        default_variant: str = "",
        variants: Mapping[str, t.Container] | None = None,
        description: str = "",
        logo_url: str = "",
    ) -> t.StrMapping:
        """Build canonical plugin discovery payload from raw Meltano metadata."""
        variants_str = u.join(list(variants.keys()), separator=",") if variants else ""
        return m.Meltano.PluginDiscoveryItem.model_validate({
            "name": plugin_name,
            "type": plugin_type,
            "default_variant": default_variant,
            "variants": variants_str,
            "description": description,
            "logo_url": logo_url,
        }).model_dump()

    @staticmethod
    def command_status(
        *,
        success: bool,
        success_status: str,
        failure_status: str,
    ) -> str:
        """Select status string from command success/failure."""
        return success_status if success else failure_status

    @staticmethod
    def build_command_execution_payload(
        command_result: m.Meltano.CommandExecutionResult,
        *,
        extra_fields: Mapping[str, t.Container] | None = None,
        success_status: str = c.Meltano.OperationStatus.SUCCESS,
        failure_status: str = c.Meltano.OperationStatus.ERROR,
        status_field: str | None = "status",
        duration_field: str | None = "execution_time",
    ) -> Mapping[str, t.Container]:
        """Build a standard command payload for services over Meltano runtime."""
        payload: t.MutableRecursiveContainerMapping = {
            "success": command_result.success,
            "output": u.to_str(command_result.output),
            "error": u.to_str(command_result.error),
            "exit_code": command_result.exit_code,
        }
        if status_field is not None:
            payload[status_field] = FlextMeltanoUtilitiesRuntime.command_status(
                success=command_result.success,
                success_status=success_status,
                failure_status=failure_status,
            )
        if duration_field is not None:
            payload[duration_field] = float(command_result.execution_time)
        if extra_fields is None:
            return payload
        merged = u.merge_mappings(payload, extra_fields, strategy="replace")
        if merged.success:
            return merged.value
        return {
            **payload,
            **extra_fields,
        }

    @staticmethod
    def command_failure_message(
        command_result: m.Meltano.CommandExecutionResult,
        *,
        default: str,
    ) -> str:
        """Resolve the best failure/output text from a command result."""
        error_text = u.to_str(command_result.error).strip()
        if u.chk(error_text, empty=False):
            return error_text
        output_text = u.to_str(command_result.output).strip()
        if u.chk(output_text, empty=False):
            return output_text
        return default

    @staticmethod
    def normalize_discovered_plugin_type(plugin_type: str, plugin_name: str) -> str:
        """Normalize Meltano project plugin groups to public discovery labels."""
        normalized = FlextMeltanoUtilitiesRuntime.normalize_plugin_group(plugin_type)
        if normalized == c.Meltano.PluginType.EXTRACTORS.value:
            return c.Meltano.PREFIX_TAP.rstrip("-")
        if normalized == c.Meltano.PluginType.LOADERS.value:
            return c.Meltano.PREFIX_TARGET.rstrip("-")
        if (
            normalized == c.Meltano.PluginType.TRANSFORMS.value
            or plugin_name.startswith(c.Meltano.PREFIX_DBT)
        ):
            return "transformer"
        return normalized or plugin_type
