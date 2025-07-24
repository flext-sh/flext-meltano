"""Testes reais para integrations/bridge.py - COVERAGE DIRETO.

Objetivo: Gerar coverage real no arquivo integrations/bridge.py (188 statements, 0% coverage).
Target CRÍTICO de alto impacto para maximizar coverage improvement.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

# Import direto das classes REAIS do integrations/bridge.py
from flext_meltano.integrations.bridge import (
    FlextMeltanoBridge,
    FlextMeltanoResult,
)


class TestFlextMeltanoResult:
    """Testes reais da classe FlextMeltanoResult."""

    def test_result_creation_success(self) -> None:
        """Testa criação de resultado de sucesso."""
        result = FlextMeltanoResult(
            success=True,
            message="Operation completed successfully",
            data={"records": 100, "status": "completed"},
        )

        assert result.success is True
        assert result.message == "Operation completed successfully"
        assert result.data == {"records": 100, "status": "completed"}
        assert result.metadata is None
        assert result.error is None

    def test_result_creation_failure(self) -> None:
        """Testa criação de resultado de falha."""
        result = FlextMeltanoResult(
            success=False,
            message="Operation failed",
            error="Connection timeout",
        )

        assert result.success is False
        assert result.message == "Operation failed"
        assert result.error == "Connection timeout"
        assert result.data is None
        assert result.metadata is None

    def test_result_with_metadata(self) -> None:
        """Testa resultado com metadata."""
        metadata = {"execution_time": 45.2, "memory_usage": "120MB"}
        result = FlextMeltanoResult(
            success=True,
            message="Completed with metadata",
            metadata=metadata,
        )

        assert result.metadata == metadata
        assert result.success is True

    def test_result_to_dict(self) -> None:
        """Testa conversão para dict."""
        result = FlextMeltanoResult(
            success=True,
            message="Test message",
            data={"key": "value"},
            metadata={"version": "1.0"},
            error=None,
        )

        result_dict = result.to_dict()

        expected = {
            "success": True,
            "message": "Test message",
            "data": {"key": "value"},
            "metadata": {"version": "1.0"},
            "error": None,
        }
        assert result_dict == expected

    def test_result_to_dict_with_error(self) -> None:
        """Testa conversão para dict com erro."""
        result = FlextMeltanoResult(
            success=False,
            message="Failed operation",
            error="Invalid input",
        )

        result_dict = result.to_dict()

        expected = {
            "success": False,
            "message": "Failed operation",
            "data": None,
            "metadata": None,
            "error": "Invalid input",
        }
        assert result_dict == expected


class TestFlextMeltanoBridge:
    """Testes reais da classe FlextMeltanoBridge."""

    @pytest.fixture
    def mock_project_manager(self) -> Mock:
        """Cria mock do project manager."""
        mock = Mock()
        mock.create_project_bridge = AsyncMock()
        mock.add_plugin_bridge = AsyncMock()
        mock.run_pipeline_bridge = AsyncMock()
        mock.get_project_status = AsyncMock()
        return mock

    @pytest.fixture
    def mock_singer_direct(self) -> Mock:
        """Cria mock do singer direct runner."""
        mock = Mock()
        mock.run_tap = AsyncMock()
        mock.discover_schema = AsyncMock()
        return mock

    @pytest.fixture
    def bridge(self, mock_project_manager: Mock, mock_singer_direct: Mock) -> FlextMeltanoBridge:
        """Cria instância real do bridge com mocks."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager") as mock_pm_class,
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner") as mock_sdr_class,
        ):
            mock_pm_class.return_value = mock_project_manager
            mock_sdr_class.return_value = mock_singer_direct

            return FlextMeltanoBridge("/test/project")

    def test_bridge_initialization(self, bridge: FlextMeltanoBridge) -> None:
        """Testa inicialização do bridge."""
        assert bridge.project_root == Path("/test/project").resolve()
        assert bridge.logger is not None
        assert bridge.project_manager is not None
        assert bridge.singer_direct is not None

    def test_bridge_initialization_with_default_path(self) -> None:
        """Testa inicialização com path padrão."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager"),
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner"),
        ):
            bridge = FlextMeltanoBridge()
            assert bridge.project_root == Path.cwd()

    def test_is_available(self, bridge: FlextMeltanoBridge) -> None:
        """Testa verificação de disponibilidade."""
        result = bridge.is_available()
        assert result is True

    @pytest.mark.asyncio
    async def test_init_project_success(self, bridge: FlextMeltanoBridge) -> None:
        """Testa inicialização de projeto com sucesso."""
        # Mock successful project creation
        mock_result = Mock()
        mock_result.success = True
        bridge.project_manager.create_project_bridge.return_value = mock_result

        result_json = await bridge.init_project("test-project", "/test/dir")
        result = json.loads(result_json)

        assert result["success"] is True
        assert result["message"] == "Project initialized successfully"
        assert result["data"]["project_name"] == "test-project"
        assert result["data"]["project_dir"] == "/test/dir"

        bridge.project_manager.create_project_bridge.assert_called_once_with(
            project_name="test-project",
            environment="dev",
        )

    @pytest.mark.asyncio
    async def test_init_project_failure(self, bridge: FlextMeltanoBridge) -> None:
        """Testa inicialização de projeto com falha."""
        # Mock failed project creation
        mock_result = Mock()
        mock_result.success = False
        mock_result.error = "Project already exists"
        bridge.project_manager.create_project_bridge.return_value = mock_result

        result_json = await bridge.init_project("existing-project")
        result = json.loads(result_json)

        assert result["success"] is False
        assert result["message"] == "Failed to initialize"
        assert result["error"] == "Project already exists"

    @pytest.mark.asyncio
    async def test_init_project_exception(self, bridge: FlextMeltanoBridge) -> None:
        """Testa inicialização de projeto com exceção."""
        # Mock exception during project creation
        bridge.project_manager.create_project_bridge.side_effect = Exception("Unexpected error")

        result_json = await bridge.init_project("error-project")
        result = json.loads(result_json)

        assert result["success"] is False
        assert result["message"] == "Failed to initialize"
        assert result["error"] == "Unexpected error"

    @pytest.mark.asyncio
    async def test_init_project_without_project_dir(self, bridge: FlextMeltanoBridge) -> None:
        """Testa inicialização sem especificar diretório."""
        mock_result = Mock()
        mock_result.success = True
        bridge.project_manager.create_project_bridge.return_value = mock_result

        result_json = await bridge.init_project("no-dir-project")
        result = json.loads(result_json)

        assert result["success"] is True
        assert result["data"]["project_name"] == "no-dir-project"
        assert result["data"]["project_dir"] is None


class TestFlextMeltanoBridgeAdvanced:
    """Testes avançados para métodos específicos do bridge."""

    @pytest.fixture
    def bridge_with_mocks(self) -> FlextMeltanoBridge:
        """Cria bridge com todos os mocks necessários."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager") as mock_pm,
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner") as mock_sdr,
            patch("flext_meltano.config.settings.FlextMeltanoSettings"),
            patch("flext_meltano.infrastructure.di_container.get_di_container"),
        ):
            mock_pm_instance = Mock()
            mock_sdr_instance = Mock()
            mock_pm.return_value = mock_pm_instance
            mock_sdr.return_value = mock_sdr_instance

            bridge = FlextMeltanoBridge("/advanced/test")
            bridge.project_manager = mock_pm_instance
            bridge.singer_direct = mock_sdr_instance

            return bridge

    def test_bridge_project_root_resolution(self, bridge_with_mocks: FlextMeltanoBridge) -> None:
        """Testa resolução do project root."""
        assert bridge_with_mocks.project_root == Path("/advanced/test").resolve()

    def test_bridge_logger_configuration(self, bridge_with_mocks: FlextMeltanoBridge) -> None:
        """Testa configuração do logger."""
        assert bridge_with_mocks.logger is not None
        assert hasattr(bridge_with_mocks.logger, "info")
        assert hasattr(bridge_with_mocks.logger, "error")

    def test_result_json_serialization_complex(self) -> None:
        """Testa serialização JSON com dados complexos."""
        complex_data = {
            "nested": {"level1": {"level2": "value"}},
            "list": [1, 2, 3, {"item": "data"}],
            "numbers": [3.14, 42, -1],
            "booleans": [True, False],
        }

        result = FlextMeltanoResult(
            success=True,
            message="Complex data test",
            data=complex_data,
            metadata={"timestamp": "2024-01-01T00:00:00Z"},
        )

        result_dict = result.to_dict()
        json_str = json.dumps(result_dict)
        parsed_back = json.loads(json_str)

        assert parsed_back["success"] is True
        assert parsed_back["data"]["nested"]["level1"]["level2"] == "value"
        assert parsed_back["data"]["list"][3]["item"] == "data"
        assert parsed_back["metadata"]["timestamp"] == "2024-01-01T00:00:00Z"

    @pytest.mark.asyncio
    async def test_init_project_path_handling(self, bridge_with_mocks: FlextMeltanoBridge) -> None:
        """Testa manipulação de paths na inicialização."""
        mock_result = Mock()
        mock_result.success = True
        bridge_with_mocks.project_manager.create_project_bridge.return_value = mock_result

        # Test com path relativo
        result_json = await bridge_with_mocks.init_project("relative-project", "./relative/path")
        result = json.loads(result_json)

        assert result["success"] is True
        assert result["data"]["project_dir"] == "./relative/path"

        # Test com path absoluto
        result_json = await bridge_with_mocks.init_project("absolute-project", "/absolute/path")
        result = json.loads(result_json)

        assert result["success"] is True
        assert result["data"]["project_dir"] == "/absolute/path"

    def test_result_backwards_compatibility(self) -> None:
        """Testa compatibilidade com versões anteriores."""
        # Test que o campo 'error' ainda existe para compatibilidade
        result = FlextMeltanoResult(
            success=False,
            message="Compatibility test",
            error="Legacy error field",
        )

        result_dict = result.to_dict()
        assert "error" in result_dict
        assert result_dict["error"] == "Legacy error field"


class TestFlextMeltanoBridgeIntegration:
    """Testes de integração para o bridge."""

    def test_result_dataclass_fields(self) -> None:
        """Testa campos do dataclass Result."""
        result = FlextMeltanoResult(success=True)

        # Verifica que todos os campos esperados existem
        assert hasattr(result, "success")
        assert hasattr(result, "message")
        assert hasattr(result, "data")
        assert hasattr(result, "metadata")
        assert hasattr(result, "error")

        # Verifica valores padrão
        assert result.success is True
        assert result.message == ""
        assert result.data is None
        assert result.metadata is None
        assert result.error is None

    def test_bridge_component_integration(self) -> None:
        """Testa integração dos componentes do bridge."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager") as mock_pm,
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner") as mock_sdr,
        ):
            bridge = FlextMeltanoBridge("/integration/test")

            # Verifica que os componentes foram inicializados
            mock_pm.assert_called_once()
            mock_sdr.assert_called_once_with(Path("/integration/test").resolve())

            # Verifica que os atributos foram definidos
            assert hasattr(bridge, "project_manager")
            assert hasattr(bridge, "singer_direct")
            assert hasattr(bridge, "project_root")
            assert hasattr(bridge, "logger")

    def test_json_string_type_alias(self) -> None:
        """Testa que JSONStr é um alias válido para str."""
        from flext_meltano.integrations.bridge import JSONStr

        # JSONStr deve ser str
        assert JSONStr is str

        # Deve aceitar string values
        json_value: JSONStr = '{"test": "value"}'
        assert isinstance(json_value, str)
        assert json.loads(json_value) == {"test": "value"}
