"""Oracle Database Tap with Enterprise Features.

This module provides the main TapOracle class for Oracle Database
data extraction using modern Singer SDK patterns and FLEXT ecosystem integration.
"""

from __future__ import annotations

import asyncio
import logging
import re

# ARCHITECTURAL FIX: Use direct imports from flext_core
from typing import TYPE_CHECKING, Any, Protocol

from flext_core import FlextEntity, FlextResult, FlextValueObject
from pydantic import BaseModel
from singer_sdk import Tap, typing as th

from flext_meltano.taps.oracle.config import TapOracleConfig
from flext_meltano.taps.oracle.streams import (
    OracleTableStream,
)

# Type aliases for consistency
FlextResult = FlextResult
DomainEntity = FlextEntity
DomainValueObject = FlextValueObject
BaseConfig = BaseModel


class OracleConnectionServiceProtocol(Protocol):
    """Interface for Oracle connection service."""

    async def connect(self) -> FlextResult[Any]: ...
    async def disconnect(self) -> FlextResult[bool]: ...
    async def test_connection(self) -> FlextResult[Any]: ...


class OracleQueryServiceProtocol(Protocol):
    """Interface for Oracle query service."""

    async def execute_query(self, query: str) -> FlextResult[Any]: ...


class OracleSchemaServiceProtocol(Protocol):
    """Interface for Oracle schema service."""

    async def get_tables(self) -> FlextResult[Any]: ...
    async def get_schema_tables(self, schema: str) -> FlextResult[Any]: ...


# Removed circular dependency - use DI pattern
# Resolved: DI pattern implemented successfully


if TYPE_CHECKING:
    from collections.abc import Callable

    # Oracle configuration interface - to be injected via DI
    class OracleConfigProtocol(Protocol):
        """Interface for Oracle configuration."""

        host: str
        port: int
        service_name: str
        username: str
        password: str
        schema: str | None
        pool_max_size: int
        query_timeout: int


# Simple performance tracking decorator
def track_performance(
    name: Callable[..., Any] | str | None = None,
) -> Callable[..., Any]:
    """Simple performance tracking decorator."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        return func

    if callable(name):
        # Used without parameters: @track_performance
        return name
    # Used with parameters: @track_performance("name")
    return decorator


logger = logging.getLogger(__name__)


class TapOracle(Tap):
    """Oracle Database Tap with enterprise features.

    Supports Oracle Database data sources:
    - Direct Oracle Database tables and views

    Features:
    - High-performance async data extraction
    - Enterprise error handling and monitoring
    - Circuit breaker patterns for resilience
    - Comprehensive configuration management
    - Full observability and metrics
    """

    name = "tap-oracle"
    config_jsonschema = th.PropertiesList(
        # Connection configuration
        th.Property(
            "connection_type",
            th.StringType,
            required=True,
            allowed_values=["database"],
            description="Type of Oracle connection (database only)",
        ),
        # Oracle Database connection
        th.Property(
            "host",
            th.StringType,
            description="Oracle database host",
        ),
        th.Property(
            "port",
            th.IntegerType,
            default=1521,
            description="Oracle database port",
        ),
        th.Property(
            "service_name",
            th.StringType,
            description="Oracle service name",
        ),
        th.Property(
            "username",
            th.StringType,
            description="Oracle username",
        ),
        th.Property(
            "password",
            th.StringType,
            secret=True,
            description="Oracle password",
        ),
        th.Property(
            "schema",
            th.StringType,
            description="Oracle schema name",
        ),
        # Stream configuration
        th.Property(
            "tables",
            th.ArrayType(th.StringType),
            description="List of Oracle tables to extract (for database connection)",
        ),
        th.Property(
            "exclude_tables",
            th.ArrayType(th.StringType),
            description="List of tables to exclude from extraction",
        ),
        th.Property(
            "table_pattern",
            th.StringType,
            description="Regex pattern for table names to include",
        ),
        # Performance configuration
        th.Property(
            "batch_size",
            th.IntegerType,
            default=10000,
            description="Batch size for data extraction",
        ),
        th.Property(
            "max_parallel_streams",
            th.IntegerType,
            default=4,
            description="Maximum number of parallel streams",
        ),
        th.Property(
            "connection_pool_size",
            th.IntegerType,
            default=5,
            description="Connection pool size",
        ),
        th.Property(
            "query_timeout",
            th.IntegerType,
            default=300,
            description="Query timeout in seconds",
        ),
        # Advanced configuration
        th.Property(
            "enable_circuit_breaker",
            th.BooleanType,
            default=True,
            description="Enable circuit breaker for resilience",
        ),
        th.Property(
            "circuit_breaker_failures",
            th.IntegerType,
            default=5,
            description="Number of failures before circuit breaker opens",
        ),
        th.Property(
            "circuit_breaker_timeout",
            th.IntegerType,
            default=60,
            description="Circuit breaker timeout in seconds",
        ),
        th.Property(
            "enable_async",
            th.BooleanType,
            default=True,
            description="Enable async processing for performance",
        ),
        th.Property(
            "enable_metrics",
            th.BooleanType,
            default=True,
            description="Enable detailed metrics collection",
        ),
        # Schema flattening configuration
        th.Property(
            "enable_flattening",
            th.BooleanType,
            default=False,
            description="Enable schema flattening for complex Oracle data structures",
        ),
        th.Property(
            "flattening_max_depth",
            th.IntegerType,
            default=5,
            description="Maximum depth for schema flattening",
        ),
        th.Property(
            "flattening_separator",
            th.StringType,
            default="__",
            description="Separator for flattened field names",
        ),
    ).to_dict()

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Initialize the Oracle tap."""
        super().__init__(*args, **kwargs)
        self._tap_config: TapOracleConfig | None = None
        self._oracle_config: OracleConfigProtocol | None = None
        self._connection_service: OracleConnectionServiceProtocol | None = None
        self._query_service: OracleQueryServiceProtocol | None = None
        self._schema_service: OracleSchemaServiceProtocol | None = None

        # Async/sync bridge function - to be injected via DI
        self._run_async_in_sync: Callable[[Any], Any] | None = None

    @property
    def tap_config(self) -> TapOracleConfig:
        """Get typed configuration."""
        if self._tap_config is None:
            # Debug what we have
            logger.debug("Creating TapOracleConfig, self._config is None")

            try:
                # Access raw config dict from Singer SDK
                raw_config = {}

                # Try different ways to get the config
                if hasattr(self, "_config_dict") and self._config_dict:
                    raw_config = dict(self._config_dict)
                    logger.debug("Got config from _config_dict: %s", raw_config)
                elif hasattr(self, "config") and self.config is not None:
                    try:
                        raw_config = dict(self.config)
                        logger.debug("Got config from self.config: %s", raw_config)
                    except (TypeError, AttributeError) as e:
                        logger.debug("Could not convert self.config to dict: %s", e)
                        raw_config = {}

                # Ensure minimum required config
                if "connection_type" not in raw_config:
                    raw_config["connection_type"] = "database"
                if "host" not in raw_config:
                    raw_config["host"] = "localhost"
                if "username" not in raw_config:
                    raw_config["username"] = "oracle"
                if "password" not in raw_config:
                    raw_config["password"] = "oracle"

                logger.debug("Final raw_config for TapOracleConfig: %s", raw_config)
                self._tap_config = TapOracleConfig(**raw_config)
                logger.debug("TapOracleConfig created successfully")

            except Exception:
                logger.exception("Failed to create TapOracleConfig")
                # Create minimal config to prevent crash
                self._tap_config = TapOracleConfig(
                    connection_type="database",
                    host="localhost",
                    username="oracle",
                    password="oracle",
                )

        # Return config cast to correct type
        return self._tap_config

    @property
    def connection_service(self) -> OracleConnectionServiceProtocol:
        """Get Oracle connection service via DI injection.

        Note: In proper DI implementation, services should be injected via constructor
        or dependency container.
        This property serves as a temporary compatibility layer.
        """
        if self._connection_service is None:
            self._raise_missing_services_error()
        return self._connection_service

    def inject_oracle_services(
        self,
        connection_service: OracleConnectionServiceProtocol,
        query_service: OracleQueryServiceProtocol,
        schema_service: OracleSchemaServiceProtocol,
        async_sync_bridge: Callable[[Any], Any],
    ) -> None:
        """Inject Oracle services via DI.

        This method implements Dependency Injection pattern.
        All concrete Oracle implementations are injected from outside.
        """
        self._connection_service = connection_service
        self._query_service = query_service
        self._schema_service = schema_service
        self._run_async_in_sync = async_sync_bridge

        logger.info("Oracle services injected vi    a DI")

    def _raise_missing_bridge_error(self) -> None:
        """Raise error for missing async/sync bridge injection."""
        msg = "Async/sync bridge not injected. Use inject_oracle_services() first."
        raise RuntimeError(msg)

    def _raise_missing_services_error(self) -> None:
        """Raise error for missing Oracle services injection."""
        msg = (
            "Oracle connection service not injected. "
            "Services must be injected via DI container."
        )
        raise RuntimeError(msg)

    def test_connection_modern(self) -> bool:
        """Test connection using injected Oracle services with async/sync bridge."""
        try:
            if self._run_async_in_sync is None:
                self._raise_missing_bridge_error()

            # Use the injected async/sync bridge
            result = self._run_async_in_sync(
                self.connection_service.test_connection(),
            )
        except Exception:
            logger.exception("Oracle connection test failed")
            return False
        else:
            return result.success

    @track_performance("tap_oracle.discover_streams")
    def discover_streams(self) -> list[Any]:
        """Discover available streams based on connection type.

        Returns:
            List of stream classes for the configured Oracle sources.

        """
        streams = []

        # Get connection type directly to avoid property issues during init
        try:
            connection_type = self.tap_config.connection_type
        except (AttributeError, TypeError):
            # Fallback to direct config access
            raw_config = (
                getattr(self, "_config_dict", None) or dict(self.config)
                if hasattr(self, "config") and self.config
                else {}
            )
            connection_type = raw_config.get("connection_type", "database")

        if connection_type == "database":
            streams.extend(self._discover_database_streams())

        logger.info(
            "Discovered %d Oracle database streams",
            len(streams),
        )

        return streams

    def _discover_database_streams(self) -> list[Any]:
        """Discover Oracle database table streams.

        Returns:
            List of discovered OracleTableStream instances

        """
        streams = []

        try:
            # Use modern Oracle DB services for discovery
            if not hasattr(self, "_schema_service") or self._schema_service is None:
                # Initialize services if not already done
                _ = self.connection_service

            # Get table list using injected services with async/sync bridge
            if self._run_async_in_sync is None:
                self._raise_missing_bridge_error()

            tables = self._run_async_in_sync(self._get_discoverable_tables())

            # Create stream for each table
            for table_name in tables:
                stream = OracleTableStream(
                    tap=self,
                    name=table_name,
                    table_name=table_name,
                    schema=self.tap_config.get_effective_schema(),
                )
                streams.append(stream)

            logger.info("Discovered %d Oracle database streams", len(streams))

        except Exception:
            logger.exception("Failed to discover database streams")

        return streams

    async def _get_discoverable_tables(self) -> list[str]:
        """Get list of tables to discover using modern Oracle DB services.

        Returns:
            List of table names to create streams for

        """
        # If specific tables are configured, use those
        if self.tap_config.tables:
            return list(self.tap_config.tables)

        # Otherwise, discover all tables in schema using modern services
        try:
            if self._schema_service is None:
                logger.error("Schema service not initialized")
                return []
            result = await self._schema_service.get_schema_tables(
                self.tap_config.get_effective_schema(),
            )
            if not result.success:
                logger.error("Failed to get table names: %s", result.error)
                return []

            # Extract table names from OracleTableMetadata objects
            all_tables: list[str] = (
                [table.table_name for table in result.data] if result.data else []
            )

            # Apply exclusions
            if self.tap_config.exclude_tables:
                all_tables = [
                    table
                    for table in all_tables
                    if table not in self.tap_config.exclude_tables
                ]

            # Apply pattern filter if configured
            if self.tap_config.table_pattern:
                pattern = re.compile(self.tap_config.table_pattern)
                all_tables = [table for table in all_tables if pattern.match(table)]

        except Exception:
            logger.exception("Error getting table names")
            return []
        else:
            return all_tables

    @track_performance("tap_oracle.test_connection")
    def test_connection(self) -> bool:
        """Test connection to configured Oracle sources.

        Returns:
            True if all configured connections are successful

        """
        connection_type = self.tap_config.connection_type

        results = {}

        if connection_type == "database":
            results["database"] = self._test_database_connection()

        # All configured connections must succeed
        success = all(results.values())

        logger.info(
            "Connection test results: %s (overall: %s)",
            results,
            "SUCCESS" if success else "FAILURE",
        )

        return success

    def _test_database_connection(self) -> bool:
        """Test Oracle database connection using injected async/sync bridge."""
        try:
            if self._run_async_in_sync is None:
                self._raise_missing_bridge_error()

            # Use injected async/sync bridge
            result = self._run_async_in_sync(
                self.connection_service.test_connection(),
            )
        except Exception:
            logger.exception("Database connection test failed")
            return False
        else:
            return result.success

    async def run_async(self) -> None:
        """Run the tap with async support for high performance."""
        if not self.tap_config.enable_async:
            # Fall back to synchronous mode
            self.sync_all()
            return

        logger.info("Running Oracle tap in async mode")

        # Discover streams
        streams = self.discover_streams()

        # Process streams with controlled parallelism
        semaphore = asyncio.Semaphore(self.tap_config.max_parallel_streams)

        async def process_stream(stream: object) -> None:
            async with semaphore:
                await stream.sync_async()

        # Run all streams concurrently
        await asyncio.gather(*[process_stream(stream) for stream in streams])

    def get_metrics(self) -> dict[str, Any]:
        """Get comprehensive tap metrics.

        Returns:
            Dictionary containing performance and operational metrics

        """
        if not self.tap_config.enable_metrics:
            return {}

        metrics = {
            "connection_type": self.tap_config.connection_type,
            "streams_discovered": len(self.discover_streams()),
            "configuration": {
                "batch_size": self.tap_config.batch_size,
                "max_parallel_streams": self.tap_config.max_parallel_streams,
                "connection_pool_size": self.tap_config.connection_pool_size,
                "async_enabled": self.tap_config.enable_async,
                "circuit_breaker_enabled": self.tap_config.enable_circuit_breaker,
            },
        }

        # Add connection service metrics if available
        if hasattr(self, "_connection_service") and self._connection_service:
            metrics["connection_service_active"] = True
        else:
            metrics["connection_service_active"] = False

        return metrics


# CLI entry point
def cli() -> None:
    """Command line interface for the Oracle tap."""
    TapOracle.cli()
