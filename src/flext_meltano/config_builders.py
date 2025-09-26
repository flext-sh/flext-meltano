"""FLEXT Meltano Config Builders - Configuration building utilities.

SOURCE OF TRUTH: All configuration through FlextMeltanoConstants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import FlextLogger, FlextResult, FlextUtilities
from flext_meltano.constants import FlextMeltanoConstants

# Type alias for configuration dictionaries
ConfigDict = dict["str", "object"]


class FlextMeltanoConfigBuilders:
    """UNIFIED configuration builders class - SINGLE RESPONSIBILITY.

    Handles ALL Meltano configuration building operations in one cohesive class
    following SOLID principles and eliminating nested class violations.

    SOLID Principles Compliance:
    - Single Responsibility: ONE class with unified configuration building purpose
    - Open/Closed: Extensible through method addition, closed for structural modification
    - Liskov Substitution: All configuration methods return consistent FlextResult types
    - Interface Segregation: Clear method separation by configuration type
    - Dependency Inversion: Depends on flext-core abstractions, not implementations
    """

    # =================================================================
    # UNIFIED CONFIGURATION BUILDING METHODS - NO NESTED CLASSES
    # =================================================================

    @override
    def __init__(self: object) -> None:
        """Initialize unified configuration builders."""
        self._logger = FlextLogger(__name__)

    # DBT Configuration Methods

    def create_dbt_config(
        self,
        project_name: str,
        profile_name: str = "",
    ) -> FlextResult[ConfigDict]:
        """Create basic DBT configuration using FlextResult patterns.

        Args:
            project_name: DBT project name
            profile_name: Profile name (optional)

        Returns:
            FlextResult containing Dict with DBT configuration or error

        """
        try:
            # Validate input using FlextUtilities
            safe_project_name = FlextUtilities.TextProcessor.safe_string(project_name)
            safe_profile_name = FlextUtilities.TextProcessor.safe_string(profile_name)

            config: ConfigDict = {
                "name": safe_project_name,
                "version": "1.0.0",
                "profile": safe_profile_name,
                "model-paths": ["models"],
                "analysis-paths": ["analysis"],
                "test-paths": ["tests"],
                "seed-paths": ["data"],
                "macro-paths": ["macros"],
                "snapshot-paths": ["snapshots"],
                "target-path": "target",
                "clean-targets": ["target", "dbt_packages"],
                "models": {safe_project_name: {"+materialized": "view"}},
                "metadata": {
                    "created_by": FlextMeltanoConstants.METADATA_CREATED_BY,  # SOURCE OF TRUTH
                    "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                    "entity_id": FlextUtilities.Generators.generate_id(),
                },
            }

            return FlextResult[ConfigDict].ok(data=config)
        except Exception as e:
            return FlextResult[ConfigDict].fail(f"Failed to create DBT config: {e}")

    # Singer Configuration Methods

    def _create_singer_config_generic(
        self,
        plugin_name: str,
        plugin_type: str = FlextMeltanoConstants.PluginTypes.EXTRACTORS.value,
        namespace: str = "",
        pip_url: str = "",
        executable: str = "",
    ) -> FlextResult[ConfigDict]:
        """Generic Singer plugin config creator using flext-core factories extensively.

        ZERO DUPLICATION: Uses flext-core configuration factory patterns
        with metadata templates and validation utilities.

        Args:
            plugin_name: Name of the plugin
            plugin_type: Type of plugin (extractors/loaders)
            namespace: Plugin namespace
            pip_url: Pip URL for installation
            executable: Executable name

        Returns:
            FlextResult containing plugin configuration dictionary

        """
        try:
            # Create type-specific configuration using flext-core patterns
            type_prefix = (
                FlextMeltanoConstants.PLUGIN_PREFIX_TAP
                if plugin_type == FlextMeltanoConstants.PluginTypes.EXTRACTORS.value
                else FlextMeltanoConstants.PLUGIN_PREFIX_TARGET
            )

            # Use flext-core text processing - EXTENSIVE REUSE
            safe_name = FlextUtilities.TextProcessor.safe_string(plugin_name)
            FlextUtilities.TextProcessor.safe_string(
                namespace or f"{type_prefix}_{safe_name.replace('-', '_')}",
            )
            FlextUtilities.TextProcessor.safe_string(executable)

            # Use flext-core configuration template - NO CUSTOM IMPLEMENTATION
            result_config: ConfigDict = {
                "name": "safe_name",
                "namespace": "safe_namespace",
                "executable": "safe_executable",
                "type": "plugin_type",
                "metadata": {
                    "created_by": FlextMeltanoConstants.METADATA_CREATED_BY,  # SOURCE OF TRUTH
                    "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                    "entity_id": FlextUtilities.Generators.generate_id(),
                },
            }

            # Smart pip_url using flext-core defaults factory
            if pip_url:
                result_config["pip_url"] = FlextUtilities.TextProcessor.safe_string(
                    pip_url,
                )
            else:
                prefix = (
                    "pipelinewise"
                    if plugin_type == FlextMeltanoConstants.PluginTypes.EXTRACTORS.value
                    else type_prefix
                )
                result_config["pip_url"] = f"{prefix}-{safe_name}"

            return FlextResult[ConfigDict].ok(data=result_config)
        except Exception as e:
            return FlextResult[ConfigDict].fail(
                f"Failed to create Singer {plugin_type} config: {e}",
            )

    def create_singer_tap_config(
        self,
        tap_name: str,
        namespace: str = "",
        pip_url: str = "",
        executable: str = "",
    ) -> FlextResult[ConfigDict]:
        """Creates tap configuration using generic factory pattern with object-based parameters.

        Returns:
            FlextResult[ConfigDict]: Configuration result with tap settings.

        """
        return self._create_singer_config_generic(
            plugin_name=tap_name,
            plugin_type=FlextMeltanoConstants.PluginTypes.EXTRACTORS.value,
            namespace=namespace,
            pip_url=pip_url,
            executable=executable,
        )

    def create_singer_target_config(
        self,
        target_name: str,
        namespace: str = "",
        pip_url: str = "",
        executable: str = "",
    ) -> FlextResult[ConfigDict]:
        """Creates target configuration using generic factory pattern with object-based parameters.

        Returns:
            FlextResult[ConfigDict]: Configuration result with target settings.

        """
        return self._create_singer_config_generic(
            plugin_name=target_name,
            plugin_type=FlextMeltanoConstants.PluginTypes.LOADERS.value,
            namespace=namespace,
            pip_url=pip_url,
            executable=executable,
        )

    # Plugin Configuration Methods

    def create_plugin_config(
        self,
        plugin_name: str,
        *,
        namespace: str = "",
        pip_url: str = "",
        executable: str = "",
        variant: str = FlextMeltanoConstants.PLUGIN_DEFAULT_VARIANT,
        config_defaults: ConfigDict | None = None,
    ) -> FlextResult[ConfigDict]:
        """Create complete plugin configuration for Meltano using FlextResult patterns.

        Args:
            plugin_name: Name of the plugin
            namespace: Plugin namespace
            pip_url: Pip URL for installation
            executable: Executable name
            variant: Plugin variant
            config_defaults: Default configuration (optional)

        Returns:
            FlextResult containing Dict with complete plugin configuration or error

        """
        try:
            # Use flext-core text processing extensively - NO CUSTOM LOGIC
            safe_name = FlextUtilities.TextProcessor.safe_string(plugin_name)
            FlextUtilities.TextProcessor.safe_string(
                namespace or safe_name,
            )
            FlextUtilities.TextProcessor.safe_string(pip_url)

            plugin_config: ConfigDict = {
                "name": "safe_name",
                "namespace": "safe_namespace",
                "pip_url": "safe_pip_url",
                # Use flext-core metadata template - ZERO DUPLICATION
                "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                "entity_id": FlextUtilities.Generators.generate_entity_id(),
            }

            if executable:
                plugin_config["executable"] = FlextUtilities.TextProcessor.safe_string(
                    executable,
                )

            if variant:
                plugin_config["variant"] = FlextUtilities.TextProcessor.safe_string(
                    variant,
                )

            if config_defaults:
                plugin_config["config"] = config_defaults

            return FlextResult[ConfigDict].ok(data=plugin_config)
        except Exception as e:
            return FlextResult[ConfigDict].fail(f"Failed to create plugin config: {e}")

    def create_extractor_config(
        self,
        tap_name: str,
        pip_url: str,
        config_defaults: ConfigDict | None = None,
    ) -> FlextResult[ConfigDict]:
        """Create specific configuration for extractors (taps) using FlextResult patterns.

        Args:
            tap_name: Tap name
            pip_url: Pip URL for installation
            config_defaults: Default tap configuration

        Returns:
            FlextResult containing Dict with extractor configuration or error

        """
        try:
            # Validate inputs using FlextUtilities
            safe_tap_name = FlextUtilities.TextProcessor.safe_string(tap_name)
            FlextUtilities.TextProcessor.safe_string(pip_url)

            config: ConfigDict = {
                "name": "safe_tap_name",
                "namespace": f"tap_{safe_tap_name.replace('-', '_')}",
                "pip_url": "safe_pip_url",
                "executable": "safe_tap_name",
                "config": config_defaults or {},
                "select": ["*.*"],  # Selecionar todas as tabelas por padrão
                "metadata": {
                    "created_by": FlextMeltanoConstants.METADATA_CREATED_BY,  # SOURCE OF TRUTH
                    "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                    "type": FlextMeltanoConstants.PluginTypes.EXTRACTORS.value,  # SOURCE OF TRUTH
                },
            }

            return FlextResult[ConfigDict].ok(data=config)
        except Exception as e:
            return FlextResult[ConfigDict].fail(
                f"Failed to create extractor config: {e}",
            )

    def create_loader_config(
        self,
        target_name: str,
        pip_url: str,
        config_defaults: ConfigDict | None = None,
    ) -> FlextResult[ConfigDict]:
        """Create specific configuration for loaders (targets) using FlextResult patterns.

        Args:
            target_name: Target name
            pip_url: Pip URL for installation
            config_defaults: Default target configuration

        Returns:
            FlextResult containing Dict with loader configuration or error

        """
        try:
            # Validate inputs using FlextUtilities
            safe_target_name = FlextUtilities.TextProcessor.safe_string(target_name)
            FlextUtilities.TextProcessor.safe_string(pip_url)

            config: ConfigDict = {
                "name": "safe_target_name",
                "namespace": f"target_{safe_target_name.replace('-', '_')}",
                "pip_url": "safe_pip_url",
                "executable": "safe_target_name",
                "config": config_defaults or {},
                "metadata": {
                    "created_by": FlextMeltanoConstants.METADATA_CREATED_BY,  # SOURCE OF TRUTH
                    "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                    "type": FlextMeltanoConstants.PluginTypes.LOADERS.value,  # SOURCE OF TRUTH
                },
            }

            return FlextResult[ConfigDict].ok(data=config)
        except Exception as e:
            return FlextResult[ConfigDict].fail(f"Failed to create loader config: {e}")

    # Meltano Configuration Methods

    def create_meltano_config(
        self,
        project_id: str,
        project_name: str = "",
    ) -> FlextResult[ConfigDict]:
        """Create complete Meltano configuration - ZERO DUPLICATION using flext-core.

        Args:
            project_id: Project ID
            project_name: Project name (optional)

        Returns:
            FlextResult[ConfigDict]: Complete Meltano configuration

        """
        try:
            # Use flext-core utilities directly
            FlextUtilities.TextProcessor.safe_string(project_id)
            FlextUtilities.TextProcessor.safe_string(project_name)

            # DOMAIN-SPECIFIC: Meltano configuration structure
            config_dict: ConfigDict = {
                "version": 1,
                "project_id": "safe_project_id",
                "project_name": "safe_project_name",
                "environments": [
                    {"name": "env"}
                    for env in FlextMeltanoConstants.METADATA_DEFAULT_ENVIRONMENTS
                ],
                "plugins": {
                    "extractors": [],
                    "loaders": [],
                    "transformers": [],
                    "orchestrators": [],
                },
                "metadata": {
                    "created_by": FlextMeltanoConstants.METADATA_CREATED_BY,
                    "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                    "flext_version": FlextMeltanoConstants.FLEXT_MELTANO_VERSION,
                },
            }
            return FlextResult[ConfigDict].ok(data=config_dict)
        except Exception as e:
            return FlextResult[ConfigDict].fail(f"Failed to create Meltano config: {e}")

    def add_plugin_to_config(
        self,
        meltano_config: ConfigDict,
        plugin_type: str,
        plugin_config: ConfigDict,
    ) -> FlextResult[ConfigDict]:
        """Add plugin to Meltano configuration using FlextResult patterns.

        Args:
            meltano_config: Existing Meltano configuration
            plugin_type: Plugin type (extractors, loaders, etc.)
            plugin_config: Plugin configuration

        Returns:
            FlextResult containing updated Meltano configuration or error

        """
        try:
            # Validate inputs using FlextUtilities
            safe_plugin_type = FlextUtilities.TextProcessor.safe_string(plugin_type)

            # Validate plugin type
            valid_types = ["extractors", "loaders", "transformers", "orchestrators"]
            if safe_plugin_type not in valid_types:
                return FlextResult[ConfigDict].fail(
                    f"Invalid plugin type: {safe_plugin_type}. "
                    f"Valid types: {valid_types}",
                )

            # Create copy to avoid mutation
            updated_config: dict[str, object] = dict(meltano_config)
            plugins: dict[str, object] = updated_config.setdefault("plugins", {})

            if isinstance(plugins, dict):
                typed_plugins = plugins
                if safe_plugin_type not in typed_plugins:
                    typed_plugins[safe_plugin_type] = []
                plugin_list = typed_plugins[safe_plugin_type]
                if isinstance(plugin_list, list):
                    plugin_list_copy: list[object] = list(
                        plugin_list
                    )  # Create mutable copy
                    plugin_list_copy.append(plugin_config)
                    typed_plugins[safe_plugin_type] = plugin_list_copy

            # Add metadata about the operation
            metadata: dict[str, object] = updated_config.get("metadata", {})
            if isinstance(metadata, dict):
                metadata_copy: dict[str, object] = dict(metadata)
                metadata_copy["last_plugin_added"] = {
                    "type": "safe_plugin_type",
                    "name": plugin_config.get("name", "unknown"),
                    "added_at": FlextUtilities.Generators.generate_iso_timestamp(),
                }
                updated_config["metadata"] = metadata_copy

            return FlextResult[ConfigDict].ok(data=updated_config)
        except Exception as e:
            return FlextResult[ConfigDict].fail(f"Failed to add plugin to config: {e}")

    # =================================================================
    # BACKWARD COMPATIBILITY - Methods now directly available
    # =================================================================

    # All methods are now direct methods of the unified class
    # No aliases needed - methods are directly accessible as:
    # - self.create_dbt_config()
    # - self.create_singer_tap_config()
    # - self.create_singer_target_config()
    # - self.create_plugin_config()
    # - self.create_extractor_config()
    # - self.create_loader_config()
    # - self.create_meltano_config()
    # - self.add_plugin_to_config()


__all__ = [
    "FlextMeltanoConfigBuilders",
]
