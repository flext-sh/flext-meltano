"""Test models for flext-meltano.

Provides test-specific models extending FlextTestsModels and FlextMeltanoModels
with proper hierarchy composition.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import m

from flext_meltano import FlextMeltanoModels


class TestsFlextMeltanoModels(FlextTestsModels, FlextMeltanoModels):
    """Test models - composition of FlextTestsModels + FlextMeltanoModels.

    Hierarchy:
    - FlextTestsModels: Generic test utilities from flext-tests
    - FlextMeltanoModels: Domain models from flext-meltano
    - TestsFlextMeltanoModels: Composition + namespace .Tests

    Access patterns:
    - m.Tests.* - Project-specific test fixtures
    - m.Meltano.* - Production domain models (inherited)
    - FlextTestsModels.Tests.* - Generic test utilities
    """

    class Meltano(FlextMeltanoModels.Meltano):
        """Meltano domain models test namespace."""

        class Tests:
            """Test fixtures namespace for flext-meltano.

            Contains test-specific models and fixtures that should not
            be part of production code.
            """


m = TestsFlextMeltanoModels

__all__ = ["TestsFlextMeltanoModels", "m"]
