"""Test module for flext-meltano plugin protocols - UNIFIED patterns only.

Tests the FlextMeltanoPluginProtocols unified class following FLEXT standards.
NO ALIASES, NO BACKWARD COMPATIBILITY - Direct API testing only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import unittest
from unittest import TestCase

import flext_meltano.plugin_protocols as protocols_module
from flext_core import FlextTypes
from flext_meltano import FlextMeltanoPluginProtocols


class TestFlextMeltanoPluginProtocolsUnified(TestCase):
    """Test FlextMeltanoPluginProtocols unified class - NO ALIASES."""

    def test_unified_class_exists(self) -> None:
        """Test FlextMeltanoPluginProtocols unified class exists."""
        assert hasattr(FlextMeltanoPluginProtocols, "__name__")
        assert FlextMeltanoPluginProtocols.__name__ == "FlextMeltanoPluginProtocols"

    def test_unified_class_has_core_plugin_types(self) -> None:
        """Test FlextMeltanoPluginProtocols has core plugin type definitions."""
        expected_core_types = [
            "TapPlugin",
            "TargetPlugin",
            "DbtPlugin",
        ]

        for plugin_type in expected_core_types:
            assert hasattr(FlextMeltanoPluginProtocols, plugin_type), (
                f"FlextMeltanoPluginProtocols missing core type: {plugin_type}"
            )

    def test_unified_class_has_service_protocols(self) -> None:
        """Test FlextMeltanoPluginProtocols has service protocol definitions."""
        expected_service_protocols = [
            "TapServiceProtocol",
            "TargetServiceProtocol",
            "DbtServiceProtocol",
        ]

        for service_protocol in expected_service_protocols:
            assert hasattr(FlextMeltanoPluginProtocols, service_protocol), (
                f"FlextMeltanoPluginProtocols missing service protocol: {service_protocol}"
            )

    def test_tap_plugin_protocol_definition(self) -> None:
        protocol = FlextMeltanoPluginProtocols.TapPlugin
        assert protocol is not None
        assert protocol == FlextTypes.JsonValue  # Placeholder implementation

    def test_target_plugin_protocol_definition(self) -> None:
        """Test TargetPlugin protocol definition is valid."""
        protocol = FlextMeltanoPluginProtocols.TargetPlugin
        assert protocol is not None
        # TargetPlugin is a type alias for JsonObject, not object itself
        assert protocol == FlextTypes.JsonValue  # Placeholder implementation

    def test_dbt_plugin_protocol_definition(self) -> None:
        protocol = FlextMeltanoPluginProtocols.DbtPlugin
        assert protocol is not None
        assert protocol == FlextTypes.JsonValue  # Placeholder implementation

    def test_tap_service_protocol_definition(self) -> None:
        protocol = FlextMeltanoPluginProtocols.TapServiceProtocol
        assert protocol is not None
        assert protocol == FlextTypes.JsonValue  # Placeholder implementation

    def test_target_service_protocol_definition(self) -> None:
        """Test TargetServiceProtocol definition is valid."""
        protocol = FlextMeltanoPluginProtocols.TargetServiceProtocol
        assert protocol is not None
        # TargetServiceProtocol is a type alias for JsonObject, not object itself
        assert protocol == FlextTypes.JsonValue  # Placeholder implementation

    def test_dbt_service_protocol_definition(self) -> None:
        protocol = FlextMeltanoPluginProtocols.DbtServiceProtocol
        assert protocol is not None
        assert protocol == FlextTypes.JsonValue  # Placeholder implementation

    def test_no_aliases_exist(self) -> None:
        """Test that NO aliases exist - direct API access only."""
        # Verify the class does NOT have backward compatibility aliases
        no_alias_attributes = [
            "FlextTapPlugin",
            "FlextTargetPlugin",
            "FlextDbtPlugin",
            "TapService",
            "TargetService",
            "DbtService",
        ]

        for alias in no_alias_attributes:
            assert not hasattr(FlextMeltanoPluginProtocols, alias), (
                f"VIOLATION: Found eliminated alias {alias} - should not exist"
            )

    def test_unified_class_structure(self) -> None:
        """Test unified class has proper structure."""
        assert hasattr(FlextMeltanoPluginProtocols, "__module__")
        assert (
            FlextMeltanoPluginProtocols.__module__ == "flext_meltano.plugin_protocols"
        )

    def test_direct_api_access_only(self) -> None:
        """Test that only direct API access works - NO module-level aliases."""
        # Should be importable directly
        assert FlextMeltanoPluginProtocols is not None

        # Should have expected unified structure
        assert hasattr(FlextMeltanoPluginProtocols, "__name__")

    def test_class_documentation_exists(self) -> None:
        """Test unified class has proper documentation."""
        # Should have class docstring
        assert FlextMeltanoPluginProtocols.__doc__ is not None

        # Should have module docstring
        assert protocols_module.__doc__ is not None

    def test_module_exports_only_unified_class(self) -> None:
        """Test module exports only the unified class - NO ALIASES."""
        # Check __all__ exports only the unified class
        all_exports = getattr(protocols_module, "__all__", [])
        assert "FlextMeltanoPluginProtocols" in all_exports

        # Should NOT export any aliases
        forbidden_exports = [
            "FlextTapPlugin",
            "FlextTargetPlugin",
            "FlextDbtPlugin",
            "TapService",
            "TargetService",
            "TapServiceProtocol",
            "TargetServiceProtocol",
            "DbtServiceProtocol",
        ]

        for forbidden in forbidden_exports:
            assert forbidden not in all_exports, (
                f"VIOLATION: Found forbidden alias export: {forbidden}"
            )


if __name__ == "__main__":
    unittest.main()
