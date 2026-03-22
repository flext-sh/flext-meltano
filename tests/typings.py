"""Test type aliases for flext-meltano.

Provides FlextMeltanoTestTypes, combining FlextTestsTypes with
FlextMeltanoTypes for test-specific type aliases.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_meltano import FlextMeltanoTypes


class FlextMeltanoTestTypes(FlextTestsTypes, FlextMeltanoTypes):
    """Test type aliases for flext-meltano."""

    class Meltano(FlextMeltanoTypes.Meltano):
        """Meltano-specific type aliases."""

        class Tests:
            """Meltano test type aliases."""


t = FlextMeltanoTestTypes
__all__ = ["FlextMeltanoTestTypes", "t"]
