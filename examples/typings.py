"""Example typings for flext-meltano."""

from __future__ import annotations

from flext_meltano import FlextMeltanoTypes


class ExamplesFlextMeltanoTypes(FlextMeltanoTypes):
    """Examples types facade extending flext-meltano types."""

    class Meltano(FlextMeltanoTypes.Meltano):
        """Meltano domain types for examples."""

        class Examples:
            """Examples-only type namespace."""


t = ExamplesFlextMeltanoTypes

__all__ = ["ExamplesFlextMeltanoTypes", "t"]
