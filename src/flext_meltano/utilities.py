"""FLEXT Meltano Utilities - Domain-specific Meltano utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import FlextCliUtilities

from flext_meltano._utilities import (
    FlextMeltanoUtilitiesConfig,
    FlextMeltanoUtilitiesProject,
    FlextMeltanoUtilitiesYaml,
)


class FlextMeltanoUtilities(FlextCliUtilities):
    """DOMAIN-SPECIFIC Meltano utilities.

    ONLY what cannot be generalized to flext-core.
    Inherits from FlextUtilities to avoid duplication and ensure consistency.
    """

    class Meltano(
        FlextMeltanoUtilitiesYaml,
        FlextMeltanoUtilitiesConfig,
        FlextMeltanoUtilitiesProject,
    ):
        """Plugin-related utility methods.

        NOTE: These methods were moved from constants.py to follow
        FLEXT pattern: constants contain ONLY pure constants, no methods.
        """


u = FlextMeltanoUtilities
__all__ = ["FlextMeltanoUtilities", "u"]
