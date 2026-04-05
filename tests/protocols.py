"""Test protocol definitions for flext-meltano.

Provides FlextMeltanoTestProtocols, combining FlextTestsProtocols with
FlextMeltanoProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol

from flext_tests import FlextTestsProtocols

from flext_meltano import FlextMeltanoProtocols, t


class FlextMeltanoTestProtocols(FlextTestsProtocols, FlextMeltanoProtocols):
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

            class CliRunner(Protocol):
                """Protocol for CLI runner interface used in tests."""

                def invoke(
                    self, *args: t.Scalar, **kwargs: t.Scalar
                ) -> FlextMeltanoTestProtocols.Meltano.Tests.MockCliResultLike:
                    """Invoke CLI command."""
                    ...

            class MockCliResultLike(Protocol):
                """Protocol for CLI result objects."""

                exit_code: int
                output: str


p = FlextMeltanoTestProtocols
__all__ = ["FlextMeltanoTestProtocols", "p"]
