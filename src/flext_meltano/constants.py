# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Meltano constants.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliConstants

from flext_meltano._constants import (
    FlextMeltanoConstantsBase,
    FlextMeltanoConstantsEnums,
    FlextMeltanoConstantsSettings,
)


class FlextMeltanoConstants(
    FlextCliConstants,
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


c = FlextMeltanoConstants

__all__: list[str] = ["FlextMeltanoConstants", "c"]
