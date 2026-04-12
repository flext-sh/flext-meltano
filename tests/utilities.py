"""Test utilities for flext-meltano.

Provides TestsFlextMeltanoUtilities using the shared test utility stack.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities


class TestsFlextMeltanoUtilities(FlextTestsUtilities):
    """Test utilities for flext-meltano."""

    class Meltano:
        """Meltano-specific utilities."""

        class Tests:
            """Meltano test utilities."""


u = TestsFlextMeltanoUtilities
__all__: list[str] = ["TestsFlextMeltanoUtilities", "u"]
