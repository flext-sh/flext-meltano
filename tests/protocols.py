"""Test protocols facade via MRO composition.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from tests import FlextMeltanoProtocols


class TestsFlextMeltanoProtocols(FlextTestsProtocols, FlextMeltanoProtocols):
    """Test protocols facade for flext-meltano."""

    class Tests(FlextTestsProtocols.Tests):
        """Meltano-specific test protocols."""


p = TestsFlextMeltanoProtocols
__all__: list[str] = ["TestsFlextMeltanoProtocols", "p"]
