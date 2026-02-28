"""FLEXT Meltano Singer Types Tests - Real functionality testing.

This module provides tests for t using real functionality
without mocks or patches.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_meltano import t


class TestFlextSingerTypes:
    """Test suite for t with real functionality."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.singer_types = t()

    def test_singer_types_initialization(self) -> None:
        """Test t initialization."""
        singer_types = t()

        assert singer_types is not None
        assert hasattr(singer_types, "Meltano")
        assert hasattr(singer_types, "Plugin")

    def test_singer_types_basic_functionality(self) -> None:
        """Test basic singer types functionality."""
        # Test that t can be instantiated
        singer_types = t()

        assert singer_types is not None
        assert hasattr(singer_types, "Meltano")
        assert hasattr(singer_types, "Plugin")
