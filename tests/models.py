"""Test models for flext-meltano.

Provides test-specific models extending TestsFlextModels and m
with proper hierarchy composition.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from flext_meltano import m


class TestsFlextMeltanoModels(FlextTestsModels, m):
    """Test models - composition of TestsFlextModels + m.

    Hierarchy:
    - TestsFlextModels: Generic test utilities from flext-tests
    - m: Domain models from flext-meltano
    - TestsFlextMeltanoModels: Composition + namespace .Tests

    Access patterns:
    - m.Tests.* - Project-specific test fixtures
    - m.Meltano.* - Production domain models (inherited)
    """

    class Meltano(m.Meltano):
        """Meltano domain models test namespace."""

        class Tests(FlextTestsModels.Tests):
            """Test fixtures namespace for flext-meltano.

            Contains test-specific models and fixtures that should not
            be part of production code.
            """


m = TestsFlextMeltanoModels

__all__: list[str] = ["TestsFlextMeltanoModels", "m"]
