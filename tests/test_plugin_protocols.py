"""Test module for flext-meltano."""

from __future__ import annotations

import unittest
from unittest import TestCase

import flext_meltano.plugin_protocols as protocols_module
from flext_meltano.plugin_protocols import (
    DbtServiceProtocol,
    FlextDbtPlugin,
    FlextMeltanoPluginProtocols,  # Updated unified class name
    FlextTapPlugin,
    FlextTargetPlugin,
    TapServiceProtocol,
    TargetServiceProtocol,
)


class TestFlextMeltanoPluginProtocolsBasic(TestCase):
    """Basic functionality tests for FlextMeltanoPluginProtocols."""

    def test_class_exists(self) -> None:
        """Test FlextMeltanoPluginProtocols class exists."""
        assert hasattr(FlextMeltanoPluginProtocols, "__name__")
        assert FlextMeltanoPluginProtocols.__name__ == "FlextMeltanoPluginProtocols"

    def test_has_plugin_type_definitions(self) -> None:
        """Test FlextMeltanoPluginProtocols has plugin type definitions."""
        expected_plugin_types = [
            "TapPlugin",
            "TargetPlugin",
            "DbtPlugin",
            "TapService",
            "TargetService",
            "DbtService",
        ]

        for plugin_type in expected_plugin_types:
            assert hasattr(FlextMeltanoPluginProtocols, plugin_type), (
                f"FlextMeltanoPluginProtocols missing plugin type: {plugin_type}"
            )

    def test_tap_plugin_protocol(self) -> None:
        """Test TapPlugin protocol definition."""
        protocol = FlextMeltanoPluginProtocols.TapPlugin

        # Should be a class or type
        assert protocol is not None
        # Minimal plugin type - should exist
        assert protocol is object

    def test_target_plugin_protocol(self) -> None:
        """Test TargetPlugin protocol definition."""
        protocol = FlextMeltanoPluginProtocols.TargetPlugin

        # Should be a class or type
        assert protocol is not None
        # Minimal plugin type - should exist
        assert protocol is object

    def test_dbt_plugin_protocol(self) -> None:
        """Test DbtPlugin protocol definition."""
        protocol = FlextMeltanoPluginProtocols.DbtPlugin

        # Should be a class or type
        assert protocol is not None
        # Minimal plugin type - should exist
        assert protocol is object

    def test_service_protocol_aliases(self) -> None:
        """Test service protocol aliases exist."""
        # TapService should alias TapPlugin
        assert (
            FlextMeltanoPluginProtocols.TapService
            is FlextMeltanoPluginProtocols.TapPlugin
        )

        # TargetService should alias TargetPlugin
        assert (
            FlextMeltanoPluginProtocols.TargetService
            is FlextMeltanoPluginProtocols.TargetPlugin
        )

        # DbtService should alias DbtPlugin
        assert (
            FlextMeltanoPluginProtocols.DbtService
            is FlextMeltanoPluginProtocols.DbtPlugin
        )

    def test_backward_compatibility_aliases(self) -> None:
        """Test backward compatibility aliases exist."""
        # FlextTapPlugin should alias TapPlugin
        assert (
            FlextMeltanoPluginProtocols.FlextTapPlugin
            is FlextMeltanoPluginProtocols.TapPlugin
        )

        # FlextTargetPlugin should alias TargetPlugin
        assert (
            FlextMeltanoPluginProtocols.FlextTargetPlugin
            is FlextMeltanoPluginProtocols.TargetPlugin
        )

        # FlextDbtPlugin should alias DbtPlugin
        assert (
            FlextMeltanoPluginProtocols.FlextDbtPlugin
            is FlextMeltanoPluginProtocols.DbtPlugin
        )

    def test_nested_types_structure(self) -> None:
        """Test nested types structure exists."""
        # Should have proper class structure
        assert hasattr(FlextMeltanoPluginProtocols, "__module__")
        assert (
            FlextMeltanoPluginProtocols.__module__ == "flext_meltano.plugin_protocols"
        )

    def test_module_level_aliases(self) -> None:
        """Test module-level backward compatibility aliases."""
        # All should be importable
        assert FlextTapPlugin is not None
        assert FlextTargetPlugin is not None
        assert FlextDbtPlugin is not None
        assert TapServiceProtocol is not None
        assert TargetServiceProtocol is not None
        assert DbtServiceProtocol is not None

    def test_import_works(self) -> None:
        """Test importing from module works."""
        # Should be importable without errors
        assert FlextMeltanoPluginProtocols is not None

        # Should have expected structure
        assert hasattr(FlextMeltanoPluginProtocols, "__name__")

    def test_class_documentation(self) -> None:
        """Test class has proper documentation."""
        # Should have class docstring
        assert FlextMeltanoPluginProtocols.__doc__ is not None

        # Should have module docstring
        assert protocols_module.__doc__ is not None


if __name__ == "__main__":
    unittest.main()
