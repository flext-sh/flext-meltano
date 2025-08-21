"""Singer SDK Wrapper - Adapta Singer SDK para padrões flext-core.

FUNÇÃO 1: Wrapper para Singer SDK adaptando para flext-core
- MeltanoSingerWrapper: Wrapper principal
- FlextSingerAdapter: Adaptador de tipos
- Real Singer SDK integration (NO MOCKS)
"""

from __future__ import annotations

from collections.abc import Iterator

# Removendo Any types - usando types específicos
from flext_core import FlextDomainService, FlextLogger, FlextResult, get_logger
from singer_sdk import Stream, Tap, Target, typing as singer_typing
from singer_sdk.typing import PropertiesList, Property

logger = get_logger(__name__)

# =============================================================================
# SINGER SDK WRAPPER - REAL IMPLEMENTATION
# =============================================================================


class MeltanoSingerWrapper(FlextDomainService[None]):
    """Wrapper principal para Singer SDK → flext-core.

    Adapta Singer SDK patterns para flext-core patterns, usando FlextResult
    para error handling e integrando com flext-core observability.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def logger(self) -> FlextLogger:
        """Get logger instance."""
        return get_logger(self.__class__.__name__)

    def execute(self) -> FlextResult[None]:
        """Execute Singer service operation (required by FlextDomainService).

        Returns:
            FlextResult contendo informações do serviço

        """
        # Execute operation - Singer wrapper is operational
        self.logger.info("Singer wrapper executed successfully")
        return FlextResult.ok(None)

    def create_tap(
        self, tap_class: type[Tap], config: dict[str, object]
    ) -> FlextResult[Tap]:
        """Cria tap Singer usando FlextResult pattern.

        Args:
            tap_class: Classe Singer Tap (ex: TapCSV, TapOracle)
            config: Configuração do tap

        Returns:
            FlextResult contendo Tap instance ou erro

        """
        try:
            self.logger.info("Creating Singer tap", tap_class=tap_class.__name__)

            # Validar configuração obrigatória
            if not config:
                return FlextResult.fail("Tap configuration cannot be empty")

            # Criar instância do tap
            tap_instance = tap_class(config=config)

            # Validar se tap foi criado corretamente
            if not hasattr(tap_instance, "discover_streams"):
                return FlextResult.fail(f"Invalid tap class: {tap_class.__name__}")

            self.logger.info(
                "Singer tap created successfully", tap_class=tap_class.__name__
            )
            return FlextResult.ok(tap_instance)

        except Exception as e:
            error_msg = f"Failed to create tap {tap_class.__name__}: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def create_target(
        self, target_class: type[Target], config: dict[str, object]
    ) -> FlextResult[Target]:
        """Cria target Singer usando FlextResult pattern.

        Args:
            target_class: Classe Singer Target (ex: TargetCSV, TargetPostgres)
            config: Configuração do target

        Returns:
            FlextResult contendo Target instance ou erro

        """
        try:
            self.logger.info(
                "Creating Singer target", target_class=target_class.__name__
            )

            # Validar configuração obrigatória
            if not config:
                return FlextResult.fail("Target configuration cannot be empty")

            # Criar instância do target
            target_instance = target_class(config=config)

            # Validar se target foi criado corretamente
            if not hasattr(target_instance, "process_messages"):
                return FlextResult.fail(
                    f"Invalid target class: {target_class.__name__}"
                )

            self.logger.info(
                "Singer target created successfully", target_class=target_class.__name__
            )
            return FlextResult.ok(target_instance)

        except Exception as e:
            error_msg = f"Failed to create target {target_class.__name__}: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def run_elt_pipeline(
        self, tap: Tap, target: Target, catalog: dict[str, int] | None = None
    ) -> FlextResult[dict[str, int]]:
        """Executa pipeline ELT completo com observabilidade flext-core.

        Args:
            tap: Instância Singer Tap
            target: Instância Singer Target
            catalog: Catálogo opcional (auto-descoberto se None)

        Returns:
            FlextResult contendo resultado do pipeline

        """
        try:
            self.logger.info(
                "Starting ELT pipeline",
                tap=tap.__class__.__name__,
                target=target.__class__.__name__,
            )

            # Descobrir catálogo se não fornecido
            if catalog is None:
                catalog_result = self.discover_catalog(tap)
                if not catalog_result.is_success:
                    return FlextResult.fail(
                        f"Failed to discover catalog: {catalog_result.error}"
                    )
                catalog = catalog_result.value

            # Executar sync do tap
            records_processed = 0
            streams_processed = 0

            # Get streams from catalog
            streams = catalog.get("streams", [])

            for stream_def in streams:
                if not stream_def.get("selected", True):
                    continue

                stream_name = stream_def["stream"]
                self.logger.info("Processing stream", stream=stream_name)

                # Sync stream records
                try:
                    records = tap.get_records(stream=stream_name)

                    # Process records through target
                    for record in records:
                        # Convert to Singer message format
                        message = {
                            "type": "RECORD",
                            "stream": stream_name,
                            "record": record,
                        }

                        # Send to target
                        target.process_messages([message])
                        records_processed += 1

                    streams_processed += 1

                except Exception as stream_error:
                    self.logger.exception(
                        "Stream processing failed",
                        stream=stream_name,
                        error=str(stream_error),
                    )
                    continue

            # Flush target
            target.drain()

            result = {
                "success": True,
                "records_processed": records_processed,
                "streams_processed": streams_processed,
                "catalog": catalog,
            }

            self.logger.info(
                "ELT pipeline completed successfully",
                records=records_processed,
                streams=streams_processed,
            )
            return FlextResult.ok(result)

        except Exception as e:
            error_msg = f"ELT pipeline failed: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)

    def discover_catalog(self, tap: Tap) -> FlextResult[dict[str, object]]:
        """Descobre catálogo do tap e adapta para tipos flext-core.

        Args:
            tap: Instância Singer Tap

        Returns:
            FlextResult contendo catálogo descoberto

        """
        try:
            self.logger.info("Discovering catalog", tap=tap.__class__.__name__)

            # Executar descoberta do catálogo
            catalog = tap.catalog_dict

            if not catalog or "streams" not in catalog:
                return FlextResult.fail("Invalid catalog returned by tap")

            # Validar streams
            streams = catalog["streams"]
            if not isinstance(streams, list):
                return FlextResult.fail("Invalid streams format in catalog")

            self.logger.info(
                "Catalog discovered successfully", streams_count=len(streams)
            )
            return FlextResult.ok(catalog)

        except Exception as e:
            error_msg = f"Failed to discover catalog: {e}"
            self.logger.exception(error_msg, error=str(e))
            return FlextResult.fail(error_msg)


# =============================================================================
# SINGER TYPE ADAPTERS - FLEXT-CORE INTEGRATION
# =============================================================================


class FlextSingerAdapter:
    """Adaptador de tipos Singer → FLEXT patterns."""

    @staticmethod
    def adapt_catalog(
        singer_catalog: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Converte singer catalog para FlextCatalog pattern.

        Args:
            singer_catalog: Catálogo Singer original

        Returns:
            FlextResult contendo catálogo adaptado

        """
        try:
            # Validar estrutura
            if not isinstance(singer_catalog, dict) or "streams" not in singer_catalog:
                return FlextResult.fail("Invalid Singer catalog structure")

            # Adaptar para formato FlextCatalog
            flext_catalog = {
                "version": "1.0",
                "streams": [],
                "metadata": singer_catalog.get("metadata", {}),
            }

            # Processar streams
            for stream in singer_catalog["streams"]:
                flext_stream = {
                    "name": stream.get("stream"),
                    "schema": stream.get("schema", {}),
                    "key_properties": stream.get("key_properties", []),
                    "replication_method": stream.get(
                        "replication_method", "FULL_TABLE"
                    ),
                    "replication_key": stream.get("replication_key"),
                    "selected": stream.get("selected", True),
                }
                flext_catalog["streams"].append(flext_stream)

            return FlextResult.ok(flext_catalog)

        except Exception as e:
            return FlextResult.fail(f"Failed to adapt catalog: {e}")

    @staticmethod
    def adapt_schema(
        singer_schema: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Converte singer schema para FlextSchema pattern.

        Args:
            singer_schema: Schema Singer original

        Returns:
            FlextResult contendo schema adaptado

        """
        try:
            # Validar estrutura
            if not isinstance(singer_schema, dict) or "properties" not in singer_schema:
                return FlextResult.fail("Invalid Singer schema structure")

            # Adaptar para formato FlextSchema
            flext_schema = {
                "type": "object",
                "properties": {},
                "required": singer_schema.get("required", []),
            }

            # Processar propriedades
            for prop_name, prop_def in singer_schema["properties"].items():
                flext_schema["properties"][prop_name] = {
                    "type": prop_def.get("type", "string"),
                    "format": prop_def.get("format"),
                    "description": prop_def.get("description"),
                }

            return FlextResult.ok(flext_schema)

        except Exception as e:
            return FlextResult.fail(f"Failed to adapt schema: {e}")

    @staticmethod
    def adapt_records(
        singer_records: Iterator[dict[str, object]],
    ) -> Iterator[dict[str, object]]:
        """Converte singer records para FlextRecord pattern.

        Args:
            singer_records: Iterator de records Singer

        Yields:
            Records adaptados para padrão FLEXT

        """
        for record in singer_records:
            # Adaptar record para formato FLEXT
            flext_record = {
                "data": record,
                "timestamp": record.get("_sdc_extracted_at"),
                "source": "singer",
                "metadata": {
                    "table_name": record.get("_sdc_table_name"),
                    "sequence": record.get("_sdc_sequence"),
                },
            }
            yield flext_record


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    # Singer SDK re-exports for convenience
    "FlextSingerAdapter",
    "MeltanoSingerWrapper",
    "PropertiesList",
    "Property",
    "Stream",
    "Tap",
    "Target",
    "singer_typing",
]
