"""Runtime settings for flext-meltano tests."""

from __future__ import annotations

from flext_meltano import FlextMeltanoSettings
from flext_tests import FlextTestsSettings


class TestsFlextMeltanoSettings(FlextMeltanoSettings, FlextTestsSettings):
    """Meltano settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextMeltanoSettings"]
