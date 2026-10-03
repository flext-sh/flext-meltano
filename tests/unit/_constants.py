"""Constants for tests.unit._constants.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar


class TestsFlextMeltanoConstants:
    """Canonical namespace owner."""

    TEST_EXECUTION_TIME_SUCCESS: ClassVar[float] = 1.5

    TEST_EXECUTION_TIME_FAILURE: ClassVar[float] = 0.5

    TEST_EXECUTION_TIME_DICT_SUCCESS: ClassVar[float] = 0.2

    TEST_EXECUTION_TIME_DICT_FAILURE: ClassVar[float] = 0.1

    TEST_EXECUTION_TIME_JSON_SUCCESS: ClassVar[float] = 2.0

    TEST_EXECUTION_TIME_JSON_FAILURE: ClassVar[float] = 0.3

    TEST_EXECUTION_TIME_JSON_ERROR: ClassVar[float] = 5.5

    TEST_EXECUTION_TIME_HOUR: ClassVar[float] = 3600.5

    TEST_COMMAND_COUNT: ClassVar[int] = 2
