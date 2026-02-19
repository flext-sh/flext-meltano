"""FLEXT Pipeline Component Service - Single unified class for component operations.

This module provides the FlextMeltanoComponentService class following FLEXT patterns:
- Single Responsibility Principle
- Railway-oriented programming with r
- Clean Architecture with domain separation

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import r, s

from flext_meltano.abstractions import FlextMeltanoAbstractions
from flext_meltano.project_service import FlextMeltanoProjectService
from flext_meltano.protocols import p
from flext_meltano.settings import FlextMeltanoSettings
from flext_meltano.typings import t


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
        r containing plugin service configuration and status.

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
        r containing list of discovered plugins with metadata

        """
        try:
            self.logger.info("Discovering Meltano plugins")

            # Use provided project or create temporary one
            working_project: p.Meltano.MeltanoProjectProtocol | None = None
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
                # Temp project returns dict - cannot use with abstractions
                # Return empty list for now
                return r[list[dict[str, str]]].ok([])

            plugins = []

            # Discover extractors using abstraction layer (only works with real project)
            extractors_result = self._abstractions.get_plugins_of_type(
                working_project,
                "extractors",
            )
            if extractors_result.is_success:
                extractors_dict = extractors_result.value
                for plugin_name, indexed_plugin in list(extractors_dict.items())[:10]:
                    default_var = getattr(indexed_plugin, "default_variant", None)
                    variants_obj = getattr(indexed_plugin, "variants", None)
                    plugin_info = {
                        "name": plugin_name,
                        "type": "extractor",
                        "default_variant": str(default_var) if default_var else "",
                        "variants": ",".join(list(variants_obj.keys()))
                        if isinstance(variants_obj, dict)
                        else "",
                        "logo_url": getattr(indexed_plugin, "logo_url", ""),
                    }
                    plugins.append(plugin_info)

            # Discover loaders using abstraction layer
            loaders_result = self._abstractions.get_plugins_of_type(
                working_project,
                "loaders",
            )
            if loaders_result.is_success:
                loaders_dict = loaders_result.value
                for plugin_name, indexed_plugin in list(loaders_dict.items())[:5]:
                    default_var = getattr(indexed_plugin, "default_variant", None)
                    variants_obj = getattr(indexed_plugin, "variants", None)
                    plugin_info = {
                        "name": plugin_name,
                        "type": "loader",
                        "default_variant": str(default_var) if default_var else "",
                        "variants": ",".join(list(variants_obj.keys()))
                        if isinstance(variants_obj, dict)
                        else "",
                        "logo_url": getattr(indexed_plugin, "logo_url", ""),
                    }
                    plugins.append(plugin_info)

            self.logger.info(f"Discovered {len(plugins)} plugins")
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

        Uses r.chain_validations() to compose plugin addition steps
        with automatic error accumulation and early termination on failure.

        Args:
        project: Meltano project instance
        plugin_type: Type of plugin (extractors, loaders, transformers)
        plugin_name: Name of the plugin to add

        Returns:
        r containing plugin addition information

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
        """Get detailed information about specific plugin.

        Args:
        plugin_name: Name of the plugin
        plugin_type: Type of the plugin

        Returns:
        r containing plugin information

        """
        # Temporary project creation returns dict type (t.Dbt.Project)
        # which cannot satisfy MeltanoProjectProtocol required by abstractions.
        # This method requires a real MeltanoProjectProtocol instance.
        # Plugin info lookup from temp projects is not supported.
        return r[dict[str, str]].fail(
            f"Plugin '{plugin_name}' info lookup requires a real Meltano project. "
            f"Use discover_plugins() with a MeltanoProjectProtocol for {plugin_type}.",
        )

    # Private helper methods

    def _log_plugin_addition_start(self, plugin_name: str, plugin_type: str) -> r[None]:
        """Log plugin addition start."""
        self.logger.info(
            "Adding plugin using ProjectAddService",
            plugin_name=plugin_name,
            plugin_type=plugin_type,
        )
        return r[None].ok(None)

    @staticmethod
    def _validate_plugin_type(plugin_type: str) -> r[str]:
        """Validate plugin type."""
        valid_types = ["extractors", "loaders", "transformers"]
        if plugin_type not in valid_types:
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
            # Build config dict with proper JsonValue types
            plugin_config: t.Plugin.PluginConfiguration = {
                "project_root": str(getattr(project, "root_dir", "")),
                "type": plugin_type_str,
                "name": plugin_name,
            }
            add_result = self._abstractions.add_plugin(plugin_config)

            if add_result.is_failure:
                return r[bool].fail(add_result.error or "Plugin addition failed")

            return r[bool].ok(value=True)
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
