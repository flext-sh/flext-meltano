"""FLEXT Meltano typings - Base type aliases and plugin types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import ClassVar

from flext_cli import m, t

from flext_meltano import c


class FlextMeltanoTypingsBase:
    """Base Meltano type aliases and plugin type definitions.

    All aliases are FLAT namespace with descriptive prefixes.
    No nested classes. No duplicates. No simple aliases to existing ``t.*``.
    """

    CONTAINER_MAP_ADAPTER: ClassVar[m.TypeAdapter[t.FlatContainerMapping]] = (
        m.TypeAdapter(t.FlatContainerMapping)
    )

    type ValidatorInput = t.JsonValue

    PluginType = c.Meltano.PluginType

    type VariantValue = str | t.StrSequence | t.ScalarMapping | None
    """Normalized plugin variant: string, string list, scalar mapping, or null."""

    type NormalizedValue = t.Scalar
    """Canonical scalar value after normalization (string, number, boolean, or null)."""

    type PathDict = Mapping[str, str | Path]

    type OptionalScalarMap = Mapping[str, t.Scalar | None]

    type ServicePayload = t.JsonMapping
    """Canonical payload returned by Meltano service operations."""

    type EnvironmentInput = c.Meltano.Environment | t.JsonMapping
    """Environment selector input: a named environment or a full environment configuration mapping."""

    type MutableContainerValueMapping = t.MutableFlatContainerMapping
    """Mutable container bridge for Singer SDK record/context mappings."""
