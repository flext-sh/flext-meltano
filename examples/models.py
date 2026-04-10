"""Example models for flext-meltano."""

from __future__ import annotations

from flext_meltano import FlextMeltanoModels


class ExamplesFlextMeltanoModels(FlextMeltanoModels):
    """Examples models facade extending flext-meltano models."""

    class Meltano(FlextMeltanoModels.Meltano):
        """Meltano domain models for examples."""

        class Examples:
            """Examples-only model namespace."""


m = ExamplesFlextMeltanoModels

__all__ = ["ExamplesFlextMeltanoModels", "m"]
