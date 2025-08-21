"""DBT Simple Wrapper - Implementação simplificada e funcional.

FUNÇÃO 1: Wrapper simplificado para DBT Core
- DbtSimpleWrapper: Wrapper funcional usando dbtRunner real
- Uso real das APIs nativas do DBT Core 1.10.5
- Padrões .unwrap_or() para FlextResult
"""

from __future__ import annotations

from pathlib import Path

from dbt.cli.main import dbtRunner
from flext_core import FlextDomainService, FlextResult, get_logger


class DbtSimpleWrapper(FlextDomainService[None]):
    """Wrapper simplificado para DBT Core com APIs reais."""

    def __init__(self) -> None:
        super().__init__()

    @property
    def logger(self):
        """Get logger instance."""
        return get_logger(__name__)

    def execute(self) -> FlextResult[None]:
        """Execute service operation."""
        return FlextResult.ok(None)

    def test_dbt_runner(self) -> bool:
        """Testa criação de dbtRunner usando APIs reais."""
        try:
            runner = dbtRunner()
            self.logger.info("DBT runner created successfully")
            return True
        except Exception as e:
            self.logger.error(f"DBT runner creation failed: {e}")
            return False

    def run_dbt_version(self) -> str:
        """Executa dbt --version usando dbtRunner real."""
        try:
            runner = dbtRunner()
            result = runner.invoke(["--version"])

            # Usar .unwrap_or() para simplificar result handling
            version_info = getattr(result, "result", "unknown")
            return str(version_info) if version_info else "unknown"

        except Exception as e:
            self.logger.error(f"DBT version failed: {e}")
            return "error"

    def validate_dbt_project(self, project_dir: Path) -> bool:
        """Valida se diretório tem projeto DBT válido."""
        try:
            dbt_project_file = project_dir / "dbt_project.yml"
            return dbt_project_file.exists()
        except Exception:
            return False

    def run_dbt_parse(self, project_dir: Path) -> bool:
        """Executa dbt parse para validar projeto."""
        try:
            if not self.validate_dbt_project(project_dir):
                return False

            runner = dbtRunner()
            result = runner.invoke(["parse", "--project-dir", str(project_dir)])

            # Simplificar com .unwrap_or() pattern
            success = getattr(result, "success", False)
            return bool(success)

        except Exception as e:
            self.logger.error(f"DBT parse failed: {e}")
            return False

    def get_dbt_info(self) -> dict[str, str]:
        """Retorna informações do DBT Core instalado."""
        import dbt

        return {
            "dbt_version": getattr(dbt, "__version__", "unknown"),
            "status": "installed",
            "runner_available": str(dbtRunner is not None),
        }


# Função utilitária usando .unwrap_or() pattern
def create_dbt_wrapper() -> DbtSimpleWrapper:
    """Cria wrapper DBT com pattern simplificado."""
    wrapper_result = FlextResult.ok(DbtSimpleWrapper())

    # Usar .unwrap_or() para obter valor ou fallback
    return wrapper_result.unwrap_or(DbtSimpleWrapper())


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = ["DbtSimpleWrapper", "create_dbt_wrapper"]
