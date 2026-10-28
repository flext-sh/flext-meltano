# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Meltano Utilities - Domain-specific Meltano utilities.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_cli import u

from flext_meltano._utilities import (
    FlextMeltanoUtilitiesBase,
    FlextMeltanoUtilitiesRuntime,
    FlextMeltanoUtilitiesSinger,
)


class FlextMeltanoUtilities(u):
    """DOMAIN-SPECIFIC Meltano utilities.

    ONLY what cannot be generalized to flext-core.
    Inherits from FlextUtilities to avoid duplication and ensure consistency.
    """

    class Meltano(
        FlextMeltanoUtilitiesRuntime,
        FlextMeltanoUtilitiesSinger,
        FlextMeltanoUtilitiesBase,
    ):
        """Meltano domain utility methods.

        Includes Singer protocol utilities (message emission, stdin
        processing, catalog construction) alongside settings, project,
        and YAML utilities.
        """


u = FlextMeltanoUtilities
__all__: list[str] = ["FlextMeltanoUtilities", "u"]
