"""Minimal mock for flext-tests to enable testing.

This is a temporary mock to allow tests to run until the real flext-tests
dependency is available.
"""

from __future__ import annotations

from collections.abc import Callable, Container
from typing import Any, TypeVar
from unittest.mock import MagicMock

T = TypeVar("T")
ContainerT = TypeVar("ContainerT", bound=Container)


class FlextTestsUtilities:
    """Mock utilities for testing."""

    @staticmethod
    def utilities() -> FlextTestsUtilities:
        """Get utilities instance."""
        return FlextTestsUtilities()

    @staticmethod
    def assertion() -> FlextTestsAssertion:
        """Get assertion instance."""
        return FlextTestsAssertion()

    @staticmethod
    def functional_service(_service_name: str) -> object:
        """Get functional service mock.

        Args:
        _service_name: Service name (reserved for future filtering)

        Returns:
        Mock service object for testing

        """
        return MagicMock()


class FlextTestsAssertion:
    """Mock assertions for testing."""

    def assert_true(self, condition: bool, message: str) -> None:
        """Assert condition is true."""
        assert condition, message

    def assert_false(self, condition: bool, message: str) -> None:
        """Assert condition is false."""
        assert not condition, message

    def assert_equal(self, actual: object, expected: object, message: str = "") -> None:
        """Assert values are equal."""
        assert actual == expected, message or f"Expected {expected}, got {actual}"

    def assert_not_equal(
        self, actual: object, expected: object, message: str = ""
    ) -> None:
        """Assert values are not equal."""
        assert actual != expected, message or f"Values should not be equal: {actual}"

    def assert_is_none(self, value: object, message: str = "") -> None:
        """Assert value is None."""
        assert value is None, message or f"Expected None, got {value}"

    def assert_is_not_none(self, value: object, message: str = "") -> None:
        """Assert value is not None."""
        assert value is not None, message or f"Expected not None, got {value}"

    def assert_in(self, item: T, container: Container[T], message: str = "") -> None:
        """Assert item is in container."""
        assert item in container, message or f"{item} not in {container}"

    def assert_not_in(
        self, item: T, container: Container[T], message: str = ""
    ) -> None:
        """Assert item is not in container."""
        assert item not in container, message or f"{item} should not be in {container}"

    def assert_is_instance(self, obj: object, cls: type, message: str = "") -> None:
        """Assert object is instance of class."""
        assert isinstance(obj, cls), message or f"{obj} is not instance of {cls}"

    def assert_raises(
        self,
        exception: type[Exception],
        callable_obj: Callable[..., Any],
        *args: object,
        **kwargs: object,
    ) -> None:
        """Assert that callable raises exception."""
        try:
            callable_obj(*args, **kwargs)
            msg = f"Expected {exception.__name__} to be raised"
            raise AssertionError(msg)
        except exception:
            pass
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            msg = f"Expected {exception.__name__}, got {type(e).__name__}"
            raise AssertionError(msg) from None
