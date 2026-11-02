# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Meltano Utilities - Domain-specific Meltano utilities.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TypeAlias

from flext_cli import u as flext_cli_u

from flext_meltano._utilities.base import FlextMeltanoUtilitiesBase
from flext_meltano._utilities.runtime import FlextMeltanoUtilitiesRuntime
from flext_meltano._utilities.singer import FlextMeltanoUtilitiesSinger


class FlextMeltanoUtilities(flext_cli_u):
    """DOMAIN-SPECIFIC Meltano utilities.

    ONLY what cannot be generalized to flext-core.
    Inherits from FlextUtilities to avoid duplication and ensure consistency.
    """

    class Meltano(
        FlextMeltanoUtilitiesRuntime,
        FlextMeltanoUtilitiesSinger,
    ):
        """Meltano domain utility methods.

        Includes Singer protocol utilities (message emission, stdin
        processing, catalog construction) alongside settings, project,
        and YAML utilities.
        """

        FlextMeltanoUtilitiesBase: TypeAlias = FlextMeltanoUtilitiesBase


u = FlextMeltanoUtilities
__all__: list[str] = ["FlextMeltanoUtilities", "u"]
