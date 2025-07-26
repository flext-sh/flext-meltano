"""Exemplo de uso das constantes do FlextMeltanoConstants.

Demonstra como usar as constantes seguindo o padrão do flext-core.
"""

from __future__ import annotations

from flext_meltano.constants import (
    MeltanoEnvironment,
    MeltanoLogLevel,
    MeltanoResultStatus,
)


def example_constants_usage() -> None:
    """Exemplo de uso das constantes do FlextMeltanoConstants."""
    # 1. Acesso direto às constantes (padrão flext-core)


def example_environment_usage() -> None:
    """Exemplo de uso dos enums de ambiente."""
    # Uso dos enums
    env = MeltanoEnvironment.DEVELOPMENT
    log_level = MeltanoLogLevel.INFO
    status = MeltanoResultStatus.SUCCESS

    # Comparação
    if env == MeltanoEnvironment.DEVELOPMENT:
        pass

    if log_level == MeltanoLogLevel.INFO:
        pass

    if status == MeltanoResultStatus.SUCCESS:
        pass


if __name__ == "__main__":
    example_constants_usage()
    example_environment_usage()
