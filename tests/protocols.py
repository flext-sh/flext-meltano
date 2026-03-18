"""Test protocol definitions for flext-meltano.

Provides TestsFlextMeltanoProtocols, combining p with
FlextMeltanoProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import p

from flext_meltano import FlextMeltanoProtocols


class TestsFlextMeltanoProtocols(p, FlextMeltanoProtocols):
    """Test protocols combining p and FlextMeltanoProtocols.

    Provides access to:
    - p.Tests.Docker.* (from p)
    - p.Tests.Factory.* (from p)
    - p.Meltano.* (from FlextMeltanoProtocols)
    """

    class Meltano(FlextMeltanoProtocols.Meltano):
        """Meltano-specific test protocols."""

        class Tests:
            """Project-specific test protocols.

            Extends p.Tests with Meltano-specific protocols.
            """


p = TestsFlextMeltanoProtocols
__all__ = ["TestsFlextMeltanoProtocols", "p"]
