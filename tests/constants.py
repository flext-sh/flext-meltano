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

from collections.abc import Mapping
from enum import StrEnum, unique
from pathlib import Path
from types import MappingProxyType
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

            @unique
            class _DockerService(StrEnum):
                """Docker service identifiers used by the local test stack."""

                POSTGRES = "postgres"
                REDIS = "redis"
                MELTANO = "meltano"

            HOST: Final[str] = FlextMeltanoConstants.LOCALHOST
            SERVICE_PORTS: Final[Mapping[_DockerService, int]] = MappingProxyType({
                _DockerService.POSTGRES: 5433,
                _DockerService.REDIS: 6380,
                _DockerService.MELTANO: 3389,
            })
            POSTGRES_PORT: Final[int] = SERVICE_PORTS[_DockerService.POSTGRES]
            REDIS_PORT: Final[int] = SERVICE_PORTS[_DockerService.REDIS]
            MELTANO_PORT: Final[int] = SERVICE_PORTS[_DockerService.MELTANO]
            COMPOSE_FILE: Final[str] = "docker-compose.test.yml"
            FIXTURES_DATA_DIR: Final[Path] = Path("tests/fixtures/data")
            TEST_INPUT_DIR: Final[str] = (FIXTURES_DATA_DIR / "input").as_posix()
            TEST_OUTPUT_DIR: Final[str] = (FIXTURES_DATA_DIR / "output").as_posix()
            TEST_TEMP_PREFIX: Final[str] = "flext_meltano_test_"


c = TestsFlextMeltanoConstants
__all__: list[str] = ["TestsFlextMeltanoConstants", "c"]
