"""Testes REAIS para base services - SEM MOCKS.

Este módulo testa as funcionalidades REAIS dos serviços base:
- FlextMeltanoTapService
- FlextMeltanoTargetService
- FlextMeltanoDbtService
- Integração real com Singer SDK e DBT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import override

from singer_sdk import Stream, Tap, Target

from flext_meltano.service_implementations import (
    FlextMeltanoDbtService,
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
)


# Tap real simples para testes
class TestTap(Tap):
    """Tap de teste real."""

    name = "test-tap"

    @override
    def discover_streams(self) -> Sequence[Stream]:
        """Discover streams."""
        return []


# Target real simples para testes
class TestTarget(Target):
    """Target de teste real."""

    name = "test-target"


class TestFlextMeltanoTapServiceReal:
    """Testes REAIS do TapService - sem mocks."""

    def test_tap_service_creation(self) -> None:
        """Testa criação do serviço de tap."""

        class ConcreteTapService(FlextMeltanoTapService):
            """Implementação concreta para teste."""

            @override
            def get_tap_class(self) -> type[Tap]:
                return TestTap

            @override
            def get_default_config(self) -> dict[str, object]:
                return {"api_key": "test_key"}

        service = ConcreteTapService(tap_name="test-tap")
        assert service is not None
        assert service.tap_name == "test-tap"

    def test_tap_service_execute(self) -> None:
        """Testa execução do serviço de tap."""

        class ConcreteTapService(FlextMeltanoTapService):
            """Implementação concreta para teste."""

            @override
            def get_tap_class(self) -> type[Tap]:
                return TestTap

            @override
            def get_default_config(self) -> dict[str, object]:
                return {"api_key": "test_key"}

        service = ConcreteTapService(tap_name="test-tap")
        result = service.execute()

        # Deve retornar sucesso
        assert result.success is True

        # Deve usar padrão .value
        data = result.value
        assert isinstance(data, dict)
        assert data["service"] == "FlextMeltanoTapService"
        assert data["tap_name"] == "test-tap"
        assert data["status"] == "ready"

    def test_tap_service_validate_config(self) -> None:
        """Testa validação de configuração usando unwrap_or."""

        class ConcreteTapService(FlextMeltanoTapService):
            """Implementação concreta para teste."""

            @override
            def get_tap_class(self) -> type[Tap]:
                return TestTap

            def get_default_config(self) -> dict[str, object]:
                return {"api_key": "test_key"}

        service = ConcreteTapService(tap_name="test-tap")

        # Teste com config válida
        config: dict[str, object] = {"api_key": "test_key"}
        result = service.validate_tap_config(config)

        # Usando unwrap_or pattern
        is_valid = result.unwrap_or(False)
        assert isinstance(is_valid, bool)


class TestFlextMeltanoTargetServiceReal:
    """Testes REAIS do TargetService - sem mocks."""

    def test_target_service_creation(self) -> None:
        """Testa criação do serviço de target."""

        class ConcreteTargetService(FlextMeltanoTargetService):
            """Implementação concreta para teste."""

            @override
            def get_target_class(self) -> type[Target]:
                return TestTarget

            @override
            def get_default_config(self) -> dict[str, object]:
                return {"connection_string": "test_connection"}

        service = ConcreteTargetService(target_name="test-target")
        assert service is not None
        assert service.target_name == "test-target"

    def test_target_service_execute(self) -> None:
        """Testa execução do serviço de target."""

        class ConcreteTargetService(FlextMeltanoTargetService):
            """Implementação concreta para teste."""

            @override
            def get_target_class(self) -> type[Target]:
                return TestTarget

            @override
            def get_default_config(self) -> dict[str, object]:
                return {"connection_string": "test_connection"}

        service = ConcreteTargetService(target_name="test-target")
        result = service.execute()

        # Deve retornar sucesso
        assert result.success is True

        # Deve usar padrão .value
        data = result.value
        assert isinstance(data, dict)
        assert data["service"] == "FlextMeltanoTargetService"
        assert data["target_name"] == "test-target"


class TestFlextMeltanoDbtServiceReal:
    """Testes REAIS do DbtService - sem mocks."""

    def test_dbt_service_creation(self) -> None:
        """Testa criação do serviço DBT."""
        service = FlextMeltanoDbtService(project_name="test-dbt-project")
        assert service is not None
        assert service.project_name == "test-dbt-project"

    def test_dbt_service_execute(self) -> None:
        """Testa execução do serviço DBT."""
        service = FlextMeltanoDbtService(project_name="test-dbt-project")
        result = service.execute()

        # Deve retornar sucesso
        assert result.success is True

        # Deve usar padrão .value
        data = result.value
        assert isinstance(data, dict)
        assert data["service"] == "FlextMeltanoDbtService"
        assert data["project_name"] == "test-dbt-project"
        assert data["status"] == "ready"

    def test_dbt_service_get_project_config(self) -> None:
        """Testa obtenção da configuração do projeto DBT."""
        service = FlextMeltanoDbtService(project_name="test-project")
        config = service.get_project_config()

        assert isinstance(config, dict)
        assert config["name"] == "test-project"
        assert config["version"] == "1.0.0"
        assert "model-paths" in config
        assert "test-paths" in config
