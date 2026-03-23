"""Test module for flext-meltano plugin type definitions.

Tests the canonical t.Meltano.PluginDefinition and t.Meltano.PluginConfiguration
types from FlextMeltanoTypes following FLEXT standards.
NO ALIASES, NO BACKWARD COMPATIBILITY - Direct canonical API testing only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import unittest
from unittest import TestCase

from flext_tests import tm

from flext_meltano import FlextMeltanoTypes

t = FlextMeltanoTypes


class TestFlextMeltanoPluginProtocolsUnified(TestCase):
    """Test canonical Meltano plugin type definitions via t.Meltano namespace."""

    def test_plugin_definition_type_exists(self) -> None:
        """Test t.Meltano.PluginDefinition type alias exists."""
        tm.that(hasattr(t.Meltano, "PluginDefinition"), eq=True)

    def test_plugin_configuration_type_exists(self) -> None:
        """Test t.Meltano.PluginConfiguration type alias exists."""
        tm.that(hasattr(t.Meltano, "PluginConfiguration"), eq=True)

    def test_plugin_catalog_type_exists(self) -> None:
        """Test t.Meltano.PluginCatalog type alias exists."""
        tm.that(hasattr(t.Meltano, "PluginCatalog"), eq=True)

    def test_plugin_definition_is_type_alias(self) -> None:
        """Test PluginDefinition is accessible as type alias."""
        plugin_def = t.Meltano.PluginDefinition
        tm.that(plugin_def is not None, eq=True)

    def test_plugin_configuration_is_type_alias(self) -> None:
        """Test PluginConfiguration is accessible as type alias."""
        plugin_cfg = t.Meltano.PluginConfiguration
        tm.that(plugin_cfg is not None, eq=True)

    def test_meltano_namespace_exists(self) -> None:
        """Test FlextMeltanoTypes.Meltano namespace exists."""
        tm.that(hasattr(FlextMeltanoTypes, "Meltano"), eq=True)

    def test_typings_module_has_documentation(self) -> None:
        """Test FlextMeltanoTypes class has documentation."""
        tm.that(FlextMeltanoTypes.__doc__ is not None, eq=True)


if __name__ == "__main__":
    unittest.main()
