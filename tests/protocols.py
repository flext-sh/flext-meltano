"""Test protocols facade via MRO composition."""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_meltano import p


class TestsFlextMeltanoProtocols(FlextTestsProtocols, p):
    """Test protocols facade for flext-meltano."""

    class Meltano(p.Meltano):
        """Meltano test protocols namespace."""

        class Tests(FlextTestsProtocols.Tests):
            """Meltano-specific test protocols."""


p = TestsFlextMeltanoProtocols
__all__: list[str] = ["TestsFlextMeltanoProtocols", "p"]
