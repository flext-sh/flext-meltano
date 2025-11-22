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


class FunctionalServiceMock:
    """Mock functional service with configuration support."""

    def __init__(self, service_type: str, **config: object) -> None:
        """Initialize functional service mock."""
        self.service_type = service_type
        self.config = config
        self._configured_methods: dict[str, dict[str, object]] = {}

    def configure_method(
        self,
        method_name: str,
        return_value: object = None,
        side_effect: object = None,
        *,
        should_fail: bool = False,
        failure_message: str | None = None,
    ) -> None:
        """Configure a method with a return value or side effect.

        Args:
            method_name: Name of the method to configure
            return_value: Return value for the method
            side_effect: Side effect to execute
            should_fail: Whether this method should fail
            failure_message: Error message if should_fail is True

        """
        # Use create_entry for consistent data structure
        self._configured_methods[method_name] = FlextTestsUtilities.create_entry(
            "method_config",
            return_value=return_value,
            side_effect=side_effect,
            should_fail=should_fail,
            failure_message=failure_message or "Method configured to fail",
        )

    def get_configured_value(self, method_name: str) -> object:
        """Get configured return value for a method."""
        if method_name in self._configured_methods:
            return self._configured_methods[method_name].get("return_value")
        return None

    def should_fail(self, method_name: str) -> bool:
        """Check if a method is configured to fail."""
        if method_name in self._configured_methods:
            return bool(self._configured_methods[method_name].get("should_fail", False))
        return False

    def get_failure_message(self, method_name: str) -> str:
        """Get failure message for a method."""
        if method_name in self._configured_methods:
            return str(
                self._configured_methods[method_name].get(
                    "failure_message", "Method configured to fail"
                )
            )
        return "Method configured to fail"


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
    def create_entry(entry_type: str, **overrides: object) -> dict[str, object]:
        """Create a generalized entry with defaults and overrides.

        Args:
            entry_type: Type of entry to create ('service', 'result', 'data', etc.)
            **overrides: Key-value pairs to override defaults

        Returns:
            Dictionary with entry data

        """
        defaults: dict[str, dict[str, object]] = {
            "service": {
                "service_name": "test_service",
                "version": "1.0.0",
                "status": "active",
            },
            "result": {
                "value": None,
                "error": None,
                "status": "success",
            },
            "data": {
                "items": [],
                "count": 0,
                "metadata": {},
            },
            "method_config": {
                "return_value": None,
                "side_effect": None,
                "should_fail": False,
                "failure_message": "Method configured to fail",
            },
        }

        if entry_type not in defaults:
            raise ValueError(f"Unknown entry type: {entry_type}")

        entry = defaults[entry_type].copy()
        entry.update(overrides)

        # Auto-update status for result entries
        if entry_type == "result" and entry.get("error") is not None:
            entry["status"] = "error"

        return entry

    @classmethod
    def utilities(cls) -> FlextTestsUtilities:
        """Get utilities instance."""
        return cls()

    @classmethod
    def assertion(cls) -> FlextTestsMatchers:
        """Get assertion matchers."""
        return FlextTestsMatchers()

    @staticmethod
    def functional_service(
        service_type: str = "api", **config: object
    ) -> FunctionalServiceMock:
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
        return FunctionalServiceMock(service_type, **base_config)

    @staticmethod
    def create_entries(
        entry_type: str,
        size: int | None = None,
        prefix: str | None = None,
        **overrides: object,
    ) -> list[dict[str, object]] | dict[str, object]:
        """Create multiple entries or a single entry with generation logic.

        Args:
            entry_type: Type of entry to create
            size: Number of entries to create (returns list if set)
            prefix: Prefix for generated names
            **overrides: Key-value pairs to override defaults

        Returns:
            List of entries if size is specified, otherwise single entry

        """
        if size is not None:
            # Generate list of entries
            items: list[dict[str, object]] = []
            for i in range(size):
                item_overrides = overrides.copy()
                item_overrides.update({
                    "id": i + 1,
                    "name": f"{prefix}_{i + 1}" if prefix else f"item_{i + 1}",
                })
                item = FlextTestsUtilities.create_entry(entry_type, **item_overrides)
                items.append(item)
            return items
        # Generate single entry
        item_overrides = overrides.copy()
        if prefix:
            item_overrides["name"] = f"{prefix}_1"
        return FlextTestsUtilities.create_entry(entry_type, **item_overrides)
