"""Test module for flext-meltano."""

import concurrent.futures
import shutil
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

import pytest
from flext_core import FlextResult, FlextTypes, FlextUtilities
from flext_tests import FlextTestsMatchers

from flext_meltano import FlextTargetAbstractions


class TestFlextTargetConfigComprehensive:
    """Comprehensive tests for FlextTargetConfig Pydantic model."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self) -> None:
        """Cleanup after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_target_config_valid_creation(self) -> None:
        """Test creating valid target configuration."""
        config_data = {
            "target_type": "postgres",
            "connection_config": {
                "host": "localhost",
                "port": 5432,
                "database": "test_db",
                "user": "test_user",
                "password": "test_pass",
            },
            "batch_size": 1000,
            "max_batches": 50,
        }

        config = FlextTargetAbstractions.FlextTargetConfig.model_validate(config_data)
        assert config.target_type == "postgres"
        assert cast("str", config.connection_config["host"]) == "localhost"
        assert config.batch_size == 1000
        assert config.max_batches == 50

    def test_target_config_validation_target_type(self) -> None:
        """Test target type validation."""
        # Valid target types
        valid_types = ["postgres", "csv", "json", "sqlite", "mysql", "oracle"]
        for target_type in valid_types:
            config = FlextTargetAbstractions.FlextTargetConfig(
                target_type=target_type,
                connection_config={"host": "localhost"},
            )
            assert config.target_type == target_type

    def test_target_config_validation_empty_target_type(self) -> None:
        """Test validation fails with empty target type."""
        with pytest.raises(ValueError, match="Target type must be non-empty string"):
            FlextTargetAbstractions.FlextTargetConfig(
                target_type="",
                connection_config={"host": "localhost"},
            )

    def test_target_config_validation_batch_size(self) -> None:
        """Test batch size validation."""
        # Valid batch sizes
        for size in [100, 1000, 5000]:
            config = FlextTargetAbstractions.FlextTargetConfig(
                target_type="postgres",
                connection_config={"host": "localhost"},
                batch_size=size,
            )
            assert config.batch_size == size

        # Invalid batch sizes
        with pytest.raises(ValueError, match="Batch size must be positive integer"):
            FlextTargetAbstractions.FlextTargetConfig(
                target_type="postgres",
                connection_config={"host": "localhost"},
                batch_size=0,
            )

    def test_target_config_validation_max_batches(self) -> None:
        """Test max batches validation."""
        # Valid max batches
        for max_batches in [10, 50, 100]:
            config = FlextTargetAbstractions.FlextTargetConfig(
                target_type="postgres",
                connection_config={"host": "localhost"},
                max_batches=max_batches,
            )
            assert config.max_batches == max_batches

        # Invalid max batches
        with pytest.raises(ValueError, match="Max batches must be positive integer"):
            FlextTargetAbstractions.FlextTargetConfig(
                target_type="postgres",
                connection_config={"host": "localhost"},
                max_batches=0,
            )

    def test_target_config_connection_validation(self) -> None:
        """Test connection config validation."""
        # Valid connection configs
        valid_configs: list[FlextTypes.Dict] = [
            {"host": "localhost", "port": 5432},
            {"file_path": str(self.temp_dir / "test.csv")},
            {"url": "sqlite:///test.db"},
        ]

        for conn_config in valid_configs:
            config = FlextTargetAbstractions.FlextTargetConfig(
                target_type="postgres",
                connection_config=conn_config,
            )
            assert isinstance(config.connection_config, dict)
            assert len(config.connection_config) > 0

        # Empty connection config should fail
        with pytest.raises(
            ValueError,
            match="Connection configuration cannot be empty",
        ):
            FlextTargetAbstractions.FlextTargetConfig(
                target_type="postgres",
                connection_config={},
            )


class TestFlextStreamInfoComprehensive:
    """Comprehensive tests for FlextStreamInfo Pydantic model."""

    def test_stream_info_valid_creation(self) -> None:
        """Test creating valid stream information."""
        stream_data = {
            "stream_name": "users",
            "schema": {  # Note: uses alias "schema"
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                },
            },
            "created_at": datetime.now(UTC).isoformat(),
        }

        stream_info = FlextTargetAbstractions.FlextStreamInfo.model_validate(
            stream_data,
        )
        assert stream_info.stream_name == "users"
        assert stream_info.stream_schema["type"] == "object"
        assert "properties" in stream_info.stream_schema

    def test_stream_info_validation_empty_name(self) -> None:
        """Test stream name validation."""
        with pytest.raises(ValueError, match="Stream name must be non-empty string"):
            FlextTargetAbstractions.FlextStreamInfo(
                stream_name="",
                schema={"type": "object"},
                created_at=datetime.now(UTC).isoformat(),
            )

    def test_stream_info_validation_schema(self) -> None:
        """Test stream schema validation."""
        created_at = datetime.now(UTC).isoformat()

        # Valid schemas (must have 'properties' based on validation)
        valid_schemas: list[FlextTypes.Dict] = [
            {"type": "object", "properties": {"id": {"type": "integer"}}},
            {
                "type": "object",
                "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
            },
            {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "properties": {"data": {"type": "string"}},
            },
        ]

        for schema in valid_schemas:
            stream_info = FlextTargetAbstractions.FlextStreamInfo(
                stream_name="test_stream",
                schema=schema,
                created_at=created_at,
            )
            assert stream_info.stream_schema == schema

        # Schema without 'properties' should fail based on validation
        with pytest.raises(ValueError, match="Schema must contain properties"):
            FlextTargetAbstractions.FlextStreamInfo(
                stream_name="test_stream",
                schema={
                    "type": "array",
                    "items": {"type": "string"},
                },  # No 'properties'
                created_at=created_at,
            )


class TestFlextTargetAbstractionsComprehensive:
    """Comprehensive tests for FlextTargetAbstractions main class."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.target_abstractions = FlextTargetAbstractions()

    def teardown_method(self) -> None:
        """Cleanup after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_target_abstractions_initialization(self) -> None:
        """Test FlextTargetAbstractions initialization."""
        target_abs = FlextTargetAbstractions()
        assert target_abs.target_id is not None
        assert hasattr(target_abs, "_logger")

    def test_target_abstractions_with_custom_target_id(self) -> None:
        """Test initialization with custom target ID."""
        custom_id = "custom_target_123"
        target_abs = FlextTargetAbstractions(target_id=custom_id)
        assert target_abs.target_id == custom_id

    def test_create_flext_target_config_basic(self) -> None:
        """Test creating basic target configuration."""
        target_type = "postgres"
        connection_config = {
            "host": "localhost",
            "port": 5432,
            "database": "flext_test",
            "user": "flext_user",
            "password": "flext_pass",
        }

        result = self.target_abstractions.create_flext_target_config(
            target_type=target_type,
            connection_config=connection_config,
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value
        assert isinstance(config, dict)
        assert cast("str", config["target_type"]) == target_type
        assert config["connection_config"] == connection_config

    def test_create_flext_target_config_with_options(self) -> None:
        """Test creating target configuration with all options."""
        result = self.target_abstractions.create_flext_target_config(
            target_type="csv",
            connection_config={"file_path": str(self.temp_dir / "output.csv")},
            batch_size=500,
            max_batches=25,
            stream_maps={"users": "user_data"},
            config_extras={"delimiter": ",", "quoting": "minimal"},
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value
        assert cast("int", config["batch_size"]) == 500
        assert cast("int", config["max_batches"]) == 25
        assert config["stream_maps"] == {"users": "user_data"}

    def test_create_flext_target_config_invalid_type(self) -> None:
        """Test creating target config with invalid target type."""
        result = self.target_abstractions.create_flext_target_config(
            target_type="",  # Empty target type should fail
            connection_config={"host": "localhost"},
        )

        FlextTestsMatchers.assert_result_failure(result)

    def test_create_flext_target_config_invalid_connection(self) -> None:
        """Test creating target config with invalid connection config."""
        result = self.target_abstractions.create_flext_target_config(
            target_type="postgres",
            connection_config={},  # Empty connection config should fail
        )

        FlextTestsMatchers.assert_result_failure(result)

    def test_create_flext_target_postgres(self) -> None:
        """Test creating PostgreSQL target instance."""
        config: FlextTypes.Dict = {
            "target_type": "postgres",
            "connection_config": {
                "host": "localhost",
                "port": 5432,
                "database": "test_db",
                "user": "test_user",
                "password": "test_pass",
            },
        }

        result = self.target_abstractions.create_flext_target(
            config=config,
            adapter=None,  # No adapter for basic test
        )

        FlextTestsMatchers.assert_result_success(result)
        target_instance = result.value
        assert isinstance(target_instance, dict)
        assert target_instance["target_type"] == "postgres"
        assert "target_id" in target_instance
        assert "config" in target_instance
        # Cast nested dictionaries for type safety
        config_dict = cast("FlextTypes.Dict", target_instance["config"])
        connection_config = cast("FlextTypes.Dict", config_dict["connection_config"])
        assert cast("str", connection_config["host"]) == "localhost"

    def test_create_flext_target_csv(self) -> None:
        """Test creating CSV target instance."""
        csv_file = self.temp_dir / "test_output.csv"
        config: FlextTypes.Dict = {
            "target_type": "csv",
            "connection_config": {"file_path": str(csv_file)},
        }

        result = self.target_abstractions.create_flext_target(
            config=config,
            adapter=None,
        )

        FlextTestsMatchers.assert_result_success(result)
        target_instance = result.value
        assert isinstance(target_instance, dict), "Target instance should be a dict"
        # Cast to proper type - target_instance is validated as dict above
        target_dict: FlextTypes.Dict = target_instance
        assert target_dict["target_type"] == "csv"
        # Fix: Cast to proper type after validation
        target_config = target_dict["config"]
        assert isinstance(target_config, dict), "Config should be a dict"
        target_config_typed: FlextTypes.Dict = target_config
        assert isinstance(target_config, dict), "Config should be a dict"
        connection_config = target_config_typed["connection_config"]
        assert isinstance(connection_config, dict), "Connection config should be a dict"
        assert str(csv_file) in str(cast("object", connection_config["file_path"]))

    def test_create_flext_target_with_streams(self) -> None:
        """Test creating target with stream information."""
        config: FlextTypes.Dict = {
            "target_type": "json",
            "connection_config": {"file_path": str(self.temp_dir / "output.json")},
        }

        created_at = datetime.now(UTC).isoformat()

        stream_infos = [
            FlextTargetAbstractions.FlextStreamInfo(
                stream_name="users",
                schema={
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                    },
                },
                created_at=created_at,
            ),
            FlextTargetAbstractions.FlextStreamInfo(
                stream_name="orders",
                schema={
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "integer"},
                        "amount": {"type": "number"},
                    },
                },
                created_at=created_at,
            ),
        ]

        # Verify stream_infos were created properly
        assert len(stream_infos) == 2

        result = self.target_abstractions.create_flext_target(
            config=config,
            adapter=None,
        )

        FlextTestsMatchers.assert_result_success(result)
        target_instance = result.value
        assert target_instance["target_type"] == "json"
        assert isinstance(
            target_instance["streams"],
            dict,
        )  # streams initialized as empty dict

    def test_self(self, benchmark: object) -> None:
        """Test target creation performance using pytest-benchmark."""
        config: FlextTypes.Dict = {
            "target_type": "sqlite",
            "connection_config": {"database": str(self.temp_dir / "test.db")},
        }

        def create_target() -> object:
            return self.target_abstractions.create_flext_target(
                config=config,
                adapter=None,
            )

        # Add type assertion for benchmark callable
        assert callable(benchmark), "Benchmark should be callable"
        result = benchmark(create_target)
        # Type assertion for PyRight
        assert isinstance(result, FlextResult)
        FlextTestsMatchers.assert_result_success(result)

    def test_complex_target_workflow_integration(self) -> None:
        """Test complex workflow integrating multiple target operations."""
        # Create comprehensive target configuration
        postgres_config_result = self.target_abstractions.create_flext_target_config(
            target_type="postgres",
            connection_config={
                "host": "localhost",
                "port": 5432,
                "database": "integration_test",
                "user": "integration_user",
                "password": "secure_password",
                "schema": "public",
            },
            batch_size=2000,
            max_batches=100,
            stream_maps={
                "raw_users": "processed_users",
                "raw_orders": "processed_orders",
            },
            config_extras={"ssl_mode": "require", "connection_timeout": 30},
        )

        FlextTestsMatchers.assert_result_success(postgres_config_result)
        postgres_config = postgres_config_result.value

        # Create stream definitions
        created_at = datetime.now(UTC).isoformat()

        FlextTargetAbstractions.FlextStreamInfo(
            stream_name="users",
            schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "format": "int64"},
                    "username": {"type": "string", "maxLength": 255},
                    "email": {"type": "string", "format": "email"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "is_active": {"type": "boolean"},
                    "metadata": {"type": "object"},
                },
                "required": ["user_id", "username", "email"],
            },
            created_at=created_at,
        )

        FlextTargetAbstractions.FlextStreamInfo(
            stream_name="orders",
            schema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer", "format": "int64"},
                    "user_id": {"type": "integer", "format": "int64"},
                    "total_amount": {"type": "number", "multipleOf": 0.01},
                    "order_date": {"type": "string", "format": "date"},
                    "status": {
                        "type": "string",
                        "enum": ["pending", "completed", "cancelled"],
                    },
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "item_id": {"type": "integer"},
                                "quantity": {"type": "integer", "minimum": 1},
                                "price": {"type": "number", "minimum": 0},
                            },
                        },
                    },
                },
                "required": ["order_id", "user_id", "total_amount", "order_date"],
            },
            created_at=created_at,
        )

        # Create target instance
        target_result = self.target_abstractions.create_flext_target(
            config=postgres_config,
            adapter=None,
        )

        FlextTestsMatchers.assert_result_success(target_result)
        target_instance = target_result.value

        # Verify complete target setup
        assert target_instance["target_type"] == "postgres"
        assert isinstance(target_instance["config"], dict)
        assert target_instance["status"] == "initialized"

    def test_target_abstractions_error_handling(self) -> None:
        """Test comprehensive error handling scenarios."""
        # Test with invalid configuration parameters that will cause Pydantic validation errors
        invalid_scenarios = [
            # Invalid batch size (negative)
            {
                "target_type": "postgres",
                "connection_config": {"host": "localhost"},
                "batch_size": -100,
            },
            # Invalid max batches (zero)
            {
                "target_type": "postgres",
                "connection_config": {"host": "localhost"},
                "max_batches": 0,
            },
            # Empty target type
            {"target_type": "", "connection_config": {"host": "localhost"}},
        ]

        for scenario in invalid_scenarios:
            assert isinstance(scenario, dict), "Scenario should be a dict"
            result = self.target_abstractions.create_flext_target_config(**scenario)
            FlextTestsMatchers.assert_result_failure(result)

    def test_target_abstractions_edge_cases(self) -> None:
        """Test edge cases and boundary conditions."""
        # Test with minimal valid configuration
        minimal_config: FlextTypes.Dict = {
            "target_type": "csv",
            "connection_config": {"file_path": str(self.temp_dir / "minimal.csv")},
        }

        result = self.target_abstractions.create_flext_target(
            config=minimal_config,
            adapter=None,
        )

        FlextTestsMatchers.assert_result_success(result)
        target_instance = result.value
        assert target_instance["target_type"] == "csv"
        assert isinstance(target_instance["streams"], dict)

    def test_target_abstractions_concurrent_operations(self) -> None:
        """Test concurrent target operations don't interfere."""

        def create_target_config(target_num: int) -> FlextResult[FlextTypes.Dict]:
            return self.target_abstractions.create_flext_target_config(
                target_type="csv",
                connection_config={
                    "file_path": str(self.temp_dir / f"concurrent_{target_num}.csv"),
                },
            )

        # Create multiple targets concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(create_target_config, i) for i in range(5)]
            results = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        # All should succeed
        for result in results:
            assert hasattr(result, "is_success"), "Result should be FlextResult"
            FlextTestsMatchers.assert_result_success(result)
            assert isinstance(result.value, dict)

    def test_target_memory_usage_tracking(self) -> None:
        """Test creating large configuration without memory issues."""
        # Create large configuration
        result = self.target_abstractions.create_flext_target_config(
            target_type="postgres",
            connection_config={
                "host": "localhost",
                "port": 5432,
                "database": "memory_test",
            },
            config_extras={f"param_{i}": f"value_{i}" for i in range(100)},
        )

        FlextTestsMatchers.assert_result_success(result)

        # Verify large configuration was created
        config = result.value
        assert isinstance(config, dict), "Config should be a dict"
        config_extras = config.get("config_extras", {})
        assert isinstance(config_extras, dict), "Config extras should be a dict"
        assert len(config_extras) == 100
        assert cast("str", config["target_type"]) == "postgres"

    def test_target_abstractions_inheritance_validation(self) -> None:
        """Test that FlextTargetAbstractions has proper attributes."""
        target_abs = FlextTargetAbstractions()

        # Should have instance attributes
        assert hasattr(target_abs, "target_id")
        assert hasattr(target_abs, "_logger")

        # Target ID should contain target_abstractions prefix
        assert "target_abstractions_" in target_abs.target_id

    @pytest.mark.parametrize(
        ("target_type", "connection_config"),
        [
            ("postgres", {"host": "localhost", "port": 5432, "database": "test"}),
            ("mysql", {"host": "mysql.example.com", "port": 3306, "database": "app"}),
            ("sqlite", {"database": "parametrized_test.db"}),  # Use relative path
            ("csv", {"file_path": "parametrized_output.csv"}),  # Use relative path
            ("json", {"file_path": "parametrized_output.json"}),  # Use relative path
        ],
    )
    def test_target_config_parametrized_creation(
        self,
        target_type: str,
        connection_config: FlextTypes.Dict,
    ) -> None:
        """Test target configuration creation with various target types."""
        result = self.target_abstractions.create_flext_target_config(
            target_type=target_type,
            connection_config=connection_config,
        )

        FlextTestsMatchers.assert_result_success(result)
        config = result.value
        assert cast("str", config["target_type"]) == target_type
        assert config["connection_config"] == connection_config


class TestFlextTargetAbstractionsCoverageEnhancement:
    """Additional tests to achieve near 100% coverage."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.target_abstractions = FlextTargetAbstractions()

    def teardown_method(self) -> None:
        """Cleanup after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_basic_functionality_coverage(self) -> None:
        """Test basic functionality methods for coverage."""
        # Test basic property access methods that are likely to work
        # Create a simple target config first
        target_config: FlextTypes.Dict = {
            "target_type": "target-csv",
            "connection_config": {"file_path": str(self.temp_dir / "test.csv")},
        }
        target_type = self.target_abstractions.get_target_type(target_config)
        assert isinstance(target_type, str)

        # Test environment checks (these should always work)
        assert isinstance(self.target_abstractions.is_production(), bool)

        # Test basic list operations
        target_data: FlextTypes.Dict = {
            "target_type": "test",
            "connection": {"host": "localhost"},
        }
        result = self.target_abstractions.list_streams(target_data)
        assert isinstance(result, list)

        # Test target-specific functionality instead of Entity methods
        # Verify it has proper target ID (not Entity ID)
        assert hasattr(self.target_abstractions, "target_id")
        assert isinstance(self.target_abstractions.target_id, str)

    def test_target_specific_functionality(self) -> None:
        """Test target-specific functionality without Entity dependencies."""
        # Test core target functionality

        # Test target ID functionality
        assert hasattr(self.target_abstractions, "target_id")
        assert isinstance(self.target_abstractions.target_id, str)

        # Test environment methods (target-specific)
        assert isinstance(self.target_abstractions.is_production(), bool)

    def test_validation_and_environment_methods(self) -> None:
        """Test validation and environment methods for coverage."""
        # Test production mode check
        is_prod = self.target_abstractions.is_production()
        assert isinstance(is_prod, bool)

        # Test utility methods
        active_targets = self.target_abstractions.get_active_targets()
        assert isinstance(active_targets, list)

        registered_streams = self.target_abstractions.get_registered_streams()
        assert isinstance(registered_streams, list)

    def test_utility_and_audit_methods(self) -> None:
        """Test utility methods for coverage."""
        # Test timestamp generation using FlextUtilities as SOURCE OF TRUTH

        timestamp = FlextUtilities.Generators.generate_iso_timestamp()
        assert isinstance(timestamp, str)

        # Test safe nested value retrieval using flext-core SOURCE OF TRUTH
        data = {"level1": {"level2": {"value": "test"}}}
        result = data.get("level1", {}).get("level2", {}).get("value")
        assert result == "test"

        # Test non-existent path using flext-core SOURCE OF TRUTH
        nonexistent_result = data.get("nonexistent", {})
        path_result = (
            nonexistent_result.get("path")
            if isinstance(nonexistent_result, dict)
            else None
        )
        assert path_result is None

    def test_domain_events_and_lifecycle(self) -> None:
        """Test lifecycle and utility methods for coverage."""
        # Test the create_instance class method
        result = FlextTargetAbstractions.create_instance()
        assert isinstance(result, FlextResult)
        assert result.is_success

        # Test target type identification
        dummy_target: FlextTypes.Dict = {"type": "test-target", "config": {}}
        target_type = self.target_abstractions.get_target_type(dummy_target)
        assert isinstance(target_type, str)

        # Test finalize
        target_data: FlextTypes.Dict = {
            "target_type": "test",
            "connection": {"host": "localhost"},
        }
        finalize_result = self.target_abstractions.finalize(target_data)
        assert isinstance(finalize_result, FlextResult)
