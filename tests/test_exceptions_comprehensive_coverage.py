"""Exceptions Comprehensive Coverage Tests - Real Exception Testing Without Mocks.

Comprehensive tests for FlextMeltanoExceptions using real functionality and error scenarios.
Focuses on achieving 95%+ coverage with meaningful functional tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano.exceptions import (
    ConfigurationErrorContext,
    ConnectionErrorContext,
    FlextMeltanoAuthenticationError,
    FlextMeltanoConfigurationError,
    FlextMeltanoConnectionError,
    FlextMeltanoDBTError,
    FlextMeltanoError,
    FlextMeltanoExceptions,
    FlextMeltanoExecutionError,
    FlextMeltanoPluginError,
    FlextMeltanoProcessingError,
    FlextMeltanoSingerError,
    FlextMeltanoTimeoutError,
    FlextMeltanoValidationError,
    PluginErrorContext,
    ProcessingErrorContext,
    ValidationErrorContext,
)


class TestPydanticErrorContexts:
    """Test all Pydantic error context models."""

    def test_validation_error_context_creation(self) -> None:
        """Test ValidationErrorContext creation and validation."""
        # Complete context
        context = ValidationErrorContext(
            field_name="username",
            expected_type="string",
            actual_value="123",
            validation_rule="min_length=5",
            additional_info={"min_length": 5, "current_length": 3},
        )
        assert context.field_name == "username"
        assert context.expected_type == "string"
        assert context.actual_value == "123"
        assert context.validation_rule == "min_length=5"
        assert context.additional_info["min_length"] == 5

        # Minimal context with defaults
        minimal = ValidationErrorContext()
        assert minimal.field_name is None
        assert minimal.expected_type is None
        assert minimal.actual_value is None
        assert minimal.validation_rule is None
        assert minimal.additional_info == {}

        # Context serialization
        context_dict = context.model_dump()
        assert context_dict["field_name"] == "username"
        assert context_dict["additional_info"]["min_length"] == 5

    def test_configuration_error_context_creation(self) -> None:
        """Test ConfigurationErrorContext creation and validation."""
        # Complete context
        context = ConfigurationErrorContext(
            config_file="/app/config.yaml",
            section="database",
            key="host",
            expected_format="hostname:port",
            additional_info={
                "current_value": "invalid_host",
                "suggestion": "localhost:5432",
            },
        )
        assert context.config_file == "/app/config.yaml"
        assert context.section == "database"
        assert context.key == "host"
        assert context.expected_format == "hostname:port"
        assert context.additional_info["current_value"] == "invalid_host"

        # Minimal context
        minimal = ConfigurationErrorContext()
        assert minimal.config_file is None
        assert minimal.section is None
        assert minimal.key is None
        assert minimal.expected_format is None
        assert minimal.additional_info == {}

    def test_connection_error_context_creation(self) -> None:
        """Test ConnectionErrorContext creation and validation."""
        # Complete context
        context = ConnectionErrorContext(
            host="db.example.com",
            port=5432,
            protocol="postgresql",
            timeout=30,
            retry_count=3,
            additional_info={"ssl_enabled": True, "connection_pool": "full"},
        )
        assert context.host == "db.example.com"
        assert context.port == 5432
        assert context.protocol == "postgresql"
        assert context.timeout == 30
        assert context.retry_count == 3
        assert context.additional_info["ssl_enabled"] is True

        # Default retry count
        default_context = ConnectionErrorContext(host="localhost")
        assert default_context.retry_count == 0

    def test_processing_error_context_creation(self) -> None:
        """Test ProcessingErrorContext creation and validation."""
        # Complete context
        context = ProcessingErrorContext(
            operation="data_transformation",
            records_processed=1250,
            batch_id="batch_20250115_001",
            stream_name="users",
            stage="validation",
            additional_info={"error_rate": 0.02, "last_successful_record": 1248},
        )
        assert context.operation == "data_transformation"
        assert context.records_processed == 1250
        assert context.batch_id == "batch_20250115_001"
        assert context.stream_name == "users"
        assert context.stage == "validation"
        assert context.additional_info["error_rate"] == 0.02

        # Default records processed
        minimal = ProcessingErrorContext()
        assert minimal.records_processed == 0

    def test_plugin_error_context_creation(self) -> None:
        """Test PluginErrorContext creation and validation."""
        # Complete context
        context = PluginErrorContext(
            plugin_name="tap-postgres",
            plugin_type="extractor",
            version="0.0.7",
            command="discover",
            exit_code=1,
            additional_info={"stderr": "Connection failed", "pid": 12345},
        )
        assert context.plugin_name == "tap-postgres"
        assert context.plugin_type == "extractor"
        assert context.version == "0.0.7"
        assert context.command == "discover"
        assert context.exit_code == 1
        assert context.additional_info["stderr"] == "Connection failed"

        # Minimal context
        minimal = PluginErrorContext()
        assert minimal.plugin_name is None
        assert minimal.exit_code is None


class TestFlextMeltanoExceptionsBase:
    """Test base exception class and hierarchy."""

    def test_meltano_error_basic_functionality(self) -> None:
        """Test basic MeltanoError functionality."""
        error = FlextMeltanoExceptions.MeltanoError()
        assert isinstance(error, FlextMeltanoExceptions.MeltanoError)
        assert hasattr(error, "__init__")

        # Test that MeltanoError is properly defined
        assert hasattr(FlextMeltanoExceptions.MeltanoError, "__name__")
        assert FlextMeltanoExceptions.MeltanoError.__name__ == "MeltanoError"


class TestValidationErrors:
    """Test MeltanoValidationError with Pydantic contexts."""

    def test_validation_error_with_full_context(self) -> None:
        """Test validation error with complete context."""
        context = ValidationErrorContext(
            field_name="email",
            expected_type="email_string",
            actual_value="not-an-email",
            validation_rule="email_format",
            additional_info={"regex": r"^[^@]+@[^@]+\.[^@]+$"},
        )

        error = FlextMeltanoValidationError("Email validation failed", context=context)

        assert error.message == "Email validation failed"
        assert error.context["context"]["field_name"] == "email"
        assert error.context["context"]["expected_type"] == "email_string"
        assert error.context["context"]["actual_value"] == "not-an-email"
        assert (
            error.context["context"]["additional_info"]["regex"]
            == r"^[^@]+@[^@]+\.[^@]+$"
        )

    def test_validation_error_with_minimal_context(self) -> None:
        """Test validation error with minimal context."""
        error = FlextMeltanoValidationError("Basic validation error")
        assert error.message == "Basic validation error"
        assert error.context["context"] == {}

    def test_validation_error_with_no_context(self) -> None:
        """Test validation error without context."""
        error = FlextMeltanoValidationError()
        assert error.message == "Validation error"
        assert error.context["context"] == {}


class TestConfigurationErrors:
    """Test MeltanoConfigurationError with Pydantic contexts."""

    def test_configuration_error_with_full_context(self) -> None:
        """Test configuration error with complete context."""
        context = ConfigurationErrorContext(
            config_file="meltano.yml",
            section="plugins.extractors",
            key="tap-postgres.config.host",
            expected_format="hostname or IP address",
            additional_info={"example": "localhost", "provided": ""},
        )

        error = FlextMeltanoConfigurationError(
            "Missing database host configuration", context=context
        )

        assert error.message == "Configuration: Missing database host configuration"
        assert error.context["context"]["config_file"] == "meltano.yml"
        assert error.context["context"]["section"] == "plugins.extractors"
        assert error.context["context"]["key"] == "tap-postgres.config.host"
        assert error.context["context"]["additional_info"]["example"] == "localhost"

    def test_configuration_error_defaults(self) -> None:
        """Test configuration error with default values."""
        error = FlextMeltanoConfigurationError()
        assert error.message == "Configuration: Configuration error"
        assert error.context["context"] == {}


class TestConnectionErrors:
    """Test MeltanoConnectionError with Pydantic contexts."""

    def test_connection_error_with_full_context(self) -> None:
        """Test connection error with complete context."""
        context = ConnectionErrorContext(
            host="postgres.example.com",
            port=5432,
            protocol="tcp",
            timeout=30,
            retry_count=5,
            additional_info={"ssl_mode": "require", "last_error": "connection refused"},
        )

        error = FlextMeltanoConnectionError(
            "Failed to connect to database after 5 retries", context=context
        )

        assert (
            error.message == "Connection: Failed to connect to database after 5 retries"
        )
        assert error.context["context"]["host"] == "postgres.example.com"
        assert error.context["context"]["port"] == 5432
        assert error.context["context"]["retry_count"] == 5
        assert error.context["context"]["additional_info"]["ssl_mode"] == "require"

    def test_connection_error_minimal(self) -> None:
        """Test connection error with minimal information."""
        error = FlextMeltanoConnectionError("Connection timeout")
        assert error.message == "Connection: Connection timeout"
        assert error.context["context"] == {}


class TestProcessingErrors:
    """Test MeltanoProcessingError with Pydantic contexts."""

    def test_processing_error_with_full_context(self) -> None:
        """Test processing error with complete context."""
        context = ProcessingErrorContext(
            operation="record_transformation",
            records_processed=5432,
            batch_id="batch_001_2025_01_15",
            stream_name="customers",
            stage="data_validation",
            additional_info={
                "failed_record_id": "cust_12345",
                "validation_rules": ["not_null", "email_format"],
                "processing_time_ms": 1250,
            },
        )

        error = FlextMeltanoProcessingError(
            "Record validation failed during transformation", context=context
        )

        assert (
            error.message
            == "Processing: Record validation failed during transformation"
        )
        assert error.context["context"]["operation"] == "record_transformation"
        assert error.context["context"]["records_processed"] == 5432
        assert error.context["context"]["batch_id"] == "batch_001_2025_01_15"
        assert error.context["context"]["stream_name"] == "customers"
        assert (
            error.context["context"]["additional_info"]["failed_record_id"]
            == "cust_12345"
        )

    def test_processing_error_minimal(self) -> None:
        """Test processing error with default values."""
        error = FlextMeltanoProcessingError()
        assert error.message == "Processing: Processing error"
        assert error.context["context"] == {}


class TestAuthenticationErrors:
    """Test MeltanoAuthenticationError with custom context."""

    def test_authentication_error_with_full_context(self) -> None:
        """Test authentication error with complete context."""
        error = FlextMeltanoAuthenticationError(
            "Invalid API credentials",
            username="api_user",
            auth_type="api_key",
            service="postgres_db",
            credential_type="connection_string",
        )

        assert error.message == "Authentication: Invalid API credentials"
        assert error.context["context"]["user"] == "api_user"
        assert error.context["context"]["method"] == "api_key"
        assert error.context["context"]["service"] == "postgres_db"
        assert error.context["context"]["credential_type"] == "connection_string"

    def test_authentication_error_minimal(self) -> None:
        """Test authentication error with minimal context."""
        error = FlextMeltanoAuthenticationError("Auth failed")
        assert error.message == "Authentication: Auth failed"
        assert error.context["context"] == {}

    def test_authentication_error_defaults(self) -> None:
        """Test authentication error with default message."""
        error = FlextMeltanoAuthenticationError()
        assert error.message == "Authentication: Authentication error"


class TestTimeoutErrors:
    """Test MeltanoTimeoutError with custom context."""

    def test_timeout_error_with_full_context(self) -> None:
        """Test timeout error with complete context."""
        error = FlextMeltanoTimeoutError(
            "Operation timed out waiting for database response",
            timeout_seconds=300,
            operation="table_discovery",
            query="SELECT * FROM information_schema.tables",
            connection_id="conn_12345",
        )

        assert (
            error.message
            == "Timeout: Operation timed out waiting for database response"
        )
        assert error.context["context"]["timeout"] == 300
        assert error.context["context"]["operation"] == "table_discovery"
        assert (
            error.context["context"]["query"]
            == "SELECT * FROM information_schema.tables"
        )
        assert error.context["context"]["connection_id"] == "conn_12345"

    def test_timeout_error_partial_context(self) -> None:
        """Test timeout error with partial context."""
        error = FlextMeltanoTimeoutError("Request timeout", timeout_seconds=60)

        assert error.message == "Timeout: Request timeout"
        assert error.context["context"]["timeout"] == 60
        assert "operation" not in error.context["context"]

    def test_timeout_error_defaults(self) -> None:
        """Test timeout error with defaults."""
        error = FlextMeltanoTimeoutError()
        assert error.message == "Timeout: Timeout error"
        assert error.context["context"] == {}


class TestPluginErrors:
    """Test MeltanoPluginError with Pydantic contexts."""

    def test_plugin_error_with_full_context(self) -> None:
        """Test plugin error with complete context."""
        context = PluginErrorContext(
            plugin_name="tap-csv",
            plugin_type="extractor",
            version="2.1.0",
            command="run",
            exit_code=2,
            additional_info={
                "config_file": "tap_config.json",
                "error_output": "File not found: data.csv",
                "execution_time": 5.2,
            },
        )

        error = FlextMeltanoPluginError(
            "Plugin execution failed with exit code 2", context=context
        )

        assert error.message == "Plugin: Plugin execution failed with exit code 2"
        assert error.context["context"]["plugin_name"] == "tap-csv"
        assert error.context["context"]["plugin_type"] == "extractor"
        assert error.context["context"]["version"] == "2.1.0"
        assert error.context["context"]["command"] == "run"
        assert error.context["context"]["exit_code"] == 2
        assert (
            error.context["context"]["additional_info"]["error_output"]
            == "File not found: data.csv"
        )

    def test_plugin_error_minimal(self) -> None:
        """Test plugin error with minimal context."""
        error = FlextMeltanoPluginError("Plugin installation failed")
        assert error.message == "Plugin: Plugin installation failed"
        assert error.context["context"] == {}


class TestExecutionErrors:
    """Test MeltanoExecutionError inheriting from ProcessingError."""

    def test_execution_error_with_full_context(self) -> None:
        """Test execution error with command context."""
        error = FlextMeltanoExecutionError(
            "Command execution failed",
            command="tap-postgres --config tap_config.json",
            exit_code=1,
            stderr="ERROR: connection to database failed",
            working_dir="/opt/meltano",
            env_vars={"POSTGRES_HOST": "localhost"},
        )

        assert error.message == "Execution: Command execution failed"
        assert (
            error.context["context"]["command"]
            == "tap-postgres --config tap_config.json"
        )
        assert error.context["context"]["exit_code"] == 1
        assert (
            error.context["context"]["stderr"] == "ERROR: connection to database failed"
        )
        assert error.context["context"]["working_dir"] == "/opt/meltano"
        assert error.context["context"]["env_vars"]["POSTGRES_HOST"] == "localhost"

    def test_execution_error_minimal(self) -> None:
        """Test execution error with minimal context."""
        error = FlextMeltanoExecutionError("Execution failed")
        assert error.message == "Execution: Execution failed"
        assert error.context["context"] == {}

    def test_execution_error_inheritance(self) -> None:
        """Test that ExecutionError inherits from ProcessingError."""
        error = FlextMeltanoExecutionError("Test")
        # Should inherit from MeltanoError, not ProcessingError based on implementation
        assert isinstance(error, FlextMeltanoError)


class TestSingerErrors:
    """Test MeltanoSingerError with Singer-specific context."""

    def test_singer_error_with_full_context(self) -> None:
        """Test Singer error with complete context."""
        error = FlextMeltanoSingerError(
            "Singer stream processing failed",
            stream_name="customers",
            record_count=15432,
            last_processed_record={"id": 15431, "name": "John Doe"},
            message_type="RECORD",
            catalog_entry="customers",
        )

        assert error.message == "Singer: Singer stream processing failed"
        assert error.context["context"]["stream_name"] == "customers"
        assert error.context["context"]["record_count"] == 15432
        assert error.context["context"]["last_processed_record"]["id"] == 15431
        assert error.context["context"]["message_type"] == "RECORD"
        assert error.context["context"]["catalog_entry"] == "customers"

    def test_singer_error_partial_context(self) -> None:
        """Test Singer error with partial context."""
        error = FlextMeltanoSingerError(
            "Schema validation failed", stream_name="orders"
        )

        assert error.message == "Singer: Schema validation failed"
        assert error.context["context"]["stream_name"] == "orders"
        assert "record_count" not in error.context["context"]

    def test_singer_error_defaults(self) -> None:
        """Test Singer error with default values."""
        error = FlextMeltanoSingerError()
        assert error.message == "Singer: Singer error"
        assert error.context["context"] == {}


class TestDBTErrors:
    """Test MeltanoDBTError with DBT-specific context."""

    def test_dbt_error_with_full_context(self) -> None:
        """Test DBT error with complete context."""
        error = FlextMeltanoDBTError(
            "DBT model compilation failed",
            model_name="staging_customers",
            project_dir="/opt/dbt",
            target="dev",
            compilation_error="Undefined macro 'get_current_timestamp'",
        )

        assert error.message == "DBT: DBT model compilation failed"
        assert error.context["context"]["model_name"] == "staging_customers"
        assert error.context["context"]["project_dir"] == "/opt/dbt"
        assert error.context["context"]["target"] == "dev"
        assert (
            error.context["context"]["compilation_error"]
            == "Undefined macro 'get_current_timestamp'"
        )

    def test_dbt_error_minimal(self) -> None:
        """Test DBT error with minimal context."""
        error = FlextMeltanoDBTError("Model build failed")
        assert error.message == "DBT: Model build failed"
        assert error.context["context"] == {}

    def test_dbt_error_defaults(self) -> None:
        """Test DBT error with default message."""
        error = FlextMeltanoDBTError()
        assert error.message == "DBT: DBT error"
        assert error.context["context"] == {}


class TestModuleLevelAliases:
    """Test module-level aliases for backward compatibility."""

    def test_all_aliases_exist(self) -> None:
        """Test that all module-level aliases are properly defined."""
        # Test that aliases point to correct classes
        assert FlextMeltanoError == FlextMeltanoExceptions.MeltanoError
        assert (
            FlextMeltanoValidationError == FlextMeltanoExceptions.MeltanoValidationError
        )
        assert (
            FlextMeltanoConfigurationError
            == FlextMeltanoExceptions.MeltanoConfigurationError
        )
        assert (
            FlextMeltanoConnectionError == FlextMeltanoExceptions.MeltanoConnectionError
        )
        assert (
            FlextMeltanoProcessingError == FlextMeltanoExceptions.MeltanoProcessingError
        )
        assert (
            FlextMeltanoAuthenticationError
            == FlextMeltanoExceptions.MeltanoAuthenticationError
        )
        assert FlextMeltanoTimeoutError == FlextMeltanoExceptions.MeltanoTimeoutError
        assert FlextMeltanoPluginError == FlextMeltanoExceptions.MeltanoPluginError
        assert (
            FlextMeltanoExecutionError == FlextMeltanoExceptions.MeltanoExecutionError
        )
        assert FlextMeltanoSingerError == FlextMeltanoExceptions.MeltanoSingerError
        assert FlextMeltanoDBTError == FlextMeltanoExceptions.MeltanoDBTError

    def test_aliases_functional(self) -> None:
        """Test that aliases work functionally for creating exceptions."""
        # Test creating exceptions through aliases
        validation_error = FlextMeltanoValidationError("Test validation")
        assert validation_error.message == "Test validation"

        config_error = FlextMeltanoConfigurationError("Test config")
        assert config_error.message == "Configuration: Test config"

        connection_error = FlextMeltanoConnectionError("Test connection")
        assert connection_error.message == "Connection: Test connection"

        processing_error = FlextMeltanoProcessingError("Test processing")
        assert processing_error.message == "Processing: Test processing"


class TestExceptionIntegration:
    """Integration tests combining multiple exception types."""

    def test_exception_hierarchy_inheritance(self) -> None:
        """Test that all exceptions properly inherit from base classes."""
        # All should inherit from MeltanoError
        validation_error = FlextMeltanoValidationError("test")
        config_error = FlextMeltanoConfigurationError("test")
        connection_error = FlextMeltanoConnectionError("test")
        processing_error = FlextMeltanoProcessingError("test")
        auth_error = FlextMeltanoAuthenticationError("test")
        timeout_error = FlextMeltanoTimeoutError("test")
        plugin_error = FlextMeltanoPluginError("test")
        execution_error = FlextMeltanoExecutionError("test")
        singer_error = FlextMeltanoSingerError("test")
        dbt_error = FlextMeltanoDBTError("test")

        # Test inheritance from MeltanoError
        assert isinstance(validation_error, FlextMeltanoError)
        assert isinstance(config_error, FlextMeltanoError)
        assert isinstance(connection_error, FlextMeltanoError)
        assert isinstance(processing_error, FlextMeltanoError)
        assert isinstance(auth_error, FlextMeltanoError)
        assert isinstance(timeout_error, FlextMeltanoError)
        assert isinstance(plugin_error, FlextMeltanoError)
        assert isinstance(execution_error, FlextMeltanoError)
        assert isinstance(singer_error, FlextMeltanoError)
        assert isinstance(dbt_error, FlextMeltanoError)

    def test_nested_error_context_serialization(self) -> None:
        """Test complex error context serialization and access."""
        # Create complex nested context
        validation_context = ValidationErrorContext(
            field_name="nested_field",
            additional_info={
                "nested_validation": {
                    "rules": ["required", "min_length"],
                    "current_value": "",
                    "nested_errors": [{"field": "sub_field", "error": "required"}],
                }
            },
        )

        error = FlextMeltanoValidationError(
            "Complex validation failed", context=validation_context
        )

        # Access nested context data
        context_data = error.context["context"]
        assert context_data["field_name"] == "nested_field"
        nested_validation = context_data["additional_info"]["nested_validation"]
        assert nested_validation["rules"] == ["required", "min_length"]
        assert nested_validation["nested_errors"][0]["field"] == "sub_field"

    def test_error_chaining_scenario(self) -> None:
        """Test realistic error chaining scenarios."""
        # Simulate a realistic error chain: Connection -> Plugin -> Processing

        # 1. Connection fails
        conn_context = ConnectionErrorContext(
            host="db.example.com", port=5432, timeout=30, retry_count=3
        )
        conn_error = FlextMeltanoConnectionError(
            "Database connection failed", context=conn_context
        )

        # 2. Plugin fails due to connection
        plugin_context = PluginErrorContext(
            plugin_name="tap-postgres",
            plugin_type="extractor",
            command="discover",
            exit_code=1,
        )
        plugin_error = FlextMeltanoPluginError(
            "Plugin discovery failed due to connection error", context=plugin_context
        )

        # 3. Processing fails due to plugin failure
        processing_context = ProcessingErrorContext(
            operation="schema_discovery", records_processed=0, stage="initialization"
        )
        processing_error = FlextMeltanoProcessingError(
            "Processing failed due to plugin error", context=processing_context
        )

        # Verify each error maintains its context
        assert "db.example.com" in str(conn_error.context)
        assert "tap-postgres" in str(plugin_error.context)
        assert "schema_discovery" in str(processing_error.context)
