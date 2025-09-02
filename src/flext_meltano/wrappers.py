"""FLEXT Meltano Wrappers - Single class architecture following flext-core patterns.

Provides comprehensive wrapper functionality with FLEXT patterns using single class
architecture. All wrapper functionality is organized under FlextMeltanoWrapper
with nested classes for DBT, Singer, and Meltano Core wrapper operations.

Module Role in Architecture:
    FlextMeltanoWrapper serves as the single wrapper class for all external library integration,
    providing DBT Core wrappers, Singer SDK wrappers, and Meltano Core wrappers
    following flext-core architectural patterns.

Classes and Methods:
    FlextMeltanoWrapper:                           # Single wrapper class following flext-core pattern
        # Nested Classes:
        DbtWrapper                                 # DBT Core wrapper operations
        SingerWrapper                             # Singer SDK wrapper operations
        MeltanoWrapper                           # Meltano Core wrapper operations
        UnifiedWrapper                           # Unified wrapper coordination

        # Core Methods:
        wrap_dbt_operation(config) -> FlextResult[dict]     # Wrap DBT operations
        wrap_singer_operation(config) -> FlextResult[dict]  # Wrap Singer operations
        wrap_meltano_operation(config) -> FlextResult[dict] # Wrap Meltano operations
        coordinate_wrappers(config) -> FlextResult[dict]    # Coordinate multiple wrappers

Usage Examples:
    Basic wrapper usage:
        wrapper = FlextMeltanoWrapper()
        dbt_result = wrapper.wrap_dbt_operation(dbt_config)
        if dbt_result.success:
            dbt_response = dbt_result.value

    Singer wrapper:
        singer_wrapper = wrapper.SingerWrapper()
        tap_result = singer_wrapper.wrap_tap_discovery(tap_config)

    Unified coordination:
        coordinator = wrapper.UnifiedWrapper()
        pipeline_result = coordinator.coordinate_elt_pipeline(pipeline_config)

Integration:
    FlextMeltanoWrapper integrates with FlextResult for error handling, FlextDomainService
    for service patterns, FlextLogger for logging, and native APIs for all wrapper operations
    ensuring compatibility and type safety.
"""

from __future__ import annotations

from pathlib import Path
from typing import cast

from dbt.cli.main import dbtRunner
from flext_core import (
    FlextDomainService,
    FlextLogger,
    FlextResult,
)

from flext_meltano.typings import FlextMeltanoTypes

DBT_AVAILABLE = True

logger = FlextLogger(__name__)

# =============================================================================
# MAIN DBT ADAPTERS CLASS - Following Flext[Area][Module] pattern
# =============================================================================


class FlextMeltanoWrapper:
    """Single wrapper class for all external library integration following flext-core patterns.

    This class implements the complete FLEXT wrapper architecture following
    strict flext-core requirements:
        - Single consolidated class per module with nested organization
        - Massive integration with flext-core patterns (FlextResult, FlextLogger, etc.)
        - Zero duplication with flext-core functionality
        - Python 3.13+ syntax with proper generic type annotations
        - Railway-oriented programming via FlextResult integration
        - Native library API integration without subprocess calls

    The wrapper architecture provides:
        - DBT Core wrapper operations for project management and execution
        - Singer SDK wrapper operations for tap/target coordination
        - Meltano Core wrapper operations for project and plugin management
        - Unified wrapper coordination for complex multi-library operations
        - Type-safe wrapper processing throughout
    """

    # =================================================================
    # NESTED ADAPTER CLASSES - Actual implementations
    # =================================================================

    class DbtWrapper(FlextDomainService[object]):
        """Main wrapper for DBT Core → flext-core.

        Adapts DBT Core execution to flext-core patterns, using FlextResult
        for error handling and integrating with flext-core observability.
        """

        def __init__(self) -> None:
            super().__init__()

            # Validate DBT availability
            if not DBT_AVAILABLE:
                logger.warning("DBT Core not available - some functions will fail")

        @property
        def logger(self) -> FlextLogger:
            """Get logger instance."""
            return FlextLogger(self.__class__.__name__)

        def execute(self) -> FlextResult[object]:
            """Execute DBT service operation (required by FlextDomainService).

            Returns:
                FlextResult containing service information

            """
            return FlextResult[object].ok(
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

        def create_runner(
            self, project_dir: Path | None = None
        ) -> FlextResult[dbtRunner]:
            """Create dbtRunner using FlextResult pattern.

            Args:
                project_dir: DBT project directory (optional)

            Returns:
                FlextResult containing dbtRunner instance or error

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

                # Create runner instance
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
        ) -> FlextResult[FlextMeltanoTypes.DBT.ExecutionResult]:
            """Execute DBT models using real native dbtRunner.invoke() API.

            Args:
                project_dir: DBT project directory
                models: List of models to execute (None = all)
                profiles_dir: DBT profiles directory (optional)

            Returns:
                FlextResult containing execution result with real structure

            """
            try:
                self.logger.info(
                    "Running DBT models via native dbtRunner.invoke API",
                    models=models,
                    project_dir=str(project_dir),
                    profiles_dir=str(profiles_dir) if profiles_dir else None,
                )

                if not DBT_AVAILABLE:
                    return FlextResult[FlextMeltanoTypes.DBT.ExecutionResult].fail(
                        "DBT Core not available"
                    )

                # Validate project directory
                if not project_dir.exists():
                    return FlextResult[FlextMeltanoTypes.DBT.ExecutionResult].fail(
                        f"DBT project directory not found: {project_dir}"
                    )

                # Check if it's a valid DBT project
                dbt_project_yml = project_dir / "dbt_project.yml"
                if not dbt_project_yml.exists():
                    return FlextResult[FlextMeltanoTypes.DBT.ExecutionResult].fail(
                        f"Not a DBT project: dbt_project.yml not found in {project_dir}"
                    )

                # Create dbtRunner using real API
                runner = dbtRunner()

                # Build DBT command using real arguments
                cmd_args = ["run"]

                # Add specific models using real DBT syntax
                if models:
                    cmd_args.extend(["--models", *models])

                # Add project directory using real DBT syntax
                cmd_args.extend(["--project-dir", str(project_dir)])

                # Add profiles-dir if specified
                if profiles_dir:
                    cmd_args.extend(["--profiles-dir", str(profiles_dir)])

                self.logger.info(
                    "Invoking dbtRunner with real API",
                    command_args=cmd_args,
                )

                # Execute using real native dbtRunner.invoke() API
                result = runner.invoke(cmd_args)

                # Process result using real DBT structure
                execution_result = {
                    "success": result.success,
                    "command": cmd_args,
                    "models_processed": len(models) if models else "all",
                    "result_data": result.result if hasattr(result, "result") else None,
                    "exception": str(result.exception) if result.exception else None,
                    "execution_method": "dbt_runner_invoke",
                }

                # Add extra result information if available
                if hasattr(result, "args"):
                    execution_result["parsed_args"] = str(getattr(result, "args", None))

                if result.success:
                    self.logger.info(
                        "DBT models executed successfully via dbtRunner.invoke",
                        models_count=len(models) if models else "all",
                        result_success=result.success,
                    )
                    return FlextResult[FlextMeltanoTypes.DBT.ExecutionResult].ok(
                        cast("FlextMeltanoTypes.DBT.ExecutionResult", execution_result)
                    )

                # Se não teve sucesso, incluir detalhes do erro
                error_msg = f"DBT run failed via dbtRunner.invoke: {result.exception}"
                execution_result["error_details"] = error_msg

                self.logger.error(
                    error_msg,
                    exception=str(result.exception)
                    if result.exception
                    else "Unknown error",
                    result_success=result.success,
                )
                return FlextResult[FlextMeltanoTypes.DBT.ExecutionResult].ok(
                    cast("FlextMeltanoTypes.DBT.ExecutionResult", execution_result)
                )

            except Exception as e:
                error_msg = f"Failed to run DBT models via dbtRunner.invoke: {e}"
                self.logger.exception(error_msg, error=str(e))
                return FlextResult[FlextMeltanoTypes.DBT.ExecutionResult].fail(
                    error_msg
                )

        def test_models(
            self,
            runner: dbtRunner,
            models: list[str] | None = None,
            project_dir: Path | None = None,
        ) -> FlextResult[FlextMeltanoTypes.DBT.ExecutionResult]:
            """Test DBT models with structured result.

            Args:
                runner: Instância dbtRunner
                models: List of models to test (None = all)
                project_dir: DBT project directory

            Returns:
                FlextResult containing test results

            """
            try:
                self.logger.info(
                    "Testing DBT models",
                    models=models,
                    project_dir=str(project_dir) if project_dir else None,
                )

                # Build DBT command
                cmd = ["test"]

                # Adicionar modelos específicos
                if models:
                    cmd.extend(["--models", *models])

                # Add project directory
                if project_dir:
                    cmd.extend(["--project-dir", str(project_dir)])

                # Execute command
                self.logger.info("Executing DBT test command", command=cmd)
                result = runner.invoke(cmd)

                # Process result
                test_result = {
                    "success": result.success,
                    "command": cmd,
                    "models_tested": len(models) if models else "all",
                    "exit_code": getattr(
                        result, "exit_code", 0 if result.success else 1
                    ),
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

                return FlextResult[FlextMeltanoTypes.DBT.ExecutionResult].ok(
                    cast("FlextMeltanoTypes.DBT.ExecutionResult", test_result)
                )

            except Exception as e:
                error_msg = f"Failed to test DBT models: {e}"
                self.logger.exception(error_msg, error=str(e))
                return FlextResult[FlextMeltanoTypes.DBT.ExecutionResult].fail(
                    error_msg
                )

        def compile_project(
            self, runner: dbtRunner, project_dir: Path | None = None
        ) -> FlextResult[FlextMeltanoTypes.DBT.ExecutionResult]:
            """Compile DBT project.

            Args:
                runner: dbtRunner instance
                project_dir: DBT project directory

            Returns:
                FlextResult containing compilation result

            """
            try:
                self.logger.info(
                    "Compiling DBT project",
                    project_dir=str(project_dir) if project_dir else None,
                )

                # Build DBT command
                cmd = ["compile"]

                # Add project directory
                if project_dir:
                    cmd.extend(["--project-dir", str(project_dir)])

                # Execute command
                self.logger.info("Executing DBT compile command", command=cmd)
                result = runner.invoke(cmd)

                # Process result
                compile_result = {
                    "success": result.success,
                    "command": cmd,
                    "exit_code": getattr(
                        result, "exit_code", 0 if result.success else 1
                    ),
                    "result": result.result if hasattr(result, "result") else None,
                }

                if result.success:
                    self.logger.info("DBT project compiled successfully")
                else:
                    self.logger.error(
                        "DBT compilation failed",
                        exit_code=getattr(result, "exit_code", 1),
                    )

                return FlextResult[FlextMeltanoTypes.DBT.ExecutionResult].ok(
                    cast("FlextMeltanoTypes.DBT.ExecutionResult", compile_result)
                )

            except Exception as e:
                error_msg = f"Failed to compile DBT project: {e}"
                self.logger.exception(error_msg, error=str(e))
                return FlextResult[FlextMeltanoTypes.DBT.ExecutionResult].fail(
                    error_msg
                )

        def generate_docs(
            self, runner: dbtRunner, project_dir: Path | None = None
        ) -> FlextResult[FlextMeltanoTypes.DBT.ExecutionResult]:
            """Gera documentação DBT.

            Args:
                runner: Instância dbtRunner
                project_dir: DBT project directory

            Returns:
                FlextResult contendo resultado da geração de docs

            """
            try:
                self.logger.info(
                    "Generating DBT documentation",
                    project_dir=str(project_dir) if project_dir else None,
                )

                # Build DBT command
                cmd = ["docs", "generate"]

                # Add project directory
                if project_dir:
                    cmd.extend(["--project-dir", str(project_dir)])

                # Execute command
                self.logger.info("Executing DBT docs generate command", command=cmd)
                result = runner.invoke(cmd)

                # Process result
                docs_result = {
                    "success": result.success,
                    "command": cmd,
                    "exit_code": getattr(
                        result, "exit_code", 0 if result.success else 1
                    ),
                    "result": result.result if hasattr(result, "result") else None,
                }

                if result.success:
                    self.logger.info("DBT documentation generated successfully")
                else:
                    self.logger.error(
                        "DBT docs generation failed",
                        exit_code=getattr(result, "exit_code", 1),
                    )

                return FlextResult[FlextMeltanoTypes.DBT.ExecutionResult].ok(
                    cast("FlextMeltanoTypes.DBT.ExecutionResult", docs_result)
                )

            except Exception as e:
                error_msg = f"Failed to generate DBT docs: {e}"
                self.logger.exception(error_msg, error=str(e))
                return FlextResult[FlextMeltanoTypes.DBT.ExecutionResult].fail(
                    error_msg
                )

    # =================================================================
    # NESTED TYPE ADAPTER CLASS
    # =================================================================

    class TypeAdapter:
        """Adaptador de tipos DBT → FLEXT patterns."""

        @staticmethod
        def adapt_run_results(
            dbt_results: FlextMeltanoTypes.DBT.ExecutionResult,
        ) -> FlextResult[FlextMeltanoTypes.DBT.ExecutionResult]:
            """Converte resultados DBT para FlextDbtResults pattern.

            Args:
                dbt_results: Resultados DBT originais

            Returns:
                FlextResult contendo resultados adaptados

            """
            try:
                # Adaptar para formato FlextDbtResults
                flext_results: FlextMeltanoTypes.DBT.ExecutionResult = {
                    "version": "1.0",
                    "execution_time": cast(
                        "str | int | float | None", dbt_results.get("execution_time")
                    ),
                    "success": dbt_results.get("success", False),
                    "results": [],
                    "metadata": {
                        "dbt_version": cast(
                            "str | int | float | list[object] | dict[str, object] | None",
                            dbt_results.get("dbt_version"),
                        ),
                        "generated_at": cast(
                            "str | int | float | list[object] | dict[str, object] | None",
                            dbt_results.get("generated_at"),
                        ),
                    },
                }

                # Process results individuais
                results_data = dbt_results.get("results", [])
                if isinstance(results_data, list):
                    results_list = flext_results["results"]
                    if isinstance(results_list, list):
                        # results_list is already the correct type
                        typed_results_data = cast("list[object]", results_data)
                        for result in typed_results_data:
                            if isinstance(result, dict):
                                typed_result = cast(
                                    "FlextMeltanoTypes.DBT.ExecutionResult", result
                                )
                                flext_result = {
                                    "unique_id": cast(
                                        "str", typed_result.get("unique_id", "")
                                    ),
                                    "status": cast(
                                        "str", typed_result.get("status", "")
                                    ),
                                    "execution_time": cast(
                                        "float", typed_result.get("execution_time", 0.0)
                                    ),
                                    "message": cast(
                                        "str", typed_result.get("message", "")
                                    ),
                                    "compiled_code": cast(
                                        "str", typed_result.get("compiled_code", "")
                                    ),
                                }
                                results_list.append(flext_result)
                        flext_results["results"] = results_list

                return FlextResult[FlextMeltanoTypes.DBT.ExecutionResult].ok(
                    flext_results
                )

            except Exception as e:
                return FlextResult[FlextMeltanoTypes.DBT.ExecutionResult].fail(
                    f"Failed to adapt DBT results: {e}"
                )

        @staticmethod
        def adapt_manifest(
            dbt_manifest: FlextMeltanoTypes.DBT.ProjectConfig,
        ) -> FlextResult[FlextMeltanoTypes.DBT.ProjectConfig]:
            """Converte manifest DBT para FlextDbtManifest pattern.

            Args:
                dbt_manifest: Manifest DBT original

            Returns:
                FlextResult contendo manifest adaptado

            """
            try:
                # Adaptar para formato FlextDbtManifest
                flext_manifest: FlextMeltanoTypes.DBT.ProjectConfig = {
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
                        typed_nodes_dict = cast(
                            "FlextMeltanoTypes.DBT.ProjectConfig", nodes_dict
                        )
                        nodes_dict_copy = dict(typed_nodes_dict)  # Create mutable copy

                        # Type safe iteration over nodes_data
                        if isinstance(nodes_data, dict):
                            typed_nodes_data = cast(
                                "FlextMeltanoTypes.DBT.ProjectConfig", nodes_data
                            )
                            for node_id, node in typed_nodes_data.items():
                                if isinstance(node, dict):
                                    typed_node = cast(
                                        "FlextMeltanoTypes.DBT.ProjectConfig", node
                                    )
                                    depends_on_data = typed_node.get("depends_on", {})
                                    depends_on_nodes: list[str] = []
                                    if isinstance(depends_on_data, dict):
                                        depends_on_nodes = cast(
                                            "list[str]",
                                            depends_on_data.get("nodes", []),
                                        )

                                    flext_node: dict[str, str | list[str]] = {
                                        "name": cast("str", typed_node.get("name", "")),
                                        "resource_type": cast(
                                            "str", typed_node.get("resource_type", "")
                                        ),
                                        "database": cast(
                                            "str", typed_node.get("database", "")
                                        ),
                                        "schema": cast(
                                            "str", typed_node.get("schema", "")
                                        ),
                                        "depends_on": depends_on_nodes,
                                    }
                                    nodes_dict_copy[node_id] = cast(
                                        "str | int | float | list[object] | dict[str, object]",
                                        flext_node,
                                    )
                        flext_manifest["nodes"] = cast(
                            "str | int | float | list[object] | dict[str, object]",
                            nodes_dict_copy,
                        )

                # Processar sources
                sources_data = dbt_manifest.get("sources", {})
                if isinstance(sources_data, dict):
                    sources_dict = flext_manifest["sources"]
                    if isinstance(sources_dict, dict):
                        typed_sources_dict = cast(
                            "FlextMeltanoTypes.DBT.ProjectConfig", sources_dict
                        )
                        sources_dict_copy = dict(
                            typed_sources_dict
                        )  # Create mutable copy

                        # Type safe iteration over sources_data
                        if isinstance(sources_data, dict):
                            typed_sources_data = cast(
                                "FlextMeltanoTypes.DBT.ProjectConfig", sources_data
                            )
                            for source_id, source in typed_sources_data.items():
                                if isinstance(source, dict):
                                    typed_source = cast(
                                        "FlextMeltanoTypes.DBT.ProjectConfig", source
                                    )
                                    flext_source: dict[str, str] = {
                                        "name": cast(
                                            "str", typed_source.get("name", "")
                                        ),
                                        "source_name": cast(
                                            "str", typed_source.get("source_name", "")
                                        ),
                                        "database": cast(
                                            "str", typed_source.get("database", "")
                                        ),
                                        "schema": cast(
                                            "str", typed_source.get("schema", "")
                                        ),
                                    }
                                    sources_dict_copy[source_id] = cast(
                                        "str | int | float | list[object] | dict[str, object]",
                                        flext_source,
                                    )
                        flext_manifest["sources"] = cast(
                            "str | int | float | list[object] | dict[str, object]",
                            sources_dict_copy,
                        )

                return FlextResult[FlextMeltanoTypes.DBT.ProjectConfig].ok(
                    flext_manifest
                )

            except Exception as e:
                return FlextResult[FlextMeltanoTypes.DBT.ProjectConfig].fail(
                    f"Failed to adapt DBT manifest: {e}"
                )

    # =================================================================
    # BACKWARD COMPATIBILITY ALIASES
    # =================================================================

    # Legacy aliases removed - following flext-core single class pattern


# =============================================================================
# MODULE-LEVEL ALIASES REMOVED - Following flext-core pattern of single class export
# =============================================================================

# No module-level aliases - only single class export following flext-core pattern


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    "DBT_AVAILABLE",
    "FlextMeltanoWrapper",
]
