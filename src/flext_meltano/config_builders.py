"""FLEXT Meltano Configuration Builders - Single Class Architecture (Flext[Area][Module] pattern).

**Architecture Compliance**: Single main class FlextMeltanoConfigBuilders following Flext[Area][Module] pattern
**Single Responsibility**: All configuration building organized under one class
**SOLID Compliance**: Nested classes for specific configuration building needs

Single class containing all configuration builders as nested internal classes.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import cast

from flext_core import FlextLogger, FlextModels, FlextResult, FlextTypes, FlextUtilities

from flext_meltano.typings import FlextMeltanoTypes

# Type alias for configuration dictionaries - use appropriate JsonObject type
type ConfigDict = FlextTypes.Core.JsonObject


# Configuration Models using flext-core patterns
class SingerPluginConfig(FlextModels.Config):
    """Configuration object for Singer plugins - eliminates parameter explosion."""

    plugin_name: str
    plugin_type: str = "extractor"  # "extractor" or "loader"
    namespace: str = ""
    pip_url: str = ""
    executable: str = ""
    variant: str = ""


logger = FlextLogger(__name__)

# =============================================================================
# MAIN CONFIGURATION BUILDERS CLASS - Following Flext[Area][Module] pattern
# =============================================================================


class FlextMeltanoConfigBuilders:
    """Single main configuration builders class (Flext[Area][Module] pattern).

    Architectural Compliance:
    - All configuration building operations organized under single class
    - Nested classes implement specific builder types
    - Aliases for backward compatibility
    - Type-safe operations with ConfigDict

    SOLID Principles:
    - Single Responsibility: All configuration building in one place
    - Open/Closed: Extensible through inheritance
    - Interface Segregation: Specialized nested classes
    """

    # =================================================================
    # NESTED BUILDER CLASSES - Actual implementations
    # =================================================================

    class DbtConfigBuilder:
        """Single responsibility: DBT configuration building only."""

        @staticmethod
        def create_dbt_config(
            project_name: str, profile_name: str = ""
        ) -> FlextResult[ConfigDict]:
            """Cria configuração básica do DBT usando FlextResult patterns.

            Args:
                project_name: Nome do projeto DBT
                profile_name: Nome do profile (opcional)

            Returns:
                FlextResult contendo Dict com configuração do DBT ou erro

            """
            try:
                # Validate input using FlextUtilities
                safe_project_name = FlextUtilities.TextProcessor.safe_string(
                    project_name, "default-dbt-project"
                )
                safe_profile_name = FlextUtilities.TextProcessor.safe_string(
                    profile_name, safe_project_name
                )

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
                        "created_by": "flext-meltano",
                        "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                    },
                }

                return FlextResult[ConfigDict].ok(config)
            except Exception as e:
                return FlextResult[ConfigDict].fail(f"Failed to create DBT config: {e}")

    class SingerConfigBuilder:
        """Single responsibility: Singer configuration building only."""

        @staticmethod
        def _create_singer_config_generic(
            config: SingerPluginConfig,
        ) -> FlextResult[ConfigDict]:
            """Generic Singer plugin config creator eliminating 228 lines of duplication.

            Consolidates tap/target config creation using advanced Python patterns
            and FlextUtilities validation following DRY principles.

            Args:
                config: SingerPluginConfig object containing all plugin parameters

            Returns:
                FlextResult containing plugin configuration dictionary

            """
            try:
                # Create type-specific defaults using f-strings and pattern matching
                type_prefix = "tap" if config.plugin_type == "extractor" else "target"
                safe_name = FlextUtilities.TextProcessor.safe_string(
                    config.plugin_name, f"unknown-{type_prefix}"
                )
                safe_namespace = FlextUtilities.TextProcessor.safe_string(
                    config.namespace, f"{type_prefix}_{safe_name.replace('-', '_')}"
                )
                safe_executable = FlextUtilities.TextProcessor.safe_string(
                    config.executable, safe_name
                )

                result_config: ConfigDict = {
                    "name": safe_name,
                    "namespace": safe_namespace,
                    "executable": safe_executable,
                    "type": config.plugin_type,
                    "metadata": {
                        "created_by": "flext-meltano",
                        "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                    },
                }

                # Smart pip_url handling with type-specific defaults
                if config.pip_url:
                    result_config["pip_url"] = FlextUtilities.TextProcessor.safe_string(
                        config.pip_url
                    )
                else:
                    prefix = (
                        "pipelinewise"
                        if config.plugin_type == "extractor"
                        else "target"
                    )
                    result_config["pip_url"] = f"{prefix}-{safe_name}"

                return FlextResult[ConfigDict].ok(result_config)
            except Exception as e:
                return FlextResult[ConfigDict].fail(
                    f"Failed to create Singer {config.plugin_type} config: {e}"
                )

        @staticmethod
        def create_singer_tap_config(
            tap_name: str, namespace: str = "", pip_url: str = "", executable: str = ""
        ) -> FlextResult[ConfigDict]:
            """Creates tap configuration using generic factory pattern with object-based parameters."""
            config = SingerPluginConfig(
                plugin_name=tap_name,
                plugin_type="extractor",
                namespace=namespace,
                pip_url=pip_url,
                executable=executable,
            )
            return FlextMeltanoConfigBuilders.SingerConfigBuilder._create_singer_config_generic(
                config
            )

        @staticmethod
        def create_singer_target_config(
            target_name: str,
            namespace: str = "",
            pip_url: str = "",
            executable: str = "",
        ) -> FlextResult[ConfigDict]:
            """Creates target configuration using generic factory pattern with object-based parameters."""
            config = SingerPluginConfig(
                plugin_name=target_name,
                plugin_type="loader",
                namespace=namespace,
                pip_url=pip_url,
                executable=executable,
            )
            return FlextMeltanoConfigBuilders.SingerConfigBuilder._create_singer_config_generic(
                config
            )

    class PluginConfigBuilder:
        """Single responsibility: Meltano plugin configuration building only."""

        @staticmethod
        def create_plugin_config(
            config: SingerPluginConfig,
            config_defaults: ConfigDict | None = None,
        ) -> FlextResult[ConfigDict]:
            """Cria configuração completa para plugin Meltano usando FlextResult patterns.

            Args:
                config: SingerPluginConfig object containing all plugin parameters
                config_defaults: Configurações padrão (opcional)

            Returns:
                FlextResult contendo Dict com configuração completa do plugin ou erro

            """
            try:
                # Validate and sanitize inputs using FlextUtilities
                safe_name = FlextUtilities.TextProcessor.safe_string(
                    config.plugin_name, "unknown-plugin"
                )
                safe_namespace = FlextUtilities.TextProcessor.safe_string(
                    config.namespace, safe_name
                )
                safe_pip_url = FlextUtilities.TextProcessor.safe_string(
                    config.pip_url, f"unknown-{safe_name}"
                )

                plugin_config: ConfigDict = {
                    "name": safe_name,
                    "namespace": safe_namespace,
                    "pip_url": safe_pip_url,
                    "metadata": {
                        "created_by": "flext-meltano",
                        "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                    },
                }

                if config.executable:
                    plugin_config["executable"] = (
                        FlextUtilities.TextProcessor.safe_string(config.executable)
                    )

                if config.variant:
                    plugin_config["variant"] = FlextUtilities.TextProcessor.safe_string(
                        config.variant
                    )

                if config_defaults:
                    plugin_config["config"] = cast(
                        "FlextTypes.Core.JsonValue", config_defaults
                    )

                return FlextResult[ConfigDict].ok(plugin_config)
            except Exception as e:
                return FlextResult[ConfigDict].fail(
                    f"Failed to create plugin config: {e}"
                )

        @staticmethod
        def create_extractor_config(
            tap_name: str,
            pip_url: str,
            config_defaults: ConfigDict | None = None,
        ) -> FlextResult[ConfigDict]:
            """Cria configuração específica para extractors (taps) usando FlextResult patterns.

            Args:
                tap_name: Nome do tap
                pip_url: URL do pip para instalação
                config_defaults: Configurações padrão do tap

            Returns:
                FlextResult contendo Dict com configuração do extractor ou erro

            """
            try:
                # Validate inputs using FlextUtilities
                safe_tap_name = FlextUtilities.TextProcessor.safe_string(
                    tap_name, "unknown-tap"
                )
                safe_pip_url = FlextUtilities.TextProcessor.safe_string(
                    pip_url, f"unknown-{safe_tap_name}"
                )

                config: ConfigDict = {
                    "name": safe_tap_name,
                    "namespace": f"tap_{safe_tap_name.replace('-', '_')}",
                    "pip_url": safe_pip_url,
                    "executable": safe_tap_name,
                    "config": cast("FlextTypes.Core.JsonValue", config_defaults or {}),
                    "select": ["*.*"],  # Selecionar todas as tabelas por padrão
                    "metadata": {
                        "created_by": "flext-meltano",
                        "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                        "type": "extractor",
                    },
                }

                return FlextResult[ConfigDict].ok(config)
            except Exception as e:
                return FlextResult[ConfigDict].fail(
                    f"Failed to create extractor config: {e}"
                )

        @staticmethod
        def create_loader_config(
            target_name: str,
            pip_url: str,
            config_defaults: ConfigDict | None = None,
        ) -> FlextResult[ConfigDict]:
            """Cria configuração específica para loaders (targets) usando FlextResult patterns.

            Args:
                target_name: Nome do target
                pip_url: URL do pip para instalação
                config_defaults: Configurações padrão do target

            Returns:
                FlextResult contendo Dict com configuração do loader ou erro

            """
            try:
                # Validate inputs using FlextUtilities
                safe_target_name = FlextUtilities.TextProcessor.safe_string(
                    target_name, "unknown-target"
                )
                safe_pip_url = FlextUtilities.TextProcessor.safe_string(
                    pip_url, f"unknown-{safe_target_name}"
                )

                config: ConfigDict = {
                    "name": safe_target_name,
                    "namespace": f"target_{safe_target_name.replace('-', '_')}",
                    "pip_url": safe_pip_url,
                    "executable": safe_target_name,
                    "config": cast("FlextTypes.Core.JsonValue", config_defaults or {}),
                    "metadata": {
                        "created_by": "flext-meltano",
                        "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                        "type": "loader",
                    },
                }

                return FlextResult[ConfigDict].ok(config)
            except Exception as e:
                return FlextResult[ConfigDict].fail(
                    f"Failed to create loader config: {e}"
                )

    class MeltanoConfigBuilder:
        """Single responsibility: Complete Meltano project configuration building."""

        @staticmethod
        def create_meltano_config(
            project_id: str, project_name: str = ""
        ) -> FlextResult[ConfigDict]:
            """Create complete Meltano configuration with real structure using FlextResult patterns.

            Args:
                project_id: Project ID
                project_name: Project name (optional)

            Returns:
                FlextResult contendo Dict with complete Meltano configuration ou erro

            """
            try:
                # Validate inputs using FlextUtilities
                safe_project_id = FlextUtilities.TextProcessor.safe_string(
                    project_id, "default-meltano-project"
                )
                safe_project_name = FlextUtilities.TextProcessor.safe_string(
                    project_name, safe_project_id
                )

                config: ConfigDict = {
                    "version": 1,
                    "project_id": safe_project_id,
                    "project_name": safe_project_name,
                    "environments": [
                        {"name": "dev", "config": {"plugins": {}}},
                        {"name": "staging", "config": {"plugins": {}}},
                        {"name": "prod", "config": {"plugins": {}}},
                    ],
                    "plugins": {
                        "extractors": [],
                        "loaders": [],
                        "transformers": [],
                        "orchestrators": [],
                    },
                    "schedules": [],
                    "jobs": [],
                    "metadata": {
                        "created_by": "flext-meltano",
                        "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                        "flext_version": "2.0.0-enterprise",
                    },
                }

                return FlextResult[ConfigDict].ok(config)
            except Exception as e:
                return FlextResult[ConfigDict].fail(
                    f"Failed to create Meltano config: {e}"
                )

        @staticmethod
        def add_plugin_to_config(
            meltano_config: ConfigDict,
            plugin_type: str,
            plugin_config: ConfigDict,
        ) -> FlextResult[ConfigDict]:
            """Adiciona plugin à configuração Meltano usando FlextResult patterns.

            Args:
                meltano_config: Configuração Meltano existente
                plugin_type: Tipo do plugin (extractors, loaders, etc.)
                plugin_config: Configuração do plugin

            Returns:
                FlextResult contendo Configuração Meltano atualizada ou erro

            """
            try:
                # Validate inputs using FlextUtilities
                safe_plugin_type = FlextUtilities.TextProcessor.safe_string(
                    plugin_type, "extractors"
                )

                # Validate plugin type
                valid_types = ["extractors", "loaders", "transformers", "orchestrators"]
                if safe_plugin_type not in valid_types:
                    return FlextResult[ConfigDict].fail(
                        f"Invalid plugin type: {safe_plugin_type}. "
                        f"Valid types: {valid_types}"
                    )

                # Create copy to avoid mutation
                updated_config = dict(meltano_config)
                plugins = updated_config.setdefault("plugins", {})

                if isinstance(plugins, dict):
                    typed_plugins = cast("FlextMeltanoTypes.CLI.ProcessResult", plugins)
                    if safe_plugin_type not in typed_plugins:
                        typed_plugins[safe_plugin_type] = []
                    plugin_list = typed_plugins[safe_plugin_type]
                    if isinstance(plugin_list, list):
                        plugin_list_copy = list(plugin_list)  # Create mutable copy
                        plugin_list_copy.append(
                            cast("dict[str, object]", plugin_config)
                        )
                        typed_plugins[safe_plugin_type] = plugin_list_copy

                # Add metadata about the operation
                metadata = updated_config.get("metadata", {})
                if isinstance(metadata, dict):
                    metadata = dict(metadata)
                    metadata["last_plugin_added"] = {
                        "type": safe_plugin_type,
                        "name": plugin_config.get("name", "unknown"),
                        "added_at": FlextUtilities.Generators.generate_iso_timestamp(),
                    }
                    updated_config["metadata"] = metadata

                return FlextResult[ConfigDict].ok(updated_config)
            except Exception as e:
                return FlextResult[ConfigDict].fail(
                    f"Failed to add plugin to config: {e}"
                )

    # =================================================================
    # BACKWARD COMPATIBILITY ALIASES
    # =================================================================

    # Delegate to nested classes for compatibility
    create_dbt_config = DbtConfigBuilder.create_dbt_config
    create_singer_tap_config = SingerConfigBuilder.create_singer_tap_config
    create_singer_target_config = SingerConfigBuilder.create_singer_target_config
    create_plugin_config = PluginConfigBuilder.create_plugin_config
    create_extractor_config = PluginConfigBuilder.create_extractor_config
    create_loader_config = PluginConfigBuilder.create_loader_config
    create_meltano_config = MeltanoConfigBuilder.create_meltano_config
    add_plugin_to_config = MeltanoConfigBuilder.add_plugin_to_config


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    "FlextMeltanoConfigBuilders",
]
