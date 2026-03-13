"""FLEXT Pipeline Component Service - Single unified class for component operations.

This module provides the FlextMeltanoComponentService class following FLEXT patterns:
- Single Responsibility Principle
- Railway-oriented programming with r
- Clean Architecture with domain separation

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TypeGuard, override

from flext_core import r, s

from flext_meltano import (
    FlextMeltanoProjectService,
    FlextMeltanoSettings,
    m,
    p,
    t,
    u,
)
from flext_meltano.abstractions import FlextMeltanoAbstractions


def _is_meltano_project(value: object) -> TypeGuard[p.Meltano.Project]:
    """Type guard for protocol-compatible Meltano project objects."""
    return hasattr(value, "root_dir") and callable(getattr(value, "find_plugins", None))


class FlextMeltanoComponentService(s[t.Meltano.MeltanoConfigDict]):
    """Service for pipeline component operations.

    Handles component discovery, addition, and management following
    FLEXT patterns with railway-oriented programming.
    """

    def __init__(self, config: FlextMeltanoSettings | None = None) -> None:
        """Initialize component service with FLEXT configuration."""
        super().__init__()
        self._meltano_config: FlextMeltanoSettings = (
            config if config is not None else FlextMeltanoSettings()
        )

    @staticmethod
    def _validate_plugin_type(plugin_type: str) -> r[str]:
        """Validate plugin type."""
        valid_types = ["extractors", "loaders", "transformers"]
        if u.not_(u.in_(plugin_type, valid_types)):
            return r[str].fail(
                f"Invalid plugin type: {plugin_type}. Valid types: {valid_types}"
            )
        return r[str].ok(plugin_type)

    def add_plugin(
        self, project: p.Meltano.Project, plugin_type: str, plugin_name: str
    ) -> r[Mapping[str, str]]:
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
        return (
            self
            ._log_plugin_addition_start(plugin_name, plugin_type)
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

    def discover_plugins(
        self, project: p.Meltano.Project | None = None
    ) -> r[list[Mapping[str, str]]]:
        """Discover plugins from Meltano Hub using native API.

        Args:
        project: Optional Project instance (creates temporary if None)

        Returns:
        r containing list of discovered plugins with metadata

        """
        try:
            self.logger.info("Discovering Meltano plugins")
            working_project: p.Meltano.Project
            if project:
                working_project = project
            else:
                temp_project_result = (
                    FlextMeltanoProjectService().create_temporary_project()
                )
                if temp_project_result.is_failure:
                    return r[list[Mapping[str, str]]].fail(
                        temp_project_result.error
                        or "Failed to create temporary project"
                    )
                temp_project = temp_project_result.value
                if not _is_meltano_project(temp_project):
                    return r[list[Mapping[str, str]]].fail(
                        "Temporary project does not satisfy Project"
                    )
                working_project = temp_project
            plugins: list[Mapping[str, str]] = []

            def build_plugin_info(
                plugin_name: str,
                indexed_plugin: t.Meltano.PluginDefinition,
                plugin_type: str,
            ) -> Mapping[str, str]:
                """Builder function using u.construct() mnemonic pattern for object construction."""
                source = m.Meltano.PluginDiscoverySource.model_validate(indexed_plugin)
                variants_str = (
                    u.join(list(source.variants.keys()), separator=",")
                    if source.variants
                    else ""
                )
                constructed = u.construct({
                    "name": {"value": plugin_name},
                    "type": {"value": plugin_type},
                    "default_variant": {"value": source.default_variant},
                    "variants": {"value": variants_str},
                    "logo_url": {"value": source.logo_url},
                    "description": {"value": source.description},
                })
                return m.Meltano.PluginDiscoveryItem.model_validate(constructed).model_dump()

            abstractions: FlextMeltanoAbstractions = FlextMeltanoAbstractions()
            extractors_result: r[Mapping[str, t.Meltano.PluginDefinition]] = (
                abstractions.get_plugins_of_type(working_project, "extractors")
            )
            if extractors_result.is_success:
                extractors_dict: Mapping[str, t.Meltano.PluginDefinition] = (
                    extractors_result.value
                )
                max_extractors = 10
                for idx, (k, v) in enumerate(extractors_dict.items()):
                    if idx >= max_extractors:
                        break
                    plugins.append(build_plugin_info(k, v, "extractor"))
            loaders_result: r[Mapping[str, t.Meltano.PluginDefinition]] = (
                abstractions.get_plugins_of_type(working_project, "loaders")
            )
            if loaders_result.is_success:
                loaders_dict: Mapping[str, t.Meltano.PluginDefinition] = (
                    loaders_result.value
                )
                max_loaders = 5
                for idx, (k, v) in enumerate(loaders_dict.items()):
                    if idx >= max_loaders:
                        break
                    plugins.append(build_plugin_info(k, v, "loader"))
            self.logger.info(f"Discovered {u.count(plugins)} plugins")
            return r[list[Mapping[str, str]]].ok(plugins)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to discover plugins: {e}"
            self.logger.exception(error_msg, error=str(e))
            return r[list[Mapping[str, str]]].fail(error_msg)

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute the pipeline component service.

        Returns:
        r containing plugin service configuration and status.

        """
        try:
            config_data: t.Meltano.MeltanoConfigDict = {
                "service_type": "flext_meltano_plugin_service",
                "status": "ready",
                "config": self._meltano_config.model_dump()
                if u.is_pydantic_model(self._meltano_config)
                else {},
            }
            self.logger.info("FlextMeltanoPluginService executed successfully")
            return r[t.Meltano.MeltanoConfigDict].ok(config_data)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Plugin service execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.Meltano.MeltanoConfigDict].fail(error_msg)

    def get_plugin_info(
        self, plugin_name: str, plugin_type: str
    ) -> r[Mapping[str, str]]:
        """Get detailed information about specific plugin using monadic composition.

        Args:
        plugin_name: Name of the plugin
        plugin_type: Type of the plugin

        Returns:
        r containing plugin information

        """

        def extract_plugin_info(plugins_data: object) -> r[Mapping[str, str]]:
            """Extract plugin info from plugins dict."""
            plugins_dict = m.Meltano.PluginDiscoveryCatalog.model_validate({
                "plugins": plugins_data
            }).plugins
            if u.not_(u.in_(plugin_name, plugins_dict)) or u.empty(
                u.get(plugins_dict, plugin_name)
            ):
                return r[Mapping[str, str]].fail(
                    f"Plugin '{plugin_name}' not found in {plugin_type}"
                )
            indexed_plugin = plugins_dict[plugin_name]
            variants_str = (
                u.join(list(indexed_plugin.variants.keys()), separator=",")
                if indexed_plugin.variants
                else ""
            )
            plugin_info = m.Meltano.PluginDiscoveryItem.model_validate({
                "name": plugin_name,
                "type": plugin_type,
                "default_variant": indexed_plugin.default_variant,
                "variants": variants_str,
                "description": indexed_plugin.description,
                "logo_url": indexed_plugin.logo_url,
            }).model_dump()
            return r[Mapping[str, str]].ok(plugin_info)

        try:
            temp_project_result = FlextMeltanoProjectService().create_temporary_project(
                project_id="temp-info-project", prefix="flext_plugin_info_"
            )
            if temp_project_result.is_failure:
                return r[Mapping[str, str]].fail(
                    temp_project_result.error or "Failed to create temporary project"
                )
            temp_project = temp_project_result.value
            if not _is_meltano_project(temp_project):
                return r[Mapping[str, str]].fail(
                    "Temporary project does not satisfy Project"
                )
            abstractions: FlextMeltanoAbstractions = FlextMeltanoAbstractions()
            plugins_result: r[Mapping[str, t.Meltano.PluginDefinition]] = (
                abstractions.get_plugins_of_type(temp_project, plugin_type)
            )
            if plugins_result.is_failure:
                return r[Mapping[str, str]].fail(
                    plugins_result.error or "Failed to get plugins"
                )
            return extract_plugin_info(plugins_result.value)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to get plugin info: {e}"
            self.logger.exception(error_msg)
            return r[Mapping[str, str]].fail(error_msg)

    def _build_plugin_addition_result(
        self, plugin_name: str, plugin_type: str, *, addition_success: bool
    ) -> r[Mapping[str, str]]:
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
        return r[Mapping[str, str]].ok(plugin_result)

    def _execute_plugin_addition(
        self, project: p.Meltano.Project, plugin_type_str: str, plugin_name: str
    ) -> r[bool]:
        """Execute the actual plugin addition using abstraction layer."""
        try:
            plugin_config: t.Meltano.PluginConfiguration = {
                "project_root": str(project.root_dir),
                "plugin_type": plugin_type_str,
                "plugin_name": plugin_name,
            }
            abstractions: FlextMeltanoAbstractions = FlextMeltanoAbstractions()
            add_result: r[bool] = abstractions.add_plugin(plugin_config)
            if add_result.is_failure:
                error_msg = add_result.error or "Plugin addition failed"
                return r[bool].fail(error_msg)
            return r[bool].ok(value=True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[bool].fail(f"Plugin addition failed: {e}")

    def _log_plugin_addition_start(self, plugin_name: str, plugin_type: str) -> r[None]:
        """Log plugin addition start."""
        self.logger.info(
            "Adding plugin using ProjectAddService",
            plugin_name=plugin_name,
            plugin_type=plugin_type,
        )
        return r[None].ok(None)


__all__ = ["FlextMeltanoComponentService"]
