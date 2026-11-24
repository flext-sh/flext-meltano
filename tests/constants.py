"""Constants for flext-meltano tests.

Provides TestsFlextMeltanoConstants, composing FlextTestsConstants and
FlextMeltanoConstants by MRO.

Inheritance hierarchy:
- FlextTestsConstants (flext_tests) - Provides the flat .Tests.* namespace
- FlextMeltanoConstants (flext_meltano) - Provides .Meltano.* production constants

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import StrEnum, unique
from pathlib import Path
from types import MappingProxyType
from typing import ClassVar

from flext_tests import FlextTestsConstants

from tests import FlextMeltanoConstants


class TestsFlextMeltanoConstants(FlextTestsConstants, FlextMeltanoConstants):
    """Constants for flext-meltano tests, composed by MRO.

    MANDATORY: Inherits FlextTestsConstants for test infrastructure (.Tests.*)
    and FlextMeltanoConstants for the production namespace (.Meltano.*).

    Access patterns:
    - c.Tests.* (container testing)
    - c.Tests.* (assertion messages)
    - c.Tests.Factory.* (test data generation)
    - c.Meltano.* (domain constants from production)

    Rules:
    - NEVER duplicate constants from FlextTestsConstants or c
    - Only flext-meltano-specific test constants allowed (not generic for
    other projects)
    - All generic constants come from FlextTestsConstants
    - All production constants come from c
    """

    class Tests(FlextTestsConstants.Tests):
        """Meltano tests namespace."""

        @unique
        class _DockerService(StrEnum):
            """Docker service identifiers used by the local test stack."""

            POSTGRES = "postgres"
            REDIS = "redis"
            MELTANO = "meltano"

        HOST: ClassVar[str] = FlextMeltanoConstants.LOCALHOST
        SERVICE_PORTS: ClassVar[Mapping[_DockerService, int]] = MappingProxyType({
            _DockerService.POSTGRES: 5433,
            _DockerService.REDIS: 6380,
            _DockerService.MELTANO: 3000,
        })
        POSTGRES_PORT: ClassVar[int] = SERVICE_PORTS[_DockerService.POSTGRES]
        REDIS_PORT: ClassVar[int] = SERVICE_PORTS[_DockerService.REDIS]
        MELTANO_PORT: ClassVar[int] = SERVICE_PORTS[_DockerService.MELTANO]
        COMPOSE_FILE: ClassVar[str] = "docker-compose.test.yml"
        PRIMARY_SERVICE: ClassVar[str] = _DockerService.MELTANO
        PRIMARY_CONTAINER_NAME: ClassVar[str] = "flext-test-meltano"
        FIXTURES_DATA_DIR: ClassVar[Path] = Path("tests/fixtures/data")
        TEST_INPUT_DIR: ClassVar[str] = (FIXTURES_DATA_DIR / "input").as_posix()
        TEST_OUTPUT_DIR: ClassVar[str] = (FIXTURES_DATA_DIR / "output").as_posix()
        TEST_TEMP_PREFIX: ClassVar[str] = "flext_meltano_test_"

        # Test service credentials (mirror docker-compose.test.yml)
        POSTGRES_TEST_DATABASE: ClassVar[str] = "flext_test"
        POSTGRES_TEST_USER: ClassVar[str] = "test"
        POSTGRES_TEST_VALUE: ClassVar[str] = "test"

        @unique
        class _SingerSdkAdapterValue(StrEnum):
            """Deterministic values for Singer SDK adapter tests."""

            SETTINGS_KEY = "tap"
            SETTINGS_VALUE = "ok"
            STREAM_USERS = "users"
            SUCCESS_COMMAND = "tap-ok"
            FAILURE_COMMAND = "tap-fail"

        SINGER_SDK_ADAPTER_SETTINGS: ClassVar[Mapping[str, str]] = MappingProxyType({
            _SingerSdkAdapterValue.SETTINGS_KEY: (
                _SingerSdkAdapterValue.SETTINGS_VALUE
            ),
        })
        SINGER_SDK_ADAPTER_STREAM_USERS: ClassVar[str] = (
            _SingerSdkAdapterValue.STREAM_USERS
        )
        SINGER_SDK_ADAPTER_SUCCESS_COMMAND: ClassVar[str] = (
            _SingerSdkAdapterValue.SUCCESS_COMMAND
        )
        SINGER_SDK_ADAPTER_FAILURE_COMMAND: ClassVar[str] = (
            _SingerSdkAdapterValue.FAILURE_COMMAND
        )
        SINGER_SDK_ADAPTER_FAILURE_EXIT_CODE: ClassVar[int] = 3


c = TestsFlextMeltanoConstants
__all__: list[str] = ["TestsFlextMeltanoConstants", "c"]
