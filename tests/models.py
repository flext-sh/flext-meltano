"""Test models for flext-meltano.

Provides test-specific models extending TestsFlextModels and FlextMeltanoModels
with proper hierarchy composition.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_infra import FlextInfraModels
from flext_tests import FlextTestsModels

from flext_meltano import FlextMeltanoModels


class TestsFlextMeltanoModels(FlextTestsModels, FlextInfraModels, FlextMeltanoModels):
    """Test models - composition of TestsFlextModels + FlextMeltanoModels.

    Hierarchy:
    - TestsFlextModels: Generic test utilities from flext-tests
    - FlextMeltanoModels: Domain models from flext-meltano
    - TestsFlextMeltanoModels: Composition + namespace .Tests

    Access patterns:
    - m.Tests.* - Project-specific test fixtures
    - m.Meltano.* - Production domain models (inherited)
    """

    class Meltano(FlextMeltanoModels.Meltano):
        """Meltano domain models test namespace."""

        class Tests(FlextTestsModels.Tests):
            """Test fixtures namespace for flext-meltano.

            Contains test-specific models and fixtures that should not
            be part of production code.
            """


m = TestsFlextMeltanoModels

__all__: list[str] = ["TestsFlextMeltanoModels", "m"]
