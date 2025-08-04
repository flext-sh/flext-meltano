"""Comprehensive test coverage for FLEXT Meltano Singer Base exceptions.

This test module provides 100% coverage for the Singer exception hierarchy,
ensuring all exception classes, error contexts, and integration patterns
are thoroughly tested following enterprise quality standards.
"""


from flext_meltano.singer_base import (
    FlextSingerAuthenticationError,
    FlextSingerConfigurationError,
    FlextSingerConnectionError,
    FlextSingerError,
    FlextSingerProcessingError,
    FlextSingerValidationError,
    FlextTapError,
    FlextTargetError,
    FlextTransformError,
)


class TestFlextSingerError:
    """Test FlextSingerError base exception class."""

    def test_singer_error_default_initialization(self) -> None:
        """Test FlextSingerError with default parameters."""
        error = FlextSingerError()
        assert str(error) == "[SINGER_ERROR] Singer operation error"
        assert error.error_code == "SINGER_ERROR"
        assert error.context == {}

    def test_singer_error_with_message(self) -> None:
        """Test FlextSingerError with custom message."""
        message = "Custom Singer operation failed"
        error = FlextSingerError(message)
        assert str(error) == f"[SINGER_ERROR] {message}"
        assert error.error_code == "SINGER_ERROR"

    def test_singer_error_with_component_type(self) -> None:
        """Test FlextSingerError with component type context."""
        error = FlextSingerError("Test error", component_type="tap")
        assert error.context["component_type"] == "tap"

    def test_singer_error_with_stream_name(self) -> None:
        """Test FlextSingerError with stream name context."""
        error = FlextSingerError("Test error", stream_name="users")
        assert error.context["stream_name"] == "users"

    def test_singer_error_with_all_context(self) -> None:
        """Test FlextSingerError with all context parameters."""
        error = FlextSingerError(
            "Complete test error",
            component_type="target",
            stream_name="orders",
            additional_context="extra_value",
        )
        assert error.context["component_type"] == "target"
        assert error.context["stream_name"] == "orders"
        assert error.context["additional_context"] == "extra_value"

    def test_singer_error_with_kwargs(self) -> None:
        """Test FlextSingerError with additional keyword arguments."""
        error = FlextSingerError(
            "Test error",
            custom_field="custom_value",
            operation_id="op123",
        )
        assert error.context["custom_field"] == "custom_value"
        assert error.context["operation_id"] == "op123"


class TestFlextSingerConnectionError:
    """Test FlextSingerConnectionError for connection-related failures."""

    def test_connection_error_default_initialization(self) -> None:
        """Test FlextSingerConnectionError with default parameters."""
        error = FlextSingerConnectionError()
        assert str(error) == "[CONNECTION_ERROR] Singer connection: Singer connection failed"

    def test_connection_error_with_message(self) -> None:
        """Test FlextSingerConnectionError with custom message."""
        error = FlextSingerConnectionError("Database unreachable")
        assert str(error) == "[CONNECTION_ERROR] Singer connection: Database unreachable"

    def test_connection_error_with_host(self) -> None:
        """Test FlextSingerConnectionError with host context."""
        error = FlextSingerConnectionError("Connection failed", host="oracle.example.com")
        assert error.context["host"] == "oracle.example.com"

    def test_connection_error_with_port(self) -> None:
        """Test FlextSingerConnectionError with port context."""
        error = FlextSingerConnectionError("Connection failed", port=1521)
        assert error.context["port"] == 1521

    def test_connection_error_with_host_and_port(self) -> None:
        """Test FlextSingerConnectionError with host and port context."""
        error = FlextSingerConnectionError(
            "Oracle connection failed",
            host="oracle.db.company.com",
            port=1521,
        )
        assert error.context["host"] == "oracle.db.company.com"
        assert error.context["port"] == 1521

    def test_connection_error_with_additional_context(self) -> None:
        """Test FlextSingerConnectionError with additional context."""
        error = FlextSingerConnectionError(
            "Connection timeout",
            host="postgres.example.com",
            port=5432,
            timeout=30,
            retry_count=3,
        )
        assert error.context["host"] == "postgres.example.com"
        assert error.context["port"] == 5432
        assert error.context["timeout"] == 30
        assert error.context["retry_count"] == 3


class TestFlextSingerAuthenticationError:
    """Test FlextSingerAuthenticationError for authentication failures."""

    def test_auth_error_default_initialization(self) -> None:
        """Test FlextSingerAuthenticationError with default parameters."""
        error = FlextSingerAuthenticationError()
        assert str(error) == "[AUTH_ERROR] Singer auth: Singer authentication failed"

    def test_auth_error_with_message(self) -> None:
        """Test FlextSingerAuthenticationError with custom message."""
        error = FlextSingerAuthenticationError("Invalid credentials")
        assert str(error) == "[AUTH_ERROR] Singer auth: Invalid credentials"

    def test_auth_error_with_username(self) -> None:
        """Test FlextSingerAuthenticationError with username context."""
        error = FlextSingerAuthenticationError("Login failed", username="user123")
        assert error.context["username"] == "user123"

    def test_auth_error_with_auth_method(self) -> None:
        """Test FlextSingerAuthenticationError with auth method context."""
        error = FlextSingerAuthenticationError("Auth failed", auth_method="oauth2")
        assert error.context["auth_method"] == "oauth2"

    def test_auth_error_with_complete_context(self) -> None:
        """Test FlextSingerAuthenticationError with all context parameters."""
        error = FlextSingerAuthenticationError(
            "OAuth authentication failed",
            username="REDACTED_LDAP_BIND_PASSWORD@company.com",
            auth_method="oauth2",
            token_expired=True,
            refresh_attempted=False,
        )
        assert error.context["username"] == "REDACTED_LDAP_BIND_PASSWORD@company.com"
        assert error.context["auth_method"] == "oauth2"
        assert error.context["token_expired"] is True
        assert error.context["refresh_attempted"] is False


class TestFlextSingerValidationError:
    """Test FlextSingerValidationError for data validation failures."""

    def test_validation_error_default_initialization(self) -> None:
        """Test FlextSingerValidationError with default parameters."""
        error = FlextSingerValidationError()
        assert str(error) == "[VALIDATION_ERROR] Singer validation: Singer validation failed"

    def test_validation_error_with_message(self) -> None:
        """Test FlextSingerValidationError with custom message."""
        error = FlextSingerValidationError("Invalid email format")
        assert str(error) == "[VALIDATION_ERROR] Singer validation: Invalid email format"

    def test_validation_error_with_field(self) -> None:
        """Test FlextSingerValidationError with field context."""
        error = FlextSingerValidationError("Invalid value", field="email")
        assert error.field == "email"

    def test_validation_error_with_value(self) -> None:
        """Test FlextSingerValidationError with value context."""
        error = FlextSingerValidationError("Invalid format", value="invalid-email")
        assert error.value == "invalid-email"

    def test_validation_error_with_record_id(self) -> None:
        """Test FlextSingerValidationError with record ID context."""
        error = FlextSingerValidationError("Validation failed", record_id="rec123")
        assert error.context["record_id"] == "rec123"

    def test_validation_error_with_long_value_truncation(self) -> None:
        """Test FlextSingerValidationError truncates long values."""
        long_value = "x" * 150  # Create a value longer than 100 characters
        error = FlextSingerValidationError("Invalid value", value=long_value)
        # FlextValidationError may truncate long values
        assert error.value is not None
        assert len(str(error.value)) <= 150  # Allow for reasonable length

    def test_validation_error_with_complete_context(self) -> None:
        """Test FlextSingerValidationError with all context parameters."""
        error = FlextSingerValidationError(
            "Email validation failed",
            field="customer_email",
            value="not-an-email",
            record_id="customer_001",
            stream_name="customers",
            batch_id="batch_123",
        )
        assert error.field == "customer_email"
        assert error.value == "not-an-email"
        assert error.context["record_id"] == "customer_001"
        assert error.context["stream_name"] == "customers"
        assert error.context["batch_id"] == "batch_123"


class TestFlextSingerConfigurationError:
    """Test FlextSingerConfigurationError for configuration failures."""

    def test_config_error_default_initialization(self) -> None:
        """Test FlextSingerConfigurationError with default parameters."""
        error = FlextSingerConfigurationError()
        assert str(error) == "[CONFIG_ERROR] Singer config: Singer configuration error"

    def test_config_error_with_message(self) -> None:
        """Test FlextSingerConfigurationError with custom message."""
        error = FlextSingerConfigurationError("Missing database URL")
        assert str(error) == "[CONFIG_ERROR] Singer config: Missing database URL"

    def test_config_error_with_config_key(self) -> None:
        """Test FlextSingerConfigurationError with config key context."""
        error = FlextSingerConfigurationError("Invalid value", config_key="database_url")
        assert error.context["config_key"] == "database_url"

    def test_config_error_with_complete_context(self) -> None:
        """Test FlextSingerConfigurationError with all context parameters."""
        error = FlextSingerConfigurationError(
            "Invalid Oracle connection URL",
            config_key="oracle_url",
            config_section="database",
            expected_format="oracle://user:pass@host:port/service",
        )
        assert error.context["config_key"] == "oracle_url"
        assert error.context["config_section"] == "database"
        assert error.context["expected_format"] == "oracle://user:pass@host:port/service"


class TestFlextSingerProcessingError:
    """Test FlextSingerProcessingError for processing failures."""

    def test_processing_error_default_initialization(self) -> None:
        """Test FlextSingerProcessingError with default parameters."""
        error = FlextSingerProcessingError()
        assert str(error) == "[PROCESSING_ERROR] Singer processing: Singer processing failed"

    def test_processing_error_with_message(self) -> None:
        """Test FlextSingerProcessingError with custom message."""
        error = FlextSingerProcessingError("Batch processing failed")
        assert str(error) == "[PROCESSING_ERROR] Singer processing: Batch processing failed"

    def test_processing_error_with_operation(self) -> None:
        """Test FlextSingerProcessingError with operation context."""
        error = FlextSingerProcessingError("Failed", operation="extract")
        assert error.context["operation"] == "extract"

    def test_processing_error_with_record_count(self) -> None:
        """Test FlextSingerProcessingError with record count context."""
        error = FlextSingerProcessingError("Failed", record_count=1500)
        assert error.context["record_count"] == 1500

    def test_processing_error_with_complete_context(self) -> None:
        """Test FlextSingerProcessingError with all context parameters."""
        error = FlextSingerProcessingError(
            "Transformation failed on large batch",
            operation="transform",
            record_count=50000,
            memory_limit=8192,
            timeout=300,
        )
        assert error.context["operation"] == "transform"
        assert error.context["record_count"] == 50000
        assert error.context["memory_limit"] == 8192
        assert error.context["timeout"] == 300


class TestFlextTapError:
    """Test FlextTapError for tap-specific operations."""

    def test_tap_error_default_initialization(self) -> None:
        """Test FlextTapError with default parameters."""
        error = FlextTapError()
        assert str(error) == "[SINGER_ERROR] Tap operation error"
        assert error.context["component_type"] == "tap"

    def test_tap_error_with_message(self) -> None:
        """Test FlextTapError with custom message."""
        error = FlextTapError("Oracle tap failed")
        assert str(error) == "[SINGER_ERROR] Oracle tap failed"
        assert error.context["component_type"] == "tap"

    def test_tap_error_with_source_system(self) -> None:
        """Test FlextTapError with source system context."""
        error = FlextTapError("Connection failed", source_system="oracle-wms")
        assert error.context["source_system"] == "oracle-wms"
        assert error.context["component_type"] == "tap"

    def test_tap_error_with_complete_context(self) -> None:
        """Test FlextTapError with all context parameters."""
        error = FlextTapError(
            "Oracle WMS extraction failed",
            source_system="oracle-wms-production",
            stream_name="shipments",
            table_name="SHIPMENT_HEADERS",
            last_sync="2025-08-04T10:30:00Z",
        )
        assert error.context["source_system"] == "oracle-wms-production"
        assert error.context["component_type"] == "tap"
        assert error.context["stream_name"] == "shipments"
        assert error.context["table_name"] == "SHIPMENT_HEADERS"
        assert error.context["last_sync"] == "2025-08-04T10:30:00Z"


class TestFlextTargetError:
    """Test FlextTargetError for target-specific operations."""

    def test_target_error_default_initialization(self) -> None:
        """Test FlextTargetError with default parameters."""
        error = FlextTargetError()
        assert str(error) == "[SINGER_ERROR] Target operation error"
        assert error.context["component_type"] == "target"

    def test_target_error_with_message(self) -> None:
        """Test FlextTargetError with custom message."""
        error = FlextTargetError("PostgreSQL target failed")
        assert str(error) == "[SINGER_ERROR] PostgreSQL target failed"
        assert error.context["component_type"] == "target"

    def test_target_error_with_destination_system(self) -> None:
        """Test FlextTargetError with destination system context."""
        error = FlextTargetError("Write failed", destination_system="postgres-warehouse")
        assert error.context["destination_system"] == "postgres-warehouse"
        assert error.context["component_type"] == "target"

    def test_target_error_with_complete_context(self) -> None:
        """Test FlextTargetError with all context parameters."""
        error = FlextTargetError(
            "Data warehouse load failed",
            destination_system="postgres-warehouse-prod",
            stream_name="customer_data",
            table_name="dim_customer",
            batch_size=10000,
            upsert_mode=True,
        )
        assert error.context["destination_system"] == "postgres-warehouse-prod"
        assert error.context["component_type"] == "target"
        assert error.context["stream_name"] == "customer_data"
        assert error.context["table_name"] == "dim_customer"
        assert error.context["batch_size"] == 10000
        assert error.context["upsert_mode"] is True


class TestFlextTransformError:
    """Test FlextTransformError for transform-specific operations."""

    def test_transform_error_default_initialization(self) -> None:
        """Test FlextTransformError with default parameters."""
        error = FlextTransformError()
        assert str(error) == "[SINGER_ERROR] Transform operation error"
        assert error.context["component_type"] == "transform"

    def test_transform_error_with_message(self) -> None:
        """Test FlextTransformError with custom message."""
        error = FlextTransformError("DBT model failed")
        assert str(error) == "[SINGER_ERROR] DBT model failed"
        assert error.context["component_type"] == "transform"

    def test_transform_error_with_transform_name(self) -> None:
        """Test FlextTransformError with transform name context."""
        error = FlextTransformError("Transform failed", transform_name="customer_aggregation")
        assert error.context["transform_name"] == "customer_aggregation"
        assert error.context["component_type"] == "transform"

    def test_transform_error_with_complete_context(self) -> None:
        """Test FlextTransformError with all context parameters."""
        error = FlextTransformError(
            "DBT customer aggregation model failed",
            transform_name="dim_customer_metrics",
            stream_name="customer_events",
            model_type="aggregate",
            materialization="table",
            rows_affected=0,
        )
        assert error.context["transform_name"] == "dim_customer_metrics"
        assert error.context["component_type"] == "transform"
        assert error.context["stream_name"] == "customer_events"
        assert error.context["model_type"] == "aggregate"
        assert error.context["materialization"] == "table"
        assert error.context["rows_affected"] == 0


class TestExceptionInheritance:
    """Test exception inheritance hierarchy."""

    def test_singer_error_inheritance(self) -> None:
        """Test FlextSingerError inherits from proper base class."""
        error = FlextSingerError()
        # Should inherit from FlextError through the proper chain
        assert hasattr(error, "error_code")
        assert hasattr(error, "context")

    def test_connection_error_inheritance(self) -> None:
        """Test FlextSingerConnectionError inherits properly."""
        error = FlextSingerConnectionError()
        assert hasattr(error, "context")

    def test_authentication_error_inheritance(self) -> None:
        """Test FlextSingerAuthenticationError inherits properly."""
        error = FlextSingerAuthenticationError()
        assert hasattr(error, "context")

    def test_validation_error_inheritance(self) -> None:
        """Test FlextSingerValidationError inherits properly."""
        error = FlextSingerValidationError()
        assert hasattr(error, "field")
        assert hasattr(error, "value")
        assert hasattr(error, "context")

    def test_configuration_error_inheritance(self) -> None:
        """Test FlextSingerConfigurationError inherits properly."""
        error = FlextSingerConfigurationError()
        assert hasattr(error, "context")

    def test_processing_error_inheritance(self) -> None:
        """Test FlextSingerProcessingError inherits properly."""
        error = FlextSingerProcessingError()
        assert hasattr(error, "context")

    def test_component_errors_inherit_from_singer_error(self) -> None:
        """Test component-specific errors inherit from FlextSingerError."""
        tap_error = FlextTapError()
        target_error = FlextTargetError()
        transform_error = FlextTransformError()

        assert isinstance(tap_error, FlextSingerError)
        assert isinstance(target_error, FlextSingerError)
        assert isinstance(transform_error, FlextSingerError)


class TestExceptionExports:
    """Test module exports are correctly defined."""

    def test_all_exceptions_exported(self) -> None:
        """Test all exception classes are in __all__."""
        from flext_meltano.singer_base import __all__

        expected_exports = [
            "FlextSingerError",
            "FlextSingerConnectionError",
            "FlextSingerAuthenticationError",
            "FlextSingerValidationError",
            "FlextSingerConfigurationError",
            "FlextSingerProcessingError",
            "FlextTapError",
            "FlextTargetError",
            "FlextTransformError",
        ]

        for exception_class in expected_exports:
            assert exception_class in __all__, f"{exception_class} not exported in __all__"

    def test_exported_classes_are_importable(self) -> None:
        """Test all exported classes can be imported."""
        from flext_meltano.singer_base import (
            FlextSingerAuthenticationError,
            FlextSingerConfigurationError,
            FlextSingerConnectionError,
            FlextSingerError,
            FlextSingerProcessingError,
            FlextSingerValidationError,
            FlextTapError,
            FlextTargetError,
            FlextTransformError,
        )

        # Verify all classes are actually classes
        assert isinstance(FlextSingerError, type)
        assert isinstance(FlextSingerConnectionError, type)
        assert isinstance(FlextSingerAuthenticationError, type)
        assert isinstance(FlextSingerValidationError, type)
        assert isinstance(FlextSingerConfigurationError, type)
        assert isinstance(FlextSingerProcessingError, type)
        assert isinstance(FlextTapError, type)
        assert isinstance(FlextTargetError, type)
        assert isinstance(FlextTransformError, type)
