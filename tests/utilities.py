"""Test utilities for flext-meltano.

Provides TestsFlextMeltanoUtilities using the shared test utility stack.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from flext_meltano import FlextMeltanoUtilities


class TestsFlextMeltanoUtilities(FlextTestsUtilities, FlextMeltanoUtilities):
    """Test utilities for flext-meltano."""

    class Meltano(FlextMeltanoUtilities.Meltano):
        """Meltano-specific utilities."""

        class Tests(FlextTestsUtilities.Tests):
            """Meltano test utilities."""


u = TestsFlextMeltanoUtilities
__all__: list[str] = ["TestsFlextMeltanoUtilities", "u"]
