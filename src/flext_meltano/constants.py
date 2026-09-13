"""FLEXT Meltano constants."""

from __future__ import annotations

from flext_cli import c

from ._constants.base import FlextMeltanoConstantsBase
from ._constants.enums import FlextMeltanoConstantsEnums
from ._constants.settings import FlextMeltanoConstantsSettings


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
