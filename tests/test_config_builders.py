"""Test config_builders module - Basic functionality tests.

Tests FlextMeltanoConfigBuilders class and nested builder classes.
Zero mock usage - all real function testing.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import unittest

from flext_meltano.config_builders import FlextMeltanoConfigBuilders


class TestFlextMeltanoConfigBuildersBasic(unittest.TestCase):
    """Basic functionality tests for FlextMeltanoConfigBuilders."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.builders = FlextMeltanoConfigBuilders()

    def test_class_instantiation(self) -> None:
        """Test FlextMeltanoConfigBuilders instantiation."""
        builders = FlextMeltanoConfigBuilders()
        assert isinstance(builders, FlextMeltanoConfigBuilders)

    def test_nested_dbt_builder_exists(self) -> None:
        """Test DbtConfigBuilder nested class exists."""
        assert hasattr(FlextMeltanoConfigBuilders, "DbtConfigBuilder")
        builder = FlextMeltanoConfigBuilders.DbtConfigBuilder()
        assert isinstance(builder, FlextMeltanoConfigBuilders.DbtConfigBuilder)

    def test_nested_singer_builder_exists(self) -> None:
        """Test SingerConfigBuilder nested class exists."""
        assert hasattr(FlextMeltanoConfigBuilders, "SingerConfigBuilder")
        builder = FlextMeltanoConfigBuilders.SingerConfigBuilder()
        assert isinstance(builder, FlextMeltanoConfigBuilders.SingerConfigBuilder)

    def test_nested_meltano_builder_exists(self) -> None:
        """Test MeltanoConfigBuilder nested class exists."""
        assert hasattr(FlextMeltanoConfigBuilders, "MeltanoConfigBuilder")
        builder = FlextMeltanoConfigBuilders.MeltanoConfigBuilder()
        assert isinstance(builder, FlextMeltanoConfigBuilders.MeltanoConfigBuilder)

    def test_dbt_config_builder_has_build_method(self) -> None:
        """Test DbtConfigBuilder has build functionality."""
        builder = FlextMeltanoConfigBuilders.DbtConfigBuilder()
        assert hasattr(builder, "create_dbt_config")

    def test_singer_config_builder_has_build_method(self) -> None:
        """Test SingerConfigBuilder has build functionality."""
        builder = FlextMeltanoConfigBuilders.SingerConfigBuilder()
        assert hasattr(builder, "create_singer_tap_config")

    def test_meltano_config_builder_has_build_method(self) -> None:
        """Test MeltanoConfigBuilder has build functionality."""
        builder = FlextMeltanoConfigBuilders.MeltanoConfigBuilder()
        assert hasattr(builder, "create_meltano_config")

    def test_all_exports_available(self) -> None:
        """Test all expected exports are available."""
        # Main class should be importable
        assert FlextMeltanoConfigBuilders is not None

        # Should be able to access nested classes
        assert hasattr(FlextMeltanoConfigBuilders, "DbtConfigBuilder")
        assert hasattr(FlextMeltanoConfigBuilders, "SingerConfigBuilder")
        assert hasattr(FlextMeltanoConfigBuilders, "MeltanoConfigBuilder")


if __name__ == "__main__":
    unittest.main()
