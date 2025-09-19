"""Test configuration builders for flext-meltano."""

from __future__ import annotations

import unittest

from flext_meltano.config_builders import FlextMeltanoConfigBuilders

"""FLEXT Meltano Config Builders Tests - Enterprise ELT configuration testing.

This module provides tests for FlextMeltanoConfigBuilders following
FLEXT patterns with comprehensive configuration validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


class TestFlextMeltanoConfigBuildersBasic(unittest.TestCase):
    """Basic functionality tests for FlextMeltanoConfigBuilders."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.builders = FlextMeltanoConfigBuilders()

    def test_class_instantiation(self) -> None:
        """Test FlextMeltanoConfigBuilders instantiation."""
        builders = FlextMeltanoConfigBuilders()
        assert isinstance(builders, FlextMeltanoConfigBuilders)

    def test_unified_builder_has_dbt_functionality(self) -> None:
        """Test unified builder has DBT functionality (SOLID refactored)."""
        builder = FlextMeltanoConfigBuilders()
        assert hasattr(builder, "create_dbt_config")
        assert callable(builder.create_dbt_config)

    def test_unified_builder_has_singer_functionality(self) -> None:
        """Test unified builder has Singer functionality (SOLID refactored)."""
        builder = FlextMeltanoConfigBuilders()
        assert hasattr(builder, "create_singer_tap_config")
        assert hasattr(builder, "create_singer_target_config")
        assert callable(builder.create_singer_tap_config)

    def test_unified_builder_has_meltano_functionality(self) -> None:
        """Test unified builder has Meltano functionality (SOLID refactored)."""
        builder = FlextMeltanoConfigBuilders()
        assert hasattr(builder, "create_meltano_config")
        assert hasattr(builder, "add_plugin_to_config")
        assert callable(builder.create_meltano_config)

    def test_dbt_config_builder_has_build_method(self) -> None:
        """Test unified builder has DBT functionality."""
        builder = FlextMeltanoConfigBuilders()
        assert hasattr(builder, "create_dbt_config")

    def test_singer_config_builder_has_build_method(self) -> None:
        """Test unified builder has Singer functionality."""
        builder = FlextMeltanoConfigBuilders()
        assert hasattr(builder, "create_singer_tap_config")

    def test_meltano_config_builder_has_build_method(self) -> None:
        """Test unified builder has Meltano functionality."""
        builder = FlextMeltanoConfigBuilders()
        assert hasattr(builder, "create_meltano_config")

    def test_all_exports_available(self) -> None:
        """Test all expected exports are available (updated for unified architecture)."""
        # Main class should be importable
        assert FlextMeltanoConfigBuilders is not None

        # Create instance and verify all unified methods are available
        builder = FlextMeltanoConfigBuilders()

        # DBT configuration methods
        assert hasattr(builder, "create_dbt_config")

        # Singer configuration methods
        assert hasattr(builder, "create_singer_tap_config")
        assert hasattr(builder, "create_singer_target_config")

        # Plugin configuration methods
        assert hasattr(builder, "create_plugin_config")
        assert hasattr(builder, "create_extractor_config")
        assert hasattr(builder, "create_loader_config")

        # Meltano configuration methods
        assert hasattr(builder, "create_meltano_config")
        assert hasattr(builder, "add_plugin_to_config")


if __name__ == "__main__":
    unittest.main()
