"""Runtime settings for flext-meltano tests."""

from __future__ import annotations

from flext_tests.settings import FlextTestsSettings

from flext_meltano import FlextMeltanoSettings


class TestsFlextMeltanoSettings(FlextMeltanoSettings, FlextTestsSettings):
    """Meltano settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextMeltanoSettings"]
