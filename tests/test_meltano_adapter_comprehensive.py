"""Testes REAIS COMPREHENSIVE para MeltanoBridge - COVERAGE PRÓXIMO 100%.

Este módulo implementa testes REAIS para TODAS as funcionalidades do MeltanoBridge:
- Usando APIs nativas Meltano 3.9.1 - SEM MOCKS
- Cobrindo TODAS as funções públicas
- Usando FlextResult patterns (.value, .unwrap_or())
- Testando cenários de sucesso E erro
- Target: 85%+ coverage para base_meltano.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from flext_meltano.meltano_adapters import FlextMeltanoAdapter, MeltanoBridge


class TestMeltanoBridgeComprehensive:
    """Testes COMPREHENSIVE REAIS - SEM MOCKS."""

    def test_bridge_initialization(self) -> None:
        """Testa inicialização completa do bridge."""
        bridge = MeltanoBridge()

        # Propriedades básicas
        assert bridge is not None
        assert bridge._current_project is None
        assert hasattr(bridge, "logger")

        # Logger deve ser configurado corretamente
        logger = bridge.logger
        assert logger is not None
        assert hasattr(logger, "_name")
        assert logger._name == "MeltanoBridge"

    def test_execute_domain_service(self) -> None:
        """Testa execução como FlextDomainService."""
        bridge = MeltanoBridge()
        result = bridge.execute()

        # Deve retornar sucesso
        assert result.success is True

        # Usar padrão .value
        data = result.value
        assert isinstance(data, dict)
        assert data["service"] == "MeltanoBridge"
        assert data["status"] == "ready"

    def test_get_version_comprehensive(self) -> None:
        """Testa get_version com verificações completas."""
        bridge = MeltanoBridge()
        result = bridge.get_version()

        # Deve retornar sucesso
        assert result.success is True

        # Dados completos da versão
        version_data = result.value
        assert isinstance(version_data, dict)

        # Campos obrigatórios
        required_fields = ["version", "meltano", "cli_type"]
        for field in required_fields:
            assert field in version_data, f"Campo obrigatório ausente: {field}"

        # Valores corretos
        assert version_data["meltano"] == "3.9.1"
        assert version_data["cli_type"] == "native_meltano_api"
        assert version_data["version"] == version_data["meltano"]

    def test_create_temp_project_real(self) -> None:
        """Testa criação de projeto temporário REAL."""
        bridge = MeltanoBridge()

        # Acessar método privado para testar (necessário para coverage)
        project = bridge._create_temp_project()

        assert project is not None
        assert hasattr(project, "root")
        assert project.root.exists()
        assert project.root.is_dir()

        # Verificar estrutura do projeto
        meltano_yml = project.root / "meltano.yml"
        assert meltano_yml.exists()

    def test_initialize_project_with_existing_directory(self) -> None:
        """Testa inicialização de projeto com diretório existente."""
        bridge = MeltanoBridge()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Criar meltano.yml básico
            meltano_yml = project_root / "meltano.yml"
            meltano_yml.write_text("""
version: 1
project_id: test-project
environments:
- name: dev
""")

            result = bridge.initialize_project(project_root)

            # Deve retornar sucesso
            assert result.success is True

            # Projeto deve ser válido
            project = result.value
            assert project is not None
            assert hasattr(project, "root")
            # Projeto foi inicializado com sucesso - suficiente para verificar funcionalidade

    def test_initialize_project_without_meltano_yml(self) -> None:
        """Testa inicialização com diretório sem meltano.yml."""
        bridge = MeltanoBridge()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            result = bridge.initialize_project(project_root)

            # Deve falhar
            assert result.success is False
            assert result.error is not None
            assert "meltano.yml not found" in result.error

    def test_discover_plugins_real(self) -> None:
        """Testa descoberta de plugins usando API REAL."""
        bridge = MeltanoBridge()

        # Descobrir plugins (sem parâmetro plugin_type)
        result = bridge.discover_plugins()

        # Deve retornar sucesso (mesmo se lista vazia)
        assert result.success is True

        # Resultado deve ser lista
        plugins = result.value
        assert isinstance(plugins, list)

        # Se houver plugins, verificar estrutura
        if plugins:
            plugin = plugins[0]
            assert isinstance(plugin, dict)
            # Plugins do hub têm 'name' e outras propriedades
            assert "name" in plugin or "type" in plugin

    def test_discover_plugins_with_project(self) -> None:
        """Testa descoberta de plugins com projeto específico."""
        bridge = MeltanoBridge()

        # Criar projeto temporário para teste
        temp_project = bridge._create_temp_project()

        result = bridge.discover_plugins(_project=temp_project)

        # Deve retornar sucesso (mesmo se lista vazia)
        assert result.success is True

        # Resultado deve ser lista
        plugins = result.value
        assert isinstance(plugins, list)

    def test_discover_plugins_unwrap_or_pattern(self) -> None:
        """Testa padrão unwrap_or com discover_plugins."""
        bridge = MeltanoBridge()

        # Com sucesso
        result = bridge.discover_plugins()
        plugins = result.unwrap_or([])
        assert isinstance(plugins, list)

        # Testar com projeto None também
        result_none = bridge.discover_plugins(_project=None)
        plugins_none = result_none.unwrap_or([])
        assert isinstance(plugins_none, list)

    def test_list_installed_plugins_temp_project(self) -> None:
        """Testa listagem de plugins em projeto temporário."""
        bridge = MeltanoBridge()

        # Criar projeto temporário
        temp_project = bridge._create_temp_project()

        result = bridge.list_installed_plugins(temp_project)

        # Deve retornar sucesso mesmo sem plugins
        assert result.success is True

        # Lista pode estar vazia
        plugins = result.value
        assert isinstance(plugins, list)

    def test_install_plugin_with_invalid_directory(self) -> None:
        """Testa instalação de plugin com diretório inválido."""
        bridge = MeltanoBridge()

        invalid_path = Path("/invalid/path/that/does/not/exist")

        result = bridge.install_plugin(invalid_path, "extractor", "tap-csv")

        # Deve falhar por diretório não existir
        assert result.success is False
        assert result.error is not None
        assert "not found" in result.error.lower() or "failed" in result.error.lower()

    def test_execute_meltano_command_invalid_command(self) -> None:
        """Testa execução de comando inválido."""
        bridge = MeltanoBridge()

        # Criar diretório temporário para teste
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Criar meltano.yml mínimo
            meltano_yml = project_root / "meltano.yml"
            meltano_yml.write_text("""version: 1
project_id: test
""")

            result = bridge.execute_meltano_command_real(
                project_root, ["invalid_command", "args"]
            )

            # Deve falhar
            assert result.success is False
            assert result.error is not None
            assert (
                "invalid_command" in result.error.lower()
                or "failed" in result.error.lower()
                or "format not supported" in result.error.lower()
            )

    def test_create_project_real_with_adapter(self) -> None:
        """Testa criação de projeto REAL usando FlextMeltanoAdapter."""
        adapter = FlextMeltanoAdapter()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            project_name = "test-project"

            result = adapter.create_project_real(project_name, project_root)

            # Deve retornar sucesso
            assert result.success is True

            # Projeto deve ter sido criado
            project_info = result.value
            assert isinstance(project_info, dict)
            assert project_info["project_name"] == project_name
            assert "project_path" in project_info

    def test_create_project_real_invalid_directory(self) -> None:
        """Testa criação de projeto em diretório inválido."""
        adapter = FlextMeltanoAdapter()

        invalid_path = Path("/invalid/path/that/does/not/exist")
        project_name = "test-project"

        result = adapter.create_project_real(project_name, invalid_path)

        # Deve falhar
        assert result.success is False
        assert result.error is not None
        assert "failed" in result.error.lower() or "create" in result.error.lower()

    def test_run_elt_pipeline_without_project(self) -> None:
        """Testa execução de pipeline ELT sem projeto."""
        bridge = MeltanoBridge()

        result = bridge.run_elt_pipeline("tap-csv", "target-csv")

        # Deve falhar por não ter projeto
        assert result.success is False
        assert result.error is not None
        assert "project" in result.error.lower() or "not found" in result.error.lower()


class TestFlextMeltanoAdapterComprehensive:
    """Testes COMPREHENSIVE REAIS do FlextMeltanoAdapter."""

    def test_adapter_initialization(self) -> None:
        """Testa inicialização do adapter."""
        adapter = FlextMeltanoAdapter()

        assert adapter is not None
        assert hasattr(adapter, "adapt_plugin")
        assert hasattr(adapter, "adapt_project_config")

    def test_adapt_plugin_valid_data(self) -> None:
        """Testa adaptação de plugin com dados válidos."""
        plugin_data = {
            "name": "tap-csv",
            "namespace": "tap_csv",
            "pip_url": "git+https://github.com/example/tap-csv.git",
            "executable": "tap-csv",
        }

        result = FlextMeltanoAdapter.adapt_plugin(plugin_data)

        # Deve retornar sucesso
        assert result.success is True

        # Plugin adaptado
        adapted = result.value
        assert isinstance(adapted, dict)
        assert adapted["name"] == "tap-csv"
        assert "namespace" in adapted

    def test_adapt_plugin_missing_name(self) -> None:
        """Testa adaptação de plugin sem nome - deve funcionar com nome vazio."""
        plugin_data = {"pip_url": "some-url"}

        result = FlextMeltanoAdapter.adapt_plugin(plugin_data)

        # Deve retornar sucesso mesmo sem nome
        assert result.success is True

        # Deve ter nome vazio
        adapted = result.value
        assert adapted["name"] == ""

    def test_adapt_plugin_unwrap_or_pattern(self) -> None:
        """Testa padrão unwrap_or com adapt_plugin."""
        # Plugin válido
        valid_plugin = {"name": "tap-csv"}
        result = FlextMeltanoAdapter.adapt_plugin(valid_plugin)
        adapted = result.unwrap_or({})
        assert adapted != {}
        assert adapted["name"] == "tap-csv"

        # Plugin vazio - ainda retorna sucesso com campos vazios
        empty_plugin: dict[str, str] = {}
        result_empty = FlextMeltanoAdapter.adapt_plugin(empty_plugin)
        adapted_empty = result_empty.unwrap_or({"fallback": "true"})
        assert result_empty.success is True
        assert adapted_empty["name"] == ""  # Nome vazio mas estrutura válida

    def test_adapt_project_config_valid(self) -> None:
        """Testa adaptação de configuração de projeto."""
        config = {
            "project_id": "test-project",
            "version": 1,
            "environments": [{"name": "dev"}],
            "plugins": {
                "extractors": [{"name": "tap-csv"}],
                "loaders": [{"name": "target-csv"}],
            },
        }

        result = FlextMeltanoAdapter.adapt_project_config(config)

        # Deve retornar sucesso
        assert result.success is True

        # Config adaptada
        adapted = result.value
        assert isinstance(adapted, dict)
        assert adapted["project_id"] == "test-project"
        assert "version" in adapted

    def test_adapt_project_config_missing_project_id(self) -> None:
        """Testa adaptação sem project_id - não deve falhar pois project_id é opcional."""
        config: dict[str, object] = {"version": 1}

        result = FlextMeltanoAdapter.adapt_project_config(config)

        # Deve retornar sucesso mesmo sem project_id
        assert result.success is True

        # Deve ter project_id vazio
        adapted = result.value
        assert adapted["project_id"] == ""

    def test_adapter_error_handling_comprehensive(self) -> None:
        """Testa tratamento abrangente de erros."""
        # Teste com None
        result = FlextMeltanoAdapter.adapt_plugin(None)  # type: ignore[arg-type]
        assert result.success is False

        # Teste com tipo errado
        result = FlextMeltanoAdapter.adapt_plugin("invalid")  # type: ignore[arg-type]
        assert result.success is False


class TestMeltanoBridgeIntegration:
    """Testes de integração REAIS - end-to-end."""

    def test_full_workflow_project_creation_to_discovery(self) -> None:
        """Testa workflow completo: criação → inicialização → descoberta."""
        bridge = MeltanoBridge()
        adapter = FlextMeltanoAdapter()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            project_name = "integration-test"

            # 1. Criar projeto usando adapter
            create_result = adapter.create_project_real(project_name, project_root)
            assert create_result.success is True

            # Path do projeto criado
            created_project_path = project_root / project_name

            # 2. Inicializar projeto
            init_result = bridge.initialize_project(created_project_path)
            assert init_result.success is True

            # Obter projeto inicializado
            initialized_project = init_result.value

            # 3. Descobrir plugins disponíveis no hub (não plugins instalados)
            discover_result = bridge.discover_plugins(initialized_project)
            assert discover_result.success is True

            # Usar unwrap_or pattern
            plugins = discover_result.unwrap_or([])
            assert isinstance(plugins, list)
            # Deve ter plugins descobertos no hub
            assert len(plugins) > 0

    def test_version_and_discovery_integration(self) -> None:
        """Testa integração versão + descoberta."""
        bridge = MeltanoBridge()

        # 1. Verificar versão (deve funcionar sempre)
        version_result = bridge.get_version()
        assert version_result.success is True

        # 2. Descobrir plugins (deve funcionar com Meltano hub)
        discovery_result = bridge.discover_plugins()

        # Ambos devem usar mesma instância do Meltano
        version_data = version_result.value
        discovery_success = discovery_result.success

        assert version_data["meltano"] == "3.9.1"
        # Discovery pode falhar se não tiver acesso ao hub, mas version sempre funciona
        if discovery_success:
            plugins = discovery_result.value
            assert isinstance(plugins, list)
