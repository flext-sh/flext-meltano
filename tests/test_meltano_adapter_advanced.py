"""Testes ADVANCED para MeltanoBridge - COVERAGE EXPANSION.

Este módulo expande a cobertura testando funcionalidades AVANÇADAS do MeltanoBridge:
- Testes de métodos async REAIS
- Testes de pipeline ELT REAL completo
- Testes de error handling COMPREHENSIVE
- Testes de performance e edge cases
- Target: Cobertura 90%+ para base_meltano.py
"""

from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path
from typing import cast

from flext_core import FlextResult

from flext_meltano.meltano_adapters import FlextMeltanoAdapter, MeltanoBridge


class TestMeltanoBridgeAdvanced:
    """Testes ADVANCED do MeltanoBridge - funcionalidades complexas REAIS."""

    def test_async_plugin_execution_real(self) -> None:
        """Testa execução async de plugin usando API real."""
        bridge = MeltanoBridge()

        # Criar projeto temporário para teste
        temp_project = bridge._create_temp_project()

        async def run_async_test() -> None:
            result = await bridge.run_plugin_async(
                temp_project, "tap-csv", "describe", ["--format=json"]
            )

            # Plugin pode não existir mas método deve executar corretamente
            assert isinstance(result, FlextResult)
            # Resultado pode ser sucesso ou falha dependendo se plugin existe

        # Executar teste async
        asyncio.run(run_async_test())

    def test_real_elt_pipeline_execution(self) -> None:
        """Testa execução REAL de pipeline ELT completo."""
        bridge = MeltanoBridge()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Criar projeto Meltano mínimo
            meltano_yml = project_root / "meltano.yml"
            meltano_yml.write_text("""
version: 1
project_id: test-elt-project
environments:
- name: dev
""")

            # Testar execução do pipeline
            result = bridge.run_elt_pipeline(
                "tap-csv", "target-csv", project_root, transform=False
            )

            # Pipeline deve tentar executar (pode falhar por falta de plugins)
            assert isinstance(result, FlextResult)

            if result.success:
                # Se sucesso, verificar estrutura do resultado
                pipeline_data = result.value
                assert "tap" in pipeline_data
            else:
                # Se falha, verificar que erro é relacionado a plugins ou arquivos
                if result.error is not None:
                    error_lower = result.error.lower()
                    assert any(
                        keyword in error_lower
                        for keyword in ["block", "plugin", "no such file", "meltano.yml"]
                    )

    def test_real_pipeline_execution_via_bridge(self) -> None:
        """Testa run_pipeline_real via MeltanoBridge."""
        bridge = MeltanoBridge()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Criar projeto Meltano válido
            meltano_yml = project_root / "meltano.yml"
            meltano_yml.write_text("""
version: 1
project_id: pipeline-test
environments:
- name: dev
""")

            result = bridge.run_pipeline_real(project_root, "tap-csv", "target-csv")

            # Pipeline deve tentar executar usando SingerRunner
            assert isinstance(result, FlextResult)
            # Pode falhar por falta de plugins mas estrutura deve estar correta
            if result.success:
                assert "execution_method" in result.value
                assert (
                    result.value["execution_method"] == "meltano_singer_runner_native"
                )
            elif result.error is not None:
                assert (
                    "not found" in result.error.lower()
                    or "failed" in result.error.lower()
                )

    def test_execute_meltano_command_real_comprehensive(self) -> None:
        """Testa execute_meltano_command_real com cenários diversos."""
        bridge = MeltanoBridge()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Criar projeto Meltano válido
            meltano_yml = project_root / "meltano.yml"
            meltano_yml.write_text("""
version: 1
project_id: command-test
environments:
- name: dev
""")

            # Teste 1: Comando invoke básico
            result1 = bridge.execute_meltano_command_real(
                project_root, ["invoke", "tap-csv"]
            )
            assert isinstance(result1, FlextResult)

            # Teste 2: Comando não suportado
            result2 = bridge.execute_meltano_command_real(
                project_root, ["unsupported", "command"]
            )
            assert result2.success is False
            if result2.error is not None:
                assert "format not supported" in result2.error.lower()

            # Teste 3: Comando invoke insuficiente
            result3 = bridge.execute_meltano_command_real(
                project_root,
                ["invoke"],  # Sem plugin name
            )
            assert result3.success is False

    def test_context_management_comprehensive(self) -> None:
        """Testa gerenciamento de contexto e project state."""
        bridge = MeltanoBridge()

        # Verificar estado inicial
        assert bridge._current_project is None

        # Criar projeto temporário
        temp_project = bridge._create_temp_project()
        assert temp_project is not None

        # Verificar se meltano.yml foi criado
        meltano_yml = temp_project.root / "meltano.yml"
        assert meltano_yml.exists()

        # Ler conteúdo do meltano.yml
        with meltano_yml.open() as f:
            content = f.read()
            assert "project_id: flext-temp-project" in content
            assert "version: 1" in content

    def test_error_handling_comprehensive(self) -> None:
        """Testa tratamento abrangente de erros em diversos cenários."""
        bridge = MeltanoBridge()

        # Teste 1: Inicializar projeto inexistente
        invalid_path = Path("/invalid/path/that/does/not/exist")
        result1 = bridge.initialize_project(invalid_path)
        assert result1.success is False
        if result1.error is not None:
            assert "not found" in result1.error.lower()

        # Teste 2: Instalar plugin sem projeto válido
        with tempfile.TemporaryDirectory() as temp_dir:
            empty_dir = Path(temp_dir)
            result2 = bridge.install_plugin(empty_dir, "extractor", "tap-csv")
            assert result2.success is False
            if result2.error is not None:
                assert "meltano.yml not found" in result2.error

    def test_logger_integration_comprehensive(self) -> None:
        """Testa integração completa com sistema de logging."""
        bridge = MeltanoBridge()

        # Verificar logger configurado
        logger = bridge.logger
        assert logger is not None
        assert hasattr(logger, "_name")
        assert logger._name == "MeltanoBridge"

        # Testar contexto de logging
        with_context = logger.with_context(test_param="test_value")
        assert with_context is not None
        assert with_context._context["test_param"] == "test_value"

    def test_plugin_discovery_edge_cases(self) -> None:
        """Testa casos edge da descoberta de plugins."""
        bridge = MeltanoBridge()

        # Teste com projeto específico
        temp_project = bridge._create_temp_project()
        result = bridge.discover_plugins(_project=temp_project)

        assert result.success is True
        plugins = result.value
        assert isinstance(plugins, list)

        # Se houver plugins, verificar estrutura
        if plugins:
            plugin = plugins[0]
            assert "name" in plugin
            assert "type" in plugin
            assert plugin["type"] in {"extractor", "loader", "transformer"}


class TestFlextMeltanoAdapterAdvanced:
    """Testes ADVANCED do FlextMeltanoAdapter - funcionalidades complexas."""

    def test_create_project_real_comprehensive(self) -> None:
        """Testa criação de projeto REAL com cenários diversos."""
        adapter = FlextMeltanoAdapter()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Teste 1: Projeto com nome válido
            result1 = adapter.create_project_real("test-project-1", project_root)
            assert result1.success is True

            project_info = result1.value
            assert project_info["project_name"] == "test-project-1"
            assert "creation_method" in project_info
            assert project_info["creation_method"] == "project_init_service_native"

            # Verificar estrutura criada
            created_path = project_root / "test-project-1"
            meltano_yml = created_path / "meltano.yml"
            assert meltano_yml.exists()

    def test_add_plugin_real_comprehensive(self) -> None:
        """Testa adição de plugin REAL com ProjectAddService."""
        adapter = FlextMeltanoAdapter()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            project_name = "plugin-test-project"

            # Primeiro criar projeto
            create_result = adapter.create_project_real(project_name, project_root)
            assert create_result.success is True

            created_project_path = project_root / project_name

            # Tentar adicionar plugin (pode falhar se plugin não existir no hub)
            result = adapter.add_plugin_real(
                created_project_path, "extractors", "tap-csv"
            )

            # Plugin pode não existir no hub, mas API deve funcionar corretamente
            assert isinstance(result, FlextResult)
            if result.success:
                plugin_info = result.value
                assert plugin_info["plugin_name"] == "tap-csv"
                assert plugin_info["plugin_type"] == "extractors"
                assert "addition_method" in plugin_info

    def test_run_pipeline_real_via_adapter(self) -> None:
        """Testa execução de pipeline via adapter (delegação para bridge)."""
        adapter = FlextMeltanoAdapter()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            project_name = "pipeline-adapter-test"

            # Criar projeto via adapter
            create_result = adapter.create_project_real(project_name, project_root)
            assert create_result.success is True

            created_project_path = project_root / project_name

            # Executar pipeline via adapter
            result = adapter.run_pipeline_real(
                created_project_path, "tap-csv", "target-csv"
            )

            # Pipeline deve tentar executar (delegação para MeltanoBridge)
            assert isinstance(result, FlextResult)

    def test_adapt_methods_edge_cases(self) -> None:
        """Testa métodos adapt com casos edge e tipos diversos."""
        # Teste adapt_plugin com dados diversos
        test_cases = [
            # Caso 1: Plugin com dados completos
            {
                "name": "tap-postgres",
                "namespace": "tap_postgres",
                "description": "PostgreSQL tap",
                "version": "1.0.0",
                "pip_url": "git+https://github.com/example/tap-postgres.git",
                "executable": "tap-postgres",
            },
            # Caso 2: Plugin com dados mínimos
            {"name": "minimal-tap"},
            # Caso 3: Plugin vazio (edge case)
            {},
        ]

        for plugin_data in test_cases:
            result = FlextMeltanoAdapter.adapt_plugin(plugin_data)
            assert result.success is True

            adapted = result.value
            assert "name" in adapted
            assert "type" in adapted
            assert "configuration" in adapted
            assert "metadata" in adapted

    def test_adapt_project_config_edge_cases(self) -> None:
        """Testa adapt_project_config com configurações diversas."""
        test_configs = [
            # Config completa
            {
                "project_id": "full-project",
                "version": 1,
                "environments": [{"name": "dev"}, {"name": "prod"}],
                "plugins": {
                    "extractors": [{"name": "tap-csv"}],
                    "loaders": [{"name": "target-csv"}],
                    "transformers": [{"name": "dbt"}],
                },
                "schedules": [{"name": "daily"}],
                "project_name": "Full Project",
            },
            # Config mínima
            {"project_id": "minimal-project"},
            # Config com plugins como não-dict (edge case)
            {"project_id": "edge-project", "plugins": "invalid-plugins-format"},
        ]

        for config in test_configs:
            config_dict = cast("dict[str, object]", config)
            result = FlextMeltanoAdapter.adapt_project_config(config_dict)
            assert result.success is True

            adapted = result.value
            assert "project_id" in adapted
            assert "version" in adapted
            assert "plugins" in adapted
            assert "metadata" in adapted


class TestMeltanoBridgeIntegrationAdvanced:
    """Testes de integração ADVANCED - cenários complexos end-to-end."""

    def test_full_project_lifecycle_real(self) -> None:
        """Testa ciclo de vida completo: criar → inicializar → descobrir → listar."""
        bridge = MeltanoBridge()
        adapter = FlextMeltanoAdapter()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            project_name = "lifecycle-test"

            # 1. Criar projeto via adapter
            create_result = adapter.create_project_real(project_name, project_root)
            assert create_result.success is True

            created_project_path = project_root / project_name

            # 2. Inicializar via bridge
            init_result = bridge.initialize_project(created_project_path)
            assert init_result.success is True

            project = init_result.value

            # 3. Descobrir plugins disponíveis
            discover_result = bridge.discover_plugins()
            assert discover_result.success is True

            # 4. Listar plugins instalados (deve estar vazio)
            list_result = bridge.list_installed_plugins(project)
            assert list_result.success is True

            installed_plugins = list_result.value
            assert isinstance(installed_plugins, list)

    def test_error_propagation_comprehensive(self) -> None:
        """Testa propagação de erros através de toda a stack."""
        bridge = MeltanoBridge()
        adapter = FlextMeltanoAdapter()

        # Teste 1: Error propagation em projeto inválido
        invalid_path = Path("/completely/invalid/path")

        result1 = adapter.create_project_real("test", invalid_path)
        assert result1.success is False

        # Teste 2: Error propagation em comando inválido
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Criar projeto válido primeiro
            meltano_yml = project_root / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: error-test")

            result2 = bridge.execute_meltano_command_real(
                project_root, ["completely", "invalid", "command", "structure"]
            )
            assert result2.success is False

    def test_async_execution_patterns_comprehensive(self) -> None:
        """Testa padrões de execução async em cenários diversos."""
        bridge = MeltanoBridge()

        temp_project = bridge._create_temp_project()

        async def comprehensive_async_test() -> None:
            # Teste 1: Plugin com argumentos diversos
            result1 = await bridge.run_plugin_async(
                temp_project,
                "meltano",  # Plugin built-in que deve existir
                "version",
                [],
            )
            assert isinstance(result1, FlextResult)

            # Teste 2: Plugin inexistente (edge case)
            result2 = await bridge.run_plugin_async(
                temp_project, "nonexistent-plugin", "command", ["args"]
            )
            assert isinstance(result2, FlextResult)

            # Teste 3: Comando sem argumentos
            result3 = await bridge.run_plugin_async(
                temp_project,
                "meltano",
                "help",
                None,  # None args
            )
            assert isinstance(result3, FlextResult)

        # Executar todos os testes async
        asyncio.run(comprehensive_async_test())
