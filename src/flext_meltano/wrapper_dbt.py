"""DBT Core Wrapper - Adapta DBT Core para padrões flext-core.

FUNÇÃO 1: Wrapper para DBT Core adaptando para flext-core
- MeltanoDbtWrapper: Wrapper principal
- FlextDbtAdapter: Adaptador de tipos
- Real DBT Core integration (NO MOCKS)
"""

from __future__ import annotations

from pathlib import Path

# Importar DBT Core REAL - bibliotecas instaladas
from dbt.cli.main import dbtRunner
from flext_core import FlextDomainService, FlextResult, get_logger

DBT_AVAILABLE = True

logger = get_logger(__name__)

# =============================================================================
# DBT CORE WRAPPER - REAL IMPLEMENTATION
# =============================================================================


class MeltanoDbtWrapper(FlextDomainService):
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
    def logger(self) -> object:
        """Get logger instance."""
        return get_logger(self.__class__.__name__)

    def execute(self) -> FlextResult[dict[str, object]]:
        """Execute DBT service operation (required by FlextDomainService).

        Returns:
            FlextResult contendo informações do serviço

        """
        return FlextResult.ok(
            {
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
            }
        )

    def create_runner(self, project_dir: Path | None = None) -> FlextResult[object]:
        """Cria dbtRunner usando FlextResult pattern.

        Args:
            project_dir: Diretório do projeto DBT (opcional)

        Returns:
            FlextResult contendo dbtRunner instance ou erro

        """
        try:
            if not DBT_AVAILABLE:
                return FlextResult.fail("DBT Core not available - install dbt-core")

            self.logger.info(
                "Creating DBT runner",
                project_dir=str(project_dir) if project_dir else None,
            )

            # Criar instância do runner
            runner = dbtRunner()

            if project_dir and not project_dir.exists():
                return FlextResult.fail(
                    f"DBT project directory not found: {project_dir}"
                )

            self.logger.info("DBT runner created successfully")
            return FlextResult.ok(runner)

        except Exception as e:
            error_msg = f"Failed to create DBT runner: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def run_models(
        self,
        runner: object,
        models: list[str] | None = None,
        project_dir: Path | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Executa modelos DBT com observabilidade flext-core.

        Args:
            runner: Instância dbtRunner
            models: Lista de modelos para executar (None = todos)
            project_dir: Diretório do projeto DBT

        Returns:
            FlextResult contendo resultado da execução

        """
        try:
            self.logger.info(
                "Running DBT models",
                models=models,
                project_dir=str(project_dir) if project_dir else None,
            )

            # Construir comando DBT
            cmd = ["run"]

            # Adicionar modelos específicos
            if models:
                cmd.extend(["--models", *models])

            # Adicionar diretório do projeto
            if project_dir:
                cmd.extend(["--project-dir", str(project_dir)])

            # Executar comando
            self.logger.info("Executing DBT command", command=cmd)
            result = runner.invoke(cmd)

            # Processar resultado
            if result.is_success:
                execution_result = {
                    "success": True,
                    "command": cmd,
                    "models_processed": len(models) if models else "all",
                    "result": result.result if hasattr(result, "result") else None,
                }

                self.logger.info(
                    "DBT models executed successfully",
                    models_count=len(models) if models else "all",
                )
                return FlextResult.ok(execution_result)
            error_msg = f"DBT run failed with exit code {result.exit_code}"
            self.logger.exception(error_msg, exit_code=result.exit_code)
            return FlextResult.fail(error_msg)

        except Exception as e:
            error_msg = f"Failed to run DBT models: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def test_models(
        self,
        runner: object,
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
                "success": result.is_success,
                "command": cmd,
                "models_tested": len(models) if models else "all",
                "exit_code": result.exit_code,
                "result": result.result if hasattr(result, "result") else None,
            }

            if result.is_success:
                self.logger.info(
                    "DBT tests passed successfully",
                    models_count=len(models) if models else "all",
                )
            else:
                self.logger.warning(
                    "DBT tests failed",
                    exit_code=result.exit_code,
                    models_count=len(models) if models else "all",
                )

            return FlextResult.ok(test_result)

        except Exception as e:
            error_msg = f"Failed to test DBT models: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def compile_project(
        self, runner: object, project_dir: Path | None = None
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
                "success": result.is_success,
                "command": cmd,
                "exit_code": result.exit_code,
                "result": result.result if hasattr(result, "result") else None,
            }

            if result.is_success:
                self.logger.info("DBT project compiled successfully")
            else:
                self.logger.exception(
                    "DBT compilation failed", exit_code=result.exit_code
                )

            return FlextResult.ok(compile_result)

        except Exception as e:
            error_msg = f"Failed to compile DBT project: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def generate_docs(
        self, runner: object, project_dir: Path | None = None
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
                "success": result.is_success,
                "command": cmd,
                "exit_code": result.exit_code,
                "result": result.result if hasattr(result, "result") else None,
            }

            if result.is_success:
                self.logger.info("DBT documentation generated successfully")
            else:
                self.logger.exception(
                    "DBT docs generation failed", exit_code=result.exit_code
                )

            return FlextResult.ok(docs_result)

        except Exception as e:
            error_msg = f"Failed to generate DBT docs: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)


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
            flext_results = {
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
            for result in dbt_results.get("results", []):
                flext_result = {
                    "unique_id": result.get("unique_id"),
                    "status": result.get("status"),
                    "execution_time": result.get("execution_time"),
                    "message": result.get("message"),
                    "compiled_code": result.get("compiled_code"),
                }
                flext_results["results"].append(flext_result)

            return FlextResult.ok(flext_results)

        except Exception as e:
            return FlextResult.fail(f"Failed to adapt DBT results: {e}")

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
            flext_manifest = {
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
            for node_id, node in dbt_manifest.get("nodes", {}).items():
                flext_node = {
                    "name": node.get("name"),
                    "resource_type": node.get("resource_type"),
                    "database": node.get("database"),
                    "schema": node.get("schema"),
                    "depends_on": node.get("depends_on", {}).get("nodes", []),
                }
                flext_manifest["nodes"][node_id] = flext_node

            # Processar sources
            for source_id, source in dbt_manifest.get("sources", {}).items():
                flext_source = {
                    "name": source.get("name"),
                    "source_name": source.get("source_name"),
                    "database": source.get("database"),
                    "schema": source.get("schema"),
                }
                flext_manifest["sources"][source_id] = flext_source

            return FlextResult.ok(flext_manifest)

        except Exception as e:
            return FlextResult.fail(f"Failed to adapt DBT manifest: {e}")


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = ["DBT_AVAILABLE", "FlextDbtAdapter", "MeltanoDbtWrapper"]
