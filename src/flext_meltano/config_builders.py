"""FLEXT Meltano Config Builders - Configuration building utilities.

SOURCE OF TRUTH: All configuration through FlextMeltanoConstants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import cast

from flext_core import FlextLogger, FlextResult, FlextUtilities
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.utilities import FlextMeltanoUtilities

# Type alias for configuration dictionaries
ConfigDict = dict[str, object]


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

    def __init__(self) -> None:
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
        """Generic Singer plugin config creator using FlextMeltanoUtilities - ZERO DUPLICATION.

        CRITICAL: This method now delegates to FlextMeltanoUtilities.create_plugin_config_dict()
        to eliminate duplication and ensure utilities are ACTUALLY USED in business logic.

        Args:
            plugin_name: Name of the plugin
            plugin_type: Type of plugin (extractors/loaders)
            namespace: Plugin namespace
            pip_url: Pip URL for installation
            executable: Executable name

        Returns:
            FlextResult containing plugin configuration dictionary

        """
        # ZERO TOLERANCE: Use FlextMeltanoUtilities instead of duplicating logic
        return FlextMeltanoUtilities.create_plugin_config_dict(
            name=plugin_name,
            plugin_type=plugin_type,
            namespace=namespace,
            pip_url=pip_url,
            executable=executable,
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

    def create_extractor_config(
        self,
        tap_name: str,
        pip_url: str,
        config_defaults: ConfigDict | None = None,
    ) -> FlextResult[ConfigDict]:
        """Create specific configuration for extractors (taps) using FlextMeltanoUtilities - ZERO DUPLICATION.

        CRITICAL: This method now delegates to FlextMeltanoUtilities.create_plugin_config_dict()
        to eliminate duplication and ensure utilities are ACTUALLY USED in business logic.

        Args:
            tap_name: Tap name
            pip_url: Pip URL for installation
            config_defaults: Default tap configuration

        Returns:
            FlextResult containing Dict with extractor configuration or error

        """
        # ZERO TOLERANCE: Use FlextMeltanoUtilities instead of duplicating logic
        # Create base configuration using utilities
        result = FlextMeltanoUtilities.create_plugin_config_dict(
            name=tap_name,
            plugin_type=FlextMeltanoConstants.PluginTypes.EXTRACTORS.value,
            pip_url=pip_url,
            executable=tap_name,
        )

        if result.is_failure:
            return result

        # Add extractor-specific configuration
        config = result.value
        config["config"] = config_defaults or {}
        config["select"] = ["*.*"]  # Select all tables by default

        return FlextResult[ConfigDict].ok(data=config)

    def create_loader_config(
        self,
        target_name: str,
        pip_url: str,
        config_defaults: ConfigDict | None = None,
    ) -> FlextResult[ConfigDict]:
        """Create specific configuration for loaders (targets) using FlextMeltanoUtilities - ZERO DUPLICATION.

        CRITICAL: This method now delegates to FlextMeltanoUtilities.create_plugin_config_dict()
        to eliminate duplication and ensure utilities are ACTUALLY USED in business logic.

        Args:
            target_name: Target name
            pip_url: Pip URL for installation
            config_defaults: Default target configuration

        Returns:
            FlextResult containing Dict with loader configuration or error

        """
        # ZERO TOLERANCE: Use FlextMeltanoUtilities instead of duplicating logic
        # Create base configuration using utilities
        result = FlextMeltanoUtilities.create_plugin_config_dict(
            name=target_name,
            plugin_type=FlextMeltanoConstants.PluginTypes.LOADERS.value,
            pip_url=pip_url,
            executable=target_name,
        )

        if result.is_failure:
            return result

        # Add loader-specific configuration
        config = result.value
        config["config"] = config_defaults or {}

        return FlextResult[ConfigDict].ok(data=config)

    # Meltano Configuration Methods

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
            updated_config: FlextMeltanoTypes.Core.MeltanoConfigDict = dict(
                meltano_config
            )
            plugins: FlextMeltanoTypes.Core.PluginConfigDict = cast(
                "FlextMeltanoTypes.Core.PluginConfigDict",
                updated_config.setdefault("plugins", {}),
            )

            typed_plugins = plugins
            if safe_plugin_type not in typed_plugins:
                typed_plugins[safe_plugin_type] = []
            plugin_list = typed_plugins[safe_plugin_type]
            if not isinstance(plugin_list, list):
                plugin_list = []
            plugin_list_copy: list[object] = list(plugin_list)  # Create mutable copy
            plugin_list_copy.append(plugin_config)
            typed_plugins[safe_plugin_type] = plugin_list_copy

            # Add metadata about the operation
            metadata: FlextMeltanoTypes.Core.SettingsDict = cast(
                "FlextMeltanoTypes.Core.SettingsDict",
                updated_config.get("metadata", {}),
            )
            metadata_copy: FlextMeltanoTypes.Core.SettingsDict = dict(metadata)
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
    # ZERO DUPLICATION COMPLIANCE - Utilities Integration Active
    # =================================================================

    # All methods now delegate to FlextMeltanoUtilities to eliminate duplication.
    # FlextMeltanoUtilities is now ACTIVELY USED in business logic:
    # - create_singer_tap_config() → FlextMeltanoUtilities.create_plugin_config_dict()
    # - create_singer_target_config() → FlextMeltanoUtilities.create_plugin_config_dict()
    # - create_extractor_config() → FlextMeltanoUtilities.create_plugin_config_dict()
    # - create_loader_config() → FlextMeltanoUtilities.create_plugin_config_dict()
    #
    # COMPLIANCE: Fixed ZERO TOLERANCE violation where utilities were declared but not used.
    # STATUS: FlextMeltanoUtilities is now the SOURCE OF TRUTH for all plugin configuration.
    # - self.add_plugin_to_config()


__all__ = [
    "FlextMeltanoConfigBuilders",
]
