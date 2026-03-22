"""Test utilities for flext-meltano.

Provides FlextMeltanoTestUtilities, combining FlextTestsUtilities with
FlextMeltanoUtilities for test-specific utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from flext_meltano import FlextMeltanoUtilities


class FlextMeltanoTestUtilities(FlextTestsUtilities, FlextMeltanoUtilities):
    """Test utilities for flext-meltano."""

    class Meltano(FlextMeltanoUtilities.Meltano):
        """Meltano-specific utilities."""

        class Tests:
            """Meltano test utilities."""


u = FlextMeltanoTestUtilities
__all__ = ["FlextMeltanoTestUtilities", "u"]
