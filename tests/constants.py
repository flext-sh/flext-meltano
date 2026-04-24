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

from flext_tests import FlextTestsConstants

from flext_meltano import FlextMeltanoConstants


class TestsFlextMeltanoConstants(FlextTestsConstants, FlextMeltanoConstants):
    """Constants for flext-meltano tests using COMPOSITION INHERITANCE.

    MANDATORY: Inherits from FlextTestsConstants for test infrastructure (.Tests.*).
    Access project constants via inner class inheriting from FlextMeltanoConstants.Meltano.

    Access patterns:
    - c.Tests.* (container testing)
    - c.Tests.* (assertion messages)
    - c.Tests.Factory.* (test data generation)
    - c.Meltano.* (domain constants from production)
    - c.Paths.* (project-specific test data)

    Rules:
    - NEVER duplicate constants from FlextTestsConstants or FlextMeltanoConstants
    - Only flext-meltano-specific test constants allowed (not generic for other projects)
    - All generic constants come from FlextTestsConstants
    - All production constants come from FlextMeltanoConstants
    """

    class Meltano(FlextMeltanoConstants.Meltano):
        """Meltano domain namespace."""

        class Tests(FlextTestsConstants.Tests):
            """Meltano tests namespace."""

            HOST: Final[str] = "localhost"
            POSTGRES_PORT: Final[int] = 5433
            REDIS_PORT: Final[int] = 6380
            MELTANO_PORT: Final[int] = 3389
            COMPOSE_FILE: Final[str] = "docker-compose.test.yml"
            TEST_INPUT_DIR: Final[str] = "tests/fixtures/data/input"
            TEST_OUTPUT_DIR: Final[str] = "tests/fixtures/data/output"
            TEST_TEMP_PREFIX: Final[str] = "flext_meltano_test_"


c = TestsFlextMeltanoConstants
__all__: list[str] = ["TestsFlextMeltanoConstants", "c"]
