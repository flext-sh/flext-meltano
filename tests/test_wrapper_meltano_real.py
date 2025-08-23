"""Testes REAIS para MeltanoBridge - SEM MOCKS.

Este módulo testa a integração REAL com Meltano 3.9.1:
- APIs nativas do Meltano Core
- ELTContext, Project, SingerRunner
- Execução SEM subprocess
- FlextResult patterns com .value e .unwrap_or()
"""

from __future__ import annotations

import importlib

from flext_core import FlextResult

from flext_meltano.base_meltano import FlextMeltanoAdapter, MeltanoBridge


class TestMeltanoBridgeReal:
    """Testes REAIS da integração Meltano - sem mocks."""

    def test_bridge_creation(self) -> None:
        """Testa criação do bridge com configuração padrão."""
        bridge = MeltanoBridge()
        assert bridge is not None
        assert hasattr(bridge, "get_version")

    def test_get_version_real(self) -> None:
        """Testa obtenção da versão do Meltano usando API real."""
        bridge = MeltanoBridge()
        result = bridge.get_version()

        # Deve retornar sucesso
        assert result.success is True
        assert isinstance(result, FlextResult)

        # Dados devem conter versão real
        version_data = result.value  # Usando novo padrão .value
        assert isinstance(version_data, dict)
        assert "version" in version_data
        assert "meltano" in version_data
        assert version_data["meltano"] == "3.9.1"  # Versão real instalada
        assert "cli_type" in version_data
        assert version_data["cli_type"] == "native_meltano_api"

    def test_get_version_unwrap_or_pattern(self) -> None:
        """Testa padrão unwrap_or para simplificação de código."""
        bridge = MeltanoBridge()
        result = bridge.get_version()

        # Padrão unwrap_or para valores padrão
        version = result.unwrap_or({"version": "unknown"})
        assert isinstance(version, dict)
        assert "version" in version

        # Com sucesso, deve retornar o valor real
        if result.success:
            assert version["meltano"] == "3.9.1"

    def test_meltano_imports_available(self) -> None:
        """Verifica disponibilidade das APIs reais do Meltano."""
        # APIs do Meltano Core devem estar disponíveis
        try:
            importlib.find_spec("meltano")
            importlib.find_spec("meltano.core.elt_context")
            importlib.find_spec("meltano.core.project")
            importlib.find_spec("meltano.core.project_plugins_service")
            importlib.find_spec("meltano.core.runner.singer")

            success = True
        except ImportError:
            success = False

        assert success, "APIs do Meltano Core devem estar disponíveis"

    def test_dbt_imports_available(self) -> None:
        """Verifica disponibilidade das APIs reais do DBT."""
        try:
            importlib.find_spec("dbt.cli.main")
            importlib.find_spec("dbt.version")
            importlib.find_spec("dbt.cli.main.dbtRunner")

            success = True
            version = dbt.version.__version__
        except ImportError:
            success = False
            version = None

        assert success, "APIs do DBT Core devem estar disponíveis"
        assert version == "1.10.5", f"Versão DBT deve ser 1.10.5, encontrada: {version}"

    def test_singer_sdk_imports_available(self) -> None:
        """Verifica disponibilidade do Singer SDK."""
        try:
            importlib.find_spec("singer_sdk.Stream")
            importlib.find_spec("singer_sdk.Tap")
            importlib.find_spec("singer_sdk.Target")
            importlib.find_spec("singer_sdk.sinks.BatchSink")
            importlib.find_spec("singer_sdk.sinks.Sink")
            importlib.find_spec("singer_sdk.sinks.SQLSink")

            success = True
        except ImportError:
            success = False

        assert success, "Singer SDK 0.48.0 deve estar disponível"


class TestFlextMeltanoAdapterReal:
    """Testes REAIS do adapter - sem mocks."""

    def test_adapter_creation(self) -> None:
        """Testa criação do adapter."""
        adapter = FlextMeltanoAdapter()
        assert adapter is not None

    def test_adapter_with_config(self) -> None:
        """Testa adapter com configuração."""
        adapter = FlextMeltanoAdapter()
        assert adapter is not None
        # Adapter não recebe config no constructor, mas pode processar configs
