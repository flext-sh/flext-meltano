"""In-Memory DBT Executor for FLEXT Ecosystem.

Provides DuckDB-based in-memory execution for DBT models without
requiring external database connections.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import duckdb
import pandas as pd  # type: ignore[import-untyped]
from flext_core import FlextResult, get_logger

if TYPE_CHECKING:
    from pathlib import Path

logger = get_logger(__name__)


class FlextDbtInMemoryExecutor:
    """Executes DBT models in-memory using DuckDB.

    Enables testing and validation of DBT transformations without
    requiring external database connections.
    """

    def __init__(self, database: str = ":memory:") -> None:
        """Initialize in-memory executor.

        Args:
            database: DuckDB database path (default: in-memory)

        """
        self.database = database
        self.connection = duckdb.connect(database)
        self.schemas: dict[str, dict[str, Any]] = {}
        self.mock_data: dict[str, pd.DataFrame] = {}
        logger.info(f"Initialized DuckDB executor: {database}")

    def load_mock_data(
        self, schema: dict[str, Any],
    ) -> FlextResult[None]:
        """Load mock data based on schema definition.

        Args:
            schema: Schema definition with table structures

        Returns:
            FlextResult indicating success or failure

        """
        try:
            for table_name, table_def in schema.items():
                # Create table structure
                columns = table_def.get("columns", {})
                if columns:
                    # Build CREATE TABLE statement
                    col_defs = []
                    for col_name, col_type in columns.items():
                        duckdb_type = self._map_to_duckdb_type(col_type)
                        col_defs.append(f"{col_name} {duckdb_type}")

                    create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(col_defs)})"
                    self.connection.execute(create_sql)

                    # Load sample data if provided
                    sample_data = table_def.get("sample_data", [])
                    if sample_data:
                        df = pd.DataFrame(sample_data)
                        self.connection.register(f"temp_{table_name}", df)
                        # Safe table names for internal DuckDB operations
                        self.connection.execute(
                            f"INSERT INTO {table_name} SELECT * FROM {f'temp_{table_name}'}",  # noqa: S608
                        )
                        self.connection.unregister(f"temp_{table_name}")

                    self.schemas[table_name] = table_def
                    logger.debug(f"Loaded schema for table: {table_name}")

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to load mock data: {e}")

    def _map_to_duckdb_type(self, type_str: str) -> str:
        """Map generic types to DuckDB types.

        Args:
            type_str: Generic type string

        Returns:
            DuckDB type string

        """
        type_mapping = {
            "string": "VARCHAR",
            "text": "VARCHAR",
            "integer": "INTEGER",
            "int": "INTEGER",
            "bigint": "BIGINT",
            "float": "FLOAT",
            "double": "DOUBLE",
            "decimal": "DECIMAL",
            "boolean": "BOOLEAN",
            "bool": "BOOLEAN",
            "date": "DATE",
            "datetime": "TIMESTAMP",
            "timestamp": "TIMESTAMP",
            "json": "JSON",
            "array": "VARCHAR[]",
        }
        return type_mapping.get(type_str.lower(), "VARCHAR")

    def execute_model(
        self, model_sql: str, data: dict[str, pd.DataFrame] | None = None,
    ) -> FlextResult[pd.DataFrame]:
        """Execute a DBT model in-memory.

        Args:
            model_sql: SQL to execute
            data: Optional DataFrames to register before execution

        Returns:
            FlextResult with resulting DataFrame

        """
        try:
            # Register any provided DataFrames
            if data:
                for name, df in data.items():
                    self.connection.register(name, df)

            # Execute the model
            result = self.connection.execute(model_sql).fetchdf()

            # Unregister temporary DataFrames
            if data:
                for name in data:
                    self.connection.unregister(name)

            logger.debug(f"Executed model, returned {len(result)} rows")
            return FlextResult.ok(result)

        except Exception as e:
            return FlextResult.fail(f"Failed to execute model: {e}")

    def validate_transformations(
        self, models: list[dict[str, Any]],
    ) -> FlextResult[dict[str, Any]]:
        """Validate a series of transformations.

        Args:
            models: List of models to validate

        Returns:
            FlextResult with validation results

        """
        try:
            results = {}

            for model in models:
                model_name = model.get("name", "unknown")
                model_sql = model.get("sql", "")
                expected = model.get("expected", {})

                # Execute the model
                exec_result = self.execute_model(model_sql)

                if exec_result.success:
                    df = exec_result.data

                    # Validate results
                    validations = {}

                    # Ensure df is a DataFrame
                    if not isinstance(df, pd.DataFrame):
                        validations["dataframe_type"] = {
                            "expected": "DataFrame",
                            "actual": type(df).__name__,
                            "passed": False,
                        }
                    else:
                        # Check row count
                        if "row_count" in expected:
                            actual_count = len(df)
                            expected_count = expected["row_count"]
                            validations["row_count"] = {
                                "expected": expected_count,
                                "actual": actual_count,
                                "passed": actual_count == expected_count,
                            }

                        # Check columns
                        if "columns" in expected:
                            actual_columns = set(df.columns)
                            expected_columns = set(expected["columns"])
                            validations["columns"] = {
                                "expected": list(expected_columns),
                                "actual": list(actual_columns),
                                "passed": actual_columns == expected_columns,
                            }

                        # Check specific values
                        if "values" in expected:
                            for check in expected["values"]:
                                column = check.get("column")
                                value = check.get("value")
                                if column and column in df.columns:
                                    matches = df[column].eq(value).any()
                                    validations[f"value_{column}"] = {
                                        "expected": value,
                                        "found": matches,
                                        "passed": matches,
                                    }

                    results[model_name] = {
                        "success": True,
                        "validations": validations,
                        "all_passed": all(
                            v.get("passed", False) for v in validations.values()
                        ),
                    }
                else:
                    results[model_name] = {
                        "success": False,
                        "error": exec_result.error,
                    }

            # Summary
            total_models = len(models)
            successful = sum(1 for r in results.values() if r["success"])
            all_valid = all(
                r.get("all_passed", False) for r in results.values() if r["success"]
            )

            summary = {
                "total_models": total_models,
                "successful": successful,
                "failed": total_models - successful,
                "all_validations_passed": all_valid,
                "results": results,
            }

            logger.info(
                f"Validation complete: {successful}/{total_models} models successful, "
                f"all valid: {all_valid}",
            )

            return FlextResult.ok(summary)

        except Exception as e:
            return FlextResult.fail(f"Failed to validate transformations: {e}")

    def create_test_data(
        self, table_name: str, rows: int = 100,
    ) -> FlextResult[pd.DataFrame]:
        """Create test data for a table.

        Args:
            table_name: Table to create test data for
            rows: Number of rows to generate

        Returns:
            FlextResult with generated DataFrame

        """
        try:
            if table_name not in self.schemas:
                return FlextResult.fail(f"Schema not found for table: {table_name}")

            schema = self.schemas[table_name]
            columns = schema.get("columns", {})

            # Generate test data
            data: dict[str, list[Any]] = {}
            for col_name, col_type in columns.items():
                if "int" in col_type.lower():
                    data[col_name] = list(range(1, rows + 1))
                elif "float" in col_type.lower() or "double" in col_type.lower():
                    data[col_name] = [float(i) * 1.1 for i in range(rows)]
                elif "bool" in col_type.lower():
                    data[col_name] = [i % 2 == 0 for i in range(rows)]
                elif "date" in col_type.lower():
                    base_date = pd.Timestamp("2024-01-01")
                    data[col_name] = [
                        base_date + pd.Timedelta(days=i) for i in range(rows)
                    ]
                else:  # Default to string
                    data[col_name] = [f"{col_name}_{i}" for i in range(rows)]

            df = pd.DataFrame(data)
            self.mock_data[table_name] = df

            logger.debug(f"Generated {rows} rows of test data for {table_name}")
            return FlextResult.ok(df)

        except Exception as e:
            return FlextResult.fail(f"Failed to create test data: {e}")

    def export_results(
        self, query: str, path: Path, file_format: str = "csv",
    ) -> FlextResult[None]:
        """Export query results to file.

        Args:
            query: SQL query to execute
            path: Output file path
            file_format: Export format (csv, parquet, json)

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Execute query
            result = self.connection.execute(query).fetchdf()

            # Export based on format
            if file_format == "csv":
                result.to_csv(path, index=False)
            elif file_format == "parquet":
                result.to_parquet(path)
            elif file_format == "json":
                result.to_json(path, orient="records", indent=2)
            else:
                return FlextResult.fail(f"Unsupported format: {file_format}")

            logger.info(f"Exported {len(result)} rows to {path} as {file_format}")
            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to export results: {e}")

    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            logger.debug("Closed DuckDB connection")


def create_in_memory_executor(
    database: str = ":memory:",
) -> FlextDbtInMemoryExecutor:
    """Create a new in-memory executor instance.

    Args:
        database: DuckDB database path (default: in-memory)

    Returns:
        FlextDbtInMemoryExecutor instance

    """
    return FlextDbtInMemoryExecutor(database)
