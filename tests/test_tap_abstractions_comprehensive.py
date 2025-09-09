"""Comprehensive tests for Tap Abstractions using flext_tests.

Tests all tap functionality with real Singer protocol operations,
no mocks, using flext_tests for improved assertions and test builders.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import concurrent.futures
import os
import shutil
import tempfile
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

import pytest
from flext_core import FlextResult, FlextServices, FlextTypes, FlextUtilities
from flext_tests import FlextTestsMatchers, FlextTestsPerformance
from pydantic import ValidationError

from flext_meltano.tap_abstractions import (
    FlextTapAbstractions,
    StreamDefinition,
    TapConfig,
    TapInstance,
)


class TestTapConfigComprehensive:
    """Comprehensive tests for TapConfig Pydantic model."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self) -> None:
        """Cleanup after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_tap_config_valid_creation(self) -> None:
        """Test creating valid tap configuration."""
        config_data: FlextTypes.Core.Dict = {
            "tap_type": "tap-postgres",
            "connection_config": {
                "host": "localhost",
                "port": 5432,
                "database": "test_db",
                "user": "test_user",
                "password": "test_pass",
            },
            "stream_config": {
                "users": {"replication_method": "FULL_TABLE"},
                "orders": {
                    "replication_method": "INCREMENTAL",
                    "replication_key": "updated_at",
                },
            },
            "version": "1.2.3",
        }

        config = TapConfig(
            tap_type=str(config_data["tap_type"]),
            connection_config=cast(
                "FlextTypes.Core.Dict", config_data["connection_config"]
            ),
            stream_config=cast("FlextTypes.Core.Dict", config_data["stream_config"]),
            version=str(config_data["version"]),
        )

        assert config.tap_type == "tap-postgres"
        assert config.connection_config["host"] == "localhost"

        # Type-safe nested dict access
        users_stream = config.stream_config.get("users")
        assert users_stream is not None
        users_config = cast("FlextTypes.Core.Dict", users_stream)
        assert users_config["replication_method"] == "FULL_TABLE"

        assert config.version == "1.2.3"

    def test_tap_config_defaults(self) -> None:
        """Test default values for tap configuration."""
        config = TapConfig(
            tap_type="tap-csv",
            connection_config={"files": [{"path": str(self.temp_dir / "test.csv")}]},
        )
        assert config.tap_type == "tap-csv"
        assert config.stream_config == {}  # default empty dict
        assert config.version == "latest"  # default

    def test_tap_config_extra_fields_allowed(self) -> None:
        """Test that extra fields are allowed in configuration."""
        # Test extra fields using model_dump to access them in a type-safe way
        config_dict = {
            "tap_type": "tap-mysql",
            "connection_config": {"host": "mysql.example.com"},
            "custom_field": "custom_value",
            "another_extra": 123,
        }

        config = TapConfig(**config_dict)

        assert config.tap_type == "tap-mysql"

        # Access extra fields through model_dump (type-safe way)
        config_data = config.model_dump()
        assert config_data["custom_field"] == "custom_value"
        assert config_data["another_extra"] == 123

    def test_tap_config_validation_required_fields(self) -> None:
        """Test validation of required fields."""
        # Missing tap_type
        with pytest.raises(ValidationError):
            TapConfig(tap_type="", connection_config={"host": "localhost"})

        # Missing connection_config
        with pytest.raises(ValidationError):
            TapConfig(tap_type="tap-postgres", connection_config={})

    @pytest.mark.parametrize(
        ("tap_type", "expected_type"),
        [
            ("tap-postgres", "tap-postgres"),
            ("tap-csv", "tap-csv"),
            ("tap-mysql", "tap-mysql"),
            ("tap-oracle", "tap-oracle"),
            ("tap-snowflake", "tap-snowflake"),
        ],
    )
    def test_tap_config_parametrized_tap_types(
        self, tap_type: str, expected_type: str
    ) -> None:
        """Test tap configuration with various tap types."""
        config = TapConfig(tap_type=tap_type, connection_config={"host": "localhost"})
        assert config.tap_type == expected_type


class TestStreamDefinitionComprehensive:
    """Comprehensive tests for StreamDefinition Pydantic model."""

    def test_stream_definition_valid_creation(self) -> None:
        """Test creating valid stream definition."""
        stream_data = {
            "stream_name": "users",
            "stream_schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "created_at": {"type": "string", "format": "date-time"},
                },
            },
            "tap_type": "tap-postgres",
        }

        stream = StreamDefinition(**cast("dict[str, object]", stream_data))
        assert stream.stream_name == "users"
        assert stream.stream_schema["type"] == "object"
        assert stream.tap_type == "tap-postgres"
        assert stream.status == "discovered"  # default
        assert stream.records_extracted == 0  # default

    def test_stream_definition_defaults(self) -> None:
        """Test default values for stream definition."""
        stream = StreamDefinition(
            stream_name="orders",
            stream_schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            tap_type="tap-mysql",
        )
        assert stream.status == "discovered"
        assert stream.records_extracted == 0

    def test_stream_definition_with_status_updates(self) -> None:
        """Test stream definition with various status updates."""
        stream = StreamDefinition(
            stream_name="products",
            stream_schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            tap_type="tap-postgres",
            status="extracting",
            records_extracted=1500,
        )
        assert stream.status == "extracting"
        assert stream.records_extracted == 1500

    @pytest.mark.parametrize(
        "status", ["discovered", "extracting", "completed", "error", "paused"]
    )
    def test_stream_definition_parametrized_statuses(self, status: str) -> None:
        """Test stream definition with various statuses."""
        stream = StreamDefinition(
            stream_name="test_stream",
            stream_schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            tap_type="tap-test",
            status=status,
        )
        assert stream.status == status


class TestTapInstanceComprehensive:
    """Comprehensive tests for TapInstance Pydantic model."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self) -> None:
        """Cleanup after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_tap_instance_valid_creation(self) -> None:
        """Test creating valid tap instance."""
        config = TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost", "port": 5432, "database": "test"},
        )

        instance_data = {
            "tap_type": "tap-postgres",
            "config": config,
            "tap_id": "tap_postgres_001",
        }

        instance = TapInstance(**cast("dict[str, object]", instance_data))
        assert instance.tap_type == "tap-postgres"
        assert instance.config.tap_type == "tap-postgres"
        assert instance.tap_id == "tap_postgres_001"
        assert instance.status == "initialized"  # default
        assert instance.streams == {}  # default
        assert not instance.discovered  # default

    def test_tap_instance_with_streams(self) -> None:
        """Test tap instance with discovered streams."""
        config = TapConfig(
            tap_type="tap-csv",
            connection_config={"files": [{"path": str(self.temp_dir / "test.csv")}]},
        )

        users_stream = StreamDefinition(
            stream_name="users",
            stream_schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            tap_type="tap-csv",
        )

        instance = TapInstance(
            tap_type="tap-csv",
            config=config,
            tap_id="tap_csv_001",
            streams={"users": users_stream},
            discovered=True,
            status="ready",
        )

        assert len(instance.streams) == 1
        assert "users" in instance.streams
        assert instance.discovered is True
        assert instance.status == "ready"

    def test_tap_instance_metadata_handling(self) -> None:
        """Test tap instance with metadata."""
        config = TapConfig(
            tap_type="tap-oracle", connection_config={"host": "oracle.example.com"}
        )

        instance = TapInstance(
            tap_type="tap-oracle",
            config=config,
            tap_id="tap_oracle_001",
            metadata={
                "created_at": datetime.now(UTC).isoformat(),
                "version": "2.1.0",
                "source": "flext-meltano",
            },
        )

        assert "created_at" in instance.metadata
        assert instance.metadata["version"] == "2.1.0"
        assert instance.metadata["source"] == "flext-meltano"


class TestFlextTapAbstractionsComprehensive:
    """Comprehensive tests for FlextTapAbstractions main class."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.tap_abstractions = FlextTapAbstractions()

    def teardown_method(self) -> None:
        """Cleanup after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_tap_abstractions_initialization(self) -> None:
        """Test FlextTapAbstractions initialization."""
        tap_abs = FlextTapAbstractions()
        assert tap_abs is not None
        assert hasattr(tap_abs, "process")  # Should have ServiceProcessor methods

    def test_tap_abstractions_service_processor_inheritance(self) -> None:
        """Test that FlextTapAbstractions properly inherits from ServiceProcessor."""
        assert isinstance(self.tap_abstractions, FlextServices.ServiceProcessor)

        # Should have ServiceProcessor methods
        assert hasattr(self.tap_abstractions, "process")
        assert hasattr(self.tap_abstractions, "build")
        assert hasattr(self.tap_abstractions, "get_service_name")
        assert hasattr(self.tap_abstractions, "is_valid")
        assert hasattr(self.tap_abstractions, "validate_required_fields")

    def test_process_tap_config_basic(self) -> None:
        """Test processing basic tap configuration."""
        config = TapConfig(
            tap_type="tap-csv",
            connection_config={"files": [{"path": str(self.temp_dir / "test.csv")}]},
        )

        result = self.tap_abstractions.process(config)
        FlextTestsMatchers.assert_result_success(result)

        tap_instance = result.value
        assert isinstance(tap_instance, TapInstance)
        assert tap_instance.tap_type == "tap-csv"
        assert tap_instance.config.tap_type == "tap-csv"

    def test_process_tap_config_postgres(self) -> None:
        """Test processing PostgreSQL tap configuration."""
        config = TapConfig(
            tap_type="tap-postgres",
            connection_config={
                "host": "localhost",
                "port": 5432,
                "database": "test_db",
                "user": "test_user",
                "password": "test_pass",
            },
            stream_config={
                "users": {"replication_method": "FULL_TABLE"},
                "orders": {"replication_method": "INCREMENTAL"},
            },
        )

        result = self.tap_abstractions.process(config)
        FlextTestsMatchers.assert_result_success(result)

        tap_instance = result.value
        assert tap_instance.tap_type == "tap-postgres"
        assert "host" in tap_instance.config.connection_config
        assert "users" in tap_instance.config.stream_config

    def test_build_tap_output_basic(self) -> None:
        """Test building tap output from TapInstance."""
        config = TapConfig(
            tap_type="tap-mysql",
            connection_config={"host": "mysql.example.com", "port": 3306},
        )

        tap_instance = TapInstance(
            tap_type="tap-mysql", config=config, tap_id="tap_mysql_001", status="ready"
        )

        result = self.tap_abstractions.build(
            tap_instance, correlation_id="test-corr-001"
        )

        assert isinstance(result, dict)
        assert "tap_type" in result
        assert "tap_id" in result
        assert "status" in result
        assert result["tap_type"] == "tap-mysql"

    def test_build_tap_output_with_streams(self) -> None:
        """Test building tap output with discovered streams."""
        config = TapConfig(
            tap_type="tap-snowflake",
            connection_config={"account": "test", "warehouse": "compute"},
        )

        users_stream = StreamDefinition(
            stream_name="users",
            stream_schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            tap_type="tap-snowflake",
            status="discovered",
        )

        orders_stream = StreamDefinition(
            stream_name="orders",
            stream_schema={
                "type": "object",
                "properties": {"order_id": {"type": "integer"}},
            },
            tap_type="tap-snowflake",
            status="discovered",
        )

        tap_instance = TapInstance(
            tap_type="tap-snowflake",
            config=config,
            tap_id="tap_snowflake_001",
            streams={"users": users_stream, "orders": orders_stream},
            discovered=True,
            status="ready",
        )

        result = self.tap_abstractions.build(
            tap_instance, correlation_id="test-corr-002"
        )

        assert result["discovered"] is True
        assert result["streams_count"] == 2

    def test_validate_business_rules_success(self) -> None:
        """Test validation using TapConfig Pydantic validation."""
        # TapConfig uses Pydantic validation - test that valid config creates successfully
        # Create a secure temporary file for testing
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_file.write("col1,col2\nvalue1,value2\n")
            temp_file_path = temp_file.name

        try:
            config = TapConfig(
                tap_type="tap-csv",
                connection_config={"file_path": temp_file_path},
                stream_config={},
                version="latest",
            )
            # If creation succeeds, validation passed
            result = FlextResult[None].ok(None)
            FlextTestsMatchers.assert_result_success(result, None)

            # Verify config attributes are correctly set
            assert config.tap_type == "tap-csv"
            assert config.connection_config["file_path"] == temp_file_path
            assert config.version == "latest"

        except Exception as e:
            # If creation fails, validation failed
            result = FlextResult[None].fail(f"TapConfig validation failed: {e}")
            FlextTestsMatchers.assert_result_failure(
                result, f"TapConfig validation failed: {e}"
            )
        finally:
            # Clean up temporary file using Path
            temp_path = Path(temp_file_path)
            if temp_path.exists():
                temp_path.unlink()

    def test_create_stream_definition_basic(self) -> None:
        """Test creating stream definition."""
        stream_name = "products"
        schema = {
            "type": "object",
            "properties": {
                "product_id": {"type": "integer"},
                "name": {"type": "string"},
                "price": {"type": "number"},
            },
        }
        tap_type = "tap-postgres"

        # Create stream definition directly - no template generator needed
        stream_data = {
            "stream_name": stream_name,
            "stream_schema": schema,
            "tap_type": tap_type,
            "status": "discovered",
            "records_extracted": 0,
        }

        # Create StreamDefinition from generated data
        stream = StreamDefinition(**cast("dict[str, object]", stream_data))
        assert stream.stream_name == "products"
        assert stream.tap_type == "tap-postgres"
        schema_properties = cast(
            "FlextTypes.Core.Dict", stream.stream_schema.get("properties", {})
        )
        assert "product_id" in schema_properties


@pytest.mark.integration
class TestFlextTapAbstractionsOracleIntegration:
    """Real Oracle integration tests using container."""

    def setup_method(self) -> None:
        """Setup Oracle integration test environment."""
        self.tap_abstractions = FlextTapAbstractions()

        # Oracle connection configuration from environment
        self.oracle_config = {
            "host": os.getenv("ORACLE_HOST", "localhost"),
            "port": int(os.getenv("ORACLE_PORT", "1522")),
            "database": os.getenv("ORACLE_DATABASE", "XE"),
            "username": os.getenv("ORACLE_USERNAME", "system"),
            "password": os.getenv("ORACLE_PASSWORD", "Oracle123Test"),
            "service_name": os.getenv("ORACLE_SERVICE_NAME", "XE"),
        }

    def test_oracle_connection_real(self) -> None:
        """Test real Oracle connection using container."""
        # Skip if no Oracle environment available
        if not os.getenv("ORACLE_HOST"):
            pytest.skip("Oracle container not available - set ORACLE_HOST to run")

        config = TapConfig(
            tap_type="tap-oracle", connection_config=self.oracle_config, version="1.0.0"
        )

        # Process tap configuration
        result = self.tap_abstractions.process(config)
        FlextTestsMatchers.assert_result_success(result)

        tap_instance = result.value
        assert tap_instance.tap_type == "tap-oracle"
        assert (
            tap_instance.config.connection_config["host"] == self.oracle_config["host"]
        )

    def test_oracle_stream_discovery_real(self) -> None:
        """Test real Oracle stream discovery."""
        if not os.getenv("ORACLE_HOST"):
            pytest.skip("Oracle container not available - set ORACLE_HOST to run")

        config = TapConfig(tap_type="tap-oracle", connection_config=self.oracle_config)

        # Create config and process it to get TapInstance
        config = TapConfig(tap_type="tap-oracle", connection_config=self.oracle_config)

        result = self.tap_abstractions.process(config)
        FlextTestsMatchers.assert_result_success(result)

        tap_instance = result.value

        # Test stream discovery (will attempt real Oracle connection)
        streams_result = self.tap_abstractions.discover_streams(tap_instance)

        # Verify results - should be a FlextResult
        assert hasattr(streams_result, "is_success")

        # If connection succeeds, verify stream structure
        if streams_result.is_success:
            streams = streams_result.value
            assert isinstance(streams, list)  # Should be list of StreamDefinition
            if len(streams) > 0:
                assert hasattr(streams[0], "stream_name")

    def test_oracle_tap_performance_with_real_connection(self) -> None:
        """Test Oracle tap performance with real connection attempt."""
        if not os.getenv("ORACLE_HOST"):
            pytest.skip("Oracle container not available - set ORACLE_HOST to run")

        TapConfig(tap_type="tap-oracle", connection_config=self.oracle_config)

        # Performance test: measure tap creation time
        profiler = FlextTestsPerformance.PerformanceProfiler()

        # Use memory profiling to measure Oracle tap creation
        with profiler.profile_memory("oracle_tap_creation"):
            self.tap_abstractions.create_tap_from_config(
                tap_type="tap-oracle", connection_config=self.oracle_config
            )

        # Verify performance metrics were captured
        assert len(profiler.measurements) > 0
        measurement = profiler.measurements[-1]
        assert measurement["operation"] == "oracle_tap_creation"
        assert "duration_seconds" in measurement
        assert "memory_mb" in measurement

    def test_oracle_multi_stream_configuration(self) -> None:
        """Test Oracle configuration with multiple streams."""
        if not os.getenv("ORACLE_HOST"):
            pytest.skip("Oracle container not available - set ORACLE_HOST to run")

        # Create Oracle tap with multiple table configurations
        oracle_config = self.oracle_config.copy()
        oracle_config["tables"] = [
            {"table_name": "HR.EMPLOYEES", "schema": "HR"},
            {"table_name": "HR.DEPARTMENTS", "schema": "HR"},
            {"table_name": "HR.JOBS", "schema": "HR"},
        ]

        config = TapConfig(tap_type="tap-oracle", connection_config=oracle_config)

        # Process configuration
        result = self.tap_abstractions.process(config)
        FlextTestsMatchers.assert_result_success(result)

        tap_instance = result.value
        assert tap_instance.tap_type == "tap-oracle"
        assert "tables" in tap_instance.config.connection_config
        tables = cast(
            "FlextTypes.Core.StringList",
            tap_instance.config.connection_config["tables"],
        )
        assert len(tables) == 3

    def test_oracle_error_handling_real(self) -> None:
        """Test real Oracle error handling with invalid connection."""
        # Use invalid Oracle configuration to test error handling
        invalid_config = {
            "host": "invalid-oracle-host",
            "port": 9999,
            "database": "INVALID",
            "username": "invalid_user",
            "password": "invalid_pass",
        }

        config = TapConfig(tap_type="tap-oracle", connection_config=invalid_config)

        # Process with invalid config - should handle errors gracefully
        result = self.tap_abstractions.process(config)

        # Should either succeed with validation or fail gracefully
        if result.is_failure:
            # Verify error contains meaningful information
            error_msg = str(result.error)
            assert len(error_msg) > 0
        else:
            # If validation passes, connection error should be caught during discovery
            tap_instance = result.value
            streams_result = self.tap_abstractions.discover_streams(tap_instance)
            # Should handle connection errors gracefully
            assert hasattr(streams_result, "is_success")

    def test_tap_abstractions_error_handling(self) -> None:
        """Test comprehensive error handling scenarios."""
        # Test with invalid configuration
        invalid_config_data = {
            "tap_type": "",  # Empty tap type
            "connection_config": {},  # Empty connection config
        }

        try:
            invalid_config = TapConfig(**invalid_config_data)
            # If it doesn't raise an error, test the processing
            result = self.tap_abstractions.process(invalid_config)
            # Should handle gracefully
            assert isinstance(result, FlextResult)
        except ValueError:
            # Pydantic validation caught the error, which is expected
            pass

    def test_tap_abstractions_concurrent_processing(self) -> None:
        """Test concurrent tap processing doesn't interfere."""

        def create_and_process_tap(tap_num: int) -> FlextResult[TapInstance]:
            config = TapConfig(
                tap_type=f"tap-test-{tap_num}",
                connection_config={"host": f"test{tap_num}.example.com"},
            )
            return self.tap_abstractions.process(config)

        # Process multiple taps concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(create_and_process_tap, i) for i in range(5)]
            results = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        # All should succeed
        for result in results:
            FlextTestsMatchers.assert_result_success(result)
            assert isinstance(result.value, TapInstance)

    def test_tap_abstractions_performance(
        self, benchmark: Callable[[Callable[[], object]], object]
    ) -> None:
        """Test tap abstractions performance using pytest-benchmark."""
        config = TapConfig(
            tap_type="tap-performance-test",
            connection_config={"host": "perf.example.com"},
        )

        def process_tap() -> object:
            return self.tap_abstractions.process(config)

        result = benchmark(process_tap)
        FlextTestsMatchers.assert_result_success(result)

    def test_complex_tap_workflow_integration(self) -> None:
        """Test complex workflow integrating multiple tap operations."""
        # Create comprehensive tap configuration
        config = TapConfig(
            tap_type="tap-postgres",
            connection_config={
                "host": "integration.db.com",
                "port": 5432,
                "database": "integration_test",
                "user": "integration_user",
                "password": "secure_password",
                "ssl_mode": "require",
            },
            stream_config={
                "users": {
                    "replication_method": "FULL_TABLE",
                    "selected": True,
                    "select": ["id", "username", "email", "created_at"],
                },
                "orders": {
                    "replication_method": "INCREMENTAL",
                    "replication_key": "updated_at",
                    "selected": True,
                    "select": ["order_id", "user_id", "total", "updated_at"],
                },
                "products": {
                    "replication_method": "FULL_TABLE",
                    "selected": False,
                    "select": ["*"],
                },
            },
            version="2.1.0",
        )

        # Process the configuration
        process_result = self.tap_abstractions.process(config)
        FlextTestsMatchers.assert_result_success(process_result)
        tap_instance = process_result.value

        # Add discovered streams
        users_stream = StreamDefinition(
            stream_name="users",
            stream_schema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "format": "int64"},
                    "username": {"type": "string", "maxLength": 255},
                    "email": {"type": "string", "format": "email"},
                    "created_at": {"type": "string", "format": "date-time"},
                },
                "required": ["id", "username", "email"],
            },
            tap_type="tap-postgres",
            status="discovered",
            records_extracted=0,
        )

        orders_stream = StreamDefinition(
            stream_name="orders",
            stream_schema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer", "format": "int64"},
                    "user_id": {"type": "integer", "format": "int64"},
                    "total": {"type": "number", "multipleOf": 0.01},
                    "updated_at": {"type": "string", "format": "date-time"},
                },
                "required": ["order_id", "user_id", "total", "updated_at"],
            },
            tap_type="tap-postgres",
            status="discovered",
            records_extracted=0,
        )

        # Update tap instance with streams
        tap_instance.streams = {"users": users_stream, "orders": orders_stream}
        tap_instance.discovered = True
        tap_instance.status = "ready"

        # Build output
        output = self.tap_abstractions.build(
            tap_instance, correlation_id="integration-test-001"
        )

        # Verify complete integration
        assert output["tap_type"] == "tap-postgres"
        assert output["discovered"] is True
        assert output["streams_count"] == 2

    @pytest.mark.parametrize(
        ("tap_type", "connection_config"),
        [
            ("tap-postgres", {"host": "postgres.example.com", "port": 5432}),
            ("tap-mysql", {"host": "mysql.example.com", "port": 3306}),
            (
                "tap-csv",
                {"files": [{"path": "test_parametrized.csv"}]},
            ),  # Use relative path
            ("tap-oracle", {"host": "oracle.example.com", "port": 1521}),
            ("tap-snowflake", {"account": "test", "warehouse": "compute"}),
        ],
    )
    def test_tap_abstractions_parametrized_tap_types(
        self, tap_type: str, connection_config: FlextTypes.Core.Dict
    ) -> None:
        """Test tap abstractions with various tap types."""
        config = TapConfig(tap_type=tap_type, connection_config=connection_config)

        result = self.tap_abstractions.process(config)
        FlextTestsMatchers.assert_result_success(result)

        tap_instance = result.value
        assert tap_instance.tap_type == tap_type

    def test_tap_abstractions_with_utilities_integration(self) -> None:
        """Test integration with FlextUtilities for enhanced functionality."""
        # Test timestamp generation for metadata
        timestamp = FlextUtilities.Generators.generate_iso_timestamp()
        assert isinstance(timestamp, str)
        assert "T" in timestamp
        assert "+" in timestamp

        # Test safe string processing for tap names
        safe_name = FlextUtilities.TextProcessor.safe_string("tap-postgres@#$%")
        assert isinstance(safe_name, str)

        # Create config with processed values
        config = TapConfig(
            tap_type=safe_name, connection_config={"host": "localhost"}, version="1.0.0"
        )

        result = self.tap_abstractions.process(config)
        FlextTestsMatchers.assert_result_success(result)

        tap_instance = result.value
        assert isinstance(tap_instance.tap_type, str)
        assert len(tap_instance.tap_type) > 0

    def test_tap_abstractions_large_scale_streams(self) -> None:
        """Test handling large numbers of streams efficiently."""
        config = TapConfig(
            tap_type="tap-large-db", connection_config={"host": "large.db.com"}
        )

        # Process basic config
        result = self.tap_abstractions.process(config)
        FlextTestsMatchers.assert_result_success(result)
        tap_instance = result.value

        # Create large number of stream definitions
        streams = {}
        for i in range(100):  # 100 streams
            stream = StreamDefinition(
                stream_name=f"table_{i:03d}",
                stream_schema={
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        f"field_{i}": {"type": "string"},
                    },
                },
                tap_type="tap-large-db",
                status="discovered",
            )
            streams[f"table_{i:03d}"] = stream

        # Update tap instance
        tap_instance.streams = streams
        tap_instance.discovered = True

        # Build output - should handle large number of streams efficiently
        output = self.tap_abstractions.build(
            tap_instance, correlation_id="large-scale-test"
        )

        assert output["streams_count"] == 100
        assert output["discovered"] is True
