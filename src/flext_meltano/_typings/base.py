"""FLEXT Meltano typings - Base type aliases and plugin types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from pathlib import Path

from flext_cli import t

from flext_meltano import c


class FlextMeltanoTypingsBase:
    """Base Meltano type aliases and plugin type definitions.

    All aliases are FLAT namespace with descriptive prefixes.
    No nested classes. No duplicates. No simple aliases to existing ``t.*``.
    """

    JsonValue = t.JsonValue
    type JsonMapping = t.JsonMapping
    type JsonMappingList = Sequence[t.JsonMapping]
    type ValidatorInput = t.JsonValue | t.RuntimeData | None

    type PluginDefinition = t.JsonMapping
    type PluginCatalog = Mapping[
        str, Sequence[FlextMeltanoTypingsBase.PluginDefinition]
    ]
    PluginType = c.Meltano.PluginType

    type VariantValue = str | t.StrSequence | t.JsonMapping | None
    """Normalized plugin variant: string, string list, scalar mapping, or null."""

    type FileConfigDict = t.JsonMapping
    type PathDict = Mapping[str, str | Path]

    type OptionalScalarMap = Mapping[str, t.Scalar | None]

    type CliProcessResult = t.JsonMapping
