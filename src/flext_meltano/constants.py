# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Meltano constants.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TypeAlias

from flext_cli import c as flext_cli_c

from flext_meltano._constants.base import FlextMeltanoConstantsBase
from flext_meltano._constants.enums import FlextMeltanoConstantsEnums
from flext_meltano._constants.settings import FlextMeltanoConstantsSettings


class FlextMeltanoConstants(
    flext_cli_c,
    FlextMeltanoConstantsBase,
    FlextMeltanoConstantsEnums,
):
    """Domain constants for the flext-meltano package."""

    class Meltano(
        FlextMeltanoConstantsBase,
        FlextMeltanoConstantsEnums,
        FlextMeltanoConstantsSettings,
    ):
        """Meltano domain constants namespace."""

    FlextMeltanoConstantsSettings: TypeAlias = FlextMeltanoConstantsSettings


c = FlextMeltanoConstants

__all__: list[str] = ["FlextMeltanoConstants", "c"]
