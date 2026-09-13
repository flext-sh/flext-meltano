"""Test type aliases for flext-meltano.

Provides TestsFlextMeltanoTypes, combining TestsFlextTypes with
t for test-specific type aliases.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_meltano import t


class TestsFlextMeltanoTypes(FlextTestsTypes, t):
    """Test type aliases for flext-meltano."""

    class Meltano(t.Meltano):
        """Meltano test types namespace."""

        class Tests(FlextTestsTypes.Tests):
            """Meltano-specific test type aliases."""


t = TestsFlextMeltanoTypes
__all__: list[str] = ["TestsFlextMeltanoTypes", "t"]
