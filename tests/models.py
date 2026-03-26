"""Test models for flext-meltano.

Provides test-specific models extending FlextTestsModels and FlextMeltanoModels
with proper hierarchy composition.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_infra import FlextInfraModels
from flext_tests import FlextTestsModels

from flext_meltano import FlextMeltanoModels


class FlextMeltanoTestModels(FlextTestsModels, FlextInfraModels, FlextMeltanoModels):
    """Test models - composition of FlextTestsModels + FlextMeltanoModels.

    Hierarchy:
    - FlextTestsModels: Generic test utilities from flext-tests
    - FlextMeltanoModels: Domain models from flext-meltano
    - FlextMeltanoTestModels: Composition + namespace .Tests

    Access patterns:
    - m.Tests.* - Project-specific test fixtures
    - m.Meltano.* - Production domain models (inherited)
    """

    class Meltano(FlextMeltanoModels.Meltano):
        """Meltano domain models test namespace."""

        class Tests:
            """Test fixtures namespace for flext-meltano.

            Contains test-specific models and fixtures that should not
            be part of production code.
            """


m = FlextMeltanoTestModels

__all__ = ["FlextMeltanoTestModels", "m"]
