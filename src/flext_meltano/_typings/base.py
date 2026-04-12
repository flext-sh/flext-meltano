"""FLEXT Meltano typings - Base type aliases and plugin types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import ClassVar

from flext_cli import t

from flext_meltano import c


class FlextMeltanoTypingsBase:
    """Base Meltano type aliases and plugin type definitions.

    All aliases are FLAT namespace with descriptive prefixes.
    No nested classes. No duplicates. No simple aliases to existing ``t.*``.
    """

    CONTAINER_MAP_ADAPTER: ClassVar[c.TypeAdapter[t.ContainerMapping]] = c.TypeAdapter(
        t.ContainerMapping
    )
    INTEGER_ADAPTER: ClassVar[c.TypeAdapter[t.IntegerValue]] = c.TypeAdapter(
        t.IntegerValue
    )

    type ValidatorInput = (
        t.ContainerMapping
        | Mapping[str, t.ContainerMapping | None]
        | Sequence[t.ContainerMapping | None]
        | tuple[t.ContainerMapping | None, ...]
        | set[t.ContainerMapping | None]
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
        t.NormalizedValue | t.StrSequence,
    ]
    type PathDict = Mapping[str, str | Path]

    type OptionalScalarMap = Mapping[str, t.Scalar | None]

    type CliProcessResult = Mapping[str, t.Scalar | t.StrSequence]
