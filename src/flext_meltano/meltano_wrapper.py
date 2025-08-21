"""Meltano Core Bridge - Adapta Meltano Core para padrões flext-core.

FUNÇÃO 1: Wrapper para Meltano Core adaptando para flext-core
- MeltanoBridge: Bridge principal
- FlextMeltanoAdapter: Adaptador de tipos
- Real Meltano Core integration (NO MOCKS)
"""

from __future__ import annotations

import os
import tempfile
import yaml
from pathlib import Path
from typing import Any

import click.testing
from flext_core import FlextDomainService, FlextResult, get_logger
from meltano.cli import cli

# Importar Meltano Core REAL - bibliotecas instaladas
from meltano.core.hub import MeltanoHubService
from meltano.core.project import Project
from meltano.core.plugin.base import PluginType
from meltano.core.plugin_install_service import PluginInstallService
from meltano.core.project_plugins_service import ProjectPluginsService

MELTANO_AVAILABLE = True

logger = get_logger(__name__)

# =============================================================================
# MELTANO CORE BRIDGE - REAL IMPLEMENTATION
# =============================================================================


class MeltanoBridge(FlextDomainService):
    """Bridge principal para Meltano Core → flext-core.

    Adapta Meltano Core operations para flext-core patterns, usando FlextResult
    para error handling e integrando com flext-core observability.
    """

    def __init__(self) -> None:
        super().__init__()

    def _create_temp_project(self) -> Project:
        """Cria um projeto Meltano temporário para usar HubService.
        
        Returns:
            Project instance válido
        """
        # Criar diretório temporário (será limpo automaticamente)  
        temp_dir = tempfile.mkdtemp(prefix="flext_meltano_")
        temp_path = Path(temp_dir)
        
        # Criar meltano.yml mínimo
        meltano_config = {
            'version': 1,
            'project_id': 'flext-temp-project', 
            'environments': [
                {'name': 'dev'}
            ]
        }
        
        meltano_file = temp_path / 'meltano.yml'
        with meltano_file.open('w') as f:
            yaml.dump(meltano_config, f)
        
        return Project(root=temp_path)

        # Validar disponibilidade do Meltano
        if not MELTANO_AVAILABLE:
            logger.warning("Meltano Core not available - some functions will fail")

    @property
    def logger(self) -> object:
        """Get logger instance."""
        return get_logger(self.__class__.__name__)

    def execute(self) -> FlextResult[dict[str, Any]]:
        """Execute Meltano bridge operation (required by FlextDomainService).

        Returns:
            FlextResult contendo informações do serviço

        """
        return FlextResult.ok(
            {
                "service": "MeltanoBridge",
                "status": "ready",
                "meltano_available": MELTANO_AVAILABLE,
                "capabilities": [
                    "initialize_project",
                    "discover_plugins",
                    "install_plugin",
                    "list_installed_plugins",
                    "run_meltano_command",
                ],
            }
        )

    def initialize_project(self, project_root: Path) -> FlextResult[Project]:
        """Inicializa projeto Meltano usando API nativa.

        Args:
            project_root: Diretório raiz do projeto Meltano

        Returns:
            FlextResult contendo Project instance ou erro

        """
        try:
            self.logger.info(
                "Initializing Meltano project", project_root=str(project_root)
            )

            # Verificar se diretório existe
            if not project_root.exists():
                return FlextResult.fail(f"Project directory not found: {project_root}")

            # Verificar se é um projeto Meltano válido
            meltano_yml = project_root / "meltano.yml"
            if not meltano_yml.exists():
                return FlextResult.fail(
                    f"Not a Meltano project: meltano.yml not found in {project_root}"
                )

            # Usar API nativa Meltano para carregar projeto
            project = Project.find(project_root)

            if project is None:
                return FlextResult.fail(
                    f"Failed to load Meltano project from {project_root}"
                )

            self.logger.info(
                "Meltano project initialized successfully", project_name=project.name
            )
            return FlextResult.ok(project)

        except Exception as e:
            error_msg = f"Failed to initialize Meltano project: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def discover_plugins(
        self, _project: Project | None = None
    ) -> FlextResult[list[dict[str, Any]]]:
        """Descobre plugins do hub usando API nativa Meltano.

        Args:
            project: Instância Project do Meltano (opcional)

        Returns:
            FlextResult contendo lista de plugins descobertos

        """
        try:
            self.logger.info("Discovering Meltano plugins")

            # Usar API nativa do Meltano Hub (precisa de Project)
            project = self._create_temp_project()
            hub_service = MeltanoHubService(project=project)

            plugins = []

            # Descobrir extractors usando API nativa
            extractors_dict = hub_service.get_plugins_of_type(PluginType.EXTRACTORS)
            for plugin_name, indexed_plugin in list(extractors_dict.items())[:10]:  # Limitar para performance
                plugin_info = {
                    "name": indexed_plugin.name,
                    "type": "extractor",
                    "default_variant": indexed_plugin.default_variant,
                    "variants": list(indexed_plugin.variants.keys()) if indexed_plugin.variants else [],
                    "logo_url": getattr(indexed_plugin, "logo_url", ""),
                }
                plugins.append(plugin_info)

            # Descobrir loaders usando API nativa
            loaders_dict = hub_service.get_plugins_of_type(PluginType.LOADERS)
            for plugin_name, indexed_plugin in list(loaders_dict.items())[:5]:  # Limitar para performance
                plugin_info = {
                    "name": indexed_plugin.name,
                    "type": "loader",
                    "default_variant": indexed_plugin.default_variant,
                    "variants": list(indexed_plugin.variants.keys()) if indexed_plugin.variants else [],
                    "logo_url": getattr(indexed_plugin, "logo_url", ""),
                }
                plugins.append(plugin_info)

            # Descobrir transformers usando API nativa
            transformers_dict = hub_service.get_plugins_of_type(PluginType.TRANSFORMERS)
            for plugin_name, indexed_plugin in list(transformers_dict.items())[:3]:  # Limitar para performance
                plugin_info = {
                    "name": indexed_plugin.name,
                    "type": "transformer", 
                    "default_variant": indexed_plugin.default_variant,
                    "variants": list(indexed_plugin.variants.keys()) if indexed_plugin.variants else [],
                    "logo_url": getattr(indexed_plugin, "logo_url", ""),
                }
                plugins.append(plugin_info)

            self.logger.info(
                "Plugins discovered successfully", plugins_count=len(plugins)
            )
            return FlextResult.ok(plugins)

        except Exception as e:
            error_msg = f"Failed to discover plugins: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def install_plugin(
        self, project_root: Path, plugin_type: str, plugin_name: str
    ) -> FlextResult[dict[str, Any]]:
        """Instala plugin usando API nativa Meltano.

        Args:
            project_root: Diretório do projeto Meltano
            plugin_type: Tipo do plugin (extractor, loader, transformer)
            plugin_name: Nome do plugin

        Returns:
            FlextResult contendo informações da instalação

        """
        try:
            self.logger.info(
                "Installing Meltano plugin",
                plugin_type=plugin_type,
                plugin_name=plugin_name,
                project_root=str(project_root),
            )

            # Carregar projeto usando API nativa
            project_result = self.initialize_project(project_root)
            if not project_result.is_success:
                return FlextResult.fail(
                    f"Failed to load project: {project_result.error}"
                )

            project = project_result.value

            # Converter string type para PluginType enum
            plugin_type_enum = None
            if plugin_type.lower() in ["extractor", "extractors"]:
                plugin_type_enum = PluginType.EXTRACTORS
            elif plugin_type.lower() in ["loader", "loaders", "target", "targets"]:
                plugin_type_enum = PluginType.LOADERS
            elif plugin_type.lower() in ["transformer", "transformers", "dbt"]:
                plugin_type_enum = PluginType.TRANSFORMERS
            else:
                return FlextResult.fail(f"Invalid plugin type: {plugin_type}")

            # Usar API nativa para buscar plugin no hub
            hub_service = MeltanoHubService()
            found_plugins = hub_service.find_plugins(plugin_type=plugin_type_enum)

            # Encontrar plugin específico
            target_plugin = None
            for plugin in found_plugins:
                if plugin.name == plugin_name:
                    target_plugin = plugin
                    break

            if target_plugin is None:
                return FlextResult.fail(
                    f"Plugin {plugin_name} not found in Meltano Hub"
                )

            # Usar ProjectPluginsService para adicionar plugin ao projeto
            plugins_service = ProjectPluginsService(project)

            # Criar definição do plugin
            plugin_def = {
                "name": plugin_name,
                "namespace": target_plugin.namespace,
                "pip_url": target_plugin.pip_url,
                "executable": target_plugin.executable,
            }

            # Adicionar plugin ao projeto
            added_plugin = plugins_service.add_to_file(plugin_type_enum, plugin_def)

            # Usar PluginInstallService para instalar dependências
            install_service = PluginInstallService(project)
            install_result = install_service.install_plugin(added_plugin)

            if install_result:
                result_info = {
                    "plugin_name": plugin_name,
                    "plugin_type": plugin_type,
                    "namespace": target_plugin.namespace,
                    "pip_url": target_plugin.pip_url,
                    "executable": target_plugin.executable,
                    "installation_status": "success",
                }

                self.logger.info(
                    "Plugin installed successfully",
                    plugin_type=plugin_type,
                    plugin_name=plugin_name,
                )
                return FlextResult.ok(result_info)
            return FlextResult.fail(f"Plugin installation failed for {plugin_name}")

        except Exception as e:
            error_msg = f"Failed to install plugin {plugin_name}: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def list_installed_plugins(self, project: Project) -> FlextResult[list[dict[str, Any]]]:
        """Lista plugins instalados no projeto usando API nativa.

        Args:
            project: Instância Project do Meltano

        Returns:
            FlextResult contendo lista de plugins instalados

        """
        try:
            self.logger.info("Listing installed plugins")

            installed_plugins = []

            # Usar ProjectPluginsService para obter plugins instalados
            plugins_service = ProjectPluginsService(project)

            # Listar todos os tipos de plugins
            for plugin_type in [PluginType.EXTRACTORS, PluginType.LOADERS, PluginType.TRANSFORMERS]:
                type_plugins = plugins_service.get_plugins_of_type(plugin_type)

                for plugin in type_plugins:
                    plugin_info = {
                        "name": plugin.name,
                        "type": plugin_type.singular,  # extractor/loader/transformer
                        "namespace": getattr(plugin, "namespace", ""),
                        "executable": getattr(plugin, "executable", ""),
                        "pip_url": getattr(plugin, "pip_url", ""),
                        "config": getattr(plugin, "config", {}),
                        "settings": getattr(plugin, "settings", {}),
                        "variant": getattr(plugin, "variant", "original"),
                        "docs": getattr(plugin, "docs", ""),
                    }
                    installed_plugins.append(plugin_info)

            self.logger.info(
                "Installed plugins listed successfully",
                plugins_count=len(installed_plugins),
            )
            return FlextResult.ok(installed_plugins)

        except Exception as e:
            error_msg = f"Failed to list installed plugins: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def run_meltano_command(
        self, project_root: Path, command: list[str]
    ) -> FlextResult[dict[str, Any]]:
        """Executa comando meltano usando API nativa (sem subprocess).

        Args:
            project_root: Diretório do projeto Meltano
            command: Comando meltano para executar

        Returns:
            FlextResult contendo resultado do comando

        """
        try:
            self.logger.info(
                "Executing Meltano command natively",
                command=command,
                project_root=str(project_root),
            )

            # Validar projeto
            if not (project_root / "meltano.yml").exists():
                return FlextResult.fail(f"Not a Meltano project: {project_root}")

            # Carregar projeto Meltano
            project_result = self.initialize_project(project_root)
            if not project_result.is_success:
                return FlextResult.fail(f"Failed to load project: {project_result.error}")

            # Usar Click testing para execução nativa
            # Salvar diretório atual e mudar para projeto
            original_cwd = Path.cwd()
            os.chdir(project_root)

            try:
                # Criar runner Click para execução nativa
                runner = click.testing.CliRunner()

                # Executar comando Meltano nativamente via Click CLI
                self.logger.info("Executing native Meltano CLI", command=command)
                result = runner.invoke(cli, command)

                execution_result = {
                    "success": result.exit_code == 0,
                    "exit_code": result.exit_code,
                    "stdout": result.output,
                    "stderr": "",  # Click testing não separa stderr
                    "command": command,
                    "execution_method": "native_cli",
                }

                if result.exit_code == 0:
                    self.logger.info(
                        "Meltano command executed successfully via native API",
                        command=command
                    )
                    return FlextResult.ok(execution_result)
                self.logger.warning(
                    "Meltano command failed via native API",
                    command=command,
                    exit_code=result.exit_code,
                )
                return FlextResult.fail(
                    f"Native command failed with exit code {result.exit_code}"
                )

            finally:
                # Restaurar diretório original
                os.chdir(original_cwd)

        except Exception as e:
            error_msg = f"Failed to execute native Meltano command {command}: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)


# =============================================================================
# MELTANO TYPE ADAPTERS - FLEXT-CORE INTEGRATION
# =============================================================================


class FlextMeltanoAdapter:
    """Adaptador de tipos Meltano → FLEXT patterns."""

    @staticmethod
    def adapt_plugin(meltano_plugin: dict[str, Any]) -> FlextResult[dict[str, Any]]:
        """Converte meltano plugin para FlextPlugin pattern.

        Args:
            meltano_plugin: Plugin Meltano original

        Returns:
            FlextResult contendo plugin adaptado

        """
        try:
            # Adaptar para formato FlextPlugin
            flext_plugin = {
                "id": meltano_plugin.get("name"),
                "name": meltano_plugin.get("name"),
                "type": meltano_plugin.get("type"),
                "namespace": meltano_plugin.get("namespace"),
                "description": meltano_plugin.get("description", ""),
                "version": meltano_plugin.get("version", ""),
                "configuration": {
                    "pip_url": meltano_plugin.get("pip_url", ""),
                    "executable": meltano_plugin.get("executable", ""),
                    "config": meltano_plugin.get("config", {}),
                },
                "metadata": {
                    "source": "meltano",
                    "installed": meltano_plugin.get("installed", False),
                },
            }

            return FlextResult.ok(flext_plugin)

        except Exception as e:
            return FlextResult.fail(f"Failed to adapt Meltano plugin: {e}")

    @staticmethod
    def adapt_project_config(
        meltano_config: dict[str, Any],
    ) -> FlextResult[dict[str, Any]]:
        """Converte configuração meltano para FlextProjectConfig pattern.

        Args:
            meltano_config: Configuração Meltano original

        Returns:
            FlextResult contendo configuração adaptada

        """
        try:
            # Adaptar para formato FlextProjectConfig
            flext_config = {
                "version": "1.0",
                "project_name": meltano_config.get("project_name"),
                "project_id": meltano_config.get("project_id"),
                "environments": meltano_config.get("environments", []),
                "plugins": {
                    "extractors": meltano_config.get("plugins", {}).get(
                        "extractors", []
                    ),
                    "loaders": meltano_config.get("plugins", {}).get("loaders", []),
                    "transformers": meltano_config.get("plugins", {}).get(
                        "transformers", []
                    ),
                },
                "schedules": meltano_config.get("schedules", []),
                "metadata": {
                    "meltano_version": meltano_config.get("version"),
                    "created_at": meltano_config.get("created_at"),
                },
            }

            return FlextResult.ok(flext_config)

        except Exception as e:
            return FlextResult.fail(f"Failed to adapt Meltano config: {e}")


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = ["MELTANO_AVAILABLE", "FlextMeltanoAdapter", "MeltanoBridge"]
