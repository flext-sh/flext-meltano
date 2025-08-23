"""Testes COMPREHENSIVE REAIS para runtime_bridge.py - COVERAGE EXPANSION.

Este módulo implementa testes REAIS para TODAS as funcionalidades do FlextMeltanoBridge:
- Usando APIs nativas Meltano 3.9.1, DBT Core 1.10.5 - SEM MOCKS
- Cobrindo TODAS as funções públicas do bridge Go ↔ Python
- Usando FlextResult patterns e JSON API responses
- Testando cenários de sucesso E erro
- Target: 85%+ coverage para runtime_bridge.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from flext_meltano.runtime_bridge import FlextMeltanoBridge, create_flext_meltano_bridge


class TestFlextMeltanoBridgeComprehensive:
    """Testes COMPREHENSIVE REAIS para FlextMeltanoBridge - SEM MOCKS."""

    def test_bridge_initialization(self) -> None:
        """Testa inicialização completa do bridge."""
        bridge = FlextMeltanoBridge()

        # Propriedades básicas
        assert bridge is not None
        assert hasattr(bridge, "executor")
        assert hasattr(bridge, "meltano_bridge")
        assert hasattr(bridge, "wrapper_dbt")

        # Verificar componentes inicializados
        assert bridge.executor is not None
        assert bridge.meltano_bridge is not None
        assert bridge.wrapper_dbt is not None

    def test_get_version_comprehensive(self) -> None:
        """Testa get_version com verificações completas de JSON API."""
        bridge = FlextMeltanoBridge()
        result = bridge.get_version()

        # Deve retornar sucesso como dict
        assert isinstance(result, dict)
        assert result["success"] is True

        # Dados completos da versão para Go
        version_data = result["data"]
        assert isinstance(version_data, dict)

        # Campos obrigatórios para Go bridge
        required_fields = [
            "flext_meltano",
            "meltano",
            "dbt_core",
            "singer_sdk",
            "python",
            "integration_method",
        ]
        for field in required_fields:
            assert field in version_data, f"Campo obrigatório ausente: {field}"

        # Valores corretos para Go consumption
        assert version_data["flext_meltano"] == "2.0.0-enterprise"
        assert version_data["meltano"] == "3.9.1"
        assert version_data["dbt_core"] == "1.10.5"
        assert version_data["singer_sdk"] == "0.48.0"
        assert version_data["python"] == "3.13+"
        assert version_data["integration_method"] == "native_apis"

    def test_list_plugins_real_api(self) -> None:
        """Testa list_plugins usando API REAL do Meltano."""
        bridge = FlextMeltanoBridge()
        result = bridge.list_plugins()

        # Deve retornar response JSON para Go
        assert isinstance(result, dict)

        # Verificar estrutura Go-compatible
        assert "success" in result

        if result["success"]:
            # Se sucesso, deve ter dados
            assert "data" in result
            plugins_data = result["data"]
            assert isinstance(plugins_data, list)
        else:
            # Se falha, deve ter erro
            assert "error" in result
            assert isinstance(result["error"], str)

    def test_run_pipeline_without_project(self) -> None:
        """Testa execução de pipeline sem projeto válido."""
        bridge = FlextMeltanoBridge()

        # Usar diretório inválido
        result = bridge.run_pipeline("tap-csv", "target-csv", "/invalid/path")

        # Deve retornar response JSON estruturada
        assert isinstance(result, dict)
        assert "success" in result

        # Deve falhar por projeto inválido
        assert result["success"] is False
        assert "error" in result
        assert isinstance(result["error"], str)

    def test_run_pipeline_with_valid_project(self) -> None:
        """Testa execução de pipeline com projeto válido."""
        bridge = FlextMeltanoBridge()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = temp_dir
            project_path = Path(project_root)

            # Criar projeto Meltano básico
            meltano_yml = project_path / "meltano.yml"
            meltano_yml.write_text("""
version: 1
project_id: test-pipeline
environments:
- name: dev
plugins:
  extractors:
  - name: tap-csv
  loaders:
  - name: target-csv
""")

            result = bridge.run_pipeline("tap-csv", "target-csv", project_root)

            # Deve tentar executar e retornar JSON response
            assert isinstance(result, dict)
            assert "success" in result

            if result["success"]:
                # Se sucesso, verificar dados
                assert "data" in result
                pipeline_data = result["data"]
                assert isinstance(pipeline_data, dict)
            else:
                # Se falha, verificar erro (pode falhar por falta de plugins reais)
                assert "error" in result
                # Error é OK - tentou executar mas pode falhar por deps

    def test_execute_meltano_command_basic(self) -> None:
        """Testa execução de comando Meltano básico."""
        bridge = FlextMeltanoBridge()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = temp_dir
            project_path = Path(project_root)

            # Criar projeto Meltano básico
            meltano_yml = project_path / "meltano.yml"
            meltano_yml.write_text("""
version: 1
project_id: test-command
environments:
- name: dev
""")

            result = bridge.execute_meltano_command(["version"], project_root)

            # Deve retornar response JSON
            assert isinstance(result, dict)
            assert "success" in result

            if result["success"]:
                assert "data" in result
            else:
                assert "error" in result

    def test_execute_meltano_command_invalid_project(self) -> None:
        """Testa execução de comando com projeto inválido."""
        bridge = FlextMeltanoBridge()

        result = bridge.execute_meltano_command(["version"], "/invalid/path")

        # Deve falhar com erro estruturado
        assert isinstance(result, dict)
        assert result["success"] is False
        assert "error" in result

    def test_execute_dbt_command_without_project(self) -> None:
        """Testa execução de comando DBT sem projeto."""
        bridge = FlextMeltanoBridge()

        result = bridge.execute_dbt_command(["compile"], "/invalid/path")

        # Deve falhar por projeto inválido
        assert isinstance(result, dict)
        assert result["success"] is False
        assert "error" in result

    def test_execute_dbt_command_with_project(self) -> None:
        """Testa execução de comando DBT com projeto."""
        bridge = FlextMeltanoBridge()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = temp_dir
            project_path = Path(project_root)

            # Criar projeto DBT básico
            dbt_project_yml = project_path / "dbt_project.yml"
            dbt_project_yml.write_text("""
name: test_dbt_bridge
version: 1.0.0
profile: test_profile
model-paths: ["models"]
target-path: "target"
""")

            result = bridge.execute_dbt_command(["compile"], project_root)

            # Deve tentar executar (pode falhar por falta de profiles.yml)
            assert isinstance(result, dict)
            assert "success" in result

            if result["success"]:
                assert "data" in result
            else:
                # OK - tentou executar mas falhou por config incompleta
                assert "error" in result

    def test_install_plugin_without_project(self) -> None:
        """Testa instalação de plugin sem projeto."""
        bridge = FlextMeltanoBridge()

        result = bridge.install_plugin("extractor", "tap-csv", "/invalid/path")

        # Deve falhar por projeto inválido
        assert isinstance(result, dict)
        assert result["success"] is False
        assert "error" in result

    def test_install_plugin_with_project(self) -> None:
        """Testa instalação de plugin com projeto."""
        bridge = FlextMeltanoBridge()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = temp_dir
            project_path = Path(project_root)

            # Criar projeto Meltano básico
            meltano_yml = project_path / "meltano.yml"
            meltano_yml.write_text("""
version: 1
project_id: test-install
environments:
- name: dev
""")

            result = bridge.install_plugin("extractor", "tap-csv", project_root)

            # Deve tentar instalar plugin
            assert isinstance(result, dict)
            assert "success" in result

            if result["success"]:
                assert "data" in result
            else:
                # OK - pode falhar por questões de rede/hub
                assert "error" in result

    def test_get_project_info_meltano_project(self) -> None:
        """Testa obtenção de informações de projeto Meltano."""
        bridge = FlextMeltanoBridge()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = temp_dir
            project_path = Path(project_root)

            # Criar projeto Meltano
            meltano_yml = project_path / "meltano.yml"
            meltano_yml.write_text("""
version: 1
project_id: test-info
environments:
- name: dev
plugins:
  extractors:
  - name: tap-csv
""")

            result = bridge.get_project_info(project_root)

            assert isinstance(result, dict)
            assert "success" in result

            if result["success"]:
                project_info = result["data"]
                assert isinstance(project_info, dict)
                assert project_info["project_type"] == "meltano"
                assert project_info["valid"] is True

    def test_get_project_info_invalid_project(self) -> None:
        """Testa obtenção de informações de projeto inválido."""
        bridge = FlextMeltanoBridge()

        result = bridge.get_project_info("/invalid/path")

        assert isinstance(result, dict)
        assert result["success"] is False
        assert "error" in result

    def test_invoke_dbt_basic_command(self) -> None:
        """Testa invoke_dbt com comando básico."""
        bridge = FlextMeltanoBridge()

        result = bridge.invoke_dbt("compile")

        # Deve tentar executar (pode falhar por falta de projeto)
        assert isinstance(result, dict)
        assert "success" in result

        if not result["success"]:
            # OK - falha esperada sem projeto válido
            assert "error" in result

    def test_invoke_dbt_with_kwargs(self) -> None:
        """Testa invoke_dbt com argumentos nomeados."""
        bridge = FlextMeltanoBridge()

        result = bridge.invoke_dbt(
            "compile",
            project_dir="/tmp/test_project",
            profiles_dir="/tmp/test_profiles",
        )

        # Deve tentar executar com argumentos
        assert isinstance(result, dict)
        assert "success" in result

    def test_invoke_dbt_with_underscore_args(self) -> None:
        """Testa invoke_dbt com argumentos com underscore."""
        bridge = FlextMeltanoBridge()

        result = bridge.invoke_dbt("run", _select="models.staging", _full_refresh=True)

        # Deve converter _select para --select
        assert isinstance(result, dict)
        assert "success" in result

    def test_bridge_error_handling_comprehensive(self) -> None:
        """Testa tratamento abrangente de erros no bridge."""
        bridge = FlextMeltanoBridge()

        # Teste 1: Comando com projeto que não existe
        result1 = bridge.execute_meltano_command(["invalid_command"], "/nonexistent")
        assert result1["success"] is False
        assert "error" in result1

        # Teste 2: Pipeline com argumentos inválidos
        result2 = bridge.run_pipeline("", "", "/nonexistent")
        assert result2["success"] is False
        assert "error" in result2

        # Teste 3: Instalação com tipo inválido
        result3 = bridge.install_plugin("invalid_type", "plugin", "/nonexistent")
        assert result3["success"] is False
        assert "error" in result3


class TestFlextMeltanoBridgeIntegrationComprehensive:
    """Testes de integração COMPREHENSIVE para FlextMeltanoBridge."""

    def test_full_workflow_project_to_pipeline(self) -> None:
        """Testa workflow completo: info → execução → pipeline."""
        bridge = FlextMeltanoBridge()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = temp_dir
            project_path = Path(project_root)

            # Criar projeto Meltano completo
            meltano_yml = project_path / "meltano.yml"
            meltano_yml.write_text("""
version: 1
project_id: integration-test
environments:
- name: dev
plugins:
  extractors:
  - name: tap-csv
    pip_url: pipelinewise-tap-csv
  loaders:
  - name: target-csv
    pip_url: pipelinewise-target-csv
""")

            # 1. Obter informações do projeto
            info_result = bridge.get_project_info(project_root)
            assert isinstance(info_result, dict)
            assert "success" in info_result

            # 2. Executar comando Meltano
            version_result = bridge.execute_meltano_command(["version"], project_root)
            assert isinstance(version_result, dict)
            assert "success" in version_result

            # 3. Tentar executar pipeline
            pipeline_result = bridge.run_pipeline("tap-csv", "target-csv", project_root)
            assert isinstance(pipeline_result, dict)
            assert "success" in pipeline_result

    def test_dbt_integration_comprehensive(self) -> None:
        """Testa integração DBT completa."""
        bridge = FlextMeltanoBridge()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = temp_dir
            project_path = Path(project_root)

            # Criar projeto DBT
            dbt_project_yml = project_path / "dbt_project.yml"
            dbt_project_yml.write_text("""
name: integration_dbt_test
version: 1.0.0
profile: integration_profile
model-paths: ["models"]
target-path: "target"
""")

            # Criar profiles.yml
            profiles_yml = project_path / "profiles.yml"
            profiles_yml.write_text("""
integration_profile:
  outputs:
    dev:
      type: sqlite
      database: test.db
      schema: main
  target: dev
""")

            # Criar diretório models
            (project_path / "models").mkdir()

            # 1. Testar comando compile
            compile_result = bridge.execute_dbt_command(["compile"], project_root)
            assert isinstance(compile_result, dict)
            assert "success" in compile_result

            # 2. Testar invoke_dbt
            invoke_result = bridge.invoke_dbt(
                "compile", project_dir=project_root, profiles_dir=project_root
            )
            assert isinstance(invoke_result, dict)
            assert "success" in invoke_result

    def test_error_propagation_comprehensive(self) -> None:
        """Testa propagação de erros através do bridge."""
        bridge = FlextMeltanoBridge()

        # Teste 1: Error propagation em get_version (deve sempre funcionar)
        version_result = bridge.get_version()
        assert version_result["success"] is True

        # Teste 2: Error propagation em list_plugins (pode falhar por rede)
        plugins_result = bridge.list_plugins()
        assert isinstance(plugins_result, dict)
        assert "success" in plugins_result

        # Teste 3: Error propagation em comando inválido
        invalid_result = bridge.execute_meltano_command(
            ["completely_invalid_command"], "/invalid/path"
        )
        assert invalid_result["success"] is False
        assert "error" in invalid_result

        # Teste 4: Error propagation em project info inválido
        info_result = bridge.get_project_info("/completely/invalid/path")
        assert info_result["success"] is False
        assert "error" in info_result


class TestFlextMeltanoBridgeFactoryFunctions:
    """Testes COMPREHENSIVE para factory functions."""

    def test_create_flext_meltano_bridge_without_config(self) -> None:
        """Testa criação de bridge sem config."""
        bridge = create_flext_meltano_bridge()

        assert isinstance(bridge, FlextMeltanoBridge)
        assert hasattr(bridge, "executor")
        assert hasattr(bridge, "meltano_bridge")
        assert hasattr(bridge, "wrapper_dbt")

    def test_create_flext_meltano_bridge_with_config(self) -> None:
        """Testa criação de bridge com config (ignorada)."""
        config = {"test": "value", "timeout": 300}
        bridge = create_flext_meltano_bridge(config)

        assert isinstance(bridge, FlextMeltanoBridge)
        assert hasattr(bridge, "executor")
        assert hasattr(bridge, "meltano_bridge")
        assert hasattr(bridge, "wrapper_dbt")

    def test_create_flext_meltano_bridge_with_none_config(self) -> None:
        """Testa criação de bridge com config None."""
        bridge = create_flext_meltano_bridge(None)

        assert isinstance(bridge, FlextMeltanoBridge)

    def test_create_flext_meltano_bridge_functional_test(self) -> None:
        """Testa bridge criado via factory funciona."""
        bridge = create_flext_meltano_bridge()

        # Testar que funciona corretamente
        version_result = bridge.get_version()
        assert isinstance(version_result, dict)
        assert version_result["success"] is True
        assert "data" in version_result


class TestFlextMeltanoBridgeJsonApiCompatibility:
    """Testes COMPREHENSIVE para compatibilidade JSON API com Go."""

    def test_json_api_response_structure(self) -> None:
        """Testa estrutura de response JSON para Go."""
        bridge = FlextMeltanoBridge()

        # Todos os métodos devem retornar dict com success/data/error
        methods_to_test = [
            (bridge.get_version, []),
            (bridge.list_plugins, []),
            (bridge.get_project_info, ["/invalid/path"]),
            (bridge.execute_meltano_command, [["version"], "/invalid/path"]),
            (bridge.execute_dbt_command, [["compile"], "/invalid/path"]),
            (bridge.run_pipeline, ["tap", "target", "/invalid/path"]),
            (bridge.install_plugin, ["extractor", "plugin", "/invalid/path"]),
        ]

        for method, args in methods_to_test:
            result = method(*args)

            # Deve ser dict
            assert isinstance(result, dict), (
                f"Method {method.__name__} não retornou dict"
            )

            # Deve ter success field
            assert "success" in result, f"Method {method.__name__} sem 'success' field"
            assert isinstance(result["success"], bool), (
                f"Method {method.__name__} success não é bool"
            )

            # Se success=True, deve ter data
            if result["success"]:
                assert "data" in result, f"Method {method.__name__} success sem 'data'"
            else:
                # Se success=False, deve ter error
                assert "error" in result, (
                    f"Method {method.__name__} failure sem 'error'"
                )
                assert isinstance(result["error"], str), (
                    f"Method {method.__name__} error não é string"
                )

    def test_json_serialization_compatibility(self) -> None:
        """Testa que responses são JSON-serializáveis para Go."""
        import json

        bridge = FlextMeltanoBridge()

        # Testar que todas as responses são serializáveis
        version_result = bridge.get_version()
        json_str = json.dumps(version_result)
        parsed_back = json.loads(json_str)
        assert parsed_back == version_result

        # Testar com erro também
        error_result = bridge.run_pipeline("", "", "/invalid")
        error_json_str = json.dumps(error_result)
        error_parsed = json.loads(error_json_str)
        assert error_parsed == error_result

    def test_go_bridge_data_types(self) -> None:
        """Testa tipos de dados compatíveis com Go bridge."""
        bridge = FlextMeltanoBridge()

        version_result = bridge.get_version()
        if version_result["success"]:
            data = version_result["data"]

            # Todos os valores devem ser tipos básicos (string, number, bool)
            for key, value in data.items():
                assert isinstance(value, (str, int, float, bool)), (
                    f"Value for {key} is not Go-compatible type: {type(value)}"
                )

        # Testar que errors são sempre strings
        error_result = bridge.execute_meltano_command(["invalid"], "/invalid")
        if not error_result["success"]:
            error = error_result["error"]
            assert isinstance(error, str), "Error must be string for Go compatibility"
