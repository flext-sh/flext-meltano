"""Example constants for flext-meltano."""

from __future__ import annotations

from typing import Final

from flext_meltano import FlextMeltanoConstants


class ExamplesFlextMeltanoConstants(FlextMeltanoConstants):
    """Examples constants facade extending flext-meltano constants."""

    class Meltano(FlextMeltanoConstants.Meltano):
        """Meltano domain constants for examples."""

        class Examples:
            """Examples-only constants."""

            SAMPLE_DBT: Final[str] = "analytics"
            SAMPLE_TAP: Final[str] = "tap-csv"
            SAMPLE_TARGET: Final[str] = "target-jsonl"


c = ExamplesFlextMeltanoConstants

__all__: list[str] = ["ExamplesFlextMeltanoConstants", "c"]
