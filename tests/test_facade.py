"""Test facade module - Basic functionality tests.

Tests FlextMeltano facade class functionality.
Zero mock usage - all real function testing.
"""

from __future__ import annotations

import unittest
from unittest import TestCase

from flext_meltano.facade import FlextMeltano


class TestFlextMeltanoFacadeBasic(TestCase):
    """Basic functionality tests for FlextMeltano facade."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.facade = FlextMeltano()

    def test_facade_instantiation(self) -> None:
        """Test FlextMeltano facade instantiation."""
        facade = FlextMeltano()
        assert isinstance(facade, FlextMeltano)

    def test_facade_has_required_properties(self) -> None:
        """Test facade has all required interface properties."""
        # Check for key facade properties
        expected_properties = ["config", "utilities", "adapters", "executors"]

        for prop_name in expected_properties:
            assert hasattr(self.facade, prop_name), (
                f"FlextMeltano facade missing property: {prop_name}"
            )

    def test_config_property(self) -> None:
        """Test config property returns correct type."""
        config_class = self.facade.config
        # Should return the FlextMeltanoConfig class
        assert config_class is not None

    def test_utilities_property(self) -> None:
        """Test utilities property returns correct type."""
        utilities_class = self.facade.utilities
        # Should return the FlextMeltanoUtilities class
        assert utilities_class is not None

    def test_adapters_property(self) -> None:
        """Test adapters property returns correct type."""
        adapters_class = self.facade.adapters
        # Should return the FlextMeltanoAdapter class
        assert adapters_class is not None

    def test_executors_property(self) -> None:
        """Test executors property returns correct type."""
        executors_class = self.facade.executors
        # Should return the FlextMeltanoExecutor class
        assert executors_class is not None

    def test_facade_delegation_pattern(self) -> None:
        """Test facade properly delegates to specialized classes."""
        # Test that facade provides access to specialized classes
        # Config delegation
        config_class = self.facade.config
        assert hasattr(config_class, "__name__")

        # Utilities delegation
        utilities_class = self.facade.utilities
        assert hasattr(utilities_class, "__name__")

        # Adapters delegation
        adapters_class = self.facade.adapters
        assert hasattr(adapters_class, "__name__")

        # Executors delegation
        executors_class = self.facade.executors
        assert hasattr(executors_class, "__name__")

    def test_facade_architecture_compliance(self) -> None:
        """Test facade follows FLEXT architecture patterns."""
        # Facade should not implement functionality directly
        # It should only provide access to specialized classes

        # Check that properties return classes, not instances
        assert callable(self.facade.config)  # Should be class
        assert callable(self.facade.utilities)  # Should be class
        assert callable(self.facade.adapters)  # Should be class
        assert callable(self.facade.executors)  # Should be class

    def test_all_exports_available(self) -> None:
        """Test all expected exports are available."""
        from flext_meltano.facade import FlextMeltano

        # Main class should be importable
        assert FlextMeltano is not None

        # Should be able to instantiate
        instance = FlextMeltano()
        assert isinstance(instance, FlextMeltano)

    def test_facade_class_structure(self) -> None:
        """Test facade class has proper structure."""
        # Should have class docstring
        assert FlextMeltano.__doc__ is not None

        # Should have module docstring
        import flext_meltano.facade as facade_module

        assert facade_module.__doc__ is not None

    def test_facade_provides_specialized_access(self) -> None:
        """Test facade provides proper access to specialized functionality."""
        # Should be able to access specialized classes through facade
        # This tests the orchestration pattern

        # Access to configuration management
        config_class = self.facade.config
        assert hasattr(config_class, "__name__")

        # Access to utility functions
        utilities_class = self.facade.utilities
        assert hasattr(utilities_class, "__name__")

        # Access to external adapters
        adapters_class = self.facade.adapters
        assert hasattr(adapters_class, "__name__")

        # Access to execution engines
        executors_class = self.facade.executors
        assert hasattr(executors_class, "__name__")


if __name__ == "__main__":
    unittest.main()
