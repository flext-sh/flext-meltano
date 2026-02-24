"""Constants for flext-meltano tests.

Provides TestsFlextMeltanoConstants, extending FlextTestsConstants with flext-meltano-specific
constants using COMPOSITION INHERITANCE.

Inheritance hierarchy:
- FlextTestsConstants (flext_tests) - Provides .Tests.* namespace
- FlextMeltanoConstants (production) - Provides .Meltano.* namespace

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_meltano.constants import FlextMeltanoConstants
from flext_tests.constants import FlextTestsConstants


class TestsFlextMeltanoConstants(FlextTestsConstants, FlextMeltanoConstants):
    """Constants for flext-meltano tests using COMPOSITION INHERITANCE.

    MANDATORY: Inherits from BOTH:
    1. FlextTestsConstants - for test infrastructure (.Tests.*)
    2. FlextMeltanoConstants - for domain constants (.Meltano.*)

    Access patterns:
    - c.Tests.Docker.* (container testing)
    - c.Tests.Matcher.* (assertion messages)
    - c.Tests.Factory.* (test data generation)
    - c.Meltano.* (domain constants from production)
    - c.Paths.* (project-specific test data)

    Rules:
    - NEVER duplicate constants from FlextTestsConstants or FlextMeltanoConstants
    - Only flext-meltano-specific test constants allowed (not generic for other projects)
    - All generic constants come from FlextTestsConstants
    - All production constants come from FlextMeltanoConstants
    """

    class Paths:
        """Test path constants."""

        TEST_INPUT_DIR: Final[str] = "tests/fixtures/data/input"
        TEST_OUTPUT_DIR: Final[str] = "tests/fixtures/data/output"
        TEST_TEMP_PREFIX: Final[str] = "flext_meltano_test_"


# Short aliases per FLEXT convention
c = TestsFlextMeltanoConstants  # Primary test constants alias
c = TestsFlextMeltanoConstants  # Alternative alias for compatibility

__all__ = [
    "TestsFlextMeltanoConstants",
    "c",
    "c",
]
