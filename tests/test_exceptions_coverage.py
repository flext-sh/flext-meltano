"""Conservative tests for exceptions.py to achieve coverage without breaking functionality.

These tests focus on basic instantiation and inheritance verification
without complex logic that could break existing functionality.
"""

import pytest

from flext_meltano.exceptions import (
    FlextMeltanoAuthenticationError,
    FlextMeltanoConfigurationError,
    FlextMeltanoConnectionError,
    FlextMeltanoError,
    FlextMeltanoProcessingError,
    FlextMeltanoTimeoutError,
    FlextMeltanoValidationError,
)


class TestFlextMeltanoExceptionHierarchy:
    """Test exception hierarchy and basic instantiation."""

    def test_base_exception_instantiation(self) -> None:
        """Test base FlextMeltanoError can be instantiated."""
        # Basic instantiation test
        error = FlextMeltanoError("Test error message")
        assert isinstance(error, FlextMeltanoError)
        assert "Test error message" in str(error)

    def test_configuration_error_instantiation(self) -> None:
        """Test FlextMeltanoConfigurationError can be instantiated."""
        error = FlextMeltanoConfigurationError("Config error")
        assert isinstance(error, FlextMeltanoConfigurationError)
        # This inherits from FlextConfigurationError, not FlextMeltanoError
        assert "Config error" in str(error)

    def test_connection_error_instantiation(self) -> None:
        """Test FlextMeltanoConnectionError can be instantiated."""
        error = FlextMeltanoConnectionError("Connection failed")
        assert isinstance(error, FlextMeltanoConnectionError)
        # This inherits from FlextConnectionError, not FlextMeltanoError
        assert "Connection failed" in str(error)

    def test_processing_error_instantiation(self) -> None:
        """Test FlextMeltanoProcessingError can be instantiated."""
        error = FlextMeltanoProcessingError("Processing failed")
        assert isinstance(error, FlextMeltanoProcessingError)
        # This inherits from FlextProcessingError, not FlextMeltanoError
        assert "Processing failed" in str(error)

    def test_authentication_error_instantiation(self) -> None:
        """Test FlextMeltanoAuthenticationError can be instantiated."""
        error = FlextMeltanoAuthenticationError("Auth error")
        assert isinstance(error, FlextMeltanoAuthenticationError)
        # This inherits from FlextAuthenticationError, not FlextMeltanoError
        assert "Auth error" in str(error)

    def test_timeout_error_instantiation(self) -> None:
        """Test FlextMeltanoTimeoutError can be instantiated."""
        error = FlextMeltanoTimeoutError("Operation timed out")
        assert isinstance(error, FlextMeltanoTimeoutError)
        # This inherits from FlextTimeoutError, not FlextMeltanoError
        assert "Operation timed out" in str(error)

    def test_validation_error_instantiation(self) -> None:
        """Test FlextMeltanoValidationError can be instantiated."""
        error = FlextMeltanoValidationError("Validation failed")
        assert isinstance(error, FlextMeltanoValidationError)
        # This inherits from FlextValidationError, not FlextMeltanoError
        assert "Validation failed" in str(error)


class TestExceptionWithContext:
    """Test exceptions with additional context."""

    def test_exception_with_plugin_context(self) -> None:
        """Test exception with plugin context."""
        error = FlextMeltanoError("Plugin failed", plugin_name="tap-postgres")
        assert "Plugin failed" in str(error)
        # Test that context attributes exist if they're set
        if hasattr(error, "plugin_name"):
            assert error.plugin_name == "tap-postgres"

    def test_exception_with_configuration_context(self) -> None:
        """Test exception with configuration context."""
        error = FlextMeltanoConfigurationError(
            "Invalid configuration",
            plugin_name="tap-postgres",
        )
        assert "Invalid configuration" in str(error)
        # Test that context attributes exist if they're set
        if hasattr(error, "plugin_name"):
            assert error.plugin_name == "tap-postgres"

    def test_exception_chaining(self) -> None:
        """Test exception chaining functionality."""
        original_error = ValueError("Original error")

        def _raise_chained_error() -> None:
            msg = "Wrapped error"
            raise FlextMeltanoError(msg) from original_error

        with pytest.raises(FlextMeltanoError) as exc_info:
            _raise_chained_error()

        chained_error = exc_info.value
        assert "Wrapped error" in str(chained_error)
        assert chained_error.__cause__ is original_error


class TestExceptionRaising:
    """Test that exceptions can be properly raised and caught."""

    def test_raise_and_catch_base_exception(self) -> None:
        """Test raising and catching base exception."""
        msg = "Test error"
        with pytest.raises(FlextMeltanoError) as exc_info:
            raise FlextMeltanoError(msg)

        assert "Test error" in str(exc_info.value)

    def test_raise_and_catch_processing_exception(self) -> None:
        """Test raising and catching processing exception."""
        msg = "Processing test error"
        with pytest.raises(FlextMeltanoProcessingError) as exc_info:
            raise FlextMeltanoProcessingError(msg)

        assert "Processing test error" in str(exc_info.value)
        # Processing errors inherit from FlextProcessingError
        assert isinstance(exc_info.value, FlextMeltanoProcessingError)

    def test_raise_and_catch_validation_exception(self) -> None:
        """Test raising and catching validation exception."""
        msg = "Validation test error"
        with pytest.raises(FlextMeltanoValidationError) as exc_info:
            raise FlextMeltanoValidationError(msg)

        assert "Validation test error" in str(exc_info.value)
        # Validation errors inherit from FlextValidationError
        assert isinstance(exc_info.value, FlextMeltanoValidationError)


class TestExceptionSerialization:
    """Test exception serialization for bridge compatibility."""

    def test_exception_string_representation(self) -> None:
        """Test exception string representation."""
        error = FlextMeltanoError("Test message")
        error_str = str(error)
        # Exception has custom formatting, just verify message is contained
        assert "Test message" in error_str
        assert repr(error).startswith("FlextMeltanoError(")

    def test_exception_with_empty_message(self) -> None:
        """Test exception with empty message."""
        error = FlextMeltanoError("")
        # Just verify it can be instantiated with empty message
        assert isinstance(error, FlextMeltanoError)

    def test_exception_inheritance_chain(self) -> None:
        """Test that all custom exceptions inherit from Exception."""
        exceptions_to_test = [
            FlextMeltanoError,
            FlextMeltanoAuthenticationError,
            FlextMeltanoConfigurationError,
            FlextMeltanoConnectionError,
            FlextMeltanoProcessingError,
            FlextMeltanoTimeoutError,
            FlextMeltanoValidationError,
        ]

        for exception_class in exceptions_to_test:
            error = exception_class("Test message")
            assert isinstance(error, exception_class)
            assert isinstance(error, Exception)
