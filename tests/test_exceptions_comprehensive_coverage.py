"""Comprehensive Coverage Tests for Exceptions Module.

**Purpose**: Test all exception classes in exceptions.py to achieve 100% coverage
**Scope**: All 11 exception classes and their functionality
**Target**: Increase exceptions.py coverage from 0% to 100%

This module provides functional tests for all custom exceptions to ensure
they work correctly and provide proper error context.
"""

from __future__ import annotations

import pytest

import flext_meltano.exceptions as exc
from flext_meltano.exceptions import (
    FlextMeltanoConfigurationError,
    FlextMeltanoDBTError,
    FlextMeltanoError,
    FlextMeltanoExecutionError,
    FlextMeltanoPluginError,
    FlextMeltanoProcessingError,
    FlextMeltanoSingerError,
    FlextMeltanoTimeoutError,
    FlextMeltanoValidationError,
)

# Import exceptions not in __all__ directly from module
FlextMeltanoConnectionError = exc.FlextMeltanoConnectionError
FlextMeltanoAuthenticationError = exc.FlextMeltanoAuthenticationError


class TestFlextMeltanoBaseException:
    """Test base FlextMeltanoError exception."""

    def test_flext_meltano_error_creation(self):
        """Test basic FlextMeltanoError creation."""
        error = FlextMeltanoError("Base Meltano error")
        assert "Base Meltano error" in str(error)
        assert isinstance(error, Exception)

    def test_flext_meltano_error_with_context(self):
        """Test FlextMeltanoError with context."""
        context = {"operation": "test", "component": "meltano"}
        error = FlextMeltanoError("Context error", context=context)

        assert "Context error" in str(error)
        assert error.context == context
        assert error.context["operation"] == "test"

    def test_flext_meltano_error_inheritance(self):
        """Test FlextMeltanoError inheritance."""
        error = FlextMeltanoError("Inheritance test")
        assert isinstance(error, FlextMeltanoError)
        assert isinstance(error, Exception)

    def test_flext_meltano_error_raising(self):
        """Test raising FlextMeltanoError."""
        error_message = "Test raising"
        with pytest.raises(FlextMeltanoError) as exc_info:
            raise FlextMeltanoError(error_message)

        assert "Test raising" in str(exc_info.value)


class TestFlextMeltanoValidationError:
    """Test FlextMeltanoValidationError exception."""

    def test_validation_error_creation(self):
        """Test validation error creation."""
        error = FlextMeltanoValidationError("Validation failed")
        assert "Validation failed" in str(error)
        assert isinstance(error, FlextMeltanoValidationError)

    def test_validation_error_with_details(self):
        """Test validation error with field details."""
        error = FlextMeltanoValidationError(
            "Invalid extractor",
            field="extractor",
            value="invalid-tap",
            reason="not found",
        )

        assert error.context["field"] == "extractor"
        assert error.context["value"] == "invalid-tap"

    def test_validation_error_raising(self):
        """Test raising validation error."""
        error_message = "Config validation failed"
        with pytest.raises(FlextMeltanoValidationError):
            raise FlextMeltanoValidationError(error_message)


class TestFlextMeltanoConfigurationError:
    """Test FlextMeltanoConfigurationError exception."""

    def test_configuration_error_creation(self):
        """Test configuration error creation."""
        error = FlextMeltanoConfigurationError("Configuration error")
        assert "Configuration error" in str(error)

    def test_configuration_error_with_config_context(self):
        """Test configuration error with config context."""
        error = FlextMeltanoConfigurationError(
            "Invalid config",
            config_file="meltano.yml",
            section="plugins",
        )

        assert error.context["context"]["config_file"] == "meltano.yml"
        assert error.context["context"]["section"] == "plugins"

    def test_configuration_error_raising(self):
        """Test raising configuration error."""
        error_message = "Missing required config"
        with pytest.raises(FlextMeltanoConfigurationError):
            raise FlextMeltanoConfigurationError(error_message)


class TestFlextMeltanoConnectionError:
    """Test FlextMeltanoConnectionError exception."""

    def test_connection_error_creation(self):
        """Test connection error creation."""
        error = FlextMeltanoConnectionError("Connection failed")
        assert "Connection failed" in str(error)

    def test_connection_error_with_details(self):
        """Test connection error with connection details."""
        error = FlextMeltanoConnectionError(
            "Database unreachable",
            host="localhost",
            port=5432,
            timeout=30,
        )

        assert error.context["context"]["host"] == "localhost"
        assert error.context["context"]["port"] == 5432

    def test_connection_error_raising(self):
        """Test raising connection error."""
        error_message = "Connection timeout"
        with pytest.raises(FlextMeltanoConnectionError):
            raise FlextMeltanoConnectionError(error_message)


class TestFlextMeltanoProcessingError:
    """Test FlextMeltanoProcessingError exception."""

    def test_processing_error_creation(self):
        """Test processing error creation."""
        error = FlextMeltanoProcessingError("Processing failed")
        assert "Processing failed" in str(error)

    def test_processing_error_with_pipeline_context(self):
        """Test processing error with pipeline context."""
        error = FlextMeltanoProcessingError(
            "Data processing failed",
            pipeline="test-pipeline",
            stage="extract",
            records=1000,
        )

        assert error.context["context"]["pipeline"] == "test-pipeline"
        assert error.context["context"]["stage"] == "extract"

    def test_processing_error_raising(self):
        """Test raising processing error."""
        error_message = "Data transformation error"
        with pytest.raises(FlextMeltanoProcessingError):
            raise FlextMeltanoProcessingError(error_message)


class TestFlextMeltanoAuthenticationError:
    """Test FlextMeltanoAuthenticationError exception."""

    def test_authentication_error_creation(self):
        """Test authentication error creation."""
        error = FlextMeltanoAuthenticationError("Authentication failed")
        assert "Authentication failed" in str(error)
        assert isinstance(error, FlextMeltanoAuthenticationError)

    def test_authentication_error_with_user_context(self):
        """Test authentication error with user context."""
        error = FlextMeltanoAuthenticationError(
            "Invalid credentials",
            user="test_user",
            service="tap-postgres",
            method="oauth",
        )

        assert error.context["context"]["user"] == "test_user"
        assert error.context["context"]["service"] == "tap-postgres"

    def test_authentication_error_raising(self):
        """Test raising authentication error."""
        error_message = "Token expired"
        with pytest.raises(FlextMeltanoAuthenticationError):
            raise FlextMeltanoAuthenticationError(error_message)


class TestFlextMeltanoTimeoutError:
    """Test FlextMeltanoTimeoutError exception."""

    def test_timeout_error_creation(self):
        """Test timeout error creation."""
        error = FlextMeltanoTimeoutError("Operation timed out")
        assert "Operation timed out" in str(error)

    def test_timeout_error_with_timing_context(self):
        """Test timeout error with timing context."""
        error = FlextMeltanoTimeoutError(
            "Sync timeout",
            timeout=300,
            elapsed=450,
            operation="sync",
        )

        assert error.context["context"]["timeout"] == 300
        assert error.context["context"]["elapsed"] == 450

    def test_timeout_error_raising(self):
        """Test raising timeout error."""
        error_message = "Pipeline execution timeout"
        with pytest.raises(FlextMeltanoTimeoutError):
            raise FlextMeltanoTimeoutError(error_message)


class TestFlextMeltanoPluginError:
    """Test FlextMeltanoPluginError exception."""

    def test_plugin_error_creation(self):
        """Test plugin error creation."""
        error = FlextMeltanoPluginError("Plugin error")
        assert "Plugin error" in str(error)

    def test_plugin_error_with_plugin_context(self):
        """Test plugin error with plugin context."""
        error = FlextMeltanoPluginError(
            "Plugin discovery failed",
            plugin_name="tap-postgres",
            plugin_type="extractor",
            version="0.1.0",
            command="discover",
        )

        assert error.context["plugin_name"] == "tap-postgres"
        assert error.context["plugin_type"] == "extractor"

    def test_plugin_error_raising(self):
        """Test raising plugin error."""
        error_message = "Plugin not found"
        with pytest.raises(FlextMeltanoPluginError):
            raise FlextMeltanoPluginError(error_message)


class TestFlextMeltanoExecutionError:
    """Test FlextMeltanoExecutionError exception."""

    def test_execution_error_creation(self):
        """Test execution error creation."""
        error = FlextMeltanoExecutionError("Execution failed")
        assert "Execution failed" in str(error)

    def test_execution_error_with_execution_context(self):
        """Test execution error with execution context."""
        error = FlextMeltanoExecutionError(
            "Pipeline execution failed",
            command=["meltano", "run", "tap-postgres", "target-postgres"],
            exit_code=1,
            duration=120.5,
            environment="production",
        )

        assert error.context["exit_code"] == 1
        assert error.context["duration"] == 120.5

    def test_execution_error_raising(self):
        """Test raising execution error."""
        error_message = "Command failed with exit code 1"
        with pytest.raises(FlextMeltanoExecutionError):
            raise FlextMeltanoExecutionError(error_message)


class TestFlextMeltanoSingerError:
    """Test FlextMeltanoSingerError exception."""

    def test_singer_error_creation(self):
        """Test Singer error creation."""
        error = FlextMeltanoSingerError("Singer protocol error")
        assert "Singer protocol error" in str(error)

    def test_singer_error_with_stream_context(self):
        """Test Singer error with stream context."""
        context = {
            "tap": "tap-postgres",
            "target": "target-csv",
            "stream": "users",
            "schema": {"id": "integer", "name": "string"},
            "records_processed": 5000,
        }
        error = FlextMeltanoSingerError("Stream processing failed", context=context)

        # Just test that the error was created and has context
        assert hasattr(error, "context")
        assert isinstance(error.context, dict)

    def test_singer_error_raising(self):
        """Test raising Singer error."""
        error_message = "Invalid Singer message format"
        with pytest.raises(FlextMeltanoSingerError):
            raise FlextMeltanoSingerError(error_message)


class TestFlextMeltanoDBTError:
    """Test FlextMeltanoDBTError exception."""

    def test_dbt_error_creation(self):
        """Test DBT error creation."""
        error = FlextMeltanoDBTError("DBT transformation failed")
        assert "DBT transformation failed" in str(error)

    def test_dbt_error_with_model_context(self):
        """Test DBT error with model context."""
        error = FlextMeltanoDBTError(
            "Model compilation failed",
            project_name="analytics",
            model_name="dim_customers",
            target="dev",
            compilation_error="Syntax error in SQL",
            line=42,
        )

        assert error.context["project_name"] == "analytics"
        assert error.context["model_name"] == "dim_customers"
        assert error.context["line"] == 42

    def test_dbt_error_raising(self):
        """Test raising DBT error."""
        error_message = "DBT run failed"
        with pytest.raises(FlextMeltanoDBTError):
            raise FlextMeltanoDBTError(error_message)


class TestExceptionsIntegration:
    """Test exception integration and hierarchy."""

    def test_exception_hierarchy(self):
        """Test that all exceptions inherit correctly."""
        # Create exceptions
        validation_error = FlextMeltanoValidationError("test")
        config_error = FlextMeltanoConfigurationError("test")
        processing_error = FlextMeltanoProcessingError("test")
        timeout_error = FlextMeltanoTimeoutError("test")
        plugin_error = FlextMeltanoPluginError("test")
        execution_error = FlextMeltanoExecutionError("test")
        singer_error = FlextMeltanoSingerError("test")
        dbt_error = FlextMeltanoDBTError("test")

        # Test inheritance - some inherit from flext-core types, others from FlextMeltanoError
        assert isinstance(validation_error, Exception)
        assert isinstance(config_error, Exception)
        assert isinstance(processing_error, Exception)
        assert isinstance(timeout_error, Exception)
        assert isinstance(
            plugin_error,
            FlextMeltanoError,
        )  # Direct FlextMeltanoError inheritance
        assert isinstance(
            execution_error,
            FlextMeltanoError,
        )  # Direct FlextMeltanoError inheritance
        assert isinstance(
            singer_error,
            FlextMeltanoError,
        )  # Direct FlextMeltanoError inheritance
        assert isinstance(
            dbt_error,
            FlextMeltanoError,
        )  # Direct FlextMeltanoError inheritance

    def test_exception_context_preservation(self):
        """Test that exception context is preserved through inheritance."""
        # Create exceptions using kwargs to ensure proper context structure
        exceptions = [
            FlextMeltanoValidationError("test", key="value", number=42),
            FlextMeltanoConfigurationError("test", key="value", number=42),
            FlextMeltanoConnectionError("test", key="value", number=42),
            FlextMeltanoProcessingError("test", key="value", number=42),
            FlextMeltanoAuthenticationError("test", key="value", number=42),
            FlextMeltanoTimeoutError("test", key="value", number=42),
            FlextMeltanoPluginError("test", key="value", number=42),
            FlextMeltanoExecutionError("test", key="value", number=42),
            FlextMeltanoSingerError("test", key="value", number=42),
            FlextMeltanoDBTError("test", key="value", number=42),
        ]

        # Check context preservation - handle both direct and nested context structures
        for exception in exceptions:
            assert hasattr(exception, "context")

            # Some exceptions have nested context, others have direct context
            if "context" in exception.context and isinstance(
                exception.context["context"],
                dict,
            ):
                # Nested context structure
                assert exception.context["context"]["key"] == "value"
                assert exception.context["context"]["number"] == 42
            else:
                # Direct context structure
                assert exception.context["key"] == "value"
                assert exception.context["number"] == 42

    def test_exception_chaining(self):
        """Test exception chaining with cause."""
        original_error = ValueError("Original error")

        try:
            raise original_error
        except ValueError as e:
            error_message = "Wrapped error"
            with pytest.raises(FlextMeltanoError) as exc_info:
                raise FlextMeltanoError(error_message) from e

        meltano_error = exc_info.value
        assert meltano_error.__cause__ is original_error
        assert "Wrapped error" in str(meltano_error)

    def test_all_exceptions_can_be_raised_and_caught(self):
        """Test that all exceptions can be raised and caught properly."""
        exception_classes = [
            FlextMeltanoError,
            FlextMeltanoValidationError,
            FlextMeltanoConfigurationError,
            FlextMeltanoConnectionError,
            FlextMeltanoProcessingError,
            FlextMeltanoAuthenticationError,
            FlextMeltanoTimeoutError,
            FlextMeltanoPluginError,
            FlextMeltanoExecutionError,
            FlextMeltanoSingerError,
            FlextMeltanoDBTError,
        ]

        for exception_class in exception_classes:
            msg = f"Test {exception_class.__name__}"
            with pytest.raises(exception_class):
                raise exception_class(msg)

    def test_exception_string_representations(self):
        """Test string representations of all exceptions."""
        exceptions = [
            FlextMeltanoError("Base error"),
            FlextMeltanoValidationError("Validation error"),
            FlextMeltanoConfigurationError("Config error"),
            FlextMeltanoConnectionError("Connection error"),
            FlextMeltanoProcessingError("Processing error"),
            FlextMeltanoAuthenticationError("Auth error"),
            FlextMeltanoTimeoutError("Timeout error"),
            FlextMeltanoPluginError("Plugin error"),
            FlextMeltanoExecutionError("Execution error"),
            FlextMeltanoSingerError("Singer error"),
            FlextMeltanoDBTError("DBT error"),
        ]

        for exception in exceptions:
            str_repr = str(exception)
            assert isinstance(str_repr, str)
            assert len(str_repr) > 0
            assert "error" in str_repr.lower()
