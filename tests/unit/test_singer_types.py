"""FLEXT Meltano Singer Types Tests - Real functionality testing.

This module provides tests for FlextMeltanoTypes using real functionality
without mocks or patches.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_meltano import FlextMeltanoTypes


class TestFlextSingerTypes:
    """Test suite for FlextMeltanoTypes with real functionality."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.singer_types = FlextMeltanoTypes()

    def test_singer_types_initialization(self) -> None:
        """Test FlextMeltanoTypes initialization."""
        singer_types = FlextMeltanoTypes()

        assert singer_types is not None
        assert hasattr(singer_types, "MeltanoCore")
        assert hasattr(singer_types, "Plugin")

    def test_singer_types_basic_functionality(self) -> None:
        """Test basic singer types functionality."""
        # Test that FlextMeltanoTypes can be instantiated
        singer_types = FlextMeltanoTypes()

        assert singer_types is not None
        assert hasattr(singer_types, "MeltanoCore")
        assert hasattr(singer_types, "Plugin")
