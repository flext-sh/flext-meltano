"""Base Services - Componentes base para projetos flext-(dbt|tap|target).

FUNÇÃO 3: Base components para projetos flext-*
- FlextMeltanoTapService: Base para flext-tap-* projects
- FlextMeltanoTargetService: Base para flext-target-* projects
- FlextMeltanoDbtService: Base para flext-dbt-* projects
- Real flext-core integration using proper protocols and service patterns
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from dbt.cli.main import dbtRunner
from flext_core import (
    FlextLogger,
    FlextResult,
    FlextServiceProcessor,
    get_logger,
)
from singer_sdk import Tap, Target

from flext_meltano.base_dbt import FlextDbtAdapter, MeltanoDbtWrapper
from flext_meltano.base_singer import FlextSingerAdapter, MeltanoSingerWrapper

logger = get_logger(__name__)

# =============================================================================
# BASE SERVICES - FUNÇÃO 3
# =============================================================================


class FlextMeltanoTapService(
    FlextServiceProcessor[dict[str, Any], Tap, dict[str, Any]], ABC
):
    """Serviço base para projetos flext-tap-*.

    Fornece funcionalidades comuns para todos os taps FLEXT,
    integrando Singer SDK com padrões flext-core usando FlextServiceProcessor.
    """

    def __init__(self, tap_name: str) -> None:
        """Initialize tap service with name."""
        super().__init__()
        self.tap_name = tap_name
        self.wrapper_singer = MeltanoSingerWrapper()
        self.singer_adapter = FlextSingerAdapter()
        self._logger = get_logger(self.__class__.__name__)

    @property
    def logger(self) -> FlextLogger:
        """Get logger instance."""
        return self._logger

    def process(self, request: dict[str, Any]) -> FlextResult[Tap]:
        """Process tap configuration and create Singer Tap instance."""
        try:
            self.logger.info("Processing tap configuration", tap_name=self.tap_name)

            # Validate configuration
            config_result = self.validate_tap_config(request)
            if config_result.is_failure:
                return FlextResult[Tap].fail(
                    config_result.error or "Invalid configuration"
                )

            # Create tap instance
            tap_class = self.get_tap_class()
            tap_instance = tap_class(config=request)

            return FlextResult[Tap].ok(tap_instance)

        except Exception as e:
            error_msg = f"Failed to process tap configuration: {e}"
            self.logger.error(error_msg, tap_name=self.tap_name, error=str(e))
            return FlextResult[Tap].fail(error_msg)

    def build(self, domain: Tap, *, correlation_id: str) -> dict[str, Any]:
        """Build final result from tap instance."""
        return {
            "service": "FlextMeltanoTapService",
            "tap_name": self.tap_name,
            "tap_class": domain.__class__.__name__,
            "status": "ready",
            "correlation_id": correlation_id,
        }

    @abstractmethod
    def get_tap_class(self) -> type[Tap]:
        """Retorna a classe Singer Tap específica.

        Returns:
            Classe Singer Tap para este tap

        """

    @abstractmethod
    def get_default_config(self) -> dict[str, object]:
        """Retorna configuração padrão do tap.

        Returns:
            Configuração padrão

        """

    def create_tap_instance(self, config: dict[str, object]) -> FlextResult[Tap]:
        """Cria instância do tap com configuração.

        Args:
            config: Configuração do tap

        Returns:
            FlextResult contendo instância do tap

        """
        try:
            self.logger.info("Creating tap instance", tap_name=self.tap_name)

            # Validar configuração usando unwrap_or pattern
            config_valid = self.validate_tap_config(config).unwrap_or(default=False)
            if not config_valid:
                validation_result = self.validate_tap_config(config)
                return FlextResult[Tap].fail(
                    f"Invalid config: {validation_result.error}"
                )

            # Criar tap usando wrapper
            tap_class = self.get_tap_class()
            return self.wrapper_singer.create_tap(tap_class, config)

        except Exception as e:
            error_msg = f"Failed to create tap {self.tap_name}: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult[Tap].fail(error_msg)

    def discover_streams(self, tap: Tap) -> FlextResult[list[dict[str, object]]]:
        """Descobre streams disponíveis no tap.

        Args:
            tap: Instância do tap

        Returns:
            FlextResult contendo lista de streams

        """
        try:
            self.logger.info("Discovering streams", tap_name=self.tap_name)

            # Usar wrapper para descoberta
            catalog_result = self.wrapper_singer.discover_catalog(tap)
            if not catalog_result.success:
                return FlextResult[list[dict[str, object]]].fail(
                    f"Failed to discover: {catalog_result.error}"
                )

            # Adaptar catálogo para formato FLEXT
            catalog = catalog_result.value
            adapter_result = self.singer_adapter.adapt_catalog(catalog)
            if not adapter_result.success:
                return FlextResult[list[dict[str, object]]].fail(
                    f"Failed to adapt catalog: {adapter_result.error}"
                )

            adapted_catalog = adapter_result.value
            streams: list[dict[str, object]] = []
            if isinstance(adapted_catalog, dict):
                streams_data = adapted_catalog.get("streams", [])
                if isinstance(streams_data, list):
                    streams = streams_data

            self.logger.info("Streams discovered", count=len(streams))
            return FlextResult[list[dict[str, object]]].ok(streams)

        except Exception as e:
            error_msg = f"Failed to discover streams: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult[list[dict[str, object]]].fail(error_msg)

    def validate_tap_config(self, config: dict[str, object]) -> FlextResult[bool]:
        """Valida configuração do tap.

        Args:
            config: Configuração a validar

        Returns:
            FlextResult indicando se config é válida

        """
        try:
            # Validação base - subclasses podem override
            if not config:
                return FlextResult[bool].fail("Configuration cannot be empty")

            # Verificar campos obrigatórios base
            required_fields = self.get_required_config_fields()
            for field in required_fields:
                if field not in config:
                    return FlextResult[bool].fail(f"Missing required field: {field}")

            return FlextResult[bool].ok(data=True)

        except Exception as e:
            return FlextResult[bool].fail(f"Config validation error: {e}")

    def get_required_config_fields(self) -> list[str]:
        """Retorna campos obrigatórios da configuração.

        Returns:
            Lista de campos obrigatórios

        """
        # Base fields - subclasses podem extend
        return []


class FlextMeltanoTargetService(FlextDomainService[dict[str, object]], ABC):
    """Serviço base para projetos flext-target-*.

    Fornece funcionalidades comuns para todos os targets FLEXT,
    integrando Singer SDK com padrões flext-core.
    """

    # Pydantic fields for frozen model
    target_name: str
    wrapper_singer: MeltanoSingerWrapper = MeltanoSingerWrapper()
    singer_adapter: FlextSingerAdapter = FlextSingerAdapter()

    @property
    def logger(self) -> FlextLogger:
        """Get logger instance."""
        return get_logger(self.__class__.__name__)

    def execute(self) -> FlextResult[dict[str, object]]:
        """Execute target service operation (required by FlextDomainService)."""
        try:
            return FlextResult[dict[str, object]].ok({
                "service": "FlextMeltanoTargetService",
                "target_name": getattr(self, "target_name", "unknown"),
                "status": "ready",
            })
        except Exception as e:
            return FlextResult[dict[str, object]].fail(f"Execution failed: {e}")

    @abstractmethod
    def get_target_class(self) -> type[Target]:
        """Retorna a classe Singer Target específica.

        Returns:
            Classe Singer Target para este target

        """

    @abstractmethod
    def get_default_config(self) -> dict[str, object]:
        """Retorna configuração padrão do target.

        Returns:
            Configuração padrão

        """

    def create_target_instance(self, config: dict[str, object]) -> FlextResult[Target]:
        """Cria instância do target com configuração.

        Args:
            config: Configuração do target

        Returns:
            FlextResult contendo instância do target

        """
        try:
            self.logger.info("Creating target instance", target_name=self.target_name)

            # Validar configuração
            validation_result = self.validate_target_config(config)
            if not validation_result.success:
                return FlextResult[Target].fail(
                    f"Invalid config: {validation_result.error}"
                )

            # Criar target usando wrapper
            target_class = self.get_target_class()
            return self.wrapper_singer.create_target(target_class, config)

        except Exception as e:
            error_msg = f"Failed to create target {self.target_name}: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult[Target].fail(error_msg)

    def process_records(
        self, target: Target, records: Iterator[dict[str, object]], stream_name: str
    ) -> FlextResult[dict[str, object]]:
        """Processa records através do target.

        Args:
            target: Instância do target
            records: Iterator de records
            stream_name: Nome do stream

        Returns:
            FlextResult contendo resultado do processamento

        """
        try:
            self.logger.info(
                "Processing records", target_name=self.target_name, stream=stream_name
            )

            records_processed = 0

            # Converter records para formato Singer
            for record in records:
                # Criar mensagem Singer
                singer_message = {
                    "type": "RECORD",
                    "stream": stream_name,
                    "record": record,
                    "time_extracted": record.get("_sdc_extracted_at"),
                }

                # Usar Target SDK diretamente (esta é uma implementação base simples)
                # Em implementações reais, subclasses podem usar métodos específicos
                try:
                    # Note: Esta é uma implementação base - subclasses devem sobrescrever
                    # com implementações específicas usando o wrapper adequadamente
                    # Process message through target
                    if hasattr(target, "process_record_message"):
                        target.process_record_message(singer_message)
                    records_processed += 1
                except Exception as e:
                    self.logger.warning("Failed to process record", error=str(e))

            # Processamento finalizado - em implementações reais,
            # subclasses podem precisar de lógica específica de finalization

            result = {
                "records_processed": records_processed,
                "stream": stream_name,
                "target": self.target_name,
            }

            self.logger.info("Records processed successfully", count=records_processed)
            return FlextResult[dict[str, object]].ok(result)

        except Exception as e:
            error_msg = f"Failed to process records: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult[dict[str, object]].fail(error_msg)

    def validate_target_config(self, config: dict[str, object]) -> FlextResult[bool]:
        """Valida configuração do target.

        Args:
            config: Configuração a validar

        Returns:
            FlextResult indicando se config é válida

        """
        try:
            # Validação base - subclasses podem override
            if not config:
                return FlextResult[bool].fail("Configuration cannot be empty")

            # Verificar campos obrigatórios base
            required_fields = self.get_required_config_fields()
            for field in required_fields:
                if field not in config:
                    return FlextResult[bool].fail(f"Missing required field: {field}")

            return FlextResult[bool].ok(data=True)

        except Exception as e:
            return FlextResult[bool].fail(f"Config validation error: {e}")

    def get_required_config_fields(self) -> list[str]:
        """Retorna campos obrigatórios da configuração.

        Returns:
            Lista de campos obrigatórios

        """
        # Base fields - subclasses podem extend
        return []


class FlextMeltanoDbtService(FlextDomainService[dict[str, object]]):
    """Serviço base para projetos flext-dbt-*.

    Fornece funcionalidades comuns para todos os projetos DBT FLEXT,
    integrando DBT Core com padrões flext-core.
    """

    # Pydantic fields for frozen model
    project_name: str
    wrapper_dbt: MeltanoDbtWrapper = MeltanoDbtWrapper()
    dbt_adapter: FlextDbtAdapter = FlextDbtAdapter()

    @property
    def logger(self) -> FlextLogger:
        """Get logger instance."""
        return get_logger(self.__class__.__name__)

    def execute(self) -> FlextResult[dict[str, object]]:
        """Execute DBT service operation (required by FlextDomainService)."""
        try:
            return FlextResult[dict[str, object]].ok({
                "service": "FlextMeltanoDbtService",
                "project_name": self.project_name,
                "status": "ready",
            })
        except Exception as e:
            return FlextResult[dict[str, object]].fail(f"Execution failed: {e}")

    def get_project_config(self) -> dict[str, object]:
        """Retorna configuração do projeto DBT.

        Returns:
            Configuração do projeto DBT

        """
        return {
            "name": self.project_name,
            "version": "1.0.0",
            "profile": self.project_name,
            "model-paths": ["models"],
            "analysis-paths": ["analysis"],
            "test-paths": ["tests"],
            "seed-paths": ["data"],
            "macro-paths": ["macros"],
            "snapshot-paths": ["snapshots"],
            "target-path": "target",
            "clean-targets": ["target", "dbt_packages"],
            "models": {self.project_name: {"materialized": "table"}},
        }

    def get_models_directory(self) -> Path:
        """Retorna diretório dos models.

        Returns:
            Path para diretório models/

        """
        return Path("models")

    def initialize_project(self, project_root: Path) -> FlextResult[dbtRunner]:
        """Inicializa projeto DBT.

        Args:
            project_root: Diretório raiz do projeto

        Returns:
            FlextResult contendo runner DBT

        """
        try:
            self.logger.info(
                "Initializing DBT project",
                project_name=self.project_name,
                project_root=str(project_root),
            )

            # Validar estrutura do projeto
            if not (project_root / "dbt_project.yml").exists():
                return FlextResult[dbtRunner].fail(
                    f"No dbt_project.yml found in {project_root}"
                )

            # Criar runner DBT
            return self.wrapper_dbt.create_runner(project_root)

        except Exception as e:
            error_msg = f"Failed to initialize DBT project: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult[dbtRunner].fail(error_msg)

    def run_models(
        self,
        runner: dbtRunner,  # noqa: ARG002
        models: list[str] | None = None,
        project_dir: Path | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Executa models DBT.

        Args:
            runner: Instância dbtRunner
            models: Lista de models (None = todos)
            project_dir: Diretório do projeto

        Returns:
            FlextResult contendo resultado da execução

        """
        try:
            self.logger.info(
                "Running DBT models", project_name=self.project_name, models=models
            )

            # Validar project_dir e usar wrapper DBT
            if project_dir is None:
                return FlextResult.fail("Project directory is required")

            result = self.wrapper_dbt.run_models_real(project_dir, models)

            if result.success:
                # Adaptar resultado para formato FLEXT
                adapted_result = self.dbt_adapter.adapt_run_results(result.value)
                if adapted_result.success:
                    return adapted_result
                # Se adaptação falhar, retornar resultado original
                return result
            return result

        except Exception as e:
            error_msg = f"Failed to run DBT models: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult[dict[str, object]].fail(error_msg)

    def test_models(
        self,
        runner: dbtRunner,
        models: list[str] | None = None,
        project_dir: Path | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Executa testes DBT.

        Args:
            runner: Instância dbtRunner
            models: Lista de models para testar
            project_dir: Diretório do projeto

        Returns:
            FlextResult contendo resultado dos testes

        """
        try:
            self.logger.info(
                "Testing DBT models", project_name=self.project_name, models=models
            )

            # Usar wrapper DBT
            return self.wrapper_dbt.test_models(runner, models, project_dir)

        except Exception as e:
            error_msg = f"Failed to test DBT models: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult[dict[str, object]].fail(error_msg)

    def get_model_lineage(self, project_dir: Path) -> FlextResult[dict[str, object]]:
        """Obtém lineage dos models.

        Args:
            project_dir: Diretório do projeto

        Returns:
            FlextResult contendo lineage information

        """
        try:
            self.logger.info("Getting model lineage", project_name=self.project_name)

            # Compilar projeto para gerar manifest
            runner_result = self.wrapper_dbt.create_runner(project_dir)
            if not runner_result.success:
                return FlextResult[dict[str, object]].fail(
                    f"Failed to create runner: {runner_result.error}"
                )

            runner = runner_result.value
            compile_result = self.wrapper_dbt.compile_project(runner, project_dir)
            if not compile_result.success:
                return FlextResult[dict[str, object]].fail(
                    f"Failed to compile: {compile_result.error}"
                )

            # Tentar ler manifest.json
            manifest_path = project_dir / "target" / "manifest.json"
            if manifest_path.exists():
                with manifest_path.open() as f:
                    manifest_data = json.load(f)

                # Adaptar manifest para formato FLEXT
                adapted_manifest = self.dbt_adapter.adapt_manifest(manifest_data)
                if adapted_manifest.success:
                    return adapted_manifest
                return FlextResult[dict[str, object]].fail(
                    f"Failed to adapt manifest: {adapted_manifest.error}"
                )
            return FlextResult[dict[str, object]].fail(
                "Manifest.json not found after compilation"
            )

        except Exception as e:
            error_msg = f"Failed to get model lineage: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult[dict[str, object]].fail(error_msg)


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    "FlextMeltanoDbtService",
    "FlextMeltanoTapService",
    "FlextMeltanoTargetService",
]
