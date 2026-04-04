"""FLEXT Meltano Utilities - Runtime command normalization helpers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

from pydantic import BaseModel

from flext_core import u
from flext_meltano import c, m, p, t


class FlextMeltanoUtilitiesRuntime:
    """Runtime-focused helpers for in-process Meltano execution."""

    @staticmethod
    def _normalized_parts(values: t.StrSequence) -> list[str]:
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
    def normalize_runtime_command(command: t.StrSequence) -> list[str]:
        """Normalize legacy Meltano command arguments for in-process execution."""
        normalized = FlextMeltanoUtilitiesRuntime._normalized_parts(command)
        if normalized and normalized[0] == c.Meltano.Commands.BINARY:
            normalized = normalized[1:]
        if not normalized:
            return normalized
        match normalized[0]:
            case c.Meltano.Enums.ExecutorCommand.VERSION:
                return [c.Meltano.Commands.VERSION_OPTION, *normalized[1:]]
            case c.Meltano.Enums.ExecutorCommand.HELP:
                return [c.Meltano.Commands.HELP_OPTION, *normalized[1:]]
            case _:
                return normalized

    @staticmethod
    def normalize_plugin_group(plugin_type: str | None) -> str | None:
        """Normalize public plugin labels to Meltano project plugin groups."""
        if plugin_type is None:
            return None
        normalized = u.normalize(u.to_str(plugin_type), case="lower").strip()
        mapping = {
            "extractor": c.Meltano.Enums.PluginType.EXTRACTORS.value,
            c.Meltano.Enums.PluginType.EXTRACTORS.value: (
                c.Meltano.Enums.PluginType.EXTRACTORS.value
            ),
            c.Meltano.Prefixes.TAP.rstrip(
                "-"
            ): c.Meltano.Enums.PluginType.EXTRACTORS.value,
            "loader": c.Meltano.Enums.PluginType.LOADERS.value,
            c.Meltano.Enums.PluginType.LOADERS.value: (
                c.Meltano.Enums.PluginType.LOADERS.value
            ),
            c.Meltano.Prefixes.TARGET.rstrip(
                "-"
            ): c.Meltano.Enums.PluginType.LOADERS.value,
            "transformer": c.Meltano.Enums.PluginType.TRANSFORMS.value,
            "transformers": c.Meltano.Enums.PluginType.TRANSFORMS.value,
            c.Meltano.Enums.PluginType.TRANSFORMS.value: (
                c.Meltano.Enums.PluginType.TRANSFORMS.value
            ),
            c.Meltano.Prefixes.DBT.rstrip(
                "-"
            ): c.Meltano.Enums.PluginType.TRANSFORMS.value,
        }
        return mapping.get(normalized, normalized)

    @staticmethod
    def is_help_request(args: t.StrSequence) -> bool:
        """Return whether the provided args request CLI help."""
        normalized_args = FlextMeltanoUtilitiesRuntime._normalized_parts(args)
        return not normalized_args or normalized_args[0] in {
            c.Meltano.Commands.HELP_OPTION,
            c.Meltano.Commands.SHORT_HELP_OPTION,
        }

    @staticmethod
    def resolve_project_root(settings: t.ValueOrModel | p.Settings) -> Path | None:
        """Extract and normalize project_root from a settings-like object."""
        if isinstance(settings, Mapping):
            raw = settings.get("project_root")
        elif isinstance(settings, BaseModel):
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
            c.Meltano.Enums.Environment.DEVELOPMENT.value: "dev",
            c.Meltano.Enums.Environment.TESTING.value: "test",
            c.Meltano.Enums.Environment.PRODUCTION.value: "prod",
        }
        return aliases.get(normalized, normalized)

    @staticmethod
    def build_pipeline_runtime_command(
        tap_name: str,
        target_name: str,
    ) -> list[str]:
        """Build the canonical Meltano ELT runtime command."""
        return FlextMeltanoUtilitiesRuntime._normalized_parts(
            [c.Meltano.Commands.ELT, tap_name, target_name],
        )

    @staticmethod
    def build_dbt_runtime_command(
        dbt_command: str,
        args: t.StrSequence | None = None,
    ) -> list[str]:
        """Build the canonical Meltano DBT invoke runtime command."""
        command = [
            c.Meltano.Commands.INVOKE,
            f"{c.Meltano.Plugin.DBT_DEFAULT_NAME}:{dbt_command}",
        ]
        if args:
            command.extend(FlextMeltanoUtilitiesRuntime._normalized_parts(args))
        return FlextMeltanoUtilitiesRuntime._normalized_parts(command)

    @staticmethod
    def build_bridge_command_args(
        command: str,
        args: t.ConfigurationMapping | None = None,
    ) -> list[str]:
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
        raw_plugin: t.ContainerMapping,
    ) -> dict[str, str] | None:
        """Normalize a Meltano runtime plugin mapping to discovery payload shape."""
        name_val = raw_plugin.get("name", "")
        plugin_name = str(name_val).strip() if name_val is not None else ""
        if not u.chk(plugin_name, empty=False):
            return None
        ns_val = raw_plugin.get("namespace", "")
        pip_val = raw_plugin.get("pip_url", "")
        variant_val = raw_plugin.get("variant", "")
        plugin_data: t.ContainerMapping = {
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
        variants: Mapping[str, object] | None = None,
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
        extra_fields: t.ContainerMapping | None = None,
        success_status: str = c.Meltano.Enums.OperationStatus.SUCCESS,
        failure_status: str = c.Meltano.Enums.OperationStatus.ERROR,
        status_field: str | None = "status",
        duration_field: str | None = "execution_time",
    ) -> t.ContainerMapping:
        """Build a standard command payload for services over Meltano runtime."""
        payload: t.MutableContainerMapping = {
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
        if merged.is_success:
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
        if normalized == c.Meltano.Enums.PluginType.EXTRACTORS.value:
            return c.Meltano.Prefixes.TAP.rstrip("-")
        if normalized == c.Meltano.Enums.PluginType.LOADERS.value:
            return c.Meltano.Prefixes.TARGET.rstrip("-")
        if (
            normalized == c.Meltano.Enums.PluginType.TRANSFORMS.value
            or plugin_name.startswith(c.Meltano.Prefixes.DBT)
        ):
            return "transformer"
        return normalized or plugin_type
