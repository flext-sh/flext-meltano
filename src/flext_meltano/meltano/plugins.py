"""FLEXT Pipeline Component Service - Single unified class for component operations.

This module provides the FlextMeltanoComponentService class following FLEXT patterns:
- Single Responsibility Principle
- Railway-oriented programming with FlextResult
- Clean Architecture with domain separation

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextResult, FlextService, FlextTypes

from flext_meltano.abstractions import FlextMeltanoAbstractions
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.project_service import FlextMeltanoProjectService
from flext_meltano.protocols import FlextMeltanoProtocols
from flext_meltano.settings import FlextMeltanoSettings
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.utilities import u

# Import aliases following order: c -> t -> p -> r -> m -> u
c = FlextMeltanoConstants
t = FlextMeltanoTypes
t_core = FlextTypes
p = FlextMeltanoProtocols
r = FlextResult
m = FlextMeltanoModels
s = FlextService


class FlextMeltanoComponentService(s[t.MeltanoCore.MeltanoConfigDict]):
    """Service for pipeline component operations.

    Handles component discovery, addition, and management following
    FLEXT patterns with railway-oriented programming.
    """

    # Instance attributes for type checker
    _abstractions: FlextMeltanoAbstractions

    def __init__(self, config: FlextMeltanoSettings | None = None) -> None:
        """Initialize component service with FLEXT configuration."""
        super().__init__()
        self._meltano_config: FlextMeltanoSettings = config or FlextMeltanoSettings()
        self._abstractions = FlextMeltanoAbstractions()

    def execute(
        self,
    ) -> r[t.MeltanoCore.MeltanoConfigDict]:
        """Execute the pipeline component service.

        Returns:
        FlextResult containing plugin service configuration and status.

        """
        try:
            config_data: t.MeltanoCore.MeltanoConfigDict = {
                "service_type": "flext_meltano_plugin_service",
                "status": "ready",
                "config": self._meltano_config.model_dump()
                if hasattr(self._meltano_config, "model_dump")
                else {},
            }

            self.logger.info("FlextMeltanoPluginService executed successfully")
            return r[t.MeltanoCore.MeltanoConfigDict].ok(config_data)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Plugin service execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.MeltanoCore.MeltanoConfigDict].fail(error_msg)

    def discover_plugins(
        self,
        project: p.Meltano.MeltanoProjectProtocol | None = None,
    ) -> r[list[dict[str, str]]]:
        """Discover plugins from Meltano Hub using native API.

        Args:
        project: Optional Project instance (creates temporary if None)

        Returns:
        FlextResult containing list of discovered plugins with metadata

        """
        try:
            self.logger.info("Discovering Meltano plugins")

            # Use provided project or create temporary one
            working_project: p.Meltano.MeltanoProjectProtocol
            if project:
                working_project = project
            else:
                temp_project_result = (
                    FlextMeltanoProjectService().create_temporary_project()
                )
                if temp_project_result.is_failure:
                    return r[list[dict[str, str]]].fail(
                        temp_project_result.error
                        or "Failed to create temporary project",
                    )

                # Type narrowing: ensure result is a protocol-compliant project
                temp_project = temp_project_result.value
                if not isinstance(temp_project, p.Meltano.MeltanoProjectProtocol):
                    return r[list[dict[str, str]]].fail(
                        "Temporary project does not satisfy MeltanoProjectProtocol",
                    )
                working_project = temp_project

            plugins = []

            # DSL Builder Pattern: Process plugins using u.construct() mnemonic pattern
            def build_plugin_info(
                plugin_name: str,
                indexed_plugin: t.Plugin.PluginDefinition,
                plugin_type: str,
            ) -> dict[str, str]:
                """Builder function using u.construct() mnemonic pattern for object construction."""
                variants_obj = u.get(indexed_plugin, "variants")
                variants_raw = u.guard(variants_obj, dict, return_value=True)
                variants_dict = variants_raw if isinstance(variants_raw, dict) else {}
                variants_str = ""
                if variants_dict:
                    items_list = list(variants_dict.keys())
                    variants_str = u.join(items_list, separator=",")

                constructed = u.construct(
                    {
                        "name": {"value": plugin_name},
                        "type": {"value": plugin_type},
                        "default_variant": {
                            "field": "default_variant",
                            "default": "",
                            "ops": {"ensure": "str"},
                        },
                        "variants": {"value": variants_str},
                        "logo_url": {
                            "field": "logo_url",
                            "default": "",
                            "ops": {"ensure": "str"},
                        },
                    },
                    source=indexed_plugin,
                )

                # Type narrowing: u.construct() returns dict[str, str] when all values are str
                if not isinstance(constructed, dict):
                    return {}

                # Ensure all values are strings
                result: dict[str, str] = {}
                for key, value in constructed.items():
                    if isinstance(key, str):
                        result[key] = str(value) if value is not None else ""

                return result

            # Process extractors using u.process() with limit via filter_keys
            # Type narrowing: ensure working_project satisfies the protocol
            if not isinstance(working_project, p.Meltano.MeltanoProjectProtocol):
                # Create a protocol-compliant wrapper if needed
                return r[list[dict[str, str]]].fail(
                    "Invalid project type - does not satisfy MeltanoProjectProtocol",
                )

            extractors_result = self._abstractions.get_plugins_of_type(
                working_project,
                "extractors",
            )
            if extractors_result.is_success:
                extractors_dict = extractors_result.value
                # Limit to first 10 extractors
                max_extractors = 10
                for idx, (k, v) in enumerate(extractors_dict.items()):
                    if idx >= max_extractors:
                        break
                    plugins.append(build_plugin_info(k, v, "extractor"))

            # Process loaders - limit to first 5
            loaders_result = self._abstractions.get_plugins_of_type(
                working_project,
                "loaders",
            )
            if loaders_result.is_success:
                loaders_dict = loaders_result.value
                # Limit to first 5 loaders
                max_loaders = 5
                for idx, (k, v) in enumerate(loaders_dict.items()):
                    if idx >= max_loaders:
                        break
                    plugins.append(build_plugin_info(k, v, "loader"))

            self.logger.info(f"Discovered {u.count(plugins)} plugins")
            return r[list[dict[str, str]]].ok(plugins)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to discover plugins: {e}"
            self.logger.exception(error_msg, error=str(e))
            return r[list[dict[str, str]]].fail(error_msg)

    def add_plugin(
        self,
        project: p.Meltano.MeltanoProjectProtocol,
        plugin_type: str,
        plugin_name: str,
    ) -> r[dict[str, str]]:
        """Add plugin to Meltano project using railway-oriented validation chain.

        Uses FlextResult.chain_validations() to compose plugin addition steps
        with automatic error accumulation and early termination on failure.

        Args:
        project: Meltano project instance
        plugin_type: Type of plugin (extractors, loaders, transformers)
        plugin_name: Name of the plugin to add

        Returns:
        FlextResult containing plugin addition information

        """
        # RAILWAY PATTERN: Chain validations and operations
        return (
            self
            ._log_plugin_addition_start(plugin_name, plugin_type)
            .flat_map(lambda _: self._validate_plugin_type(plugin_type))
            .flat_map(
                lambda pt: self._execute_plugin_addition(project, pt, plugin_name),
            )
            .flat_map(
                lambda result: self._build_plugin_addition_result(
                    plugin_name,
                    plugin_type,
                    addition_success=result,
                ),
            )
        )

    def get_plugin_info(
        self,
        plugin_name: str,
        plugin_type: str,
    ) -> r[dict[str, str]]:
        """Get detailed information about specific plugin using monadic composition.

        Args:
        plugin_name: Name of the plugin
        plugin_type: Type of the plugin

        Returns:
        FlextResult containing plugin information

        """

        # Use monadic composition to reduce returns (DSL pattern)
        def extract_plugin_info(plugins_data: object) -> r[dict[str, str]]:
            """Extract plugin info from plugins dict."""
            plugins_dict = plugins_data if isinstance(plugins_data, dict) else {}
            # Use u.not_() + u.in_() for membership check (DSL pattern)
            if u.not_(u.in_(plugin_name, plugins_dict)) or u.empty(
                u.get(plugins_dict, plugin_name),
            ):
                return r[dict[str, str]].fail(
                    f"Plugin '{plugin_name}' not found in {plugin_type}",
                )

            indexed_plugin = u.get(plugins_dict, plugin_name)
            # Use u.fields() + u.build() for unified extraction and transformation (DSL pattern)
            fields_spec: dict[str, str] = {
                "default_variant": "",
                "variants": "{}",
                "description": "",
                "logo_url": "",
            }
            fields_result = u.fields(indexed_plugin, fields_spec)
            if isinstance(fields_result, r) and fields_result.is_failure:
                error_msg = fields_result.error or "Field extraction failed"
                return r[dict[str, str]].fail(error_msg)

            # Extract values directly with type narrowing
            def transform_variants_dict(v: object) -> str:
                """Transform variants dict to string."""
                if not isinstance(v, dict):
                    return ""
                items_list = list(v.keys())
                return u.join(items_list, separator=",") if items_list else ""

            # Get data from fields_result
            data = (
                fields_result.value if isinstance(fields_result, r) else fields_result
            )
            if not isinstance(data, dict):
                data = {}

            # Use .get() for dict access with proper defaults
            variants_raw = data.get("variants", {})
            default_variant_raw = data.get("default_variant")
            description_raw = data.get("description")
            logo_url_raw = data.get("logo_url")

            plugin_info: dict[str, str] = {
                "name": plugin_name,
                "type": plugin_type,
                "default_variant": str(default_variant_raw)
                if default_variant_raw
                else "",
                "variants": transform_variants_dict(variants_raw),
                "description": str(description_raw) if description_raw else "",
                "logo_url": str(logo_url_raw) if logo_url_raw else "",
            }
            return r[dict[str, str]].ok(plugin_info)

        try:
            # Use monadic composition to chain operations (DSL pattern)
            # Create temporary project and ensure it satisfies protocol
            temp_project_result = FlextMeltanoProjectService().create_temporary_project(
                project_id="temp-info-project",
                prefix="flext_plugin_info_",
            )

            if temp_project_result.is_failure:
                return r[dict[str, str]].fail(
                    temp_project_result.error or "Failed to create temporary project",
                )

            # Type narrowing: ensure project satisfies protocol
            temp_project = temp_project_result.value
            if not isinstance(temp_project, p.Meltano.MeltanoProjectProtocol):
                return r[dict[str, str]].fail(
                    "Temporary project does not satisfy MeltanoProjectProtocol",
                )

            # Get plugins and extract info
            plugins_result = self._abstractions.get_plugins_of_type(
                temp_project,
                plugin_type,
            )

            if plugins_result.is_failure:
                return r[dict[str, str]].fail(
                    plugins_result.error or "Failed to get plugins",
                )

            return extract_plugin_info(plugins_result.value)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to get plugin info: {e}"
            self.logger.exception(error_msg)
            return r[dict[str, str]].fail(error_msg)

    # Private helper methods

    def _log_plugin_addition_start(self, plugin_name: str, plugin_type: str) -> r[None]:
        """Log plugin addition start."""
        self.logger.info(
            "Adding plugin using ProjectAddService",
            plugin_name=plugin_name,
            plugin_type=plugin_type,
        )
        return r.ok(None)

    @staticmethod
    def _validate_plugin_type(plugin_type: str) -> r[str]:
        """Validate plugin type."""
        valid_types = ["extractors", "loaders", "transformers"]
        # Use u.not_() + u.in_() for membership check (DSL pattern)
        if u.not_(u.in_(plugin_type, valid_types)):
            return r[str].fail(
                f"Invalid plugin type: {plugin_type}. Valid types: {valid_types}",
            )
        return r[str].ok(plugin_type)

    def _execute_plugin_addition(
        self,
        project: p.Meltano.MeltanoProjectProtocol,
        plugin_type_str: str,
        plugin_name: str,
    ) -> r[bool]:
        """Execute the actual plugin addition using abstraction layer."""
        try:
            # Use abstraction layer for plugin addition
            # Build properly typed plugin config
            plugin_config: t.Plugin.PluginConfiguration = {
                "project_root": str(project.root_dir),
                "plugin_type": plugin_type_str,
                "plugin_name": plugin_name,
            }
            add_result = self._abstractions.add_plugin(plugin_config)

            if add_result.is_failure:
                error_msg = add_result.error or "Plugin addition failed"
                return r[bool].fail(error_msg)

            return r[bool].ok(True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[bool].fail(f"Plugin addition failed: {e}")

    def _build_plugin_addition_result(
        self,
        plugin_name: str,
        plugin_type: str,
        *,
        addition_success: bool,
    ) -> r[dict[str, str]]:
        """Build successful plugin addition result."""
        plugin_result: dict[str, str] = {
            "success": "true" if addition_success else "false",
            "plugin_name": plugin_name,
            "plugin_type": plugin_type,
            "addition_method": "project_add_service_native",
        }

        self.logger.info(
            "Plugin added successfully",
            plugin_name=plugin_name,
            plugin_type=plugin_type,
        )

        return r[dict[str, str]].ok(plugin_result)


# Import here to avoid circular import

__all__ = [
    "FlextMeltanoComponentService",
]
