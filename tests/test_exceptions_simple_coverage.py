"""Simple Complete Coverage Tests for Exceptions Module.

**Purpose**: Test all exception classes in exceptions.py to achieve 100% coverage
**Scope**: All 11 exception classes and their basic functionality
**Target**: Increase exceptions.py coverage from 0% to 100%

This module provides simple tests for all custom exceptions to ensure
maximum coverage with minimal complexity.
"""

import pytest

from flext_meltano.exceptions import (
    FlextMeltanoAuthenticationError,
    FlextMeltanoConfigurationError,
    FlextMeltanoConnectionError,
    FlextMeltanoDBTError,
    FlextMeltanoError,
    FlextMeltanoExecutionError,
    FlextMeltanoPluginError,
    FlextMeltanoProcessingError,
    FlextMeltanoSingerError,
    FlextMeltanoTimeoutError,
    FlextMeltanoValidationError,
)


class TestAllExceptions:
    """Test all exception classes for basic functionality."""

    def test_flext_meltano_error(self):
        """Test FlextMeltanoError."""
        error = FlextMeltanoError("Base error")
        assert isinstance(error, FlextMeltanoError)
        assert isinstance(error, Exception)
        with pytest.raises(FlextMeltanoError):
            raise error

    def test_flext_meltano_validation_error(self):
        """Test FlextMeltanoValidationError."""
        error = FlextMeltanoValidationError("Validation error")
        assert isinstance(error, FlextMeltanoValidationError)
        # This inherits from flext-core, not FlextMeltanoError
        assert isinstance(error, Exception)
        with pytest.raises(FlextMeltanoValidationError):
            raise error

    def test_flext_meltano_configuration_error(self):
        """Test FlextMeltanoConfigurationError."""
        error = FlextMeltanoConfigurationError("Config error")
        assert isinstance(error, FlextMeltanoConfigurationError)
        # This inherits from flext-core, not FlextMeltanoError
        assert isinstance(error, Exception)
        with pytest.raises(FlextMeltanoConfigurationError):
            raise error

    def test_flext_meltano_connection_error(self):
        """Test FlextMeltanoConnectionError."""
        error = FlextMeltanoConnectionError("Connection error")
        assert isinstance(error, FlextMeltanoConnectionError)
        # This inherits from flext-core, not FlextMeltanoError
        assert isinstance(error, Exception)
        with pytest.raises(FlextMeltanoConnectionError):
            raise error

    def test_flext_meltano_processing_error(self):
        """Test FlextMeltanoProcessingError."""
        error = FlextMeltanoProcessingError("Processing error")
        assert isinstance(error, FlextMeltanoProcessingError)
        # This inherits from flext-core, not FlextMeltanoError
        assert isinstance(error, Exception)
        with pytest.raises(FlextMeltanoProcessingError):
            raise error

    def test_flext_meltano_authentication_error(self):
        """Test FlextMeltanoAuthenticationError."""
        error = FlextMeltanoAuthenticationError("Auth error")
        assert isinstance(error, FlextMeltanoAuthenticationError)
        # This inherits from flext-core, not FlextMeltanoError
        assert isinstance(error, Exception)
        with pytest.raises(FlextMeltanoAuthenticationError):
            raise error

    def test_flext_meltano_timeout_error(self):
        """Test FlextMeltanoTimeoutError."""
        error = FlextMeltanoTimeoutError("Timeout error")
        assert isinstance(error, FlextMeltanoTimeoutError)
        # This inherits from flext-core, not FlextMeltanoError
        assert isinstance(error, Exception)
        with pytest.raises(FlextMeltanoTimeoutError):
            raise error

    def test_flext_meltano_plugin_error(self):
        """Test FlextMeltanoPluginError."""
        error = FlextMeltanoPluginError("Plugin error")
        assert isinstance(error, FlextMeltanoPluginError)
        assert isinstance(error, FlextMeltanoError)
        with pytest.raises(FlextMeltanoPluginError):
            raise error

    def test_flext_meltano_execution_error(self):
        """Test FlextMeltanoExecutionError."""
        error = FlextMeltanoExecutionError("Execution error")
        assert isinstance(error, FlextMeltanoExecutionError)
        assert isinstance(error, FlextMeltanoError)
        with pytest.raises(FlextMeltanoExecutionError):
            raise error

    def test_flext_meltano_singer_error(self):
        """Test FlextMeltanoSingerError."""
        error = FlextMeltanoSingerError("Singer error")
        assert isinstance(error, FlextMeltanoSingerError)
        assert isinstance(error, FlextMeltanoError)
        with pytest.raises(FlextMeltanoSingerError):
            raise error

    def test_flext_meltano_dbt_error(self):
        """Test FlextMeltanoDBTError."""
        error = FlextMeltanoDBTError("DBT error")
        assert isinstance(error, FlextMeltanoDBTError)
        assert isinstance(error, FlextMeltanoError)
        with pytest.raises(FlextMeltanoDBTError):
            raise error

    def test_all_exceptions_with_context(self):
        """Test all exceptions can be created with context."""
        context = {"test": "value"}

        exceptions = [
            FlextMeltanoError("test", context=context),
            FlextMeltanoValidationError("test", context=context),
            FlextMeltanoConfigurationError("test", context=context),
            FlextMeltanoConnectionError("test", context=context),
            FlextMeltanoProcessingError("test", context=context),
            FlextMeltanoAuthenticationError("test", context=context),
            FlextMeltanoTimeoutError("test", context=context),
            FlextMeltanoPluginError("test", context=context),
            FlextMeltanoExecutionError("test", context=context),
            FlextMeltanoSingerError("test", context=context),
            FlextMeltanoDBTError("test", context=context),
        ]

        # Test that all exceptions were created successfully
        for exception in exceptions:
            assert isinstance(exception, Exception)
            assert hasattr(exception, "context")

    def test_exception_string_representations(self):
        """Test that all exceptions have string representations."""
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

    def test_exception_hierarchy(self):
        """Test that exception hierarchy is correct."""
        # Domain-specific exceptions inherit from FlextMeltanoError
        domain_exceptions = [
            FlextMeltanoPluginError("test"),
            FlextMeltanoExecutionError("test"),
            FlextMeltanoSingerError("test"),
            FlextMeltanoDBTError("test"),
        ]

        for exception in domain_exceptions:
            assert isinstance(exception, FlextMeltanoError)
            assert isinstance(exception, Exception)

        # Core-based exceptions inherit from flext-core
        core_exceptions = [
            FlextMeltanoValidationError("test"),
            FlextMeltanoConfigurationError("test"),
            FlextMeltanoConnectionError("test"),
            FlextMeltanoProcessingError("test"),
            FlextMeltanoAuthenticationError("test"),
            FlextMeltanoTimeoutError("test"),
        ]

        for exception in core_exceptions:
            # These don't inherit from FlextMeltanoError, but do inherit from Exception
            assert isinstance(exception, Exception)

    def test_exception_chaining(self):
        """Test exception chaining works."""
        original = ValueError("original")

        try:
            raise original
        except ValueError:
            error_message = "chained"
            with pytest.raises(FlextMeltanoError) as exc_info:
                raise FlextMeltanoError(error_message) from original

        chained = exc_info.value
        assert chained.__cause__ is original

    def test_exception_messages(self):
        """Test exception messages are preserved."""
        test_message = "Test exception message"

        exceptions = [
            FlextMeltanoError(test_message),
            FlextMeltanoValidationError(test_message),
            FlextMeltanoConfigurationError(test_message),
            FlextMeltanoConnectionError(test_message),
            FlextMeltanoProcessingError(test_message),
            FlextMeltanoAuthenticationError(test_message),
            FlextMeltanoTimeoutError(test_message),
            FlextMeltanoPluginError(test_message),
            FlextMeltanoExecutionError(test_message),
            FlextMeltanoSingerError(test_message),
            FlextMeltanoDBTError(test_message),
        ]

        for exception in exceptions:
            assert test_message in str(exception)

    def test_all_exceptions_are_raisable(self):
        """Test that all exceptions can be raised and caught."""
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
            msg = "Test exception"
            with pytest.raises(exception_class):
                raise exception_class(msg)

    def test_import_all_exceptions(self):
        """Test that all exceptions can be imported."""
        # This test exercises the import paths
        assert FlextMeltanoError is not None
        assert FlextMeltanoValidationError is not None
        assert FlextMeltanoConfigurationError is not None
        assert FlextMeltanoConnectionError is not None
        assert FlextMeltanoProcessingError is not None
        assert FlextMeltanoAuthenticationError is not None
        assert FlextMeltanoTimeoutError is not None
        assert FlextMeltanoPluginError is not None
        assert FlextMeltanoExecutionError is not None
        assert FlextMeltanoSingerError is not None
        assert FlextMeltanoDBTError is not None
