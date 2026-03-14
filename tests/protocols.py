"""Test protocol definitions for flext-meltano.

Provides TestsFlextMeltanoProtocols, combining FlextTestsProtocols with
FlextMeltanoProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_meltano import FlextMeltanoProtocols


class TestsFlextMeltanoProtocols(FlextTestsProtocols, FlextMeltanoProtocols):
    """Test protocols combining FlextTestsProtocols and FlextMeltanoProtocols.

    Provides access to:
    - p.Tests.Docker.* (from FlextTestsProtocols)
    - p.Tests.Factory.* (from FlextTestsProtocols)
    - p.Meltano.* (from FlextMeltanoProtocols)
    """

    class Meltano(FlextMeltanoProtocols.Meltano):
        """Meltano-specific test protocols."""

        class Tests:
            """Project-specific test protocols.

            Extends FlextTestsProtocols.Tests with Meltano-specific protocols.
            """


p = TestsFlextMeltanoProtocols
__all__ = ["TestsFlextMeltanoProtocols", "p"]
