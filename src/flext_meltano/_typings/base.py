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

    CONTAINER_MAP_ADAPTER: ClassVar[u.TypeAdapter[Mapping[str, t.Container]]] = (
        u.TypeAdapter(Mapping[str, t.Container])
    )
    CONTAINER_MAP_LIST_ADAPTER: ClassVar[
        u.TypeAdapter[list[Mapping[str, t.Container]]]
    ] = u.TypeAdapter(list[Mapping[str, t.Container]])
    INTEGER_ADAPTER: ClassVar[u.TypeAdapter[t.IntegerValue]] = u.TypeAdapter(
        t.IntegerValue
    )

    type ValidatorInput = (
        Mapping[str, t.Container]
        | Mapping[str, Mapping[str, t.Container] | None]
        | Sequence[Mapping[str, t.Container] | None]
        | tuple[Mapping[str, t.Container] | None, ...]
        | set[Mapping[str, t.Container] | None]
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
        t.Container | t.StrSequence,
    ]
    type PathDict = Mapping[str, str | Path]

    type OptionalScalarMap = Mapping[str, t.Scalar | None]

    type CliProcessResult = Mapping[str, t.Scalar | t.StrSequence]
