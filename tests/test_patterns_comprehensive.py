"""Comprehensive tests for FLEXT Meltano patterns and helpers.

Tests all new functionality including mixins, builders, validators, and utilities.
Validates massive boilerplate reduction and professional enterprise patterns.
"""

from pathlib import Path
from typing import Never

import pytest

from flext_meltano.helpers import (
    FlextMeltanoConfigValidator,
    FlextMeltanoSingerUtils,
    FlextMeltanoTypedDict,
    create_flext_meltano_config_validator,
    create_flext_meltano_typed_dict,
    detect_plugin_type,
    normalize_plugin_name,
)
from flext_meltano.patterns import (
    FlextMeltanoBaseMixin,
    FlextMeltanoConfigMixin,
    FlextMeltanoConfigService,
    FlextMeltanoExecutionService,
    FlextMeltanoPipelineBuilder,
    FlextMeltanoPipelineConfig,
    FlextMeltanoResult,
    create_flext_meltano_config_service,
    create_flext_meltano_execution_service,
    create_flext_meltano_pipeline,
    flext_meltano_safe_operation,
)


class TestFlextMeltanoBaseMixin:
    """Test the base mixin functionality."""

    def test_base_mixin_initialization(self) -> None:
        """Test base mixin initializes correctly."""

        class TestClass(FlextMeltanoBaseMixin):
            def __init__(self) -> None:
                super().__init__()

        instance = TestClass()
        assert hasattr(instance, "logger")
        assert hasattr(instance, "_container")
        assert hasattr(instance, "_initialized")
        assert instance._initialized is False

    def test_safe_execute_success(self) -> None:
        """Test safe execute with successful operation."""

        class TestClass(FlextMeltanoBaseMixin):
            def __init__(self) -> None:
                super().__init__()

        instance = TestClass()

        def successful_operation():
            return {"result": "success"}

        result = instance.flext_meltano_safe_execute(successful_operation, "test_op")

        assert result.is_success
        assert result.data == {"result": "success"}

    def test_safe_execute_failure(self) -> None:
        """Test safe execute with failing operation."""

        class TestClass(FlextMeltanoBaseMixin):
            def __init__(self) -> None:
                super().__init__()

        instance = TestClass()

        def failing_operation() -> Never:
            msg = "Test error"
            raise ValueError(msg)

        result = instance.flext_meltano_safe_execute(failing_operation, "test_op")

        assert not result.is_success
        assert "test_op failed: Test error" in result.error

    @pytest.mark.asyncio
    async def test_safe_execute_async_success(self) -> None:
        """Test async safe execute with successful operation."""

        class TestClass(FlextMeltanoBaseMixin):
            def __init__(self) -> None:
                super().__init__()

        instance = TestClass()

        async def async_operation():
            return {"result": "async_success"}

        result = await instance.flext_meltano_safe_execute_async(async_operation, "async_test")

        assert result.is_success
        assert result.data == {"result": "async_success"}


class TestFlextMeltanoConfigMixin:
    """Test the configuration mixin functionality."""

    def test_config_mixin_initialization(self) -> None:
        """Test config mixin initializes with templates."""

        class TestClass(FlextMeltanoConfigMixin):
            def __init__(self) -> None:
                super().__init__()

        instance = TestClass()
        assert hasattr(instance, "_config_templates")
        assert isinstance(instance._config_templates, dict)
        assert "tap_postgres" in instance._config_templates
        assert "target_jsonl" in instance._config_templates

    def test_get_config_with_valid_config(self) -> None:
        """Test getting configuration with valid config attribute."""

        class TestClass(FlextMeltanoConfigMixin):
            def __init__(self) -> None:
                super().__init__()
                self.config = {
                    "host": "localhost",
                    "port": 5432,
                    "debug": True,
                }

        instance = TestClass()

        # Test string config
        result = instance.flext_meltano_get_config("host", config_type=str)
        assert result.is_success
        assert result.data == "localhost"

        # Test integer config
        result = instance.flext_meltano_get_config("port", config_type=int)
        assert result.is_success
        assert result.data == 5432

        # Test boolean config
        result = instance.flext_meltano_get_config("debug", config_type=bool)
        assert result.is_success
        assert result.data is True

    def test_validate_config_success(self) -> None:
        """Test config validation with valid configuration."""

        class TestClass(FlextMeltanoConfigMixin):
            def __init__(self) -> None:
                super().__init__()

        instance = TestClass()

        config = {
            "host": "localhost",
            "port": 5432,
            "user": "postgres",
        }

        schema = {
            "required": ["host", "port", "user"],
            "types": {
                "host": "string",
                "port": "integer",
                "user": "string",
            },
        }

        result = instance.flext_meltano_validate_config(config, schema)
        assert result.is_success
        assert result.data == config

    def test_validate_config_missing_required(self) -> None:
        """Test config validation with missing required field."""

        class TestClass(FlextMeltanoConfigMixin):
            def __init__(self) -> None:
                super().__init__()

        instance = TestClass()

        config = {
            "host": "localhost",
            "port": 5432,
            # Missing 'user'
        }

        schema = {
            "required": ["host", "port", "user"],
            "types": {
                "host": "string",
                "port": "integer",
                "user": "string",
            },
        }

        result = instance.flext_meltano_validate_config(config, schema)
        assert not result.is_success
        assert "validation failed" in result.error


class TestFlextMeltanoPipelineBuilder:
    """Test the pipeline builder functionality."""

    def test_builder_initialization(self) -> None:
        """Test pipeline builder initializes correctly."""
        builder = FlextMeltanoPipelineBuilder()

        assert builder._tap_name == ""
        assert builder._target_name == "target-jsonl"
        assert isinstance(builder._overrides, dict)
        assert isinstance(builder._project_root, Path)

    def test_fluent_postgres_configuration(self) -> None:
        """Test PostgreSQL tap configuration."""
        builder = FlextMeltanoPipelineBuilder()

        result_builder = builder.from_postgres(
            host="custom-host",
            database="custom-db",
        )

        # Should return self for chaining
        assert result_builder is builder
        assert builder._tap_name == "tap-postgres"
        assert "tap_config" in builder._overrides
        assert builder._overrides["tap_config"]["host"] == "custom-host"
        assert builder._overrides["tap_config"]["database"] == "custom-db"

    def test_fluent_target_configuration(self) -> None:
        """Test target configuration."""
        builder = FlextMeltanoPipelineBuilder()

        result_builder = builder.to_csv(
            destination_path="/tmp/output",
            delimiter=";",
        )

        assert result_builder is builder
        assert builder._target_name == "target-csv"
        assert "target_config" in builder._overrides
        assert builder._overrides["target_config"]["destination_path"] == "/tmp/output"
        assert builder._overrides["target_config"]["delimiter"] == ";"

    def test_fluent_chaining(self) -> None:
        """Test fluent API chaining."""
        builder = (FlextMeltanoPipelineBuilder()
                  .from_mysql(host="mysql-host", database="test_db")
                  .to_parquet(destination_path="/data/output")
                  .with_environment("production")
                  .with_custom_config(batch_size=5000))

        assert builder._tap_name == "tap-mysql"
        assert builder._target_name == "target-parquet"
        assert builder._overrides["environment"] == "production"
        assert builder._overrides["batch_size"] == 5000

    def test_build_config(self) -> None:
        """Test configuration building."""
        builder = (FlextMeltanoPipelineBuilder()
                  .from_postgres(host="localhost", database="test")
                  .to_jsonl(destination_path="/tmp"))

        result = builder.build_config()

        assert result.is_success
        config = result.data
        assert config["tap_name"] == "tap-postgres"
        assert config["target_name"] == "target-jsonl"
        assert "tap_config" in config
        assert "target_config" in config

    def test_run_without_tap_fails(self) -> None:
        """Test that running without tap configuration fails."""
        builder = FlextMeltanoPipelineBuilder()

        result = builder.run_sync()

        assert not result.is_success
        assert "Tap name not configured" in result.error


class TestFlextMeltanoConfigService:
    """Test the configuration service functionality."""

    def test_config_service_initialization(self) -> None:
        """Test config service initializes correctly."""
        service = FlextMeltanoConfigService()

        assert hasattr(service, "_config_templates")
        assert hasattr(service, "_schema_registry")

    def test_config_service_execute(self) -> None:
        """Test config service execution."""
        service = FlextMeltanoConfigService()

        result = service.execute()

        assert result.is_success
        data = result.data
        assert data["service"] == "FlextMeltanoConfigService"
        assert data["status"] == "ready"
        assert "templates_loaded" in data
        assert "schemas_loaded" in data

    def test_get_tap_config_template_postgres(self) -> None:
        """Test getting PostgreSQL tap template."""
        service = FlextMeltanoConfigService()

        result = service.get_tap_config_template(
            "postgres",
            host="custom-host",
            port=5433,
        )

        assert result.is_success
        template = result.data
        assert template["host"] == "custom-host"
        assert template["port"] == 5433
        assert template["user"] == "postgres"  # From default template

    def test_get_tap_config_template_unknown(self) -> None:
        """Test getting unknown tap template fails."""
        service = FlextMeltanoConfigService()

        result = service.get_tap_config_template("unknown_tap")

        assert not result.is_success
        assert "Unknown tap type: unknown_tap" in result.error

    def test_get_target_config_template_jsonl(self) -> None:
        """Test getting JSONL target template."""
        service = FlextMeltanoConfigService()

        result = service.get_target_config_template(
            "jsonl",
            destination_path="/custom/path",
        )

        assert result.is_success
        template = result.data
        assert template["destination_path"] == "/custom/path"
        assert template["file_naming_scheme"] == "{stream_name}.jsonl"


class TestFlextMeltanoExecutionService:
    """Test the execution service functionality."""

    def test_execution_service_initialization(self) -> None:
        """Test execution service initializes correctly."""
        config_service = FlextMeltanoConfigService()
        exec_service = FlextMeltanoExecutionService(config_service)

        assert exec_service.config_service is config_service

    def test_execution_service_execute(self) -> None:
        """Test execution service execution."""
        config_service = FlextMeltanoConfigService()
        exec_service = FlextMeltanoExecutionService(config_service)

        result = exec_service.execute()

        assert result.is_success
        data = result.data
        assert data["service"] == "FlextMeltanoExecutionService"
        assert data["status"] == "ready"
        assert data["config_service_status"] == "injected"


class TestFlextMeltanoTypedDict:
    """Test the typed dictionary functionality."""

    def test_typed_dict_initialization(self) -> None:
        """Test typed dict initializes correctly."""
        data = {"key1": "value1", "key2": 42}
        typed_dict = FlextMeltanoTypedDict(data)

        assert typed_dict._data == data
        assert hasattr(typed_dict, "_meltano_schema_cache")

    def test_get_tap_config_success(self) -> None:
        """Test getting tap configuration successfully."""
        data = {
            "tap-postgres": {
                "host": "localhost",
                "port": 5432,
                "user": "postgres",
            },
        }
        typed_dict = FlextMeltanoTypedDict(data)

        result = typed_dict.get_tap_config("tap-postgres")

        assert result.is_success
        config = result.data
        assert config["host"] == "localhost"
        assert config["port"] == 5432

    def test_get_tap_config_with_required_fields(self) -> None:
        """Test getting tap config with required field validation."""
        data = {
            "tap-mysql": {
                "host": "localhost",
                "user": "root",
                # Missing 'port' which will be required
            },
        }
        typed_dict = FlextMeltanoTypedDict(data)

        result = typed_dict.get_tap_config("tap-mysql", required_fields=["host", "port", "user"])

        assert not result.is_success
        assert "Required tap field missing: port" in result.error

    def test_validate_singer_catalog_valid(self) -> None:
        """Test validating valid Singer catalog."""
        catalog_data = {
            "streams": [
                {
                    "tap_stream_id": "users",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                        },
                    },
                },
            ],
        }
        typed_dict = FlextMeltanoTypedDict(catalog_data)

        result = typed_dict.validate_singer_catalog()

        assert result.is_success
        assert result.data is True

    def test_validate_singer_catalog_missing_streams(self) -> None:
        """Test validating Singer catalog missing streams field."""
        catalog_data = {"version": 1}  # Missing 'streams'
        typed_dict = FlextMeltanoTypedDict(catalog_data)

        result = typed_dict.validate_singer_catalog()

        assert not result.is_success
        assert "must contain 'streams' field" in result.error

    def test_extract_plugin_configs(self) -> None:
        """Test extracting plugin configurations."""
        meltano_data = {
            "plugins": {
                "extractors": [
                    {
                        "name": "tap-postgres",
                        "executable": "tap-postgres",
                        "config": {"host": "localhost"},
                    },
                ],
                "loaders": [
                    {
                        "name": "target-jsonl",
                        "executable": "target-jsonl",
                        "config": {"destination_path": "output"},
                    },
                ],
            },
        }
        typed_dict = FlextMeltanoTypedDict(meltano_data)

        result = typed_dict.extract_plugin_configs()

        assert result.is_success
        configs = result.data
        assert "taps" in configs
        assert "targets" in configs
        assert "tap-postgres" in configs["taps"]
        assert "target-jsonl" in configs["targets"]


class TestFlextMeltanoConfigValidator:
    """Test the configuration validator functionality."""

    def test_validator_initialization(self) -> None:
        """Test validator initializes with schemas."""
        validator = FlextMeltanoConfigValidator()

        assert hasattr(validator, "_schemas")
        assert isinstance(validator._schemas, dict)
        assert "tap_postgres" in validator._schemas

    def test_validate_postgres_config_valid(self) -> None:
        """Test validating valid PostgreSQL configuration."""
        validator = FlextMeltanoConfigValidator()

        config = {
            "host": "localhost",
            "port": 5432,
            "user": "postgres",
            "database": "test_db",
        }

        result = validator.validate_tap_postgres_config(config)

        assert result.is_success
        assert result.data == config

    def test_validate_postgres_config_missing_required(self) -> None:
        """Test validating PostgreSQL config with missing required field."""
        validator = FlextMeltanoConfigValidator()

        config = {
            "host": "localhost",
            "port": 5432,
            # Missing 'user' and 'database'
        }

        result = validator.validate_tap_postgres_config(config)

        assert not result.is_success
        assert "validation failed" in result.error

    def test_validate_postgres_config_invalid_port(self) -> None:
        """Test validating PostgreSQL config with invalid port."""
        validator = FlextMeltanoConfigValidator()

        config = {
            "host": "localhost",
            "port": 99999,  # Invalid port number
            "user": "postgres",
            "database": "test_db",
        }

        result = validator.validate_tap_postgres_config(config)

        assert not result.is_success
        assert "constraint failed" in result.error


class TestFlextMeltanoSingerUtils:
    """Test the Singer utilities functionality."""

    def test_create_singer_record(self) -> None:
        """Test creating Singer RECORD message."""
        record_data = {"id": 1, "name": "test"}

        message = FlextMeltanoSingerUtils.create_singer_record(
            "users", record_data, "2024-01-01T00:00:00Z",
        )

        assert message["type"] == "RECORD"
        assert message["stream"] == "users"
        assert message["record"] == record_data
        assert message["time_extracted"] == "2024-01-01T00:00:00Z"

    def test_create_singer_schema(self) -> None:
        """Test creating Singer SCHEMA message."""
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        }

        message = FlextMeltanoSingerUtils.create_singer_schema(
            "users", schema, ["id"],
        )

        assert message["type"] == "SCHEMA"
        assert message["stream"] == "users"
        assert message["schema"] == schema
        assert message["key_properties"] == ["id"]

    def test_create_singer_state(self) -> None:
        """Test creating Singer STATE message."""
        state_data = {
            "bookmarks": {
                "users": {
                    "replication_key_value": "2024-01-01T00:00:00Z",
                },
            },
        }

        message = FlextMeltanoSingerUtils.create_singer_state(state_data)

        assert message["type"] == "STATE"
        assert message["value"] == state_data

    def test_validate_singer_message_record(self) -> None:
        """Test validating Singer RECORD message."""
        message = {
            "type": "RECORD",
            "stream": "users",
            "record": {"id": 1, "name": "test"},
        }

        result = FlextMeltanoSingerUtils.validate_singer_message(message)

        assert result.is_success
        assert result.data is True

    def test_validate_singer_message_invalid(self) -> None:
        """Test validating invalid Singer message."""
        message = {
            "type": "RECORD",
            # Missing 'stream' and 'record'
        }

        result = FlextMeltanoSingerUtils.validate_singer_message(message)

        assert not result.is_success
        assert "missing field" in result.error

    def test_extract_records_from_singer_output(self) -> None:
        """Test extracting records from Singer output."""
        singer_output = """{"type": "SCHEMA", "stream": "users", "schema": {}}
{"type": "RECORD", "stream": "users", "record": {"id": 1, "name": "Alice"}}
{"type": "RECORD", "stream": "users", "record": {"id": 2, "name": "Bob"}}
{"type": "STATE", "value": {"bookmarks": {}}}"""

        result = FlextMeltanoSingerUtils.extract_records_from_singer_output(singer_output)

        assert result.is_success
        records = result.data
        assert len(records) == 2
        assert records[0] == {"id": 1, "name": "Alice"}
        assert records[1] == {"id": 2, "name": "Bob"}


class TestFactoryFunctions:
    """Test factory functions."""

    def test_create_flext_meltano_pipeline(self) -> None:
        """Test creating pipeline builder."""
        builder = create_flext_meltano_pipeline()

        assert isinstance(builder, FlextMeltanoPipelineBuilder)

    def test_create_flext_meltano_config_service(self) -> None:
        """Test creating config service."""
        service = create_flext_meltano_config_service()

        assert isinstance(service, FlextMeltanoConfigService)

    def test_create_flext_meltano_execution_service(self) -> None:
        """Test creating execution service."""
        service = create_flext_meltano_execution_service()

        assert isinstance(service, FlextMeltanoExecutionService)
        assert isinstance(service.config_service, FlextMeltanoConfigService)

    def test_create_flext_meltano_typed_dict(self) -> None:
        """Test creating typed dictionary."""
        data = {"test": "value"}
        typed_dict = create_flext_meltano_typed_dict(data)

        assert isinstance(typed_dict, FlextMeltanoTypedDict)
        assert typed_dict._data == data

    def test_create_flext_meltano_config_validator(self) -> None:
        """Test creating config validator."""
        validator = create_flext_meltano_config_validator()

        assert isinstance(validator, FlextMeltanoConfigValidator)


class TestUtilityFunctions:
    """Test utility functions."""

    def test_normalize_plugin_name(self) -> None:
        """Test plugin name normalization."""
        assert normalize_plugin_name("tap-postgres") == "postgres"
        assert normalize_plugin_name("target-jsonl") == "jsonl"
        assert normalize_plugin_name("tap_mysql_custom") == "mysql-custom"

    def test_detect_plugin_type(self) -> None:
        """Test plugin type detection."""
        assert detect_plugin_type("tap-postgres") == "postgres"
        assert detect_plugin_type("tap-postgresql") == "postgres"
        assert detect_plugin_type("tap-mysql") == "mysql"
        assert detect_plugin_type("tap-oracle") == "oracle"
        assert detect_plugin_type("target-jsonl") == "jsonl"
        assert detect_plugin_type("target-parquet") == "parquet"
        assert detect_plugin_type("tap-csv") == "csv"


class TestDecorators:
    """Test decorator functionality."""

    def test_safe_operation_decorator_success(self) -> None:
        """Test safe operation decorator with successful function."""

        @flext_meltano_safe_operation("test_operation")
        def successful_function(x: int, y: int) -> int:
            return x + y

        result = successful_function(5, 3)

        assert isinstance(result, FlextMeltanoResult)
        assert result.is_success
        assert result.data == 8

    def test_safe_operation_decorator_failure(self) -> None:
        """Test safe operation decorator with failing function."""

        @flext_meltano_safe_operation("test_operation")
        def failing_function() -> int:
            msg = "Test error"
            raise ValueError(msg)

        result = failing_function()

        assert isinstance(result, FlextMeltanoResult)
        assert not result.is_success
        assert "test_operation failed: Test error" in result.error


class TestFlextMeltanoPipelineConfig:
    """Test pipeline configuration value object."""

    def test_pipeline_config_creation(self) -> None:
        """Test creating pipeline configuration."""
        config = FlextMeltanoPipelineConfig(
            tap_name="tap-postgres",
            target_name="target-jsonl",
            environment="production",
            project_root=Path("/tmp/test"),
            tap_config={"host": "localhost"},
            target_config={"destination_path": "/output"},
        )

        assert config.tap_name == "tap-postgres"
        assert config.target_name == "target-jsonl"
        assert config.environment == "production"
        assert config.project_root == Path("/tmp/test")
        assert config.tap_config == {"host": "localhost"}
        assert config.target_config == {"destination_path": "/output"}

    def test_pipeline_config_validation_success(self) -> None:
        """Test pipeline config validation with valid data."""
        config = FlextMeltanoPipelineConfig(
            tap_name="tap-postgres",
            target_name="target-jsonl",
        )

        # Should not raise any exception
        config.validate_domain_rules()

    def test_pipeline_config_validation_missing_tap(self) -> None:
        """Test pipeline config validation with missing tap name."""
        config = FlextMeltanoPipelineConfig(
            tap_name="",  # Empty tap name
            target_name="target-jsonl",
        )

        with pytest.raises(ValueError, match="tap_name is required"):
            config.validate_domain_rules()

    def test_pipeline_config_validation_missing_target(self) -> None:
        """Test pipeline config validation with missing target name."""
        config = FlextMeltanoPipelineConfig(
            tap_name="tap-postgres",
            target_name="",  # Empty target name
        )

        with pytest.raises(ValueError, match="target_name is required"):
            config.validate_domain_rules()


# Performance and Integration Tests
class TestIntegrationScenarios:
    """Test complete integration scenarios."""

    def test_complete_pipeline_configuration_flow(self) -> None:
        """Test complete pipeline configuration flow."""
        # Create services
        config_service = create_flext_meltano_config_service()

        # Get tap template
        tap_result = config_service.get_tap_config_template(
            "postgres",
            host="production-db",
            database="analytics",
        )
        assert tap_result.is_success

        # Get target template
        target_result = config_service.get_target_config_template(
            "jsonl",
            destination_path="/data/output",
        )
        assert target_result.is_success

        # Build pipeline using fluent API
        pipeline = (create_flext_meltano_pipeline()
                   .from_postgres(**tap_result.data)
                   .to_jsonl(**target_result.data)
                   .with_environment("production"))

        # Build configuration
        config_result = pipeline.build_config()
        assert config_result.is_success

        config = config_result.data
        assert config["tap_name"] == "tap-postgres"
        assert config["target_name"] == "target-jsonl"
        assert config["environment"] == "production"
        assert config["tap_config"]["host"] == "production-db"
        assert config["target_config"]["destination_path"] == "/data/output"

    def test_configuration_validation_flow(self) -> None:
        """Test configuration validation flow."""
        validator = create_flext_meltano_config_validator()

        # Test multiple configuration types
        postgres_config = {
            "host": "localhost",
            "port": 5432,
            "user": "postgres",
            "database": "test",
        }

        mysql_config = {
            "host": "mysql-server",
            "port": 3306,
            "user": "root",
            "database": "app_db",
        }

        jsonl_config = {
            "destination_path": "/tmp/output",
        }

        # Validate all configs
        postgres_result = validator.validate_tap_postgres_config(postgres_config)
        mysql_result = validator.validate_tap_mysql_config(mysql_config)
        jsonl_result = validator.validate_target_jsonl_config(jsonl_config)

        assert postgres_result.is_success
        assert mysql_result.is_success
        assert jsonl_result.is_success

    def test_singer_message_processing_flow(self) -> None:
        """Test Singer message processing flow."""
        utils = FlextMeltanoSingerUtils()

        # Create schema message
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
            },
        }
        schema_msg = utils.create_singer_schema("users", schema, ["id"])

        # Create record messages
        records = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
        ]
        record_msgs = [utils.create_singer_record("users", record) for record in records]

        # Create state message
        state_data = {
            "bookmarks": {
                "users": {
                    "replication_key_value": "2024-01-01T00:00:00Z",
                },
            },
        }
        state_msg = utils.create_singer_state(state_data)

        # Validate all messages
        schema_valid = utils.validate_singer_message(schema_msg)
        record_valid = all(utils.validate_singer_message(msg).is_success for msg in record_msgs)
        state_valid = utils.validate_singer_message(state_msg)

        assert schema_valid.is_success
        assert record_valid
        assert state_valid.is_success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
