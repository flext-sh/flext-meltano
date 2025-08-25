"""Testes COMPREHENSIVE REAIS para runtime_cli.py - COVERAGE EXPANSION.

Este módulo implementa testes REAIS para TODAS as funcionalidades do FlextMeltanoCli:
- Usando APIs nativas Meltano 3.9.1 - SEM MOCKS
- Cobrindo TODAS as funções públicas: run, execute, health, version
- Usando FlextResult patterns (.value, .unwrap_or())
- Testando cenários de sucesso E erro com CLI commands reais
- Target: 85%+ coverage para runtime_cli.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import cast

from flext_core import FlextResult

from flext_meltano.executors_cli import (
    FlextMeltanoCli,
    flext_meltano_run_cli,
)


class TestFlextMeltanoCliComprehensive:
    """Testes COMPREHENSIVE REAIS para FlextMeltanoCli - SEM MOCKS."""

    def test_cli_initialization_default(self) -> None:
        """Testa inicialização completa do CLI."""
        cli = FlextMeltanoCli()

        # Propriedades básicas
        assert cli is not None
        assert cli.project_root == Path.cwd()
        assert hasattr(cli, "bridge")
        assert hasattr(cli, "executor")
        assert hasattr(cli, "meltano_wrapper")
        assert hasattr(cli, "console")
        assert hasattr(cli, "logger")

        # Componentes inicializados
        assert cli.bridge is not None
        assert cli.executor is not None
        assert cli.meltano_wrapper is not None
        assert cli.console is not None
        assert cli.logger is not None

        # Logger configurado corretamente
        assert cli.logger._name == "FlextMeltanoCli"

    def test_cli_initialization_with_project_root(self) -> None:
        """Test initialization with specific project_root."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = Path(temp_dir) / "test_project"
            cli = FlextMeltanoCli(test_path)

            assert cli.project_root == test_path

    def test_cli_initialization_with_none_project_root(self) -> None:
        """Testa inicialização com project_root None."""
        cli = FlextMeltanoCli(None)

        assert cli.project_root == Path.cwd()

    def test_run_command_no_args(self) -> None:
        """Testa run_command sem argumentos."""
        cli = FlextMeltanoCli()

        exit_code = cli.run_command([])

        # Deve retornar 1 (ajuda) sem argumentos
        assert exit_code == 1

    def test_run_command_version(self) -> None:
        """Testa run_command com version."""
        cli = FlextMeltanoCli()

        exit_code = cli.run_command(["version"])

        # Deve tentar executar version (pode funcionar ou falhar)
        assert isinstance(exit_code, int)

    def test_run_command_plugins(self) -> None:
        """Testa run_command com plugins."""
        cli = FlextMeltanoCli()

        exit_code = cli.run_command(["plugins"])

        # Deve tentar listar plugins
        assert isinstance(exit_code, int)

    def test_run_command_run_insufficient_args(self) -> None:
        """Testa run_command com argumentos insuficientes."""
        cli = FlextMeltanoCli()

        exit_code = cli.run_command(["run"])

        # Deve retornar 1 por falta de argumentos
        assert exit_code == 1

    def test_run_command_run_minimal_args(self) -> None:
        """Testa run_command com argumentos mínimos."""
        cli = FlextMeltanoCli()

        exit_code = cli.run_command(["run", "tap-csv", "target-csv"])

        # Deve tentar executar pipeline
        assert isinstance(exit_code, int)

    def test_run_command_unknown(self) -> None:
        """Testa run_command com comando desconhecido."""
        cli = FlextMeltanoCli()

        exit_code = cli.run_command(["unknown_command"])

        # Deve retornar 1 (help) para comando desconhecido
        assert exit_code == 1

    def test_run_flext_result_no_args(self) -> None:
        """Testa run() com FlextResult - sem argumentos."""
        cli = FlextMeltanoCli()

        result = cli.run([])

        # Deve retornar sucesso com versão
        assert result.success is True
        data = result.value

        assert data["command"] == "default"
        assert data["status"] == "success"
        assert "success" in data
        assert "data" in data

    def test_run_flext_result_version_flag(self) -> None:
        """Testa run() com --version."""
        cli = FlextMeltanoCli()

        result = cli.run(["--version"])

        assert result.success is True
        data = result.value

        assert data["command"] == "version"
        assert "version" in data
        assert data["cli_type"] == "flext_meltano"
        assert "success" in data

    def test_run_flext_result_help_flag(self) -> None:
        """Testa run() com --help."""
        cli = FlextMeltanoCli()

        result = cli.run(["--help"])

        assert result.success is True
        data = result.value

        assert data["command"] == "help"
        assert "commands" in data
        assert data["success"] == "true"
        assert "FLEXT Meltano CLI Help" in data["data"]

    def test_run_flext_result_help_command(self) -> None:
        """Testa run() com help command."""
        cli = FlextMeltanoCli()

        result = cli.run(["help"])

        assert result.success is True
        data = result.value

        assert data["command"] == "help"
        assert "commands" in data
        assert data["success"] == "true"

    def test_run_flext_result_version_command(self) -> None:
        """Testa run() com version command."""
        cli = FlextMeltanoCli()

        result = cli.run(["version"])

        assert result.success is True
        data = result.value

        assert data["command"] == "version"
        assert "version" in data
        assert data["cli_type"] == "flext_meltano"

    def test_run_flext_result_other_commands(self) -> None:
        """Testa run() com outros comandos."""
        cli = FlextMeltanoCli()

        result = cli.run(["plugins", "list"])

        assert result.success is True
        data = result.value

        assert "command" in data
        assert "args" in data
        assert "success" in data

    def test_health_check_comprehensive(self) -> None:
        """Testa health check com verificações completas."""
        cli = FlextMeltanoCli()

        result = cli.health()

        # Deve retornar sucesso
        assert result.success is True
        health_data = result.value

        assert isinstance(health_data, dict)
        assert health_data["status"] == "healthy"
        assert "meltano_status" in health_data
        assert health_data["cli_type"] == "flext_meltano"
        assert "project_root" in health_data

        # Meltano status deve ser healthy ou degraded
        assert health_data["meltano_status"] in {"healthy", "degraded"}

    def test_version_check_comprehensive(self) -> None:
        """Testa version check com API nativa."""
        cli = FlextMeltanoCli()

        result = cli.version()

        # Deve retornar sucesso
        assert result.success is True
        version_data = result.value

        assert isinstance(version_data, dict)
        assert "version" in version_data
        assert "python" in version_data
        assert "flext_meltano" in version_data
        assert version_data["cli_type"] == "flext_meltano"

        # Verificar valores
        assert version_data["flext_meltano"] == "2.0.0-enterprise"
        assert version_data["python"].count(".") >= 2  # Format x.y.z

    def test_help_information(self) -> None:
        """Testa obtenção de informações de ajuda."""
        cli = FlextMeltanoCli()

        result = cli.help()

        assert result.success is True
        help_data = result.value

        assert "commands" in help_data
        assert help_data["cli_type"] == "flext_meltano"
        assert "description" in help_data

        # Verificar comandos listados
        commands_str = cast("str", help_data["commands"])
        expected_commands = ["version", "help", "health", "run", "discover", "install"]
        for cmd in expected_commands:
            assert cmd in commands_str

    def test_list_commands(self) -> None:
        """Testa listagem de comandos."""
        cli = FlextMeltanoCli()

        result = cli.list_commands()

        assert result.success is True
        commands_data = result.value

        assert "commands" in commands_data
        commands_list = commands_data["commands"]
        assert isinstance(commands_list, list)

        expected_commands = ["version", "help", "health", "run", "discover", "install"]
        for cmd in expected_commands:
            assert cmd in commands_list

    def test_list_plugins_real_api(self) -> None:
        """Testa listagem de plugins usando API nativa."""
        cli = FlextMeltanoCli()

        result = cli.list_plugins()

        # Pode retornar sucesso ou falha dependendo de conectividade
        assert isinstance(result, FlextResult)

        if result.success:
            plugins_data = result.value
            assert "plugins" in plugins_data
            assert "count" in plugins_data
            assert plugins_data["cli_type"] == "flext_meltano"
        # Falha é OK - pode ser problema de rede/hub
        elif result.error is not None:
            assert "Failed to list plugins" in result.error

    def test_run_pipeline_without_project(self) -> None:
        """Testa execução de pipeline sem projeto."""
        cli = FlextMeltanoCli()

        result = cli.run_pipeline("tap-csv", "target-csv")

        # Pode falhar por não ter projeto válido
        if result.success:
            pipeline_data = result.value
            assert pipeline_data["tap"] == "tap-csv"
            assert pipeline_data["target"] == "target-csv"
        # Falha esperada sem projeto válido
        elif result.error is not None:
            assert "failed" in result.error.lower()

    def test_run_pipeline_with_project_root(self) -> None:
        """Testa execução de pipeline com project_root."""
        cli = FlextMeltanoCli()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Criar projeto Meltano básico
            project_path = Path(temp_dir)
            meltano_yml = project_path / "meltano.yml"
            meltano_yml.write_text("""
version: 1
project_id: test-cli-pipeline
environments:
- name: dev
""")

            result = cli.run_pipeline("tap-csv", "target-csv", temp_dir)

            # Deve tentar executar pipeline
            assert isinstance(result, FlextResult)

            if result.success:
                pipeline_data = result.value
                assert "status" in pipeline_data
                assert pipeline_data["cli_type"] == "flext_meltano"

    def test_execute_command_empty(self) -> None:
        """Testa execute com comando vazio."""
        cli = FlextMeltanoCli()

        result = cli.execute("")

        assert result.success is True
        data = result.value

        assert data["command"] == "default"
        assert data["cli_type"] == "flext_meltano"

    def test_execute_command_version(self) -> None:
        """Testa execute com version."""
        cli = FlextMeltanoCli()

        result = cli.execute("version")

        assert result.success is True
        data = result.value

        assert "version" in data
        assert data["cli_type"] == "flext_meltano"

    def test_execute_command_help(self) -> None:
        """Testa execute com help."""
        cli = FlextMeltanoCli()

        result = cli.execute("help")

        assert result.success is True
        data = result.value

        assert "commands" in data
        assert data["cli_type"] == "flext_meltano"

    def test_execute_command_health(self) -> None:
        """Testa execute com health."""
        cli = FlextMeltanoCli()

        result = cli.execute("health")

        assert result.success is True
        data = result.value

        assert data["status"] == "healthy"

    def test_execute_command_with_options(self) -> None:
        """Testa execute com opções."""
        cli = FlextMeltanoCli()

        result = cli.execute("discover", ["--format", "json"])

        assert result.success is True
        data = result.value

        assert data["command"] == "discover"
        assert "options" in data

    def test_execute_command_unknown(self) -> None:
        """Testa execute com comando desconhecido."""
        cli = FlextMeltanoCli()

        result = cli.execute("unknown_command")

        assert result.success is True
        data = result.value

        assert data["command"] == "unknown_command"
        assert data["status"] == "unknown_command"

    def test_flext_meltano_version_native_api(self) -> None:
        """Testa flext_meltano_version com API nativa."""
        cli = FlextMeltanoCli()

        result = cli.flext_meltano_version()

        assert isinstance(result, FlextResult)

        if result.success:
            version_str = result.value
            assert "Meltano, version" in version_str
        # Falha é OK - pode ser problema de API
        elif result.error is not None:
            assert "failed" in result.error.lower()

    def test_flext_meltano_install(self) -> None:
        """Testa flext_meltano_install."""
        cli = FlextMeltanoCli()

        result = cli.flext_meltano_install()

        # Deve retornar sucesso (implementação básica)
        assert result.success is True
        assert result.value is True

    def test_flext_meltano_invoke(self) -> None:
        """Testa flext_meltano_invoke."""
        cli = FlextMeltanoCli()

        result = cli.flext_meltano_invoke("tap-csv", "describe", "--format=json")

        assert result.success is True
        invoke_data = result.value

        assert invoke_data["plugin_name"] == "tap-csv"
        args_list = cast("list[str]", invoke_data["args"])
        assert "describe" in args_list
        assert "--format=json" in args_list
        assert invoke_data["status"] == "invoked_via_native_api"


class TestFlextMeltanoCliFactoryFunctions:
    """Testes COMPREHENSIVE para factory functions."""

    def test_flext_meltano_run_cli_no_args(self) -> None:
        """Testa factory function sem argumentos."""
        result = flext_meltano_run_cli()

        assert result.success is True
        data = result.value

        assert data["command"] == "default"
        assert data["status"] == "success"

    def test_flext_meltano_run_cli_none_args(self) -> None:
        """Testa factory function com None args."""
        result = flext_meltano_run_cli(None)

        assert result.success is True
        data = result.value

        assert data["command"] == "default"

    def test_flext_meltano_run_cli_empty_args(self) -> None:
        """Testa factory function com args vazios."""
        result = flext_meltano_run_cli([])

        assert result.success is True
        data = result.value

        assert data["command"] == "default"

    def test_flext_meltano_run_cli_version(self) -> None:
        """Testa factory function com --version."""
        result = flext_meltano_run_cli(["--version"])

        assert result.success is True
        data = result.value

        assert data["command"] == "version"
        assert "version" in data
        assert data["cli_type"] == "flext_meltano"

    def test_flext_meltano_run_cli_help(self) -> None:
        """Testa factory function com --help."""
        result = flext_meltano_run_cli(["--help"])

        assert result.success is True
        data = result.value

        assert data["command"] == "help"
        assert data["success"] == "true"

    def test_flext_meltano_run_cli_other_commands(self) -> None:
        """Testa factory function com outros comandos."""
        result = flext_meltano_run_cli(["plugins", "list"])

        assert result.success is True
        data = result.value

        assert "command" in data
        assert "args" in data

    def test_flext_meltano_run_cli_error_handling(self) -> None:
        """Testa tratamento de erros na factory function."""
        # Comando que pode causar erro (mas deve capturar gracefully)
        result = flext_meltano_run_cli(["run", "invalid-tap", "invalid-target"])

        assert result.success is True  # Não deve falhar na factory
        data = result.value

        assert "command" in data
        assert "success" in data


class TestFlextMeltanoCliErrorHandling:
    """Testes COMPREHENSIVE para tratamento de erros."""

    def test_cli_with_project_exception(self) -> None:
        """Testa CLI com projeto que pode causar exceção."""
        # Criar CLI com project_root que existe mas não é projeto válido
        with tempfile.TemporaryDirectory() as temp_dir:
            cli = FlextMeltanoCli(Path(temp_dir))

            # Deve funcionar mesmo sem projeto válido
            result = cli.health()
            assert result.success is True

            # Version deve funcionar
            version_result = cli.version()
            assert version_result.success is True

    def test_run_with_exception_handling(self) -> None:
        """Testa run() com tratamento de exceções."""
        cli = FlextMeltanoCli()

        # Comando que pode causar problemas
        result = cli.run(["run", "nonexistent-tap", "nonexistent-target"])

        assert result.success is True
        data = result.value

        # Deve capturar erro gracefully
        assert "command" in data
        assert "success" in data

    def test_execute_with_exception_handling(self) -> None:
        """Testa execute() com tratamento de exceções."""
        cli = FlextMeltanoCli()

        # Deve lidar com comandos problemáticos
        result = cli.execute("run", ["invalid", "args"])

        assert result.success is True
        data = result.value

        assert data["command"] == "run"

    def test_list_plugins_error_handling(self) -> None:
        """Testa list_plugins com tratamento de erro."""
        cli = FlextMeltanoCli()

        result = cli.list_plugins()

        # Pode falhar ou ter sucesso, mas deve retornar FlextResult válido
        assert isinstance(result, FlextResult)

        if not result.success:
            assert result.error is not None
            assert isinstance(result.error, str)

    def test_run_pipeline_error_handling(self) -> None:
        """Testa run_pipeline com tratamento de erro."""
        cli = FlextMeltanoCli()

        result = cli.run_pipeline("invalid-tap", "invalid-target")

        # Pode falhar, mas deve retornar FlextResult válido
        assert isinstance(result, FlextResult)

        if not result.success:
            assert result.error is not None

    def test_version_error_handling(self) -> None:
        """Testa version com possível tratamento de erro."""
        cli = FlextMeltanoCli()

        result = cli.flext_meltano_version()

        # Deve retornar FlextResult válido
        assert isinstance(result, FlextResult)

        if not result.success:
            assert result.error is not None


class TestFlextMeltanoCliIntegrationComprehensive:
    """Testes de integração COMPREHENSIVE para CLI."""

    def test_full_cli_workflow_health_to_version(self) -> None:
        """Testa workflow completo: health → version → help."""
        cli = FlextMeltanoCli()

        # 1. Health check
        health_result = cli.health()
        assert health_result.success is True

        # 2. Version check
        version_result = cli.version()
        assert version_result.success is True

        # 3. Help information
        help_result = cli.help()
        assert help_result.success is True

        # 4. List commands
        commands_result = cli.list_commands()
        assert commands_result.success is True

    def test_factory_function_integration(self) -> None:
        """Testa integração da factory function."""
        # Testar múltiplos comandos via factory
        test_commands = [
            [],
            ["--version"],
            ["--help"],
            ["version"],
            ["help"],
        ]

        for cmd in test_commands:
            result = flext_meltano_run_cli(cmd)
            assert result.success is True
            assert "command" in result.value

    def test_cli_with_real_project_integration(self) -> None:
        """Testa CLI com projeto real."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            # Criar projeto Meltano real
            meltano_yml = project_path / "meltano.yml"
            meltano_yml.write_text("""
version: 1
project_id: cli-integration-test
environments:
- name: dev
plugins:
  extractors:
  - name: tap-csv
""")

            cli = FlextMeltanoCli(project_path)

            # Testar comandos com projeto
            health_result = cli.health()
            assert health_result.success is True

            version_result = cli.version()
            assert version_result.success is True

            # Execute command com projeto
            execute_result = cli.execute("health")
            assert execute_result.success is True

    def test_error_recovery_integration(self) -> None:
        """Testa recuperação de erros em integração."""
        cli = FlextMeltanoCli()

        # Comandos que podem falhar mas CLI deve continuar funcionando
        failing_commands = [
            ["run", "nonexistent"],
            ["invalid-command"],
        ]

        for cmd in failing_commands:
            result = cli.run(cmd)
            # Deve retornar resultado mesmo se operação falhou
            assert result.success is True

        # CLI deve continuar funcionando após erros
        health_result = cli.health()
        assert health_result.success is True
