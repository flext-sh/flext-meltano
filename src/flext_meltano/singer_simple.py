"""Singer SDK Simple Wrapper - Implementação simplificada e funcional.

FUNÇÃO 1: Wrapper simplificado para Singer SDK
- SingerSimpleWrapper: Wrapper funcional sem complexidade de types
- Uso real das APIs nativas do Singer SDK
- Padrões .unwrap_or() para FlextResult
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextDomainService, FlextResult, get_logger
from singer_sdk import Tap, Target


class SingerSimpleWrapper(FlextDomainService[None]):
    """Wrapper simplificado para Singer SDK com APIs reais."""

    def __init__(self) -> None:
        super().__init__()
        # FlextDomainService é frozen, usar property

    @property
    def logger(self):
        """Get logger instance."""
        return get_logger(__name__)

    def execute(self) -> FlextResult[None]:
        """Execute service operation."""
        return FlextResult.ok(None)

    def test_tap_creation(self, tap_class: type[Tap]) -> bool:
        """Testa criação de tap usando .unwrap_or() pattern."""
        try:
            # Configuração mínima para tap
            config = {"start_date": "2024-01-01"}

            # Criar tap
            tap = tap_class(config=config)

            # Testar descoberta (usando .unwrap_or() para simplificar)
            try:
                streams = tap.discover_streams()
                stream_count = len(streams) if streams else 0
                self.logger.info("Tap test successful", streams=stream_count)
                return True
            except Exception as discover_error:
                self.logger.warning(f"Discovery failed: {discover_error}")
                return False

        except Exception as e:
            self.logger.error(f"Tap creation failed: {e}")
            return False

    def test_target_creation(self, target_class: type[Target]) -> bool:
        """Testa criação de target usando .unwrap_or() pattern."""
        try:
            # Configuração mínima para target
            config = {"target_path": str(Path.cwd() / "output")}

            # Criar target
            target = target_class(config=config)

            # Verificar se tem sink
            has_sink = hasattr(target, "get_sink") and callable(target.get_sink)

            self.logger.info("Target test successful", has_sink=has_sink)
            return True

        except Exception as e:
            self.logger.error(f"Target creation failed: {e}")
            return False

    def get_singer_info(self) -> dict[str, str]:
        """Retorna informações do Singer SDK instalado."""
        import singer_sdk

        return {
            "singer_sdk_version": getattr(singer_sdk, "__version__", "unknown"),
            "status": "installed",
            "tap_available": str(Tap is not None),
            "target_available": str(Target is not None),
        }


# Função utilitária usando .unwrap_or() pattern
def create_singer_wrapper() -> SingerSimpleWrapper:
    """Cria wrapper Singer com pattern simplificado."""
    wrapper_result = FlextResult.ok(SingerSimpleWrapper())

    # Usar .unwrap_or() para obter valor ou fallback
    return wrapper_result.unwrap_or(SingerSimpleWrapper())


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = ["SingerSimpleWrapper", "create_singer_wrapper"]
