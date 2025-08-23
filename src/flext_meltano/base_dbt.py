"""DBT Core Wrapper - Adapta DBT Core para padrões flext-core.

FUNÇÃO 1: Wrapper para DBT Core adaptando para flext-core
- MeltanoDbtWrapper: Wrapper principal
- FlextDbtAdapter: Adaptador de tipos
- Real DBT Core integration (NO MOCKS)
"""

from __future__ import annotations

from pathlib import Path

from dbt.cli.main import dbtRunner
from flext_core import FlextDomainService, FlextLogger, FlextResult, get_logger

DBT_AVAILABLE = True

logger = get_logger(__name__)

# =============================================================================
# DBT CORE WRAPPER - REAL IMPLEMENTATION
# =============================================================================


class MeltanoDbtWrapper(FlextDomainService[object]):
    """Wrapper principal para DBT Core → flext-core.

    Adapta DBT Core execution para flext-core patterns, usando FlextResult
    para error handling e integrando com flext-core observability.
    """

    def __init__(self) -> None:
        super().__init__()

        # Validar disponibilidade do DBT
        if not DBT_AVAILABLE:
            logger.warning("DBT Core not available - some functions will fail")

    @property
    def logger(self) -> FlextLogger:
        """Get logger instance."""
        return get_logger(self.__class__.__name__)

    def execute(self) -> FlextResult[object]:
        """Execute DBT service operation (required by FlextDomainService).

        Returns:
            FlextResult contendo informações do serviço

        """
        return FlextResult[object].ok({
            "service": "MeltanoDbtWrapper",
            "status": "ready",
            "dbt_available": DBT_AVAILABLE,
            "capabilities": [
                "create_runner",
                "run_models",
                "test_models",
                "compile_project",
                "generate_docs",
            ],
        })

    def create_runner(self, project_dir: Path | None = None) -> FlextResult[dbtRunner]:
        """Cria dbtRunner usando FlextResult pattern.

        Args:
            project_dir: Diretório do projeto DBT (opcional)

        Returns:
            FlextResult contendo dbtRunner instance ou erro

        """
        try:
            if not DBT_AVAILABLE:
                return FlextResult[dbtRunner].fail(
                    "DBT Core not available - install dbt-core"
                )

            self.logger.info(
                "Creating DBT runner",
                project_dir=str(project_dir) if project_dir else None,
            )

            # Criar instância do runner
            runner = dbtRunner()

            if project_dir and not project_dir.exists():
                return FlextResult[dbtRunner].fail(
                    f"DBT project directory not found: {project_dir}"
                )

            self.logger.info("DBT runner created successfully")
            return FlextResult[dbtRunner].ok(runner)

        except Exception as e:
            error_msg = f"Failed to create DBT runner: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult[dbtRunner].fail(error_msg)

    # Using FlextDecorators for performance monitoring - real DBT API execution
    def run_models_real(
        self,
        project_dir: Path,
        models: list[str] | None = None,
        profiles_dir: Path | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Executa modelos DBT usando API nativa real dbtRunner.invoke().

        Args:
            project_dir: Diretório do projeto DBT
            models: Lista de modelos para executar (None = todos)
            profiles_dir: Diretório dos profiles DBT (opcional)

        Returns:
            FlextResult contendo resultado da execução com estrutura real

        """
        try:
            self.logger.info(
                "Running DBT models via native dbtRunner.invoke API",
                models=models,
                project_dir=str(project_dir),
                profiles_dir=str(profiles_dir) if profiles_dir else None,
            )

            if not DBT_AVAILABLE:
                return FlextResult[dict[str, object]].fail("DBT Core not available")

            # Validar diretório do projeto
            if not project_dir.exists():
                return FlextResult[dict[str, object]].fail(
                    f"DBT project directory not found: {project_dir}"
                )

            # Verificar se é um projeto DBT válido
            dbt_project_yml = project_dir / "dbt_project.yml"
            if not dbt_project_yml.exists():
                return FlextResult[dict[str, object]].fail(
                    f"Not a DBT project: dbt_project.yml not found in {project_dir}"
                )

            # Criar dbtRunner usando API real
            runner = dbtRunner()

            # Construir comando DBT usando argumentos reais
            cmd_args = ["run"]

            # Adicionar modelos específicos usando sintaxe real DBT
            if models:
                cmd_args.extend(["--models", *models])

            # Adicionar diretório do projeto usando sintaxe real DBT
            cmd_args.extend(["--project-dir", str(project_dir)])

            # Adicionar profiles-dir se especificado
            if profiles_dir:
                cmd_args.extend(["--profiles-dir", str(profiles_dir)])

            self.logger.info(
                "Invoking dbtRunner with real API",
                command_args=cmd_args,
            )

            # Executar usando API nativa real dbtRunner.invoke()
            result = runner.invoke(cmd_args)

            # Processar resultado usando estrutura real do DBT
            execution_result = {
                "success": result.success,
                "command": cmd_args,
                "models_processed": len(models) if models else "all",
                "result_data": result.result if hasattr(result, "result") else None,
                "exception": str(result.exception) if result.exception else None,
                "execution_method": "dbt_runner_invoke",
            }

            # Adicionar informações extras do resultado se disponíveis
            if hasattr(result, "args"):
                execution_result["parsed_args"] = str(result.args)

            if result.success:
                self.logger.info(
                    "DBT models executed successfully via dbtRunner.invoke",
                    models_count=len(models) if models else "all",
                    result_success=result.success,
                )
                return FlextResult[dict[str, object]].ok(execution_result)

            # Se não teve sucesso, incluir detalhes do erro
            error_msg = f"DBT run failed via dbtRunner.invoke: {result.exception}"
            execution_result["error_details"] = error_msg

            self.logger.exception(
                error_msg,
                exception=str(result.exception)
                if result.exception
                else "Unknown error",
                result_success=result.success,
            )
            return FlextResult[dict[str, object]].ok(execution_result)

        except Exception as e:
            error_msg = f"Failed to run DBT models via dbtRunner.invoke: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult[dict[str, object]].fail(error_msg)

    def test_models(
        self,
        runner: dbtRunner,
        models: list[str] | None = None,
        project_dir: Path | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Testa modelos DBT com resultado estruturado.

        Args:
            runner: Instância dbtRunner
            models: Lista de modelos para testar (None = todos)
            project_dir: Diretório do projeto DBT

        Returns:
            FlextResult contendo resultado dos testes

        """
        try:
            self.logger.info(
                "Testing DBT models",
                models=models,
                project_dir=str(project_dir) if project_dir else None,
            )

            # Construir comando DBT
            cmd = ["test"]

            # Adicionar modelos específicos
            if models:
                cmd.extend(["--models", *models])

            # Adicionar diretório do projeto
            if project_dir:
                cmd.extend(["--project-dir", str(project_dir)])

            # Executar comando
            self.logger.info("Executing DBT test command", command=cmd)
            result = runner.invoke(cmd)

            # Processar resultado
            test_result = {
                "success": result.success,
                "command": cmd,
                "models_tested": len(models) if models else "all",
                "exit_code": getattr(result, "exit_code", 0 if result.success else 1),
                "result": result.result if hasattr(result, "result") else None,
            }

            if result.success:
                self.logger.info(
                    "DBT tests passed successfully",
                    models_count=len(models) if models else "all",
                )
            else:
                self.logger.warning(
                    "DBT tests failed",
                    exit_code=getattr(result, "exit_code", 1),
                    models_count=len(models) if models else "all",
                )

            return FlextResult[dict[str, object]].ok(test_result)

        except Exception as e:
            error_msg = f"Failed to test DBT models: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult[dict[str, object]].fail(error_msg)

    def compile_project(
        self, runner: dbtRunner, project_dir: Path | None = None
    ) -> FlextResult[dict[str, object]]:
        """Compila projeto DBT.

        Args:
            runner: Instância dbtRunner
            project_dir: Diretório do projeto DBT

        Returns:
            FlextResult contendo resultado da compilação

        """
        try:
            self.logger.info(
                "Compiling DBT project",
                project_dir=str(project_dir) if project_dir else None,
            )

            # Construir comando DBT
            cmd = ["compile"]

            # Adicionar diretório do projeto
            if project_dir:
                cmd.extend(["--project-dir", str(project_dir)])

            # Executar comando
            self.logger.info("Executing DBT compile command", command=cmd)
            result = runner.invoke(cmd)

            # Processar resultado
            compile_result = {
                "success": result.success,
                "command": cmd,
                "exit_code": getattr(result, "exit_code", 0 if result.success else 1),
                "result": result.result if hasattr(result, "result") else None,
            }

            if result.success:
                self.logger.info("DBT project compiled successfully")
            else:
                self.logger.exception(
                    "DBT compilation failed", exit_code=getattr(result, "exit_code", 1)
                )

            return FlextResult[dict[str, object]].ok(compile_result)

        except Exception as e:
            error_msg = f"Failed to compile DBT project: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult[dict[str, object]].fail(error_msg)

    def generate_docs(
        self, runner: dbtRunner, project_dir: Path | None = None
    ) -> FlextResult[dict[str, object]]:
        """Gera documentação DBT.

        Args:
            runner: Instância dbtRunner
            project_dir: Diretório do projeto DBT

        Returns:
            FlextResult contendo resultado da geração de docs

        """
        try:
            self.logger.info(
                "Generating DBT documentation",
                project_dir=str(project_dir) if project_dir else None,
            )

            # Construir comando DBT
            cmd = ["docs", "generate"]

            # Adicionar diretório do projeto
            if project_dir:
                cmd.extend(["--project-dir", str(project_dir)])

            # Executar comando
            self.logger.info("Executing DBT docs generate command", command=cmd)
            result = runner.invoke(cmd)

            # Processar resultado
            docs_result = {
                "success": result.success,
                "command": cmd,
                "exit_code": getattr(result, "exit_code", 0 if result.success else 1),
                "result": result.result if hasattr(result, "result") else None,
            }

            if result.success:
                self.logger.info("DBT documentation generated successfully")
            else:
                self.logger.exception(
                    "DBT docs generation failed",
                    exit_code=getattr(result, "exit_code", 1),
                )

            return FlextResult[dict[str, object]].ok(docs_result)

        except Exception as e:
            error_msg = f"Failed to generate DBT docs: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult[dict[str, object]].fail(error_msg)


# =============================================================================
# DBT TYPE ADAPTERS - FLEXT-CORE INTEGRATION
# =============================================================================


class FlextDbtAdapter:
    """Adaptador de tipos DBT → FLEXT patterns."""

    @staticmethod
    def adapt_run_results(
        dbt_results: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Converte resultados DBT para FlextDbtResults pattern.

        Args:
            dbt_results: Resultados DBT originais

        Returns:
            FlextResult contendo resultados adaptados

        """
        try:
            # Adaptar para formato FlextDbtResults
            flext_results: dict[str, object] = {
                "version": "1.0",
                "execution_time": dbt_results.get("execution_time"),
                "success": dbt_results.get("success", False),
                "results": [],
                "metadata": {
                    "dbt_version": dbt_results.get("dbt_version"),
                    "generated_at": dbt_results.get("generated_at"),
                },
            }

            # Processar resultados individuais
            results_data = dbt_results.get("results", [])
            if isinstance(results_data, list):
                results_list = flext_results["results"]
                if isinstance(results_list, list):
                    for result in results_data:
                        if isinstance(result, dict):
                            flext_result = {
                                "unique_id": result.get("unique_id"),
                                "status": result.get("status"),
                                "execution_time": result.get("execution_time"),
                                "message": result.get("message"),
                                "compiled_code": result.get("compiled_code"),
                            }
                            results_list.append(flext_result)

            return FlextResult[dict[str, object]].ok(flext_results)

        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Failed to adapt DBT results: {e}"
            )

    @staticmethod
    def adapt_manifest(
        dbt_manifest: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Converte manifest DBT para FlextDbtManifest pattern.

        Args:
            dbt_manifest: Manifest DBT original

        Returns:
            FlextResult contendo manifest adaptado

        """
        try:
            # Adaptar para formato FlextDbtManifest
            flext_manifest: dict[str, object] = {
                "version": "1.0",
                "nodes": {},
                "sources": {},
                "macros": {},
                "metadata": {
                    "dbt_version": dbt_manifest.get("dbt_version"),
                    "generated_at": dbt_manifest.get("generated_at"),
                    "adapter_type": dbt_manifest.get("adapter_type"),
                },
            }

            # Processar nodes (models, tests, etc.)
            nodes_data = dbt_manifest.get("nodes", {})
            if isinstance(nodes_data, dict):
                nodes_dict = flext_manifest["nodes"]
                if isinstance(nodes_dict, dict):
                    for node_id, node in nodes_data.items():
                        if isinstance(node, dict):
                            depends_on_data = node.get("depends_on", {})
                            depends_on_nodes = []
                            if isinstance(depends_on_data, dict):
                                depends_on_nodes = depends_on_data.get("nodes", [])

                            flext_node = {
                                "name": node.get("name"),
                                "resource_type": node.get("resource_type"),
                                "database": node.get("database"),
                                "schema": node.get("schema"),
                                "depends_on": depends_on_nodes,
                            }
                            nodes_dict[node_id] = flext_node

            # Processar sources
            sources_data = dbt_manifest.get("sources", {})
            if isinstance(sources_data, dict):
                sources_dict = flext_manifest["sources"]
                if isinstance(sources_dict, dict):
                    for source_id, source in sources_data.items():
                        if isinstance(source, dict):
                            flext_source = {
                                "name": source.get("name"),
                                "source_name": source.get("source_name"),
                                "database": source.get("database"),
                                "schema": source.get("schema"),
                            }
                            sources_dict[source_id] = flext_source

            return FlextResult[dict[str, object]].ok(flext_manifest)

        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Failed to adapt DBT manifest: {e}"
            )


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = ["DBT_AVAILABLE", "FlextDbtAdapter", "MeltanoDbtWrapper"]
