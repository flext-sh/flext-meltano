"""FLEXT Meltano typings - Base type aliases and plugin types.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import t


class FlextMeltanoTypingsBase:
    """Base Meltano type aliases and plugin type definitions.

    All aliases are FLAT namespace with descriptive prefixes.
    No nested classes. No duplicates. No simple aliases to existing ``t.*``.
    """

    type ValidatorInput = t.JsonValue

    type NormalizedValue = t.Scalar
    """Canonical scalar value after normalization (string, number, boolean, or null)."""

    type MutableContainerValueMapping = t.MutableFlatContainerMapping
    """Mutable container bridge for Singer SDK record/context mappings."""


__all__: list[str] = ["FlextMeltanoTypingsBase"]
