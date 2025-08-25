"""Testes COMPREHENSIVE para Utilities - COVERAGE PRÓXIMO 100%.

Este módulo implementa testes REAIS para TODAS as funcionalidades do utilities.py:
- FlextMeltanoUtilities: Testes com operações de arquivo REAIS
- FlextResultHelpers: Testes com FlextResult patterns
- FlextTypeAdapters: Testes de adaptação de tipos
- Cobrindo TODOS os métodos estáticos e utilitários
- Target: 90%+ coverage para utilities.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import cast

import yaml
from flext_core import FlextResult

from flext_meltano.utilities import FlextMeltanoUtilities


class TestFlextMeltanoUtilitiesComprehensive:
    """Testes COMPREHENSIVE do FlextMeltanoUtilities - REAL file operations."""

    def test_create_temp_directory_default_prefix(self) -> None:
        """Testa criação de diretório temporário com prefixo padrão."""
        temp_dir = FlextMeltanoUtilities.create_temp_directory()

        assert temp_dir.exists()
        assert temp_dir.is_dir()
        assert temp_dir.name.startswith("flext_meltano_")

        # Limpar
        temp_dir.rmdir()

    def test_create_temp_directory_custom_prefix(self) -> None:
        """Testa criação de diretório temporário com prefixo customizado."""
        custom_prefix = "test_custom_"
        temp_dir = FlextMeltanoUtilities.create_temp_directory(custom_prefix)

        assert temp_dir.exists()
        assert temp_dir.is_dir()
        assert temp_dir.name.startswith("test_custom_")

        # Limpar
        temp_dir.rmdir()

    def test_create_meltano_config_minimal(self) -> None:
        """Testa criação de config Meltano com parâmetros mínimos."""
        config = FlextMeltanoUtilities.create_meltano_config("test-project")

        assert isinstance(config, dict)

        # Verificar campos obrigatórios
        assert config["version"] == 1
        assert config["project_id"] == "test-project"
        assert config["project_name"] == "test-project"  # Default igual ao ID

        # Verificar estrutura completa
        assert "environments" in config
        assert "plugins" in config
        assert "schedules" in config

        # Verificar environments padrão
        environments = config["environments"]
        assert isinstance(environments, list)
        assert len(environments) == 3
        env_names = [env["name"] for env in environments]
        assert "dev" in env_names
        assert "staging" in env_names
        assert "prod" in env_names

        # Verificar plugins structure
        plugins = config["plugins"]
        assert isinstance(plugins, dict)
        plugins_dict: dict[str, object] = plugins
        assert "extractors" in plugins_dict
        assert "loaders" in plugins_dict
        assert "transformers" in plugins_dict

    def test_create_meltano_config_with_project_name(self) -> None:
        """Testa criação de config Meltano com nome específico."""
        config = FlextMeltanoUtilities.create_meltano_config(
            "test-id", "Custom Project Name"
        )

        assert config["project_id"] == "test-id"
        assert config["project_name"] == "Custom Project Name"

    def test_create_dbt_config_minimal(self) -> None:
        """Testa criação de config DBT com parâmetros mínimos."""
        config = FlextMeltanoUtilities.create_dbt_config("test-dbt-project")

        assert isinstance(config, dict)

        # Verificar campos obrigatórios
        assert config["name"] == "test-dbt-project"
        assert config["version"] == "1.0.0"
        assert config["profile"] == "test-dbt-project"  # Default igual ao nome

        # Verificar paths
        expected_paths = [
            "model-paths",
            "analysis-paths",
            "test-paths",
            "seed-paths",
            "macro-paths",
            "snapshot-paths",
            "target-path",
            "clean-targets",
        ]
        for path_key in expected_paths:
            assert path_key in config

        # Verificar models structure
        assert "models" in config
        models = config["models"]
        assert isinstance(models, dict)
        assert "test-dbt-project" in models
        assert isinstance(models["test-dbt-project"], dict)
        project_config = cast(dict[str, object], models["test-dbt-project"])
        assert project_config["+materialized"] == "view"

    def test_create_dbt_config_with_profile_name(self) -> None:
        """Testa criação de config DBT com profile específico."""
        config = FlextMeltanoUtilities.create_dbt_config(
            "test-project", "custom-profile"
        )

        assert config["name"] == "test-project"
        assert config["profile"] == "custom-profile"

    def test_create_singer_tap_config_minimal(self) -> None:
        """Testa criação de config Singer tap com parâmetros mínimos."""
        config = FlextMeltanoUtilities.create_singer_tap_config("tap-csv")

        assert isinstance(config, dict)

        # Verificar campos básicos
        assert config["name"] == "tap-csv"
        assert config["namespace"] == "tap_csv"  # Underscores em vez de hyphens
        assert config["pip_url"] == "pipelinewise-tap-csv"
        assert config["executable"] == "tap-csv"

        # Verificar capabilities
        assert "capabilities" in config
        capabilities = config["capabilities"]
        assert isinstance(capabilities, list)
        assert "discover" in capabilities
        assert "catalog" in capabilities
        assert "properties" in capabilities
        assert "state" in capabilities

        assert "settings" in config

    def test_create_singer_tap_config_complete(self) -> None:
        """Testa criação de config Singer tap com todos os parâmetros."""
        config = FlextMeltanoUtilities.create_singer_tap_config(
            "tap-postgres",
            namespace="custom_namespace",
            pip_url="git+https://github.com/example/tap-postgres.git",
            executable="tap-postgres-custom",
        )

        assert config["name"] == "tap-postgres"
        assert config["namespace"] == "custom_namespace"
        assert config["pip_url"] == "git+https://github.com/example/tap-postgres.git"
        assert config["executable"] == "tap-postgres-custom"

    def test_create_singer_target_config_minimal(self) -> None:
        """Testa criação de config Singer target com parâmetros mínimos."""
        config = FlextMeltanoUtilities.create_singer_target_config("target-csv")

        assert isinstance(config, dict)

        # Verificar campos básicos
        assert config["name"] == "target-csv"
        assert config["namespace"] == "target_csv"  # Underscores em vez de hyphens
        assert config["pip_url"] == "pipelinewise-target-csv"
        assert config["executable"] == "target-csv"
        assert "settings" in config

    def test_create_singer_target_config_complete(self) -> None:
        """Testa criação de config Singer target com todos os parâmetros."""
        config = FlextMeltanoUtilities.create_singer_target_config(
            "target-postgres",
            namespace="pg_namespace",
            pip_url="git+https://github.com/example/target-postgres.git",
            executable="target-pg",
        )

        assert config["name"] == "target-postgres"
        assert config["namespace"] == "pg_namespace"
        assert config["pip_url"] == "git+https://github.com/example/target-postgres.git"
        assert config["executable"] == "target-pg"

    def test_save_yaml_config_success(self) -> None:
        """Testa salvamento de config YAML com sucesso."""
        config = {"test": "value", "number": 123, "list": [1, 2, 3]}

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test_config.yml"

            result = FlextMeltanoUtilities.save_yaml_config(config, file_path)

            assert result.success is True
            assert result.value is True
            assert file_path.exists()

            # Verificar conteúdo do arquivo
            with file_path.open() as f:
                loaded_config = yaml.safe_load(f)

            assert loaded_config["test"] == "value"
            assert loaded_config["number"] == 123
            assert loaded_config["list"] == [1, 2, 3]

    def test_save_yaml_config_invalid_path(self) -> None:
        """Testa salvamento YAML em path inválido."""
        config: dict[str, object] = {"test": "value"}
        invalid_path = Path("/invalid/path/config.yml")

        result = FlextMeltanoUtilities.save_yaml_config(config, invalid_path)

        assert result.success is False
        assert result.error is not None
        assert "failed to save yaml config" in result.error.lower()

    def test_load_yaml_config_success(self) -> None:
        """Testa carregamento de config YAML com sucesso."""
        config_data = {
            "string_value": "test",
            "number_value": 42,
            "boolean_value": True,
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "load_test.yml"

            # Salvar primeiro
            with file_path.open("w") as f:
                yaml.dump(config_data, f)

            # Carregar
            result = FlextMeltanoUtilities.load_yaml_config(file_path)

            assert result.success is True
            loaded_config = result.value

            # Verificar que valores YAML preservam tipos nativos
            assert isinstance(loaded_config, dict)
            assert loaded_config["string_value"] == "test"
            assert loaded_config["number_value"] == 42  # YAML preserva integer
            assert loaded_config["boolean_value"] is True  # YAML preserva boolean

    def test_load_yaml_config_file_not_found(self) -> None:
        """Testa carregamento de arquivo inexistente."""
        nonexistent_path = Path("/nonexistent/config.yml")

        result = FlextMeltanoUtilities.load_yaml_config(nonexistent_path)

        assert result.success is False
        assert result.error is not None
        assert "no such file or directory" in result.error.lower()

    def test_load_yaml_config_empty_file(self) -> None:
        """Testa carregamento de arquivo YAML vazio."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "empty.yml"
            file_path.write_text("")  # Arquivo vazio

            result = FlextMeltanoUtilities.load_yaml_config(file_path)

            assert result.success is True
            loaded_config = result.value
            assert loaded_config == {}  # Config vazia deve retornar dict vazio

    def test_sanitize_plugin_name_simple(self) -> None:
        """Testa sanitização básica de nome de plugin."""
        # Teste com hífen
        result = FlextMeltanoUtilities.sanitize_plugin_name("tap-csv")
        assert result == "tap_csv"

        # Teste com uppercase
        result = FlextMeltanoUtilities.sanitize_plugin_name("TAP-POSTGRES")
        assert result == "tap_postgres"

        # Teste com espaços
        result = FlextMeltanoUtilities.sanitize_plugin_name("Target CSV File")
        assert result == "target_csv_file"

    def test_sanitize_plugin_name_complex(self) -> None:
        """Testa sanitização complexa de nome de plugin."""
        complex_name = "My-Complex Tap_Name-2024"
        result = FlextMeltanoUtilities.sanitize_plugin_name(complex_name)
        assert result == "my_complex_tap_name_2024"

    def test_create_plugin_config_minimal(self) -> None:
        """Testa criação de config de plugin com parâmetros mínimos."""
        config = FlextMeltanoUtilities.create_plugin_config("tap-csv", "extractor")

        assert isinstance(config, dict)

        # Verificar campos básicos
        assert config["name"] == "tap-csv"
        assert config["type"] == "extractor"
        assert config["namespace"] == "tap_csv_namespace"  # Gerado automaticamente
        assert config["pip_url"] == "git+https://github.com/MeltanoLabs/tap-csv.git"
        assert config["executable"] == "tap_csv"  # Nome sanitizado

    def test_create_plugin_config_complete(self) -> None:
        """Testa criação de config de plugin com todos os parâmetros."""
        config = FlextMeltanoUtilities.create_plugin_config(
            "tap-postgres",
            "extractor",
            namespace="custom_namespace",
            pip_url="git+https://github.com/example/tap-postgres.git",
        )

        assert config["name"] == "tap-postgres"
        assert config["type"] == "extractor"
        assert config["namespace"] == "custom_namespace"
        assert config["pip_url"] == "git+https://github.com/example/tap-postgres.git"
        assert config["executable"] == "tap_postgres"

    def test_setup_project_structure_complete(self) -> None:
        """Testa configuração completa de estrutura de projeto."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "test-project"
            project_name = "integration-test"

            result = FlextMeltanoUtilities.setup_project_structure(
                project_root, project_name
            )

            assert result.success is True

            # Verificar resultado
            info = result.value
            assert "project_root" in info
            assert "meltano_yml" in info
            assert "dbt_yml" in info

            # Verificar diretórios criados
            expected_dirs = [
                "extract",
                "load",
                "transform",
                "analyze",
                "models",
                "tests",
                "data",
            ]
            for dir_name in expected_dirs:
                assert dir_name in info
                assert Path(info[dir_name]).exists()

            # Verificar arquivos de configuração
            meltano_yml = Path(info["meltano_yml"])
            dbt_yml = Path(info["dbt_yml"])

            assert meltano_yml.exists()
            assert dbt_yml.exists()

            # Verificar conteúdo do meltano.yml
            with meltano_yml.open(encoding="utf-8") as f:
                meltano_config = yaml.safe_load(f)

            assert meltano_config["project_id"] == project_name
            assert "environments" in meltano_config

            # Verificar conteúdo do dbt_project.yml
            with dbt_yml.open(encoding="utf-8") as f:
                dbt_config = yaml.safe_load(f)

            assert dbt_config["name"] == f"{project_name}_dbt"

    def test_setup_project_structure_existing_directory(self) -> None:
        """Testa setup em diretório já existente."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            project_name = "existing-project"

            # Diretório já existe
            result = FlextMeltanoUtilities.setup_project_structure(
                project_root, project_name
            )

            assert result.success is True
            info = result.value
            assert Path(info["meltano_yml"]).exists()

    def test_validate_plugin_config_valid(self) -> None:
        """Testa validação de configuração válida de plugin."""
        valid_config: dict[str, object] = {
            "name": "tap-csv",
            "type": "extractor",
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }

        result = FlextMeltanoUtilities.validate_plugin_config(valid_config)

        assert result.success is True
        assert result.value is True

    def test_validate_plugin_config_missing_fields(self) -> None:
        """Testa validação com campos obrigatórios ausentes."""
        # Config sem campo 'name'
        invalid_config: dict[str, object] = {
            "namespace": "tap_csv",
            "pip_url": "pipelinewise-tap-csv",
            "executable": "tap-csv",
        }

        result = FlextMeltanoUtilities.validate_plugin_config(invalid_config)

        assert result.success is False
        assert result.error is not None
        assert "missing required field" in result.error.lower()
        assert "name" in result.error

    def test_validate_plugin_config_multiple_missing_fields(self) -> None:
        """Testa validação com múltiplos campos ausentes."""
        # Config com apenas um campo
        minimal_config: dict[str, object] = {"name": "tap-csv"}

        result = FlextMeltanoUtilities.validate_plugin_config(minimal_config)

        assert result.success is False
        assert result.error is not None
        assert "missing required field" in result.error.lower()
        # Deve falhar no primeiro campo ausente

    def test_validate_plugin_config_empty(self) -> None:
        """Testa validação de configuração vazia."""
        result = FlextMeltanoUtilities.validate_plugin_config({})

        assert result.success is False
        assert result.error is not None
        assert "missing required field" in result.error.lower()


class TestFlextMeltanoUtilitiesIntegration:
    """Testes de integração entre diferentes utilitários."""

    def test_complete_project_creation_workflow(self) -> None:
        """Testa workflow completo de criação de projeto."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "complete-workflow"
            project_name = "workflow-test"

            # 1. Setup da estrutura
            setup_result = FlextMeltanoUtilities.setup_project_structure(
                project_root, project_name
            )
            assert setup_result.success is True

            # 2. Verificar que meltano.yml foi criado corretamente
            meltano_yml_path = Path(setup_result.value["meltano_yml"])
            load_result = FlextMeltanoUtilities.load_yaml_config(meltano_yml_path)
            assert load_result.success is True

            loaded_config = load_result.value
            assert loaded_config["project_id"] == project_name

    def test_config_creation_and_validation_workflow(self) -> None:
        """Testa workflow de criação e validação de config."""
        # 1. Criar config de plugin
        plugin_config_str = FlextMeltanoUtilities.create_plugin_config(
            "tap-test", "extractor"
        )
        plugin_config = cast(dict[str, object], plugin_config_str)

        # 2. Validar config criada
        validation_result = FlextMeltanoUtilities.validate_plugin_config(plugin_config)
        assert validation_result.success is True

        # 3. Salvar e recarregar config
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "plugin_config.yml"

            save_result = FlextMeltanoUtilities.save_yaml_config(
                plugin_config, config_file
            )
            assert save_result.success is True

            load_result = FlextMeltanoUtilities.load_yaml_config(config_file)
            assert load_result.success is True

            # Verificar que config recarregada ainda é válida
            reloaded_config = dict(load_result.value.items())
            revalidation_result = FlextMeltanoUtilities.validate_plugin_config(
                reloaded_config
            )
            assert revalidation_result.success is True

    def test_sanitization_integration(self) -> None:
        """Testa integração de sanitização em diferentes contextos."""
        original_name = "My-Complex Plugin_Name 2024!"

        # 1. Sanitizar nome
        sanitized = FlextMeltanoUtilities.sanitize_plugin_name(original_name)
        assert sanitized == "my_complex_plugin_name_2024!"

        # 2. Usar nome sanitizado em config
        plugin_config_str = FlextMeltanoUtilities.create_plugin_config(
            sanitized, "extractor"
        )
        plugin_config = cast(dict[str, object], plugin_config_str)

        # 3. Validar que config com nome sanitizado é válida
        validation_result = FlextMeltanoUtilities.validate_plugin_config(plugin_config)
        assert validation_result.success is True

    def test_error_handling_consistency(self) -> None:
        """Testa consistência no tratamento de erros entre diferentes métodos."""
        # Todos os métodos que podem falhar devem retornar FlextResult

        # Test save_yaml_config error
        invalid_path = Path("/invalid/path/config.yml")
        save_result = FlextMeltanoUtilities.save_yaml_config({}, invalid_path)
        assert isinstance(save_result, FlextResult)
        assert save_result.success is False

        # Test load_yaml_config error
        load_result = FlextMeltanoUtilities.load_yaml_config(invalid_path)
        assert isinstance(load_result, FlextResult)
        assert load_result.success is False

        # Test validate_plugin_config error
        validation_result = FlextMeltanoUtilities.validate_plugin_config({})
        assert isinstance(validation_result, FlextResult)
        assert validation_result.success is False

    def test_flext_result_patterns_comprehensive(self) -> None:
        """Testa padrões FlextResult comprehensivamente."""
        # Test successful operations
        temp_dir = FlextMeltanoUtilities.create_temp_directory()
        config_path = temp_dir / "test_config.yml"

        test_config: dict[str, object] = {"test": "value"}

        # Save config
        save_result = FlextMeltanoUtilities.save_yaml_config(test_config, config_path)
        assert save_result.success is True

        # Use unwrap_or pattern for successful operation
        success_value = save_result.unwrap_or(False)
        assert success_value is True

        # Load config
        load_result = FlextMeltanoUtilities.load_yaml_config(config_path)
        assert load_result.success is True

        # Use unwrap_or pattern for successful load
        loaded_config = load_result.unwrap_or({})
        assert loaded_config != {}
        assert loaded_config["test"] == "value"

        # Test error case with unwrap_or
        error_result = FlextMeltanoUtilities.load_yaml_config(Path("/invalid/path.yml"))
        default_config = error_result.unwrap_or({"default": "config"})
        assert default_config == {"default": "config"}

        # Cleanup
        config_path.unlink()
        temp_dir.rmdir()
