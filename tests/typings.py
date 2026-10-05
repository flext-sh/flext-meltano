"""Test type aliases for flext-meltano.

Provides TestsFlextMeltanoTypes, combining TestsFlextTypes with
t for test-specific type aliases.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from flext_tests import FlextTestsTypes

from flext_meltano import FlextMeltanoTypes


class TestsFlextMeltanoTypes(FlextTestsTypes, FlextMeltanoTypes):
    """Test type aliases for flext-meltano."""

    class Meltano(FlextMeltanoTypes.Meltano):
        """Meltano test types namespace."""

        type ComponentCase = tuple[str, str, str]
        """One canonical component-factory case: kind, name, selector field."""

        type ProjectEnv = Mapping[str, str | Path | t.JsonMapping]
        """Environment mapping exported for one test Meltano project."""

        class Tests(FlextTestsTypes.Tests):
            """Meltano-specific test type aliases."""


t = TestsFlextMeltanoTypes
__all__: list[str] = ["TestsFlextMeltanoTypes", "t"]
