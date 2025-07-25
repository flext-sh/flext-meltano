"""Tests for FLEXT Meltano SDK module.

Comprehensive tests for custom exception classes.
Zero tolerance for untested code.
"""

from __future__ import annotations

import pytest

from flext_meltano.sdk import (
    FlextMeltanoConfigError,
    FlextMeltanoError,
    FlextMeltanoExecutionError,
    FlextMeltanoPluginError,
    FlextMeltanoProjectError,
    FlextMeltanoStateError,
)


class TestFlextMeltanoError:
    """Test FlextMeltanoError base exception class."""

    def test_meltano_error_basic_creation(self) -> None:
        """Test basic creation of FlextMeltanoError."""
        error = FlextMeltanoError("Test error message")
        assert str(error) == "Test error message"
        assert error.args == ("Test error message",)

    def test_meltano_error_inheritance(self) -> None:
        """Test that FlextMeltanoError inherits from Exception."""
        error = FlextMeltanoError("Test error")
        assert isinstance(error, Exception)
        assert isinstance(error, FlextMeltanoError)

    def test_meltano_error_empty_message(self) -> None:
        """Test FlextMeltanoError with empty message."""
        error = FlextMeltanoError("")
        assert str(error) == ""

    def test_meltano_error_raising(self) -> None:
        """Test raising FlextMeltanoError."""
        msg = "Test exception"
        with pytest.raises(FlextMeltanoError) as exc_info:
            raise FlextMeltanoError(msg)
        assert str(exc_info.value) == "Test exception"

    def test_meltano_error_catching(self) -> None:
        """Test catching FlextMeltanoError."""
        msg = "Catch test"
        with pytest.raises(FlextMeltanoError, match="Catch test"):
            raise FlextMeltanoError(msg)


class TestFlextMeltanoProjectError:
    """Test FlextMeltanoProjectError exception class."""

    def test_project_error_creation(self) -> None:
        """Test creation of FlextMeltanoProjectError."""
        error = FlextMeltanoProjectError("Project error message")
        assert str(error) == "Project error message"

    def test_project_error_inheritance(self) -> None:
        """Test that FlextMeltanoProjectError inherits correctly."""
        error = FlextMeltanoProjectError("Test")
        assert isinstance(error, FlextMeltanoError)
        assert isinstance(error, FlextMeltanoProjectError)
        assert isinstance(error, Exception)

    def test_project_error_raising(self) -> None:
        """Test raising FlextMeltanoProjectError."""
        msg = "Project not found"
        with pytest.raises(FlextMeltanoProjectError):
            raise FlextMeltanoProjectError(msg)

    def test_project_error_catching_as_base(self) -> None:
        """Test catching FlextMeltanoProjectError as base FlextMeltanoError."""
        msg = "Project error"
        with pytest.raises(FlextMeltanoError):
            raise FlextMeltanoProjectError(msg)


class TestFlextMeltanoExecutionError:
    """Test FlextMeltanoExecutionError exception class."""

    def test_execution_error_basic_creation(self) -> None:
        """Test basic creation of FlextMeltanoExecutionError."""
        error = FlextMeltanoExecutionError("Execution failed")
        assert str(error) == "Execution failed"
        assert error.command is None
        assert error.returncode is None
        assert error.stdout is None
        assert error.stderr is None

    def test_execution_error_with_command(self) -> None:
        """Test FlextMeltanoExecutionError with command details."""
        command = ["meltano", "run", "tap-csv", "target-jsonl"]
        error = FlextMeltanoExecutionError(
            "Command failed",
            command=command,
            returncode=1,
            stdout="Some output",
            stderr="Error details",
        )

        assert str(error) == "Command failed"
        assert error.command == command
        assert error.returncode == 1
        assert error.stdout == "Some output"
        assert error.stderr == "Error details"

    def test_execution_error_inheritance(self) -> None:
        """Test that FlextMeltanoExecutionError inherits correctly."""
        error = FlextMeltanoExecutionError("Test")
        assert isinstance(error, FlextMeltanoError)
        assert isinstance(error, FlextMeltanoExecutionError)
        assert isinstance(error, Exception)

    def test_execution_error_partial_parameters(self) -> None:
        """Test FlextMeltanoExecutionError with partial parameters."""
        error = FlextMeltanoExecutionError(
            "Partial failure",
            command=["meltano", "test"],
            returncode=2,
        )

        assert error.command == ["meltano", "test"]
        assert error.returncode == 2
        assert error.stdout is None
        assert error.stderr is None

    def test_execution_error_empty_command(self) -> None:
        """Test FlextMeltanoExecutionError with empty command."""
        error = FlextMeltanoExecutionError("Failed", command=[])
        assert error.command == []

    def test_execution_error_raising_with_details(self) -> None:
        """Test raising FlextMeltanoExecutionError with full details."""
        msg = "Command execution failed"
        with pytest.raises(FlextMeltanoExecutionError) as exc_info:
            raise FlextMeltanoExecutionError(
                msg,
                command=["meltano", "run"],
                returncode=1,
                stdout="Output text",
                stderr="Error text",
            )

        error = exc_info.value
        assert error.command == ["meltano", "run"]
        assert error.returncode == 1
        assert error.stdout == "Output text"
        assert error.stderr == "Error text"

    def test_execution_error_init_parameters(self) -> None:
        """Test all parameters in __init__ method."""
        error = FlextMeltanoExecutionError(
            message="Custom message",
            command=["cmd", "arg1", "arg2"],
            returncode=42,
            stdout="standard output",
            stderr="standard error",
        )

        # Test all attributes are set correctly
        assert str(error) == "Custom message"
        assert error.command == ["cmd", "arg1", "arg2"]
        assert error.returncode == 42
        assert error.stdout == "standard output"
        assert error.stderr == "standard error"


class TestFlextMeltanoPluginError:
    """Test FlextMeltanoPluginError exception class."""

    def test_plugin_error_creation(self) -> None:
        """Test creation of FlextMeltanoPluginError."""
        error = FlextMeltanoPluginError("Plugin error message")
        assert str(error) == "Plugin error message"

    def test_plugin_error_inheritance(self) -> None:
        """Test that FlextMeltanoPluginError inherits correctly."""
        error = FlextMeltanoPluginError("Test")
        assert isinstance(error, FlextMeltanoError)
        assert isinstance(error, FlextMeltanoPluginError)
        assert isinstance(error, Exception)

    def test_plugin_error_raising(self) -> None:
        """Test raising FlextMeltanoPluginError."""
        msg = "Plugin installation failed"
        with pytest.raises(FlextMeltanoPluginError):
            raise FlextMeltanoPluginError(msg)


class TestFlextMeltanoStateError:
    """Test FlextMeltanoStateError exception class."""

    def test_state_error_creation(self) -> None:
        """Test creation of FlextMeltanoStateError."""
        error = FlextMeltanoStateError("State error message")
        assert str(error) == "State error message"

    def test_state_error_inheritance(self) -> None:
        """Test that FlextMeltanoStateError inherits correctly."""
        error = FlextMeltanoStateError("Test")
        assert isinstance(error, FlextMeltanoError)
        assert isinstance(error, FlextMeltanoStateError)
        assert isinstance(error, Exception)

    def test_state_error_raising(self) -> None:
        """Test raising FlextMeltanoStateError."""
        msg = "State management failed"
        with pytest.raises(FlextMeltanoStateError):
            raise FlextMeltanoStateError(msg)


class TestFlextMeltanoConfigError:
    """Test FlextMeltanoConfigError exception class."""

    def test_config_error_creation(self) -> None:
        """Test creation of FlextMeltanoConfigError."""
        error = FlextMeltanoConfigError("Config error message")
        assert str(error) == "Config error message"

    def test_config_error_inheritance(self) -> None:
        """Test that FlextMeltanoConfigError inherits correctly."""
        error = FlextMeltanoConfigError("Test")
        assert isinstance(error, FlextMeltanoError)
        assert isinstance(error, FlextMeltanoConfigError)
        assert isinstance(error, Exception)

    def test_config_error_raising(self) -> None:
        """Test raising FlextMeltanoConfigError."""
        msg = "Configuration invalid"
        with pytest.raises(FlextMeltanoConfigError):
            raise FlextMeltanoConfigError(msg)


class TestExceptionHierarchy:
    """Test the complete exception hierarchy and interactions."""

    def test_all_exceptions_inherit_from_base(self) -> None:
        """Test that all custom exceptions inherit from FlextMeltanoError."""
        exceptions = [
            FlextMeltanoProjectError,
            FlextMeltanoExecutionError,
            FlextMeltanoPluginError,
            FlextMeltanoStateError,
            FlextMeltanoConfigError,
        ]

        for exc_class in exceptions:
            assert issubclass(exc_class, FlextMeltanoError)
            assert issubclass(exc_class, Exception)

    def test_catching_specific_exceptions_as_base(self) -> None:
        """Test catching specific exceptions as base FlextMeltanoError."""
        exceptions_to_test = [
            FlextMeltanoProjectError("Project error"),
            FlextMeltanoExecutionError("Execution error"),
            FlextMeltanoPluginError("Plugin error"),
            FlextMeltanoStateError("State error"),
            FlextMeltanoConfigError("Config error"),
        ]

        for exc in exceptions_to_test:
            with pytest.raises(FlextMeltanoError):
                raise exc

    def test_exception_types_are_distinct(self) -> None:
        """Test that exception types are distinct and not identical."""
        exceptions = [
            FlextMeltanoError,
            FlextMeltanoProjectError,
            FlextMeltanoExecutionError,
            FlextMeltanoPluginError,
            FlextMeltanoStateError,
            FlextMeltanoConfigError,
        ]

        # All should be different types
        for i, exc1 in enumerate(exceptions):
            for j, exc2 in enumerate(exceptions):
                if i != j:
                    assert exc1 is not exc2

    def test_mixed_exception_handling(self) -> None:
        """Test handling multiple exception types in a single try block."""

        def raise_random_exception(exc_type: str) -> None:
            if exc_type == "project":
                msg = "Project error"
                raise FlextMeltanoProjectError(msg)
            if exc_type == "execution":
                msg = "Execution error"
                raise FlextMeltanoExecutionError(msg)
            if exc_type == "plugin":
                msg = "Plugin error"
                raise FlextMeltanoPluginError(msg)
            if exc_type == "state":
                msg = "State error"
                raise FlextMeltanoStateError(msg)
            if exc_type == "config":
                msg = "Config error"
                raise FlextMeltanoConfigError(msg)

        # Test catching all as base exception
        for exc_type in ["project", "execution", "plugin", "state", "config"]:
            with pytest.raises(FlextMeltanoError):
                raise_random_exception(exc_type)
