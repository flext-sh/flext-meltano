"""FLEXT Meltano typings - Base type aliases and plugin types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import ClassVar

from flext_cli import FlextCliTypes
from pydantic import TypeAdapter

from flext_meltano import c


class FlextMeltanoTypingsBase:
    """Base Meltano type aliases and plugin type definitions.

    All aliases are FLAT namespace with descriptive prefixes.
    No nested classes. No duplicates. No simple aliases to existing ``t.*``.
    """

    CONTAINER_MAP_ADAPTER: ClassVar[TypeAdapter[FlextCliTypes.ContainerMapping]] = (
        TypeAdapter(FlextCliTypes.ContainerMapping)
    )
    INTEGER_ADAPTER: ClassVar[TypeAdapter[FlextCliTypes.IntegerValue]] = TypeAdapter(
        FlextCliTypes.IntegerValue
    )

    type ValidatorInput = (
        FlextCliTypes.ContainerMapping
        | Mapping[str, FlextCliTypes.ContainerMapping | None]
        | Sequence[FlextCliTypes.ContainerMapping | None]
        | tuple[FlextCliTypes.ContainerMapping | None, ...]
        | set[FlextCliTypes.ContainerMapping | None]
        | None
    )

    type PluginDefinition = Mapping[
        str,
        str | FlextCliTypes.StrSequence | Mapping[str, FlextCliTypes.Scalar | None],
    ]
    type PluginCatalog = Mapping[
        str,
        Sequence[FlextMeltanoTypingsBase.PluginDefinition],
    ]
    PluginType = c.Meltano.PluginType

    type VariantValue = (
        str | FlextCliTypes.StrSequence | FlextCliTypes.ScalarMapping | None
    )
    """Normalized plugin variant: string, string list, scalar mapping, or null."""

    type FileConfigDict = Mapping[
        str,
        FlextCliTypes.NormalizedValue | FlextCliTypes.StrSequence,
    ]
    PathDict = Mapping[str, str | Path]

    type OptionalScalarMap = Mapping[str, FlextCliTypes.Scalar | None]

    type CliProcessResult = Mapping[
        str, FlextCliTypes.Scalar | FlextCliTypes.StrSequence
    ]
