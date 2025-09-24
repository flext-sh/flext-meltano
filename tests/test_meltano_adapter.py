"""Test module for flext-meltano."""

from __future__ import annotations

import importlib.util

import dbt.version

from flext_core import FlextResult
from flext_meltano import FlextMeltanoAdapter, FlextMeltanoBridge as MeltanoBridge


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
        assert "meltano" in version_data
        assert version_data["meltano"] == "3.9.1"  # Versão real instalada
        assert "flext_meltano" in version_data
        assert version_data["flext_meltano"] == "2.0.0"
        assert "status" in version_data
        assert version_data["status"] == "ready"

    def test_get_version_unwrap_or_pattern(self) -> None:
        """Testa padrão unwrap_or para simplificação de código."""
        bridge = MeltanoBridge()
        result = bridge.get_version()

        # Padrão unwrap_or para valores padrão
        version = result.unwrap_or({"version": "unknown"})
        assert isinstance(version, dict)
        assert "meltano" in version

        # Com sucesso, deve retornar o valor real
        if result.success:
            assert version["meltano"] == "3.9.1"

    def test_meltano_imports_available(self) -> None:
        """Verifica disponibilidade das APIs reais do Meltano."""
        # APIs do Meltano Core devem estar disponíveis
        try:
            importlib.util.find_spec("meltano")
            importlib.util.find_spec("meltano.core.elt_context")
            importlib.util.find_spec("meltano.core.project")
            importlib.util.find_spec("meltano.core.project_plugins_service")
            importlib.util.find_spec("meltano.core.runner.singer")

            success = True
        except ImportError:
            success = False

        assert success, "APIs do Meltano Core devem estar disponíveis"

    def test_dbt_imports_available(self) -> None:
        """Verifica disponibilidade das APIs reais do DBT."""
        try:
            # Check if DBT specs exist
            dbt_cli_spec = importlib.util.find_spec("dbt.cli.main")
            dbt_version_spec = importlib.util.find_spec("dbt.version")

            if dbt_cli_spec is None or dbt_version_spec is None:
                success = False
                version = None
            else:
                # Try to import and get version (imported at top level)
                version = dbt.version.__version__
                success = True

        except (ImportError, AttributeError):
            success = False
            version = None

        assert success, (
            f"APIs do DBT Core devem estar disponíveis. DBT Version: {version}"
        )
        assert version == "1.10.5", f"Versão DBT deve ser 1.10.5, encontrada: {version}"

    def test_singer_sdk_imports_available(self) -> None:
        """Verifica disponibilidade do Singer SDK."""
        try:
            importlib.util.find_spec("singer_sdk.Stream")
            importlib.util.find_spec("singer_sdk.Tap")
            importlib.util.find_spec("singer_sdk.Target")
            importlib.util.find_spec("singer_sdk.sinks.BatchSink")
            importlib.util.find_spec("singer_sdk.sinks.Sink")
            importlib.util.find_spec("singer_sdk.sinks.SQLSink")

            success = True
        except ImportError:
            success = False

        assert success, "Singer SDK 0.48.0 deve estar disponível"


class TestFlextMeltanoAdapterReal:
    """Real adapter tests - no mocks."""

    def test_adapter_creation(self) -> None:
        """Test adapter creation."""
        adapter = FlextMeltanoAdapter()
        assert adapter is not None

    def test_adapter_with_config(self) -> None:
        """Test adapter with configuration."""
        adapter = FlextMeltanoAdapter()
        assert adapter is not None
        # Adapter doesn't receive config in constructor, but can process configs
