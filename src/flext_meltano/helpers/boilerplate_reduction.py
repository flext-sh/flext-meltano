"""FLEXT Meltano Boilerplate Reduction Helpers.

Copyright (c) 2025 FLEXT Team. All rights reserved.

Este módulo fornece utilities para reduzir drasticamente o boilerplate:
- Decorators para pipelines automáticos
- Mixins para funcionalidades comuns
- TypeDefs para simplificar tipos
- Dict/Config helpers
- One-liner functions

FOCO: Transformar 50+ linhas em 1-3 linhas de código!
"""

from __future__ import annotations

import asyncio
import functools
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, TypeVar

from flext_meltano.core import FlextMeltanoPipelineResult

if TYPE_CHECKING:
    from pathlib import Path

# =============================================================================
# TYPEDEFS - Simplificar tipos comuns
# =============================================================================

# Pipeline types - reduz definições repetitivas
type PipelineConfig = dict[str, Any]
type PipelineResult = FlextMeltanoPipelineResult
type TapTargetPair = tuple[str, str]
type StreamList = list[str]
type ConfigDict = dict[str, str | int | bool | None]

# Function types - para decorators
F = TypeVar("F", bound=Callable[..., Any])
AsyncF = TypeVar("AsyncF", bound=Callable[..., Any])

# =============================================================================
# CONFIGURATION HELPERS - Dict/Config simplificados
# =============================================================================

class QuickConfig:
    """Configuração ultra-simplificada - reduz 20+ linhas para 1."""

    # Presets para eliminação de boilerplate
    POSTGRES_TAP = {"tap": "tap-postgres", "schema": "public"}
    CSV_TAP = {"tap": "tap-csv", "files": []}
    ORACLE_TAP = {"tap": "tap-oracle", "sqlnet": True}

    JSON_TARGET = {"target": "target-jsonl", "path": "output/"}
    CSV_TARGET = {"target": "target-csv", "path": "output/"}
    POSTGRES_TARGET = {"target": "target-postgres", "schema": "raw"}

    @classmethod
    def quick_pipeline(
        cls,
        source: str = "postgres",
        dest: str = "csv",
        **kwargs: object,
    ) -> PipelineConfig:
        """Uma linha para configurar pipeline completo."""
        sources = {
            "postgres": cls.POSTGRES_TAP,
            "csv": cls.CSV_TAP,
            "oracle": cls.ORACLE_TAP,
        }
        destinations = {
            "csv": cls.CSV_TARGET,
            "json": cls.JSON_TARGET,
            "postgres": cls.POSTGRES_TARGET,
        }

        return {
            **sources.get(source, cls.CSV_TAP),
            **destinations.get(dest, cls.CSV_TARGET),
            **kwargs,
        }

# =============================================================================
# MIXINS - Funcionalidades reutilizáveis
# =============================================================================

class PipelineMixin:
    """Mixin que adiciona capacidades de pipeline - reduz 30+ linhas."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Initialize pipeline capabilities."""
        super().__init__(*args, **kwargs)  # type: ignore[misc]
        self._pipeline_cache: dict[str, Any] = {}
        self._last_result: PipelineResult | None = None

    def quick_run(self, tap: str, target: str, **config: object) -> PipelineResult:
        """Uma linha para executar pipeline."""
        from flext_meltano.flext_meltano_core_api import flext_meltano_pipeline_sync

        result = flext_meltano_pipeline_sync(tap, target, **config)
        self._last_result = result
        return result

    async def quick_run_async(self, tap: str, target: str, **config: object) -> PipelineResult:
        """Uma linha para executar pipeline async."""
        from flext_meltano.flext_meltano_core_api import flext_meltano_pipeline

        result = await flext_meltano_pipeline(tap, target, **config)
        self._last_result = result
        return result

    @property
    def last_success(self) -> bool:
        """Check se último pipeline teve sucesso."""
        return self._last_result is not None and self._last_result.success

    @property
    def last_records(self) -> int:
        """Get records processados no último pipeline."""
        return self._last_result.records_processed if self._last_result else 0


class ConfigMixin:
    """Mixin para configurações simplificadas - reduz 15+ linhas."""

    _default_config: ClassVar[ConfigDict] = {
        "environment": "dev",
        "project_root": ".",
        "batch_size": 1000,
    }

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Initialize with default config."""
        super().__init__(*args, **kwargs)  # type: ignore[misc]
        self.config = {**self._default_config, **kwargs}

    def update_config(self, **updates: object) -> None:
        """Uma linha para atualizar configuração."""
        self.config.update(updates)

    def get_config_value(self, key: str, default: object = None) -> object:
        """Uma linha para pegar valor de config."""
        return self.config.get(key, default)


class LoggingMixin:
    """Mixin para logging simplificado - reduz 10+ linhas."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Initialize with auto-logging."""
        super().__init__(*args, **kwargs)  # type: ignore[misc]
        from flext_core import get_logger
        self.logger = get_logger(self.__class__.__name__)

    def log_pipeline_start(self, tap: str, target: str) -> None:
        """Uma linha para log de início."""
        self.logger.info("Starting pipeline: %s -> %s", tap, target)

    def log_pipeline_success(self, records: int, duration: float) -> None:
        """Uma linha para log de sucesso."""
        self.logger.info("Pipeline completed: %d records in %.2fs", records, duration)

    def log_pipeline_error(self, error: str) -> None:
        """Uma linha para log de erro."""
        self.logger.error("Pipeline failed: %s", error)

# =============================================================================
# DECORATORS - Automatização máxima
# =============================================================================

def auto_pipeline(tap: str, target: str, **default_config: object) -> Callable[[F], F]:
    """Decorator para transformar função em pipeline automático.

    Reduz 50+ linhas para 3 linhas:

    @auto_pipeline("tap-csv", "target-json")
    def my_data_flow():
        return {"files": ["data.csv"]}
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> PipelineResult:
            # Get config from function
            config = func(*args, **kwargs) or {}
            final_config = {**default_config, **config}

            # Execute pipeline
            from flext_meltano.flext_meltano_core_api import flext_meltano_pipeline_sync
            return flext_meltano_pipeline_sync(tap, target, **final_config)

        return wrapper  # type: ignore[return-value]
    return decorator


def async_pipeline(tap: str, target: str, **default_config: object) -> Callable[[AsyncF], AsyncF]:
    """Decorator async para pipeline automático.

    @async_pipeline("tap-postgres", "target-csv")
    async def extract_users():
        return {"query": "SELECT * FROM users"}
    """
    def decorator(func: AsyncF) -> AsyncF:
        @functools.wraps(func)
        async def wrapper(*args: object, **kwargs: object) -> PipelineResult:
            # Get config from function
            config = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            config = config or {}
            final_config = {**default_config, **config}

            # Execute pipeline
            from flext_meltano.flext_meltano_core_api import flext_meltano_pipeline
            return await flext_meltano_pipeline(tap, target, **final_config)

        return wrapper  # type: ignore[return-value]
    return decorator


def retry_pipeline(max_retries: int = 3, delay: float = 1.0) -> Callable[[F], F]:
    """Decorator para retry automático de pipelines.

    @retry_pipeline(max_retries=3)
    @auto_pipeline("tap-api", "target-postgres")
    def unreliable_api():
        return {"base_url": "https://api.example.com"}
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            last_error = None

            for attempt in range(max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                    if hasattr(result, "success") and result.success:
                        return result
                    last_error = getattr(result, "error_message", "Unknown error")
                except Exception as e:
                    last_error = str(e)

                if attempt < max_retries:
                    import time
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff

            # Return failed result after all retries
            import uuid

            from flext_meltano.core import (
                FlextMeltanoExecutionState,
                FlextMeltanoPipelineResult,
            )
            return FlextMeltanoPipelineResult(
                pipeline_id=str(uuid.uuid4()),
                state=FlextMeltanoExecutionState.FAILED,
                error_message=f"Failed after {max_retries} retries: {last_error}",
            )

        return wrapper  # type: ignore[return-value]
    return decorator


def batch_pipeline(batch_size: int = 1000) -> Callable[[F], F]:
    """Decorator para processamento em batch automático."""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> list[PipelineResult]:
            # Get data source
            data_config = func(*args, **kwargs)

            # Split into batches and process
            # Implement batching logic here
            # For now, return single result
            return [data_config]  # type: ignore[list-item]

        return wrapper  # type: ignore[return-value]
    return decorator

# =============================================================================
# ONE-LINER FUNCTIONS - Máxima redução de código
# =============================================================================

def quick_csv_to_json(input_file: str, output_dir: str = "output/") -> PipelineResult:
    """Uma linha: CSV → JSON."""
    from flext_meltano.flext_meltano_core_api import flext_meltano_pipeline_sync
    return flext_meltano_pipeline_sync(
        "tap-csv",
        "target-jsonl",
        files=[input_file],
        path=output_dir,
    )


def quick_postgres_to_csv(
    connection_string: str,
    query: str,
    output_dir: str = "output/",
) -> PipelineResult:
    """Uma linha: PostgreSQL → CSV."""
    from flext_meltano.flext_meltano_core_api import flext_meltano_pipeline_sync
    return flext_meltano_pipeline_sync(
        "tap-postgres",
        "target-csv",
        connection_string=connection_string,
        query=query,
        path=output_dir,
    )


def quick_oracle_to_postgres(
    oracle_conn: str,
    postgres_conn: str,
    table: str,
) -> PipelineResult:
    """Uma linha: Oracle → PostgreSQL."""
    from flext_meltano.flext_meltano_core_api import flext_meltano_pipeline_sync
    return flext_meltano_pipeline_sync(
        "tap-oracle",
        "target-postgres",
        oracle_connection=oracle_conn,
        postgres_connection=postgres_conn,
        selected_streams=[table],
    )


async def quick_api_to_db(
    api_url: str,
    db_connection: str,
    endpoint: str = "/api/data",
) -> PipelineResult:
    """Uma linha async: API → Database."""
    from flext_meltano.flext_meltano_core_api import flext_meltano_pipeline
    return await flext_meltano_pipeline(
        "tap-rest-api",
        "target-postgres",
        base_url=api_url,
        endpoints=[endpoint],
        connection_string=db_connection,
    )

# =============================================================================
# UTILITY CLASSES - Para casos específicos
# =============================================================================

@dataclass
class PipelineBuilder:
    """Builder pattern para pipelines complexos - reduz 100+ linhas."""

    tap: str = ""
    target: str = ""
    config: dict[str, Any] = field(default_factory=dict)
    streams: list[str] = field(default_factory=list)
    environment: str = "dev"

    def from_source(self, source: str, **config: object) -> PipelineBuilder:
        """Fluent interface para configurar source."""
        source_map = {
            "csv": "tap-csv",
            "postgres": "tap-postgres",
            "oracle": "tap-oracle",
            "api": "tap-rest-api",
        }
        self.tap = source_map.get(source, source)
        self.config.update(config)
        return self

    def to_destination(self, dest: str, **config: object) -> PipelineBuilder:
        """Fluent interface para configurar destination."""
        dest_map = {
            "csv": "target-csv",
            "json": "target-jsonl",
            "postgres": "target-postgres",
        }
        self.target = dest_map.get(dest, dest)
        self.config.update(config)
        return self

    def with_streams(self, *streams: str) -> PipelineBuilder:
        """Fluent interface para configurar streams."""
        self.streams.extend(streams)
        return self

    def in_env(self, env: str) -> PipelineBuilder:
        """Fluent interface para configurar environment."""
        self.environment = env
        return self

    def build(self) -> PipelineConfig:
        """Build final configuration."""
        return {
            "tap": self.tap,
            "target": self.target,
            "selected_streams": self.streams if self.streams else None,
            "environment": self.environment,
            **self.config,
        }

    def run(self) -> PipelineResult:
        """Build e execute em uma linha."""
        from flext_meltano.flext_meltano_core_api import flext_meltano_pipeline_sync
        return flext_meltano_pipeline_sync(self.tap, self.target, **self.config)

    async def run_async(self) -> PipelineResult:
        """Build e execute async em uma linha."""
        from flext_meltano.flext_meltano_core_api import flext_meltano_pipeline
        return await flext_meltano_pipeline(self.tap, self.target, **self.config)


class QuickMeltano(PipelineMixin, ConfigMixin, LoggingMixin):
    """Classe all-in-one para redução máxima de boilerplate.

    Em vez de 50+ linhas:
    quick = QuickMeltano()
    result = quick.csv_to_json("data.csv")
    """

    def __init__(self, project_root: str | Path = ".") -> None:
        """Initialize com defaults inteligentes."""
        super().__init__(project_root=str(project_root))

    def csv_to_json(self, csv_file: str, output_dir: str = "output/") -> PipelineResult:
        """Uma linha: CSV → JSON."""
        return self.quick_run("tap-csv", "target-jsonl", files=[csv_file], path=output_dir)

    def postgres_to_csv(self, connection: str, query: str) -> PipelineResult:
        """Uma linha: PostgreSQL → CSV."""
        return self.quick_run("tap-postgres", "target-csv", connection_string=connection, query=query)

    def oracle_to_postgres(self, oracle_conn: str, postgres_conn: str) -> PipelineResult:
        """Uma linha: Oracle → PostgreSQL."""
        return self.quick_run("tap-oracle", "target-postgres",
                             oracle_connection=oracle_conn, postgres_connection=postgres_conn)

    def api_to_db(self, api_url: str, db_conn: str, endpoint: str = "/data") -> PipelineResult:
        """Uma linha: API → Database."""
        return self.quick_run("tap-rest-api", "target-postgres",
                             base_url=api_url, endpoints=[endpoint], connection_string=db_conn)

# =============================================================================
# EXPORTS - Só o essencial para reduzir imports
# =============================================================================

__all__ = [
    "ConfigDict",
    "ConfigMixin",
    "LoggingMixin",
    # Utility Classes
    "PipelineBuilder",
    # TypeDefs
    "PipelineConfig",
    # Mixins
    "PipelineMixin",
    "PipelineResult",
    # Config Helpers
    "QuickConfig",
    "QuickMeltano",
    "StreamList",
    "TapTargetPair",
    "async_pipeline",
    # Decorators
    "auto_pipeline",
    "batch_pipeline",
    "quick_api_to_db",
    # One-liners
    "quick_csv_to_json",
    "quick_oracle_to_postgres",
    "quick_postgres_to_csv",
    "retry_pipeline",
]
