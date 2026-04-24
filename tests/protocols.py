"""Test protocols facade via MRO composition."""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_meltano import FlextMeltanoProtocols


class TestsFlextMeltanoProtocols(FlextTestsProtocols, FlextMeltanoProtocols):
    """Test protocols facade for flext-meltano."""


p = TestsFlextMeltanoProtocols
__all__: list[str] = ["TestsFlextMeltanoProtocols", "p"]
