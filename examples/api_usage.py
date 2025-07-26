"""Exemplo de uso da API modernizada do FLEXT Meltano.

Demonstra como usar a nova API FlextMeltanoAPI seguindo padrões flext-core.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from flext_meltano.api import (
    FlextMeltanoAPI,
)


def example_basic_api_usage() -> None:
    """Exemplo básico de uso da API FlextMeltanoAPI."""
    # Criar diretório temporário para o exemplo
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir) / "example_project"
        project_root.mkdir()

        # Inicializar API
        FlextMeltanoAPI(
            project_root=project_root,
            environment="dev",
            auto_install=True,
        )

        # Exemplo de configuração de plugin (seria usado em projeto real)

        # Exemplo de descoberta de catálogo (seria usado em projeto real)

        # Exemplo de teste de conexão (seria usado em projeto real)

        # Exemplo de execução de pipeline (seria usado em projeto real)


def example_one_liner_functions() -> None:
    """Exemplo de uso das funções one-liner."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir) / "oneliner_project"
        project_root.mkdir()

        # Exemplos conceituais das funções one-liner


def example_advanced_usage() -> None:
    """Exemplo de uso avançado da API."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir) / "advanced_project"
        project_root.mkdir()

        # API com configurações customizadas
        FlextMeltanoAPI(
            project_root=project_root,
            environment="prod",
            auto_install=False,  # Controle manual de plugins
            state_backend="filesystem",
        )


def example_error_handling() -> None:
    """Exemplo de tratamento de erros com FlextResult."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir) / "error_handling"
        project_root.mkdir()

        FlextMeltanoAPI(project_root=project_root)


if __name__ == "__main__":
    example_basic_api_usage()
    example_one_liner_functions()
    example_advanced_usage()
    example_error_handling()
