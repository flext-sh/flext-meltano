"""Execution Engine - Runtime execution via Go bridge for Meltano and DBT.

FUNÇÃO 2: Runtime execution via Go bridge
- FlextMeltanoExecutor: Subprocess-based execution for Go calls
- FlextExecutionResult: Structured results for Go consumption
- Real subprocess integration (NO MOCKS)
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from flext_core import FlextDomainService, FlextResult, get_logger

from .meltano_wrapper import MeltanoBridge
from .dbt_wrapper import MeltanoDbtWrapper

logger = get_logger(__name__)

# =============================================================================
# EXECUTION ENGINE - RUNTIME FOR GO BRIDGE
# =============================================================================


class FlextMeltanoExecutor(FlextDomainService):
    """Executor principal para runtime via Go bridge.

    Executa comandos Meltano e DBT via subprocess para integração com FlexCore Go,
    fornecendo resultados estruturados em JSON para consumo pelos serviços Go.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def logger(self) -> object:
        """Get logger instance."""
        return get_logger(self.__class__.__name__)

    def execute(self) -> FlextResult[dict[str, Any]]:
        """Execute Meltano executor operation (required by FlextDomainService).

        Returns:
            FlextResult contendo informações do serviço

        """
        return FlextResult.ok(
            {
                "service": "FlextMeltanoExecutor",
                "status": "ready",
                "capabilities": [
                    "execute_meltano_command",
                    "execute_dbt_command",
                    "run_elt_pipeline",
                    "install_plugin",
                    "get_project_info",
                ],
            }
        )

    def execute_meltano_command(
        self, project_root: Path, command: list[str], timeout: int = 300
    ) -> FlextResult[dict[str, Any]]:
        """Executa comando Meltano usando API nativa com resultado estruturado.

        Args:
            project_root: Diretório do projeto Meltano
            command: Comando meltano para executar (ex: ["run", "tap-csv", "target-csv"])
            timeout: Timeout em segundos (padrão 5 minutos) - não usado na API nativa

        Returns:
            FlextResult contendo resultado estruturado para Go

        """
        try:
            self.logger.info(
                "Executing Meltano command natively",
                command=command,
                project_root=str(project_root),
                timeout=timeout,
            )

            # Validar projeto Meltano
            if not (project_root / "meltano.yml").exists():
                return FlextResult.fail(f"Not a Meltano project: {project_root}")

            # Usar MeltanoBridge para execução nativa
            bridge = MeltanoBridge()
            result = bridge.run_meltano_command(project_root, command)

            if result.is_success:
                # Adaptar resultado do bridge para formato Go
                bridge_result = result.value
                execution_result = {
                    "success": bridge_result.get("success", False),
                    "exit_code": bridge_result.get("exit_code", 0),
                    "stdout": bridge_result.get("stdout", ""),
                    "stderr": bridge_result.get("stderr", ""),
                    "command": command,
                    "context": {
                        "project_root": str(project_root),
                        "timeout": timeout,
                        "execution_method": "native_api",
                    },
                    "parsed_output": self._parse_output(bridge_result.get("stdout", "")),
                }

                self.logger.info(
                    "Meltano command executed successfully via native API",
                    command=command,
                    exit_code=execution_result["exit_code"],
                )
                return FlextResult.ok(execution_result)
            error_msg = f"Native Meltano command failed: {result.error}"
            self.logger.exception(error_msg, command=command)
            return FlextResult.fail(error_msg)

        except Exception as e:
            error_msg = f"Failed to execute native Meltano command {command}: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def execute_dbt_command(
        self, project_root: Path, command: list[str], timeout: int = 300
    ) -> FlextResult[dict[str, Any]]:
        """Executa comando DBT usando API nativa com resultado estruturado.

        Args:
            project_root: Diretório do projeto DBT
            command: Comando dbt para executar (ex: ["run", "--models", "model1"])
            timeout: Timeout em segundos (padrão 5 minutos) - não usado na API nativa

        Returns:
            FlextResult contendo resultado estruturado para Go

        """
        try:
            self.logger.info(
                "Executing DBT command natively",
                command=command,
                project_root=str(project_root),
                timeout=timeout,
            )

            # Validar projeto DBT
            if not (project_root / "dbt_project.yml").exists():
                return FlextResult.fail(f"Not a DBT project: {project_root}")

            # Usar MeltanoDbtWrapper para execução nativa
            dbt_wrapper = MeltanoDbtWrapper()

            # Criar runner DBT
            runner_result = dbt_wrapper.create_runner(project_root)
            if not runner_result.is_success:
                return FlextResult.fail(f"Failed to create DBT runner: {runner_result.error}")

            runner = runner_result.value

            # Executar comando DBT baseado no tipo
            if command[0] == "run":
                # Extrair modelos se especificados
                models = None
                if "--models" in command:
                    models_index = command.index("--models")
                    if models_index + 1 < len(command):
                        models = command[models_index + 1].split(",")

                result = dbt_wrapper.run_models(runner, models, project_root)

            elif command[0] == "test":
                # Extrair modelos se especificados
                models = None
                if "--models" in command:
                    models_index = command.index("--models")
                    if models_index + 1 < len(command):
                        models = command[models_index + 1].split(",")

                result = dbt_wrapper.test_models(runner, models, project_root)

            elif command[0] == "compile":
                result = dbt_wrapper.compile_project(runner, project_root)

            elif command[0] == "docs" and len(command) > 1 and command[1] == "generate":
                result = dbt_wrapper.generate_docs(runner, project_root)

            else:
                return FlextResult.fail(f"Unsupported DBT command: {command[0]}")

            if result.is_success:
                # Adaptar resultado do wrapper para formato Go
                dbt_result = result.value
                execution_result = {
                    "success": dbt_result.get("success", False),
                    "exit_code": dbt_result.get("exit_code", 0),
                    "stdout": json.dumps(dbt_result) if dbt_result else "",
                    "stderr": "",
                    "command": command,
                    "context": {
                        "project_root": str(project_root),
                        "timeout": timeout,
                        "execution_method": "native_dbt_api",
                    },
                    "parsed_output": dbt_result,
                }

                self.logger.info(
                    "DBT command executed successfully via native API",
                    command=command,
                    exit_code=execution_result["exit_code"],
                )
                return FlextResult.ok(execution_result)
            error_msg = f"Native DBT command failed: {result.error}"
            self.logger.exception(error_msg, command=command)
            return FlextResult.fail(error_msg)

        except Exception as e:
            error_msg = f"Failed to execute native DBT command {command}: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def run_elt_pipeline(
        self, project_root: Path, tap_name: str, target_name: str, timeout: int = 600
    ) -> FlextResult[dict[str, Any]]:
        """Executa pipeline ELT completo Meltano.

        Args:
            project_root: Diretório do projeto Meltano
            tap_name: Nome do tap (ex: "tap-csv")
            target_name: Nome do target (ex: "target-csv")
            timeout: Timeout em segundos (padrão 10 minutos)

        Returns:
            FlextResult contendo resultado do pipeline

        """
        try:
            self.logger.info(
                "Running ELT pipeline",
                tap=tap_name,
                target=target_name,
                project_root=str(project_root),
            )

            # Executar pipeline via meltano run
            command = ["run", tap_name, target_name]
            return self.execute_meltano_command(project_root, command, timeout)

        except Exception as e:
            error_msg = f"Failed to run ELT pipeline {tap_name}->{target_name}: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def install_plugin(
        self, project_root: Path, plugin_type: str, plugin_name: str, timeout: int = 300
    ) -> FlextResult[dict[str, Any]]:
        """Instala plugin Meltano via CLI.

        Args:
            project_root: Diretório do projeto Meltano
            plugin_type: Tipo do plugin (extractor, loader, transformer)
            plugin_name: Nome do plugin
            timeout: Timeout em segundos

        Returns:
            FlextResult contendo resultado da instalação

        """
        try:
            self.logger.info(
                "Installing Meltano plugin",
                plugin_type=plugin_type,
                plugin_name=plugin_name,
                project_root=str(project_root),
            )

            # Executar instalação via meltano add
            command = ["add", plugin_type, plugin_name]
            return self.execute_meltano_command(project_root, command, timeout)

        except Exception as e:
            error_msg = f"Failed to install plugin {plugin_name}: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def get_project_info(self, project_root: Path) -> FlextResult[dict[str, Any]]:
        """Obtém informações do projeto Meltano/DBT.

        Args:
            project_root: Diretório do projeto

        Returns:
            FlextResult contendo informações do projeto

        """
        try:
            self.logger.info("Getting project info", project_root=str(project_root))

            project_info = {
                "project_root": str(project_root),
                "project_type": None,
                "config_files": [],
                "plugins": [],
                "valid": False,
            }

            # Detectar tipo de projeto
            if (project_root / "meltano.yml").exists():
                project_info["project_type"] = "meltano"
                project_info["config_files"].append("meltano.yml")
                project_info["valid"] = True

                # Obter informações de plugins via meltano config
                config_result = self.execute_meltano_command(
                    project_root, ["config", "list"], 30
                )
                if config_result.is_success:
                    project_info["meltano_config"] = config_result.value

            if (project_root / "dbt_project.yml").exists():
                if project_info["project_type"]:
                    project_info["project_type"] = "meltano+dbt"
                else:
                    project_info["project_type"] = "dbt"
                project_info["config_files"].append("dbt_project.yml")
                project_info["valid"] = True

            if not project_info["valid"]:
                return FlextResult.fail(f"No valid project found in {project_root}")

            self.logger.info(
                "Project info retrieved", project_type=project_info["project_type"]
            )
            return FlextResult.ok(project_info)

        except Exception as e:
            error_msg = f"Failed to get project info: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def _parse_output(self, output: str) -> dict[str, Any] | None:
        """Tenta parsear output como JSON.

        Args:
            output: String de output para parsear

        Returns:
            Dict parseado ou None se não for JSON válido

        """
        if not output:
            return None

        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return None


# =============================================================================
# EXECUTION RESULT TYPES - GO COMPATIBILITY
# =============================================================================


class FlextExecutionResult:
    """Wrapper para resultados de execução compatíveis com Go."""

    @staticmethod
    def success(data: dict[str, Any]) -> dict[str, Any]:
        """Cria resultado de sucesso para Go bridge.

        Args:
            data: Dados do resultado

        Returns:
            Resultado estruturado para JSON

        """
        return {
            "success": True,
            "data": data,
            "error": None,
            "timestamp": datetime.now(tz=UTC).isoformat(),
        }

    @staticmethod
    def failure(error_message: str, error_code: str | None = None) -> dict[str, Any]:
        """Cria resultado de erro para Go bridge.

        Args:
            error_message: Mensagem de erro
            error_code: Código de erro opcional

        Returns:
            Resultado de erro estruturado para JSON

        """
        return {
            "success": False,
            "data": None,
            "error": {
                "message": error_message,
                "code": error_code or "EXECUTION_ERROR",
            },
            "timestamp": datetime.now(tz=UTC).isoformat(),
        }


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = ["FlextExecutionResult", "FlextMeltanoExecutor"]
