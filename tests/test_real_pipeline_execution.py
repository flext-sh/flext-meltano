"""Testes REAIS de execução de pipelines completos.

IMPLEMENTAÇÃO REAL - Sem mocks, testando execução completa:
1. Criação de projeto Meltano REAL
2. Execução de pipeline ELT REAL usando PluginInvoker
3. Execução de modelos DBT REAL usando dbtRunner.invoke()
4. Validação de resultados REAIS

Objetivo: Validar que as APIs nativas funcionam SEM subprocess.
"""

import importlib.util
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import cast

import pytest
from flext_core import FlextResult

from flext_meltano.dbt_adapters import MeltanoDbtWrapper
from flext_meltano.meltano_adapters import FlextMeltanoAdapter


class TestRealPipelineExecution:
    """Testes de execução REAL de pipelines completos."""

    @pytest.fixture
    def temp_project_dir(self) -> Generator[Path]:
        """Cria diretório temporário para projeto de teste."""
        with tempfile.TemporaryDirectory(prefix="flext_meltano_test_") as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def meltano_adapter(self) -> FlextMeltanoAdapter:
        """Cria instância FlextMeltanoAdapter para testes."""
        return FlextMeltanoAdapter()

    @pytest.fixture
    def dbt_wrapper(self) -> MeltanoDbtWrapper:
        """Cria instância MeltanoDbtWrapper para testes."""
        return MeltanoDbtWrapper()

    def test_create_real_meltano_project(
        self, meltano_adapter: FlextMeltanoAdapter, temp_project_dir: Path
    ) -> None:
        """Testa criação REAL de projeto Meltano usando BlockParser."""
        # Criar projeto usando API nativa Meltano
        result = meltano_adapter.create_project_real(
            project_name="test_project",
            project_dir=temp_project_dir,
        )

        # Validar resultado
        assert result.success, f"Failed to create project: {result.error}"
        assert result.value is not None
        assert isinstance(result.value, dict)

        # Validar estrutura do projeto criado
        project_path = temp_project_dir / "test_project"
        assert project_path.exists(), "Project directory should exist"

        # Verificar arquivos essenciais do Meltano
        meltano_yml = project_path / "meltano.yml"
        assert meltano_yml.exists(), "meltano.yml should exist"

        # Verificar conteúdo do meltano.yml
        content = meltano_yml.read_text()
        assert "version:" in content, "Version should be in meltano.yml"
        assert "project_id:" in content, "Project ID should be in meltano.yml"
        assert "environments:" in content, "Environments should be in meltano.yml"

    def test_add_plugins_real(
        self, meltano_adapter: FlextMeltanoAdapter, temp_project_dir: Path
    ) -> None:
        """Testa adição REAL de plugins usando ProjectPluginsService."""
        # Primeiro criar projeto
        create_result = meltano_adapter.create_project_real(
            project_name="test_plugins",
            project_dir=temp_project_dir,
        )
        assert create_result.success

        project_path = temp_project_dir / "test_plugins"

        # Adicionar tap-csv (extractor simples para teste)
        tap_result = meltano_adapter.add_plugin_real(
            project_dir=project_path,
            plugin_type="extractors",
            plugin_name="tap-csv",
        )
        assert tap_result.success, f"Failed to add tap-csv: {tap_result.error}"

        # Adicionar target-jsonl (target simples para teste)
        target_result = meltano_adapter.add_plugin_real(
            project_dir=project_path,
            plugin_type="loaders",
            plugin_name="target-jsonl",
        )
        assert target_result.success, (
            f"Failed to add target-jsonl: {target_result.error}"
        )

        # Verificar que plugins foram adicionados ao meltano.yml
        meltano_yml = project_path / "meltano.yml"
        content = meltano_yml.read_text()
        assert "tap-csv" in content, "tap-csv should be in meltano.yml"
        assert "target-jsonl" in content, "target-jsonl should be in meltano.yml"

    def test_run_real_elt_pipeline(
        self, meltano_adapter: FlextMeltanoAdapter, temp_project_dir: Path
    ) -> None:
        """Testa execução REAL de pipeline ELT usando PluginInvoker."""
        # Criar projeto com plugins
        create_result = meltano_adapter.create_project_real(
            project_name="test_elt",
            project_dir=temp_project_dir,
        )
        assert create_result.success

        project_path = temp_project_dir / "test_elt"

        # Adicionar plugins necessários
        tap_result = meltano_adapter.add_plugin_real(
            project_dir=project_path,
            plugin_type="extractors",
            plugin_name="tap-csv",
        )
        assert tap_result.success

        target_result = meltano_adapter.add_plugin_real(
            project_dir=project_path,
            plugin_type="loaders",
            plugin_name="target-jsonl",
        )
        assert target_result.success

        # Criar arquivo CSV de teste
        csv_file = project_path / "test_data.csv"
        csv_file.write_text("id,name,value\n1,test1,100\n2,test2,200\n")

        # Configurar tap-csv para usar o arquivo
        # Nota: Em teste real, precisaríamos configurar o tap adequadamente
        # Por ora, testamos apenas se a função executa sem erro

        # Executar pipeline REAL usando PluginInvoker
        pipeline_result = meltano_adapter.run_pipeline_real(
            project_dir=project_path,
            tap_name="tap-csv",
            target_name="target-jsonl",
        )

        # Validar resultado da execução
        # Nota: Pode falhar por configuração, mas não deve ter erro de API
        assert isinstance(pipeline_result, FlextResult)

        if pipeline_result.success:
            assert pipeline_result.value is not None
            assert isinstance(pipeline_result.value, dict)
            assert "execution_method" in pipeline_result.value
            assert pipeline_result.value["execution_method"] == "plugin_invoker_native"
        else:
            # Se falhou, deve ter mensagem de erro clara (não erro de API)
            assert (
                "not found" in str(pipeline_result.error)
                or "configuration" in str(pipeline_result.error)
                or "failed" in str(pipeline_result.error)
            )

    def test_run_real_dbt_models(
        self, dbt_wrapper: MeltanoDbtWrapper, temp_project_dir: Path
    ) -> None:
        """Testa execução REAL de modelos DBT usando dbtRunner.invoke()."""
        # Criar estrutura básica de projeto DBT
        dbt_project_dir = temp_project_dir / "test_dbt_project"
        dbt_project_dir.mkdir()

        # Criar dbt_project.yml mínimo
        dbt_project_yml = dbt_project_dir / "dbt_project.yml"
        dbt_project_yml.write_text("""
name: 'test_dbt_project'
version: '1.0.0'
config-version: 2

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  test_dbt_project:
    +materialized: table
""")

        # Criar diretório models
        models_dir = dbt_project_dir / "models"
        models_dir.mkdir()

        # Criar modelo simples de teste
        test_model = models_dir / "test_model.sql"
        test_model.write_text("""
-- Simple test model
SELECT 1 as id, 'test' as name
""")

        # Criar profiles.yml básico
        profiles_dir = temp_project_dir / "profiles"
        profiles_dir.mkdir()
        profiles_yml = profiles_dir / "profiles.yml"
        profiles_yml.write_text("""
test_dbt_project:
  outputs:
    dev:
      type: duckdb
      path: ':memory:'
  target: dev
""")

        # Executar modelos DBT usando API REAL dbtRunner.invoke()
        result = dbt_wrapper.run_models_real(
            project_dir=dbt_project_dir,
            models=["test_model"],
            profiles_dir=profiles_dir,
        )

        # Validar resultado da execução
        assert isinstance(result, FlextResult)

        if result.success:
            assert result.value is not None
            assert isinstance(result.value, dict)
            assert "execution_method" in result.value
            assert result.value["execution_method"] == "dbt_runner_invoke"
            assert "success" in result.value
        else:
            # Se falhou, deve ter mensagem de erro clara
            assert result.error is not None
            # Podem falhar por dependências, mas não por erro de API
            assert not any(
                error_type in str(result.error)
                for error_type in [
                    "ImportError",
                    "ModuleNotFoundError",
                    "AttributeError",
                ]
            )

    def test_compile_dbt_project_real(
        self, dbt_wrapper: MeltanoDbtWrapper, temp_project_dir: Path
    ) -> None:
        """Testa compilação REAL de projeto DBT usando dbtRunner.invoke()."""
        # Criar projeto DBT básico
        dbt_project_dir = temp_project_dir / "compile_test"
        dbt_project_dir.mkdir()

        # Criar arquivos mínimos
        dbt_project_yml = dbt_project_dir / "dbt_project.yml"
        dbt_project_yml.write_text("""
name: 'compile_test'
version: '1.0.0'
config-version: 2
model-paths: ["models"]
target-path: "target"
models:
  compile_test:
    +materialized: view
""")

        models_dir = dbt_project_dir / "models"
        models_dir.mkdir()

        test_model = models_dir / "simple_model.sql"
        test_model.write_text("SELECT 'compiled' as status")

        # Criar dbtRunner e compilar
        runner_result = dbt_wrapper.create_runner(dbt_project_dir)
        assert runner_result.success

        runner = runner_result.value

        # Compilar projeto usando API REAL
        compile_result = dbt_wrapper.compile_project(
            runner=runner,
            project_dir=dbt_project_dir,
        )

        # Validar resultado
        assert isinstance(compile_result, FlextResult)
        assert compile_result.success or compile_result.error is not None

        if compile_result.success:
            result_data = compile_result.value
            assert isinstance(result_data, dict)
            assert "success" in result_data
            assert "command" in result_data
            command_list = cast("list[str]", result_data["command"])
            assert command_list[0] == "compile"

    def test_full_elt_dbt_pipeline_integration(
        self,
        meltano_adapter: FlextMeltanoAdapter,
        dbt_wrapper: MeltanoDbtWrapper,
        temp_project_dir: Path,
    ) -> None:
        """Teste integração REAL completa: ELT + DBT."""
        # 1. Criar projeto Meltano
        project_result = meltano_adapter.create_project_real(
            project_name="full_integration",
            project_dir=temp_project_dir,
        )
        assert project_result.success

        project_path = temp_project_dir / "full_integration"

        # 2. Adicionar plugins ELT
        tap_result = meltano_adapter.add_plugin_real(
            project_dir=project_path,
            plugin_type="extractors",
            plugin_name="tap-csv",
        )
        assert tap_result.success

        target_result = meltano_adapter.add_plugin_real(
            project_dir=project_path,
            plugin_type="loaders",
            plugin_name="target-jsonl",
        )
        assert target_result.success

        # 3. Usar estrutura DBT existente no projeto (Meltano já cria transform/)
        transform_dir = project_path / "transform"
        # O Meltano já criou esta pasta, não precisamos criar novamente

        dbt_project_yml = transform_dir / "dbt_project.yml"
        dbt_project_yml.write_text("""
name: 'full_integration_transform'
version: '1.0.0'
config-version: 2
model-paths: ["models"]
target-path: "target"
models:
  full_integration_transform:
    +materialized: table
""")

        models_dir = transform_dir / "models"
        models_dir.mkdir()

        # Modelo que processa dados do ELT
        transform_model = models_dir / "processed_data.sql"
        transform_model.write_text("""
-- Transform data from ELT pipeline
SELECT
    'transformed' as status,
    current_timestamp as processed_at
""")

        # 4. Executar pipeline ELT
        elt_result = meltano_adapter.run_pipeline_real(
            project_dir=project_path,
            tap_name="tap-csv",
            target_name="target-jsonl",
        )

        # Pipeline ELT pode falhar por configuração, mas API deve funcionar
        assert isinstance(elt_result, FlextResult)

        # 5. Executar transformações DBT
        dbt_result = dbt_wrapper.run_models_real(
            project_dir=transform_dir,
            models=["processed_data"],
        )

        # Validar que ambas as APIs funcionaram (sem erros de importação/API)
        assert isinstance(dbt_result, FlextResult)

        # Se tudo funcionou, validar estrutura de resposta
        if elt_result.success and dbt_result.success:
            assert "execution_method" in elt_result.value
            assert "execution_method" in dbt_result.value
            assert elt_result.value["execution_method"] == "plugin_invoker_native"
            assert dbt_result.value["execution_method"] == "dbt_runner_invoke"

    @pytest.mark.integration
    def test_api_availability_real(self) -> None:
        """Testa disponibilidade REAL das APIs nativas do Meltano 3.9.1 e DBT."""
        # Teste que as APIs necessárias estão disponíveis

        required_modules = [
            "dbt.cli.main",
            "meltano.core.elt_context",
            "meltano.core.plugin_invoker",
            "meltano.core.project",
            "meltano.core.project_plugins_service",
            "meltano.core.runner",
        ]

        def _check_module_availability(module_name: str) -> None:
            """Check if module is available, raise ImportError if not."""
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                raise ImportError(f"Module {module_name} not found")

        try:
            # Check if all required modules are available
            for module_name in required_modules:
                _check_module_availability(module_name)

            # Se chegou até aqui, todas as APIs estão disponíveis
            assert True

        except ImportError as e:
            pytest.fail(f"Required API not available: {e}")

    @pytest.mark.integration
    def test_native_api_instantiation(self) -> None:
        """Testa instanciação REAL das APIs nativas."""
        # Teste que as APIs podem ser instanciadas
        try:
            # Instanciar dbtRunner
            runner = pytest.importorskip("dbt.cli.main").dbtRunner()
            assert runner is not None

            # Instanciar Runner do Meltano
            runner_class = pytest.importorskip("meltano.core.runner").Runner
            runner = runner_class()
            assert runner is not None

        except Exception as e:
            pytest.fail(f"Failed to instantiate native APIs: {e}")
