"""FLEXT Pipeline Component Service - Single unified class for component operations.

This module provides the FlextMeltanoComponentService class following FLEXT patterns:
- Single Responsibility Principle
- Railway-oriented programming with FlextResult
- Clean Architecture with domain separation

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import cast

from flext_core import FlextResult, FlextService, u

from flext_meltano.abstractions import FlextMeltanoAbstractions
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.project_service import FlextMeltanoProjectService
from flext_meltano.protocols import FlextMeltanoProtocols
from flext_meltano.typings import FlextMeltanoTypes

# Import aliases for concise usage
t = FlextMeltanoTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels
p = FlextMeltanoProtocols
r = FlextResult
s = FlextService


class FlextMeltanoComponentService(s[t.MeltanoCore.MeltanoConfigDict]):
    """Service for pipeline component operations.

    Handles component discovery, addition, and management following
    FLEXT patterns with railway-oriented programming.
    """

    # Instance attributes for type checker
    _config: FlextMeltanoConfig
    _abstractions: FlextMeltanoAbstractions

    def __init__(self, config: FlextMeltanoConfig | None = None) -> None:
        """Initialize component service with FLEXT configuration."""
        super().__init__()
        self._config = config or FlextMeltanoConfig()
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
                "config": self._config.model_dump()
                if hasattr(self._config, "model_dump")
                else {},
            }

            self.logger.info("FlextMeltanoPluginService executed successfully")
            return r[t.MeltanoCore.MeltanoConfigDict].ok(data=config_data)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Plugin service execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.MeltanoCore.MeltanoConfigDict].fail(error_msg)

    def discover_plugins(
        self,
        project: object | None = None,
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
                # For now, we'll work with dict[str, object] - need to convert back to Project object
                # This is a simplification; in real implementation we'd maintain Project objects
                working_project = temp_project_result.unwrap()

            plugins = []

            # DSL Builder Pattern: Process plugins using u.construct() mnemonic pattern
            def build_plugin_info(plugin_name: str, indexed_plugin: object, plugin_type: str) -> dict[str, str]:
                """Builder function using u.construct() mnemonic pattern for object construction."""
                variants_obj = u.get(indexed_plugin, "variants")
                variants_dict = u.guard(variants_obj, dict, return_value=True)
                variants_str = u.join(u.map(variants_dict, str), sep=",") if variants_dict else ""
                return u.construct(
                    {
                        "name": {"value": plugin_name},
                        "type": {"value": plugin_type},
                        "default_variant": {"field": "default_variant", "default": "", "ops": {"ensure": "str"}},
                        "variants": {"value": variants_str},
                        "logo_url": {"field": "logo_url", "default": "", "ops": {"ensure": "str"}},
                    },
                    source=indexed_plugin,
                )

            # Process extractors using u.process() with limit via filter_keys
            extractors_result = self._abstractions.get_plugins_of_type(
                cast("object", working_project), "extractors"
            )
            if extractors_result.is_success:
                extractors_dict = extractors_result.unwrap()
                extractors_keys = u.take(extractors_dict, 10)
                extractors_plugins_result = u.process(
                    extractors_dict,
                    lambda k, v: build_plugin_info(k, v, "extractor"),
                    filter_keys=set(extractors_keys.keys()),
                )
                if extractors_plugins_result.is_success:
                    plugins.extend(u.vals(extractors_plugins_result))

            # Process loaders using u.process() with limit via filter_keys
            loaders_result = self._abstractions.get_plugins_of_type(
                cast("object", working_project), "loaders"
            )
            if loaders_result.is_success:
                loaders_dict = loaders_result.unwrap()
                loaders_keys = u.take(loaders_dict, 5)
                loaders_plugins_result = u.process(
                    loaders_dict,
                    lambda k, v: build_plugin_info(k, v, "loader"),
                    filter_keys=set(loaders_keys.keys()),
                )
                if loaders_plugins_result.is_success:
                    plugins.extend(u.vals(loaders_plugins_result))

            self.logger.info(f"Discovered {u.count(plugins)} plugins")
            return r[list[dict[str, str]]].ok(plugins)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to discover plugins: {e}"
            self.logger.exception(error_msg, error=str(e))
            return r[list[dict[str, str]]].fail(error_msg)

    def add_plugin(
        self,
        project: object,
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
            self._log_plugin_addition_start(plugin_name, plugin_type)
            .flat_map(lambda _: self._validate_plugin_type(plugin_type))
            .flat_map(
                lambda pt: self._execute_plugin_addition(project, pt, plugin_name)
            )
            .flat_map(
                lambda result: self._build_plugin_addition_result(
                    plugin_name, plugin_type, addition_success=result
                )
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
        def extract_plugin_info(plugins_dict: dict[str, object]) -> r[dict[str, str]]:
            """Extract plugin info from plugins dict."""
            # Use u.not_() + u.in_() for membership check (DSL pattern)
            if u.not_(u.in_(plugin_name, plugins_dict)) or u.empty(u.get(plugins_dict, plugin_name)):
                return r[dict[str, str]].fail(f"Plugin '{plugin_name}' not found in {plugin_type}")

            indexed_plugin = u.get(plugins_dict, plugin_name)
            # Use u.fields() + u.build() for unified extraction and transformation (DSL pattern)
            fields_spec = {"default_variant": "", "variants": {}, "description": "", "logo_url": ""}
            fields_result = u.fields(indexed_plugin, fields_spec)
            if isinstance(fields_result, r):
                return u.cast(fields_result, default_error="Field extraction failed")

            # Use u.build() for unified transformation (DSL pattern)
            def transform_variants(v: dict[str, object]) -> str:
                """Transform variants dict to string."""
                return u.join(u.map(v, str), sep=",") if v else ""

            plugin_info_raw = u.build(
                fields_result,
                ops={
                    "map": lambda d: {
                        "name": plugin_name,
                        "type": plugin_type,
                        "default_variant": str(u.get(d, "default_variant", default="")),
                        "variants": transform_variants(u.guard(u.get(d, "variants"), dict, return_value=True) or {}),
                        "description": str(u.get(d, "description", default="")),
                        "logo_url": str(u.get(d, "logo_url", default="")),
                    }
                },
            )
            return r[dict[str, str]].ok(cast("dict[str, str]", plugin_info_raw))

        try:
            # Use monadic composition to chain operations (DSL pattern)
            return (
                FlextMeltanoProjectService()
                .create_temporary_project(project_id="temp-info-project", prefix="flext_plugin_info_")
                .flat_map(lambda p: self._abstractions.get_plugins_of_type(cast("object", p), plugin_type))
                .flat_map(extract_plugin_info)
            )
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to get plugin info: {e}"
            self.logger.exception(error_msg)
            return r[dict[str, str]].fail(error_msg)

    # Private helper methods

    def _log_plugin_addition_start(
        self, plugin_name: str, plugin_type: str
    ) -> r[None]:
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
                f"Invalid plugin type: {plugin_type}. Valid types: {valid_types}"
            )
        return r[str].ok(plugin_type)

    def _execute_plugin_addition(
        self, project: object, plugin_type_str: str, plugin_name: str
    ) -> r[bool]:
        """Execute the actual plugin addition using abstraction layer."""
        try:
            # Use abstraction layer for plugin addition
            plugin_config = {
                "project": project,
                "plugin_type": plugin_type_str,
                "plugin_name": plugin_name,
            }
            add_result = self._abstractions.add_plugin(plugin_config)

            if add_result.is_failure:
                return r[bool].fail(
                    u.err(add_result, default="Plugin addition failed")
                )

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
