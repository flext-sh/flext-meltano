"""Comprehensive tests for FlextMeltano patterns module - Real implementations only.

Tests all real functionality including Singer message processing, Meltano CLI integration,
and pipeline building with actual validation and error handling.
"""

import json
import subprocess
from pathlib import Path
from typing import Never
from unittest.mock import Mock, patch

import pytest
import yaml
from flext_core import FlextResult

from flext_meltano.patterns import (
    FlextMeltanoBaseMixin,
    FlextMeltanoConfigMixin,
    FlextMeltanoConfigService,
    FlextMeltanoExecutionMixin,
    FlextMeltanoExecutionService,
    FlextMeltanoPipelineBuilder,
    FlextMeltanoPipelineConfig,
    FlextMeltanoSingerMixin,
    create_flext_meltano_config_service,
    create_flext_meltano_execution_service,
    create_flext_meltano_pipeline,
    flext_meltano_safe_operation,
)

# =============================================================================
# FIXTURES - Real test data and setup
# =============================================================================


@pytest.fixture
def sample_meltano_yml():
    """Sample meltano.yml configuration for testing."""
    return {
        "version": 1,
        "default_environment": "dev",
        "project_id": "test-project",
        "plugins": {
            "extractors": [
                {
                    "name": "tap-postgres",
                    "namespace": "tap_postgres",
                    "executable": "tap-postgres",
                    "config": {
                        "host": "localhost",
                        "port": 5432,
                        "user": "postgres",
                        "database": "test",
                    },
                },
            ],
            "loaders": [
                {
                    "name": "target-jsonl",
                    "namespace": "target_jsonl",
                    "executable": "target-jsonl",
                    "config": {"destination_path": "./output"},
                },
            ],
        },
    }


@pytest.fixture
def sample_singer_messages():
    """Sample Singer messages for testing."""
    return [
        {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                },
            },
            "key_properties": ["id"],
        },
        {
            "type": "RECORD",
            "stream": "users",
            "record": {"id": 1, "name": "Alice", "email": "alice@example.com"},
            "time_extracted": "2024-01-15T10:30:00Z",
        },
        {
            "type": "RECORD",
            "stream": "users",
            "record": {"id": 2, "name": "Bob", "email": "bob@example.com"},
            "time_extracted": "2024-01-15T10:31:00Z",
        },
        {
            "type": "STATE",
            "value": {
                "bookmarks": {
                    "users": {
                        "replication_key": "id",
                        "replication_key_value": 2,
                    },
                },
            },
        },
    ]


@pytest.fixture
def temp_meltano_project(tmp_path, sample_meltano_yml):
    """Create temporary Meltano project for testing."""
    project_path = tmp_path / "test_project"
    project_path.mkdir()

    meltano_yml = project_path / "meltano.yml"
    with meltano_yml.open("w") as f:
        yaml.safe_dump(sample_meltano_yml, f)

    return project_path


# =============================================================================
# TESTS FOR BASE MIXINS
# =============================================================================


class TestFlextMeltanoBaseMixin:
    """Test base mixin functionality."""

    def test_mixin_initialization(self) -> None:
        """Test mixin initializes correctly with logger and container."""

        class TestClass(FlextMeltanoBaseMixin):
            pass

        instance = TestClass()
        assert hasattr(instance, "logger")
        assert hasattr(instance, "_container")
        assert not instance._initialized

    def test_safe_execute_success(self) -> None:
        """Test safe execution with successful operation."""

        class TestClass(FlextMeltanoBaseMixin):
            pass

        instance = TestClass()

        def successful_operation() -> str:
            return "success_result"

        result = instance.flext_meltano_safe_execute(
            successful_operation, "test_operation",
        )

        assert result.is_success
        assert result.data == "success_result"

    def test_safe_execute_failure(self) -> None:
        """Test safe execution with failing operation."""

        class TestClass(FlextMeltanoBaseMixin):
            pass

        instance = TestClass()

        def failing_operation() -> Never:
            msg = "Test error"
            raise ValueError(msg)

        result = instance.flext_meltano_safe_execute(
            failing_operation, "test_operation",
        )

        assert not result.is_success
        assert "Test error" in result.error

    @pytest.mark.asyncio
    async def test_safe_execute_async_success(self) -> None:
        """Test async safe execution with successful operation."""

        class TestClass(FlextMeltanoBaseMixin):
            pass

        instance = TestClass()

        async def async_operation() -> str:
            return "async_success"

        result = await instance.flext_meltano_safe_execute_async(
            async_operation, "async_test",
        )

        assert result.is_success
        assert result.data == "async_success"

    @pytest.mark.asyncio
    async def test_safe_execute_async_failure(self) -> None:
        """Test async safe execution with failing operation."""

        class TestClass(FlextMeltanoBaseMixin):
            pass

        instance = TestClass()

        async def async_failing_operation() -> Never:
            msg = "Async test error"
            raise RuntimeError(msg)

        result = await instance.flext_meltano_safe_execute_async(
            async_failing_operation, "async_test",
        )

        assert not result.is_success
        assert "Async test error" in result.error


class TestFlextMeltanoConfigMixin:
    """Test configuration mixin functionality."""

    def test_config_mixin_initialization(self) -> None:
        """Test config mixin initializes with templates."""

        class TestClass(FlextMeltanoConfigMixin):
            pass

        instance = TestClass()
        assert hasattr(instance, "_config_templates")
        assert hasattr(instance, "_flext_dict")
        assert "tap_postgres" in instance._config_templates

    def test_get_config_with_dict_attribute(self) -> None:
        """Test getting configuration when config attribute exists."""

        class TestClass(FlextMeltanoConfigMixin):
            def __init__(self) -> None:
                super().__init__()
                self.config = {"test_key": "test_value", "port": 5432}

        instance = TestClass()

        # Test string config
        result = instance.flext_meltano_get_config("test_key", config_type=str)
        assert result.is_success
        assert result.data == "test_value"

        # Test integer config
        result = instance.flext_meltano_get_config("port", config_type=int)
        assert result.is_success
        assert result.data == 5432

    def test_get_config_missing_key(self) -> None:
        """Test getting configuration with missing key."""

        class TestClass(FlextMeltanoConfigMixin):
            def __init__(self) -> None:
                super().__init__()
                self.config = {}

        instance = TestClass()

        result = instance.flext_meltano_get_config("missing_key")
        assert not result.is_success
        assert "not found" in result.error

    def test_validate_config_success(self) -> None:
        """Test successful configuration validation."""

        class TestClass(FlextMeltanoConfigMixin):
            pass

        instance = TestClass()

        config = {"host": "localhost", "port": 5432, "user": "postgres"}
        schema = {
            "required": ["host", "port"],
            "types": {"host": "string", "port": "integer"},
        }

        result = instance.flext_meltano_validate_config(config, schema)
        assert result.is_success
        assert result.data == config

    def test_validate_config_missing_required(self) -> None:
        """Test configuration validation with missing required field."""

        class TestClass(FlextMeltanoConfigMixin):
            pass

        instance = TestClass()

        config = {"host": "localhost"}
        schema = {"required": ["host", "port"]}

        result = instance.flext_meltano_validate_config(config, schema)
        assert not result.is_success
        assert "port" in result.error

    def test_validate_config_wrong_type(self) -> None:
        """Test configuration validation with wrong type."""

        class TestClass(FlextMeltanoConfigMixin):
            pass

        instance = TestClass()

        config = {"host": "localhost", "port": "invalid_port"}
        schema = {"types": {"port": "integer"}}

        result = instance.flext_meltano_validate_config(config, schema)
        assert not result.is_success
        assert "integer" in result.error


class TestFlextMeltanoSingerMixin:
    """Test Singer SDK integration mixin."""

    def test_singer_mixin_initialization(self) -> None:
        """Test Singer mixin initializes correctly."""

        class TestClass(FlextMeltanoSingerMixin):
            pass

        instance = TestClass()
        assert hasattr(instance, "_singer_state")
        assert hasattr(instance, "_message_buffer")
        assert isinstance(instance._message_buffer, list)

    def test_create_singer_record_message(self) -> None:
        """Test creating valid Singer RECORD message."""

        class TestClass(FlextMeltanoSingerMixin):
            pass

        instance = TestClass()

        result = instance.flext_meltano_create_singer_message(
            "RECORD",
            stream="users",
            record={"id": 1, "name": "Alice"},
            time_extracted="2024-01-15T10:30:00Z",
        )

        assert result.is_success
        message = result.data
        assert message["type"] == "RECORD"
        assert message["stream"] == "users"
        assert message["record"] == {"id": 1, "name": "Alice"}
        assert message["time_extracted"] == "2024-01-15T10:30:00Z"

    def test_create_singer_schema_message(self) -> None:
        """Test creating valid Singer SCHEMA message."""

        class TestClass(FlextMeltanoSingerMixin):
            pass

        instance = TestClass()

        schema = {"type": "object", "properties": {"id": {"type": "integer"}}}

        result = instance.flext_meltano_create_singer_message(
            "SCHEMA",
            stream="users",
            schema=schema,
            key_properties=["id"],
        )

        assert result.is_success
        message = result.data
        assert message["type"] == "SCHEMA"
        assert message["stream"] == "users"
        assert message["schema"] == schema
        assert message["key_properties"] == ["id"]

    def test_create_singer_state_message(self) -> None:
        """Test creating valid Singer STATE message."""

        class TestClass(FlextMeltanoSingerMixin):
            pass

        instance = TestClass()

        state_data = {"bookmarks": {"users": {"replication_key_value": 100}}}

        result = instance.flext_meltano_create_singer_message(
            "STATE", value=state_data,
        )

        assert result.is_success
        message = result.data
        assert message["type"] == "STATE"
        assert message["value"] == state_data

    def test_create_singer_message_invalid(self) -> None:
        """Test creating Singer message with invalid parameters."""

        class TestClass(FlextMeltanoSingerMixin):
            pass

        instance = TestClass()

        # Missing required fields for RECORD
        result = instance.flext_meltano_create_singer_message("RECORD")
        assert not result.is_success

        # Unknown message type
        result = instance.flext_meltano_create_singer_message("INVALID")
        assert not result.is_success

    def test_validate_singer_message_success(self, sample_singer_messages) -> None:
        """Test validating valid Singer messages."""

        class TestClass(FlextMeltanoSingerMixin):
            pass

        instance = TestClass()

        for message in sample_singer_messages:
            result = instance.flext_meltano_validate_singer_message(message)
            assert result.is_success, f"Failed to validate {message['type']} message"

    def test_validate_singer_message_invalid(self) -> None:
        """Test validating invalid Singer messages."""

        class TestClass(FlextMeltanoSingerMixin):
            pass

        instance = TestClass()

        # Missing type field
        result = instance.flext_meltano_validate_singer_message({"stream": "test"})
        assert not result.is_success

        # Missing required fields for RECORD
        result = instance.flext_meltano_validate_singer_message({"type": "RECORD"})
        assert not result.is_success

        # Unknown message type
        result = instance.flext_meltano_validate_singer_message({"type": "INVALID"})
        assert not result.is_success

    def test_process_singer_stream(self, sample_singer_messages) -> None:
        """Test processing Singer tap output stream."""

        class TestClass(FlextMeltanoSingerMixin):
            pass

        instance = TestClass()

        # Create tap output string
        tap_output = "\n".join(json.dumps(msg) for msg in sample_singer_messages)

        result = instance.flext_meltano_process_singer_stream(tap_output)

        assert result.is_success
        data = result.data

        # Check records
        assert data["total_records"] == 2
        assert len(data["records"]) == 2
        assert data["records"][0]["record"]["name"] == "Alice"

        # Check schemas
        assert "users" in data["schemas"]
        assert data["schemas"]["users"]["key_properties"] == ["id"]

        # Check state
        assert data["state"] is not None
        assert "bookmarks" in data["state"]

        # Check streams
        assert data["streams"] == ["users"]

    def test_process_singer_stream_with_errors(self) -> None:
        """Test processing Singer stream with invalid JSON."""

        class TestClass(FlextMeltanoSingerMixin):
            pass

        instance = TestClass()

        # Include invalid JSON line
        tap_output = """{"type": "SCHEMA", "stream": "test", "schema": {}}
invalid json line
{"type": "RECORD", "stream": "test", "record": {"id": 1}}"""

        result = instance.flext_meltano_process_singer_stream(tap_output)

        assert result.is_success
        data = result.data

        # Should have errors reported
        assert "errors" in data
        assert len(data["errors"]) == 1
        assert "Invalid JSON" in data["errors"][0]

        # Should still process valid messages
        assert data["total_records"] == 1


# =============================================================================
# TESTS FOR EXECUTION MIXIN
# =============================================================================


class TestFlextMeltanoExecutionMixin:
    """Test execution mixin functionality."""

    def test_execution_mixin_initialization(self) -> None:
        """Test execution mixin initializes correctly."""

        class TestClass(FlextMeltanoExecutionMixin):
            pass

        instance = TestClass()
        assert hasattr(instance, "_execution_state")
        assert hasattr(instance, "_execution_metrics")

    def test_validate_meltano_project_valid(self, temp_meltano_project) -> None:
        """Test validating valid Meltano project structure."""

        class TestClass(FlextMeltanoExecutionMixin):
            pass

        instance = TestClass()

        is_valid = instance._validate_meltano_project(temp_meltano_project)
        assert is_valid

    def test_validate_meltano_project_missing_file(self, tmp_path) -> None:
        """Test validating Meltano project with missing meltano.yml."""

        class TestClass(FlextMeltanoExecutionMixin):
            pass

        instance = TestClass()

        is_valid = instance._validate_meltano_project(tmp_path)
        assert not is_valid

    def test_validate_meltano_project_invalid_yml(self, tmp_path) -> None:
        """Test validating Meltano project with invalid YAML."""

        class TestClass(FlextMeltanoExecutionMixin):
            pass

        instance = TestClass()

        # Create invalid YAML file
        meltano_yml = tmp_path / "meltano.yml"
        meltano_yml.write_text("invalid: yaml: content:")

        is_valid = instance._validate_meltano_project(tmp_path)
        assert not is_valid

    @patch("subprocess.run")
    def test_run_meltano_elt_success(self, mock_run) -> None:
        """Test successful Meltano ELT execution."""

        class TestClass(FlextMeltanoExecutionMixin):
            pass

        instance = TestClass()

        # Mock successful subprocess result
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "INFO Replicated 100 records\nPipeline completed successfully"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = instance._run_meltano_elt(
            Path("/test"), "tap-postgres", "target-jsonl",
        )

        assert result["success"]
        assert result["records_processed"] == 100
        assert result["output"] == mock_result.stdout
        assert result["return_code"] == 0

        # Verify subprocess was called correctly
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == ["meltano", "elt", "tap-postgres", "target-jsonl"]

    @patch("subprocess.run")
    def test_run_meltano_elt_failure(self, mock_run) -> None:
        """Test failed Meltano ELT execution."""

        class TestClass(FlextMeltanoExecutionMixin):
            pass

        instance = TestClass()

        # Mock failed subprocess result
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "ERROR: Connection to database failed"
        mock_run.return_value = mock_result

        result = instance._run_meltano_elt(
            Path("/test"), "tap-postgres", "target-jsonl",
        )

        assert not result["success"]
        assert result["records_processed"] == 0
        assert result["error"] == mock_result.stderr
        assert result["return_code"] == 1

    @patch("subprocess.run")
    def test_run_meltano_elt_timeout(self, mock_run) -> None:
        """Test Meltano ELT execution timeout."""

        class TestClass(FlextMeltanoExecutionMixin):
            pass

        instance = TestClass()

        # Mock timeout exception
        mock_run.side_effect = subprocess.TimeoutExpired(
            ["meltano", "elt"], 3600,
        )

        result = instance._run_meltano_elt(
            Path("/test"), "tap-postgres", "target-jsonl",
        )

        assert not result["success"]
        assert "timeout" in result["error"]
        assert result["return_code"] == -1

    def test_extract_record_count(self) -> None:
        """Test extracting record count from Meltano output."""

        class TestClass(FlextMeltanoExecutionMixin):
            pass

        instance = TestClass()

        # Test various output patterns
        outputs = [
            "INFO Replicated 150 records",
            "Processed 75 records successfully",
            "Loaded 200 records to target",
            "No record count information",
        ]

        expected = [150, 75, 200, 0]

        for output, expected_count in zip(outputs, expected, strict=False):
            count = instance._extract_record_count(output)
            assert count == expected_count

    @pytest.mark.asyncio
    @patch("flext_meltano.patterns.FlextMeltanoExecutionMixin._validate_meltano_project")
    @patch("flext_meltano.patterns.FlextMeltanoExecutionMixin._run_meltano_elt")
    async def test_execute_pipeline_success(self, mock_run_elt, mock_validate) -> None:
        """Test successful pipeline execution."""

        class TestClass(FlextMeltanoExecutionMixin):
            pass

        instance = TestClass()

        # Mock successful validation and execution
        mock_validate.return_value = True
        mock_run_elt.return_value = {
            "success": True,
            "records_processed": 150,
            "duration_seconds": 45.5,
            "output": "Pipeline completed",
            "error": "",
        }

        result = await instance.flext_meltano_execute_pipeline(
            "tap-postgres", "target-jsonl",
        )

        assert result.is_success
        data = result.data
        assert data["status"] == "completed"
        assert data["records_processed"] == 150
        assert data["pipeline_id"] == "tap-postgres_to_target-jsonl"


# =============================================================================
# TESTS FOR PIPELINE BUILDER
# =============================================================================


class TestFlextMeltanoPipelineBuilder:
    """Test pipeline builder functionality."""

    def test_pipeline_builder_initialization(self) -> None:
        """Test pipeline builder initializes correctly."""
        builder = FlextMeltanoPipelineBuilder()

        assert builder._tap_name == ""
        assert builder._target_name == "target-jsonl"
        assert isinstance(builder._overrides, dict)
        assert isinstance(builder._project_root, Path)

    def test_fluent_postgres_configuration(self) -> None:
        """Test fluent PostgreSQL tap configuration."""
        builder = FlextMeltanoPipelineBuilder()

        result_builder = builder.from_postgres(
            host="localhost",
            port=5432,
            user="postgres",
            database="test",
            password="secret",
        )

        # Should return same builder for chaining
        assert result_builder is builder
        assert builder._tap_name == "tap-postgres"
        assert "tap_config" in builder._overrides
        assert builder._overrides["tap_config"]["host"] == "localhost"
        assert builder._overrides["tap_config"]["port"] == 5432

    def test_fluent_mysql_configuration(self) -> None:
        """Test fluent MySQL tap configuration."""
        builder = FlextMeltanoPipelineBuilder()

        result_builder = builder.from_mysql(
            host="mysql-server", database="production",
        )

        assert result_builder is builder
        assert builder._tap_name == "tap-mysql"
        assert builder._overrides["tap_config"]["host"] == "mysql-server"
        assert builder._overrides["tap_config"]["database"] == "production"

    def test_fluent_oracle_configuration(self) -> None:
        """Test fluent Oracle tap configuration."""
        builder = FlextMeltanoPipelineBuilder()

        result_builder = builder.from_oracle(
            host="oracle-server", user="system", sid="xe",
        )

        assert result_builder is builder
        assert builder._tap_name == "tap-oracle"
        assert builder._overrides["tap_config"]["host"] == "oracle-server"

    def test_fluent_csv_configuration(self) -> None:
        """Test fluent CSV tap configuration."""
        builder = FlextMeltanoPipelineBuilder()

        files = [{"entity": "users", "path": "users.csv", "keys": ["id"]}]
        result_builder = builder.from_csv(files=files)

        assert result_builder is builder
        assert builder._tap_name == "tap-csv"
        assert builder._overrides["tap_config"]["files"] == files

    def test_fluent_custom_tap_configuration(self) -> None:
        """Test fluent custom tap configuration."""
        builder = FlextMeltanoPipelineBuilder()

        result_builder = builder.from_custom_tap(
            "tap-salesforce", client_id="test", client_secret="secret",
        )

        assert result_builder is builder
        assert builder._tap_name == "tap-salesforce"
        assert builder._overrides["tap_config"]["client_id"] == "test"

    def test_fluent_jsonl_target_configuration(self) -> None:
        """Test fluent JSONL target configuration."""
        builder = FlextMeltanoPipelineBuilder()

        result_builder = builder.to_jsonl(
            destination_path="/data/exports", overwrite_behavior="replace_file",
        )

        assert result_builder is builder
        assert builder._target_name == "target-jsonl"
        assert builder._overrides["target_config"]["destination_path"] == "/data/exports"

    def test_fluent_csv_target_configuration(self) -> None:
        """Test fluent CSV target configuration."""
        builder = FlextMeltanoPipelineBuilder()

        result_builder = builder.to_csv(
            destination_path="/exports", delimiter="|", quotechar="'",
        )

        assert result_builder is builder
        assert builder._target_name == "target-csv"
        assert builder._overrides["target_config"]["delimiter"] == "|"

    def test_fluent_parquet_target_configuration(self) -> None:
        """Test fluent Parquet target configuration."""
        builder = FlextMeltanoPipelineBuilder()

        result_builder = builder.to_parquet(
            destination_path="/data", compression="gzip",
        )

        assert result_builder is builder
        assert builder._target_name == "target-parquet"
        assert builder._overrides["target_config"]["compression"] == "gzip"

    def test_fluent_project_configuration(self) -> None:
        """Test fluent project configuration."""
        builder = FlextMeltanoPipelineBuilder()
        project_path = "/path/to/meltano/project"

        result_builder = builder.in_project(project_path)

        assert result_builder is builder
        assert builder._project_root == Path(project_path)
        assert builder._overrides["project_root"] == builder._project_root

    def test_fluent_environment_configuration(self) -> None:
        """Test fluent environment configuration."""
        builder = FlextMeltanoPipelineBuilder()

        result_builder = builder.with_environment("production")

        assert result_builder is builder
        assert builder._overrides["environment"] == "production"

    def test_fluent_custom_configuration(self) -> None:
        """Test fluent custom configuration."""
        builder = FlextMeltanoPipelineBuilder()

        result_builder = builder.with_custom_config(
            timeout=300, batch_size=1000, debug=True,
        )

        assert result_builder is builder
        assert builder._overrides["timeout"] == 300
        assert builder._overrides["batch_size"] == 1000
        assert builder._overrides["debug"] is True

    def test_build_config(self) -> None:
        """Test building configuration without execution."""
        builder = (FlextMeltanoPipelineBuilder()
                  .from_postgres(host="localhost", database="test")
                  .to_jsonl(destination_path="./output"))

        result = builder.build_config()

        assert result.is_success
        config = result.data
        assert config["tap_name"] == "tap-postgres"
        assert config["target_name"] == "target-jsonl"
        assert "tap_config" in config
        assert "target_config" in config

    def test_run_without_tap_configuration(self) -> None:
        """Test running pipeline without tap configuration."""
        builder = FlextMeltanoPipelineBuilder()

        result = builder.run_sync()

        assert not result.is_success
        assert "Tap name not configured" in result.error

    @patch("flext_meltano.patterns.FlextMeltanoPipelineBuilder._run_meltano_discover")
    def test_discover_success(self, mock_discover) -> None:
        """Test successful tap discovery."""
        builder = FlextMeltanoPipelineBuilder().from_postgres(
            host="localhost", database="test",
        )

        # Mock successful discovery
        mock_discover.return_value = {
            "catalog": {"streams": [{"tap_stream_id": "users"}]},
            "streams": ["users"],
            "total_streams": 1,
        }

        result = builder.discover()

        assert result.is_success
        data = result.data
        assert data["total_streams"] == 1
        assert "users" in data["streams"]

    def test_discover_without_tap(self) -> None:
        """Test discovery without tap configuration."""
        builder = FlextMeltanoPipelineBuilder()

        result = builder.discover()

        assert not result.is_success
        assert "Tap name not configured" in result.error

    @patch("flext_meltano.patterns.FlextMeltanoPipelineBuilder._test_meltano_connection")
    def test_connection_test_success(self, mock_test) -> None:
        """Test successful connection test."""
        builder = FlextMeltanoPipelineBuilder().from_postgres(
            host="localhost", database="test",
        )

        # Mock successful connection test
        mock_test.return_value = {
            "connection_ok": True,
            "tap_available": True,
            "help_output": "tap-postgres --help output",
        }

        result = builder.test_connection()

        assert result.is_success
        data = result.data
        assert data["connection_ok"]
        assert data["tap_available"]


# =============================================================================
# TESTS FOR SERVICE CLASSES
# =============================================================================


class TestFlextMeltanoConfigService:
    """Test configuration service functionality."""

    def test_config_service_initialization(self) -> None:
        """Test config service initializes correctly."""
        service = FlextMeltanoConfigService()

        assert hasattr(service, "_schema_registry")
        assert hasattr(service, "_config_templates")

    def test_config_service_execute(self) -> None:
        """Test config service execute method."""
        service = FlextMeltanoConfigService()

        result = service.execute()

        assert result.is_success
        data = result.data
        assert data["service"] == "FlextMeltanoConfigService"
        assert data["status"] == "ready"
        assert data["templates_loaded"] > 0
        assert data["schemas_loaded"] > 0

    def test_get_tap_config_template_postgres(self) -> None:
        """Test getting PostgreSQL tap config template."""
        service = FlextMeltanoConfigService()

        result = service.get_tap_config_template(
            "postgres", host="custom-host", port=5433,
        )

        assert result.is_success
        config = result.data
        assert config["host"] == "custom-host"
        assert config["port"] == 5433
        assert "database" in config  # From template

    def test_get_tap_config_template_unknown(self) -> None:
        """Test getting unknown tap config template."""
        service = FlextMeltanoConfigService()

        result = service.get_tap_config_template("unknown_tap")

        assert not result.is_success
        assert "Unknown tap type" in result.error

    def test_get_target_config_template_jsonl(self) -> None:
        """Test getting JSONL target config template."""
        service = FlextMeltanoConfigService()

        result = service.get_target_config_template(
            "jsonl", destination_path="/custom/path",
        )

        assert result.is_success
        config = result.data
        assert config["destination_path"] == "/custom/path"
        assert "file_naming_scheme" in config  # From template

    def test_get_target_config_template_unknown(self) -> None:
        """Test getting unknown target config template."""
        service = FlextMeltanoConfigService()

        result = service.get_target_config_template("unknown_target")

        assert not result.is_success
        assert "Unknown target type" in result.error


class TestFlextMeltanoExecutionService:
    """Test execution service functionality."""

    def test_execution_service_initialization(self) -> None:
        """Test execution service initializes correctly."""
        config_service = FlextMeltanoConfigService()
        service = FlextMeltanoExecutionService(config_service)

        assert service.config_service is config_service

    def test_execution_service_execute(self) -> None:
        """Test execution service execute method."""
        config_service = FlextMeltanoConfigService()
        service = FlextMeltanoExecutionService(config_service)

        result = service.execute()

        assert result.is_success
        data = result.data
        assert data["service"] == "FlextMeltanoExecutionService"
        assert data["config_service_status"] == "injected"


# =============================================================================
# TESTS FOR FACTORY FUNCTIONS
# =============================================================================


class TestFactoryFunctions:
    """Test factory functions for creating instances."""

    def test_create_pipeline(self) -> None:
        """Test creating pipeline builder."""
        builder = create_flext_meltano_pipeline()

        assert isinstance(builder, FlextMeltanoPipelineBuilder)
        assert builder._tap_name == ""
        assert builder._target_name == "target-jsonl"

    def test_create_config_service(self) -> None:
        """Test creating config service."""
        service = create_flext_meltano_config_service()

        assert isinstance(service, FlextMeltanoConfigService)

    def test_create_execution_service_with_config(self) -> None:
        """Test creating execution service with provided config service."""
        config_service = FlextMeltanoConfigService()
        service = create_flext_meltano_execution_service(config_service)

        assert isinstance(service, FlextMeltanoExecutionService)
        assert service.config_service is config_service

    def test_create_execution_service_without_config(self) -> None:
        """Test creating execution service without config service."""
        service = create_flext_meltano_execution_service()

        assert isinstance(service, FlextMeltanoExecutionService)
        assert isinstance(service.config_service, FlextMeltanoConfigService)


# =============================================================================
# TESTS FOR DECORATORS
# =============================================================================


class TestDecorators:
    """Test decorator functionality."""

    def test_safe_operation_decorator_success(self) -> None:
        """Test safe operation decorator with successful function."""

        @flext_meltano_safe_operation("test_operation")
        def successful_function():
            return {"result": "success", "value": 42}

        result = successful_function()

        assert isinstance(result, FlextResult)
        assert result.is_success
        assert result.data["result"] == "success"
        assert result.data["value"] == 42

    def test_safe_operation_decorator_failure(self) -> None:
        """Test safe operation decorator with failing function."""

        @flext_meltano_safe_operation("failing_operation")
        def failing_function() -> Never:
            msg = "Test error message"
            raise ValueError(msg)

        result = failing_function()

        assert isinstance(result, FlextResult)
        assert not result.is_success
        assert "Test error message" in result.error
        assert "failing_operation failed" in result.error


# =============================================================================
# TESTS FOR VALUE OBJECTS
# =============================================================================


class TestFlextMeltanoPipelineConfig:
    """Test pipeline configuration value object."""

    def test_pipeline_config_creation(self) -> None:
        """Test creating pipeline configuration."""
        config = FlextMeltanoPipelineConfig(
            tap_name="tap-postgres",
            target_name="target-jsonl",
            project_root=Path("/test"),
            environment="dev",
            tap_config={"host": "localhost"},
            target_config={"destination_path": "./output"},
        )

        assert config.tap_name == "tap-postgres"
        assert config.target_name == "target-jsonl"
        assert config.project_root == Path("/test")
        assert config.environment == "dev"
        assert config.tap_config["host"] == "localhost"

    def test_pipeline_config_defaults(self) -> None:
        """Test pipeline configuration with default values."""
        config = FlextMeltanoPipelineConfig(
            tap_name="tap-mysql", target_name="target-csv",
        )

        assert config.environment == "dev"
        assert config.tap_config == {}
        assert config.target_config == {}
        assert isinstance(config.project_root, Path)

    def test_pipeline_config_validation_empty_tap_name(self) -> None:
        """Test pipeline configuration validation with empty tap name."""
        config = FlextMeltanoPipelineConfig(tap_name="", target_name="target-jsonl")

        with pytest.raises(ValueError, match="tap_name is required"):
            config.validate_domain_rules()

    def test_pipeline_config_validation_empty_target_name(self) -> None:
        """Test pipeline configuration validation with empty target name."""
        config = FlextMeltanoPipelineConfig(tap_name="tap-postgres", target_name="")

        with pytest.raises(ValueError, match="target_name is required"):
            config.validate_domain_rules()

    def test_pipeline_config_validation_nonexistent_path(self) -> None:
        """Test pipeline configuration validation with nonexistent path."""
        config = FlextMeltanoPipelineConfig(
            tap_name="tap-postgres",
            target_name="target-jsonl",
            project_root=Path("/nonexistent/path"),
        )

        with pytest.raises(ValueError, match="project_root does not exist"):
            config.validate_domain_rules()


# =============================================================================
# INTEGRATION TESTS
# =============================================================================


class TestIntegration:
    """Integration tests combining multiple components."""

    def test_full_pipeline_configuration_flow(self) -> None:
        """Test complete pipeline configuration flow."""
        # Create config service
        config_service = create_flext_meltano_config_service()

        # Get templates
        tap_config_result = config_service.get_tap_config_template(
            "postgres", host="integration-db", database="test_db",
        )
        target_config_result = config_service.get_target_config_template(
            "jsonl", destination_path="./integration_output",
        )

        assert tap_config_result.is_success
        assert target_config_result.is_success

        # Create pipeline with templates
        builder = (create_flext_meltano_pipeline()
                  .from_postgres(**tap_config_result.data)
                  .to_jsonl(**target_config_result.data)
                  .with_environment("integration"))

        # Build final config
        config_result = builder.build_config()
        assert config_result.is_success

        final_config = config_result.data
        assert final_config["tap_name"] == "tap-postgres"
        assert final_config["target_name"] == "target-jsonl"
        assert final_config["environment"] == "integration"
        assert final_config["tap_config"]["host"] == "integration-db"

    def test_singer_message_pipeline_processing(self, sample_singer_messages) -> None:
        """Test processing Singer messages through pipeline components."""

        class TestPipeline(FlextMeltanoSingerMixin):
            pass

        pipeline = TestPipeline()

        # Process messages individually
        valid_messages = []
        for message in sample_singer_messages:
            validation = pipeline.flext_meltano_validate_singer_message(message)
            if validation.is_success:
                valid_messages.append(message)

        assert len(valid_messages) == len(sample_singer_messages)

        # Process as stream
        tap_output = "\n".join(json.dumps(msg) for msg in sample_singer_messages)
        stream_result = pipeline.flext_meltano_process_singer_stream(tap_output)

        assert stream_result.is_success
        data = stream_result.data
        assert data["total_records"] == 2
        assert len(data["schemas"]) == 1
        assert data["state"] is not None
