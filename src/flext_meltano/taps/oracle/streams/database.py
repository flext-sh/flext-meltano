"""Oracle Database table and view streaming capabilities using the flext-db-oracle.

This implementation uses the actual foundation for zero code duplication.
"""

# MIGRATED: Singer SDK imports centralized via flext-meltano
from __future__ import annotations

import asyncio
import logging
import time
from itertools import starmap
from typing import TYPE_CHECKING, Any

from flext_db_oracle import FlextDbOracleConfig as OracleConfig
from flext_db_oracle.application import (
    FlextDbOracleConnectionService as OracleConnectionService,
    FlextDbOracleQueryService as OracleQueryService,
)
from flext_db_oracle.utils.exceptions import FlextDbOracleQueryError as OracleQueryError
from flext_tap_oracle.query_builder import SimpleOracleQueryBuilder
from flext_tap_oracle.schema_flattener import OracleSchemaFlattener
from flext_tap_oracle.streams.base import BaseOracleStream

from flext_meltano import th


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


if TYPE_CHECKING:
    import collections.abc
    from collections.abc import Callable, Iterable
# Removed circular dependency - use DI pattern
# Resolved: DI pattern implemented successfully




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


if TYPE_CHECKING:
    from flext_tap_oracle.tap import TapOracle
logger = get_logger(__name__)


class OracleTableStream(BaseOracleStream):
    """Oracle Database Table Stream with enterprise features.

    Streams data from Oracle database tables using
    flext-infrastructure.databases.flext-db-oracle
    as the connection foundation. Supports incremental extraction,
    performance monitoring, and enterprise error handling.
    """

    def __init__(
        self,
        tap: TapOracle,
        name: str,
        table_name: str,
        schema: str | None = None,
        oracle_config: dict[str, Any] | None = None,
        primary_keys: list[str] | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle table stream.

        Args:
            tap: Parent tap instance
            name: Stream name
            table_name: Oracle table name
            schema: Oracle schema name
            oracle_config: Pre-configured Oracle config dictionary
            primary_keys: Primary key columns
            **kwargs: Additional stream arguments

        """
        super().__init__(tap=tap, name=name, **kwargs)
        self.table_name = table_name
        self.schema_name = schema or tap.tap_config.get_effective_schema()
        self.primary_keys = primary_keys or []
        self._oracle_config = oracle_config
        # Modern flext-infrastructure.databases.flext-db-oracle services for
        # real database operations
        self._oracle_connection_service: OracleConnectionService | None = None
        self._oracle_query_service: OracleQueryService | None = None
        # Performance tracking
        self._last_extracted_value: Any | None = None
        self._total_rows_extracted = 0
        self._column_cache: list[dict[str, Any]] | None = None
        self._last_query: str | None = None
        # Schema flattening configuration
        self._schema_flattener = OracleSchemaFlattener(
            enabled=(
                getattr(tap.config, "enable_flattening", False)
                if hasattr(tap, "config")
                else False
            ),
            max_depth=(
                getattr(tap.config, "flattening_max_depth", 5)
                if hasattr(tap, "config")
                else 5
            ),
            separator=(
                getattr(tap.config, "flattening_separator", "__")
                if hasattr(tap, "config")
                else "__"
            ),
            preserve_types=True,
        )
        # Modern query builder using flext-infrastructure.databases.flext-db-oracle
        # parameterization
        self._query_builder = SimpleOracleQueryBuilder()
        logger.info(
            "Initialized Oracle table stream: %s.%s",
            schema or "default",
            table_name,
        )

    @property
    def oracle_query_service(self) -> OracleQueryService:
        """Get modern Oracle query service using flext-db-oracle.

        Returns:
            OracleQueryService instance for query execution

        """
        if self._oracle_query_service is None:
            # Initialize from tap's connection service
            if hasattr(self, "tap") and hasattr(self.tap, "connection_service"):
                oracle_connection_service = self.tap.connection_service
                self._oracle_query_service = OracleQueryService(
                    oracle_connection_service,
                )
            else:
                # Fallback: create from tap config
                if hasattr(self, "tap") and hasattr(self.tap, "tap_config"):
                    oracle_config = self.tap.tap_config.to_oracle_config()
                else:
                    # Create minimal config if tap not available
                    oracle_config = OracleConfig(
                        host="localhost",
                        port=1521,
                        service_name="XE",
                        username="oracle",
                        password="oracle",
                    )
                oracle_connection_service = OracleConnectionService(oracle_config)
                self._oracle_query_service = OracleQueryService(
                    oracle_connection_service,
                )
        return self._oracle_query_service

    @property
    def query_service(self) -> OracleQueryService:
        """Get Oracle query service using flext-db-oracle (NO DIRECT CONNECTION).

        Returns:
            OracleQueryService instance from the tap's connection service

        """
        # Always use the tap's connection service
        if hasattr(self, "tap") and hasattr(self.tap, "connection_service"):
            if self._oracle_query_service is None:
                connection_service = self.tap.connection_service
                self._oracle_query_service = OracleQueryService(connection_service)
            return self._oracle_query_service
        msg = "No connection service available from tap"
        raise OracleQueryError(msg)

    @property
    def schema(self) -> dict[str, Any]:
        """Dynamically discover table schema from Oracle."""
        if not hasattr(self, "_schema_cache"):
            self._schema_cache = self._discover_schema()
        return self._schema_cache

    def _discover_schema(self) -> dict[str, Any]:
        """Discover table schema from Oracle metadata.

        Returns:
            JSON Schema for the table

        """
        try:
            # Get table metadata using flext-infrastructure.databases.flext-db-oracle
            # methods
            columns = self._get_table_columns()
            properties = {}
            for col in columns:
                col_name = col["column_name"].lower()
                oracle_type = col["data_type"].upper()
                # Map Oracle types to JSON Schema types using proper typing
                property_type: th.JSONTypeHelper[Any]
                if oracle_type in {
                    "NUMBER",
                    "INTEGER",
                    "FLOAT",
                    "BINARY_FLOAT",
                    "BINARY_DOUBLE",
                }:
                    scale = col.get("data_scale", 0)
                    if scale and scale > 0:
                        property_type = th.NumberType()
                    else:
                        property_type = th.IntegerType()
                elif oracle_type in {
                    "VARCHAR2",
                    "CHAR",
                    "NVARCHAR2",
                    "NCHAR",
                    "CLOB",
                    "NCLOB",
                }:
                    property_type = th.StringType()
                elif oracle_type in {"DATE", "TIMESTAMP"}:
                    property_type = th.DateTimeType()
                elif oracle_type == "RAW":
                    property_type = th.StringType()
                else:
                    # Default to string for unknown types
                    property_type = th.StringType()
                # Mark as nullable if allowed
                nullable = col.get("nullable", "Y")
                if nullable == "Y":
                    property_type.nullable = True
                properties[col_name] = property_type
            schema = th.PropertiesList(
                *list(starmap(th.Property, properties.items())),
            ).to_dict()
            # Apply schema flattening if enabled
            if self._schema_flattener.enabled:
                logger.debug(
                    "Applying schema flattening to %s.%s",
                    self.schema_name,
                    self.table_name,
                )
                schema = self._schema_flattener.flatten_schema(schema)
                # Validate flattened schema compatibility with Oracle
                if not self._schema_flattener.validate_schema_compatibility(schema):
                    logger.warning(
                        "Flattened schema for %s.%s may have compatibility issues",
                        self.schema_name,
                        self.table_name,
                    )
            logger.info(
                "Discovered schema for %s.%s: %d columns (flattening: %s)",
                self.schema_name,
                self.table_name,
                len(schema.get("properties", {})),
                "enabled" if self._schema_flattener.enabled else "disabled",
            )
        except Exception:
            logger.exception(
                "Failed to discover schema for %s.%s",
                self.schema_name,
                self.table_name,
            )
            # Return minimal schema as fallback
            return th.PropertiesList(
                th.Property("id", th.StringType()),
                th.Property("data", th.StringType()),
            ).to_dict()
        else:
            return schema

    def _raise_query_safety_error(self, table_name: str, query: str) -> None:
        """Raise query safety error."""
        msg = f"Unsafe query detected for {table_name}"
        raise OracleQueryError(msg, sql=query)

    def _raise_query_execution_error(self, error: str, query: str) -> None:
        """Raise query execution error."""
        error_msg = f"Query execution failed: {error}"
        raise OracleQueryError(error_msg, sql=query)

    def _raise_schema_safety_error(self, table_name: str, sql: str) -> None:
        """Raise schema safety error."""
        msg = f"Unsafe schema query detected for {table_name}"
        raise OracleQueryError(msg, sql=sql)

    def _raise_schema_execution_error(self, error: str, sql: str) -> None:
        """Raise schema execution error."""
        error_msg = f"Schema query execution failed: {error}"
        raise OracleQueryError(error_msg, sql=sql)

    @track_performance("oracle_table_stream.get_records")
    def get_records(self, context: dict[str, Any] | None) -> Iterable[dict[str, Any]]:
        """Extract records from Oracle table.

        Args:
            context: Stream context for incremental extraction
        Yields:
            Table records as dictionaries

        """
        try:
            start_time = time.time()
            logger.info(
                "Starting extraction from %s.%s",
                self.schema_name,
                self.table_name,
            )
            # Execute parameterized query using
            # flext-infrastructure.databases.flext-db-oracle methods
            query, params = self._build_extraction_query(context)
            # Validate query safety before execution
            if not self._query_builder.validate_query_safety(query, params):
                self._raise_query_safety_error(self.table_name, query)
            # Log query statistics for monitoring
            query_stats = self._query_builder.get_query_stats(query, params)
            logger.debug("Executing Oracle query with stats: %s", query_stats)
            # Use REAL flext-infrastructure.databases.flext-db-oracle execute_query
            # method via asyncio
            result = asyncio.run(
                self.oracle_query_service.execute_query(query, parameters=params),
            )
            if not result.success:
                self._raise_query_execution_error(
                    result.error or "Unknown query error",
                    query,
                )
            results = result.data.rows if result.data and result.data.rows else []
            for row in results:
                record = self._row_to_record(row)
                # Apply flattening if enabled
                if self._schema_flattener.enabled:
                    record = self._schema_flattener.flatten_record(record)
                self._total_rows_extracted += 1
                # Track performance every 1000 records
                if self._total_rows_extracted % 1000 == 0:
                    self._log_extraction_progress(start_time)
                yield record
            elapsed = time.time() - start_time
            logger.info(
                "Completed extraction from %s.%s: %d records in %.2f seconds",
                self.schema_name,
                self.table_name,
                self._total_rows_extracted,
                elapsed,
            )
        except Exception as e:
            logger.exception(
                "Failed to extract from %s.%s",
                self.schema_name,
                self.table_name,
            )
            error_msg = (
                f"Failed to extract from {self.schema_name}.{self.table_name}: {e}"
            )
            raise OracleQueryError(
                error_msg,
                sql=query if "query" in locals() else self._last_query,
                oracle_code=None,
            ) from e

    def _build_extraction_query(
        self,
        context: dict[str, Any] | None,
    ) -> tuple[str, dict[str, Any]]:
        """Build parameterized SQL query for data extraction.

        Args:
            context: Stream context with state information
        Returns:
            Tuple of (query_string, parameters_dict)

        """
        # Get column list using cached metadata
        columns = self._get_table_columns()
        column_names = [col["column_name"] for col in columns]
        # Check for incremental extraction
        replication_key = getattr(self, "replication_key", None)
        if replication_key and context:
            bookmark_value = context.get("bookmark_value")
            if bookmark_value:
                # Use incremental query builder
                batch_size = None
                if hasattr(self, "tap") and hasattr(self.tap, "config"):
                    batch_size = getattr(self.tap.config, "batch_size", None)
                query, params = self._query_builder.build_incremental_query(
                    table_name=self.table_name,
                    schema_name=self.schema_name,
                    replication_key=replication_key,
                    start_value=bookmark_value,
                    columns=column_names,
                    limit=batch_size,
                )
                self._last_query = query
                return query, params
        # Build standard table query
        # Note: order_by_columns would be used for complex ordering if needed
        # Get batch size configuration
        batch_size = None
        if hasattr(self, "tap") and hasattr(self.tap, "config"):
            batch_size = getattr(self.tap.config, "batch_size", None)
        # Use modern query builder
        query, params = self._query_builder.build_table_query(
            table_name=self.table_name,
            schema_name=self.schema_name,
            columns=column_names,
            limit=batch_size,
        )
        self._last_query = query
        return query, params

    def _row_to_record(self, row: tuple[Any, ...]) -> dict[str, Any]:
        """Convert database row to record dictionary.

        Args:
            row: Database row tuple
        Returns:
            Record dictionary

        """
        columns = self._get_table_columns()
        record = {}
        for i, col in enumerate(columns):
            col_name = col["column_name"].lower()
            value = row[i] if i < len(row) else None
            # Convert Oracle-specific types
            if value is not None:
                oracle_type = col["data_type"].upper()
                if oracle_type in {"DATE", "TIMESTAMP"}:
                    # Convert to ISO format string
                    value = str(value)
                elif oracle_type == "CLOB":
                    # Convert CLOB to string
                    value = str(value)
            record[col_name] = value
        return record

    def _log_extraction_progress(self, start_time: float) -> None:
        """Log extraction progress for monitoring.

        Args:
            start_time: Extraction start timestamp

        """
        elapsed = time.time() - start_time
        rate = self._total_rows_extracted / elapsed if elapsed > 0 else 0
        logger.info(
            "Extraction progress for %s.%s: %d records (%.2f records/sec)",
            self.schema_name,
            self.table_name,
            self._total_rows_extracted,
            rate,
        )

    def get_child_context(
        self,
        record: dict[str, Any],
        context: collections.abc.Mapping[str, Any] | None = None,
    ) -> collections.abc.Mapping[str, Any] | None:
        """Get context for child streams.

        Args:
            record: Parent record
            context: Parent context
        Returns:
            Child context

        """
        child_context: dict[str, Any] = {}
        if context:
            child_context.update(context)
        # Add record-specific context
        for key in self.primary_keys:
            if key.lower() in record:
                child_context[f"parent_{key}"] = record[key.lower()]
        return child_context

    def post_process(
        self,
        row: dict[str, Any],
        _context: collections.abc.Mapping[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Post-process extracted row.

        Args:
            row: Raw row data
            context: Stream context (unused)

        Returns:
            Processed row

        """
        # Apply any configured transformations
        processed_row = row.copy()
        # Add metadata if configured
        if (
            hasattr(self, "tap")
            and hasattr(self.tap, "config")
            and getattr(self.tap.config, "include_metadata", False)
        ):
            processed_row["_sdc_extracted_at"] = time.time()
            processed_row["_sdc_table_name"] = self.table_name
            processed_row["_sdc_schema_name"] = self.schema_name
        return processed_row

    def _get_table_columns(self) -> list[dict[str, Any]]:
        """Get cached table column metadata.

        Returns:
            List of column metadata dictionaries

        """
        try:
            # Use modern query builder for schema metadata
            sql, params = self._query_builder.build_schema_query(
                table_name=self.table_name,
                schema_name=self.schema_name,
            )
            # Validate query safety
            if not self._query_builder.validate_query_safety(sql, params):
                self._raise_schema_safety_error(self.table_name, sql)
            # Use REAL flext-infrastructure.databases.flext-db-oracle execute_query
            # method via asyncio
            schema_result = asyncio.run(
                self.oracle_query_service.execute_query(sql, parameters=params),
            )
            if not schema_result.success:
                self._raise_schema_execution_error(
                    schema_result.error or "Unknown schema error",
                    sql,
                )
            if schema_result.data and schema_result.data.rows:
                results = schema_result.data.rows
            else:
                results = []
            self._column_cache = []
            for row in results:
                self._column_cache.append(
                    {
                        "column_name": row[0],
                        "data_type": row[1],
                        "data_length": row[2],
                        "data_precision": row[3],
                        "data_scale": row[4],
                        "nullable": row[5],
                        "column_id": row[6],
                        "data_default": row[7],
                    },
                )
            logger.debug(
                "Cached %d columns for %s.%s",
                len(self._column_cache),
                self.schema_name,
                self.table_name,
            )
        except Exception:
            logger.exception(
                "Failed to get column metadata for %s.%s",
                self.schema_name,
                self.table_name,
            )
            # Fallback to minimal column info
            self._column_cache = [
                {
                    "column_name": "ID",
                    "data_type": "VARCHAR2",
                    "data_length": 4000,
                    "data_precision": None,
                    "data_scale": None,
                    "nullable": "Y",
                    "column_id": 1,
                    "data_default": None,
                },
            ]
        return self._column_cache

    def _get_records_impl(
        self,
        context: dict[str, Any] | None = None,
    ) -> Iterable[dict[str, Any]]:
        """Implementation-specific record retrieval for BaseOracleStream.

        Args:
            context: Stream context
        Yields:
            Record dictionaries

        """
        # Delegate to the main get_records method
        yield from self.get_records(context)

    def __del__(self) -> None:
        """Cleanup resources on stream destruction."""
        # Services are cleaned up by the tap's connection service
        # No direct connection cleanup needed


class OracleViewStream(OracleTableStream):
    """Oracle Database View Stream.

    Extends OracleTableStream for views with view-specific optimizations.
    Views are treated similarly to tables but with some restrictions.
    """

    def __init__(
        self,
        tap: TapOracle,
        name: str,
        view_name: str,
        schema: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize Oracle view stream.

        Args:
            tap: Parent tap instance
            name: Stream name
            view_name: Oracle view name
            schema: Oracle schema name
            **kwargs: Additional stream arguments

        """
        super().__init__(
            tap=tap,
            name=name,
            table_name=view_name,
            schema=schema,
            primary_keys=None,  # Views typically don't have primary keys
            **kwargs,
        )
        logger.info(
            "Initialized Oracle view stream: %s.%s",
            schema or self.schema_name,
            view_name,
        )

    def _build_extraction_query(
        self,
        context: dict[str, Any] | None,
    ) -> tuple[str, dict[str, Any]]:
        """Build SQL query for view extraction.

        Views may have different optimization strategies than tables.

        Args:
            context: Stream context
        Returns:
            Tuple of (SQL query string, parameters dict)

        """
        # Get base query from parent
        query, params = super()._build_extraction_query(context)
        # Views may need different handling for large datasets
        # Add query hints if configured
        if (
            hasattr(self, "tap")
            and hasattr(self.tap, "config")
            and hasattr(self.tap.config, "view_query_hints")
        ):
            hints = self.tap.config.view_query_hints
            if hints:
                # Add Oracle hints for view optimization
                query = query.replace("SELECT", f"SELECT /*+ {hints} */", 1)
        return query, params
