"""FLEXT Meltano Singer Types Tests - Real functionality testing.

This module provides tests for t using real functionality
without mocks or patches.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from flext_meltano import t


class TestFlextSingerTypes:
    """Test suite for t with real functionality."""

    singer_types: t.NormalizedValue

    def setup_method(self) -> None:
        """Setup for each test."""
        self.singer_types = t()

    def test_singer_types_initialization(self) -> None:
        """Test t initialization."""
        singer_types = t()
        tm.that(singer_types is not None, eq=True)
        tm.that(hasattr(singer_types, "Meltano"), eq=True)
        tm.that(hasattr(singer_types.Meltano, "PluginDefinition"), eq=True)

    def test_singer_types_basic_functionality(self) -> None:
        """Test basic singer types functionality."""
        singer_types = t()
        tm.that(singer_types is not None, eq=True)
        tm.that(hasattr(singer_types, "Meltano"), eq=True)
        tm.that(hasattr(singer_types.Meltano, "PluginDefinition"), eq=True)
