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

from flext_core import FlextResult, FlextService

from flext_meltano.abstractions import FlextMeltanoAbstractions
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.project_service import FlextMeltanoProjectService
from flext_meltano.typings import FlextMeltanoTypes


class FlextMeltanoComponentService(
    FlextService[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict]
):
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
    ) -> FlextResult[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict]:
        """Execute the pipeline component service.

        Returns:
        FlextResult containing plugin service configuration and status.

        """
        try:
            config_data: FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict = {
                "service_type": "flext_meltano_plugin_service",
                "status": "ready",
                "config": self._config.model_dump()
                if hasattr(self._config, "model_dump")
                else {},
            }

            self.logger.info("FlextMeltanoPluginService executed successfully")
            return FlextResult[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict].ok(
                data=config_data
            )

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Plugin service execution failed: {e}"
            self.logger.exception(error_msg)
            return FlextResult[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict].fail(
                error_msg
            )

    def discover_plugins(
        self,
        project: object | None = None,
    ) -> FlextResult[list[dict[str, str]]]:
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
                    return FlextResult[list[dict[str, str]]].fail(
                        temp_project_result.error
                        or "Failed to create temporary project",
                    )
                # For now, we'll work with dict[str, object] - need to convert back to Project object
                # This is a simplification; in real implementation we'd maintain Project objects
                working_project = temp_project_result.unwrap()

            plugins = []

            # Discover extractors using abstraction layer
            extractors_result = self._abstractions.get_plugins_of_type(
                cast("object", working_project), "extractors"
            )
            if extractors_result.is_success:
                extractors_dict = extractors_result.unwrap()
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
                cast("object", working_project), "loaders"
            )
            if loaders_result.is_success:
                loaders_dict = loaders_result.unwrap()
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
            return FlextResult[list[dict[str, str]]].ok(data=plugins)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to discover plugins: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult[list[dict[str, str]]].fail(error_msg)

    def add_plugin(
        self,
        project: object,
        plugin_type: str,
        plugin_name: str,
    ) -> FlextResult[dict[str, str]]:
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
    ) -> FlextResult[dict[str, str]]:
        """Get detailed information about specific plugin.

        Args:
        plugin_name: Name of the plugin
        plugin_type: Type of the plugin

        Returns:
        FlextResult containing plugin information

        """
        try:
            # Use consolidated temporary project creation method
            project_result = FlextMeltanoProjectService().create_temporary_project(
                project_id="temp-info-project",
                prefix="flext_plugin_info_",
            )
            if project_result.is_failure:
                return FlextResult[dict[str, str]].fail(
                    f"Failed to create temp project: {project_result.error}",
                )

            # Get plugins of type
            plugins_result = self._abstractions.get_plugins_of_type(
                cast("object", project_result.unwrap()), plugin_type
            )

            if plugins_result.is_failure:
                return FlextResult[dict[str, str]].fail(
                    f"Failed to get plugins of type {plugin_type}: {plugins_result.error}"
                )

            plugins_dict = plugins_result.unwrap()

            if plugin_name not in plugins_dict:
                return FlextResult[dict[str, str]].fail(
                    f"Plugin '{plugin_name}' not found in {plugin_type}",
                )

            indexed_plugin = plugins_dict[plugin_name]
            default_var = getattr(indexed_plugin, "default_variant", None)
            variants_obj = getattr(indexed_plugin, "variants", None)
            plugin_info = {
                "name": plugin_name,
                "type": plugin_type,
                "default_variant": str(default_var) if default_var else "",
                "variants": ",".join(list(variants_obj.keys()))
                if isinstance(variants_obj, dict)
                else "",
                "description": getattr(indexed_plugin, "description", ""),
                "logo_url": getattr(indexed_plugin, "logo_url", ""),
            }

            return FlextResult[dict[str, str]].ok(data=plugin_info)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to get plugin info: {e}"
            self.logger.exception(error_msg)
            return FlextResult[dict[str, str]].fail(error_msg)

    # Private helper methods

    def _log_plugin_addition_start(
        self, _plugin_name: str, plugin_type: str
    ) -> FlextResult[None]:
        """Log plugin addition start."""
        self.logger.info(
            "Adding plugin using ProjectAddService",
            plugin_name=plugin_name,
            plugin_type=plugin_type,
        )
        return FlextResult.ok(data=None)

    def _validate_plugin_type(self, plugin_type: str) -> FlextResult[str]:
        """Validate plugin type."""
        valid_types = ["extractors", "loaders", "transformers"]
        if plugin_type not in valid_types:
            return FlextResult[str].fail(
                f"Invalid plugin type: {plugin_type}. Valid types: {valid_types}"
            )
        return FlextResult[str].ok(data=plugin_type)

    def _execute_plugin_addition(
        self, project: object, plugin_type_str: str, _plugin_name: str
    ) -> FlextResult[bool]:
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
                return FlextResult[bool].fail(
                    add_result.error or "Plugin addition failed"
                )

            return FlextResult[bool].ok(data=True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return FlextResult[bool].fail(f"Plugin addition failed: {e}")

    def _build_plugin_addition_result(
        self,
        plugin_name: str,
        plugin_type: str,
        *,
        addition_success: bool,
    ) -> FlextResult[dict[str, str]]:
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

        return FlextResult[dict[str, str]].ok(data=plugin_result)


# Import here to avoid circular import

__all__ = [
    "FlextMeltanoComponentService",
]
