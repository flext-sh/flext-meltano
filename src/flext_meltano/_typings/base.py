"""FLEXT Meltano typings - Base type aliases and plugin types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import ClassVar

from flext_cli import t, u

from flext_meltano import c


class FlextMeltanoTypingsBase:
    """Base Meltano type aliases and plugin type definitions.

    All aliases are FLAT namespace with descriptive prefixes.
    No nested classes. No duplicates. No simple aliases to existing ``t.*``.
    """

    CONTAINER_MAP_ADAPTER: ClassVar[u.TypeAdapter[t.RecursiveContainerMapping]] = (
        u.TypeAdapter(t.RecursiveContainerMapping)
    )
    INTEGER_ADAPTER: ClassVar[u.TypeAdapter[t.IntegerValue]] = u.TypeAdapter(
        t.IntegerValue
    )

    type ValidatorInput = (
        t.RecursiveContainerMapping
        | Mapping[str, t.RecursiveContainerMapping | None]
        | Sequence[t.RecursiveContainerMapping | None]
        | tuple[t.RecursiveContainerMapping | None, ...]
        | set[t.RecursiveContainerMapping | None]
        | None
    )

    type PluginDefinition = Mapping[
        str,
        str | t.StrSequence | Mapping[str, t.Scalar | None],
    ]
    type PluginCatalog = Mapping[
        str,
        Sequence[FlextMeltanoTypingsBase.PluginDefinition],
    ]
    PluginType = c.Meltano.PluginType

    type VariantValue = str | t.StrSequence | t.ScalarMapping | None
    """Normalized plugin variant: string, string list, scalar mapping, or null."""

    type FileConfigDict = Mapping[
        str,
        t.RecursiveContainer | t.StrSequence,
    ]
    type PathDict = Mapping[str, str | Path]

    type OptionalScalarMap = Mapping[str, t.Scalar | None]

    type CliProcessResult = Mapping[str, t.Scalar | t.StrSequence]
