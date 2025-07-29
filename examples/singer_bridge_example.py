#!/usr/bin/env python3
"""Exemplo de uso do Bridge Singer SDK com flext-core.

Demonstra como usar o bridge real entre Singer SDK e flext-core
para criar taps e targets profissionais.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextResult, get_logger

from flext_meltano import (
    FlextIncrementalTap,
    # Bridge Singer
    FlextStreamingTarget,
    # Implementações específicas
    FlextTapBase,
    FlextTargetBase,
    create_singer_bridge,
    create_singer_catalog,
    create_singer_service,
    # Utilitários
    create_tap,
    create_target,
    validate_tap_config,
    validate_target_config,
)
from flext_meltano._base import Stream

if TYPE_CHECKING:
    from collections.abc import Iterator

logger = get_logger(__name__)


# =============================================================================
# EXEMPLO 1: USO BÁSICO DO BRIDGE SINGER
# =============================================================================


def exemplo_bridge_basico() -> None:
    """Demonstra uso básico do bridge Singer SDK."""
    # Criar bridge
    bridge = create_singer_bridge()

    # Converter flext-core para Singer SDK
    record_data = {"id": 1, "name": "Test Record", "value": 42.5}

    # Criar mensagem Singer RECORD
    singer_record = bridge.flext_to_singer_record(
        stream="test_stream",
        record=record_data,
        time_extracted="2025-01-01T12:00:00Z",
    )

    if singer_record.is_success:

        # Escrever mensagem Singer
        write_result = bridge.write_singer_message(singer_record.data)
        if write_result.is_success:
            pass


# =============================================================================
# EXEMPLO 2: CATALOG MANAGEMENT
# =============================================================================


def exemplo_catalog_management() -> None:
    """Demonstra gerenciamento de catalog."""
    # Criar catalog
    catalog = create_singer_catalog()

    # Adicionar streams
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"},
        },
    }

    result = catalog.add_stream(
        stream_name="users",
        schema=schema,
        key_properties=["id"],
    )

    if result.is_success:

        # Obter catalog completo
        catalog_data = catalog.get_catalog()
        if catalog_data.is_success:
            pass


# =============================================================================
# EXEMPLO 3: TAP PERSONALIZADO
# =============================================================================


class ExemploTap(FlextTapBase):
    """Exemplo de tap personalizado."""

    name = "exemplo-tap"

    def discover_streams(self) -> list[Any]:
        """Descobrir streams disponíveis."""
        # Simular descoberta de streams

        class ExemploStream(Stream):
            def __init__(self, tap: Any, name: str) -> None:
                schema = {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "data": {"type": "string"},
                    },
                }
                super().__init__(tap, schema=schema, name=name)
                self._key_properties = ["id"]

            def get_records(
                self,
                context: dict[str, Any] | None,
            ) -> Iterator[dict[str, Any]]:
                """Get records from stream."""
                # Simular dados
                yield {"id": 1, "data": "Record 1"}
                yield {"id": 2, "data": "Record 2"}
                yield {"id": 3, "data": "Record 3"}

        return [ExemploStream(self, "exemplo_stream")]

    def _test_connection_impl(self) -> bool:
        """Testar conexão."""
        return True

    def _process_stream(self, stream_name: str, stream_info: dict[str, Any]) -> None:
        """Processar stream durante sync."""
        # Simular extração de dados
        self._records_extracted += 10


def exemplo_tap_personalizado() -> None:
    """Demonstra criação de tap personalizado."""
    # Configuração do tap
    config = {
        "host": "localhost",
        "port": 5432,
        "username": "user",
        "password": "pass",
        "database": "testdb",
    }

    # Validar configuração
    validation = validate_tap_config(ExemploTap, config)
    if not validation.is_success:
        return

    # Criar tap
    tap = create_tap(ExemploTap, config)

    # Descobrir streams
    discovery = tap.discover()
    if discovery.is_success:

        # Sync
        catalog = discovery.data["catalog"]
        sync_result = tap.sync(catalog)
        if sync_result.is_success:
            pass


# =============================================================================
# EXEMPLO 4: TARGET PERSONALIZADO
# =============================================================================


class ExemploTarget(FlextTargetBase):
    """Exemplo de target personalizado."""

    def _write_records_impl(self, records: list[dict[str, Any]]) -> FlextResult[None]:
        """Implementação de escrita de records."""
        try:
            for _record in records:
                pass
            return FlextResult.ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.error(f"Erro ao escrever records: {e}")

    def _test_connection_impl(self) -> bool:
        """Testar conexão."""
        return True


def exemplo_target_personalizado() -> None:
    """Demonstra criação de target personalizado."""
    # Configuração do target
    config = {
        "host": "localhost",
        "port": 5432,
        "username": "user",
        "password": "pass",
        "database": "targetdb",
    }

    # Validar configuração
    validation = validate_target_config(ExemploTarget, config)
    if not validation.is_success:
        return

    # Criar target
    target = create_target(ExemploTarget, config)

    # Escrever records
    records = [
        {"id": 1, "name": "Record 1"},
        {"id": 2, "name": "Record 2"},
        {"id": 3, "name": "Record 3"},
    ]

    write_result = target.write_records(records)
    if write_result.is_success:

        # Obter métricas
        target.get_target_metrics()


# =============================================================================
# EXEMPLO 5: SERVIÇO SINGER SDK
# =============================================================================


def exemplo_servico_singer() -> None:
    """Demonstra uso do serviço Singer SDK."""
    # Criar serviço
    service = create_singer_service()

    # Obter informações do Singer SDK
    info = service.get_singer_sdk_info()
    if info.is_success:
        pass

    # Validar configuração de tap
    tap_config = {
        "host": "localhost",
        "port": 5432,
        "username": "user",
        "password": "pass",
    }

    validation = service.validate_tap_config("exemplo-tap", tap_config)
    if validation.is_success:
        pass

    # Descobrir streams
    discovery = service.discover_streams("exemplo-tap", tap_config)
    if discovery.is_success:
        pass


# =============================================================================
# EXEMPLO 6: TAP INCREMENTAL
# =============================================================================


class ExemploIncrementalTap(FlextIncrementalTap):
    """Exemplo de tap incremental."""

    name = "exemplo-incremental-tap"

    def discover_streams(self) -> list[Any]:
        """Descobrir streams disponíveis."""
        class IncrementalStream(Stream):
            def __init__(self, tap: Any, name: str) -> None:
                super().__init__(tap, name=name)
                self.schema = {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "data": {"type": "string"},
                        "updated_at": {"type": "string", "format": "date-time"},
                    },
                }
                self.key_properties = ["id"]

        return [IncrementalStream(self, "incremental_stream")]

    def _test_connection_impl(self) -> bool:
        """Testar conexão."""
        return True

    def _load_state(self) -> FlextResult[dict[str, Any]]:
        """Carregar estado atual."""
        # Simular carregamento de estado
        state = {"incremental_stream": {"updated_at": "2025-01-01T00:00:00Z"}}
        return FlextResult.ok(state)

    def _save_state(self) -> FlextResult[bool]:
        """Salvar estado atual."""
        # Simular salvamento de estado
        return FlextResult.ok(True)


def exemplo_tap_incremental() -> None:
    """Demonstra tap incremental."""
    config = {
        "host": "localhost",
        "port": 5432,
        "username": "user",
        "password": "pass",
        "replication_key": "updated_at",
    }

    tap = create_tap(ExemploIncrementalTap, config)

    # Descobrir e sync
    discovery = tap.discover()
    if discovery.is_success:
        catalog = discovery.data["catalog"]
        sync_result = tap.sync(catalog)
        if sync_result.is_success:
            pass


# =============================================================================
# EXEMPLO 7: TARGET STREAMING
# =============================================================================


class ExemploStreamingTarget(FlextStreamingTarget):
    """Exemplo de target streaming."""

    def _write_records_impl(self, records: list[dict[str, Any]]) -> FlextResult[None]:
        """Implementação de escrita de records."""
        try:
            for _record in records:
                pass
            return FlextResult.ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.error(f"Erro no streaming: {e}")

    def _test_connection_impl(self) -> bool:
        """Testar conexão."""
        return True


def exemplo_target_streaming() -> None:
    """Demonstra target streaming."""
    config = {
        "host": "localhost",
        "port": 5432,
        "username": "user",
        "password": "pass",
        "batch_size": 2,  # Buffer pequeno para demonstração
    }

    target = create_target(ExemploStreamingTarget, config)

    # Escrever records em lotes pequenos
    records_batch1 = [{"id": 1, "data": "batch1"}]
    records_batch2 = [{"id": 2, "data": "batch2"}]
    records_batch3 = [{"id": 3, "data": "batch3"}]

    # Primeiro lote (fica no buffer)
    target.write_records(records_batch1)

    # Segundo lote (processa buffer + novo lote)
    target.write_records(records_batch2)

    # Terceiro lote (fica no buffer)
    target.write_records(records_batch3)

    # Flush final
    target.flush()


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================


def main() -> None:
    """Executar todos os exemplos."""
    try:
        exemplo_bridge_basico()
        exemplo_catalog_management()
        exemplo_tap_personalizado()
        exemplo_target_personalizado()
        exemplo_servico_singer()
        exemplo_tap_incremental()
        exemplo_target_streaming()

    except (RuntimeError, ValueError, TypeError) as e:
        logger.exception(f"Erro durante execução dos exemplos: {e}")


if __name__ == "__main__":
    main()
