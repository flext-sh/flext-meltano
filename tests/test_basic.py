"""Basic tests for FLEXT Meltano simplified architecture."""

from __future__ import annotations

import pytest

import flext_meltano


class TestFlextMeltanoResult:
    """Test FlextMeltanoResult functionality."""

    def test_ok_result(self) -> None:
        """Test successful result creation."""
        result = flext_meltano.FlextMeltanoResult.ok({"test": "data"})

        assert result.success is True
        assert result.is_success is True
        assert result.is_failure is False
        assert result.data == {"test": "data"}
        assert result.error is None

    def test_fail_result(self) -> None:
        """Test failed result creation."""
        result: flext_meltano.FlextMeltanoResult[str] = flext_meltano.FlextMeltanoResult.fail("test error")

        assert result.success is False
        assert result.is_success is False
        assert result.is_failure is True
        assert result.data is None
        assert result.error == "test error"

    def test_unwrap_success(self) -> None:
        """Test unwrapping successful result."""
        result = flext_meltano.FlextMeltanoResult.ok("test_data")

        assert result.unwrap() == "test_data"

    def test_unwrap_failure_raises(self) -> None:
        """Test unwrapping failed result raises exception."""
        result: flext_meltano.FlextMeltanoResult[str] = flext_meltano.FlextMeltanoResult.fail("test error")

        with pytest.raises(ValueError, match="Result failed: test error"):
            result.unwrap()

    def test_unwrap_or_with_success(self) -> None:
        """Test unwrap_or with successful result."""
        result = flext_meltano.FlextMeltanoResult.ok("test_data")

        assert result.unwrap_or("default") == "test_data"

    def test_unwrap_or_with_failure(self) -> None:
        """Test unwrap_or with failed result."""
        result: flext_meltano.FlextMeltanoResult[str] = flext_meltano.FlextMeltanoResult.fail("test error")

        assert result.unwrap_or("default") == "default"


class TestFlextMeltanoHelpers:
    """Test helper functions."""

    def test_validate_project_missing_meltano_yml(self) -> None:
        """Test project validation with missing meltano.yml."""
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            result = flext_meltano.flext_meltano_validate_project(temp_dir)

        assert result.is_failure is True
        assert result.error is not None
        assert "meltano.yml not found" in result.error

    def test_validate_project_nonexistent_directory(self) -> None:
        """Test project validation with nonexistent directory."""
        result = flext_meltano.flext_meltano_validate_project("/nonexistent/path")

        assert result.is_failure is True
        assert result.error is not None
        assert "meltano.yml not found" in result.error


class TestFlextMeltanoExceptions:
    """Test exception hierarchy."""

    def test_base_exception(self) -> None:
        """Test base FlextMeltanoError."""
        error = flext_meltano.FlextMeltanoError("test message")

        assert str(error) == "test message"
        assert error.message == "test message"
        assert error.context == {}

    def test_exception_with_context(self) -> None:
        """Test FlextMeltanoError with context."""
        context = {"key": "value"}
        error = flext_meltano.FlextMeltanoError("test message", context=context)

        assert "test message" in str(error)
        assert "Context:" in str(error)
        assert error.context == context

    def test_configuration_error_inheritance(self) -> None:
        """Test ConfigurationError inherits from base."""
        error = flext_meltano.FlextMeltanoConfigurationError("config error")

        assert isinstance(error, flext_meltano.FlextMeltanoError)
        assert isinstance(error, Exception)

    def test_validation_error_inheritance(self) -> None:
        """Test ValidationError inherits from base."""
        error = flext_meltano.FlextMeltanoValidationError("validation error")

        assert isinstance(error, flext_meltano.FlextMeltanoError)
        assert isinstance(error, Exception)


class TestImports:
    """Test module imports and API."""

    def test_version_available(self) -> None:
        """Test version is available."""
        assert hasattr(flext_meltano, "__version__")
        assert isinstance(flext_meltano.__version__, str)
        assert flext_meltano.__version__ == "1.0.0"

    def test_author_available(self) -> None:
        """Test author is available."""
        assert hasattr(flext_meltano, "__author__")
        assert flext_meltano.__author__ == "FLEXT Team"

    def test_all_exports_available(self) -> None:
        """Test all expected exports are available."""
        expected_exports = {
            "FlextMeltanoResult",
            "flext_meltano_execute_job",
            "flext_meltano_run_command",
            "flext_meltano_validate_project",
            "FlextMeltanoError",
            "FlextMeltanoConfigurationError",
            "FlextMeltanoValidationError",
            "__version__",
            "__author__",
        }

        for export in expected_exports:
            assert hasattr(flext_meltano, export), f"Missing export: {export}"
