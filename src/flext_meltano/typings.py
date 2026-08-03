"""FLEXT Meltano Types - Domain-specific Meltano type definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import t

from flext_meltano._typings.base import FlextMeltanoTypingsBase
from flext_meltano._typings.domains import FlextMeltanoTypingsDomains
from flext_meltano._typings.singer import FlextMeltanoTypingsSinger


class FlextMeltanoTypes(t):
    """Meltano-specific type definitions extending t.

    Domain-specific type system for Meltano data integration operations.
    Contains ONLY complex Meltano-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    class Meltano(
        FlextMeltanoTypingsBase, FlextMeltanoTypingsSinger, FlextMeltanoTypingsDomains
    ):
        """Meltano plugin complex types namespace."""


t = FlextMeltanoTypes
__all__ = ["FlextMeltanoTypes", "t"]
