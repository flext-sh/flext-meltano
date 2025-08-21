"""Flext Meltano Utilities - Classes e funções utilitárias frequentes.

FUNÇÃO 1, 2 & 3: Utilidades para wrappers, runtime e base projects
- FlextMeltanoUtilities: Métodos estáticos para operações comuns
- FlextResultHelpers: Helpers para FlextResult patterns
- FlextTypeAdapters: Adaptadores de tipos para FlextCore
"""

from __future__ import annotations

import tempfile
import yaml
from pathlib import Path
from typing import TypeVar

from flext_core import FlextResult

T = TypeVar("T")


class FlextMeltanoUtilities:
    """Classe de utilidades estáticas para operações frequentes."""

    @staticmethod
    def create_temp_directory(prefix: str = "flext_meltano_") -> Path:
        """Cria diretório temporário com prefix padrão.
        
        Args:
            prefix: Prefixo para o diretório temporário
            
        Returns:
            Path do diretório criado
        """
        return Path(tempfile.mkdtemp(prefix=prefix))

    @staticmethod
    def create_meltano_config(project_id: str, project_name: str = "") -> dict[str, str]:
        """Cria configuração mínima do Meltano.
        
        Args:
            project_id: ID do projeto
            project_name: Nome do projeto (opcional)
            
        Returns:
            Dict com configuração do Meltano
        """
        return {
            "version": "1",
            "project_id": project_id,
            "project_name": project_name or project_id,
            "environments": "dev",  # Simplificado
        }

    @staticmethod
    def save_yaml_config(config: dict[str, str], file_path: Path) -> FlextResult[bool]:
        """Salva configuração YAML em arquivo.
        
        Args:
            config: Configuração para salvar
            file_path: Caminho do arquivo
            
        Returns:
            FlextResult indicando sucesso/falha
        """
        try:
            with file_path.open("w") as f:
                yaml.dump(config, f)
            return FlextResult.ok(True)
        except Exception as e:
            return FlextResult.fail(f"Failed to save YAML config: {e}")

    @staticmethod  
    def load_yaml_config(file_path: Path) -> FlextResult[dict[str, str]]:
        """Carrega configuração YAML de arquivo.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            FlextResult com configuração carregada
        """
        try:
            if not file_path.exists():
                return FlextResult.fail(f"Config file not found: {file_path}")
                
            with file_path.open("r") as f:
                config = yaml.safe_load(f)
                
            # Garantir que todos valores são strings
            str_config = {
                str(k): str(v) for k, v in (config or {}).items()
            }
            
            return FlextResult.ok(str_config)
        except Exception as e:
            return FlextResult.fail(f"Failed to load YAML config: {e}")

    @staticmethod
    def sanitize_plugin_name(name: str) -> str:
        """Sanitiza nome de plugin para formato válido.
        
        Args:
            name: Nome original do plugin
            
        Returns:
            Nome sanitizado
        """
        return name.lower().replace("-", "_").replace(" ", "_")

    @staticmethod
    def create_plugin_config(
        name: str, 
        plugin_type: str,
        namespace: str = "",
        pip_url: str = ""
    ) -> dict[str, str]:
        """Cria configuração padrão de plugin.
        
        Args:
            name: Nome do plugin
            plugin_type: Tipo (extractor, loader, transformer)
            namespace: Namespace (opcional)
            pip_url: URL do pip (opcional)
            
        Returns:
            Dict com configuração do plugin
        """
        sanitized_name = FlextMeltanoUtilities.sanitize_plugin_name(name)
        
        return {
            "name": name,
            "type": plugin_type,
            "namespace": namespace or f"{sanitized_name}_namespace",
            "pip_url": pip_url or f"git+https://github.com/MeltanoLabs/{name}.git",
            "executable": sanitized_name,
        }


class FlextResultHelpers:
    """Helpers para trabalhar com FlextResult patterns."""

    @staticmethod
    def chain_results(*results: FlextResult[T]) -> FlextResult[list[T]]:
        """Encadeia múltiplos FlextResults, parando no primeiro erro.
        
        Args:
            results: Sequência de FlextResult para encadear
            
        Returns:
            FlextResult com lista de valores ou primeiro erro
        """
        values = []
        for result in results:
            if not result.success:
                return FlextResult.fail(result.error_message or "Chain failed")
            values.append(result.value)
        
        return FlextResult.ok(values)

    @staticmethod  
    def collect_successes(*results: FlextResult[T]) -> FlextResult[list[T]]:
        """Coleta apenas os sucessos, ignorando falhas.
        
        Args:
            results: Sequência de FlextResult
            
        Returns:
            FlextResult com lista de valores bem-sucedidos
        """
        successes = []
        for result in results:
            if result.success:
                successes.append(result.value)
        
        return FlextResult.ok(successes)

    @staticmethod
    def first_success(*results: FlextResult[T]) -> FlextResult[T]:
        """Retorna o primeiro resultado bem-sucedido.
        
        Args:
            results: Sequência de FlextResult
            
        Returns:
            FlextResult com primeiro sucesso ou último erro
        """
        last_error = "No results provided"
        
        for result in results:
            if result.success:
                return result
            last_error = result.error_message or "Unknown error"
        
        return FlextResult.fail(last_error)


class FlextTypeAdapters:
    """Adaptadores de tipos para integração com FlextCore."""

    @staticmethod
    def dict_to_string_dict(data: dict) -> dict[str, str]:
        """Converte dict genérico para dict[str, str].
        
        Args:
            data: Dictionary genérico
            
        Returns:
            Dict com chaves e valores como strings
        """
        return {str(k): str(v) for k, v in data.items()}

    @staticmethod
    def list_to_comma_separated(items: list) -> str:
        """Converte lista para string separada por vírgulas.
        
        Args:
            items: Lista de itens
            
        Returns:
            String com itens separados por vírgulas
        """
        return ",".join(str(item) for item in items)

    @staticmethod
    def comma_separated_to_list(text: str) -> list[str]:
        """Converte string separada por vírgulas para lista.
        
        Args:
            text: String com itens separados por vírgulas
            
        Returns:
            Lista de strings
        """
        return [item.strip() for item in text.split(",") if item.strip()]

    @staticmethod
    def safe_get_string(data: dict, key: str, default: str = "") -> str:
        """Obtém string de dict de forma segura.
        
        Args:
            data: Dictionary
            key: Chave para buscar
            default: Valor padrão
            
        Returns:
            String value ou default
        """
        return str(data.get(key, default))


# =============================================================================
# FUNCTION-SPECIFIC UTILITIES
# =============================================================================

class FlextWrapperUtilities(FlextMeltanoUtilities):
    """Utilidades específicas para wrappers (FUNÇÃO 1)."""
    
    @staticmethod
    def adapt_meltano_plugin(meltano_plugin: dict) -> dict[str, str]:
        """Adapta plugin do Meltano para formato FlextCore.
        
        Args:
            meltano_plugin: Plugin no formato Meltano
            
        Returns:
            Plugin adaptado para FlextCore
        """
        return {
            "id": str(meltano_plugin.get("name", "")),
            "name": str(meltano_plugin.get("name", "")),
            "type": str(meltano_plugin.get("type", "")),
            "namespace": str(meltano_plugin.get("namespace", "")),
            "version": str(meltano_plugin.get("version", "")),
            "status": "adapted"
        }


class FlextRuntimeUtilities(FlextMeltanoUtilities):
    """Utilidades específicas para runtime bridge (FUNÇÃO 2)."""
    
    @staticmethod  
    def create_bridge_response(success: bool, data: dict[str, str] | None = None) -> dict[str, str]:
        """Cria resposta padrão para Go bridge.
        
        Args:
            success: Indicador de sucesso
            data: Dados da resposta (opcional)
            
        Returns:
            Dict formatado para Go bridge
        """
        return {
            "success": str(success),
            "data": str(data or {}),
            "timestamp": str(Path.cwd().stat().st_mtime),  # Simple timestamp
        }
    
    @staticmethod
    def format_command_result(exit_code: int, output: str, command: str) -> dict[str, str]:
        """Formata resultado de comando para Go bridge.
        
        Args:
            exit_code: Código de saída
            output: Output do comando
            command: Comando executado
            
        Returns:
            Dict formatado
        """
        return {
            "exit_code": str(exit_code),
            "success": str(exit_code == 0),
            "output": output,
            "command": command,
        }


class FlextBaseUtilities(FlextMeltanoUtilities):
    """Utilidades específicas para base projects (FUNÇÃO 3)."""
    
    @staticmethod
    def create_base_service_config(service_name: str, service_type: str) -> dict[str, str]:
        """Cria configuração base para serviços flext-*.
        
        Args:
            service_name: Nome do serviço
            service_type: Tipo do serviço (tap, target, dbt)
            
        Returns:
            Dict com configuração base
        """
        return {
            "name": service_name,
            "type": service_type,
            "framework": "flext_meltano",
            "version": "2.0.0",
            "status": "active"
        }


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    "FlextMeltanoUtilities",
    "FlextResultHelpers", 
    "FlextTypeAdapters",
    "FlextWrapperUtilities",
    "FlextRuntimeUtilities",
    "FlextBaseUtilities"
]