"""Test constants extending flext_meltano.constants for test-specific constants.

This module provides test-specific constants that extend the production
constants from src/flext_meltano/constants.py. All test constants use real
inheritance to expose the full hierarchy and avoid duplication.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_meltano.constants import FlextMeltanoConstants


class TestsConstants(FlextMeltanoConstants):
    """Test-specific constants extending FlextMeltanoConstants.

    Provides test-specific constants without duplicating parent functionality.
    All parent constants are accessible via inheritance hierarchy.
    """

    class Paths:
        """Test path constants."""

        TEST_INPUT_DIR: Final[str] = "tests/fixtures/data/input"
        TEST_OUTPUT_DIR: Final[str] = "tests/fixtures/data/output"
        TEST_TEMP_PREFIX: Final[str] = "flext_meltano_test_"


# Standardized short name for use in tests (same pattern as flext-core)
c = TestsConstants

__all__ = ["TestsConstants", "c"]
