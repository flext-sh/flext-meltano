"""Test protocol definitions for flext-meltano.

Provides TestsFlextMeltanoProtocols, combining FlextTestsProtocols with
FlextMeltanoProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano.protocols import FlextMeltanoProtocols
from flext_tests.protocols import FlextTestsProtocols


class TestsFlextMeltanoProtocols(FlextTestsProtocols, FlextMeltanoProtocols):
    """Test protocols combining FlextTestsProtocols and FlextMeltanoProtocols.

    Provides access to:
    - tp.Tests.Docker.* (from FlextTestsProtocols)
    - tp.Tests.Factory.* (from FlextTestsProtocols)
    - tp.Meltano.* (from FlextMeltanoProtocols)
    """

    class Tests:
        """Project-specific test protocols.

        Extends FlextTestsProtocols.Tests with Meltano-specific protocols.
        """

        class Meltano:
            """Meltano-specific test protocols."""


# Runtime aliases
p = TestsFlextMeltanoProtocols
tp = TestsFlextMeltanoProtocols

__all__ = ["TestsFlextMeltanoProtocols", "p", "tp"]
