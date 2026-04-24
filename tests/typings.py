"""Test type aliases for flext-meltano.

Provides TestsFlextMeltanoTypes, combining TestsFlextTypes with
FlextMeltanoTypes for test-specific type aliases.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_meltano import FlextMeltanoTypes


class TestsFlextMeltanoTypes(FlextTestsTypes, FlextMeltanoTypes):
    """Test type aliases for flext-meltano."""


t = TestsFlextMeltanoTypes
__all__: list[str] = ["TestsFlextMeltanoTypes", "t"]
