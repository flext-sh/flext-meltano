"""FLEXT Meltano Plugin Service - Single unified class for plugin operations.

This module provides the FlextMeltanoPluginService class following FLEXT patterns:
- Single Responsibility Principle
- Railway-oriented programming with FlextCore.Result
- Clean Architecture with domain separation

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import cast

from flext_core import FlextCore
from meltano.core.project import Project

from flext_meltano.abstractions import FlextMeltanoAbstractions
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.project_service import FlextMeltanoProjectService
from flext_meltano.protocols import FlextMeltanoProtocols
from flext_meltano.typings import FlextMeltanoTypes


class FlextMeltanoPluginService(
    FlextCore.Service[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict]
):
    """Service for Meltano plugin operations.

    Handles plugin discovery, addition, and management following
    FLEXT patterns with railway-oriented programming.
    """

    # Instance attributes for type checker
    _config: FlextMeltanoConfig
    logger: FlextCore.Logger
    _abstractions: FlextMeltanoAbstractions

    def __init__(self, config: FlextMeltanoConfig | None = None) -> None:
        """Initialize plugin service with FLEXT configuration."""
        super().__init__()
        self._config = config or FlextMeltanoConfig()
        self._logger = FlextCore.Logger(__name__)
        self._abstractions = FlextMeltanoAbstractions()

    def execute(
        self,
    ) -> FlextCore.Result[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict]:
        """Execute the Meltano plugin service.

        Returns:
            FlextCore.Result containing plugin service configuration and status.

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
            return FlextCore.Result[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict].ok(
                data=config_data
            )

        except Exception as e:
            error_msg = f"Plugin service execution failed: {e}"
            self.logger.exception(error_msg)
            return FlextCore.Result[
                FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict
            ].fail(error_msg)

    def discover_plugins(
        self,
        project: object | None = None,
    ) -> FlextCore.Result[list[FlextCore.Types.StringDict]]:
        """Discover plugins from Meltano Hub using native API.

        Args:
            project: Optional Project instance (creates temporary if None)

        Returns:
            FlextCore.Result containing list of discovered plugins with metadata

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
                    return FlextCore.Result[list[FlextCore.Types.StringDict]].fail(
                        temp_project_result.error
                        or "Failed to create temporary project",
                    )
                # For now, we'll work with dict - need to convert back to Project object
                # This is a simplification; in real implementation we'd maintain Project objects
                working_project = temp_project_result.unwrap()

            plugins = []

            # Discover extractors using abstraction layer
            extractors_result = self._abstractions.get_plugins_of_type(
                cast("Project", working_project), "extractors"
            )
            if extractors_result.is_success:
                extractors_dict = cast(
                    "dict[str, FlextMeltanoProtocols.MeltanoPluginProtocol]",
                    extractors_result.unwrap(),
                )
                for plugin_name, indexed_plugin in list(extractors_dict.items())[:10]:
                    plugin_info = {
                        "name": plugin_name,
                        "type": "extractor",
                        "default_variant": str(indexed_plugin.default_variant),
                        "variants": ",".join(list(indexed_plugin.variants.keys()))
                        if indexed_plugin.variants
                        else "",
                        "logo_url": getattr(indexed_plugin, "logo_url", ""),
                    }
                    plugins.append(plugin_info)

            # Discover loaders using abstraction layer
            loaders_result = self._abstractions.get_plugins_of_type(
                cast("Project", working_project), "loaders"
            )
            if loaders_result.is_success:
                loaders_dict = cast(
                    "dict[str, FlextMeltanoProtocols.MeltanoPluginProtocol]",
                    loaders_result.unwrap(),
                )
                for plugin_name, indexed_plugin in list(loaders_dict.items())[:5]:
                    plugin_info = {
                        "name": plugin_name,
                        "type": "loader",
                        "default_variant": str(indexed_plugin.default_variant),
                        "variants": ",".join(list(indexed_plugin.variants.keys()))
                        if indexed_plugin.variants
                        else "",
                        "logo_url": getattr(indexed_plugin, "logo_url", ""),
                    }
                    plugins.append(plugin_info)

            self.logger.info(f"Discovered {len(plugins)} plugins")
            return FlextCore.Result[list[FlextCore.Types.StringDict]].ok(data=plugins)

        except Exception as e:
            error_msg = f"Failed to discover plugins: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextCore.Result[list[FlextCore.Types.StringDict]].fail(error_msg)

    def add_plugin(
        self,
        project: object,
        plugin_type: str,
        plugin_name: str,
    ) -> FlextCore.Result[FlextCore.Types.StringDict]:
        """Add plugin to Meltano project using railway-oriented validation chain.

        Uses FlextCore.Result.chain_validations() to compose plugin addition steps
        with automatic error accumulation and early termination on failure.

        Args:
            project: Meltano project instance
            plugin_type: Type of plugin (extractors, loaders, transformers)
            plugin_name: Name of the plugin to add

        Returns:
            FlextCore.Result containing plugin addition information

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
    ) -> FlextCore.Result[FlextCore.Types.StringDict]:
        """Get detailed information about specific plugin.

        Args:
            plugin_name: Name of the plugin
            plugin_type: Type of the plugin

        Returns:
            FlextCore.Result containing plugin information

        """
        try:
            # Use consolidated temporary project creation method
            project_result = FlextMeltanoProjectService().create_temporary_project(
                project_id="temp-info-project",
                prefix="flext_plugin_info_",
            )
            if project_result.is_failure:
                return FlextCore.Result[FlextCore.Types.StringDict].fail(
                    f"Failed to create temp project: {project_result.error}",
                )

            # Get plugins of type
            plugins_result = self._abstractions.get_plugins_of_type(
                cast("Project", project_result.unwrap()), plugin_type
            )

            if plugins_result.is_failure:
                return FlextCore.Result[FlextCore.Types.StringDict].fail(
                    f"Failed to get plugins of type {plugin_type}: {plugins_result.error}"
                )

            plugins_dict = cast(
                "dict[str, FlextMeltanoProtocols.MeltanoPluginProtocol]",
                plugins_result.unwrap(),
            )

            if plugin_name not in plugins_dict:
                return FlextCore.Result[FlextCore.Types.StringDict].fail(
                    f"Plugin '{plugin_name}' not found in {plugin_type}",
                )

            indexed_plugin = plugins_dict[plugin_name]
            plugin_info = {
                "name": plugin_name,
                "type": plugin_type,
                "default_variant": str(indexed_plugin.default_variant),
                "variants": ",".join(list(indexed_plugin.variants.keys()))
                if indexed_plugin.variants
                else "",
                "description": getattr(indexed_plugin, "description", ""),
                "logo_url": getattr(indexed_plugin, "logo_url", ""),
            }

            return FlextCore.Result[FlextCore.Types.StringDict].ok(data=plugin_info)

        except Exception as e:
            error_msg = f"Failed to get plugin info: {e}"
            self.logger.exception(error_msg)
            return FlextCore.Result[FlextCore.Types.StringDict].fail(error_msg)

    # Private helper methods

    def _log_plugin_addition_start(
        self, plugin_name: str, plugin_type: str
    ) -> FlextCore.Result[None]:
        """Log plugin addition start."""
        self.logger.info(
            "Adding plugin using ProjectAddService",
            plugin_name=plugin_name,
            plugin_type=plugin_type,
        )
        return FlextCore.Result.ok(data=None)

    def _validate_plugin_type(self, plugin_type: str) -> FlextCore.Result[str]:
        """Validate plugin type."""
        valid_types = ["extractors", "loaders", "transformers"]
        if plugin_type not in valid_types:
            return FlextCore.Result[str].fail(
                f"Invalid plugin type: {plugin_type}. Valid types: {valid_types}"
            )
        return FlextCore.Result[str].ok(data=plugin_type)

    def _execute_plugin_addition(
        self, project: object, plugin_type_str: str, plugin_name: str
    ) -> FlextCore.Result[bool]:
        """Execute the actual plugin addition using abstraction layer."""
        try:
            # Use abstraction layer for plugin addition
            add_result = self._abstractions.add_plugin(
                cast("Project", project), plugin_type_str, plugin_name
            )

            if add_result.is_failure:
                return FlextCore.Result[bool].fail(
                    add_result.error or "Plugin addition failed"
                )

            return FlextCore.Result[bool].ok(data=True)
        except Exception as e:
            return FlextCore.Result[bool].fail(f"Plugin addition failed: {e}")

    def _build_plugin_addition_result(
        self,
        plugin_name: str,
        plugin_type: str,
        *,
        addition_success: bool,
    ) -> FlextCore.Result[FlextCore.Types.StringDict]:
        """Build successful plugin addition result."""
        plugin_result: FlextCore.Types.StringDict = {
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

        return FlextCore.Result[FlextCore.Types.StringDict].ok(data=plugin_result)


# Import here to avoid circular import

__all__ = [
    "FlextMeltanoPluginService",
]
