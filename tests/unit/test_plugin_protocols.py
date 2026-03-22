"""Test module for flext-meltano plugin protocols - UNIFIED patterns only.

Tests the FlextMeltanoPluginProtocols unified class following FLEXT standards.
NO ALIASES, NO BACKWARD COMPATIBILITY - Direct API testing only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import unittest
from unittest import TestCase

from flext_tests import tm

import flext_meltano.singer.protocols as protocols_module
from flext_meltano.singer.protocols import FlextMeltanoPluginProtocols


class TestFlextMeltanoPluginProtocolsUnified(TestCase):
    """Test FlextMeltanoPluginProtocols unified class - NO ALIASES."""

    def test_unified_class_exists(self) -> None:
        """Test FlextMeltanoPluginProtocols unified class exists."""
        tm.that(hasattr(FlextMeltanoPluginProtocols, "__name__"), eq=True)
        tm.that(FlextMeltanoPluginProtocols.__name__, eq="FlextMeltanoPluginProtocols")

    def test_unified_class_has_core_plugin_types(self) -> None:
        """Test FlextMeltanoPluginProtocols has core plugin type definitions."""
        expected_core_types = ["TapPlugin", "TargetPlugin", "DbtPlugin"]
        for plugin_type in expected_core_types:
            tm.that(hasattr(FlextMeltanoPluginProtocols, plugin_type), eq=True)

    def test_unified_class_has_service_protocols(self) -> None:
        """Test FlextMeltanoPluginProtocols has service protocol definitions."""
        expected_service_protocols = [
            "TapService",
            "TargetService",
            "DbtService",
        ]
        for service_protocol in expected_service_protocols:
            tm.that(hasattr(FlextMeltanoPluginProtocols, service_protocol), eq=True)

    def test_tap_plugin_protocol_definition(self) -> None:
        """Test TapPlugin protocol definition is valid."""
        protocol = FlextMeltanoPluginProtocols.TapPlugin
        tm.that(protocol is not None, eq=True)

    def test_target_plugin_protocol_definition(self) -> None:
        """Test TargetPlugin protocol definition is valid."""
        protocol = FlextMeltanoPluginProtocols.TargetPlugin
        tm.that(protocol is not None, eq=True)

    def test_dbt_plugin_protocol_definition(self) -> None:
        """Test DbtPlugin protocol definition is valid."""
        protocol = FlextMeltanoPluginProtocols.DbtPlugin
        tm.that(protocol is not None, eq=True)

    def test_tap_service_protocol_definition(self) -> None:
        """Test TapService definition is valid."""
        protocol = FlextMeltanoPluginProtocols.TapService
        tm.that(protocol is not None, eq=True)

    def test_target_service_protocol_definition(self) -> None:
        """Test TargetService definition is valid."""
        protocol = FlextMeltanoPluginProtocols.TargetService
        tm.that(protocol is not None, eq=True)

    def test_dbt_service_protocol_definition(self) -> None:
        """Test DbtService definition is valid."""
        protocol = FlextMeltanoPluginProtocols.DbtService
        tm.that(protocol is not None, eq=True)

    def test_no_aliases_exist(self) -> None:
        """Test that NO aliases exist - direct API access only."""
        no_alias_attributes = [
            "FlextMeltanoTapPlugin",
            "FlextTargetPlugin",
            "FlextDbtPlugin",
        ]
        for alias in no_alias_attributes:
            tm.that(not hasattr(FlextMeltanoPluginProtocols, alias), eq=True)

    def test_unified_class_structure(self) -> None:
        """Test unified class has proper structure."""
        tm.that(hasattr(FlextMeltanoPluginProtocols, "__module__"), eq=True)
        tm.that(
            (
                FlextMeltanoPluginProtocols.__module__
                == "flext_meltano.singer.protocols"
            ),
            eq=True,
        )

    def test_direct_api_access_only(self) -> None:
        """Test that only direct API access works - NO module-level aliases."""
        tm.that(FlextMeltanoPluginProtocols is not None, eq=True)
        tm.that(hasattr(FlextMeltanoPluginProtocols, "__name__"), eq=True)

    def test_class_documentation_exists(self) -> None:
        """Test unified class has proper documentation."""
        tm.that(FlextMeltanoPluginProtocols.__doc__ is not None, eq=True)
        tm.that(protocols_module.__doc__ is not None, eq=True)

    def test_module_exports_only_unified_class(self) -> None:
        """Test module exports only the unified class - NO ALIASES."""
        all_exports = getattr(protocols_module, "__all__", [])
        tm.that("FlextMeltanoPluginProtocols" in all_exports, eq=True)
        forbidden_exports = [
            "FlextMeltanoTapPlugin",
            "FlextTargetPlugin",
            "FlextDbtPlugin",
            "TapService",
            "TargetService",
            "TapService",
            "TargetService",
            "DbtService",
        ]
        for forbidden in forbidden_exports:
            tm.that(forbidden not in all_exports, eq=True)


if __name__ == "__main__":
    unittest.main()
