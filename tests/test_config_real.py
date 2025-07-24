"""Testes reais para config.py - COVERAGE DIRETO.

Objetivo: Gerar coverage real no arquivo config.py (91 statements, 0% coverage).
Foco em aumentar coverage total de 23% para próximo patamar significativo.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

# Import direto das classes REAIS do config.py
from flext_meltano.config import (
    FlextMeltanoExecutionConfig,
    FlextMeltanoProjectConfig,
    get_container,
)


class TestFlextMeltanoProjectConfig:
    """Testes reais da classe FlextMeltanoProjectConfig."""

    def test_project_config_creation(self) -> None:
        """Testa criação de configuração de projeto básica."""
        config = FlextMeltanoProjectConfig()

        # Testa valores padrão
        assert isinstance(config.project_root, Path)
        assert "meltano_projects" in str(config.project_root)
        assert config.default_environment == "production"
        assert config.database_uri == "sqlite:///meltano.db"
        assert config.python_version == "3.13"

    def test_project_config_with_custom_values(self) -> None:
        """Testa criação com valores customizados."""
        custom_root = Path("/custom/path")
        config = FlextMeltanoProjectConfig(
            project_root=custom_root,
            default_environment="development",
            database_uri="postgresql://localhost/meltano",
            python_version="3.12"
        )

        assert config.project_root == custom_root
        assert config.default_environment == "development"
        assert config.database_uri == "postgresql://localhost/meltano"
        assert config.python_version == "3.12"

    def test_project_config_field_validation(self) -> None:
        """Testa validação de campos."""
        # Testa que consegue criar com valores válidos
        config = FlextMeltanoProjectConfig(
            project_root=Path("/valid/path"),
            default_environment="staging",
            database_uri="mysql://localhost/meltano",
            python_version="3.11"
        )

        assert config.project_root == Path("/valid/path")
        assert config.default_environment == "staging"
        assert config.database_uri == "mysql://localhost/meltano"
        assert config.python_version == "3.11"


class TestFlextMeltanoExecutionConfig:
    """Testes reais da classe FlextMeltanoExecutionConfig."""

    def test_execution_config_creation(self) -> None:
        """Testa criação de configuração de execução básica."""
        config = FlextMeltanoExecutionConfig()

        # Testa valores padrão
        assert config.max_concurrent_jobs == 5
        assert config.job_timeout == 3600
        assert config.retry_attempts == 3
        assert config.retry_delay == 30

    def test_execution_config_with_custom_values(self) -> None:
        """Testa criação com valores customizados."""
        config = FlextMeltanoExecutionConfig(
            max_concurrent_jobs=10,
            job_timeout=7200,
            retry_attempts=5,
            retry_delay=60
        )

        assert config.max_concurrent_jobs == 10
        assert config.job_timeout == 7200
        assert config.retry_attempts == 5
        assert config.retry_delay == 60

    def test_execution_config_field_constraints(self) -> None:
        """Testa constraints de validação dos campos."""
        # Testa valores nos limites válidos
        config = FlextMeltanoExecutionConfig(
            max_concurrent_jobs=1,  # mínimo
            job_timeout=60,  # mínimo
            retry_attempts=0,  # mínimo
            retry_delay=1  # mínimo
        )

        assert config.max_concurrent_jobs == 1
        assert config.job_timeout == 60
        assert config.retry_attempts == 0
        assert config.retry_delay == 1

        # Testa valores nos limites máximos
        config_max = FlextMeltanoExecutionConfig(
            max_concurrent_jobs=50,  # máximo
            job_timeout=86400,  # máximo
            retry_attempts=10,  # máximo
            retry_delay=300  # máximo
        )

        assert config_max.max_concurrent_jobs == 50
        assert config_max.job_timeout == 86400
        assert config_max.retry_attempts == 10
        assert config_max.retry_delay == 300

    def test_execution_config_invalid_values(self) -> None:
        """Testa validação com valores inválidos."""
        # Testa valores fora dos limites - devem gerar ValidationError
        with pytest.raises(ValueError, match="validation error"):
            FlextMeltanoExecutionConfig(max_concurrent_jobs=0)  # abaixo do mínimo

        with pytest.raises(ValueError, match="validation error"):
            FlextMeltanoExecutionConfig(max_concurrent_jobs=51)  # acima do máximo

        with pytest.raises(ValueError, match="validation error"):
            FlextMeltanoExecutionConfig(job_timeout=59)  # abaixo do mínimo

        with pytest.raises(ValueError, match="validation error"):
            FlextMeltanoExecutionConfig(job_timeout=86401)  # acima do máximo

        with pytest.raises(ValueError, match="validation error"):
            FlextMeltanoExecutionConfig(retry_attempts=-1)  # abaixo do mínimo

        with pytest.raises(ValueError, match="validation error"):
            FlextMeltanoExecutionConfig(retry_attempts=11)  # acima do máximo

        with pytest.raises(ValueError, match="validation error"):
            FlextMeltanoExecutionConfig(retry_delay=0)  # abaixo do mínimo

        with pytest.raises(ValueError, match="validation error"):
            FlextMeltanoExecutionConfig(retry_delay=301)  # acima do máximo


class TestConfigHelpers:
    """Testes para funções auxiliares do config.py."""

    def test_get_container(self) -> None:
        """Testa função get_container."""
        container = get_container()

        # Deve retornar algum objeto (não None)
        assert container is not None

        # Deve ser consistente (mesmo objeto em chamadas sucessivas)
        container2 = get_container()
        assert container == container2


class TestConfigIntegration:
    """Testes de integração das configurações."""

    def test_config_combination(self) -> None:
        """Testa uso combinado das configurações."""
        project_config = FlextMeltanoProjectConfig(
            project_root=Path("/test/project"),
            default_environment="test"
        )

        execution_config = FlextMeltanoExecutionConfig(
            max_concurrent_jobs=2,
            job_timeout=1800
        )

        # Verifica que ambas as configurações podem coexistir
        assert project_config.project_root == Path("/test/project")
        assert project_config.default_environment == "test"
        assert execution_config.max_concurrent_jobs == 2
        assert execution_config.job_timeout == 1800

    def test_config_serialization(self) -> None:
        """Testa serialização das configurações."""
        project_config = FlextMeltanoProjectConfig(
            default_environment="development",
            python_version="3.12"
        )

        # Deve conseguir converter para dict (serialização básica)
        config_dict = project_config.model_dump() if hasattr(project_config, "model_dump") else project_config.dict()

        assert isinstance(config_dict, dict)
        assert config_dict["default_environment"] == "development"
        assert config_dict["python_version"] == "3.12"

    def test_config_field_access(self) -> None:
        """Testa acesso aos campos das configurações."""
        execution_config = FlextMeltanoExecutionConfig()

        # Verifica que todos os campos esperados existem
        assert hasattr(execution_config, "max_concurrent_jobs")
        assert hasattr(execution_config, "job_timeout")
        assert hasattr(execution_config, "retry_attempts")
        assert hasattr(execution_config, "retry_delay")

        # Verifica que os valores são acessíveis
        assert isinstance(execution_config.max_concurrent_jobs, int)
        assert isinstance(execution_config.job_timeout, int)
        assert isinstance(execution_config.retry_attempts, int)
        assert isinstance(execution_config.retry_delay, int)
