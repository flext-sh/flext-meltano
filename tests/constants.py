"""Constants for flext-meltano tests.

Provides TestsFlextMeltanoConstants, extending FlextTestsConstants with flext-meltano-specific
constants using COMPOSITION INHERITANCE.

Inheritance hierarchy:
- FlextTestsConstants (flext_tests) - Provides .Tests.* namespace
- c (production) - Provides .Meltano.* namespace

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum, unique
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Final

from flext_meltano import c
from flext_tests import FlextTestsConstants

if TYPE_CHECKING:
    from tests import t


class TestsFlextMeltanoConstants(FlextTestsConstants, c):
    """Constants for flext-meltano tests using COMPOSITION INHERITANCE.

    MANDATORY: Inherits from FlextTestsConstants for test infrastructure (.Tests.*).
    Access project constants via inner class inheriting from c.Meltano.

    Access patterns:
    - c.Tests.* (container testing)
    - c.Tests.* (assertion messages)
    - c.Tests.Factory.* (test data generation)
    - c.Meltano.* (domain constants from production)
    - c.Paths.* (project-specific test data)

    Rules:
    - NEVER duplicate constants from FlextTestsConstants or c
    - Only flext-meltano-specific test constants allowed (not generic for other projects)
    - All generic constants come from FlextTestsConstants
    - All production constants come from c
    """

    class Meltano(c.Meltano):
        """Meltano domain namespace."""

        class Tests(FlextTestsConstants.Tests):
            """Meltano tests namespace."""

            @unique
            class _DockerService(StrEnum):
                """Docker service identifiers used by the local test stack."""

                POSTGRES = "postgres"
                REDIS = "redis"
                MELTANO = "meltano"

            HOST: Final[str] = c.LOCALHOST
            SERVICE_PORTS: Final[t.MappingKV[_DockerService, int]] = MappingProxyType({
                _DockerService.POSTGRES: 5433,
                _DockerService.REDIS: 6380,
                _DockerService.MELTANO: 3000,
            })
            POSTGRES_PORT: Final[int] = SERVICE_PORTS[_DockerService.POSTGRES]
            REDIS_PORT: Final[int] = SERVICE_PORTS[_DockerService.REDIS]
            MELTANO_PORT: Final[int] = SERVICE_PORTS[_DockerService.MELTANO]
            COMPOSE_FILE: Final[str] = "docker-compose.test.yml"
            PRIMARY_SERVICE: Final[str] = _DockerService.MELTANO
            PRIMARY_CONTAINER_NAME: Final[str] = "flext-test-meltano"
            FIXTURES_DATA_DIR: Final[Path] = Path("tests/fixtures/data")
            TEST_INPUT_DIR: Final[str] = (FIXTURES_DATA_DIR / "input").as_posix()
            TEST_OUTPUT_DIR: Final[str] = (FIXTURES_DATA_DIR / "output").as_posix()
            TEST_TEMP_PREFIX: Final[str] = "flext_meltano_test_"

            @unique
            class _SingerSdkAdapterValue(StrEnum):
                """Deterministic values for Singer SDK adapter tests."""

                SETTINGS_KEY = "tap"
                SETTINGS_VALUE = "ok"
                STREAM_USERS = "users"
                SUCCESS_COMMAND = "tap-ok"
                FAILURE_COMMAND = "tap-fail"

            SINGER_SDK_ADAPTER_SETTINGS: Final[t.MappingKV[str, str]] = (
                MappingProxyType({
                    _SingerSdkAdapterValue.SETTINGS_KEY: (
                        _SingerSdkAdapterValue.SETTINGS_VALUE
                    )
                })
            )
            SINGER_SDK_ADAPTER_STREAM_USERS: Final[str] = (
                _SingerSdkAdapterValue.STREAM_USERS
            )
            SINGER_SDK_ADAPTER_SUCCESS_COMMAND: Final[str] = (
                _SingerSdkAdapterValue.SUCCESS_COMMAND
            )
            SINGER_SDK_ADAPTER_FAILURE_COMMAND: Final[str] = (
                _SingerSdkAdapterValue.FAILURE_COMMAND
            )
            SINGER_SDK_ADAPTER_FAILURE_EXIT_CODE: Final[int] = 3


c = TestsFlextMeltanoConstants
__all__: list[str] = ["TestsFlextMeltanoConstants", "c"]
