"""Base Services - Componentes base para projetos flext-(dbt|tap|target).

FUNÇÃO 3: Base components para projetos flext-*
- FlextMeltanoTapService: Base para flext-tap-* projects
- FlextMeltanoTargetService: Base para flext-target-* projects
- FlextMeltanoDbtService: Base para flext-dbt-* projects
- Real flext-core integration (NO MOCKS)
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any

from flext_core import (
    FlextDomainService,
    FlextResult,
    get_logger,
)
from singer_sdk import Tap, Target

from .dbt_wrapper import FlextDbtAdapter, MeltanoDbtWrapper

# Import dos wrappers para composição
from .singer_wrapper import MeltanoSingerWrapper, FlextSingerAdapter

if TYPE_CHECKING:
    from collections.abc import Iterator

logger = get_logger(__name__)

# =============================================================================
# BASE SERVICES - FUNÇÃO 3
# =============================================================================


class FlextMeltanoTapService(FlextDomainService, ABC):
    """Serviço base para projetos flext-tap-*.

    Fornece funcionalidades comuns para todos os taps FLEXT,
    integrando Singer SDK com padrões flext-core.
    """

    def __init__(self, tap_name: str) -> None:
        super().__init__()
        self.tap_name = tap_name

        # Composição de wrappers
        self.singer_wrapper = MeltanoSingerWrapper()
        self.singer_adapter = FlextSingerAdapter()

    @property
    def logger(self) -> object:
        """Get logger instance."""
        return get_logger(self.__class__.__name__)

    @abstractmethod
    def get_tap_class(self) -> type[Tap]:
        """Retorna a classe Singer Tap específica.

        Returns:
            Classe Singer Tap para este tap

        """

    @abstractmethod
    def get_default_config(self) -> dict[str, Any]:
        """Retorna configuração padrão do tap.

        Returns:
            Configuração padrão

        """

    def create_tap_instance(self, config: dict[str, Any]) -> FlextResult[Tap]:
        """Cria instância do tap com configuração.

        Args:
            config: Configuração do tap

        Returns:
            FlextResult contendo instância do tap

        """
        try:
            self.logger.info("Creating tap instance", tap_name=self.tap_name)

            # Validar configuração
            validation_result = self.validate_tap_config(config)
            if not validation_result.is_success:
                return FlextResult.fail(f"Invalid config: {validation_result.error}")

            # Criar tap usando wrapper
            tap_class = self.get_tap_class()
            return self.singer_wrapper.create_tap(tap_class, config)

        except Exception as e:
            error_msg = f"Failed to create tap {self.tap_name}: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def discover_streams(self, tap: Tap) -> FlextResult[list[dict[str, Any]]]:
        """Descobre streams disponíveis no tap.

        Args:
            tap: Instância do tap

        Returns:
            FlextResult contendo lista de streams

        """
        try:
            self.logger.info("Discovering streams", tap_name=self.tap_name)

            # Usar wrapper para descoberta
            catalog_result = self.singer_wrapper.discover_catalog(tap)
            if not catalog_result.is_success:
                return FlextResult.fail(f"Failed to discover: {catalog_result.error}")

            # Adaptar catálogo para formato FLEXT
            catalog = catalog_result.value
            adapter_result = self.singer_adapter.adapt_catalog(catalog)
            if not adapter_result.is_success:
                return FlextResult.fail(
                    f"Failed to adapt catalog: {adapter_result.error}"
                )

            streams = adapter_result.value.get("streams", [])
            self.logger.info("Streams discovered", count=len(streams))

            return FlextResult.ok(streams)

        except Exception as e:
            error_msg = f"Failed to discover streams: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def validate_tap_config(self, config: dict[str, Any]) -> FlextResult[bool]:
        """Valida configuração do tap.

        Args:
            config: Configuração a validar

        Returns:
            FlextResult indicando se config é válida

        """
        try:
            # Validação base - subclasses podem override
            if not config:
                return FlextResult.fail("Configuration cannot be empty")

            # Verificar campos obrigatórios base
            required_fields = self.get_required_config_fields()
            for field in required_fields:
                if field not in config:
                    return FlextResult.fail(f"Missing required field: {field}")

            return FlextResult.ok(True)

        except Exception as e:
            return FlextResult.fail(f"Config validation error: {e}")

    def get_required_config_fields(self) -> list[str]:
        """Retorna campos obrigatórios da configuração.

        Returns:
            Lista de campos obrigatórios

        """
        # Base fields - subclasses podem extend
        return []


class FlextMeltanoTargetService(FlextDomainService, ABC):
    """Serviço base para projetos flext-target-*.

    Fornece funcionalidades comuns para todos os targets FLEXT,
    integrando Singer SDK com padrões flext-core.
    """

    def __init__(self, target_name: str) -> None:
        super().__init__()
        self.target_name = target_name

        # Composição de wrappers
        self.singer_wrapper = MeltanoSingerWrapper()
        self.singer_adapter = FlextSingerAdapter()

    @property
    def logger(self) -> object:
        """Get logger instance."""
        return get_logger(self.__class__.__name__)

    @abstractmethod
    def get_target_class(self) -> type[Target]:
        """Retorna a classe Singer Target específica.

        Returns:
            Classe Singer Target para este target

        """

    @abstractmethod
    def get_default_config(self) -> dict[str, Any]:
        """Retorna configuração padrão do target.

        Returns:
            Configuração padrão

        """

    def create_target_instance(self, config: dict[str, Any]) -> FlextResult[Target]:
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
            if not validation_result.is_success:
                return FlextResult.fail(f"Invalid config: {validation_result.error}")

            # Criar target usando wrapper
            target_class = self.get_target_class()
            return self.singer_wrapper.create_target(target_class, config)

        except Exception as e:
            error_msg = f"Failed to create target {self.target_name}: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def process_records(
        self, target: Target, records: Iterator[dict[str, Any]], stream_name: str
    ) -> FlextResult[dict[str, Any]]:
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

                # Processar através do target
                target.process_messages([singer_message])
                records_processed += 1

            # Flush target
            target.drain()

            result = {
                "records_processed": records_processed,
                "stream": stream_name,
                "target": self.target_name,
            }

            self.logger.info("Records processed successfully", count=records_processed)
            return FlextResult.ok(result)

        except Exception as e:
            error_msg = f"Failed to process records: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def validate_target_config(self, config: dict[str, Any]) -> FlextResult[bool]:
        """Valida configuração do target.

        Args:
            config: Configuração a validar

        Returns:
            FlextResult indicando se config é válida

        """
        try:
            # Validação base - subclasses podem override
            if not config:
                return FlextResult.fail("Configuration cannot be empty")

            # Verificar campos obrigatórios base
            required_fields = self.get_required_config_fields()
            for field in required_fields:
                if field not in config:
                    return FlextResult.fail(f"Missing required field: {field}")

            return FlextResult.ok(True)

        except Exception as e:
            return FlextResult.fail(f"Config validation error: {e}")

    def get_required_config_fields(self) -> list[str]:
        """Retorna campos obrigatórios da configuração.

        Returns:
            Lista de campos obrigatórios

        """
        # Base fields - subclasses podem extend
        return []


class FlextMeltanoDbtService(FlextDomainService, ABC):
    """Serviço base para projetos flext-dbt-*.

    Fornece funcionalidades comuns para todos os projetos DBT FLEXT,
    integrando DBT Core com padrões flext-core.
    """

    def __init__(self, project_name: str) -> None:
        super().__init__()
        self.project_name = project_name
        self.logger = get_logger(self.__class__.__name__)

        # Composição de wrappers
        self.dbt_wrapper = MeltanoDbtWrapper()
        self.dbt_adapter = FlextDbtAdapter()

    @abstractmethod
    def get_project_config(self) -> dict[str, Any]:
        """Retorna configuração do projeto DBT.

        Returns:
            Configuração do projeto DBT

        """

    @abstractmethod
    def get_models_directory(self) -> Path:
        """Retorna diretório dos models.

        Returns:
            Path para diretório models/

        """

    def initialize_project(self, project_root: Path) -> FlextResult[object]:
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
                return FlextResult.fail(f"No dbt_project.yml found in {project_root}")

            # Criar runner DBT
            return self.dbt_wrapper.create_runner(project_root)

        except Exception as e:
            error_msg = f"Failed to initialize DBT project: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def run_models(
        self,
        runner: object,
        models: list[str] | None = None,
        project_dir: Path | None = None,
    ) -> FlextResult[dict[str, Any]]:
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

            # Usar wrapper DBT
            result = self.dbt_wrapper.run_models(runner, models, project_dir)

            if result.is_success:
                # Adaptar resultado para formato FLEXT
                adapted_result = self.dbt_adapter.adapt_run_results(result.value)
                if adapted_result.is_success:
                    return adapted_result
                # Se adaptação falhar, retornar resultado original
                return result
            return result

        except Exception as e:
            error_msg = f"Failed to run DBT models: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def test_models(
        self,
        runner: object,
        models: list[str] | None = None,
        project_dir: Path | None = None,
    ) -> FlextResult[dict[str, Any]]:
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
            return self.dbt_wrapper.test_models(runner, models, project_dir)

        except Exception as e:
            error_msg = f"Failed to test DBT models: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def get_model_lineage(self, project_dir: Path) -> FlextResult[dict[str, Any]]:
        """Obtém lineage dos models.

        Args:
            project_dir: Diretório do projeto

        Returns:
            FlextResult contendo lineage information

        """
        try:
            self.logger.info("Getting model lineage", project_name=self.project_name)

            # Compilar projeto para gerar manifest
            runner_result = self.dbt_wrapper.create_runner(project_dir)
            if not runner_result.is_success:
                return FlextResult.fail(
                    f"Failed to create runner: {runner_result.error}"
                )

            runner = runner_result.value
            compile_result = self.dbt_wrapper.compile_project(runner, project_dir)
            if not compile_result.is_success:
                return FlextResult.fail(f"Failed to compile: {compile_result.error}")

            # Tentar ler manifest.json
            manifest_path = project_dir / "target" / "manifest.json"
            if manifest_path.exists():
                with manifest_path.open() as f:
                    manifest_data = json.load(f)

                # Adaptar manifest para formato FLEXT
                adapted_manifest = self.dbt_adapter.adapt_manifest(manifest_data)
                if adapted_manifest.is_success:
                    return adapted_manifest
                return FlextResult.ok(manifest_data)  # Fallback para dados originais
            return FlextResult.fail("Manifest.json not found after compilation")

        except Exception as e:
            error_msg = f"Failed to get model lineage: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    "FlextMeltanoDbtService",
    "FlextMeltanoTapService",
    "FlextMeltanoTargetService",
]
