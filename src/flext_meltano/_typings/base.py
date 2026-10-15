"""FLEXT Meltano typings - Base type aliases and plugin types.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from flext_cli import t


class FlextMeltanoTypingsBase:
    """Base Meltano type aliases and plugin type definitions.

    All aliases are FLAT namespace with descriptive prefixes.
    No nested classes. No duplicates. No simple aliases to existing ``t.*``.
    """

    type ValidatorInput = t.JsonValue

    type VariantValue = str | t.StrSequence | t.ScalarMapping | None
    """Normalized plugin variant: string, string list, scalar mapping, or null."""

    type NormalizedValue = t.Scalar
    """Canonical scalar value after normalization (string, number, boolean, or null)."""

    type PathDict = Mapping[str, str | Path]

    type OptionalScalarMap = Mapping[str, t.Scalar | None]

    type ServicePayload = t.JsonMapping
    """Canonical payload returned by Meltano service operations."""

    type MutableContainerValueMapping = t.MutableFlatContainerMapping
    """Mutable container bridge for Singer SDK record/context mappings."""
