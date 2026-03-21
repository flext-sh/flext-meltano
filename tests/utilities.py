"""Module skeleton for TestsFlextMeltanoUtilities.

Test utilities for flextmeltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import u as _base_u
from flext_tests._utilities.matchers import FlextTestsMatchersUtilities

from flext_meltano.utilities import FlextMeltanoUtilities


class TestsFlextMeltanoUtilities(FlextMeltanoUtilities):
    """Test utilities for flextmeltano."""

    class Tests(FlextTestsMatchersUtilities.Tests, _base_u.Tests):
        """Merged Tests namespace with Matchers from FlextTestsMatchersUtilities."""


u = TestsFlextMeltanoUtilities
__all__ = ["TestsFlextMeltanoUtilities", "u"]
