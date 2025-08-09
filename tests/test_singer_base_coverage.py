"""FLEXT Meltano Singer Base Coverage Tests - Simplified Exception Testing.

This module provides test coverage for the Singer exception handling in flext-meltano,
using the actual exception classes available in the project.
"""

# Import Singer exceptions from flext_meltano.exceptions
from flext_meltano.exceptions import (
    FlextMeltanoAuthenticationError,
    FlextMeltanoConfigurationError,
    FlextMeltanoConnectionError,
    FlextMeltanoError,
    FlextMeltanoProcessingError,
    FlextMeltanoSingerError,
    FlextMeltanoValidationError,
)


class TestFlextMeltanoSingerError:
    """Test FlextMeltanoSingerError base exception class."""

    def test_singer_error_default_initialization(self) -> None:
        """Test FlextMeltanoSingerError with default parameters."""
        error = FlextMeltanoSingerError()
        assert isinstance(error, FlextMeltanoError)
        assert "Singer error" in str(error)

    def test_singer_error_with_message(self) -> None:
        """Test FlextMeltanoSingerError with custom message."""
        message = "Custom Singer operation failed"
        error = FlextMeltanoSingerError(message)
        assert message in str(error)

    def test_singer_error_inheritance(self) -> None:
        """Test FlextMeltanoSingerError inheritance."""
        error = FlextMeltanoSingerError("Test error")
        assert isinstance(error, FlextMeltanoError)
        assert isinstance(error, Exception)


class TestFlextMeltanoConnectionError:
    """Test FlextMeltanoConnectionError for connection-related failures."""

    def test_connection_error_initialization(self) -> None:
        """Test FlextMeltanoConnectionError initialization."""
        error = FlextMeltanoConnectionError("Connection failed")
        assert isinstance(error, FlextMeltanoError)
        assert "Connection failed" in str(error)

    def test_connection_error_inheritance(self) -> None:
        """Test FlextMeltanoConnectionError inheritance."""
        error = FlextMeltanoConnectionError("Test connection error")
        assert isinstance(error, FlextMeltanoConnectionError)
        assert isinstance(error, Exception)


class TestFlextMeltanoConfigurationError:
    """Test FlextMeltanoConfigurationError for configuration-related failures."""

    def test_configuration_error_initialization(self) -> None:
        """Test FlextMeltanoConfigurationError initialization."""
        error = FlextMeltanoConfigurationError("Configuration error")
        assert isinstance(error, FlextMeltanoError)
        assert "Configuration error" in str(error)

    def test_configuration_error_inheritance(self) -> None:
        """Test FlextMeltanoConfigurationError inheritance."""
        error = FlextMeltanoConfigurationError("Test configuration error")
        assert isinstance(error, FlextMeltanoConfigurationError)
        assert isinstance(error, Exception)


class TestFlextMeltanoValidationError:
    """Test FlextMeltanoValidationError for validation failures."""

    def test_validation_error_initialization(self) -> None:
        """Test FlextMeltanoValidationError initialization."""
        error = FlextMeltanoValidationError("Validation failed")
        assert isinstance(error, FlextMeltanoError)
        assert "Validation failed" in str(error)

    def test_validation_error_inheritance(self) -> None:
        """Test FlextMeltanoValidationError inheritance."""
        error = FlextMeltanoValidationError("Test validation error")
        assert isinstance(error, FlextMeltanoValidationError)
        assert isinstance(error, Exception)