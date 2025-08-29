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

from flext_core import FlextLogger, FlextUtilities

from flext_meltano.flext_types import ConfigDict

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
        def create_dbt_config(project_name: str, profile_name: str = "") -> ConfigDict:
            """Cria configuração básica do DBT.

            Args:
                project_name: Nome do projeto DBT
                profile_name: Nome do profile (opcional)

            Returns:
                Dict com configuração do DBT

            """
            return {
                "name": project_name,
                "version": "1.0.0",
                "profile": profile_name or project_name,
                "model-paths": ["models"],
                "analysis-paths": ["analysis"],
                "test-paths": ["tests"],
                "seed-paths": ["data"],
                "macro-paths": ["macros"],
                "snapshot-paths": ["snapshots"],
                "target-path": "target",
                "clean-targets": ["target", "dbt_packages"],
                "models": {project_name: {"+materialized": "view"}},
            }

    class SingerConfigBuilder:
        """Single responsibility: Singer configuration building only."""

        @staticmethod
        def create_singer_tap_config(
            tap_name: str, namespace: str = "", pip_url: str = "", executable: str = ""
        ) -> ConfigDict:
            """Cria configuração para Singer tap.

            Args:
                tap_name: Nome do tap
                namespace: Namespace do tap
                pip_url: URL do pip para instalação
                executable: Nome do executável

            Returns:
                Dict com configuração do tap

            """
            config: ConfigDict = {
                "name": tap_name,
                "namespace": namespace or "tap_" + tap_name.replace("-", "_"),
                "executable": executable or tap_name,
            }

            if pip_url:
                config["pip_url"] = pip_url
            else:
                # Default pip_url para taps conhecidos
                config["pip_url"] = f"pipelinewise-{tap_name}"

            return config

        @staticmethod
        def create_singer_target_config(
            target_name: str,
            namespace: str = "",
            pip_url: str = "",
            executable: str = "",
        ) -> ConfigDict:
            """Cria configuração para Singer target.

            Args:
                target_name: Nome do target
                namespace: Namespace do target
                pip_url: URL do pip para instalação
                executable: Nome do executável

            Returns:
                Dict com configuração do target

            """
            config: ConfigDict = {
                "name": target_name,
                "namespace": namespace or "target_" + target_name.replace("-", "_"),
                "executable": executable or target_name,
            }

            if pip_url:
                config["pip_url"] = pip_url
            else:
                # Default pip_url para targets conhecidos
                config["pip_url"] = f"pipelinewise-{target_name}"

            return config

    class PluginConfigBuilder:
        """Single responsibility: Meltano plugin configuration building only."""

        @staticmethod
        def create_plugin_config(
            name: str,
            namespace: str,
            pip_url: str,
            executable: str = "",
            variant: str = "",
            config_defaults: ConfigDict | None = None,
        ) -> ConfigDict:
            """Cria configuração completa para plugin Meltano.

            Args:
                name: Nome do plugin
                namespace: Namespace do plugin
                pip_url: URL do pip ou git para instalação
                executable: Nome do executável (opcional)
                variant: Variant do plugin (opcional)
                config_defaults: Configurações padrão (opcional)

            Returns:
                Dict com configuração completa do plugin

            """
            plugin_config: ConfigDict = {
                "name": name,
                "namespace": namespace,
                "pip_url": pip_url,
            }

            if executable:
                plugin_config["executable"] = executable

            if variant:
                plugin_config["variant"] = variant

            if config_defaults:
                plugin_config["config"] = config_defaults

            return plugin_config

        @staticmethod
        def create_extractor_config(
            tap_name: str,
            pip_url: str,
            config_defaults: ConfigDict | None = None,
        ) -> ConfigDict:
            """Cria configuração específica para extractors (taps).

            Args:
                tap_name: Nome do tap
                pip_url: URL do pip para instalação
                config_defaults: Configurações padrão do tap

            Returns:
                Dict com configuração do extractor

            """
            return {
                "name": tap_name,
                "namespace": f"tap_{tap_name.replace('-', '_')}",
                "pip_url": pip_url,
                "executable": tap_name,
                "config": config_defaults or {},
                "select": ["*.*"],  # Selecionar todas as tabelas por padrão
            }

        @staticmethod
        def create_loader_config(
            target_name: str,
            pip_url: str,
            config_defaults: ConfigDict | None = None,
        ) -> ConfigDict:
            """Cria configuração específica para loaders (targets).

            Args:
                target_name: Nome do target
                pip_url: URL do pip para instalação
                config_defaults: Configurações padrão do target

            Returns:
                Dict com configuração do loader

            """
            return {
                "name": target_name,
                "namespace": f"target_{target_name.replace('-', '_')}",
                "pip_url": pip_url,
                "executable": target_name,
                "config": config_defaults or {},
            }

    class MeltanoConfigBuilder:
        """Single responsibility: Complete Meltano project configuration building."""

        @staticmethod
        def create_meltano_config(
            project_id: str, project_name: str = ""
        ) -> ConfigDict:
            """Create complete Meltano configuration with real structure.

            Args:
                project_id: Project ID
                project_name: Project name (optional)

            Returns:
                Dict with complete Meltano configuration

            """
            return {
                "version": 1,
                "project_id": project_id,
                "project_name": project_name or project_id,
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
            }

        @staticmethod
        def add_plugin_to_config(
            meltano_config: ConfigDict,
            plugin_type: str,
            plugin_config: ConfigDict,
        ) -> ConfigDict:
            """Adiciona plugin à configuração Meltano.

            Args:
                meltano_config: Configuração Meltano existente
                plugin_type: Tipo do plugin (extractors, loaders, etc.)
                plugin_config: Configuração do plugin

            Returns:
                Configuração Meltano atualizada

            """
            # Create copy to avoid mutation
            updated_config = meltano_config.copy()
            plugins = updated_config.setdefault("plugins", {})

            if FlextUtilities.is_dict(plugins):
                typed_plugins = cast("dict[str, object]", plugins)
                if plugin_type not in typed_plugins:
                    typed_plugins[plugin_type] = []
                plugin_list = typed_plugins[plugin_type]
                if FlextUtilities.is_list(plugin_list):
                    typed_list = cast("list[object]", plugin_list)
                    plugin_list_copy = list(typed_list)  # Create mutable copy
                    plugin_list_copy.append(plugin_config)
                    typed_plugins[plugin_type] = plugin_list_copy

            return updated_config

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
