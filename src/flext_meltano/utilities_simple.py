"""Flext Meltano Simple Utilities - Sem dependência do flext-core temporariamente.

FUNÇÃO 1, 2 & 3: Utilidades para wrappers, runtime e base projects
Versão simplificada sem flext-core até resolver problemas de Pydantic.
"""

from __future__ import annotations

import tempfile
import yaml
from pathlib import Path
from typing import TypeVar, Generic

T = TypeVar("T")


class SimpleFlextResult(Generic[T]):
    """Versão simplificada do FlextResult."""
    
    def __init__(self, success: bool, value: T | None = None, error: str | None = None):
        self.success = success
        self.value = value  
        self.error_message = error
    
    @classmethod
    def ok(cls, value: T) -> SimpleFlextResult[T]:
        return cls(True, value, None)
    
    @classmethod  
    def fail(cls, error: str) -> SimpleFlextResult[T]:
        return cls(False, None, error)
    
    def unwrap_or(self, default: T) -> T:
        return self.value if self.success and self.value is not None else default


class FlextMeltanoUtilities:
    """Classe de utilidades estáticas para operações frequentes."""

    @staticmethod
    def create_temp_directory(prefix: str = "flext_meltano_") -> Path:
        """Cria diretório temporário com prefix padrão."""
        return Path(tempfile.mkdtemp(prefix=prefix))

    @staticmethod
    def create_meltano_config(project_id: str, project_name: str = "") -> dict[str, str]:
        """Cria configuração mínima do Meltano."""
        return {
            "version": "1",
            "project_id": project_id,
            "project_name": project_name or project_id,
            "environments": "dev",
        }

    @staticmethod
    def save_yaml_config(config: dict[str, str], file_path: Path) -> SimpleFlextResult[bool]:
        """Salva configuração YAML em arquivo."""
        try:
            with file_path.open("w") as f:
                yaml.dump(config, f)
            return SimpleFlextResult.ok(True)
        except Exception as e:
            return SimpleFlextResult.fail(f"Failed to save YAML config: {e}")

    @staticmethod  
    def load_yaml_config(file_path: Path) -> SimpleFlextResult[dict[str, str]]:
        """Carrega configuração YAML de arquivo."""
        try:
            if not file_path.exists():
                return SimpleFlextResult.fail(f"Config file not found: {file_path}")
                
            with file_path.open("r") as f:
                config = yaml.safe_load(f)
                
            # Garantir que todos valores são strings
            str_config = {
                str(k): str(v) for k, v in (config or {}).items()
            }
            
            return SimpleFlextResult.ok(str_config)
        except Exception as e:
            return SimpleFlextResult.fail(f"Failed to load YAML config: {e}")

    @staticmethod
    def sanitize_plugin_name(name: str) -> str:
        """Sanitiza nome de plugin para formato válido."""
        return name.lower().replace("-", "_").replace(" ", "_")

    @staticmethod
    def create_plugin_config(
        name: str, 
        plugin_type: str,
        namespace: str = "",
        pip_url: str = ""
    ) -> dict[str, str]:
        """Cria configuração padrão de plugin."""
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
    def chain_results(*results: SimpleFlextResult[T]) -> SimpleFlextResult[list[T]]:
        """Encadeia múltiplos FlextResults, parando no primeiro erro."""
        values = []
        for result in results:
            if not result.success:
                return SimpleFlextResult.fail(result.error_message or "Chain failed")
            values.append(result.value)
        
        return SimpleFlextResult.ok(values)


class FlextTypeAdapters:
    """Adaptadores de tipos para integração com FlextCore."""

    @staticmethod
    def dict_to_string_dict(data: dict) -> dict[str, str]:
        """Converte dict genérico para dict[str, str]."""
        return {str(k): str(v) for k, v in data.items()}

    @staticmethod
    def list_to_comma_separated(items: list) -> str:
        """Converte lista para string separada por vírgulas."""
        return ",".join(str(item) for item in items)

    @staticmethod
    def comma_separated_to_list(text: str) -> list[str]:
        """Converte string separada por vírgulas para lista."""
        return [item.strip() for item in text.split(",") if item.strip()]

    @staticmethod
    def safe_get_string(data: dict, key: str, default: str = "") -> str:
        """Obtém string de dict de forma segura."""
        return str(data.get(key, default))


# =============================================================================
# TESTING FUNCTIONS
# =============================================================================

def test_utilities() -> None:
    """Testa as utilities básicas."""
    print("🧪 Testing FlextMeltano Utilities...")
    
    # Test 1: Temp directory
    temp_dir = FlextMeltanoUtilities.create_temp_directory("test_")
    print(f"✅ Temp directory created: {temp_dir}")
    
    # Test 2: Meltano config
    config = FlextMeltanoUtilities.create_meltano_config("test-project", "My Test Project")
    print(f"✅ Meltano config: {config}")
    
    # Test 3: Plugin sanitization
    sanitized = FlextMeltanoUtilities.sanitize_plugin_name("tap-test-plugin")
    print(f"✅ Sanitized name: {sanitized}")
    
    # Test 4: Plugin config
    plugin_config = FlextMeltanoUtilities.create_plugin_config("tap-csv", "extractor")
    print(f"✅ Plugin config: {plugin_config}")
    
    # Test 5: Type adapters
    test_dict = {"key1": "value1", "key2": 123, "key3": True}
    adapted = FlextTypeAdapters.dict_to_string_dict(test_dict)
    print(f"✅ Adapted dict: {adapted}")
    
    # Test 6: FlextResult pattern
    result_ok = SimpleFlextResult.ok("success_value")
    result_fail = SimpleFlextResult.fail("error_message")
    
    print(f"✅ Success result: {result_ok.unwrap_or('default')}")
    print(f"✅ Failed result: {result_fail.unwrap_or('default')}")
    
    print("🎉 All utilities tests passed!")


if __name__ == "__main__":
    test_utilities()


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    "FlextMeltanoUtilities",
    "FlextResultHelpers", 
    "FlextTypeAdapters",
    "SimpleFlextResult"
]