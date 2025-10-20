"""Compatibility module for missing flext-tests dependency.

This module provides compatibility functions and classes that would normally
be imported from flext-tests, but since that dependency is missing, we provide
minimal implementations here.
"""

from __future__ import annotations

from collections.abc import Container
from typing import TypeVar

from flext_core import FlextResult

T = TypeVar("T")


class FlextTestsMatchers:
    """Test matchers for FlextResult assertions."""

    @staticmethod
    def assert_result_success(
        result: FlextResult[object], *, check_value: bool = True
    ) -> None:
        """Assert that a FlextResult is successful."""
        assert result.is_success, f"Expected success, got failure: {result.error}"
        if check_value:
            assert result.value is not None, "Expected result value to be non-None"

    @staticmethod
    def assert_result_failure(result: FlextResult[object]) -> None:
        """Assert that a FlextResult is a failure."""
        assert not result.is_success, f"Expected failure, got success: {result.value}"
        assert result.error is not None, "Expected error to be non-None"

    @staticmethod
    def assert_true(*, condition: bool, message: str = "Assertion failed") -> None:
        """Assert that a condition is true."""
        assert condition, message

    @staticmethod
    def assert_false(*, condition: bool, message: str = "Assertion failed") -> None:
        """Assert that a condition is false."""
        assert not condition, message

    @staticmethod
    def assert_in(
        item: T, container: Container[T], message: str = "Item not found in container"
    ) -> None:
        """Assert that an item is in a container."""
        assert item in container, message

    @staticmethod
    def assert_not_in(
        item: T, container: Container[T], message: str = "Item found in container"
    ) -> None:
        """Assert that an item is not in a container."""
        assert item not in container, message

    @staticmethod
    def assert_equal(a: object, b: object, message: str = "Values not equal") -> None:
        """Assert that two values are equal."""
        assert a == b, message

    @staticmethod
    def assert_equals(a: object, b: object, message: str = "Values not equal") -> None:
        """Assert that two values are equal (alias for assert_equal)."""
        assert a == b, message

    @staticmethod
    def assert_is_none(value: object, message: str = "Value is not None") -> None:
        """Assert that a value is None."""
        assert value is None, message

    @staticmethod
    def assert_is_not_none(value: object, message: str = "Value is None") -> None:
        """Assert that a value is not None."""
        assert value is not None, message


class FlextTestsUtilities:
    """Test utilities for common test operations."""

    @staticmethod
    def create_test_config() -> dict[str, object]:
        """Create a basic test configuration."""
        return {
            "test_mode": True,
            "log_level": "DEBUG",
            "timeout": 30,
        }

    @staticmethod
    def create_mock_service() -> dict[str, object]:
        """Create a mock service configuration."""
        return {
            "service_name": "test_service",
            "version": "1.0.0",
            "status": "active",
        }

    @classmethod
    def utilities(cls) -> "FlextTestsUtilities":
        """Get utilities instance."""
        return cls()

    @classmethod
    def assertion(cls) -> FlextTestsMatchers:
        """Get assertion matchers."""
        return FlextTestsMatchers()

    @staticmethod
    def functional_service(service_type: str = "api", **config: object) -> dict[str, object]:
        """Create a functional service configuration for testing."""
        base_config: dict[str, object] = {
            "type": service_type,
            "name": f"functional_{service_type}_service",
            "enabled": True,
            "host": "localhost",
            "port": 8000,
            "timeout": 30,
            "retries": 3,
        }
        base_config.update(config)
        return base_config

    @staticmethod
    def create_test_result(value: object | None = None, error: str | None = None) -> dict[str, object]:
        """Create a test result dictionary."""
        return {
            "value": value,
            "error": error,
            "status": "success" if error is None else "error",
        }

    @staticmethod
    def create_test_data(**data: object) -> dict[str, object]:
        """Create test data dictionary."""
        return dict(data) if data else {"test_data": "default"}
