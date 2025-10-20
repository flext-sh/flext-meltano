"""Flext Tests Matchers Mock."""

from __future__ import annotations


class FlextTestsMatchers:
    """Mock matchers for testing."""

    @staticmethod
    def contains_string(substring: str) -> FlextTestsMatcher:
        """Create a matcher that checks if string contains substring."""
        return FlextTestsMatcher("contains", substring)

    @staticmethod
    def equals(expected: object) -> FlextTestsMatcher:
        """Create a matcher that checks equality."""
        return FlextTestsMatcher("equals", expected)

    @staticmethod
    def has_length(length: int) -> FlextTestsMatcher:
        """Create a matcher that checks length."""
        return FlextTestsMatcher("length", length)


class FlextTestsMatcher:
    """Mock matcher implementation."""

    def __init__(self, match_type: str, value: object) -> None:
        """Initialize matcher."""
        self.match_type = match_type
        self.value = value

    def matches(self, actual: object) -> bool:
        """Check if actual matches the expected value."""
        if self.match_type == "contains":
            return (
                isinstance(actual, str)
                and isinstance(self.value, str)
                and self.value in actual
            )
        if self.match_type == "equals":
            return actual == self.value
        if self.match_type == "length":
            # Check if object has __len__ and cast to proper type for len()
            return (
                hasattr(actual, "__len__")
                and len(actual) == self.value  # type: ignore[arg-type]
            )
        return False
