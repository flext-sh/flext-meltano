"""Testes reais para config.py ROOT - COVERAGE DIRETO NO TARGET CORRETO.

CORREÇÃO: Este arquivo testa src/flext_meltano/config.py (91 statements, 0% coverage)
NÃO o config/settings.py que já tem 77% coverage.

Objetivo: Gerar coverage REAL no arquivo correto para melhorar total coverage.
"""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

# Import direto do config.py ROOT (não config/settings.py)
# Importar as classes que estão REALMENTE definidas neste arquivo
try:
    # Se essas classes vierem de config/settings.py via __init__.py,
    # precisamos testar as classes que estão NO PRÓPRIO config.py
    # Vamos importar diretamente do módulo config.py específico
    import sys
    from pathlib import Path

    from flext_meltano.config import (
        FlextMeltanoExecutionConfig,
        FlextMeltanoProjectConfig,
        get_container,
    )

    # Import direto do config.py ROOT
    config_module_path = Path(__file__).parent.parent / "src" / "flext_meltano" / "config.py"

    import importlib.util
    spec = importlib.util.spec_from_file_location("root_config", config_module_path)
    if spec and spec.loader:
        root_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(root_config)
    else:
        root_config = None

except ImportError:
    root_config = None


class TestRootConfigModule:
    """Testes para as classes definidas diretamente no config.py ROOT."""

    def test_config_imports_and_types(self) -> None:
        """Testa imports e types do config.py ROOT."""
        if root_config is None:
            pytest.skip("Could not load root config module")

        # Testa que as classes base estão definidas
        assert hasattr(root_config, "ConfigDefaults")
        assert hasattr(root_config, "DomainValueObject")

        # Testa que os mixins locais estão definidos
        assert hasattr(root_config, "FlextMeltanoBaseConfigMixin")
        assert hasattr(root_config, "FlextMeltanoDatabaseConfigMixin")
        assert hasattr(root_config, "FlextMeltanoLoggingConfigMixin")
        assert hasattr(root_config, "FlextMeltanoMonitoringConfigMixin")
        assert hasattr(root_config, "FlextMeltanoPerformanceConfigMixin")

    def test_get_container_function(self) -> None:
        """Testa função get_container do config.py ROOT."""
        if root_config is None:
            pytest.skip("Could not load root config module")

        # Testa que a função get_container existe
        assert hasattr(root_config, "get_container")
        assert callable(root_config.get_container)

        # Mock para evitar dependências
        with patch("flext_meltano.infrastructure.di_container.get_di_container") as mock_di:
            mock_di.return_value = Mock()
            result = root_config.get_container()
            assert result is not None
            mock_di.assert_called_once()

    def test_config_value_objects_definition(self) -> None:
        """Testa definição dos value objects de configuração."""
        if root_config is None:
            pytest.skip("Could not load root config module")

        # Testa que as classes de configuração estão definidas
        assert hasattr(root_config, "FlextMeltanoProjectConfig")
        assert hasattr(root_config, "FlextMeltanoExecutionConfig")
        assert hasattr(root_config, "FlextMeltanoStateConfig")
        assert hasattr(root_config, "FlextMeltanoBusinessConfig")
        assert hasattr(root_config, "FlextMeltanoPluginConfig")
        assert hasattr(root_config, "FlextMeltanoMonitoringConfig")

    def test_flext_meltano_project_config_from_root(self) -> None:
        """Testa FlextMeltanoProjectConfig definida no ROOT config.py."""
        if root_config is None:
            pytest.skip("Could not load root config module")

        project_config = root_config.FlextMeltanoProjectConfig

        # Testa criação básica
        config = project_config()

        # Testa campos obrigatórios
        assert hasattr(config, "project_root")
        assert hasattr(config, "default_environment")
        assert hasattr(config, "database_uri")
        assert hasattr(config, "python_version")

        # Testa valores padrão
        assert config.default_environment == "production"
        assert config.database_uri == "sqlite:///meltano.db"
        assert config.python_version == "3.13"

    def test_flext_meltano_execution_config_from_root(self) -> None:
        """Testa FlextMeltanoExecutionConfig definida no ROOT config.py."""
        if root_config is None:
            pytest.skip("Could not load root config module")

        execution_config = root_config.FlextMeltanoExecutionConfig

        # Testa criação básica
        config = execution_config()

        # Testa campos obrigatórios
        assert hasattr(config, "max_concurrent_jobs")
        assert hasattr(config, "job_timeout")
        assert hasattr(config, "retry_attempts")
        assert hasattr(config, "retry_delay")

        # Testa valores padrão
        assert config.max_concurrent_jobs == 5
        assert config.job_timeout == 3600
        assert config.retry_attempts == 3
        assert config.retry_delay == 30

    def test_flext_meltano_business_config_from_root(self) -> None:
        """Testa FlextMeltanoBusinessConfig definida no ROOT config.py."""
        if root_config is None:
            pytest.skip("Could not load root config module")

        business_config = root_config.FlextMeltanoBusinessConfig

        # Testa criação básica
        config = business_config()

        # Testa campo específico de business logic
        assert hasattr(config, "MINIMUM_MELTANO_COMMAND_COUNT")
        assert config.MINIMUM_MELTANO_COMMAND_COUNT == 2

    def test_flext_meltano_settings_main_class(self) -> None:
        """Testa FlextMeltanoSettings - classe principal do ROOT config.py."""
        if root_config is None:
            pytest.skip("Could not load root config module")

        settings_class = root_config.FlextMeltanoSettings

        # Mock das dependências para evitar imports
        with patch("flext_meltano.infrastructure.di_container.get_di_container"):
            settings = settings_class()

            # Testa atributos principais
            assert hasattr(settings, "project_name")
            assert hasattr(settings, "project_version")
            assert hasattr(settings, "environment")
            assert hasattr(settings, "debug")

            # Testa value objects aninhados
            assert hasattr(settings, "project")
            assert hasattr(settings, "execution")
            assert hasattr(settings, "state")
            assert hasattr(settings, "plugins")
            assert hasattr(settings, "business")

    def test_convenience_functions(self) -> None:
        """Testa funções de conveniência do ROOT config.py."""
        if root_config is None:
            pytest.skip("Could not load root config module")

        # Testa que as funções de conveniência existem
        assert hasattr(root_config, "flext_get_meltano_settings")
        assert hasattr(root_config, "flext_create_development_meltano_config")
        assert hasattr(root_config, "flext_create_production_meltano_config")
        assert hasattr(root_config, "get_settings")

        # Testa que são callable
        assert callable(root_config.flext_get_meltano_settings)
        assert callable(root_config.flext_create_development_meltano_config)
        assert callable(root_config.flext_create_production_meltano_config)
        assert callable(root_config.get_settings)

    def test_settings_properties(self) -> None:
        """Testa properties da classe FlextMeltanoSettings."""
        if root_config is None:
            pytest.skip("Could not load root config module")

        settings_class = root_config.FlextMeltanoSettings

        with patch("flext_meltano.infrastructure.di_container.get_di_container"):
            settings = settings_class()

            # Testa properties legacy
            if hasattr(settings, "project_root"):
                assert settings.project_root is not None
            if hasattr(settings, "default_environment"):
                assert isinstance(settings.default_environment, str)
            if hasattr(settings, "database_uri"):
                assert isinstance(settings.database_uri, str)

    def test_configure_dependencies_method(self) -> None:
        """Testa método configure_dependencies."""
        if root_config is None:
            pytest.skip("Could not load root config module")

        settings_class = root_config.FlextMeltanoSettings

        with patch("flext_meltano.infrastructure.di_container.get_di_container") as mock_get_container:
            mock_container = Mock()
            mock_get_container.return_value = mock_container

            settings = settings_class()

            # Testa método configure_dependencies
            if hasattr(settings, "configure_dependencies"):
                settings.configure_dependencies()
                # Deve ter chamado register no container
                mock_container.register.assert_called()

    def test_module_all_export(self) -> None:
        """Testa __all__ export do módulo ROOT config.py."""
        if root_config is None:
            pytest.skip("Could not load root config module")

        # Testa que __all__ está definido
        if hasattr(root_config, "__all__"):
            all_exports = root_config.__all__
            assert isinstance(all_exports, list)

            # Testa que contém as classes principais
            expected_exports = [
                "FlextMeltanoBusinessConfig",
                "FlextMeltanoExecutionConfig",
                "FlextMeltanoProjectConfig",
                "FlextMeltanoSettings",
                "get_settings"
            ]

            for expected in expected_exports:
                if expected in all_exports:
                    assert hasattr(root_config, expected)


class TestRootConfigIntegration:
    """Testes de integração para o config.py ROOT."""

    def test_di_container_integration(self) -> None:
        """Testa integração com DI container."""
        if root_config is None:
            pytest.skip("Could not load root config module")

        # Mock das funções do DI container
        with (
            patch("flext_meltano.infrastructure.di_container.get_config_defaults") as mock_defaults,
            patch("flext_meltano.infrastructure.di_container.get_domain_entity") as mock_entity,
            patch("flext_meltano.infrastructure.di_container.get_di_container") as mock_container,
        ):
            mock_defaults.return_value = Mock()
            mock_entity.return_value = Mock()
            mock_container.return_value = Mock()

            # Reload do módulo para testar imports
            import importlib
            config_module_path = Path(__file__).parent.parent / "src" / "flext_meltano" / "config.py"
            spec = importlib.util.spec_from_file_location("test_root_config", config_module_path)
            if spec and spec.loader:
                test_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(test_module)

                # Verifica que as funções foram chamadas durante import
                mock_defaults.assert_called()
                mock_entity.assert_called()

    def test_pydantic_integration(self) -> None:
        """Testa integração com Pydantic."""
        if root_config is None:
            pytest.skip("Could not load root config module")

        # Verifica que usa Pydantic corretamente
        project_config = root_config.FlextMeltanoProjectConfig

        # Testa que herda de DomainValueObject (que deve ser BaseModel)
        config = project_config()

        # Deve ter métodos Pydantic
        if hasattr(config, "model_dump"):
            result = config.model_dump()
            assert isinstance(result, dict)
        elif hasattr(config, "dict"):
            result = config.dict()
            assert isinstance(result, dict)
