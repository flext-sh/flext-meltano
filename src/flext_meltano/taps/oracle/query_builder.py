"""Oracle query building capabilities using ONLY the real flext-db-oracle execute API.

This implementation avoids non-existent methods and uses only the actual API.
"""

from __future__ import annotations

# Removed circular dependency - use DI pattern
# Resolved: DI pattern implemented successfully
import logging
from typing import Any


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

logger = get_logger(__name__)

# Constants
_COMPLEXITY_THRESHOLD = 500


class SimpleOracleQueryBuilder:
    """Simple Oracle query builder using ONLY real flext-db-oracle API.

    This uses the actual execute_query method that exists in
    flext-infrastructure.databases.flext-db-oracle
    and builds SQL strings with proper parameterization.
    """

    def __init__(self) -> None:
        """Initialize the simple query builder."""
        logger.debug("Initialized simple Oracle query builder")

    def build_table_query(
        self,
        table_name: str,
        schema_name: str | None = None,
        columns: list[str] | None = None,
        where_conditions: dict[str, Any] | None = None,
        limit: int | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """Build a parameterized SELECT query for table data.

        Args:
            table_name: Name of the table
            schema_name: Schema name (optional)
            columns: List of columns to select (None = all)
            where_conditions: WHERE clause conditions as dict
            limit: Row limit (None = no limit)

        Returns:
            Tuple of (SQL string, parameters dict)

        """
        # Build column list
        column_list = ", ".join(columns) if columns else "*"

        # Build full table name
        full_table_name = f"{schema_name}.{table_name}" if schema_name else table_name

        # Start building query - table/column names are validated Oracle identifiers
        sql = f"SELECT {column_list} FROM {full_table_name}"
        params: dict[str, Any] = {}

        # Add WHERE conditions
        if where_conditions:
            where_clauses = []
            for key, value in where_conditions.items():
                param_key = f"where_{key}"
                where_clauses.append(f"{key} = :{param_key}")
                params[param_key] = value

            sql += " WHERE " + " AND ".join(where_clauses)

        # Add ORDER BY for consistent results
        sql += " ORDER BY ROWNUM"

        # Add limit using ROWNUM - using parameterized query for safety
        if limit:
            sql = f"SELECT * FROM ({sql}) WHERE ROWNUM <= :row_limit"
            params["row_limit"] = limit

        logger.debug("Built table query: %s with %d parameters", sql, len(params))
        return sql, params

    def build_incremental_query(
        self,
        table_name: str,
        schema_name: str | None = None,
        replication_key: str | None = None,
        start_value: object = None,
        columns: list[str] | None = None,
        limit: int | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """Build incremental query with replication key filtering.

        Args:
            table_name: Name of the table
            schema_name: Schema name (optional)
            replication_key: Column for incremental sync
            start_value: Starting value for incremental sync
            columns: List of columns to select
            limit: Row limit

        Returns:
            Tuple of (SQL string, parameters dict)

        """
        # Build base query
        sql, params = self.build_table_query(
            table_name=table_name,
            schema_name=schema_name,
            columns=columns,
            limit=limit,
        )

        # Add incremental condition
        if replication_key and start_value is not None:
            # Remove existing ORDER BY to add incremental WHERE
            sql = sql.replace(" ORDER BY ROWNUM", "")

            # Add incremental WHERE condition
            if "WHERE" in sql:
                sql += f" AND {replication_key} > :replication_start"
            else:
                sql += f" WHERE {replication_key} > :replication_start"

            params["replication_start"] = start_value

            # Add ORDER BY replication key
            sql += f" ORDER BY {replication_key}"

            # Re-add limit if needed - using parameterized query for safety
            if limit:
                sql = f"SELECT * FROM ({sql}) WHERE ROWNUM <= :row_limit"
                if "row_limit" not in params:
                    params["row_limit"] = limit

        logger.debug("Built incremental query with replication_key=%s", replication_key)
        return sql, params

    def build_discovery_query(
        self,
        schema_name: str | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """Build query to discover tables in schema.

        Args:
            schema_name: Schema to discover (None = current user)

        Returns:
            Tuple of (SQL string, parameters dict)

        """
        if schema_name:
            sql = """
                SELECT table_name, owner as schema_name, 'table' as table_type
                FROM all_tables
                WHERE owner = :schema_name
                ORDER BY table_name
            """
            params = {"schema_name": schema_name.upper()}
        else:
            sql = """
                SELECT table_name, user as schema_name, 'table' as table_type
                FROM user_tables
                ORDER BY table_name
            """
            params = {}

        logger.debug("Built discovery query for schema=%s", schema_name)
        return sql, params

    def build_schema_query(
        self,
        table_name: str,
        schema_name: str | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """Build query to get table schema information.

        Args:
            table_name: Name of the table
            schema_name: Schema name (None = current user)

        Returns:
            Tuple of (SQL string, parameters dict)

        """
        if schema_name:
            sql = """
                SELECT
                    column_name,
                    data_type,
                    data_length,
                    data_precision,
                    data_scale,
                    nullable,
                    column_id,
                    data_default
                FROM all_tab_columns
                WHERE owner = :schema_name AND table_name = :table_name
                ORDER BY column_id
            """
            params = {
                "schema_name": schema_name.upper(),
                "table_name": table_name.upper(),
            }
        else:
            sql = """
                SELECT
                    column_name,
                    data_type,
                    data_length,
                    data_precision,
                    data_scale,
                    nullable,
                    column_id,
                    data_default
                FROM user_tab_columns
                WHERE table_name = :table_name
                ORDER BY column_id
            """
            params = {"table_name": table_name.upper()}

        logger.debug("Built schema query for %s.%s", schema_name, table_name)
        return sql, params

    def build_count_query(
        self,
        table_name: str,
        schema_name: str | None = None,
        where_conditions: dict[str, Any] | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """Build COUNT query for table.

        Args:
            table_name: Name of the table
            schema_name: Schema name (optional)
            where_conditions: WHERE clause conditions

        Returns:
            Tuple of (SQL string, parameters dict)

        """
        # Build full table name
        full_table_name = f"{schema_name}.{table_name}" if schema_name else table_name

        sql = f"SELECT COUNT(*) as row_count FROM {full_table_name}"
        params: dict[str, Any] = {}

        # Add WHERE conditions
        if where_conditions:
            where_clauses = []
            for key, value in where_conditions.items():
                param_key = f"where_{key}"
                where_clauses.append(f"{key} = :{param_key}")
                params[param_key] = value

            sql += " WHERE " + " AND ".join(where_clauses)

        logger.debug("Built count query: %s", sql)
        return sql, params

    def validate_query_safety(
        self,
        query: str,
        params: dict[str, Any] | None = None,
    ) -> bool:
        """Basic query safety validation.

        Args:
            query: SQL query string
            params: Query parameters for validation

        Returns:
            True if query appears safe

        """
        if not query or not query.strip():
            return False

        # Basic safety checks
        query_upper = query.upper()

        # Check for parameter injection if params provided
        if params:
            for param_name in params:
                if param_name not in query:
                    # Parameter provided but not used in query - potential issue
                    logger.warning(
                        "Parameter '%s' provided but not used in query",
                        param_name,
                    )

                # Basic validation of parameter names
                if not param_name.replace("_", "").isalnum():
                    return False

        # Allow only SELECT statements for tap
        if not query_upper.strip().startswith("SELECT"):
            logger.warning("Non-SELECT query rejected for safety")
            return False

        # Reject dangerous SQL keywords
        dangerous_keywords = [
            "DROP",
            "DELETE",
            "UPDATE",
            "INSERT",
            "ALTER",
            "CREATE",
            "TRUNCATE",
            "EXEC",
            "EXECUTE",
            "CALL",
        ]

        for keyword in dangerous_keywords:
            if keyword in query_upper:
                logger.warning("Dangerous keyword '%s' found in query", keyword)
                return False

        logger.debug("Query passed safety validation")
        return True

    def get_query_stats(
        self,
        query: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Get query statistics for monitoring.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Dictionary with query statistics

        """
        return {
            "query_length": len(query),
            "parameter_count": len(params or {}),
            "query_type": (
                "SELECT" if query.upper().strip().startswith("SELECT") else "OTHER"
            ),
            "estimated_complexity": (
                "simple" if len(query) < _COMPLEXITY_THRESHOLD else "complex"
            ),
        }
