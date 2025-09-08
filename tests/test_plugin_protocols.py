"""Test plugin_protocols module - Basic functionality tests.

Tests FlextMeltanoPluginTypes protocol definitions.
Zero mock usage - all real function testing.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import unittest
from unittest import TestCase

import flext_meltano.plugin_protocols as protocols_module
from flext_meltano.plugin_protocols import (
    DbtServiceProtocol,
    FlextDbtPlugin,
    FlextMeltanoPluginTypes,
    FlextTapPlugin,
    FlextTargetPlugin,
    TapServiceProtocol,
    TargetServiceProtocol,
)


class TestFlextMeltanoPluginTypesBasic(TestCase):
    """Basic functionality tests for FlextMeltanoPluginTypes."""

    def test_class_exists(self) -> None:
        """Test FlextMeltanoPluginTypes class exists."""
        assert hasattr(FlextMeltanoPluginTypes, "__name__")
        assert FlextMeltanoPluginTypes.__name__ == "FlextMeltanoPluginTypes"

    def test_has_plugin_type_definitions(self) -> None:
        """Test FlextMeltanoPluginTypes has plugin type definitions."""
        expected_plugin_types = [
            "TapPlugin",
            "TargetPlugin",
            "DbtPlugin",
            "TapService",
            "TargetService",
            "DbtService",
        ]

        for plugin_type in expected_plugin_types:
            assert hasattr(FlextMeltanoPluginTypes, plugin_type), (
                f"FlextMeltanoPluginTypes missing plugin type: {plugin_type}"
            )

    def test_tap_plugin_protocol(self) -> None:
        """Test TapPlugin protocol definition."""
        protocol = FlextMeltanoPluginTypes.TapPlugin

        # Should be a class or type
        assert protocol is not None
        # Minimal plugin type - should exist
        assert protocol is object

    def test_target_plugin_protocol(self) -> None:
        """Test TargetPlugin protocol definition."""
        protocol = FlextMeltanoPluginTypes.TargetPlugin

        # Should be a class or type
        assert protocol is not None
        # Minimal plugin type - should exist
        assert protocol is object

    def test_dbt_plugin_protocol(self) -> None:
        """Test DbtPlugin protocol definition."""
        protocol = FlextMeltanoPluginTypes.DbtPlugin

        # Should be a class or type
        assert protocol is not None
        # Minimal plugin type - should exist
        assert protocol is object

    def test_service_protocol_aliases(self) -> None:
        """Test service protocol aliases exist."""
        # TapService should alias TapPlugin
        assert FlextMeltanoPluginTypes.TapService is FlextMeltanoPluginTypes.TapPlugin

        # TargetService should alias TargetPlugin
        assert (
            FlextMeltanoPluginTypes.TargetService
            is FlextMeltanoPluginTypes.TargetPlugin
        )

        # DbtService should alias DbtPlugin
        assert FlextMeltanoPluginTypes.DbtService is FlextMeltanoPluginTypes.DbtPlugin

    def test_backward_compatibility_aliases(self) -> None:
        """Test backward compatibility aliases exist."""
        # FlextTapPlugin should alias TapPlugin
        assert (
            FlextMeltanoPluginTypes.FlextTapPlugin is FlextMeltanoPluginTypes.TapPlugin
        )

        # FlextTargetPlugin should alias TargetPlugin
        assert (
            FlextMeltanoPluginTypes.FlextTargetPlugin
            is FlextMeltanoPluginTypes.TargetPlugin
        )

        # FlextDbtPlugin should alias DbtPlugin
        assert (
            FlextMeltanoPluginTypes.FlextDbtPlugin is FlextMeltanoPluginTypes.DbtPlugin
        )

    def test_nested_types_structure(self) -> None:
        """Test nested types structure exists."""
        # Should have proper class structure
        assert hasattr(FlextMeltanoPluginTypes, "__module__")
        assert FlextMeltanoPluginTypes.__module__ == "flext_meltano.plugin_protocols"

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
        assert FlextMeltanoPluginTypes is not None

        # Should have expected structure
        assert hasattr(FlextMeltanoPluginTypes, "__name__")

    def test_class_documentation(self) -> None:
        """Test class has proper documentation."""
        # Should have class docstring
        assert FlextMeltanoPluginTypes.__doc__ is not None

        # Should have module docstring
        assert protocols_module.__doc__ is not None


if __name__ == "__main__":
    unittest.main()
