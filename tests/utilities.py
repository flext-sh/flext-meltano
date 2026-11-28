"""Test utilities for flext-meltano.

Provides TestsFlextMeltanoUtilities using the shared test utility stack.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from tests import FlextMeltanoUtilities


class TestsFlextMeltanoUtilities(FlextTestsUtilities, FlextMeltanoUtilities):
    """Test utilities for flext-meltano."""

    class Tests(FlextTestsUtilities.Tests):
        """Meltano test utilities."""


u = TestsFlextMeltanoUtilities
__all__: list[str] = ["TestsFlextMeltanoUtilities", "u"]
