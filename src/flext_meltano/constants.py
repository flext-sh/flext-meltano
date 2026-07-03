"""FLEXT Meltano constants."""

from __future__ import annotations

from flext_cli import c
from flext_meltano._constants.base import FlextMeltanoConstantsBase
from flext_meltano._constants.enums import FlextMeltanoConstantsEnums
from flext_meltano._constants.settings import FlextMeltanoConstantsSettings


class FlextMeltanoConstants(c):
    """Domain constants for the flext-meltano package."""

    class Meltano(
        FlextMeltanoConstantsBase,
        FlextMeltanoConstantsEnums,
        FlextMeltanoConstantsSettings,
    ):
        """Meltano domain constants namespace."""


c = FlextMeltanoConstants

__all__: list[str] = ["FlextMeltanoConstants", "c"]
